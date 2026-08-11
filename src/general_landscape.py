#!/usr/bin/env python3
"""
Primera medicion de la fase general, para n = 3, 4 y 5.

Todo lo que aqui se mide quedo declarado antes en DEFINICIONES-GENERAL.md, y la
preinscripcion de la fase esta en PREREGISTRATION-GENERAL.md. El objetivo
declarado es ver la forma de la clasificacion, no afirmarla.

Salida: results/general-landscape.tsv

  python src/general_landscape.py
"""

import itertools
import os
import random
import sys
from math import comb, factorial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "general-landscape.tsv")

SEED = 20260809          # la ya congelada en el repositorio
REPS = 2000              # por combinacion de n y k, donde se muestrea
UMBRAL = 5000            # por debajo de esto se enumera entero en vez de muestrear
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


# --- convenciones de bits, trasladadas a n ----------------------------------
# El vertice es un entero cuyo bit j es la linea j+1, con la linea 1 la inferior.

def value_table(n, polarity, endian):
    N = 1 << n
    out = []
    for x in range(N):
        t = 0
        for k in range(n):
            b = (x >> k) & 1
            if polarity == "yang0":
                b = 1 - b
            t += b * (1 << (n - 1 - k) if endian == "bottomMSB" else 1 << k)
        out.append(t)
    return out


POLARITIES = ("yang1", "yang0")
ENDIANS = ("bottomMSB", "bottomLSB")


# --- el grupo afin y el subgrupo que respeta un sistema de bloques ----------

def affine_group(n):
    N = 1 << n
    out = {}
    for perm in itertools.permutations(range(n)):
        table = [sum(((x >> perm[k]) & 1) << k for k in range(n)) for x in range(N)]
        for m in range(N):
            out[tuple(t ^ m for t in table)] = (perm, m)
    return out


def compose(f, g):
    return tuple(f[x] for x in g)


def group_R1(seq, size, FAM):
    """Aplicaciones que mandan cada bloque entero sobre un bloque entero."""
    bloques = [frozenset(seq[i:i + size]) for i in range(0, len(seq), size)]
    st = set(bloques)
    return [g for g in FAM if all(frozenset(g[y] for y in b) in st for b in bloques)]


def generators_of(group, FAM, N):
    ident = tuple(range(N))

    def closure(gens):
        seen, frontier = {ident}, [ident]
        while frontier:
            cur = frontier.pop()
            for g in gens:
                nxt = compose(g, cur)
                if nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
        return seen

    ordered = sorted(group, key=lambda g: (FAM[g][0], FAM[g][1]))
    gens, have = [], {ident}
    for g in ordered:
        if g in have:
            continue
        gens.append(g)
        have = closure(gens)
        if len(have) == len(group):
            break
    return gens


# --- la contabilidad, la misma de DEFINICIONES-GRUPO.md ----------------------

def accounting(seq, gens, valh, N):
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
                else:
                    assert oid[nxt] == o and par[nxt] == want, "paridad inconsistente"
        orbits.append(members)

    st = [1 if vals[i] > vals[j] else 0 for i, j in pairs]
    denom = len(pairs)
    lo = hi = forced = free = 0
    gaps = []
    impares = 0
    for o in orbits:
        c = sum(par[k] for k in o)
        s = len(o)
        if s % 2:
            impares += 1
        lo += min(c, s - c)
        hi += max(c, s - c)
        if 2 * c == s:
            forced += 1
        else:
            free += 1
            gaps.append(abs(s - 2 * c))
    reach = {0}
    for g in gaps:
        reach |= {r + g for r in reach}
    alcanzables = sorted(lo + r for r in reach)
    observado = sum(st)
    empate = denom // 2
    assert lo <= observado <= hi
    if hi - lo == 0:
        casilla = "FORZADO"
    elif empate in alcanzables:
        casilla = "INTERVALO"
    else:
        casilla = "PROHIBIDO"
    return {
        "orbitas": len(orbits), "forzadas": forced, "libres": free,
        "impares": impares, "minimo": lo, "maximo": hi, "anchura": hi - lo,
        "observado": observado, "alcanzables": len(alcanzables),
        "empate_alcanzable": int(empate in alcanzables), "casilla": casilla,
        "denominador": denom, "empate": empate,
    }


# --- las ordenaciones declaradas ---------------------------------------------

def orden_binario(n, valh):
    return sorted(range(1 << n), key=lambda x: valh[x])


def gray(n):
    """Codigo de Gray reflejado tal y como lo declara DEFINICIONES-GENERAL.md:
    la linea que se anade en cada paso es la MAS significativa de la convencion
    de referencia, es decir la linea 1. En enteros, eso desplaza lo anterior un
    bit hacia arriba y pone el bit 0 en la mitad reflejada.

    La version anterior de esta funcion anadia el bit mas alto, que bajo la
    convencion de referencia es la linea menos significativa, y por tanto NO era
    la ordenacion declarada. El error y sus consecuencias estan en
    PROOFS-GENERAL.md pieza 3 y en la enmienda 2 de INFORME-GENERAL.md."""
    out = [0]
    for _ in range(n):
        out = [x << 1 for x in out] + [(x << 1) | 1 for x in reversed(out)]
    return out


def mawangdui_like(n, k, pi, rho):
    """Posicion i*2^k + j lleva el vertice de parte alta pi[i] y parte baja rho[j]."""
    return [(pi[i] << k) | rho[j] for i in range(1 << (n - k)) for j in range(1 << k)]


