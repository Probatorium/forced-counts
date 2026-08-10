#!/usr/bin/env python3
"""
n = 6 entra en el mismo sistema B(n, k) que n = 3, 4 y 5, con las mismas
columnas, para que la tabla general sea una sola.

Se miden, con el aparato de src/general_landscape.py y sin cambiarle nada:

  - la torre del codigo de Gray reflejado, niveles k de 1 a 5;
  - la ordenacion canonica de la familia O3, niveles k de 1 a 5;
  - y la secuencia historica de Mawangdui contra B(6, 3), que es su sistema de
    bloques: sus octetos son las fibras del trigrama superior, es decir las
    clases laterales del subespacio de las tres lineas bajas.

Se declara aqui, y se repite en el informe, por que las otras dos historicas NO
entran en esta tabla: los palacios de Jing Fang son las clases laterales de un
conjunto M que no es subespacio, y los pares de King Wen son las orbitas del
giro. Ninguno de los dos es un B(6, k), y meterlos en la tabla seria forzar la
analogia.

Tampoco se muestrea la familia O3 para n = 6: cada caso cuesta del orden de un
segundo por los 2016 pares, y 2000 repeticiones por nivel serian horas. Se dice
en vez de disimularlo.

Salida: results/general-n6.tsv

  python src/general_n6.py
"""

import json
import os
import sys
from math import comb, factorial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import general_landscape as GL                             # noqa: E402
import measure as M                                        # noqa: E402

OUT = os.path.join(ROOT, "results", "general-n6.tsv")
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


def main():
    n = 6
    N = 1 << n
    denom = comb(N, 2)
    emit("n6.vertices", N, "")
    emit("n6.denominador", denom, "C(2^n, 2)")
    emit("n6.empate", denom // 2, "")

    print("construyendo la familia afin de n = 6 ...")
    FAM = GL.affine_group(n)
    emit("n6.orden.de.B_n", len(FAM), "n! por 2^n")
    valh = GL.value_table(n, "yang1", "bottomMSB")

    # la secuencia historica de Mawangdui, del dato del repositorio
    with open(os.path.join(ROOT, "data", "sequences.json"), "r", encoding="utf-8") as fh:
        seqs = json.load(fh)["sequences"]
    mwd = [M.enc(p) for p in seqs["Mawangdui"]]
    check("n6.mawangdui.es.una.permutacion.de.los.64", sorted(mwd) == list(range(N)))
    check("n6.los.octetos.de.mawangdui.son.los.bloques.de.B(6,3)",
          all(len(set(x >> 3 for x in mwd[i:i + 8])) == 1 for i in range(0, N, 8)),
          "cada octeto tiene un unico trigrama superior")

    # las otras dos historicas no encajan en B(n,k), y se comprueba
    jf = [M.enc(p) for p in seqs["Jing Fang"]]
    kw = [M.enc(p) for p in seqs["King Wen"]]
    difs_jf = set(x ^ jf[0] for x in jf[:8])
    es_sub = all((a ^ b) in difs_jf for a in difs_jf for b in difs_jf)
    emit("n6.los.palacios.de.jing.fang.son.clases.de.un.subespacio", int(es_sub),
         "cero quiere decir que no encajan en el sistema B(n,k)")
    pares_kw = [frozenset(kw[i:i + 2]) for i in range(0, N, 2)]
    difs_kw = set(min(p) ^ max(p) for p in pares_kw)
    emit("n6.diferencias.distintas.entre.los.pares.de.king.wen", len(difs_kw),
         "uno solo querria decir que son clases de un subespacio de dimension uno")

    for k in range(1, n):
        size = 1 << k
        et = "n6.k%d" % k
        pred = factorial(k) * factorial(n - k) * N
        ordenaciones = [("Gray", GL.gray(n)),
                        ("MWDlike.canonica",
                         GL.mawangdui_like(n, k, list(range(1 << (n - k))), list(range(size))))]
        if k == 3:
            ordenaciones.append(("Mawangdui.historica", mwd))
        for nombre, s in ordenaciones:
            print("   n=6 k=%d %s ..." % (k, nombre))
            G = GL.group_R1(s, size, FAM)
            gens = GL.generators_of(G, FAM, N)
            emit("%s.%s.grupo.orden" % (et, nombre), len(G), "")
            emit("%s.%s.grupo.orden.predicho" % (et, nombre), pred, "k! por (n-k)! por 2^n")
            emit("%s.%s.grupo.coincide.con.lo.predicho" % (et, nombre),
                 int(len(G) == pred), "")
            r = GL.accounting(s, gens, valh, N)
            for key in ("orbitas", "forzadas", "libres", "impares", "minimo", "maximo",
                        "anchura", "observado", "alcanzables", "empate_alcanzable",
                        "casilla"):
                emit("%s.%s.%s" % (et, nombre, key), r[key], "")
            if r["anchura"] == 0:
                check("%s.%s.si.fuerza.el.valor.es.el.empate" % (et, nombre),
                      r["minimo"] == denom // 2)
    emit("n6.O3.muestreada", 0,
         "no se muestreo la familia O3 para n = 6, por coste; se dice en vez de disimularlo")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# n = 6 en el mismo sistema B(n,k) que n = 3, 4 y 5.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/general-n6.tsv con %d cifras" % len(ROWS))
    for key, val, _ in ROWS:
        if any(w in key for w in (".casilla", "grupo.orden", "libres", "alcanzables",
                                  "empate_alcanzable", "son.", "diferencias")):
            print("  %-48s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
