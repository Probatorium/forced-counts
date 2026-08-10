#!/usr/bin/env python3
"""
El residuo de 5: anatomia y simetrias extendidas.

Fases 1 y 2 de lo declarado en DEFINICIONES-RESIDUO5.md, cuya lista de
candidatas es cerrada y se commiteo antes que este programa.

  Fase 1  descomposicion del 1013 sobre las 19 orbitas libres, vector completo,
          y cruce de las orbitas desviadas contra los rasgos de A1 y A2.
  Fase 2  para cada candidata, si la construccion la respeta y si anadirla
          reduce las orbitas libres o estrecha el intervalo.

Herencia de verificaciones, por la enmienda 3 de CONTACT-RULES.md: se reusa el
aparato de src/measure.py y src/group.py sin reimplementarlo, y se heredan al
arrancar el orden del grupo, el recuento observado y el intervalo ya medidos.

Salida: results/residuo5.tsv

  python src/residuo5.py
"""

import json
import os
import sys
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import measure as M                                        # noqa: E402
import group as GR                                         # noqa: E402

OUT = os.path.join(ROOT, "results", "residuo5.tsv")
N = 64
DENOM = comb(N, 2)
EMPATE = DENOM // 2
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
PINDEX = {p: k for k, p in enumerate(PAIRS)}
VAL = [M.value(M.dec(x), "yang1", "bottomMSB") for x in range(N)]


def orbitas(seq, group):
    """Orbitas de pares de posiciones, paridad y estado. Grupo cualquiera."""
    posof = {h: i for i, h in enumerate(seq)}
    vals = [VAL[h] for h in seq]
    pis = [[posof[g[seq[i]]] for i in range(N)] for g in group]

    def step(gi, k):
        g, pi = group[gi], pis[gi]
        i, j = PAIRS[k]
        a, b = pi[i], pi[j]
        A = 1 if a > b else 0
        B = 1 if ((VAL[g[seq[i]]] > VAL[g[seq[j]]]) != (vals[i] > vals[j])) else 0
        return PINDEX[(a, b) if a < b else (b, a)], A ^ B

    oid = [-1] * len(PAIRS)
    par = [0] * len(PAIRS)
    orbs = []
    for start in range(len(PAIRS)):
        if oid[start] != -1:
            continue
        o = len(orbs)
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
        orbs.append(members)
    estado = [1 if vals[i] > vals[j] else 0 for i, j in PAIRS]
    return orbs, par, estado


def resumen(orbs, par, estado):
    lo = hi = 0
    gaps = []
    libres = []
    for o in orbs:
        c = sum(par[k] for k in o)
        s = len(o)
        lo += min(c, s - c)
        hi += max(c, s - c)
        if 2 * c != s:
            libres.append(o)
            gaps.append(abs(s - 2 * c))
    reach = {0}
    for g in gaps:
        reach |= {r + g for r in reach}
    alc = sorted(lo + r for r in reach)
    return {"orbitas": len(orbs), "libres": len(libres), "minimo": lo, "maximo": hi,
            "anchura": hi - lo, "alcanzables": len(alc),
            "empate_alcanzable": int(EMPATE in alc), "observado": sum(estado),
            "orbitas_libres": libres}


def nuclear(x):
    """A1: trigrama inferior lineas 2,3,4 y superior lineas 3,4,5."""
    b = M.dec(x)                       # indice 0 es la linea 1
    bajo = b[1:4]
    alto = b[2:5]
    return M.enc(bajo + alto)


