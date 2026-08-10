#!/usr/bin/env python3
"""
Numera las tablas por orden de aparicion, y arrastra sus menciones.

Una tabla se numera por donde sale, no por cuando se escribio. Al promover al
texto la descomposicion del residuo, que vive en la seccion 6, esa tabla paso a
ser la primera del manuscrito y las dos de la seccion 7 corrieron un puesto. Con
tres tablas eso se puede hacer a mano; con tres tablas y cuatro menciones ya no
conviene, porque lo que se pierde es una mencion y no la ve nadie.

La herramienta recorre las secciones en el orden en que se ensamblan, encuentra
los rotulos, les asigna 1..n por aparicion, y renumera a la vez los rotulos y las
menciones del tipo "Table k" del texto. La sustitucion va en dos fases con
marcadores, porque un mapa que lleva 3 a 1 y otro que lleva 1 a 2 se pisarian
segun el orden en que cayeran.

  python tools/renumber_tables.py              renumera
  python tools/renumber_tables.py --comprobar  solo mira y no toca

Salida: results/table-renumber.tsv
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")
OUT = os.path.join(ROOT, "results", "table-renumber.tsv")

FUENTES = ["00-abstract.md", "01-introduction.md", "02-preliminaries.md",
           "03-orbit-accounting.md", "04-parity-obstruction.md",
           "05-characterisation.md", "06-three-historical-orderings.md",
           "07-landscape.md", "08-open-problems.md", "09-verification.md"]

ROTULO = re.compile(r"\*\*Table (\d+)\.\*\*")
MENCION = re.compile(r"\bTable (\d+)\b")

ROWS = []
FALLOS = []


def emit(k, v, n=""):
    ROWS.append((k, str(v), n))


def main():
    comprobar = "--comprobar" in sys.argv

    # los rotulos, en el orden en que el lector se los encuentra
    orden = []
    for nombre in FUENTES:
        t = open(os.path.join(PAPER, nombre), encoding="utf-8").read()
        for m in ROTULO.finditer(t):
            orden.append((nombre, m.group(1)))

    mapa = {viejo: str(i) for i, (_f, viejo) in enumerate(orden, start=1)}
    emit("tablas", len(orden))
    emit("orden.de.aparicion",
         " ".join("%s:%s" % (f.split("-")[0], v) for f, v in orden))
    emit("mapa", " ".join("%s>%s" % (k, mapa[k]) for k in
                          sorted(mapa, key=lambda x: int(mapa[x]))),
         "del numero que lleva puesto al que le toca por aparicion")
    if len(set(v for _f, v in orden)) != len(orden):
        FALLOS.append("hay dos rotulos con el mismo numero: %r" % (orden,))

    menciones_antes, menciones_despues, tocados = 0, 0, 0
    for nombre in FUENTES:
        ruta = os.path.join(PAPER, nombre)
        t = open(ruta, encoding="utf-8").read()
        original = t
        menciones_antes += len(MENCION.findall(t))

        huerfanas = sorted(set(MENCION.findall(t)) - set(mapa))
        if huerfanas:
            FALLOS.append("%s: menciona tablas que no existen: %s"
                          % (nombre, " ".join(huerfanas)))

        t = MENCION.sub(lambda m: "Table \x00%s\x00" % mapa.get(m.group(1),
                                                               m.group(1)), t)
        t = re.sub("\x00(\\d+)\x00", r"\1", t)
        menciones_despues += len(MENCION.findall(t))

        if t != original:
            tocados += 1
            if not comprobar:
                with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(t)

    emit("menciones.antes", menciones_antes)
    emit("menciones.despues", menciones_despues)
    emit("ficheros.tocados", tocados)
    emit("modo", "comprobar" if comprobar else "escribir")
    ok = menciones_antes == menciones_despues and not FALLOS
    emit("ninguna.mencion.se.pierde", int(ok))
    if not ok:
        FALLOS.append("el recuento de menciones no cuadra: %d antes, %d despues"
                      % (menciones_antes, menciones_despues))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Numeracion de las tablas por orden de aparicion.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        for f in FALLOS:
            fh.write("DESAJUSTE\t1\t%s\n" % f)

    for k, v, _ in ROWS:
        print("  %-30s %s" % (k, v))
    if FALLOS:
        print("\nDESAJUSTES:")
        for f in FALLOS:
            print("  " + f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
