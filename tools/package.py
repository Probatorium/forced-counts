#!/usr/bin/env python3
"""
El paquete: la cadena entera, tal y como la encontrara un extrano.

Todo lo que este repositorio afirma se apoya en que un tercero pueda repetirlo.
Eso no se comprueba mirando el directorio de trabajo, donde llevan meses
acumulandose ficheros, variables de entorno y suerte. Se comprueba clonando en
un sitio limpio y corriendolo todo desde cero. Eso hace este programa.

  FASE 1  clon limpio y cadena completa. Se clona el repositorio en un
          directorio nuevo y se corren todos los programas de analisis en orden
          declarado. Cada fichero de results que producen se coteja BYTE A BYTE
          contra el que esta commiteado. Un programa que no reproduce su propia
          salida no es reproducible, por mucho que corra sin error.
  FASE 2  los comprobadores, en el clon: ensamblado, congelador de cifras,
          mutaciones, constructor de tex y pdf, puente del pdf, y la cadena del
          registro de esfuerzo.
  FASE 3  la historia en una linea por commit.
  FASE 4  ausencia de secretos, sobre TODOS los blobs de la historia y no solo
          sobre el arbol de ahora, que es donde se esconden.
  FASE 5  los ficheros de terceros y el bundle. Lo que no es nuestro se filtra
          de la historia empaquetada y se declara en un manifiesto con su
          identidad, su sha256 y donde se consigue.

  python tools/package.py [--rapido]

--rapido salta la fase 1, que es la cara. Se usa para iterar sobre el resto; el
paquete de verdad no se declara bueno sin ella, y el informe dice cual de las
dos corridas fue.

Salidas: results/package.tsv, dist/HISTORY.txt, dist/THIRD-PARTY.md,
dist/forced-counts.bundle
"""

import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(ROOT, "results", "package.tsv")

ROWS = []
FALLOS = []

CRLF = b"\r\n"
LF = b"\n"

# Los programas de analisis, en el orden en que se corren. El orden importa
# porque algunos leen lo que otros dejan.
CADENA = [
    "src/measure.py",
    "src/group.py",
    "src/proofs.py",
    "src/gray.py",
    "src/transitions.py",
    "src/corroborate.py",
    "src/parity_hypotheses.py",
    "src/general_landscape.py",
    "src/general_n6.py",
    "src/general_theorems.py",
    "src/b31_characterization.py",
    "src/hall_search.py",
    "src/residuo5.py",
]

COMPROBADORES = [
    "src/assemble_paper.py",
    "src/declared_values.py",
    "src/build_paper.py",
    "src/pdf_bridge.py",
]

# Ficheros que no son nuestros. Cada uno con lo que hay que saber para
# conseguirlo por su cuenta, que es lo que sustituye al fichero en el paquete.
TERCEROS = [
    ("data/sequences.json",
     "Las tres secuencias, extraidas del paquete de replicacion "
     "kingwen-orderings-replication en la etiqueta zenodo-v3, commit "
     "d6afae20bbefba56728251f34f8e3870c43e2cbd.",
     "Se obtiene clonando ese repositorio en esa etiqueta y corriendo "
     "tools/extract_sequences.py, que esta aqui y no se filtra."),
    ("artifacts/radisic-2601.07175v3-appendix-A.tsv",
     "Transcripcion del apendice A de Alejandro Radisic, Optimal Equivariant "
     "Matchings on the 6-Cube, arXiv:2601.07175v3, pagina 11.",
     "Se obtiene descargando ese articulo de arXiv y transcribiendo su "
     "apendice A. Aqui solo se usa como objeto de comparacion, nunca como "
     "fuente de ningun computo."),
]

# Lineas que NO pueden reproducirse, porque no miden el objeto de estudio sino
# la maquina. Se declaran una por una, con su motivo, y el informe dice cuantas
# se han excluido: una exclusion sin nombre seria una manera elegante de que
# nada fallara nunca.
NO_DETERMINISTAS = [
    ("hall-search.tsv", "segundos.totales",
     "reloj de pared de la busqueda; mide esta maquina y no el resultado"),
]

