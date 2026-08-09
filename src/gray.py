#!/usr/bin/env python3
"""
El codigo de Gray reflejado de seis bits, como CUARTA ordenacion, y solo como
objeto de comparacion. Las tres historicas no se tocan.

Deslinde, obligatorio en primera aparicion: en la literatura de codigos de Gray
la palabra balanced se refiere a los recuentos de transicion por coordenada, es
decir a repartir por igual cuantas veces cambia cada bit a lo largo del ciclo.
No se refiere al empate que aqui se mide, que es el recuento de inversiones
contra el orden binario. Son dos cosas distintas y no se mezclan.

Se construye desde su definicion recursiva, aqui, sin importar nada.

  G(0) = [la palabra vacia]
  G(k) = [n seguido de w, para w en G(k-1)] ++ [y seguido de w, para w en G(k-1)
          en orden inverso]

donde la linea que se anade en cada paso es la mas significativa de la
convencion de referencia, es decir la linea 1 en el ultimo paso.

Particiones en bloques: la recursion no da una, da una torre. Se declara antes
de correr nada que se recorren TODOS los niveles, tamanos 2, 4, 8, 16 y 32, y
que se reportan todos, para que la eleccion de nivel no pueda hacerse despues de
ver resultados.

Salida: results/gray-measurements.tsv

  python src/gray.py
"""

import os
import sys
from math import comb, factorial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import measure as M                                        # noqa: E402
import group as GR                                         # noqa: E402

OUT = os.path.join(ROOT, "results", "gray-measurements.tsv")

N, LINES = M.N, M.LINES
DENOM = M.DENOM
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo la comprobacion: " + key


# --- la construccion recursiva ----------------------------------------------

def reflected_gray(k):
    """Codigo de Gray reflejado de k lineas, como lista de patrones."""
    if k == 0:
        return [""]
    prev = reflected_gray(k - 1)
    return ["n" + w for w in prev] + ["y" + w for w in reversed(prev)]


def main():
    pats = reflected_gray(LINES)
    seq = [M.enc(p) for p in pats]

    emit("gray.longitud", len(seq), "construido por la recursion, sin importar nada")
    check("gray.es.una.permutacion.de.los.64", sorted(seq) == list(range(N)))

    # dos comprobaciones de que es el codigo de Gray y no otra cosa
    ref = [M.value(M.dec(x), "yang1", "bottomMSB") for x in range(N)]
    cerrado = [n ^ (n >> 1) for n in range(N)]
    check("gray.coincide.con.la.forma.cerrada.n.xor.n.medio",
          [ref[x] for x in seq] == cerrado,
          "la recursion reproduce n XOR n desplazado uno, bajo la convencion de referencia")
    saltos = [bin(seq[i] ^ seq[i + 1]).count("1") for i in range(N - 1)]
    check("gray.pasos.de.una.sola.linea", set(saltos) == {1},
          "cada paso cambia exactamente una linea")
    emit("gray.coste.hamming.adyacente", sum(saltos), "el minimo posible para 64 palabras")

    # --- 1. la tabla, con el mismo aparato y el mismo denominador ------------
    emit("denominador", DENOM, "C(64,2), el mismo de siempre")
    for pol in M.POLARITIES:
        for end in M.ENDIANS:
            vals = [M.value(M.dec(x), pol, end) for x in seq]
            inv = M.inversions(vals)
            emit("inv.Gray.%s.%s" % (pol, end), inv, "tasa %.6f sobre C(64,2)" % (inv / DENOM))

    # --- 2. el grupo y la contabilidad, nivel a nivel ------------------------
    valh = ref
    esperado = DENOM // 2
    for k in (1, 2, 3, 4, 5):
        size = 1 << k
        bloques = GR.blocks_of(seq, size)
        # los bloques del nivel k son cosets del subespacio de las k lineas
        # inferiores de la lectura, y eso se comprueba, no se supone
        base = frozenset(x ^ bloques[0][0] for x in bloques[0])
        cosets = all(frozenset(x ^ b[0] for x in b) == base for b in bloques)
        subesp = all((a ^ b) in base for a in base for b in base)
        emit("gray.nivel.%d.bloques.son.cosets.de.un.mismo.conjunto" % size, int(cosets), "")
        emit("gray.nivel.%d.ese.conjunto.es.subespacio" % size, int(subesp), "")

        g1 = GR.group_R1(seq, size)
        g2 = GR.group_R2(seq, size)
        pred = factorial(k) * factorial(LINES - k) * N
        emit("gray.nivel.%d.R1.orden" % size, len(g1),
             "prediccion k! por (6-k)! por 64, igual a %d" % pred)
        emit("gray.nivel.%d.R1.orden.coincide.con.la.prediccion" % size, int(len(g1) == pred), "")
        emit("gray.nivel.%d.R2.orden" % size, len(g2), "")

        gens = GR.generators_of(g1)
        res = GR.accounting(seq, g1, gens, valh)
        for key in ("orbitas", "orbitas_forzadas", "orbitas_libres", "aportacion_forzada",
                    "minimo", "maximo", "observado", "anchura", "totales_alcanzables",
                    "esperado_alcanzable", "paridad_forzada"):
            emit("gray.nivel.%d.%s" % (size, key), res[key], "")
        emit("gray.nivel.%d.fuerza.el.empate" % size,
             int(res["minimo"] == res["maximo"] == esperado), "")

    # la sola complementacion, para poder comparar con las tres historicas
    ident = tuple(range(N))
    comp = tuple(x ^ (N - 1) for x in range(N))
    res = GR.accounting(seq, [ident, comp], [comp], valh)
    for key in ("orbitas_forzadas", "aportacion_forzada", "anchura", "observado"):
        emit("gray.solo.complementacion.%s" % key, res[key], "")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# El codigo de Gray reflejado como ordenacion de comparacion.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/gray-measurements.tsv con %d cifras" % len(ROWS))
    for key, val, _ in ROWS:
        print("  %-58s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
