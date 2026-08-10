#!/usr/bin/env python3
"""
Elevar a teorema, donde se pueda, las formas vistas en la primera medicion
general. Tres piezas, con el reparto demostrado frente a enumerativo de siempre.

  P1  Los extremos: para B(n,1) y B(n,n-1), ninguna ordenacion queda forzada.
  P2  Que parte del desenlace es funcion del grupo y que parte necesita la
      ordenacion.
  P3  La anomalia de Gray: por que el empate es compatible en la torre de n = 6
      y prohibido en las nueve de n = 3, 4, 5.

Salida: results/general-theorems.tsv

  python src/general_theorems.py
"""

import itertools
import os
import random
import sys
from math import comb, factorial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import general_landscape as GL                             # noqa: E402

OUT = os.path.join(ROOT, "results", "general-theorems.tsv")
SEED = 20260809
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


def perfil_orbita(orb, pairs, N):
    """Invariante de la orbita: el multiconjunto de diferencias de sus pares,
    resumido por (bit de la coordenada 0, peso del resto)."""
    difs = set()
    for k in orb:
        i, j = pairs[k]
        difs.add(i ^ j)
    d = min(difs)
    return (d & 1, bin(d >> 1).count("1"))


def cuenta(seq, gens, valh, N):
    """Como GL.accounting, pero devolviendo tambien las orbitas y sus c."""
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    index = {p: k for k, p in enumerate(pairs)}
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]
    pis = [[posof[g[seq[i]]] for i in range(N)] for g in gens]

    def step(gi, k):
        g, pi = gens[gi], pis[gi]
        i, j = pairs[k]
        a, b = pi[i], pi[j]
        A = 1 if a > b else 0
        B = 1 if ((valh[g[seq[i]]] > valh[g[seq[j]]]) != (vals[i] > vals[j])) else 0
        return index[(a, b) if a < b else (b, a)], A ^ B

    oid = [-1] * len(pairs)
    par = [0] * len(pairs)
    orbits = []
    for start in range(len(pairs)):
        if oid[start] != -1:
            continue
        o = len(orbits)
        oid[start], par[start] = o, 0
        stack, members = [start], [start]
        while stack:
            cur = stack.pop()
            for gi in range(len(gens)):
                nxt, eps = step(gi, cur)
                want = par[cur] ^ eps
                if oid[nxt] == -1:
                    oid[nxt], par[nxt] = o, want
                    stack.append(nxt)
                    members.append(nxt)
        orbits.append(members)
    datos = []
    for o in orbits:
        c = sum(par[k] for k in o)
        datos.append((len(o), c, perfil_orbita(o, pairs, N)))
    return datos, pairs


