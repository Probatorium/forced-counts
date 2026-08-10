#!/usr/bin/env python3
"""
Transiciones consecutivas de la secuencia King Wen: cuantas lineas cambian de un
hexagrama al siguiente, y como se reparte esa cuenta entre par e impar.

Por que existe este fichero. Circula una observacion informal, sin dueno
localizado, segun la cual las transiciones de King Wen se reparten en 48 pares y
16 impares, en razon 3 a 1. En la sesion 9 se dejo anotado que 48 mas 16 son 64
mientras que 64 hexagramas dan 63 transiciones consecutivas, y que o la
observacion contaba otra cosa, o cerraba el ciclo, o venia mal transmitida. Esto
lo mide en vez de suponerlo, en las dos variantes.

  lineal:  63 transiciones, de la posicion 1 a la 64
  ciclica: 64 transiciones, cerrando de la 64 a la 1

Aviso de vocabulario, por la decision registrada en PRIOR-ART.md 11: aqui par e
impar se refieren a la PARIDAD DEL NUMERO DE LINEAS QUE CAMBIAN en una
transicion entre hexagramas consecutivos. No tiene nada que ver con la
obstruccion de paridad de PROOFS.md 3.3, que es la paridad del recuento de pares
discordantes sobre pares de posiciones. Son dos objetos distintos.

Entrada: data/sequences.json. Salida: results/transitions.tsv

  python src/transitions.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import measure as M                                        # noqa: E402

OUT = os.path.join(ROOT, "results", "transitions.tsv")
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def main():
    with open(os.path.join(ROOT, "data", "sequences.json"), "r", encoding="utf-8") as fh:
        kw = json.load(fh)["sequences"]["King Wen"]
    n = len(kw)
    emit("secuencia", "King Wen", "de data/sequences.json, con su procedencia en data/PROVENANCE.md")
    emit("hexagramas", n, "")

    def dist(a, b):
        return sum(1 for x, y in zip(a, b) if x != y)

    lineal = [dist(kw[i], kw[i + 1]) for i in range(n - 1)]
    ciclica = lineal + [dist(kw[n - 1], kw[0])]

    for nombre, ds in (("lineal", lineal), ("ciclica", ciclica)):
        pares = sum(1 for d in ds if d % 2 == 0)
        impares = len(ds) - pares
        emit("%s.transiciones" % nombre, len(ds), "")
        emit("%s.pares" % nombre, pares, "numero de lineas que cambian, par")
        emit("%s.impares" % nombre, impares, "numero de lineas que cambian, impar")
        razon = ("%.4f" % (pares / impares)) if impares else "sin impares, razon indefinida"
        emit("%s.razon.pares.entre.impares" % nombre, razon, "")
        emit("%s.coincide.con.48.16" % nombre, int(pares == 48 and impares == 16),
             "la observacion informal que circula")
        emit("%s.razon.es.3.a.1" % nombre, int(impares > 0 and pares == 3 * impares), "")
        for d in range(1, 7):
            c = sum(1 for x in ds if x == d)
            if c:
                emit("%s.distancia.%d" % (nombre, d), c, "transiciones que cambian %d lineas" % d)
        emit("%s.distancia.minima" % nombre, min(ds), "")
        emit("%s.distancia.maxima" % nombre, max(ds), "")
        emit("%s.coste.total" % nombre, sum(ds), "suma de las lineas que cambian")

    # De donde sale el reparto: la construccion agrupa la secuencia en 32 pares
    # adyacentes, y no es lo mismo la transicion dentro de un par que la que
    # salta de un par al siguiente.
    dentro = [dist(kw[2 * k], kw[2 * k + 1]) for k in range(n // 2)]
    entre_lineal = [dist(kw[2 * k + 1], kw[2 * k + 2]) for k in range(n // 2 - 1)]
    entre_ciclica = entre_lineal + [dist(kw[n - 1], kw[0])]

    emit("dentro.del.par.transiciones", len(dentro), "las 32 de la regla de emparejamiento")
    emit("dentro.del.par.pares", sum(1 for d in dentro if d % 2 == 0), "")
    emit("dentro.del.par.impares", sum(1 for d in dentro if d % 2), "")
    emit("entre.pares.lineal.transiciones", len(entre_lineal), "")
    emit("entre.pares.lineal.pares", sum(1 for d in entre_lineal if d % 2 == 0), "")
    emit("entre.pares.lineal.impares", sum(1 for d in entre_lineal if d % 2), "")
    emit("entre.pares.ciclica.transiciones", len(entre_ciclica), "")
    emit("entre.pares.ciclica.pares", sum(1 for d in entre_ciclica if d % 2 == 0), "")
    emit("entre.pares.ciclica.impares", sum(1 for d in entre_ciclica if d % 2), "")

    # La transicion que solo existe en la variante ciclica
    cierre = dist(kw[n - 1], kw[0])
    emit("transicion.de.cierre.64.a.1", cierre, "solo existe en la variante ciclica")
    emit("transicion.de.cierre.es.par", int(cierre % 2 == 0), "")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Transiciones consecutivas de King Wen. Medicion propia.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/transitions.tsv con %d cifras" % len(ROWS))
    for key, val, _ in ROWS:
        print("  %-46s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
