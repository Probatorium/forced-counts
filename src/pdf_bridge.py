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

DOS PDF Y UN SOLO CANONICO. El canonico es paper/PAPER.pdf, compilado con LaTeX
desde PAPER.tex por quien tenga la cadena, y no se puede producir en esta
maquina. El de aqui es paper/PAPER-preview.pdf, compuesto con reportlab, y no va
al deposito.

Mientras el canonico no ha llegado, el puente NO se calla y NO da un verde
vacio: lee paper/PDF-STATE.tsv, que declara el estado, e imprime en cada corrida
que falta. Sobre el preview si comprueba lo que puede, que es que corresponda al
manuscrito de ahora. En cuanto el estado dice que el canonico esta entregado, lo
exige y lo valida como se validaba antes, y falla si no esta.

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
PDF = os.path.join(ROOT, "paper", "PAPER.pdf")            # el canonico
PREVIEW = os.path.join(ROOT, "paper", "PAPER-preview.pdf")  # el de aqui
ESTADO = os.path.join(ROOT, "paper", "PDF-STATE.tsv")
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


def campo_declarado(clave):
    """Un campo de paper/PDF-STATE.tsv."""
    if not os.path.exists(ESTADO):
        return ""
    for l in open(ESTADO, encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        c = l.rstrip("\n").split("\t")
        if len(c) >= 2 and c[0] == clave:
            return c[1]
    return ""


def texto_del_pdf(ruta):
    """El texto que el PDF lleva dentro, descomprimiendo sus flujos.

    El canonico lo compone pdfTeX y viene comprimido, asi que hay que inflarlo
    antes de poder leer nada. Esto es lo que permite validarlo POR CONTENIDO en
    vez de por metadatos: un colofon en el diccionario de informacion lo
    escribimos nosotros, mientras que el sha256 impreso en la ultima pagina solo
    puede estar ahi si el .tex del que salio lo llevaba.
    """
    import zlib
    datos = open(ruta, "rb").read()
    cadena = re.compile(rb"\((?:\\.|[^\\()])*\)", re.S)
    trozos = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", datos, re.S):
        try:
            s = zlib.decompress(m.group(1))
        except Exception:
            continue
        for x in cadena.finditer(s):
            u = x.group(0)[1:-1]
            u = re.sub(rb"\\([()\\])", rb"\1", u)
            u = re.sub(rb"\\([0-7]{1,3})",
                       lambda mm: bytes([int(mm.group(1), 8) & 0xFF]), u)
            trozos.append(u.decode("latin-1"))
    return "".join(trozos)


def valida_canonico():
    """Comprueba el PDF entregado contra el manuscrito, por contenido.

    Cuatro cosas, y ninguna se apoya en metadatos escritos por nosotros:

      1. sus bytes son los que el estado declara, que son los que se
         verificaron por sha256 antes de dejarlo entrar;
      2. el sha256 del manuscrito de AHORA aparece impreso dentro del PDF, cosa
         que solo puede pasar si el .tex del que salio llevaba ese colofon;
      3. el commit que ese colofon nombra existe en esta historia;
      4. los cinco nombres con diacritico llegaron compuestos.
    """
    datos = open(PDF, "rb").read()
    sha = hashlib.sha256(datos).hexdigest()
    emit("canonico.bytes", len(datos), "")
    emit("canonico.sha256", sha, "")
    emit("canonico.productor",
         (re.findall(r"/Producer\s*\(([^)]*)\)",
                     datos.decode("latin-1")) or ["sin declarar"])[0], "")
    check("el.canonico.es.el.fichero.declarado", sha == campo_declarado("sha256"),
          "los bytes no son los que se verificaron al entregarlo")

    texto = texto_del_pdf(PDF)
    plano = re.sub(r"\s+", "", texto)
    emit("canonico.caracteres.extraidos", len(texto), "")
    check("del.canonico.se.puede.extraer.texto", len(texto) > 10000,
          "sin texto no hay nada que cotejar y la comprobacion pasaria en vacio")

    ahora = hashlib.sha256(normaliza(open(MD, "rb").read())).hexdigest()
    emit("sha256.del.manuscrito.de.ahora", ahora, "")
    check("el.canonico.lleva.impreso.el.sha.del.manuscrito.de.ahora",
          ahora in plano,
          "el PDF entregado no salio de este manuscrito, o el manuscrito ha "
          "cambiado desde que se compilo: en cualquiera de los dos casos se "
          "debe una version nueva")

    # EL COMMIT ESPERADO SALE DEL ESTADO DECLARADO, no del .tex de ahora.
    #
    # El .tex se regenera cada vez que se construye, y su colofon nombra el HEAD
    # del momento. El PDF entregado es una foto del .tex tal y como estaba al
    # compilarlo, asi que en cuanto se hace un commit mas el .tex va por delante
    # del PDF y compararlos contra el .tex vivo daria rojo siempre. Lo canto la
    # verificacion en clon limpio, donde la cadena regenera el .tex antes de
    # correr los comprobadores.
    commit = campo_declarado("colofon.nombra.el.commit")
    emit("commit.del.colofon.segun.el.estado", commit or "no declarado", "")
    check("el.canonico.lleva.impreso.ese.commit", bool(commit) and commit in plano)
    check("ese.commit.existe.en.esta.historia",
          bool(commit) and git("cat-file", "-t", commit) == "commit")

    faltan = [w for w in ("Garc\u00eda", "Bj\u00f6rner", "M\u00fctze",
                          "Sch\u00f6ter", "Lafreni\u00e8re") if w not in texto]
    emit("canonico.acentos.ausentes",
         " ".join(faltan) if faltan else "ninguno", "")
    check("los.diacriticos.llegaron.compuestos.al.canonico", not faltan)


def estado_declarado():
    """Lo que paper/PDF-STATE.tsv dice del PDF canonico."""
    if not os.path.exists(ESTADO):
        return "sin declarar"
    for l in open(ESTADO, encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        c = l.rstrip("\n").split("\t")
        if len(c) >= 2 and c[0] == "estado":
            return c[1]
    return "sin declarar"


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
    datos = open(globals().get("PDF_EN_USO", PDF),
                 "rb").read().decode("latin-1")
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
    for ruta, nombre in ((MD, "PAPER.md"), (TEX, "PAPER.tex")):
        check("existe.%s" % nombre, os.path.exists(ruta))

    est = estado_declarado()
    emit("estado.declarado.del.pdf.canonico", est,
         "sale de paper/PDF-STATE.tsv")
    hay_canonico = os.path.exists(PDF)
    emit("el.pdf.canonico.esta", int(hay_canonico), "")

    if est == "esperando":
        # Estado intermedio DECLARADO. No es un descuido, y no se pasa por alto:
        # se dice en cada corrida. Lo que si se exige es que no haya un
        # PAPER.pdf por ahi que nadie sepa de donde salio.
        check("mientras.se.espera.no.hay.un.pdf.canonico.sin.origen",
              not hay_canonico,
              "el estado dice que el canonico esta por llegar, y hay un fichero "
              "en su sitio: o el estado esta desactualizado o ese PDF no se "
              "sabe de donde sale")
        print("PDF CANONICO PENDIENTE. El estado declarado es 'esperando': "
              "paper/PAPER.pdf lo entrega el auditor compilado desde "
              "paper/PAPER.tex.")
        if os.path.exists(PREVIEW):
            usar = PREVIEW
            emit("se.coteja.contra", "el preview, a falta del canonico", "")
        else:
            check("hay.al.menos.un.pdf.que.cotejar", False,
                  "ni canonico ni preview: no hay nada que comprobar")
            return informe()
    else:
        check("el.pdf.canonico.existe", hay_canonico,
              "el estado dice que esta entregado, asi que tiene que estar")
        if not hay_canonico:
            return informe()
        emit("se.coteja.contra", "el PDF canonico y, aparte, el preview", "")
        valida_canonico()
        # El preview sigue teniendo su propia comprobacion, la de siempre, con
        # su colofon en el diccionario de informacion: son dos artefactos
        # distintos y cada uno se comprueba con lo que lleva dentro.
        usar = PREVIEW
        check("el.preview.esta", os.path.exists(PREVIEW))
        if not os.path.exists(PREVIEW):
            return informe()

    globals()["PDF_EN_USO"] = usar
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

    # 5. las dos salidas, del mismo manuscrito.
    #
    # El sha va compuesto partible en el .tex, con un punto de corte cada ocho
    # caracteres, porque si no seria una palabra de sesenta y cuatro que no cabe
    # en la linea. Para buscarlo hay que quitar antes esos cortes: comprobarlo
    # sobre el .tex tal cual daria rojo por la propia solucion a la caja.
    tex = open(TEX, encoding="utf-8").read()
    tex_sin_cortes = tex.replace("\\allowbreak ", "")
    check("el.tex.declara.el.mismo.sha256.que.el.pdf",
          colo.get("sha256", "") in tex_sin_cortes,
          "el .tex y el PDF tienen que haber salido del mismo manuscrito")
    check("el.tex.declara.el.mismo.commit.que.el.pdf",
          colo.get("commit", "") in tex_sin_cortes)

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
