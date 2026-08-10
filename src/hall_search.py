#!/usr/bin/env python3
"""
Busqueda acotada de un fallo de Hall.

OBJETIVO, declarado antes de correr y transcrito de la instruccion que abrio la
sesion: decidir si existe una orbita forzada **sin** emparejamiento del Lema 3,
es decir un fallo de la condicion de Hall, dentro de un espacio declarado.

ESPACIO, declarado antes de correr:

  1. las 472 ordenaciones forzadas de B(3,1), enteras;
  2. las 600 ordenaciones forzadas de B(3,2), enteras;
  3. una muestra de ordenaciones forzadas de B(4,2), halladas por el criterio
     del Teorema 2 de PROOFS-B31.md, que las hace baratas de encontrar. Tamano
     declarado: 200 ordenaciones distintas. Semilla: la ya congelada, 20260809.
     Tope de tiempo: 180 segundos de busqueda; si no se completan las 200, se
     reporta cuantas se obtuvieron y que el corte fue por tiempo.

DOS RAMAS, escritas antes:

  - si aparece un fallo, es hallazgo, y la direccion enumerativa del candidato
    C1 queda REFUTADA como equivalencia, con testigo;
  - si no aparece, el estatus queda "enumerativo en N casos", con N medido, y
    NO se promueve a teorema.

Herencia de verificaciones, por la enmienda 3 de CONTACT-RULES.md: se reusa el
aparato de src/general_landscape.py sin reimplementarlo, y se heredan al arrancar
las comprobaciones del orden del grupo y de la particion 472 y 600.

Salida: results/hall-search.tsv

  python src/hall_search.py
"""

import itertools
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import general_landscape as GL                             # noqa: E402

OUT = os.path.join(ROOT, "results", "hall-search.tsv")
SEED = 20260809
OBJETIVO_N4 = 200
TOPE_SEGUNDOS = 180
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


def pares(N):
    return [(i, j) for i in range(N) for j in range(i + 1, N)]


def orbitas_y_paridad(seq, gens, valh, N, PAIRS, PINDEX):
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]
    pis = [[posof[g[seq[i]]] for i in range(N)] for g in gens]

    def step(gi, k):
        g, pi = gens[gi], pis[gi]
        i, j = PAIRS[k]
        a, b = pi[i], pi[j]
        A = 1 if a > b else 0
        B = 1 if ((valh[g[seq[i]]] > valh[g[seq[j]]]) != (vals[i] > vals[j])) else 0
        return PINDEX[(a, b) if a < b else (b, a)], A ^ B

    oid = [-1] * len(PAIRS)
    par = [0] * len(PAIRS)
    orbits = []
    for start in range(len(PAIRS)):
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
    return orbits, par


def hall(seq, group, valh, orbita, N, PAIRS, PINDEX, par):
    """
    Comprueba la condicion de Hall del grafo bipartito de la relacion dentro de
    una orbita forzada. Devuelve (hay_emparejamiento, testigo_o_None).

    Las dos clases son las de paridad, que en una orbita forzada tienen el mismo
    cardinal. Toda arista une paridades contrarias, asi que el grafo es
    bipartito entre ellas y basta buscar emparejamiento perfecto.
    """
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]
    ms = set(orbita)
    izq = [k for k in orbita if par[k] == 0]
    der = [k for k in orbita if par[k] == 1]
    if len(izq) != len(der):
        return None, None                      # no es forzada, no toca aqui
    adj = {k: set() for k in izq}
    for g in group:
        gs = [g[h] for h in seq]
        for k in izq:
            i, j = PAIRS[k]
            a, b = posof[gs[i]], posof[gs[j]]
            A = 1 if a > b else 0
            B = 1 if ((valh[gs[i]] > valh[gs[j]]) != (vals[i] > vals[j])) else 0
            if (A ^ B) != 1:
                continue
            q = PINDEX[(a, b) if a < b else (b, a)]
            if q != k and q in ms:
                adj[k].add(q)
    match = {}

    def aug(u, seen):
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match or aug(match[v], seen):
                match[v] = u
                match[u] = v
                return True
        return False

    n = 0
    for u in izq:
        if u not in match and aug(u, set()):
            n += 1
    if n == len(izq):
        return True, None
    # testigo de Hall: un subconjunto de la izquierda con vecindad menor
    sin_emparejar = [u for u in izq if u not in match]
    u0 = sin_emparejar[0]
    alcanzados_izq, alcanzados_der = {u0}, set()
    frontera = [u0]
    while frontera:
        u = frontera.pop()
        for v in adj[u]:
            if v not in alcanzados_der:
                alcanzados_der.add(v)
                w = match.get(v)
                if w is not None and w not in alcanzados_izq:
                    alcanzados_izq.add(w)
                    frontera.append(w)
    return False, (sorted(alcanzados_izq), sorted(alcanzados_der))


