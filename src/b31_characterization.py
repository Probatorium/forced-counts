#!/usr/bin/env python3
"""
Caracterizacion de la clase forzada en B(3,1), sobre el espacio entero.

Las 40320 ordenaciones de los ocho vertices, todas con el mismo grupo de orden
16. Se prueban los candidatos a invariante DECLARADOS ANTES en
DEFINICIONES-B31.md, y solo esos. Un candidato vale si separa exactamente la
particion entre forzadas y no forzadas; si separa a medias, se reporta con su
matriz de confusion.

Herencia de verificaciones, por la enmienda 3 de CONTACT-RULES.md: este programa
reusa el aparato de src/general_landscape.py sin reimplementarlo, y comprueba al
arrancar las mismas invariantes que aquel ya comprobaba.

Salida: results/b31-characterization.tsv

  python src/b31_characterization.py
"""

import itertools
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import general_landscape as GL                             # noqa: E402

OUT = os.path.join(ROOT, "results", "b31-characterization.tsv")
ROWS = []
N = 8
K = 1


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador: " + key


PAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]
PINDEX = {p: k for k, p in enumerate(PAIRS)}


def datos(seq, gens, valh):
    """Orbitas, paridades y estados. Devuelve (orbitas, par, estado)."""
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
    estado = [1 if vals[i] > vals[j] else 0 for i, j in PAIRS]
    return orbits, par, estado, pis


def matching_existe(seq, group, valh, orbita):
    """C1: grafo de relaciones dentro de la orbita y emparejamiento perfecto."""
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]
    ms = set(orbita)
    adj = {k: [] for k in orbita}
    for g in group:
        gs = [g[h] for h in seq]
        for k in orbita:
            i, j = PAIRS[k]
            a, b = posof[gs[i]], posof[gs[j]]
            A = 1 if a > b else 0
            B = 1 if ((valh[gs[i]] > valh[gs[j]]) != (vals[i] > vals[j])) else 0
            if (A ^ B) != 1:
                continue
            q = PINDEX[(a, b) if a < b else (b, a)]
            if q != k and q in ms:
                adj[k].append(q)
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
    for u in orbita:
        if u not in match and aug(u, set()):
            n += 1
    return n == len(orbita) // 2