def main():
    with open(os.path.join(ROOT, "data", "sequences.json"), "r", encoding="utf-8") as fh:
        kw = [M.enc(p) for p in json.load(fh)["sequences"]["King Wen"]]
    G = GR.group_R1(kw, 2)
    gens = GR.generators_of(G)
    emit("grupo.orden", len(G), "el centralizador del giro, ya demostrado")
    check("herencia.el.orden.del.grupo.es.384", len(G) == 384)

    orbs, par, estado = orbitas(kw, gens)
    r = resumen(orbs, par, estado)
    emit("orbitas", r["orbitas"], "")
    emit("orbitas.libres", r["libres"], "")
    emit("observado", r["observado"], "")
    emit("intervalo.minimo", r["minimo"], "")
    emit("intervalo.maximo", r["maximo"], "")
    check("herencia.observado.es.1013", r["observado"] == 1013)
    check("herencia.orbitas.libres.son.19", r["libres"] == 19)
    check("herencia.intervalo.es.957.a.1059",
          r["minimo"] == 957 and r["maximo"] == 1059)

    # =====================================================================
    # FASE 1. La anatomia: el vector completo sobre las orbitas libres
    # =====================================================================
    posof = {h: i for i, h in enumerate(kw)}
    par_de = {}
    for k in range(32):
        par_de[kw[2 * k]] = k
        par_de[kw[2 * k + 1]] = k

    filas = []
    for idx, o in enumerate(sorted(r["orbitas_libres"], key=lambda o: (-len(o), min(o)))):
        s = len(o)
        c = sum(par[k] for k in o)
        obs = sum(estado[k] for k in o)
        filas.append((idx, s, s // 2, obs, obs - s // 2, o))
    suma_desv = sum(f[4] for f in filas)
    for idx, s, mitad, obs, desv, o in filas:
        emit("f1.orbita.%02d.cardinal" % idx, s, "")
        emit("f1.orbita.%02d.mitad" % idx, mitad, "")
        emit("f1.orbita.%02d.aportacion" % idx, obs, "")
        emit("f1.orbita.%02d.desviacion" % idx, desv, "")
    emit("f1.suma.de.desviaciones", suma_desv, "tiene que ser 1013 menos 1008")
    check("f1.la.suma.de.desviaciones.es.5", suma_desv == 5)
    emit("f1.orbitas.con.desviacion.no.nula", sum(1 for f in filas if f[4]), "")

    # cruce contra los rasgos declarados de A1 y A2
    for idx, s, mitad, obs, desv, o in filas:
        mismo_nuc = sum(1 for k in o if nuclear(kw[PAIRS[k][0]]) == nuclear(kw[PAIRS[k][1]]))
        misma_mitad = sum(1 for k in o
                          if (PAIRS[k][0] < 30) == (PAIRS[k][1] < 30))
        mismo_par = sum(1 for k in o if par_de[kw[PAIRS[k][0]]] == par_de[kw[PAIRS[k][1]]])
        emit("f1.orbita.%02d.A1.pares.con.el.mismo.nuclear" % idx, mismo_nuc, "")
        emit("f1.orbita.%02d.A2.pares.dentro.de.una.misma.mitad" % idx, misma_mitad, "")
        emit("f1.orbita.%02d.pares.dentro.de.un.mismo.par.de.KW" % idx, mismo_par, "")

    # =====================================================================
    # FASE 2. Las simetrias extendidas
    # =====================================================================
    bloques = [frozenset(kw[2 * k:2 * k + 2]) for k in range(32)]
    bset = set(bloques)

    def respeta(f):
        return all(frozenset(f[y] for y in b) in bset for b in bloques)

    # A1: no aporta biyeccion; se comprueba si manda par a par como conjunto
    nuc_pares = sum(1 for b in bloques
                    if len(set(nuclear(x) for x in b)) == 1)
    emit("f2.A1.pares.cuyos.dos.miembros.comparten.nuclear", nuc_pares, "de 32")
    emit("f2.A1.aporta.biyeccion", 0, "la operacion nuclear no es biyectiva, declarado en la fase 0")
    fibras = {}
    for x in range(N):
        fibras.setdefault(nuclear(x), []).append(x)
    emit("f2.A1.imagenes.nucleares.distintas", len(fibras), "")
    emit("f2.A1.la.particion.nuclear.refina.o.cruza.los.pares",
         sum(1 for b in bloques if len(set(nuclear(x) for x in b)) == 1),
         "cuantos pares caen enteros en una fibra")

    # A2: no aporta biyeccion; se comprueba si el corte respeta los pares
    corte_ok = all((2 * k < 30) == (2 * k + 1 < 30) for k in range(32))
    emit("f2.A2.el.corte.respeta.los.pares", int(corte_ok), "ningun par cruza la frontera")
    emit("f2.A2.aporta.biyeccion", 0, "las mitades son de 30 y 34, declarado en la fase 0")

    # A3, A4, A5: aportan biyeccion; se prueban una a una y juntas
    def por_posiciones(mapa_pos):
        f = [0] * N
        for i in range(N):
            f[kw[i]] = kw[mapa_pos(i)]
        return tuple(f)

    A3 = por_posiciones(lambda i: (i + 2) % N)
    A4 = por_posiciones(lambda i: N - 1 - i)
    A5 = por_posiciones(lambda i: i ^ 1)

    ident = tuple(range(N))

    TOPE_GRUPO = 200000        # tope declarado; ver la advertencia de la fase 0

    def cierre(gens_extra):
        """Orden del grupo generado, con tope. Devuelve (orden, si_se_paso_del_tope).
        Para la contabilidad NO hace falta el grupo entero: bastan generadores."""
        seen = {ident}
        frontera = [ident]
        base = list(gens) + list(gens_extra)
        while frontera:
            cur = frontera.pop()
            for g in base:
                nxt = tuple(g[x] for x in cur)
                if nxt not in seen:
                    seen.add(nxt)
                    frontera.append(nxt)
                    if len(seen) > TOPE_GRUPO:
                        return len(seen), True
        return len(seen), False

    for nombre, extra in (("A3", [A3]), ("A4", [A4]), ("A5", [A5]),
                          ("A3+A4+A5", [A3, A4, A5])):
        emit("f2.%s.respeta.el.sistema.de.pares" % nombre,
             int(all(respeta(g) for g in extra)), "")
        emit("f2.%s.es.afin" % nombre,
             int(all(g in GR.FAMILY for g in extra)),
             "cero quiere decir que esta fuera de B6")
        orden, pasado = cierre(extra)
        emit("f2.%s.orden.del.grupo.generado" % nombre,
             ("mas de %d" % TOPE_GRUPO) if pasado else orden,
             "tope declarado de %d; ver la advertencia de la fase 0" % TOPE_GRUPO)
        emit("f2.%s.pasa.del.tope.declarado" % nombre, int(pasado),
             "si vale uno, el grupo es grande y sin estructura y no cuenta como hallazgo")
        gens_x = list(gens) + list(extra)
        check("f2.%s.los.generadores.respetan.los.pares" % nombre,
              all(respeta(g) for g in gens_x))
        ox, px, ex = orbitas(kw, gens_x)
        rx = resumen(ox, px, ex)
        emit("f2.%s.orbitas" % nombre, rx["orbitas"], "")
        emit("f2.%s.orbitas.libres" % nombre, rx["libres"], "")
        emit("f2.%s.intervalo.minimo" % nombre, rx["minimo"], "")
        emit("f2.%s.intervalo.maximo" % nombre, rx["maximo"], "")
        emit("f2.%s.anchura" % nombre, rx["anchura"], "")
        emit("f2.%s.empate.alcanzable" % nombre, rx["empate_alcanzable"], "")
        emit("f2.%s.reduce.las.orbitas.libres" % nombre, int(rx["libres"] < 19), "")
        emit("f2.%s.estrecha.el.intervalo" % nombre, int(rx["anchura"] < 102), "")
        emit("f2.%s.fuerza" % nombre, int(rx["anchura"] == 0), "")
        check("f2.%s.el.observado.no.cambia" % nombre, rx["observado"] == 1013,
              "cambiar el grupo no cambia la secuencia ni su recuento")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# El residuo de 5: anatomia y simetrias extendidas.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/residuo5.tsv con %d lineas" % len(ROWS))
    for key, val, _ in ROWS:
        if key.startswith("f2.") or "desviacion" in key or "herencia" in key:
            print("  %-56s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
