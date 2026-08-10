#!/usr/bin/env python3
"""
Fase previa a la firma de PREREGISTRATION-GENERAL.md: decidir por demostracion
lo decidible sobre las hipotesis de la obstruccion de paridad.

La obstruccion, tal y como quedo demostrada para n = 6 en PROOFS.md 3.3, se
apoyaba en tres hipotesis sobre un grupo T de traslaciones contenido en G:

  H1  T son las traslaciones por un subespacio V de F_2^n, contenido en G
  H2  T es normal en G
  H3  dim V es al menos 2

Este programa NO mide el paisaje de n = 3, 4, 5. No calcula recuentos, ni
intervalos, ni clasifica construcciones. Solo mira tamanos de orbitas de la
accion de un grupo sobre pares de vertices, que es lo unico que la obstruccion
necesita.

Observacion que hace todo esto independiente de la ordenacion: la accion sobre
pares de POSICIONES es conjugada por sigma de la accion sobre pares de
VERTICES, luego los tamanos de orbita no dependen de sigma. Se comprueba abajo.

Salida: results/parity-hypotheses.tsv

  python src/parity_hypotheses.py
"""

import itertools
import os
import sys
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "parity-hypotheses.tsv")
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


# --- el grupo afin B_n sobre F_2^n -------------------------------------------

def affine_group(n):
    """Todas las x -> P(x) XOR m, como tuplas de imagenes. Orden n! por 2^n."""
    N = 1 << n
    out = {}
    for perm in itertools.permutations(range(n)):
        table = [sum(((x >> perm[k]) & 1) << k for k in range(n)) for x in range(N)]
        for m in range(N):
            out[tuple(t ^ m for t in table)] = (perm, m)
    return out


def compose(f, g):
    return tuple(f[x] for x in g)


def closure(gens, N):
    ident = tuple(range(N))
    seen, frontier = {ident}, [ident]
    while frontier:
        cur = frontier.pop()
        for g in gens:
            nxt = compose(g, cur)
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def translation(v, N):
    return tuple(x ^ v for x in range(N))


def pair_orbits(group, N):
    """Orbitas de la accion sobre pares no ordenados de vertices."""
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
    index = {p: k for k, p in enumerate(pairs)}
    seen = [-1] * len(pairs)
    orbits = []
    for start in range(len(pairs)):
        if seen[start] != -1:
            continue
        o = len(orbits)
        stack, members = [start], [start]
        seen[start] = o
        while stack:
            cur = stack.pop()
            a, b = pairs[cur]
            for g in group:
                u, w = g[a], g[b]
                k = index[(u, w) if u < w else (w, u)]
                if seen[k] == -1:
                    seen[k] = o
                    stack.append(k)
                    members.append(k)
        orbits.append([pairs[k] for k in members])
    return orbits


def translations_of(group, N):
    """Vectores v tales que la traslacion por v esta en el grupo."""
    return [v for v in range(N) if translation(v, N) in group]


def span(vectors):
    s = {0}
    for v in vectors:
        s |= {x ^ v for x in s}
    return s


def linear_parts(group, N, FAM):
    return set(FAM[g][0] for g in group)


def image_of_subspace(V, perm, n):
    return span([sum(((v >> perm[k]) & 1) << k for k in range(n)) for v in V])


# --- programa ------------------------------------------------------------------

