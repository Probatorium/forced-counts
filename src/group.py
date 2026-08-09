#!/usr/bin/env python3
"""
El grupo completo de simetrias afines que cada construccion respeta, y la
contabilidad forzado frente a libre bajo la accion de ese grupo.

Las definiciones estan fijadas y commiteadas antes de esta ejecucion, en
DEFINICIONES-GRUPO.md. Este fichero las implementa y no las cambia.

  R1  f manda cada bloque de la construccion entero sobre un bloque entero
  R2  ademas f conserva el indice dentro del bloque

  epsilon(f, p) = A XOR B, con A = 1 si la permutacion de posiciones inducida
  invierte el orden del par y B = 1 si f invierte el orden binario del par.
  estado(f(p)) = estado(p) XOR epsilon(f, p).

Entradas:  data/sequences.json
Salidas:   results/group-measurements.tsv
           results/group-structure.txt

  python src/group.py
"""

import itertools
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import measure as M                                    # noqa: E402

DATA = os.path.join(ROOT, "data", "sequences.json")
OUT_TSV = os.path.join(ROOT, "results", "group-measurements.tsv")
OUT_TXT = os.path.join(ROOT, "results", "group-structure.txt")

N = M.N
LINES = M.LINES
DENOM = M.DENOM
IDENT = tuple(range(N))

ROWS, TEXT = [], []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def say(line=""):
    TEXT.append(line)


# --- la familia afin ---------------------------------------------------------

def affine_maps():
    """Las 46080 aplicaciones, cada una como tupla de 64 imagenes."""
    out = {}
    for perm in itertools.permutations(range(LINES)):
        table = [sum(((x >> perm[k]) & 1) << k for k in range(LINES)) for x in range(N)]
        for mask in range(N):
            out[tuple(t ^ mask for t in table)] = (perm, mask)
    return out


FAMILY = affine_maps()

NAMES = {}


def describe(g):
    perm, mask = FAMILY[g]
    label = "lineas %s, mascara %s" % ("".join(str(k + 1) for k in perm),
                                       format(mask, "06b"))
    if g in NAMES:
        label += "  [%s]" % NAMES[g]
    return label


def compose(f, g):
    """Primero g, despues f."""
    return tuple(f[g[x]] for x in range(N))


def closure(gens):
    seen = {IDENT}
    frontier = [IDENT]
    while frontier:
        cur = frontier.pop()
        for g in gens:
            nxt = compose(g, cur)
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def generators_of(group):
    """Conjunto generador pequeno, tomado por avidez en orden determinista."""
    ordered = sorted(group, key=lambda g: (FAMILY[g][0], FAMILY[g][1]))
    gens, have = [], {IDENT}
    for g in ordered:
        if g in have:
            continue
        gens.append(g)
        have = closure(gens)
        if len(have) == len(group):
            break
    assert have == set(group), "los generadores no reproducen el grupo"
    return gens


# --- las tres construcciones y sus bloques -----------------------------------