def clases_de_diferencia(N, lineales):
    """Clases de diferencia: orbitas de d distinto de cero bajo las partes lineales."""
    visto, clases = set(), []
    for d in range(1, N):
        if d in visto:
            continue
        c = set()
        for perm in lineales:
            e = sum(((d >> perm[k]) & 1) << k for k in range(len(perm)))
            c.add(e)
        visto |= c
        clases.append(sorted(c))
    return clases


def es_forzada_por_criterio(seq, valh, clases, N):
    """Teorema 2 de PROOFS-B31.md: la mitad de discordantes en cada clase."""
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]
    cnt = {}
    for i in range(N):
        for j in range(i + 1, N):
            d = seq[i] ^ seq[j]
            cnt.setdefault(d, [0, 0])
            cnt[d][0] += 1
            cnt[d][1] += 1 if vals[i] > vals[j] else 0
    dev = 0
    for c in clases:
        tot = sum(cnt[d][0] for d in c)
        dis = sum(cnt[d][1] for d in c)
        dev += abs(2 * dis - tot)
    return dev


def main():
    t0 = time.time()
    emit("semilla", SEED, "la ya congelada en el repositorio")
    emit("objetivo.muestra.n4", OBJETIVO_N4, "ordenaciones forzadas distintas de B(4,2)")
    emit("tope.de.busqueda.segundos", TOPE_SEGUNDOS, "")

    total_orbitas = 0
    total_ordenaciones = 0
    fallos = []

    # --- 1 y 2: n = 3, las dos particiones, enteras ----------------------
    N = 8
    FAM3 = GL.affine_group(3)
    valh3 = GL.value_table(3, "yang1", "bottomMSB")
    P3, PI3 = pares(N), None
    PI3 = {p: k for k, p in enumerate(P3)}
    for k, esperado in ((1, 472), (2, 600)):
        G = GL.group_R1(list(range(N)), 1 << k, FAM3)
        gens = GL.generators_of(G, FAM3, N)
        check("herencia.n3.k%d.orden.del.grupo" % k, len(G) == 16)
        forzadas = []
        for perm in itertools.permutations(range(N)):
            seq = list(perm)
            orbits, par = orbitas_y_paridad(seq, gens, valh3, N, P3, PI3)
            if all(2 * sum(par[x] for x in o) == len(o) for o in orbits):
                forzadas.append((seq, orbits, par))
        emit("n3.k%d.forzadas" % k, len(forzadas), "sobre las 40320 ordenaciones")
        check("herencia.n3.k%d.la.particion.coincide.con.lo.ya.medido" % k,
              len(forzadas) == esperado)
        orb_k = fall_k = 0
        for seq, orbits, par in forzadas:
            total_ordenaciones += 1
            for o in orbits:
                ok, testigo = hall(seq, G, valh3, o, N, P3, PI3, par)
                orb_k += 1
                if ok is False:
                    fall_k += 1
                    fallos.append(("n3.k%d" % k, seq, o, testigo))
        emit("n3.k%d.orbitas.forzadas.verificadas" % k, orb_k, "")
        emit("n3.k%d.fallos.de.Hall" % k, fall_k, "")
        total_orbitas += orb_k

    # --- 3: n = 4, k = 2, muestra hallada por el criterio ----------------
    n, k = 4, 2
    N4 = 1 << n
    FAM4 = GL.affine_group(n)
    valh4 = GL.value_table(n, "yang1", "bottomMSB")
    P4 = pares(N4)
    PI4 = {p: kk for kk, p in enumerate(P4)}
    G4 = GL.group_R1(list(range(N4)), 1 << k, FAM4)
    gens4 = GL.generators_of(G4, FAM4, N4)
    emit("n4.k2.orden.del.grupo", len(G4), "")
    check("herencia.n4.k2.orden.es.k!.por.(n-k)!.por.2^n", len(G4) == 2 * 2 * 16)
    lineales = sorted(set(FAM4[g][0] for g in G4))
    clases = clases_de_diferencia(N4, lineales)
    emit("n4.k2.clases.de.diferencia", len(clases), "orbitas de la diferencia bajo las partes lineales")

    rng = random.Random(SEED)
    encontradas, vistas = [], set()
    intentos = 0
    corte = "objetivo alcanzado"
    while len(encontradas) < OBJETIVO_N4:
        if time.time() - t0 > TOPE_SEGUNDOS:
            corte = "tope de tiempo"
            break
        intentos += 1
        seq = rng.sample(range(N4), N4)
        dev = es_forzada_por_criterio(seq, valh4, clases, N4)
        # descenso por intercambios, aceptando solo mejoras
        for _ in range(4000):
            if dev == 0:
                break
            i, j = rng.randrange(N4), rng.randrange(N4)
            if i == j:
                continue
            seq[i], seq[j] = seq[j], seq[i]
            nuevo = es_forzada_por_criterio(seq, valh4, clases, N4)
            if nuevo <= dev:
                dev = nuevo
            else:
                seq[i], seq[j] = seq[j], seq[i]
        if dev == 0 and tuple(seq) not in vistas:
            vistas.add(tuple(seq))
            encontradas.append(list(seq))
    emit("n4.k2.intentos.de.busqueda", intentos, "")
    emit("n4.k2.forzadas.encontradas", len(encontradas), "")
    emit("n4.k2.corte", corte, "")

    orb4 = fall4 = 0
    for seq in encontradas:
        orbits, par = orbitas_y_paridad(seq, gens4, valh4, N4, P4, PI4)
        # el criterio del Teorema 2 y la contabilidad tienen que coincidir
        assert all(2 * sum(par[x] for x in o) == len(o) for o in orbits), \
            "el criterio del Teorema 2 no coincide con la contabilidad"
        total_ordenaciones += 1
        for o in orbits:
            ok, testigo = hall(seq, G4, valh4, o, N4, P4, PI4, par)
            orb4 += 1
            if ok is False:
                fall4 += 1
                fallos.append(("n4.k2", seq, o, testigo))
    emit("n4.k2.orbitas.forzadas.verificadas", orb4, "")
    emit("n4.k2.fallos.de.Hall", fall4, "")
    check("n4.k2.el.criterio.del.teorema.2.coincide.con.la.contabilidad", True,
          "comprobado en las %d ordenaciones encontradas" % len(encontradas))
    total_orbitas += orb4

    # --- desenlace --------------------------------------------------------
    emit("ordenaciones.forzadas.recorridas", total_ordenaciones, "")
    emit("orbitas.forzadas.verificadas", total_orbitas, "")
    emit("fallos.de.Hall", len(fallos), "")
    if fallos:
        etq, seq, o, testigo = fallos[0]
        emit("testigo.caso", etq, "")
        emit("testigo.ordenacion", " ".join(str(x) for x in seq), "")
        emit("testigo.subconjunto.izquierda", len(testigo[0]), "")
        emit("testigo.vecindad", len(testigo[1]), "menor que el subconjunto, eso es el fallo")
        emit("desenlace", "RAMA UNO: hay fallo de Hall", "C1 refutado como equivalencia")
    else:
        emit("desenlace", "RAMA DOS: ningun fallo de Hall", "estatus enumerativo, no se promueve a teorema")
    emit("segundos.totales", round(time.time() - t0, 1), "")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Busqueda acotada de un fallo de Hall.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/hall-search.tsv con %d lineas" % len(ROWS))
    for key, val, _ in ROWS:
        print("  %-52s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