def main():
    # --- 0. los tamanos de orbita no dependen de la ordenacion --------------
    n = 3
    N = 1 << n
    FAM = affine_group(n)
    emit("familia.afin.n3.orden", len(FAM), "n! por 2^n")
    G = closure([translation(1, N), translation(2, N)], N)
    sigma = [5, 0, 7, 2, 1, 6, 3, 4]          # una ordenacion cualquiera
    pos = {h: i for i, h in enumerate(sigma)}
    tam_vert = sorted(len(o) for o in pair_orbits(G, N))
    pares = [(a, b) for a in range(N) for b in range(a + 1, N)]
    idx = {p: k for k, p in enumerate(pares)}
    seen = [-1] * len(pares)
    tam_pos = []
    for s in range(len(pares)):
        if seen[s] != -1:
            continue
        stack, cnt = [s], 0
        seen[s] = 1
        while stack:
            cur = stack.pop()
            cnt += 1
            i, j = pares[cur]
            x, y = sigma[i], sigma[j]
            for g in G:
                a, b = pos[g[x]], pos[g[y]]
                k = idx[(a, b) if a < b else (b, a)]
                if seen[k] == -1:
                    seen[k] = 1
                    stack.append(k)
        tam_pos.append(cnt)
    check("t0.los.tamanos.de.orbita.no.dependen.de.la.ordenacion",
          sorted(tam_pos) == tam_vert,
          "la accion sobre pares de posiciones es conjugada por sigma de la de pares de vertices")

    # --- 1. H3, dim V al menos 2: TESTIGO de que no se puede quitar ---------
    # G = {identidad, traslacion por v}. Cumple H1 y H2 (es abeliano, luego T es
    # normal en el), tiene dim V igual a 1, y falla la conclusion.
    for n in (2, 3, 4):
        N = 1 << n
        v = 1
        T = closure([translation(v, N)], N)
        emit("t1.n%d.orden.del.grupo" % n, len(T), "G igual a T igual a {id, traslacion por v}")
        vs = translations_of(T, N)
        emit("t1.n%d.dimension.del.subespacio.de.traslaciones" % n,
             len(span([x for x in vs if x])).bit_length() - 1, "log2 del cardinal del span")
        orbs = pair_orbits(T, N)
        impares = [o for o in orbs if len(o) % 2]
        emit("t1.n%d.orbitas.de.pares" % n, len(orbs), "")
        emit("t1.n%d.orbitas.de.cardinal.impar" % n, len(impares), "")
        check("t1.n%d.hay.orbita.impar" % n, len(impares) > 0,
              "testigo de que H3 no se puede quitar")
        testigo = min((o[0] for o in impares))
        emit("t1.n%d.testigo" % n, "par {%d, %d}, orbita de cardinal 1" % testigo,
             "los dos vertices difieren exactamente en v, luego la traslacion los intercambia")
        check("t1.n%d.el.testigo.es.un.par.que.difiere.en.v" % n,
              (testigo[0] ^ testigo[1]) == v)
        check("t1.n%d.T.actua.libremente" % n,
              all(t[x] != x for t in T if t != tuple(range(N)) for x in range(N)))
        check("t1.n%d.T.es.normal.en.G" % n, True, "G es igual a T, luego T es normal en G")

    # --- 2. H2, normalidad: NO es una hipotesis, es redundante --------------
    # Si G contiene las traslaciones por V con dim V al menos 2, entonces G
    # contiene tambien las traslaciones por W, el span de todas las imagenes de
    # V bajo las partes lineales de G, y esas SI son normales, con dim W al
    # menos dim V. Luego la conclusion vale sin pedir normalidad de T.
    n = 3
    N = 1 << n
    FAM = affine_group(n)
    V = span([1, 2])                            # subespacio de dimension 2
    perm = (0, 2, 1)                            # intercambia las coordenadas 1 y 2
    P = tuple(sum(((x >> perm[k]) & 1) << k for k in range(n)) for x in range(N))
    G = closure([translation(v, N) for v in V if v] + [P], N)
    emit("t2.orden.del.grupo", len(G), "generado por las traslaciones por V y una permutacion")
    emit("t2.dim.V", 2, "V es el span de e0 y e1")

    # T no es normal en G
    T = set(translation(v, N) for v in V)
    no_normal = any(compose(compose(g, t), inv(g, N)) not in T for g in G for t in T)
    check("t2.T.NO.es.normal.en.G", no_normal, "hay un conjugado de T fuera de T")

    # W, el span de las imagenes de V, y sus traslaciones dentro de G
    lin = linear_parts(G, N, FAM)
    W = span([w for p in lin for w in image_of_subspace(V, p, n)])
    emit("t2.dim.W", len(W).bit_length() - 1, "W es el span de las imagenes de V")
    check("t2.dim.W.es.al.menos.dim.V", len(W) >= len(V))
    TW = set(translation(w, N) for w in W)
    check("t2.las.traslaciones.por.W.estan.en.G", TW <= G)
    check("t2.las.traslaciones.por.W.son.normales.en.G",
          all(compose(compose(g, t), inv(g, N)) in TW for g in G for t in TW))

    orbs = pair_orbits(G, N)
    emit("t2.orbitas.de.pares", len(orbs), "")
    emit("t2.orbitas.de.cardinal.impar", sum(1 for o in orbs if len(o) % 2), "")
    check("t2.todas.las.orbitas.son.de.cardinal.par",
          all(len(o) % 2 == 0 for o in orbs),
          "la conclusion vale aunque T no sea normal, por el paso al cierre normal")

    # --- 3. la conclusion, comprobada en una familia declarada --------------
    # Para n en {2,3} y TODO subespacio V con dim V al menos 2, y para el grupo
    # generado por las traslaciones por V mas cada permutacion de coordenadas,
    # se comprueba que ninguna orbita de pares tiene cardinal impar.
    total = 0
    for n in (2, 3):
        N = 1 << n
        subespacios = set()
        for r in (2, 3):
            if r > n:
                continue
            for base in itertools.combinations(range(1, N), r):
                s = span(base)
                if len(s) == (1 << r):
                    subespacios.add(frozenset(s))
        for V in subespacios:
            for perm in itertools.permutations(range(n)):
                P = tuple(sum(((x >> perm[k]) & 1) << k for k in range(n)) for x in range(N))
                G = closure([translation(v, N) for v in V if v] + [P], N)
                orbs = pair_orbits(G, N)
                assert all(len(o) % 2 == 0 for o in orbs), "contraejemplo a la conclusion"
                total += 1
    emit("t3.casos.comprobados", total,
         "n en 2 y 3, todo subespacio de dimension al menos 2, y toda permutacion de coordenadas")
    check("t3.ninguna.orbita.impar.en.esos.casos", True)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Fase previa a la firma: hipotesis de la obstruccion de paridad.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/parity-hypotheses.tsv con %d lineas" % len(ROWS))
    for key, val, _ in ROWS:
        print("  %-58s %s" % (key, val))
    return 0


def inv(g, N):
    out = [0] * N
    for x in range(N):
        out[g[x]] = x
    return tuple(out)


if __name__ == "__main__":
    sys.exit(main())
