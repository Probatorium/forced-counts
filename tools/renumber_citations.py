#!/usr/bin/env python3
"""
Renumera las citas del manuscrito, y no a mano.

Las referencias se escribieron primero con claves alfabeticas, [BB], [Ra], [PR],
que son comodas para escribir y no son el estilo de la casa. El estilo pide
numeros, [1] a [n], con la lista en orden alfabetico de primer autor. Cambiar eso
a mano en nueve ficheros es exactamente la clase de tarea en la que se pierde una
cita, y una cita perdida no la ve nadie hasta que la ve un lector.

La numeracion NO se escribe aqui: se deriva del orden alfabetico que
src/assemble_paper.py ya fija en REFERENCIAS, de modo que la lista y el texto no
pueden discrepar. Si manana se anade una referencia y el orden cambia, se vuelve
a correr con el mapa nuevo.

  python tools/renumber_citations.py              renumera
  python tools/renumber_citations.py --comprobar  solo mira y no toca

paper/citation-order.tsv guarda la numeracion que el markdown lleva puesta. Con
ella, reordenar la bibliografia deja de ser trabajo manual: la herramienta
compara la numeracion vieja con la que sale del orden alfabetico de ahora,
remapea el texto y actualiza el fichero. Sin ese fichero no habria manera de
saber a que referencia apunta un [7] ya escrito.

La sustitucion se hace en DOS FASES, con marcadores intermedios. Sin eso, un
mapa como BB a 1 y otro de 1 a algo se pisarian entre si segun el orden en que
tocara aplicarlos, y el resultado dependeria del azar del diccionario.

Salida: results/citation-renumber.tsv
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import assemble_paper as A  # noqa: E402

PAPER = os.path.join(ROOT, "paper")
OUT = os.path.join(ROOT, "results", "citation-renumber.tsv")
ORDEN = os.path.join(PAPER, "citation-order.tsv")

FUENTES = ["00-abstract.md"] + [
    "01-introduction.md", "02-preliminaries.md", "03-orbit-accounting.md",
    "04-parity-obstruction.md", "05-characterisation.md",
    "06-three-historical-orderings.md", "07-landscape.md",
    "08-open-problems.md", "09-verification.md",
]

ROWS = []
FALLOS = []


def emit(k, v, n=""):
    ROWS.append((k, str(v), n))


def prosa(texto):
    """El texto sin comentarios de ensamblaje: donde viven las citas de verdad."""
    return re.sub(r"<!--.*?-->", " ", texto, flags=re.S)


def leer_orden():
    """La numeracion que el markdown lleva puesta, clave alfabetica a numero."""
    if not os.path.exists(ORDEN):
        return {}
    d = {}
    for l in open(ORDEN, encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        c = l.rstrip("\n").split("\t")
        if len(c) >= 2:
            d[c[0]] = c[1]
    return d


def main():
    comprobar = "--comprobar" in sys.argv
    nueva = dict(A.NUMERO)
    vieja = leer_orden()

    # El mapa que se aplica al texto. Si el markdown ya lleva numeros, va de
    # numero viejo a numero nuevo; si todavia lleva claves alfabeticas, va de
    # clave a numero. Las dos formas conviven porque la segunda solo se usa una
    # vez, en la migracion, y despues no vuelve a hacer falta.
    mapa = {}
    for clave, num_nuevo in nueva.items():
        origen = vieja.get(clave, clave)
        mapa[origen] = num_nuevo
    emit("numeracion.previa.conocida", int(bool(vieja)),
         "sin ella no habria manera de saber a que apunta un numero ya escrito")
    emit("claves.que.cambian.de.numero",
         sum(1 for c in nueva if vieja.get(c) not in (None, nueva[c])))
    emit("referencias", len(mapa))
    emit("mapa", " ".join("%s>%s" % (k, mapa[k]) for k in
                          sorted(mapa, key=lambda x: int(mapa[x]))),
         "de lo que el texto lleva hoy al numero que le toca")

    total_alfa, total_num, tocados = 0, 0, 0
    for nombre in FUENTES:
        ruta = os.path.join(PAPER, nombre)
        t = open(ruta, encoding="utf-8").read()
        original = t

        antes_aqui = re.findall(r"\[([A-Z][A-Za-z]{1,3}|\d{1,2})\]", prosa(t))
        huerfanas = sorted(set(a for a in antes_aqui if a not in mapa))
        if huerfanas:
            FALLOS.append("%s: citas que no apuntan a ninguna referencia: %s"
                          % (nombre, " ".join(huerfanas)))
        total_alfa += len(antes_aqui)

        # fase uno: a marcadores que no pueden colisionar con nada
        for clave, numero in mapa.items():
            t = t.replace("[%s]" % clave, "\x00%s\x00" % numero)
        # fase dos: los marcadores a su forma final
        t = re.sub("\x00(\\d+)\x00", r"[\1]", t)

        total_num += len(re.findall(r"\[(\d{1,2})\]", prosa(t)))
        if t != original:
            tocados += 1
            if not comprobar:
                with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(t)

    emit("citas.encontradas.antes", total_alfa)
    emit("citas.numericas.resultantes", total_num)
    emit("ficheros.tocados", tocados)
    emit("modo", "comprobar" if comprobar else "escribir")
    ok = total_alfa == total_num and not FALLOS
    emit("ninguna.cita.se.pierde.al.renumerar", int(ok),
         "el numero de citas antes y despues tiene que ser el mismo")
    if not ok:
        FALLOS.append("el recuento de citas no cuadra: %d antes, %d despues"
                      % (total_alfa, total_num))

    if not comprobar:
        with open(ORDEN, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Numeracion de las citas que el markdown lleva AHORA "
                     "MISMO.\n")
            fh.write("# La mantiene tools/renumber_citations.py, y existe para "
                     "que\n")
            fh.write("# reordenar la bibliografia no obligue a tocar el texto "
                     "a mano.\n")
            fh.write("# clave\tnumero\n")
            for clave, num in sorted(nueva.items(), key=lambda x: int(x[1])):
                fh.write("%s\t%s\n" % (clave, num))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Renumeracion de las citas del manuscrito.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        for f in FALLOS:
            fh.write("DESAJUSTE\t1\t%s\n" % f)

    for k, v, _ in ROWS:
        print("  %-40s %s" % (k, v))
    if FALLOS:
        print("\nDESAJUSTES:")
        for f in FALLOS:
            print("  " + f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