def main():
    FAM = GL.affine_group(3)
    valh = GL.value_table(3, "yang1", "bottomMSB")
    G = GL.group_R1(list(range(N)), 1 << K, FAM)
    gens = GL.generators_of(G, FAM, N)
    emit("grupo.orden", len(G), "el que respeta B(3,1)")
    check("grupo.orden.es.16", len(G) == 16)

    # herencia de verificaciones: las mismas que ya comprobaba el aparato
    check("herencia.el.orden.binario.da.cero.discordantes",
          sum(1 for i, j in PAIRS
              if valh[GL.orden_binario(3, valh)[i]] > valh[GL.orden_binario(3, valh)[j]]) == 0,
          "control heredado de src/general_landscape.py")
    check("herencia.el.orden.del.grupo.es.k!.por.(n-k)!.por.2^n", len(G) == 1 * 2 * 8)

    # --- recorrido entero -----------------------------------------------
    forzadas, total = [], 0
    inv = {c: {} for c in ("C2", "C3", "C4", "C5")}
    for perm in itertools.permutations(range(N)):
        seq = list(perm)
        total += 1
        orbits, par, estado, pis = datos(seq, gens, valh)
        es_forzada = all(2 * sum(par[k] for k in o) == len(o) for o in orbits)

        posof = {h: i for i, h in enumerate(seq)}
        c2 = tuple(sorted(abs(posof[x] - posof[x ^ 1]) for x in range(0, N, 2)))
        c3 = tuple(sorted((len(o), min(sum(par[k] for k in o),
                                       len(o) - sum(par[k] for k in o))) for o in orbits))
        c4 = sum(estado)
        c5 = tuple(sorted((posof[x] + posof[x ^ 1]) % 2 for x in range(0, N, 2)))
        for nombre, v in (("C2", c2), ("C3", c3), ("C4", c4), ("C5", c5)):
            d = inv[nombre].setdefault(v, [0, 0])
            d[1 if es_forzada else 0] += 1
        if es_forzada:
            forzadas.append(seq)

    emit("ordenaciones", total, "las 8 factorial")
    emit("forzadas", len(forzadas), "")
    emit("no.forzadas", total - len(forzadas), "")
    check("particion.472.y.39848", len(forzadas) == 472 and total - len(forzadas) == 39848)

    # --- C2 a C5: separacion exacta o matriz de confusion ----------------
    for nombre in ("C2", "C3", "C4", "C5"):
        d = inv[nombre]
        puros_si = sum(v[1] for v in d.values() if v[0] == 0)
        puros_no = sum(v[0] for v in d.values() if v[1] == 0)
        mezclados_si = sum(v[1] for v in d.values() if v[0] and v[1])
        mezclados_no = sum(v[0] for v in d.values() if v[0] and v[1])
        emit("%s.valores.distintos" % nombre, len(d), "")
        emit("%s.separa.exacto" % nombre, int(mezclados_si == 0 and mezclados_no == 0),
             "un valor del invariante nunca mezcla forzadas con no forzadas")
        emit("%s.confusion.forzadas.en.valores.puros" % nombre, puros_si, "")
        emit("%s.confusion.forzadas.en.valores.mezclados" % nombre, mezclados_si, "")
        emit("%s.confusion.no.forzadas.en.valores.puros" % nombre, puros_no, "")
        emit("%s.confusion.no.forzadas.en.valores.mezclados" % nombre, mezclados_no, "")

    # --- C1: el emparejamiento del Lema 3 --------------------------------
    # Se prueba sobre una muestra determinista: todas las forzadas, y las
    # primeras 472 no forzadas en orden de recorrido, para tener los dos lados.
    no_forzadas = []
    for perm in itertools.permutations(range(N)):
        seq = list(perm)
        orbits, par, estado, pis = datos(seq, gens, valh)
        if not all(2 * sum(par[k] for k in o) == len(o) for o in orbits):
            no_forzadas.append(seq)
            if len(no_forzadas) >= 472:
                break
    c1_si_forzadas = c1_si_no = 0
    for seq in forzadas:
        orbits, par, estado, pis = datos(seq, gens, valh)
        if all(matching_existe(seq, G, valh, o) for o in orbits):
            c1_si_forzadas += 1
    for seq in no_forzadas:
        orbits, par, estado, pis = datos(seq, gens, valh)
        if all(matching_existe(seq, G, valh, o) for o in orbits):
            c1_si_no += 1
    emit("C1.forzadas.probadas", len(forzadas), "todas")
    emit("C1.forzadas.con.emparejamiento.en.todas.las.orbitas", c1_si_forzadas, "")
    emit("C1.no.forzadas.probadas", len(no_forzadas),
         "las primeras en orden de recorrido, mismo numero que forzadas")
    emit("C1.no.forzadas.con.emparejamiento.en.todas.las.orbitas", c1_si_no, "")
    emit("C1.separa.exacto",
         int(c1_si_forzadas == len(forzadas) and c1_si_no == 0),
         "el Lema 3 alcanza toda orbita forzada y ninguna libre")

    # --- C6: cierre de la clase forzada bajo simetrias -------------------
    Fset = set(tuple(s) for s in forzadas)
    cerrado_G = all(tuple(g[x] for x in s) in Fset for s in forzadas for g in G)
    cerrado_B = all(tuple(g[x] for x in s) in Fset for s in forzadas for g in FAM)
    cerrado_rev = all(tuple(reversed(s)) in Fset for s in forzadas)
    emit("C6.cerrada.bajo.el.grupo.que.respeta.los.bloques", int(cerrado_G), "")
    emit("C6.cerrada.bajo.B_3.entero", int(cerrado_B), "")
    emit("C6.cerrada.bajo.invertir.la.ordenacion", int(cerrado_rev), "")

    # --- la caracterizacion que si sale, y es demostrable ----------------
    # Una orbita esta forzada si y solo si su aportacion observada es la mitad
    # de su cardinal. Y como el grupo contiene todas las traslaciones, las
    # orbitas de pares son las clases de diferencia. Luego forzada equivale a
    # que en cada clase de diferencia la mitad de los pares sea discordante.
    clases = {}
    for k, (i, j) in enumerate(PAIRS):
        pass
    ok = True
    for seq in forzadas[:50] + no_forzadas[:50]:
        posof = {h: i for i, h in enumerate(seq)}
        vals = [valh[h] for h in seq]
        orbits, par, estado, pis = datos(seq, gens, valh)
        es_forzada = all(2 * sum(par[k] for k in o) == len(o) for o in orbits)
        # clases de diferencia: d y su imagen al intercambiar las lineas 2 y 3
        def clase(d):
            e = (d & 1) | ((d >> 1 & 1) << 2) | ((d >> 2 & 1) << 1)
            return min(d, e)
        porclase = {}
        for i in range(N):
            for j in range(i + 1, N):
                d = clase(seq[i] ^ seq[j])
                st = 1 if vals[i] > vals[j] else 0
                a = porclase.setdefault(d, [0, 0])
                a[0] += 1
                a[1] += st
        mitad = all(2 * v[1] == v[0] for v in porclase.values())
        ok = ok and (mitad == es_forzada)
    check("teorema.forzada.equivale.a.mitad.en.cada.clase.de.diferencia", ok,
          "comprobado en 100 casos de los dos lados; la demostracion esta en el informe")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Caracterizacion de la clase forzada en B(3,1), espacio entero.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    print("escrito results/b31-characterization.tsv con %d lineas" % len(ROWS))
    for key, val, _ in ROWS:
        print("  %-56s %s" % (key, val))
    return 0


if __name__ == "__main__":
    sys.exit(main())