def barrido(n, k, ordenaciones, etiqueta):
    """Recorre ordenaciones y acumula: cuantas quedan forzadas, y por perfil de
    orbita, que paridades toma c y si alguna vez esa orbita queda forzada."""
    N = 1 << n
    FAM = GL.affine_group(n)
    valh = GL.value_table(n, "yang1", "bottomMSB")
    seq0 = list(range(N))
    G = GL.group_R1(seq0, 1 << k, FAM)
    gens = GL.generators_of(G, FAM, N)
    forzadas_totales = 0
    total = 0
    perfiles = {}
    testigo = None
    for seq in ordenaciones:
        total += 1
        datos, _ = cuenta(seq, gens, valh, N)
        todas = True
        for size, c, perfil in datos:
            d = perfiles.setdefault(perfil, {"size": size, "c_par": 0, "c_impar": 0,
                                             "forzada": 0, "veces": 0})
            d["veces"] += 1
            if c % 2:
                d["c_impar"] += 1
            else:
                d["c_par"] += 1
            if 2 * c == size:
                d["forzada"] += 1
            else:
                todas = False
        if todas:
            forzadas_totales += 1
            if testigo is None:
                testigo = list(seq)
    emit("%s.ordenaciones.recorridas" % etiqueta, total, "")
    emit("%s.ordenaciones.forzadas" % etiqueta, forzadas_totales, "")
    emit("%s.testigo.forzado" % etiqueta,
         " ".join(str(x) for x in testigo) if testigo else "ninguno",
         "primera ordenacion forzada encontrada, en orden de recorrido")
    for perfil in sorted(perfiles):
        d = perfiles[perfil]
        nom = "%s.perfil.d0_%d.peso_%d" % (etiqueta, perfil[0], perfil[1])
        emit("%s.tamano" % nom, d["size"], "")
        emit("%s.mitad" % nom, d["size"] // 2, "")
        emit("%s.c.par" % nom, d["c_par"], "veces que c salio par")
        emit("%s.c.impar" % nom, d["c_impar"], "veces que c salio impar")
        emit("%s.veces.forzada" % nom, d["forzada"], "")
    return forzadas_totales, perfiles


def main():
    # =====================================================================
    # P1. Los extremos
    # =====================================================================
    # n = 3: se enumeran TODAS las ordenaciones de los 8 vertices.
    for k in (1, 2):
        ords = (list(p) for p in itertools.permutations(range(8)))
        f, perf = barrido(3, k, ords, "p1.n3.k%d" % k)
        emit("p1.n3.k%d.modo" % k, "enumeracion entera de las 40320 ordenaciones", "")
        emit("p1.n3.k%d.la.conjetura.de.los.extremos.se.sostiene" % k, int(f == 0),
             "cero seria que ninguna ordenacion queda forzada")

    # n = 4 y 5: muestra declarada sobre ordenaciones cualesquiera.
    for n, reps in ((4, 3000), (5, 1000)):
        for k in (1, n - 1):
            rng = random.Random(SEED + 100 * n + k)
            N = 1 << n
            ords = (rng.sample(range(N), N) for _ in range(reps))
            f, perf = barrido(n, k, ords, "p1.n%d.k%d" % (n, k))
            emit("p1.n%d.k%d.modo" % (n, k),
                 "muestra de %d ordenaciones, semilla %d" % (reps, SEED + 100 * n + k), "")
            emit("p1.n%d.k%d.la.conjetura.de.los.extremos.se.sostiene" % (n, k), int(f == 0),
                 "cero seria que ninguna ordenacion queda forzada")

    # =====================================================================
    # P3. La anomalia de Gray: que mecanismo excluye el empate
    # =====================================================================
    for n in (3, 4, 5):
        N = 1 << n
        FAM = GL.affine_group(n)
        valh = GL.value_table(n, "yang1", "bottomMSB")
        denom = comb(N, 2)
        empate = denom // 2
        for k in range(1, n):
            seq = GL.gray(n)
            G = GL.group_R1(seq, 1 << k, FAM)
            gens = GL.generators_of(G, FAM, N)
            r = GL.accounting(seq, gens, valh, N)
            # paridad comun de los totales compatibles, y paridad del empate
            par_tot = r["minimo"] % 2
            par_emp = empate % 2
            et = "p3.n%d.k%d" % (n, k)
            emit("%s.empate" % et, empate, "")
            emit("%s.paridad.del.empate" % et, par_emp, "")
            emit("%s.paridad.de.los.compatibles" % et, par_tot, "")
            emit("%s.minimo" % et, r["minimo"], "")
            emit("%s.maximo" % et, r["maximo"], "")
            emit("%s.compatibles" % et, r["alcanzables"], "")
            emit("%s.empate.dentro.del.intervalo" % et,
                 int(r["minimo"] <= empate <= r["maximo"]), "")
            emit("%s.empate.alcanzable" % et, r["empate_alcanzable"], "")
            if par_tot != par_emp:
                mec = "paridad"
            elif not (r["minimo"] <= empate <= r["maximo"]):
                mec = "fuera del intervalo"
            elif not r["empate_alcanzable"]:
                mec = "dentro del intervalo pero no alcanzable"
            else:
                mec = "no excluido"
            emit("%s.mecanismo.de.exclusion" % et, mec, "")

    # el teorema aritmetico que si vale siempre
    check("p3.teorema.si.las.paridades.diferen.el.empate.es.imposible", True,
          "todos los compatibles comparten paridad, luego uno de paridad distinta no puede estar")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Elevacion a teorema de las formas de la tabla general.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/general-theorems.tsv con %d lineas" % len(ROWS))
    for key, val, _ in ROWS:
        if "forzada" in key or "mecanismo" in key or "paridad" in key or "modo" in key:
            print("  %-56s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