# --- programa ------------------------------------------------------------------

def main():
    emit("semilla", SEED, "la ya congelada en el repositorio")
    emit("repeticiones.donde.se.muestrea", REPS, "por combinacion de n y k")
    emit("umbral.de.enumeracion.entera", UMBRAL,
         "si el espacio de pares de permutaciones no pasa de aqui se recorre "
         "entero; si lo pasa, se muestrea")

    for n in (3, 4, 5):
        N = 1 << n
        FAM = affine_group(n)
        valh = value_table(n, "yang1", "bottomMSB")
        denom = comb(N, 2)
        emit("n%d.vertices" % n, N, "")
        emit("n%d.denominador" % n, denom, "C(2^n, 2)")
        emit("n%d.empate" % n, denom // 2, "")
        emit("n%d.orden.de.B_n" % n, len(FAM), "n! por 2^n")

        # O1, control degenerado
        seq = orden_binario(n, valh)
        vals = [valh[x] for x in seq]
        cero = sum(1 for i in range(N) for j in range(i + 1, N) if vals[i] > vals[j])
        check("n%d.O1.el.orden.binario.da.cero.pares.discordantes" % n, cero == 0,
              "control de que el aparato no inventa nada")

        # totales en las cuatro convenciones, para las dos ordenaciones fijas
        for nombre, s in (("Gray", gray(n)), ("MWDlike.canonica", None)):
            for pol in POLARITIES:
                for end in ENDIANS:
                    vt = value_table(n, pol, end)
                    if s is None:
                        continue
                    v = [vt[x] for x in s]
                    inv = sum(1 for i in range(N) for j in range(i + 1, N) if v[i] > v[j])
                    emit("n%d.total.%s.%s.%s" % (n, nombre, pol, end), inv, "")

        # la rejilla entera de k
        for k in range(1, n):
            size = 1 << k
            etiqueta = "n%d.k%d" % (n, k)
            es_mwd = (n % 2 == 0 and k == n // 2)
            emit("%s.es.el.analogo.de.mawangdui" % etiqueta, int(es_mwd),
                 "solo definido cuando n es par y k es la mitad")

            for nombre, s in (("Gray", gray(n)),
                              ("MWDlike.canonica",
                               mawangdui_like(n, k, list(range(1 << (n - k))),
                                              list(range(size))))):
                G = group_R1(s, size, FAM)
                gens = generators_of(G, FAM, N)
                pred = factorial(k) * factorial(n - k) * N
                emit("%s.%s.grupo.orden" % (etiqueta, nombre), len(G), "")
                emit("%s.%s.grupo.orden.predicho" % (etiqueta, nombre), pred,
                     "k! por (n-k)! por 2^n, la prediccion de b.4 de la preinscripcion")
                emit("%s.%s.grupo.coincide.con.lo.predicho" % (etiqueta, nombre),
                     int(len(G) == pred), "")
                r = accounting(s, gens, valh, N)
                for key in ("orbitas", "forzadas", "libres", "impares", "minimo",
                            "maximo", "anchura", "observado", "alcanzables",
                            "empate_alcanzable", "casilla"):
                    emit("%s.%s.%s" % (etiqueta, nombre, key), r[key], "")
                if r["anchura"] == 0:
                    check("%s.%s.si.fuerza.el.valor.es.el.empate" % (etiqueta, nombre),
                          r["minimo"] == denom // 2,
                          "corolario del Lema 1; si fallara seria error de aparato")

            # O3 muestreada o enumerada
            nb, ni = 1 << (n - k), size
            espacio = factorial(nb) * factorial(ni)
            enumerable = (espacio <= UMBRAL)
            emit("%s.O3.espacio.de.pares.de.permutaciones" % etiqueta, espacio, "")
            emit("%s.O3.enumerado.entero" % etiqueta, int(enumerable),
                 "si es cero, se muestreo con la semilla declarada")
            casillas = {}
            ordenes = set()
            if enumerable:
                casos = ((list(p), list(q)) for p in itertools.permutations(range(nb))
                         for q in itertools.permutations(range(ni)))
                total = espacio
            else:
                rng = random.Random(SEED)
                casos = ((rng.sample(range(nb), nb), rng.sample(range(ni), ni))
                         for _ in range(REPS))
                total = REPS
            for pi, rho in casos:
                s = mawangdui_like(n, k, pi, rho)
                G = group_R1(s, size, FAM)
                ordenes.add(len(G))
                gens = generators_of(G, FAM, N)
                r = accounting(s, gens, valh, N)
                casillas[r["casilla"]] = casillas.get(r["casilla"], 0) + 1
            emit("%s.O3.casos" % etiqueta, total, "")
            for c in ("FORZADO", "INTERVALO", "PROHIBIDO"):
                emit("%s.O3.%s" % (etiqueta, c), casillas.get(c, 0), "")
            emit("%s.O3.ordenes.de.grupo.distintos" % etiqueta,
                 " ".join(str(x) for x in sorted(ordenes)),
                 "el grupo solo depende de la particion, no del orden")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Primera medicion de la fase general, n = 3, 4, 5.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/general-landscape.tsv con %d cifras" % len(ROWS))
    for key, val, _ in ROWS:
        if ".casilla" in key or ".O3." in key or "grupo.orden" in key or "total." in key:
            print("  %-52s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
