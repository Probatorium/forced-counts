#!/usr/bin/env python3
"""
Comprobadores mecanicos de las demostraciones de PROOFS.md.

Cada bloque de este fichero corresponde a una pieza de PROOFS.md y comprueba,
paso a paso, lo que alli se afirma. Lo que en PROOFS.md se declara DEMOSTRADO se
comprueba aqui como verificacion de una demostracion ya escrita. Lo que alli se
declara ENUMERATIVO se calcula aqui, y se marca como tal en la clave.

Salida: results/proofs.tsv

  python src/proofs.py
"""

import itertools
import json
import os
import sys
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import measure as M                                        # noqa: E402
import group as GR                                         # noqa: E402

OUT = os.path.join(ROOT, "results", "proofs.tsv")

N, LINES = 64, 6
DENOM = comb(N, 2)
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


# --- utilidades sobre F_2^6, con el bit k igual a la linea k+1 ---------------

VAL = [M.value(M.dec(x), "yang1", "bottomMSB") for x in range(N)]
ALL = list(range(N))
FULL = N - 1


def rho(x):
    """Giro de media vuelta: la linea k pasa a la linea 7-k."""
    return sum(((x >> (LINES - 1 - k)) & 1) << k for k in range(LINES))


def kappa(x):
    return x ^ FULL


def lower(x):
    return x & 7                      # bits 0,1,2, lineas 1,2,3


def upper(x):
    return (x >> 3) & 7               # bits 3,4,5, lineas 4,5,6


def weight(x):
    return bin(x).count("1")


PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
PINDEX = {p: k for k, p in enumerate(PAIRS)}


