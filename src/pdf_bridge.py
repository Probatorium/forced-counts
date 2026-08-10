#!/usr/bin/env python3
"""
El puente entre el PDF y el manuscrito.

Un PDF es una foto. En cuanto el texto cambia, la foto miente, y lo hace en
silencio: el fichero sigue abriendose, sigue teniendo el mismo aspecto y sigue
llevando un colofon con un commit que ya no es el de nada. Este comprobador
convierte ese silencio en un fallo.

Lee el colofon que src/build_paper.py deja dentro del PDF, en el diccionario de
informacion del propio fichero, y lo coteja contra el estado del repositorio:

  1. que el sha256 que el PDF declara sea el del manuscrito que hay ahora. Es la
     comprobacion que importa: cualquier cambio del texto, por pequeno que sea,
     la rompe y avisa de que se debe una version nueva;
  2. que el commit que el PDF declara exista en la historia de este repositorio,
     y no sea uno inventado ni de otro sitio;
  3. que ese commit sea el HEAD actual, o, si no lo es, que se diga cuantos
     commits han pasado desde entonces, que es el aviso suave antes del duro;
  4. que el recuento de comprobaciones en verde del colofon siga siendo el que
     dan los ficheros de comprobador de ahora;
  5. que el .tex y el PDF declaren el mismo sha256, para que no puedan haber
     salido de dos manuscritos distintos.

  python src/pdf_bridge.py            coteja
  python src/pdf_bridge.py --prueba   exige ver el puente romperse y rehacerse

Salidas: results/pdf-bridge.tsv y results/pdf-bridge-test.tsv. Devuelve 1 si el
puente esta roto.
"""

import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "paper", "PAPER.md")
TEX = os.path.join(ROOT, "paper", "PAPER.tex")
PDF = os.path.join(ROOT, "paper", "PAPER.pdf")
OUT = os.path.join(ROOT, "results", "pdf-bridge.tsv")

ROWS = []
FALLOS = []
# Contenido alternativo del manuscrito, solo para la prueba de
# que el puente sabe romperse. Vacio en el uso normal.
MANUSCRITO = []


def emit(k, v, n=""):
    ROWS.append((k, str(v), n))


def check(k, cond, n=""):
    emit(k, int(bool(cond)), n)
    if not cond:
        FALLOS.append(k + ("  " + n if n else ""))


def normaliza(datos):
    """Los bytes del manuscrito con el fin de linea en unix.

    Lo que se resume tiene que ser el texto, no la convencion con que el sistema
    operativo de turno lo haya dejado en el disco.
    """
    return datos.replace(b"\r\n", b"\n")