# Patrones de secreto. Cada uno con su nombre, para que un aviso diga que se ha
# encontrado y no solo que se ha encontrado algo.
SECRETOS = [
    ("clave.privada", rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("token.de.github", rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    ("clave.de.aws", rb"AKIA[0-9A-Z]{16}"),
    ("token.genericos", rb"(?i)(api[_-]?key|secret|password|passwd|token)"
                       rb"\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    ("cabecera.de.autorizacion", rb"(?i)authorization:\s*(bearer|basic)\s+\S{16,}"),
    ("url.con.credenciales", rb"https?://[^/\s:@]+:[^/\s@]+@"),
]


def emit(k, v, n=""):
    ROWS.append((k, str(v), n))


def check(k, cond, n=""):
    emit(k, int(bool(cond)), n)
    if not cond:
        FALLOS.append(k + ("  " + n if n else ""))


def corre(args, cwd, timeout=1800):
    t0 = time.time()
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout)
    return r.returncode, time.time() - t0, (r.stdout + r.stderr)[-400:]


def borra_arbol(ruta):
    """Borra un arbol de git en Windows, donde los objetos son de solo lectura.

    shutil.rmtree con ignore_errors se los salta en silencio y deja el
    directorio a medias, y el clon siguiente falla diciendo que ya existe. Aqui
    se les quita el atributo y se vuelve a intentar.
    """
    if not os.path.exists(ruta):
        return
    def insiste(func, path, _exc):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass
    shutil.rmtree(ruta, onerror=insiste)


def sha(ruta):
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()


def sha_normalizado(ruta, fichero=None):
    """sha256 del contenido, con el fin de linea en unix y sin las lineas que
    estan declaradas no deterministas para ese fichero."""
    datos = open(ruta, "rb").read().replace(CRLF, LF)
    claves = [k for f, k, _ in NO_DETERMINISTAS if f == fichero]
    if claves:
        lineas = [l for l in datos.split(LF)
                  if l.split(b"	")[0].decode("utf-8", "replace") not in claves]
        datos = LF.join(lineas)
    return hashlib.sha256(datos).hexdigest()


# --- fase 1 y 2: el clon limpio ---------------------------------------------

def clon_limpio(destino, rapido):
    borra_arbol(destino)
    rc, seg, sal = corre(["git", "clone", "-q", ROOT, destino], ROOT)
    check("el.clon.se.hace", rc == 0, sal)
    if rc:
        return
    emit("clon.segundos", round(seg, 1))

    # los ficheros de results tal y como estan commiteados
    dir_res = os.path.join(destino, "results")
    # Se compara el CONTENIDO, con el fin de linea normalizado. Lo que se
    # pregunta es si el programa reproduce su salida, no con que convencion la
    # dejo el sistema de ficheros de turno.
    antes = {f: sha_normalizado(os.path.join(dir_res, f), f)
             for f in sorted(os.listdir(dir_res)) if f.endswith(".tsv")}
    emit("lineas.excluidas.por.no.deterministas", len(NO_DETERMINISTAS),
         "; ".join("%s %s: %s" % (f, k, m) for f, k, m in NO_DETERMINISTAS))
    emit("ficheros.de.results.commiteados", len(antes))

    # que el clon reciba los ficheros byte a byte como estan aqui: es donde se
    # cazan las conversiones de fin de linea que corrompen un binario
    iguales = 0
    for rel in ("paper/PAPER.pdf", "paper/PAPER.tex", "paper/PAPER.md"):
        a, b = os.path.join(ROOT, rel), os.path.join(destino, rel)
        if os.path.exists(a) and os.path.exists(b):
            mismo = open(a, "rb").read() == open(b, "rb").read()
            check("el.clon.recibe.intacto.%s" % os.path.basename(rel), mismo,
                  "git ha alterado el fichero al sacarlo, mira .gitattributes")
            if not mismo:
                emit("bytes.aqui.%s" % os.path.basename(rel),
                     os.path.getsize(a))
                emit("bytes.en.el.clon.%s" % os.path.basename(rel),
                     os.path.getsize(b))
            iguales += int(mismo)
    emit("ficheros.comparados.contra.el.clon", iguales)

    if rapido:
        emit("fase1.cadena.de.analisis", "SALTADA", "corrida con --rapido")
    else:
        fallan, cambian, total_seg = [], [], 0.0
        for prog in CADENA:
            rc, seg, sal = corre([sys.executable, prog], destino)
            total_seg += seg
            emit("cadena.%s.segundos" % os.path.basename(prog), round(seg, 1))
            if rc != 0:
                fallan.append("%s: %s" % (prog, sal.strip()[-160:]))
        emit("cadena.segundos.totales", round(total_seg, 1))
        check("todos.los.programas.de.analisis.corren", not fallan,
              " | ".join(fallan))

        for f, h in antes.items():
            ruta = os.path.join(dir_res, f)
            if not os.path.exists(ruta):
                cambian.append(f + " (desaparecido)")
            elif sha_normalizado(ruta, f) != h:
                cambian.append(f)
        emit("ficheros.de.results.que.cambian.al.rehacerlos",
             " ".join(cambian) if cambian else "ninguno")
        check("la.cadena.reproduce.sus.propias.salidas", not cambian,
              "un programa que no reproduce su salida no es reproducible")

    fallan_c = []
    for prog in COMPROBADORES:
        rc, seg, sal = corre([sys.executable, prog], destino)
        emit("comprobador.%s" % os.path.basename(prog),
             "pasa" if rc == 0 else "FALLA")
        if rc != 0:
            fallan_c.append("%s: %s" % (prog, sal.strip()[-200:]))
    rc, _, sal = corre([sys.executable, "src/declared_values.py", "--mutacion"],
                       destino)
    emit("comprobador.mutaciones", "pasa" if rc == 0 else "FALLA")
    if rc:
        fallan_c.append("mutaciones: " + sal.strip()[-200:])
    rc, _, sal = corre([sys.executable, "src/pdf_bridge.py", "--prueba"], destino)
    emit("comprobador.prueba.del.puente", "pasa" if rc == 0 else "FALLA")
    if rc:
        fallan_c.append("puente: " + sal.strip()[-200:])
    rc, _, sal = corre([sys.executable, "tools/effort.py", "verify"], destino)
    emit("comprobador.cadena.del.registro", "pasa" if rc == 0 else "FALLA")
    if rc:
        fallan_c.append("effort verify: " + sal.strip()[-200:])

    check("todos.los.comprobadores.pasan.en.el.clon", not fallan_c,
          " | ".join(fallan_c))


# --- fase 3: la historia -----------------------------------------------------

def historia():
    r = subprocess.run(["git", "-C", ROOT, "log", "--oneline", "--no-decorate"],
                       capture_output=True, text=True)
    lineas = [l for l in r.stdout.split("\n") if l.strip()]
    os.makedirs(DIST, exist_ok=True)
    with open(os.path.join(DIST, "HISTORY.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("# La historia de forced-counts, una linea por commit, del mas\n")
        fh.write("# reciente al mas antiguo. El commit raiz es la preinscripcion.\n\n")
        fh.write("\n".join(lineas) + "\n")
    emit("commits.en.la.historia", len(lineas))
    check("la.historia.tiene.commits", len(lineas) > 0)
    return lineas


# --- fase 4: secretos --------------------------------------------------------

def blobs_de_la_historia():
    r = subprocess.run(["git", "-C", ROOT, "rev-list", "--objects", "--all"],
                       capture_output=True, text=True)
    out = []
    for linea in r.stdout.split("\n"):
        partes = linea.split(" ", 1)
        if len(partes) == 2 and partes[1].strip():
            out.append((partes[0], partes[1]))
    return out


def sin_secretos():
    objetos = blobs_de_la_historia()
    emit("objetos.de.la.historia.revisados", len(objetos))
    hallazgos = []
    for oid, ruta in objetos:
        r = subprocess.run(["git", "-C", ROOT, "cat-file", "-p", oid],
                           capture_output=True)
        if r.returncode != 0:
            continue
        datos = r.stdout
        for nombre, patron in SECRETOS:
            if re.search(patron, datos):
                hallazgos.append("%s en %s (%s)" % (nombre, ruta, oid[:8]))
    emit("hallazgos.de.secreto",
         " | ".join(hallazgos) if hallazgos else "ninguno")
    check("ningun.secreto.en.la.historia", not hallazgos)
    check("la.busqueda.de.secretos.no.pasa.en.vacio",
          len(objetos) > 0 and len(SECRETOS) > 0,
          "buscar cero patrones en cero objetos daria verde sin mirar nada")


# --- fase 5: terceros y bundle -----------------------------------------------

def manifiesto_y_bundle(tmp):
    presentes = [(p, d, c) for p, d, c in TERCEROS
                 if os.path.exists(os.path.join(ROOT, p))]
    emit("ficheros.de.terceros.en.el.arbol", len(presentes))

    lineas = ["# Ficheros de terceros, y que se ha hecho con ellos", "",
              "Este repositorio contiene material que no se escribio aqui. En el",
              "bundle de la historia ese material **se filtra**, y en su lugar queda",
              "esta ficha con lo necesario para conseguirlo por cuenta propia. Los",
              "programas que lo consumen siguen en el paquete, de modo que la cadena",
              "se puede rehacer entera en cuanto el material se repone.", ""]
    for p, desc, como in presentes:
        ruta = os.path.join(ROOT, p)
        lineas += [
            "## `%s`" % p, "",
            "- **Que es:** %s" % desc,
            "- **sha256:** `%s`" % sha(ruta),
            "- **Bytes:** %d" % os.path.getsize(ruta),
            "- **Como se consigue:** %s" % como,
            "- **Estado en el bundle:** filtrado de toda la historia.", "",
        ]
    if not presentes:
        lineas += ["No hay ninguno. Nada se filtra, y el bundle es la historia",
                   "completa sin quitar una sola linea.", ""]
    os.makedirs(DIST, exist_ok=True)
    with open(os.path.join(DIST, "THIRD-PARTY.md"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("\n".join(lineas))

    # el bundle se construye en un clon aparte, para no tocar esta historia
    filtrado = os.path.join(tmp, "filtrado")
    borra_arbol(filtrado)
    rc, _, sal = corre(["git", "clone", "-q", "--no-local", ROOT, filtrado], ROOT)
    check("el.clon.para.filtrar.se.hace", rc == 0, sal)
    if rc:
        return

    if presentes:
        entorno = dict(os.environ, FILTER_BRANCH_SQUELCH_WARNING="1")
        borra = " ".join("'%s'" % p for p, _, _ in presentes)
        r = subprocess.run(
            ["git", "filter-branch", "--force", "--index-filter",
             "git rm --cached --ignore-unmatch " + borra,
             "--prune-empty", "--", "--all"],
            cwd=filtrado, capture_output=True, text=True, env=entorno,
            timeout=1800)
        check("el.filtrado.corre", r.returncode == 0,
              (r.stdout + r.stderr)[-300:])

        # filter-branch guarda la historia vieja en refs/original, y un bundle
        # hecho con --all se la lleva entera: el fichero filtrado seguiria
        # viajando dentro del paquete, alcanzable con un solo comando. Hay que
        # borrar esas referencias, caducar el reflog y podar antes de empaquetar.
        r = subprocess.run(["git", "for-each-ref", "--format=%(refname)",
                            "refs/original"], cwd=filtrado,
                           capture_output=True, text=True)
        viejas = [x for x in r.stdout.split("\n") if x.strip()]
        emit("referencias.originales.borradas", len(viejas))
        for ref in viejas:
            subprocess.run(["git", "update-ref", "-d", ref], cwd=filtrado,
                           capture_output=True)
        subprocess.run(["git", "reflog", "expire", "--expire=now", "--all"],
                       cwd=filtrado, capture_output=True)
        subprocess.run(["git", "gc", "--prune=now", "--quiet"],
                       cwd=filtrado, capture_output=True, timeout=1800)

        # y se comprueba que de verdad no queda rastro en NINGUN commit
        r = subprocess.run(["git", "rev-list", "--objects", "--all"],
                           cwd=filtrado, capture_output=True, text=True)
        quedan = [p for p, _, _ in presentes if p in r.stdout]
        emit("terceros.que.quedan.en.la.historia.filtrada",
             " ".join(quedan) if quedan else "ninguno")
        check("el.filtrado.no.deja.rastro", not quedan,
              "filtrar el arbol de ahora no basta: tiene que salir de todos los "
              "commits")

    bundle = os.path.join(DIST, "forced-counts.bundle")
    if os.path.exists(bundle):
        os.remove(bundle)
    rc, _, sal = corre(["git", "bundle", "create", bundle, "--all"], filtrado)
    check("el.bundle.se.crea", rc == 0, sal)
    if rc == 0:
        emit("bundle.bytes", os.path.getsize(bundle))
        emit("bundle.sha256", sha(bundle))
        rc, _, sal = corre(["git", "bundle", "verify", bundle], ROOT)
        check("el.bundle.se.verifica", rc == 0, sal)

        # y se abre de verdad, que es lo unico que prueba que sirve
        abierto = os.path.join(tmp, "desdebundle")
        borra_arbol(abierto)
        rc, _, sal = corre(["git", "clone", "-q", bundle, abierto], ROOT)
        check("el.bundle.se.clona", rc == 0, sal)
        if rc == 0:
            r = subprocess.run(["git", "log", "--oneline"], cwd=abierto,
                               capture_output=True, text=True)
            emit("commits.en.el.bundle",
                 len([l for l in r.stdout.split("\n") if l.strip()]))
            for p, _, _ in presentes:
                check("el.bundle.no.trae.%s" % os.path.basename(p),
                      not os.path.exists(os.path.join(abierto, p)))


# --- principal ---------------------------------------------------------------

def main():
    rapido = "--rapido" in sys.argv
    emit("modo", "rapido, la fase 1 saltada" if rapido else "completo")
    emit("head", subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip())
    sucio = subprocess.run(["git", "-C", ROOT, "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    emit("arbol.limpio.al.empaquetar", "no" if sucio else "si",
         "lo que se clona es lo commiteado, no lo que hay sin commitear")

    tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "forced-counts-paquete")
    os.makedirs(tmp, exist_ok=True)

    clon_limpio(os.path.join(tmp, "clon"), rapido)
    historia()
    sin_secretos()
    manifiesto_y_bundle(tmp)

    emit("desajustes", len(FALLOS))
    check("el.paquete.esta.entero", not FALLOS)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Verificacion del paquete: clon limpio, historia, secretos,\n")
        fh.write("# terceros y bundle.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        for f in FALLOS:
            fh.write("DESAJUSTE\t1\t%s\n" % f)

    for k, v, _ in ROWS:
        print("  %-52s %s" % (k, v))
    if FALLOS:
        print("\nDESAJUSTES:")
        for f in FALLOS:
            print("  " + f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