def load():
    with open(DATA, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    seqs = {}
    for name, pats in payload["sequences"].items():
        seqs[name] = [M.enc(p) for p in pats]
    return seqs, payload["provenance"]


BLOCK_SIZE = {"Mawangdui": 8, "Jing Fang": 8, "King Wen": 2}
BLOCK_NAME = {"Mawangdui": "octeto", "Jing Fang": "palacio", "King Wen": "par"}


def blocks_of(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def group_R1(seq, size):
    blocks = [frozenset(b) for b in blocks_of(seq, size)]
    st = set(blocks)
    return [g for g in FAMILY if all(frozenset(g[y] for y in b) in st for b in blocks)]


def group_R2(seq, size):
    blocks = blocks_of(seq, size)
    where = {}
    for bi, b in enumerate(blocks):
        for p, x in enumerate(b):
            where[x] = (bi, p)
    out = []
    for g in FAMILY:
        ok = True
        for b in blocks:
            target = None
            for p, x in enumerate(b):
                bi2, p2 = where[g[x]]
                if p2 != p or (target is not None and bi2 != target):
                    ok = False
                    break
                target = bi2
            if not ok:
                break
        if ok:
            out.append(g)
    return out


# --- la contabilidad por orbitas ---------------------------------------------

def accounting(seq, group, gens, valh):
    """
    Orbitas de pares de posiciones bajo la accion del grupo, y lo que la
    estructura fuerza sobre la aportacion de cada orbita.
    """
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    index = {p: k for k, p in enumerate(pairs)}
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]                 # valor por posicion

    def pi_of(g):
        return [posof[g[seq[i]]] for i in range(N)]

    def step(g, pi, i, j):
        """Devuelve (indice del par imagen, epsilon)."""
        a, b = pi[i], pi[j]
        A = 1 if a > b else 0
        B = 1 if ((valh[g[seq[i]]] > valh[g[seq[j]]]) != (vals[i] > vals[j])) else 0
        key = (a, b) if a < b else (b, a)
        return index[key], A ^ B

    gen_pis = [(g, pi_of(g)) for g in gens]

    orbit = [-1] * len(pairs)
    parity = [0] * len(pairs)
    orbits = []
    for start in range(len(pairs)):
        if orbit[start] != -1:
            continue
        oid = len(orbits)
        orbit[start] = oid
        parity[start] = 0
        stack, members = [start], [start]
        while stack:
            cur = stack.pop()
            i, j = pairs[cur]
            for g, pi in gen_pis:
                nxt, eps = step(g, pi, i, j)
                want = parity[cur] ^ eps
                if orbit[nxt] == -1:
                    orbit[nxt] = oid
                    parity[nxt] = want
                    stack.append(nxt)
                    members.append(nxt)
                else:
                    assert orbit[nxt] == oid, "una orbita se partio: error de aparato"
                    assert parity[nxt] == want, "contradiccion de paridad: error de aparato"
        orbits.append(members)

    status = [1 if vals[i] > vals[j] else 0 for i, j in pairs]
    rep = {}
    forced_orbits = free_orbits = 0
    forced_total = free_observed = 0
    lo = hi = 0
    sizes_free = []
    for oid, members in enumerate(orbits):
        size = len(members)
        c = sum(parity[k] for k in members)
        obs = sum(status[k] for k in members)
        assert obs in (c, size - c), "la aportacion observada no es una de las dos opciones"
        lo += min(c, size - c)
        hi += max(c, size - c)
        if 2 * c == size:
            forced_orbits += 1
            forced_total += c
        else:
            free_orbits += 1
            free_observed += obs
            sizes_free.append(size)
        rep[oid] = (size, c, obs)

    observed = sum(status)
    assert lo <= observed <= hi

    # Totales compatibles con la estructura: cada orbita libre suma su hueco o no.
    gaps = [abs(v[0] - 2 * v[1]) for v in rep.values() if 2 * v[1] != v[0]]
    reach = {0}
    for gp in gaps:
        reach |= {r + gp for r in reach}
    alcanzables = sorted(lo + r for r in reach)

    dists = [abs(t - DENOM // 2) for t in alcanzables]
    best = min(range(len(alcanzables)), key=lambda k: (dists[k], alcanzables[k]))

    return {
        "orbitas": len(orbits),
        "orbitas_de_tamano_impar": sum(1 for m in orbits if len(m) % 2),
        "paridades_alcanzables": len(set(t % 2 for t in alcanzables)),
        "paridad_forzada": alcanzables[0] % 2,
        "alcanzable_mas_cercano_al_esperado": alcanzables[best],
        "desviacion_minima_posible": dists[best],
        "orbitas_forzadas": forced_orbits,
        "orbitas_libres": free_orbits,
        "aportacion_forzada": forced_total,
        "aportacion_libre_observada": free_observed,
        "minimo": lo,
        "maximo": hi,
        "observado": observed,
        "anchura": hi - lo,
        "orbita_mayor": max(len(m) for m in orbits),
        "tamanos_libres": sorted(set(sizes_free)),
        "totales_alcanzables": len(alcanzables),
        "esperado_alcanzable": int((DENOM // 2) in alcanzables),
        "detalle": rep,
    }


def verify_full(seq, group, valh, orbit_data):
    """
    Comprobacion de la relacion epsilon sobre el grupo entero, no solo sobre los
    generadores. Se hace si el coste lo permite; si no, se dice que no se hizo.
    """
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    budget = 1000000 // len(pairs) + 1
    ordered = sorted(group)
    if len(ordered) > budget:                       # muestra por paso constante
        stride = len(ordered) // budget + 1
        group = ordered[::stride]
    index = {p: k for k, p in enumerate(pairs)}
    posof = {h: i for i, h in enumerate(seq)}
    vals = [valh[h] for h in seq]
    status = [1 if vals[i] > vals[j] else 0 for i, j in pairs]
    checks = 0
    for g in group:
        pi = [posof[g[seq[i]]] for i in range(N)]
        for k, (i, j) in enumerate(pairs):
            a, b = pi[i], pi[j]
            A = 1 if a > b else 0
            B = 1 if ((valh[g[seq[i]]] > valh[g[seq[j]]]) != (vals[i] > vals[j])) else 0
            key = (a, b) if a < b else (b, a)
            assert status[index[key]] == status[k] ^ A ^ B, "la relacion epsilon falla"
            checks += 1
    return checks, len(group)


# --- programa -----------------------------------------------------------------

def main():
    seqs, prov = load()
    emit("fuente.commit", prov["commit"], "sin cambios respecto del commit de la medicion")

    # nombres para los elementos reconocibles
    ident = tuple(range(N))
    comp = tuple(x ^ (N - 1) for x in range(N))
    giro = tuple(sum(((x >> (LINES - 1 - k)) & 1) << k for k in range(LINES)) for x in range(N))
    NAMES[ident] = "identidad"
    NAMES[comp] = "complementacion"
    NAMES[giro] = "giro de media vuelta"
    NAMES[compose(comp, giro)] = "giro compuesto con complementacion"

    valh = [M.value(M.dec(x), "yang1", "bottomMSB") for x in range(N)]
    emit("familia.afin.tamano", len(FAMILY), "permutacion de las seis lineas mas mascara")

    say("EL GRUPO COMPLETO POR CONSTRUCCION")
    say("Nociones R1 y R2 tal y como quedaron fijadas en DEFINICIONES-GRUPO.md.")
    say("")

    groups = {}
    for name in ("Mawangdui", "Jing Fang", "King Wen"):
        seq = seqs[name]
        size = BLOCK_SIZE[name]
        g1 = group_R1(seq, size)
        g2 = group_R2(seq, size)
        assert set(g2) <= set(g1)
        assert closure(g1) == set(g1), "R1 no cerro como grupo"
        assert closure(g2) == set(g2), "R2 no cerro como grupo"
        gen1, gen2 = generators_of(g1), generators_of(g2)
        groups[name] = (g1, gen1, g2, gen2)
        short = name.replace(" ", "")

        emit("grupo.R1.%s.orden" % short, len(g1),
             "aplicaciones afines que mandan cada %s entero sobre un %s"
             % (BLOCK_NAME[name], BLOCK_NAME[name]))
        emit("grupo.R1.%s.generadores" % short, len(gen1), "conjunto generador hallado por avidez")
        emit("grupo.R2.%s.orden" % short, len(g2), "ademas conservan el indice dentro del bloque")
        emit("grupo.R2.%s.generadores" % short, len(gen2), "conjunto generador hallado por avidez")
        emit("grupo.R1.%s.contiene.la.complementacion" % short, int(comp in set(g1)), "")
        emit("grupo.R2.%s.contiene.la.complementacion" % short, int(comp in set(g2)), "")
        emit("grupo.R1.%s.contiene.el.giro" % short, int(giro in set(g1)), "")
        emit("grupo.R1.%s.involuciones" % short,
             sum(1 for g in g1 if compose(g, g) == ident and g != ident),
             "para poder comparar con la cifra del commit anterior")

        say("%s, bloques de %d (%s)" % (name, size, BLOCK_NAME[name]))
        say("   R1: orden %d, %d generadores" % (len(g1), len(gen1)))
        for g in gen1:
            say("        " + describe(g))
        say("   R2: orden %d, %d generadores" % (len(g2), len(gen2)))
        for g in gen2:
            say("        " + describe(g))
        say("   contiene la complementacion: R1 %s, R2 %s"
            % (comp in set(g1), comp in set(g2)))
        say("   contiene el giro de media vuelta: R1 %s" % (giro in set(g1)))
        say("")

    # --- contabilidad ---------------------------------------------------------
    say("CONTABILIDAD POR ORBITAS DE PARES DE POSICIONES")
    say("Convencion de referencia: yang = uno, linea inferior mas significativa.")
    say("")

    esperado = DENOM // 2
    emit("valor.esperado.por.azar", esperado, "C(64,2) partido por dos")

    for name in ("Mawangdui", "Jing Fang", "King Wen"):
        seq = seqs[name]
        g1, gen1, g2, gen2 = groups[name]
        short = name.replace(" ", "")

        variants = [
            ("solo.complementacion", [ident, comp], [comp]),
            ("R1", g1, gen1),
            ("R2", g2, gen2),
        ]
        say("%s" % name)
        for vname, grp, gens in variants:
            res = accounting(seq, grp, gens, valh)
            checks, covered = verify_full(seq, grp, valh, res)
            for key in ("orbitas", "orbitas_forzadas", "orbitas_libres",
                        "orbitas_de_tamano_impar",
                        "aportacion_forzada", "aportacion_libre_observada",
                        "minimo", "maximo", "observado", "anchura", "orbita_mayor",
                        "totales_alcanzables", "esperado_alcanzable",
                        "paridades_alcanzables", "paridad_forzada",
                        "alcanzable_mas_cercano_al_esperado",
                        "desviacion_minima_posible"):
                emit("cuenta.%s.%s.%s" % (vname, short, key), res[key], "")
            # Lema: si toda orbita esta forzada, cada una aporta la mitad de su
            # tamano, luego el total es la mitad de C(64,2) y no puede ser otra
            # cosa. El grupo solo puede forzar el empate, nunca otro valor.
            assert res["anchura"] != 0 or res["minimo"] == esperado, "el lema falla"
            emit("cuenta.%s.%s.fuerza.el.empate" % (vname, short),
                 int(res["minimo"] == res["maximo"] == esperado),
                 "criterio declarado: minimo y maximo coinciden en el valor esperado")
            emit("cuenta.%s.%s.comprobacion.epsilon" % (vname, short), checks,
                 "comprobaciones par por elemento, sobre %d elementos del grupo de %d"
                 % (covered, len(grp)))
            say("   %-20s orbitas %4d  forzadas %4d  libres %4d  forzado %4d"
                % (vname, res["orbitas"], res["orbitas_forzadas"],
                   res["orbitas_libres"], res["aportacion_forzada"]))
            say("   %-20s intervalo [%d, %d] anchura %d  observado %d  fuerza el empate: %s"
                % ("", res["minimo"], res["maximo"], res["anchura"], res["observado"],
                   res["minimo"] == res["maximo"] == esperado))
            if res["orbitas_libres"] and res["orbitas_libres"] <= 12:
                det = [(o, v) for o, v in res["detalle"].items() if 2 * v[1] != v[0]]
                for oid, (sz, c, obs) in det:
                    say("        orbita libre %d: tamano %d, opciones %d o %d, observado %d"
                        % (oid, sz, min(c, sz - c), max(c, sz - c), obs))
        say("")

    # --- control: el mismo grupo sobre ordenes de familia barajados -----------
    # El grupo R1 solo depende de la particion en bloques, y barajar el orden de
    # familia no cambia esa particion. Si el grupo bastara por si solo, deberia
    # forzar lo mismo en cualquier orden. Se mide.
    import random                                            # noqa: E402
    rng = random.Random(M.CONTROL_SEED)
    CONTROL_REPS = 300
    emit("control.semilla", M.CONTROL_SEED, "la misma del commit anterior, ya congelada")
    emit("control.repeticiones", CONTROL_REPS,
         "muestra de los 40320 ordenes de familia, no enumeracion: el coste de la contabilidad lo impide")

    say("CONTROL: EL MISMO GRUPO, ORDENES DE FAMILIA BARAJADOS")
    say("")
    controls = (
        ("octetos", "Mawangdui",
         lambda: [M.enc(p) for p in M.build_mawangdui(
             upper_order=rng.sample(M.MWD_UPPER, len(M.MWD_UPPER)))]),
        ("palacios", "Jing Fang",
         lambda: [M.enc(p) for p in M.build_jing_fang(
             head_order=rng.sample(M.JF_HEADS, len(M.JF_HEADS)))]),
    )
    for cname, base, make in controls:
        g1, gen1, _, _ = groups[base]
        gset = set(g1)
        same_group = fuerza_algo = fuerza_el_empate = observado_1008 = 0
        anchuras = set()
        for _ in range(CONTROL_REPS):
            seq = make()
            if set(group_R1(seq, BLOCK_SIZE[base])) == gset:
                same_group += 1
            res = accounting(seq, g1, gen1, valh)
            anchuras.add(res["anchura"])
            if res["anchura"] == 0:
                fuerza_algo += 1
                if res["minimo"] == esperado:
                    fuerza_el_empate += 1
            if res["observado"] == esperado:
                observado_1008 += 1
        emit("control.%s.grupo.identico.al.historico" % cname, same_group,
             "de %d, el grupo R1 no cambia al barajar el orden de familia" % CONTROL_REPS)
        emit("control.%s.el.grupo.fuerza.un.valor" % cname, fuerza_algo,
             "anchura cero: la estructura determina el recuento entero")
        emit("control.%s.el.grupo.fuerza.el.empate" % cname, fuerza_el_empate,
             "anchura cero y ademas el valor forzado es el esperado")
        emit("control.%s.recuento.observado.igual.al.esperado" % cname, observado_1008,
             "para comparar con el control del commit anterior")
        emit("control.%s.anchuras.distintas" % cname, len(anchuras), "conjunto de anchuras observadas")
        emit("control.%s.anchura.maxima" % cname, max(anchuras), "")
        say("   %-9s grupo identico %d/%d, fuerza un valor %d, fuerza el empate %d, observado igual al esperado %d"
            % (cname, same_group, CONTROL_REPS, fuerza_algo, fuerza_el_empate, observado_1008))
    say("")

    # --- las cuatro convenciones bajo R1 --------------------------------------
    say("LAS CUATRO CONVENCIONES BAJO R1")
    say("")
    for name in ("Mawangdui", "Jing Fang", "King Wen"):
        seq = seqs[name]
        g1, gen1, _, _ = groups[name]
        short = name.replace(" ", "")
        for pol in M.POLARITIES:
            for end in M.ENDIANS:
                vh = [M.value(M.dec(x), pol, end) for x in range(N)]
                res = accounting(seq, g1, gen1, vh)
                emit("conv.%s.%s.%s.minimo" % (short, pol, end), res["minimo"], "")
                emit("conv.%s.%s.%s.maximo" % (short, pol, end), res["maximo"], "")
                emit("conv.%s.%s.%s.observado" % (short, pol, end), res["observado"], "")
                emit("conv.%s.%s.%s.orbitas.libres" % (short, pol, end), res["orbitas_libres"], "")
                say("   %-10s %-6s %-10s  [%d, %d]  observado %d  libres %d"
                    % (name, pol, end, res["minimo"], res["maximo"],
                       res["observado"], res["orbitas_libres"]))
    say("")

    # --- caracterizacion de cada grupo, comprobada elemento a elemento -------
    say("CARACTERIZACION DE CADA GRUPO, COMPROBADA ELEMENTO A ELEMENTO")
    say("")

    g1_mwd = set(groups["Mawangdui"][0])
    pred = [g for g, (perm, mask) in FAMILY.items()
            if set(perm[:3]) == {0, 1, 2} and set(perm[3:]) == {3, 4, 5}]
    emit("caracterizacion.Mawangdui.coincide", int(set(pred) == g1_mwd),
         "R1 es exactamente: permutar lineas dentro de cada trigrama, con cualquier mascara")
    emit("caracterizacion.Mawangdui.orden.predicho", 6 * 6 * N, "seis por seis permutaciones, por 64 mascaras")
    say("   Mawangdui: R1 es exactamente el conjunto de aplicaciones que permutan")
    say("   lineas dentro del trigrama inferior y dentro del superior, con cualquier")
    say("   mascara. Orden predicho 6 x 6 x 64 = %d. Coincide: %s"
        % (6 * 6 * N, set(pred) == g1_mwd))

    g1_jf = set(groups["Jing Fang"][0])
    pred = [g for g, (perm, mask) in FAMILY.items()
            if perm == tuple(range(LINES)) and all(((mask >> k) & 1) == ((mask >> (k + 3)) & 1)
                                                   for k in range(3))]
    emit("caracterizacion.JingFang.coincide", int(set(pred) == g1_jf),
         "R1 es exactamente: sin mover lineas, complementar la misma linea en los dos trigramas")
    emit("caracterizacion.JingFang.orden.predicho", 8, "dos elevado a tres mascaras")
    say("   Jing Fang: R1 es exactamente el conjunto de aplicaciones que no mueven")
    say("   ninguna linea y complementan la misma linea en los dos trigramas.")
    say("   Orden predicho 8. Coincide: %s" % (set(pred) == g1_jf))

    g1_kw = set(groups["King Wen"][0])
    conmutan = all(compose(g, giro) == compose(giro, g) for g in g1_kw)
    todos = [g for g in FAMILY if compose(g, giro) == compose(giro, g)]
    emit("caracterizacion.KingWen.todos.conmutan.con.el.giro", int(conmutan),
         "todo elemento de R1 conmuta con el giro de media vuelta")
    emit("caracterizacion.KingWen.coincide.con.el.centralizador", int(set(todos) == g1_kw),
         "R1 es exactamente el centralizador del giro dentro de la familia afin")
    emit("caracterizacion.KingWen.orden.del.centralizador", len(todos), "")
    say("   King Wen: los bloques son las orbitas del giro, y R1 resulta ser")
    say("   exactamente el centralizador del giro dentro de la familia afin.")
    say("   Todos conmutan con el giro: %s. Coincide con el centralizador: %s."
        % (conmutan, set(todos) == g1_kw))
    say("")

    os.makedirs(os.path.dirname(OUT_TSV), exist_ok=True)
    with open(OUT_TSV, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Cada linea es una cifra medida en esta ejecucion.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))
    with open(OUT_TXT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(TEXT) + "\n")

    print("escrito results/group-measurements.tsv con %d cifras" % len(ROWS))
    print("escrito results/group-structure.txt")
    print("\n".join(TEXT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