def git(*args):
    try:
        r = subprocess.run(["git", "-C", ROOT] + list(args),
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except Exception:
        return ""


def colofon_del_pdf():
    """El colofon tal y como el PDF lo lleva dentro, sin intermediarios."""
    datos = open(PDF, "rb").read().decode("latin-1")
    m = re.search(r"/Subject\s*\(([^)]*)\)", datos)
    if not m:
        return None
    campos = {}
    for par in m.group(1).split():
        if "=" in par:
            k, v = par.split("=", 1)
            campos[k] = v
    return campos


def comprobaciones_en_verde():
    total = 0
    for nombre in ("assembly-check.tsv", "declared-values.tsv",
                   "mutation-test.tsv", "effort.tsv"):
        ruta = os.path.join(ROOT, "results", nombre)
        if not os.path.exists(ruta):
            continue
        for linea in open(ruta, encoding="utf-8"):
            if linea.startswith("#"):
                continue
            campos = linea.rstrip("\n").split("\t")
            if len(campos) >= 2 and campos[1] == "1":
                total += 1
    return total


def prueba():
    """Exige ver el puente romperse, y volver a estar entero.

    Un comprobador que nunca ha dado rojo no esta probado. Aqui se le da un
    manuscrito con un caracter de mas, que es el cambio mas pequeno que se puede
    hacer a un texto, y se exige que avise de que se debe una version nueva. El
    fichero del disco no se toca en ningun momento.
    """
    original = open(MD, "rb").read()

    MANUSCRITO.append(original + b"\n")
    del ROWS[:]
    del FALLOS[:]
    main()
    roto = [f for f in FALLOS if "corresponde.al.manuscrito" in f]
    avisos = list(FALLOS)

    del MANUSCRITO[:]
    del ROWS[:]
    del FALLOS[:]
    salida = main()
    entero = not FALLOS

    filas = [
        ("mutacion", "un salto de linea de mas al final del manuscrito",
         "el cambio mas pequeno que se le puede hacer a un texto"),
        ("con.la.mutacion.desajustes", len(avisos), ""),
        ("con.la.mutacion.el.puente.avisa", int(bool(roto)),
         "si vale cero, el puente no vigila lo que dice vigilar"),
        ("con.la.mutacion.aviso", roto[0] if roto else "ninguno", ""),
        ("restaurado.el.puente.esta.entero", int(entero), ""),
        ("el.fichero.no.se.toco",
         int(open(MD, "rb").read() == original), ""),
        ("la.prueba.del.puente.pasa",
         int(bool(roto) and entero and salida == 0), ""),
    ]
    ruta = os.path.join(ROOT, "results", "pdf-bridge-test.tsv")
    with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Prueba de que el puente sabe romperse.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in filas:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
    print()
    for k, v, _ in filas:
        print("  %-42s %s" % (k, v))
    return 0 if (roto and entero) else 1


def main():
    for ruta, nombre in ((MD, "PAPER.md"), (TEX, "PAPER.tex"), (PDF, "PAPER.pdf")):
        check("existe.%s" % nombre, os.path.exists(ruta))
    if FALLOS:
        return informe()

    colo = colofon_del_pdf()
    check("el.pdf.lleva.colofon.legible", colo is not None,
          "sin colofon dentro del fichero no hay puente que cotejar")
    if not colo:
        return informe()

    for k in ("commit", "fecha", "sha256", "comprobaciones"):
        emit("colofon.%s" % k, colo.get(k, "ausente"))

    # 1. el sha256, que es la comprobacion que importa.
    #
    # Se normaliza el fin de linea antes de resumir. La pregunta que este puente
    # tiene que contestar es si el TEXTO ha cambiado, y un retorno de carro que
    # git anade al sacar el fichero en otra maquina no es un cambio del texto.
    # Sin esta normalizacion el puente daba rojo en el clon de cualquiera y
    # verde solo aqui, que es la peor manera posible de fallar.
    crudo = MANUSCRITO[0] if MANUSCRITO else open(MD, "rb").read()
    ahora = hashlib.sha256(normaliza(crudo)).hexdigest()
    emit("sha256.del.manuscrito.de.ahora", ahora)
    check("el.pdf.corresponde.al.manuscrito.de.ahora",
          colo.get("sha256") == ahora,
          "el texto ha cambiado desde que se construyo el PDF: se debe una "
          "version nueva, hay que volver a correr src/build_paper.py")

    # 2 y 3. el commit
    commit = colo.get("commit", "")
    existe = bool(commit) and git("cat-file", "-t", commit) == "commit"
    check("el.commit.del.colofon.existe.en.esta.historia", existe)
    head = git("rev-parse", "HEAD")
    emit("head.actual", head)
    if existe:
        detras = git("rev-list", "--count", "%s..HEAD" % commit)
        emit("commits.desde.el.del.colofon", detras or "0",
             "cero quiere decir que el PDF es del estado actual")
        # INFORMATIVO Y NO DURO, a proposito. Un colofon no puede nombrar nunca
        # el commit que lo contiene: se construye antes de que ese commit
        # exista. Lo normal es que valga cero recien construido y uno en cuanto
        # el PDF entra en un commit. Lo que si es duro es el sha256 del
        # manuscrito, que es lo que de verdad decide si el PDF miente.
        emit("el.pdf.retrata.el.head.actual", int(commit == head),
             "informativo: el PDF se construye antes del commit que lo guarda, "
             "asi que aqui un cero es lo esperado, no un fallo")

    # 4. el recuento de comprobaciones
    verde = comprobaciones_en_verde()
    emit("comprobaciones.en.verde.ahora", verde)
    check("el.recuento.de.comprobaciones.no.ha.cambiado",
          str(verde) == colo.get("comprobaciones", ""),
          "los comprobadores dan hoy un numero distinto del que el PDF declara")

    # 5. las dos salidas, del mismo manuscrito
    tex = open(TEX, encoding="utf-8").read()
    check("el.tex.declara.el.mismo.sha256.que.el.pdf",
          colo.get("sha256", "") in tex,
          "el .tex y el PDF tienen que haber salido del mismo manuscrito")

    return informe()


def informe():
    emit("desajustes", len(FALLOS))
    emit("el.puente.esta.entero", int(not FALLOS))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Puente entre paper/PAPER.pdf y el manuscrito.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        for f in FALLOS:
            fh.write("DESAJUSTE\t1\t%s\n" % f)
    for k, v, _ in ROWS:
        print("  %-48s %s" % (k, v))
    if FALLOS:
        print("\nPUENTE ROTO:")
        for f in FALLOS:
            print("  " + f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(prueba() if "--prueba" in sys.argv else main())