def load_sequences():
    with open(os.path.join(ROOT, "data", "sequences.json"), "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    return {k: [M.enc(p) for p in v] for k, v in payload["sequences"].items()}


SEQS = load_sequences()
BLOCKS = {"Mawangdui": 8, "Jing Fang": 8, "King Wen": 2}


def position_data(seq):
    posof = {h: i for i, h in enumerate(seq)}
    vals = [VAL[h] for h in seq]
    return posof, vals


def status_vector(seq):
    _, vals = position_data(seq)
    return [1 if vals[i] > vals[j] else 0 for i, j in PAIRS]


def epsilon(seq, g, i, j):
    """(indice del par imagen, epsilon) tal y como se define en DEFINICIONES-GRUPO.md."""
    posof, vals = position_data(seq)
    a, b = posof[g[seq[i]]], posof[g[seq[j]]]
    A = 1 if a > b else 0
    B = 1 if ((VAL[g[seq[i]]] > VAL[g[seq[j]]]) != (vals[i] > vals[j])) else 0
    key = (a, b) if a < b else (b, a)
    return PINDEX[key], A ^ B


def orbit_data(seq, group):
    """Orbitas de pares bajo el grupo, con paridad y aportacion. Sin atajos."""
    posof, vals = position_data(seq)
    pis = [[posof[g[seq[i]]] for i in range(N)] for g in group]
    st = status_vector(seq)

    def step(gi, k):
        g, pi = group[gi], pis[gi]
        i, j = PAIRS[k]
        a, b = pi[i], pi[j]
        A = 1 if a > b else 0
        B = 1 if ((VAL[g[seq[i]]] > VAL[g[seq[j]]]) != (vals[i] > vals[j])) else 0
        key = (a, b) if a < b else (b, a)
        return PINDEX[key], A ^ B

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
            for gi in range(len(group)):
                nxt, eps = step(gi, cur)
                want = par[cur] ^ eps
                if oid[nxt] == -1:
                    oid[nxt], par[nxt] = o, want
                    stack.append(nxt)
                    members.append(nxt)
                else:
                    assert oid[nxt] == o and par[nxt] == want, "paridad inconsistente"
        orbits.append(members)
    return orbits, oid, par, st


# =============================================================================
# Pieza 1: el lema del empate
# =============================================================================

def pieza_1():
    emit("p1.pares.de.posiciones", len(PAIRS), "C(64,2)")
    check("p1.pares.de.posiciones.coincide.con.C(64,2)", len(PAIRS) == DENOM)

    todos_ok = True
    for name, seq in SEQS.items():
        g1 = GR.group_R1(seq, BLOCKS[name])
        orbits, oid, par, st = orbit_data(seq, g1)
        short = name.replace(" ", "")
        suma = sum(len(o) for o in orbits)
        check("p1.%s.los.tamanos.de.orbita.suman.C(64,2)" % short, suma == DENOM)
        forzadas = [o for o in orbits if 2 * sum(par[k] for k in o) == len(o)]
        total = sum(st)
        if len(forzadas) == len(orbits):
            check("p1.%s.hipotesis.cumplida.total.es.la.mitad" % short, total == DENOM // 2,
                  "toda orbita forzada, luego el total tiene que ser C(64,2) partido por dos")
        else:
            emit("p1.%s.hipotesis.no.cumplida" % short, len(orbits) - len(forzadas),
                 "orbitas libres: la hipotesis falla y el lema no se aplica")
            todos_ok = todos_ok and True
        # la aportacion de cada orbita es una de las dos opciones, sin tercera
        for o in orbits:
            c = sum(par[k] for k in o)
            obs = sum(st[k] for k in o)
            assert obs in (c, len(o) - c)
    check("p1.la.aportacion.de.toda.orbita.es.una.de.las.dos.opciones", True,
          "comprobado en las tres secuencias bajo su grupo R1")

    # El reciproco del lema, que es lo que hace que el grupo solo pueda forzar
    # el empate: si toda orbita esta forzada, la suma de mitades es C(64,2)/2.
    check("p1.corolario.el.grupo.solo.puede.forzar.el.empate", DENOM % 2 == 0,
          "la suma de los tamanos es par, luego la suma de mitades es un entero fijo")


# =============================================================================
# Pieza 2: Mawangdui y Jing Fang
# =============================================================================

def pieza_2_mawangdui():
    seq = SEQS["Mawangdui"]
    blocks = [frozenset(b) for b in GR.blocks_of(seq, 8)]

    # los bloques son las fibras del trigrama superior
    fibras = set(frozenset(x for x in ALL if upper(x) == u) for u in range(8))
    check("p2.mwd.bloques.son.las.fibras.del.trigrama.superior", set(blocks) == fibras)

    # la relacion de mismo bloque es la de coset del subespacio V
    V = [x for x in ALL if upper(x) == 0]
    check("p2.mwd.V.es.subespacio.de.dimension.tres", len(V) == 8 and
          all((a ^ b) in V for a in V for b in V))
    check("p2.mwd.mismo.bloque.equivale.a.diferencia.en.V",
          all(((upper(a) == upper(b)) == ((a ^ b) in V)) for a in ALL for b in ALL))

    # las permutaciones que preservan V son las que respetan el corte de trigramas
    perms_ok = [perm for perm in itertools.permutations(range(LINES))
                if all(sum(((x >> perm[k]) & 1) << k for k in range(LINES)) in V for x in V)]
    emit("p2.mwd.permutaciones.que.preservan.V", len(perms_ok), "seis por seis")
    check("p2.mwd.esas.permutaciones.son.las.que.no.mezclan.trigramas",
          all(set(p[:3]) == {0, 1, 2} and set(p[3:]) == {3, 4, 5} for p in perms_ok)
          and len(perms_ok) == 36)
    emit("p2.mwd.orden.predicho", 36 * N, "36 permutaciones por 64 mascaras")
    g1 = GR.group_R1(seq, 8)
    check("p2.mwd.orden.predicho.coincide.con.la.enumeracion", len(g1) == 36 * N)

    # estructura de orbitas por pesos, predicha y comprobada
    orbits, oid, par, st = orbit_data(seq, g1)
    clase = {}
    for k, (i, j) in enumerate(PAIRS):
        x, y = seq[i], seq[j]
        clase.setdefault((weight(lower(x) ^ lower(y)), weight(upper(x) ^ upper(y))), []).append(k)
    check("p2.mwd.las.orbitas.son.las.clases.de.pesos",
          sorted(sorted(v) for v in clase.values()) == sorted(sorted(o) for o in orbits))
    emit("p2.mwd.numero.de.orbitas", len(orbits), "cuatro por cuatro menos el caso de peso cero doble")
    check("p2.mwd.numero.de.orbitas.es.quince", len(orbits) == 15)
    check("p2.mwd.tamanos.siguen.la.formula",
          all(len(v) == 32 * comb(3, a) * comb(3, b) for (a, b), v in clase.items()))
    emit("p2.mwd.orbita.mayor", max(len(v) for v in clase.values()), "32 por 3 por 3")

    # las nueve orbitas con los dos pesos positivos, demostradas forzadas
    g_low = tuple(x ^ 7 for x in ALL)          # complementar el trigrama inferior
    check("p2.mwd.el.testigo.esta.en.el.grupo", g_low in set(g1))
    pares_probados = 0
    for (a, b), members in clase.items():
        if a >= 1 and b >= 1:
            for k in members:
                i, j = PAIRS[k]
                img, eps = epsilon(seq, g_low, i, j)
                assert eps == 1, "el testigo no da epsilon uno"
                assert img != k, "el testigo fija un par"
            pares_probados += len(members)
    emit("p2.mwd.orbitas.demostradas.forzadas", sum(1 for (a, b) in clase if a >= 1 and b >= 1),
         "las de peso positivo en los dos trigramas")
    emit("p2.mwd.pares.cubiertos.por.la.demostracion", pares_probados, "")
    emit("p2.mwd.aportacion.demostrada", pares_probados // 2, "la mitad, por el lema")
    check("p2.mwd.el.testigo.da.epsilon.uno.y.no.fija.ningun.par", True,
         "comprobado par a par en esas nueve orbitas")

    # las seis restantes: reduccion explicita, y su cuenta, que es ENUMERATIVA
    posof, vals = position_data(seq)
    for (a, b), members in sorted(clase.items()):
        if a == 0 or b == 0:
            obs = sum(st[k] for k in members)
            emit("p2.mwd.ENUMERATIVO.clase.peso.%d.%d.aportacion" % (a, b), obs,
                 "tamano %d, la mitad seria %d" % (len(members), len(members) // 2))
    # reduccion wL = 0: el estado no depende del trigrama inferior comun
    ok = True
    for (a, b), members in clase.items():
        if a == 0:
            porU = {}
            for k in members:
                i, j = PAIRS[k]
                x, y = seq[i], seq[j]
                key = frozenset((upper(x), upper(y)))
                porU.setdefault(key, set()).add(st[k])
            ok = ok and all(len(v) == 1 for v in porU.values())
    check("p2.mwd.reduccion.peso.inferior.cero.el.estado.solo.depende.del.par.superior", ok)
    # reduccion wU = 0: el estado solo depende del octeto y del par inferior
    ok = True
    for (a, b), members in clase.items():
        if b == 0:
            porL = {}
            for k in members:
                i, j = PAIRS[k]
                x, y = seq[i], seq[j]
                key = (upper(x), frozenset((lower(x), lower(y))))
                porL.setdefault(key, set()).add(st[k])
            ok = ok and all(len(v) == 1 for v in porL.values())
    check("p2.mwd.reduccion.peso.superior.cero.el.estado.solo.depende.del.octeto.y.del.par.inferior", ok)


def pieza_2_jingfang():
    seq = SEQS["Jing Fang"]
    palacios = GR.blocks_of(seq, 8)

    # el mismo conjunto de mascaras M en los ocho palacios
    Ms = [frozenset(x ^ pal[0] for x in pal) for pal in palacios]
    check("p2.jf.los.ocho.palacios.son.el.mismo.M.trasladado", len(set(Ms)) == 1)
    Mset = sorted(Ms[0])

    def lineset(m):
        s = "".join(str(k + 1) for k in range(LINES) if (m >> k) & 1)
        return s if s else "vacio"

    emit("p2.jf.M", " ".join(lineset(m) for m in Mset),
         "cada elemento por las lineas que complementa, la linea 1 es la inferior")
    check("p2.jf.M.tiene.ocho.elementos", len(Mset) == 8)

    # D, la diagonal, y los puros
    D = [x for x in ALL if lower(x) == upper(x)]
    check("p2.jf.D.es.subespacio.de.dimension.tres",
          len(D) == 8 and all((a ^ b) in D for a in D for b in D))
    check("p2.jf.las.cabezas.de.palacio.son.exactamente.D",
          set(pal[0] for pal in palacios) == set(D))

    # diferencias de M
    dif = [a ^ b for a, b in itertools.combinations(Mset, 2)]
    emit("p2.jf.diferencias.de.M", len(dif), "C(8,2)")
    mult = [sum(1 for d in dif if (d >> k) & 1) for k in range(LINES)]
    emit("p2.jf.multiplicidad.por.linea", " ".join(str(m) for m in mult),
         "lineas 1 a 6, en ese orden")
    check("p2.jf.multiplicidades.son.12.15.16.12.15.0", mult == [12, 15, 16, 12, 15, 0])
    sing = [sum(1 for d in dif if d == (1 << k)) for k in range(LINES)]
    emit("p2.jf.multiplicidad.de.los.singletons", " ".join(str(s) for s in sing), "")
    check("p2.jf.singletons.son.1.1.1.2.3.0", sing == [1, 1, 1, 2, 3, 0])

    # el estabilizador de las diferencias en S6 es trivial
    from collections import Counter
    dc = Counter(dif)
    triv = []
    for perm in itertools.permutations(range(LINES)):
        img = Counter(sum(((d >> perm[k]) & 1) << k for k in range(LINES)) for d in dif)
        if img == dc:
            triv.append(perm)
    emit("p2.jf.estabilizador.de.las.diferencias.en.S6", len(triv), "")
    check("p2.jf.ese.estabilizador.es.trivial", triv == [tuple(range(LINES))])

    # ninguna diferencia de M cae en D, luego D mas M parte los 64
    check("p2.jf.ninguna.diferencia.de.M.esta.en.D", all(d not in D for d in dif))
    sumas = set(p ^ m for p in D for m in Mset)
    check("p2.jf.D.mas.M.recorre.los.64.sin.repetir", len(sumas) == N)

    # el grupo: solo traslaciones por D
    g1 = GR.group_R1(seq, 8)
    trasl = set(tuple(x ^ d for x in ALL) for d in D)
    emit("p2.jf.orden.predicho", 8, "traslaciones por D")
    check("p2.jf.el.grupo.es.exactamente.las.traslaciones.por.D", set(g1) == trasl)

    # estructura de orbitas, predicha a mano
    orbits, oid, par, st = orbit_data(seq, g1)
    emit("p2.jf.numero.de.orbitas", len(orbits), "")
    tam = {}
    for o in orbits:
        tam[len(o)] = tam.get(len(o), 0) + 1
    emit("p2.jf.tamanos.de.orbita", " ".join("%d:%d" % kv for kv in sorted(tam.items())),
         "tamano y cuantas hay")
    dentro = 28          # pares dentro de un palacio
    mismo_k = 56         # bloques distintos, mismo indice interno
    resto = 196          # bloques distintos, indices distintos
    check("p2.jf.el.desglose.previsto.28.56.196.da.280",
          dentro + mismo_k + resto == len(orbits) == 280)
    check("p2.jf.los.tamanos.previstos.son.8.4.8",
          tam == {8: dentro + resto, 4: mismo_k})

    # las 28 orbitas de pares dentro de un palacio, demostradas forzadas
    comp = tuple(kappa(x) for x in ALL)
    check("p2.jf.el.complemento.esta.en.el.grupo", comp in set(g1))
    dentro_pairs = 0
    for k, (i, j) in enumerate(PAIRS):
        if i // 8 == j // 8:
            img, eps = epsilon(seq, comp, i, j)
            assert eps == 1 and img != k
            dentro_pairs += 1
    emit("p2.jf.orbitas.demostradas.forzadas", dentro, "las de pares dentro de un palacio")
    emit("p2.jf.pares.cubiertos.por.la.demostracion", dentro_pairs, "")
    emit("p2.jf.aportacion.demostrada", dentro_pairs // 2, "")
    check("p2.jf.el.complemento.da.epsilon.uno.dentro.del.palacio", True)


def pieza_2_enumerativo():
    """Lo que no se demuestra y queda declarado enumerativo, con su cuenta."""
    for name in ("Mawangdui", "Jing Fang"):
        seq = SEQS[name]
        g1 = GR.group_R1(seq, BLOCKS[name])
        orbits, oid, par, st = orbit_data(seq, g1)
        short = name.replace(" ", "")
        forzadas = sum(1 for o in orbits if 2 * sum(par[k] for k in o) == len(o))
        emit("p2.ENUMERATIVO.%s.orbitas" % short, len(orbits), "")
        emit("p2.ENUMERATIVO.%s.orbitas.forzadas" % short, forzadas,
             "comprobado por enumeracion de los 2016 pares, no demostrado")
        emit("p2.ENUMERATIVO.%s.clase.libre" % short, len(orbits) - forzadas, "")
        emit("p2.ENUMERATIVO.%s.total" % short, sum(st), "")


# =============================================================================
# Pieza 3: King Wen
# =============================================================================

def pieza_3():
    seq = SEQS["King Wen"]
    pares = [frozenset(b) for b in GR.blocks_of(seq, 2)]
    pset = set(pares)

    # el sistema de bloques, tal y como quedo medido en el commit de la medicion
    orb_giro = set(frozenset((x, rho(x))) for x in ALL if rho(x) != x)
    palind = [x for x in ALL if rho(x) == x]
    pal_pairs = set(frozenset((x, kappa(x))) for x in palind)
    check("p3.los.bloques.son.las.orbitas.del.giro.mas.los.pares.de.palindromos",
          orb_giro | pal_pairs == pset)
    emit("p3.orbitas.del.giro.de.tamano.dos", len(orb_giro), "")
    emit("p3.palindromos", len(palind), "")

    # tau, el companero de bloque, y el grupo como su centralizador
    tau = [0] * N
    for b in pares:
        x, y = sorted(b)
        tau[x], tau[y] = y, x
    g1 = GR.group_R1(seq, 2)
    cent_tau = [g for g in GR.FAMILY if all(g[tau[x]] == tau[g[x]] for x in ALL)]
    check("p3.respetar.los.bloques.equivale.a.conmutar.con.tau", set(cent_tau) == set(g1))

    # toda aplicacion de la familia conmuta con la complementacion
    check("p3.toda.la.familia.conmuta.con.la.complementacion",
          all(g[kappa(x)] == kappa(g[x]) for g in list(GR.FAMILY)[:2000] for x in ALL),
          "comprobado en una muestra de 2000 elementos, y demostrado en el texto")

    # las diferencias de bloque son exactamente los no nulos de Fix(rho)
    fix = [x for x in ALL if rho(x) == x]
    difs = set()
    for b in pares:
        x, y = sorted(b)
        difs.add(x ^ y)
    check("p3.las.diferencias.de.bloque.son.los.no.nulos.de.Fix(giro)",
          difs == set(f for f in fix if f != 0))
    emit("p3.Fix(giro).tamano", len(fix), "subespacio de dimension tres")
    peso2 = [f for f in fix if weight(f) == 2]
    emit("p3.elementos.de.peso.dos.en.Fix(giro)", len(peso2), "los tres generadores")

    # permutaciones que preservan Fix(rho): el centralizador del giro en S6
    perms_ok = [perm for perm in itertools.permutations(range(LINES))
                if all(sum(((f >> perm[k]) & 1) << k for k in range(LINES)) in fix for f in fix)]
    emit("p3.permutaciones.que.preservan.Fix(giro)", len(perms_ok), "")
    check("p3.esas.permutaciones.son.48", len(perms_ok) == 48)
    emit("p3.mascaras.en.Fix(giro)", len(fix), "")
    emit("p3.orden.predicho", len(perms_ok) * len(fix), "48 por 8")
    check("p3.orden.predicho.coincide.con.la.enumeracion", len(g1) == len(perms_ok) * len(fix))

    giro = tuple(rho(x) for x in ALL)
    check("p3.el.grupo.es.el.centralizador.del.giro",
          set(g1) == set(g for g in GR.FAMILY if GR.compose(g, giro) == GR.compose(giro, g)))

    # T, traslaciones por Fix(rho): normal, libre, y orbitas de pares pares
    T = [tuple(x ^ f for x in ALL) for f in fix]
    check("p3.T.esta.contenido.en.el.grupo", set(T) <= set(g1))
    check("p3.T.es.normal.en.el.grupo",
          all(GR.compose(GR.compose(g, t), inv(g)) in set(T) for g in g1[:64] for t in T),
          "comprobado en una muestra de 64 elementos, y demostrado en el texto")
    check("p3.T.actua.libremente.sobre.los.hexagramas",
          all(all(t[x] != x for x in ALL) for t in T if t != tuple(ALL)))

    for name in ("Mawangdui", "Jing Fang", "King Wen"):
        s = SEQS[name]
        gg = GR.group_R1(s, BLOCKS[name])
        orbits, oid, par, st = orbit_data(s, gg)
        short = name.replace(" ", "")
        impares = sum(1 for o in orbits if len(o) % 2)
        check("p3.%s.ninguna.orbita.de.tamano.impar" % short, impares == 0)
        paridad = sum(sum(par[k] for k in o) for o in orbits) % 2
        emit("p3.%s.paridad.estructural" % short, paridad,
             "suma de las c de cada orbita, modulo dos, independiente de los bits libres")
        emit("p3.%s.paridad.del.recuento.observado" % short, sum(st) % 2, "")
        check("p3.%s.la.paridad.estructural.predice.la.del.recuento" % short,
              paridad == sum(st) % 2)

    # T-orbitas de pares: tamano 4 u 8, y todas iguales dentro de una G-orbita
    s = SEQS["King Wen"]
    orbits, oid, par, st = orbit_data(s, g1)
    posof = {h: i for i, h in enumerate(s)}
    tor = {}
    seen = [-1] * len(PAIRS)
    tsizes = set()
    for k, (i, j) in enumerate(PAIRS):
        if seen[k] != -1:
            continue
        o = len(tor)
        miembros = set()
        for t in T:
            a, b = posof[t[s[i]]], posof[t[s[j]]]
            miembros.add(PINDEX[(a, b) if a < b else (b, a)])
        for m in miembros:
            seen[m] = o
        tor[o] = miembros
        tsizes.add(len(miembros))
    emit("p3.tamanos.de.T.orbita.sobre.pares", " ".join(str(x) for x in sorted(tsizes)), "")
    check("p3.toda.T.orbita.de.pares.tiene.tamano.par", all(x % 2 == 0 for x in tsizes))
    iguales = all(len(set(len(tor[seen[k]]) for k in o)) == 1 for o in orbits)
    check("p3.dentro.de.una.G.orbita.todas.las.T.orbitas.miden.igual", iguales)

    # el empate, imposible
    res = GR.accounting(s, g1, GR.generators_of(g1), VAL)
    emit("p3.intervalo.minimo", res["minimo"], "")
    emit("p3.intervalo.maximo", res["maximo"], "")
    emit("p3.totales.compatibles", res["totales_alcanzables"], "")
    emit("p3.paridades.entre.los.compatibles", res["paridades_alcanzables"], "")
    emit("p3.compatible.mas.cercano.al.empate", res["alcanzable_mas_cercano_al_esperado"], "")
    emit("p3.desviacion.minima.posible", res["desviacion_minima_posible"], "")
    emit("p3.observado", res["observado"], "")
    check("p3.el.empate.no.esta.entre.los.compatibles", res["esperado_alcanzable"] == 0)
    emit("p3.ABIERTO.residuo.sobre.el.empate", res["observado"] - DENOM // 2,
         "no lo explica el grupo: queda abierto")


def inv(g):
    out = [0] * N
    for x in range(N):
        out[g[x]] = x
    return tuple(out)


# =============================================================================
# Pieza 4: terminologia
# =============================================================================

def pieza_4():
    emit("p4.orden.de.la.familia", len(GR.FAMILY), "dos elevado a seis, por seis factorial")
    check("p4.orden.es.2^6.por.6!", len(GR.FAMILY) == (1 << LINES) * 720)
    check("p4.cada.elemento.tiene.una.sola.escritura.como.permutacion.y.mascara",
          len(set(GR.FAMILY.values())) == len(GR.FAMILY))
    comp = tuple(kappa(x) for x in ALL)
    giro = tuple(rho(x) for x in ALL)
    check("p4.la.familia.contiene.la.complementacion.y.el.giro",
          comp in GR.FAMILY and giro in GR.FAMILY)
    # el grupo actua sobre los 64 vertices del 6-cubo conservando la adyacencia:
    # dos hexagramas son adyacentes cuando difieren en una sola linea
    def adj(a, b):
        return weight(a ^ b) == 1
    muestra = list(GR.FAMILY)[::720]
    check("p4.conserva.la.adyacencia.del.6.cubo",
          all(adj(g[a], g[b]) == adj(a, b) for g in muestra for a in ALL for b in ALL),
          "comprobado en una muestra de %d elementos" % len(muestra))


# =============================================================================

def uniform_witnesses(seq, group, members):
    """Elementos g del grupo con epsilon igual a uno en todos los pares dados."""
    posof, vals = position_data(seq)
    n = 0
    for g in group:
        gs = [g[h] for h in seq]
        ok = True
        for k in members:
            i, j = PAIRS[k]
            a, b = posof[gs[i]], posof[gs[j]]
            A = 1 if a > b else 0
            B = 1 if ((VAL[gs[i]] > VAL[gs[j]]) != (vals[i] > vals[j])) else 0
            if (A ^ B) != 1:
                ok = False
                break
        n += ok
    return n


def first_witness(seq, group, members):
    """Primer elemento del grupo, en orden determinista, con epsilon uno en toda
    la orbita. Devuelve None si no hay ninguno, y entonces el Lema 2 no llega."""
    posof, vals = position_data(seq)
    for g in sorted(group, key=lambda g: (GR.FAMILY[g][0], GR.FAMILY[g][1])):
        gs = [g[h] for h in seq]
        ok = True
        for k in members:
            i, j = PAIRS[k]
            a, b = posof[gs[i]], posof[gs[j]]
            A = 1 if a > b else 0
            B = 1 if ((VAL[gs[i]] > VAL[gs[j]]) != (vals[i] > vals[j])) else 0
            if (A ^ B) != 1:
                ok = False
                break
        if ok:
            return g
    return None


def verify_witness(seq, g, members):
    posof, vals = position_data(seq)
    gs = [g[h] for h in seq]
    for k in members:
        i, j = PAIRS[k]
        a, b = posof[gs[i]], posof[gs[j]]
        A = 1 if a > b else 0
        B = 1 if ((VAL[gs[i]] > VAL[gs[j]]) != (vals[i] > vals[j])) else 0
        if (A ^ B) != 1:
            return False
        if ((a, b) if a < b else (b, a)) == PAIRS[k]:
            return False                      # el testigo no puede fijar el par
    return True


def pieza_2_certificados():
    """
    Testigos explicitos para el Lema 2, uno por orbita, verificados. Donde no hay
    testigo el Lema 2 no llega y lo que quede se declara enumerativo.
    """
    cert = []

    # Mawangdui, por clases de pesos
    seq = SEQS["Mawangdui"]
    g1 = GR.group_R1(seq, 8)
    clase = {}
    for k, (i, j) in enumerate(PAIRS):
        x, y = seq[i], seq[j]
        clase.setdefault((weight(lower(x) ^ lower(y)), weight(upper(x) ^ upper(y))), []).append(k)
    cert.append("MAWANGDUI, un testigo por clase de pesos (a inferior, b superior)")
    con = pares_con = 0
    sin_clases, pares_sin = [], 0
    for (a, b), members in sorted(clase.items()):
        w = first_witness(seq, g1, members)
        if w is None:
            cert.append("  clase (%d,%d) tamano %4d   SIN TESTIGO, el Lema 2 no llega"
                        % (a, b, len(members)))
            sin_clases.append((a, b))
            pares_sin += len(members)
            continue
        assert verify_witness(seq, w, members)
        cert.append("  clase (%d,%d) tamano %4d   testigo %s"
                    % (a, b, len(members), GR.describe(w)))
        con += 1
        pares_con += len(members)
    emit("p2.CERT.mwd.clases.con.testigo", con, "de 15")
    emit("p2.CERT.mwd.pares.demostrados", pares_con, "")
    emit("p2.CERT.mwd.aportacion.demostrada", pares_con // 2, "la mitad, por los Lemas 1 y 2")
    emit("p2.CERT.mwd.clases.sin.testigo.uniforme",
         " ".join("(%d,%d)" % c for c in sin_clases) if sin_clases else "ninguna",
         "el Lema 2 no llega; se retoman en la pieza 5")
    emit("p2.CERT.mwd.pares.fuera.del.lema.2", pares_sin, "")
    obs_sin = sum(status_vector(seq)[k] for (a, b), m in clase.items()
                  if (a, b) in sin_clases for k in m)
    emit("p2.CERT.mwd.aportacion.fuera.del.lema.2", obs_sin,
         "la fija el Lema 3 en la pieza 5")

    # Jing Fang, por orbitas
    seqj = SEQS["Jing Fang"]
    gj = GR.group_R1(seqj, 8)
    orbits, oid, par, st = orbit_data(seqj, gj)
    cert.append("")
    cert.append("JING FANG, un testigo por orbita, %d orbitas" % len(orbits))
    con = sin = pares_con = 0
    resumen = {}
    for oi, o in enumerate(orbits):
        w = first_witness(seqj, gj, o)
        if w is None:
            sin += 1
            cert.append("  orbita %3d tamano %d   SIN TESTIGO" % (oi, len(o)))
            continue
        assert verify_witness(seqj, w, o)
        con += 1
        pares_con += len(o)
        key = GR.describe(w)
        resumen[key] = resumen.get(key, 0) + 1
        cert.append("  orbita %3d tamano %d   testigo %s" % (oi, len(o), key))
    emit("p2.CERT.jf.orbitas.con.testigo", con, "de %d" % len(orbits))
    emit("p2.CERT.jf.orbitas.sin.testigo", sin, "")
    emit("p2.CERT.jf.pares.demostrados", pares_con, "")
    emit("p2.CERT.jf.aportacion.demostrada", pares_con // 2, "")
    emit("p2.CERT.jf.testigos.distintos.usados", len(resumen), "")
    check("p2.CERT.jf.el.empate.queda.demostrado",
          sin == 0 and pares_con == DENOM and pares_con // 2 == DENOM // 2,
          "toda orbita forzada por el Lema 2, luego el total es C(64,2) partido por dos por el Lema 1")

    path = os.path.join(ROOT, "results", "certificates.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("Testigos del Lema 2, uno por orbita. Cada linea es verificable\n")
        fh.write("por separado: basta comprobar que epsilon vale uno en toda la orbita.\n")
        fh.write("Notacion de la mascara: seis digitos, el de mas a la izquierda es la\n")
        fh.write("linea 6 y el de mas a la derecha la linea 1. Un uno dice que esa linea\n")
        fh.write("se complementa. La permutacion se escribe por las lineas de destino.\n\n")
        fh.write("\n".join(cert) + "\n")
    print("escrito results/certificates.txt")


def relation_edges(seq, group, members):
    """
    Aristas del cierre de relaciones dentro de un conjunto de pares: {p, q} con
    testigo g tal que g manda p sobre q y epsilon(g, p) vale uno. Por el Lema 0
    los dos extremos de una arista tienen estado contrario, sin mirar el estado.
    """
    posof, vals = position_data(seq)
    ms = set(members)
    edges = {}
    for g in sorted(group, key=lambda g: (GR.FAMILY[g][0], GR.FAMILY[g][1])):
        gs = [g[h] for h in seq]
        for k in members:
            i, j = PAIRS[k]
            a, b = posof[gs[i]], posof[gs[j]]
            A = 1 if a > b else 0
            B = 1 if ((VAL[gs[i]] > VAL[gs[j]]) != (vals[i] > vals[j])) else 0
            if (A ^ B) != 1:
                continue
            q = PINDEX[(a, b) if a < b else (b, a)]
            if q == k or q not in ms:
                continue
            edges.setdefault((min(k, q), max(k, q)), []).append(g)
    return edges


def max_matching(members, edges):
    adj = {k: [] for k in members}
    for (p, q) in edges:
        adj[p].append(q)
        adj[q].append(p)
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
    for u in members:
        if u not in match and aug(u, set()):
            n += 1
    return n, match


def pieza_5_clase01():
    """
    La clase (0,1) de Mawangdui: el certificado del Lema 3, o la constancia de
    que no lo hay. Se construye el cierre de relaciones y se busca el
    emparejamiento mas corto que fije la aportacion.
    """
    seq = SEQS["Mawangdui"]
    G = GR.group_R1(seq, 8)
    cls = [k for k, (i, j) in enumerate(PAIRS)
           if weight(lower(seq[i]) ^ lower(seq[j])) == 0
           and weight(upper(seq[i]) ^ upper(seq[j])) == 1]
    emit("p5.clase01.pares", len(cls), "la clase que el Lema 2 no alcanza")

    edges = relation_edges(seq, G, cls)
    emit("p5.clase01.aristas.del.cierre", len(edges),
         "pares {p,q} con algun testigo que obliga a estados contrarios")
    # Las aristas solo unen paridades contrarias, luego su numero no puede pasar
    # de c por (96 menos c). Que haya 2304 obliga a c igual a 48.
    n = len(cls)
    cotas = [c for c in range(n + 1) if c * (n - c) >= len(edges)]
    emit("p5.clase01.valores.de.c.compatibles.con.ese.numero.de.aristas",
         " ".join(str(c) for c in cotas),
         "de c por (n menos c) mayor o igual que el numero de aristas")
    check("p5.clase01.el.recuento.de.aristas.ya.fija.c.en.48", cotas == [n // 2])

    hay, _ = max_matching(cls, edges)
    check("p5.clase01.el.cierre.admite.emparejamiento.perfecto", hay == len(cls) // 2)

    # el certificado mas corto: cuantos elementos distintos hacen falta
    unicos = []
    for g in sorted(G, key=lambda g: (GR.FAMILY[g][0], GR.FAMILY[g][1])):
        sub = {e: ws for e, ws in edges.items() if g in ws}
        m, _ = max_matching(cls, sub)
        if m == len(cls) // 2:
            unicos.append(g)
    emit("p5.clase01.elementos.que.bastan.por.si.solos", len(unicos), "de %d" % len(G))
    check("p5.clase01.basta.un.solo.elemento", len(unicos) > 0)

    g = unicos[0]
    sub = {e: ws for e, ws in edges.items() if g in ws}
    m, match = max_matching(cls, sub)
    parejas = sorted(set((min(a, b), max(a, b)) for a, b in match.items()))
    emit("p5.clase01.testigo.del.certificado", GR.describe(g), "")
    emit("p5.clase01.parejas.del.certificado", len(parejas), "")
    check("p5.clase01.las.parejas.parten.la.clase",
          len(parejas) == len(cls) // 2 and
          sorted(x for pr in parejas for x in pr) == sorted(cls))

    # verificacion de cada pareja, una por una y sin mirar ningun estado
    posof, vals = position_data(seq)
    gs = [g[h] for h in seq]
    def aplica(origen):
        """Aplica el testigo al par de posiciones y devuelve (destino, A, B)."""
        i, j = PAIRS[origen]
        a, b = posof[gs[i]], posof[gs[j]]
        A = 1 if a > b else 0
        B = 1 if ((VAL[gs[i]] > VAL[gs[j]]) != (vals[i] > vals[j])) else 0
        return PINDEX[(a, b) if a < b else (b, a)], A, B

    lineas = []
    for (p, q) in parejas:
        # la arista puede estar orientada en cualquiera de los dos sentidos
        destino, A, B = aplica(p)
        origen, llega = p, q
        if not (destino == q and (A ^ B) == 1):
            destino, A, B = aplica(q)
            origen, llega = q, p
        assert destino == llega and (A ^ B) == 1, "pareja sin testigo en ningun sentido"
        i, j = PAIRS[origen]
        u, v = PAIRS[llega]
        lineas.append("  {%2d,%2d} -> {%2d,%2d}   A=%d B=%d epsilon=1"
                      % (i, j, u, v, A, B))
    check("p5.clase01.las.48.parejas.verifican.epsilon.uno", True)
    obs = sum(status_vector(seq)[k] for k in cls)
    emit("p5.clase01.aportacion", len(cls) // 2, "demostrada por el Lema 3")
    check("p5.clase01.la.aportacion.demostrada.coincide.con.la.contada", obs == len(cls) // 2)

    path = os.path.join(ROOT, "results", "certificate-mwd-01.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("CERTIFICADO DE LA CLASE (0,1) DE MAWANGDUI\n\n")
        fh.write("Clase: los %d pares de posiciones cuyos hexagramas comparten trigrama\n" % len(cls))
        fh.write("inferior y difieren en una sola linea del superior.\n\n")
        fh.write("Testigo unico: %s\n" % GR.describe(g))
        fh.write("La mascara se lee con la linea 6 a la izquierda y la linea 1 a la derecha.\n")
        fh.write("La permutacion se escribe por las lineas de destino.\n\n")
        fh.write("Las %d parejas de abajo parten la clase entera. En cada una, el testigo\n" % len(parejas))
        fh.write("lleva el primer par de posiciones al segundo con epsilon igual a uno, y\n")
        fh.write("por el Lema 0 eso obliga a que sus estados sean contrarios: la pareja\n")
        fh.write("aporta exactamente una inversion, sin mirar cual de las dos lo es.\n")
        fh.write("Sumando, la clase aporta %d. Cada linea se verifica por separado.\n\n" % (len(cls) // 2))
        fh.write("\n".join(lineas) + "\n")
    print("escrito results/certificate-mwd-01.txt")

    # contraprueba: el Lema 3 no vale de balde. En King Wen no hay emparejamiento
    # en las orbitas libres, y por eso alli no fuerza nada.
    seqk = SEQS["King Wen"]
    gk = GR.group_R1(seqk, 2)
    orbits, oid, par, st = orbit_data(seqk, gk)
    libres = [o for o in orbits if 2 * sum(par[k] for k in o) != len(o)]
    sin_pm = 0
    for o in libres:
        e = relation_edges(seqk, gk, o)
        m, _ = max_matching(o, e)
        if m < len(o) // 2:
            sin_pm += 1
    emit("p5.contraprueba.kingwen.orbitas.libres", len(libres), "")
    emit("p5.contraprueba.kingwen.orbitas.libres.sin.emparejamiento", sin_pm,
         "el Lema 3 tampoco las alcanza, como tiene que ser")
    check("p5.contraprueba.el.lema.3.no.fuerza.lo.que.no.esta.forzado",
          sin_pm == len(libres))


def main():
    pieza_1()
    pieza_2_mawangdui()
    pieza_2_jingfang()
    pieza_2_enumerativo()
    pieza_3()
    pieza_4()
    pieza_2_certificados()
    pieza_5_clase01()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Comprobadores de PROOFS.md. Una comprobacion o una cifra por linea.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/proofs.tsv con %d lineas" % len(ROWS))
    for key, val, _ in ROWS:
        print("  %-70s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
