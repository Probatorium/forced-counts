#!/usr/bin/env python3
"""
Medicion del recuento de inversiones contra el orden binario.

Entradas:  data/sequences.json, extraido de kingwen-orderings-replication en la
           etiqueta zenodo-v3. Solo las tres secuencias, en forma neutral
           respecto de la convencion de bits.
Salidas:   results/measurements.tsv  una cifra por linea, con clave y nota
           results/permutations.txt  las permutaciones concretas y los testigos

Ninguna cifra de documentos previos entra como dato de este computo. Las unicas
constantes de este fichero son el numero de lineas de un hexagrama, el numero de
hexagramas, y la semilla del control, declarada abajo.

  python src/measure.py
"""

import itertools
import json
import os
import random
import sys
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "sequences.json")
OUT_TSV = os.path.join(ROOT, "results", "measurements.tsv")
OUT_TXT = os.path.join(ROOT, "results", "permutations.txt")

LINES = 6
N = 1 << LINES

# Semilla del control, congelada aqui y declarada en el informe. Cualquier
# cambio de esta constante cambia el control y debe quedar en la historia.
CONTROL_SEED = 20260809
CONTROL_REPS = 100000

ROWS = []      # (clave, valor, nota) que van a measurements.tsv
TEXT = []      # bloques que van a permutations.txt


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def say(line=""):
    TEXT.append(line)


# --- hexagramas -------------------------------------------------------------
# Un hexagrama es una cadena de seis caracteres, indice 0 la linea inferior,
# "y" yang y "n" yin. Esa es la forma en que data/sequences.json los guarda.

def complement(p):
    return "".join("n" if c == "y" else "y" for c in p)


def rotate(p):
    """Giro de media vuelta (fan): la figura vista del otro lado."""
    return p[::-1]


ALL_HEX = ["".join(t) for t in itertools.product("ny", repeat=LINES)]


# --- las cuatro convenciones de bits fijadas en PREREGISTRATION.md ----------

POLARITIES = ("yang1", "yang0")          # yang como uno, o yang como cero
ENDIANS = ("bottomMSB", "bottomLSB")     # linea inferior mas o menos significativa
CONVENTIONS = [(p, e) for p in POLARITIES for e in ENDIANS]


def value(p, polarity, endian):
    total = 0
    for k, ch in enumerate(p):           # k = 0 es la linea inferior
        bit = 1 if ch == "y" else 0
        if polarity == "yang0":
            bit = 1 - bit
        total += bit * (1 << (LINES - 1 - k) if endian == "bottomMSB" else 1 << k)
    return total


def valuer(convention):
    pol, end = convention
    return lambda p: value(p, pol, end)


# --- recuento de inversiones -------------------------------------------------

def inversions_fenwick(vals):
    tree = [0] * (N + 1)
    total = 0
    for x in reversed(vals):
        i = x
        while i > 0:
            total += tree[i]
            i -= i & -i
        i = x + 1
        while i <= N:
            tree[i] += 1
            i += i & -i
    return total


def inversions_naive(vals):
    return sum(1 for i in range(len(vals)) for j in range(i + 1, len(vals))
               if vals[i] > vals[j])


def inversions(vals):
    """Dos implementaciones independientes; discrepar es un error, no un aviso."""
    a = inversions_fenwick(vals)
    b = inversions_naive(vals)
    assert a == b, "las dos implementaciones de inversiones no coinciden"
    return a


DENOM = comb(N, 2)


# --- reconstruccion independiente de las dos construcciones -----------------
# Las reglas de construccion se toman de la documentacion de la fuente. Las
# cifras de la fuente no se toman. La reconstruccion se compara despues con la
# secuencia extraida: si no coinciden, el programa se detiene.

TRI = {"Qian": "yyy", "Dui": "yyn", "Li": "yny", "Zhen": "ynn",
       "Xun": "nyy", "Kan": "nyn", "Gen": "nny", "Kun": "nnn"}
TRI_BY_PATTERN = {v: k for k, v in TRI.items()}

MWD_UPPER = ["Qian", "Gen", "Kan", "Zhen", "Kun", "Dui", "Li", "Xun"]
MWD_LOWER = ["Qian", "Kun", "Gen", "Dui", "Kan", "Li", "Zhen", "Xun"]
JF_HEADS = ["Qian", "Zhen", "Kan", "Gen", "Kun", "Xun", "Li", "Dui"]


def hexg(lower, upper):
    """Lineas 1 a 3 el trigrama inferior, lineas 4 a 6 el superior."""
    return TRI[lower] + TRI[upper]


def flip(p, k):
    """Cambia la linea k, numerada 1 abajo y 6 arriba."""
    lst = list(p)
    lst[k - 1] = "n" if lst[k - 1] == "y" else "y"
    return "".join(lst)


def build_mawangdui(upper_order=None, lower_order=None):
    upper_order = upper_order or MWD_UPPER
    lower_order = lower_order or MWD_LOWER
    out = []
    for u in upper_order:
        out.append(hexg(u, u))
        for l in lower_order:
            if l != u:
                out.append(hexg(l, u))
    return out


def build_palace(head):
    pure = hexg(head, head)
    seq, cur = [pure], pure
    for k in range(1, LINES):                    # generaciones 1 a 5
        cur = flip(cur, k)
        seq.append(cur)
    wandering = flip(seq[5], 4)                  # alma errante
    seq.append(wandering)
    returning = wandering[3:]                    # alma que vuelve
    returning = pure[:3] + returning
    seq.append(returning)
    return seq


def build_jing_fang(head_order=None):
    head_order = head_order or JF_HEADS
    return [v for head in head_order for v in build_palace(head)]


# --- clausura: la permutacion inducida por la complementacion ----------------

def induced_permutation(seq):
    """pi = sigma^-1 . complemento . sigma, sobre posiciones."""
    pos = {p: i for i, p in enumerate(seq)}
    return [pos[complement(p)] for p in seq]


def forced_split(seq, val):
    """
    Descomposicion del recuento en la parte forzada por la clausura y el resto.

    Sea pi la permutacion inducida por la complementacion. Para un par de
    posiciones i<j, la complementacion invierte el orden binario de sus dos
    hexagramas. Luego:

      - si pi conserva el orden relativo del par, el par imagen tiene el estado
        de inversion contrario. La involucion sobre pares empareja entonces cada
        inversion con una no inversion, sin puntos fijos, y esa clase aporta
        exactamente la mitad de sus pares. Eso es lo que la clausura fuerza.
      - si pi invierte el orden relativo del par, el estado se conserva y la
        clausura no dice nada. Esa clase queda libre.

    Devuelve (pares_conservados, forzadas, pares_libres, inversiones_libres).
    """
    pi = induced_permutation(seq)
    vals = [val(p) for p in seq]
    keep = free = inv_keep = inv_free = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            is_inv = vals[i] > vals[j]
            if pi[i] < pi[j]:
                keep += 1
                inv_keep += is_inv
            else:
                free += 1
                inv_free += is_inv
    assert keep % 2 == 0, "la clase conservada deberia tener cardinal par"
    assert inv_keep * 2 == keep, "la mitad forzada no se cumple: revisar el argumento"
    return keep, inv_keep, free, inv_free


def blocks_of(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


# --- codificacion entera, solo para la busqueda exhaustiva de involuciones ---
# El bit k de la codificacion es la linea k+1, con la linea inferior en k = 0.
# Es una codificacion interna de trabajo, no una convencion de lectura: las
# cuatro convenciones de PREREGISTRATION.md se aplican aparte, sobre el patron.

def enc(p):
    return sum((1 << k) for k, ch in enumerate(p) if ch == "y")


def dec(x):
    return "".join("y" if x >> k & 1 else "n" for k in range(LINES))


# --- programa ----------------------------------------------------------------

def main():
    with open(DATA, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    seqs = payload["sequences"]
    prov = payload["provenance"]

    emit("fuente.commit", prov["commit"], "kingwen-orderings-replication en la etiqueta zenodo-v3")
    emit("fuente.tree", prov["tree"], "arbol de la etiqueta")
    emit("fuente.fichero.sha256", prov["extracted_file_sha256"], "verify_paper.py del que salen las secuencias")
    emit("denominador", DENOM, "C(64,2), fijado en PREREGISTRATION.md")
    emit("valor.esperado.por.azar", DENOM // 2, "mitad del denominador, media de una ordenacion al azar")

    # --- reconstruccion independiente -------------------------------------
    rebuilt = {"Mawangdui": build_mawangdui(), "Jing Fang": build_jing_fang()}
    for name, seq in rebuilt.items():
        same = seq == seqs[name]
        emit("reconstruccion.coincide." + name.replace(" ", ""), int(same),
             "1 si la construccion redderivada aqui reproduce la secuencia extraida")
        assert same, "la reconstruccion de %s no reproduce la secuencia extraida" % name
    emit("reconstruccion.coincide.KingWen", 0,
         "King Wen no se reconstruye: es el dato recibido, no una construccion generable")

    for name, seq in seqs.items():
        assert sorted(seq) == sorted(ALL_HEX), "%s no es una permutacion de los 64" % name

    # --- 1. la tabla completa ----------------------------------------------
    for name in ("Mawangdui", "Jing Fang", "King Wen"):
        for conv in CONVENTIONS:
            val = valuer(conv)
            inv = inversions([val(p) for p in seqs[name]])
            key = "inv.%s.%s.%s" % (name.replace(" ", ""), conv[0], conv[1])
            emit(key, inv, "tasa %.6f sobre C(64,2)" % (inv / DENOM))

    # comprobacion de que las cuatro convenciones son cuatro aplicaciones
    # distintas y no la misma escrita de cuatro maneras
    rng = random.Random(CONTROL_SEED)
    probe = ALL_HEX[:]
    rng.shuffle(probe)
    probe_counts = sorted(set(inversions([valuer(c)(p) for p in probe]) for c in CONVENTIONS))
    emit("convenciones.distintas.en.una.ordenacion.de.prueba", len(probe_counts),
         "recuentos distintos que dan las cuatro convenciones sobre una ordenacion barajada con la semilla del control")

    # --- 2. clausura y parte forzada ---------------------------------------
    say("PERMUTACIONES INDUCIDAS POR LA COMPLEMENTACION")
    say("Convencion de referencia para los valores: yang = uno, linea inferior")
    say("como bit mas significativo. Las otras tres se recorren en la tabla.")
    say("")

    _ref_table = {p: value(p, "yang1", "bottomMSB") for p in ALL_HEX}
    ref = _ref_table.__getitem__
    for name in ("Mawangdui", "Jing Fang", "King Wen"):
        seq = seqs[name]
        pi = induced_permutation(seq)
        keep, forced, free, inv_free = forced_split(seq, ref)
        short = name.replace(" ", "")
        emit("clausura.%s.pares.conservados" % short, keep, "pares en los que pi conserva el orden relativo")
        emit("clausura.%s.inversiones.forzadas" % short, forced, "exactamente la mitad de los pares conservados")
        emit("clausura.%s.pares.libres" % short, free, "pares en los que pi invierte el orden relativo")
        emit("clausura.%s.inversiones.libres" % short, inv_free, "no forzadas por la clausura")
        emit("clausura.%s.libres.mitad" % short, free // 2,
             "lo que aportaria la clase libre si tambien se partiera por la mitad")
        emit("clausura.%s.desviacion.en.la.clase.libre" % short, inv_free - free // 2,
             "toda la desviacion respecto del valor esperado vive aqui")
        emit("clausura.%s.total" % short, forced + inv_free, "suma de las dos partes")
        say("%s: pi = " % name + " ".join("%d" % x for x in pi))
        say("   pi es involucion sin puntos fijos: %s"
            % all(pi[pi[i]] == i and pi[i] != i for i in range(N)))
        say("   pi(i) = i + 32 mod 64 para todo i: %s"
            % all(pi[i] == (i + N // 2) % N for i in range(N)))
        say("")

    # --- 2b. Mawangdui: la permutacion, para la retrodiccion -----------------
    mwd = seqs["Mawangdui"]
    say("MAWANGDUI: CLAUSURA DE LA CONSTRUCCION, PERMUTACION CONCRETA")
    say("")
    pim = induced_permutation(mwd)
    oct_map, oct_ok, inner = [], True, []
    for b in range(8):
        targets = set(pim[8 * b + p] // 8 for p in range(8))
        t = targets.pop() if len(targets) == 1 else None
        oct_map.append(t)
        if t is None or t != (b + 4) % 8:
            oct_ok = False
        inner.append([pim[8 * b + p] % 8 for p in range(8)])
    emit("mawangdui.el.complemento.manda.octeto.sobre.octeto", int(all(t is not None for t in oct_map)),
         "cada octeto va entero a un octeto")
    emit("mawangdui.permutacion.octetos.es.desplazamiento.4", int(oct_ok),
         "el octeto de trigrama superior U va al del trigrama superior complementario")
    for b in range(8):
        say("   octeto %d (superior %-5s) -> octeto %s (superior %-5s), posiciones internas %s"
            % (b, MWD_UPPER[b], oct_map[b], MWD_UPPER[oct_map[b]],
               " ".join(str(x) for x in inner[b])))
    say("   La posicion interna si cambia, y cambia de un octeto a otro: el orden")
    say("   interno lleva los trigramas inferiores en parejas complementarias")
    say("   contiguas, y quitar de cada octeto el trigrama repetido desplaza la")
    say("   pareja de forma distinta segun donde caiga el repetido.")
    say("")

    # --- 3. Jing Fang: la demostracion --------------------------------------
    say("JING FANG: CLAUSURA DE LA CONSTRUCCION, PERMUTACION CONCRETA")
    say("")
    heads_img = []
    ok_heads = True
    for b, head in enumerate(JF_HEADS):
        comp_head = TRI_BY_PATTERN[complement(TRI[head])]
        target = JF_HEADS.index(comp_head)
        heads_img.append((b, head, target, comp_head))
        say("   palacio %d %-5s  ->  palacio %d %-5s" % (b, head, target, comp_head))
        if target != (b + 4) % 8:
            ok_heads = False
    say("   la permutacion de palacios es el desplazamiento de cuatro: %s" % ok_heads)
    emit("jingfang.permutacion.palacios.es.desplazamiento.4", int(ok_heads),
         "complementar la cabeza de un palacio lleva al palacio situado cuatro mas alla")

    jf = seqs["Jing Fang"]
    same_pos = all(complement(jf[8 * b + p]) == jf[8 * ((b + 4) % 8) + p]
                   for b in range(8) for p in range(8))
    emit("jingfang.posicion.interna.se.conserva", int(same_pos),
         "el complemento manda la posicion p de un palacio a la misma posicion p del palacio imagen")
    say("   la posicion dentro del palacio no cambia: %s" % same_pos)
    say("   luego pi(8b + p) = 8((b+4) mod 8) + p = (8b + p + 32) mod 64")
    say("")

    # la demostracion algebraica, comprobada termino a termino
    alg = []
    for head in JF_HEADS:
        comp_head = TRI_BY_PATTERN[complement(TRI[head])]
        pal, pal_c = build_palace(head), build_palace(comp_head)
        alg.append(all(complement(pal[p]) == pal_c[p] for p in range(8)))
    emit("jingfang.palacio.complementado.es.palacio.de.la.cabeza.complementada", int(all(alg)),
         "para los ocho palacios, complementar termino a termino da el palacio de la cabeza complementada")
    say("   comprobacion termino a termino en los ocho palacios: %s" % all(alg))
    say("   razon: cada generacion es la cabeza doblada mas una mascara de lineas fija,")
    say("   y complementar conmuta con anadir una mascara. El alma errante anade otra")
    say("   mascara fija. El alma que vuelve restituye el trigrama inferior de la cabeza,")
    say("   y el complemento de esa restitucion es la restitucion del complemento.")
    say("")

    # contraejemplo pedido por la seccion (b): un hexagrama de la construccion
    # cuya imagen bajo complementacion no pertenezca a ella
    outside = [p for p in jf if complement(p) not in set(jf)]
    emit("jingfang.hexagramas.cuya.imagen.sale.de.la.construccion", len(outside),
         "criterio de refutacion declarado en la seccion (b) de PREREGISTRATION.md")

    # --- 4. King Wen: la cifra y la simetria que falta -----------------------
    kw = seqs["King Wen"]
    pairs = [frozenset((kw[2 * i], kw[2 * i + 1])) for i in range(N // 2)]
    pairset = set(pairs)
    emit("kingwen.pares.adyacentes", len(pairs), "la construccion recibida agrupa la secuencia en pares adyacentes")

    rule_rot = sum(1 for i in range(N // 2) if rotate(kw[2 * i]) == kw[2 * i + 1])
    rule_comp = sum(1 for i in range(N // 2) if complement(kw[2 * i]) == kw[2 * i + 1])
    emit("kingwen.pares.por.giro", rule_rot, "el segundo miembro es el giro de media vuelta del primero")
    emit("kingwen.pares.por.complemento", rule_comp, "el segundo miembro es el complemento del primero")
    emit("kingwen.pares.cubiertos.por.la.regla", rule_rot + rule_comp, "giro cuando difiere, complemento cuando el giro no mueve")

    kept = sum(1 for pr in pairs if frozenset(complement(x) for x in pr) in pairset)
    emit("kingwen.pares.que.el.complemento.manda.a.otro.par", kept,
         "clausura de la construccion de King Wen bajo complementacion, a nivel de par")
    witnesses = [pr for pr in pairs if frozenset(complement(x) for x in pr) not in pairset]
    emit("kingwen.pares.que.el.complemento.rompe", len(witnesses), "testigos en results/permutations.txt")

    say("KING WEN: BUSQUEDA DE LA INVOLUCION QUE INVIERTE EL ORDEN BINARIO")
    say("")
    say("   La unica biyeccion que invierte un orden total finito es la que manda")
    say("   el elemento de rango r al de rango n-1-r. Sobre los hexagramas con")
    say("   cualquiera de las cuatro convenciones, esa biyeccion es exactamente la")
    say("   complementacion. Luego no hay que buscar entre todas las involuciones:")
    say("   solo la complementacion puede invertir el orden binario, y la pregunta")
    say("   es si la construccion de King Wen la respeta.")
    say("")
    say("   Pares de King Wen que el complemento manda sobre otro par: %d de %d"
        % (kept, len(pairs)))
    if witnesses:
        say("   Testigos del fallo, hasta cinco:")
        for pr in witnesses[:5]:
            a, b = sorted(pr)
            ca, cb = complement(a), complement(b)
            ia = [i for i, pp in enumerate(pairs) if pp == pr][0]
            say("     par %2d {%s, %s}  ->  {%s, %s}, que no es un par de King Wen"
                % (ia + 1, a, b, ca, cb))
    else:
        say("   No hay testigo del fallo: la construccion respeta la involucion.")
        say("   La razon es demostrable y no depende de la secuencia recibida. Los")
        say("   pares de King Wen son las orbitas del giro de media vuelta de tamano")
        say("   dos, mas los pares que forman por complementacion los hexagramas que")
        say("   el giro deja quietos. El giro y la complementacion conmutan, luego la")
        say("   complementacion manda orbita del giro sobre orbita del giro, y manda")
        say("   el par de dos hexagramas complementarios sobre si mismo.")
        rot_orbits = set(frozenset((x, rotate(x))) for x in ALL_HEX if rotate(x) != x)
        pal = [x for x in ALL_HEX if rotate(x) == x]
        pal_pairs = set(frozenset((x, complement(x))) for x in pal)
        say("     orbitas del giro de tamano dos: %d" % len(rot_orbits))
        say("     hexagramas que el giro deja quietos: %d, que forman %d pares"
            % (len(pal), len(pal_pairs)))
        say("     esas dos familias son exactamente los pares de King Wen: %s"
            % (rot_orbits | pal_pairs == pairset))
        say("     el giro y la complementacion conmutan en los 64: %s"
            % all(rotate(complement(x)) == complement(rotate(x)) for x in ALL_HEX))
        emit("kingwen.orbitas.del.giro.de.tamano.dos", len(rot_orbits),
             "primera familia de pares de la construccion")
        emit("kingwen.hexagramas.que.el.giro.deja.quietos", len(pal),
             "los que se emparejan por complementacion, segunda familia")
        emit("kingwen.las.dos.familias.son.los.32.pares",
             int(rot_orbits | pal_pairs == pairset),
             "la construccion queda cubierta por las dos familias")
        emit("kingwen.giro.y.complemento.conmutan",
             int(all(rotate(complement(x)) == complement(rotate(x)) for x in ALL_HEX)),
             "de aqui sale la clausura, sin mirar la secuencia recibida")
    say("")
    say("   El giro de media vuelta, que la construccion tambien respeta, no invierte")
    say("   el orden binario. Testigo:")
    bad = None
    for a, b in itertools.combinations(ALL_HEX, 2):
        if ref(a) < ref(b) and ref(rotate(a)) < ref(rotate(b)):
            bad = (a, b)
            break
    say("     %s < %s en binario, y sus giros %s < %s siguen en el mismo orden"
        % (bad[0], bad[1], rotate(bad[0]), rotate(bad[1])))
    say("")

    # Busqueda documentada sobre la familia afin de F_2^6: toda aplicacion
    # x -> permutacion de las seis lineas, seguida de complementar un subconjunto
    # de lineas. Son 720 por 64 aplicaciones. Contiene la complementacion, el
    # giro de media vuelta, su composicion, y toda relectura de las lineas.
    ref_int = [ref(dec(x)) for x in range(N)]
    pairs_int = set(frozenset(enc(y) for y in pr) for pr in pairs)
    fam_total = fam_inv = fam_rev = fam_pres = fam_both = 0
    found = []
    for perm in itertools.permutations(range(LINES)):
        table = [sum(((x >> perm[k]) & 1) << k for k in range(LINES)) for x in range(N)]
        for mask in range(N):
            fam_total += 1
            img = [table[x] ^ mask for x in range(N)]
            if any(img[img[x]] != x for x in range(N)):
                continue
            fam_inv += 1
            reverses = all(ref_int[img[x]] == N - 1 - ref_int[x] for x in range(N))
            preserves = all(frozenset(img[y] for y in pr) in pairs_int for pr in pairs_int)
            fam_rev += reverses
            fam_pres += preserves
            if reverses and preserves:
                fam_both += 1
                found.append((perm, mask))

    say("   Busqueda sobre la familia afin: %d aplicaciones, %d involuciones."
        % (fam_total, fam_inv))
    say("   Involuciones que invierten el orden binario: %d." % fam_rev)
    say("   Involuciones que la construccion de King Wen respeta: %d." % fam_pres)
    say("   Las que cumplen las dos cosas, exhibidas:")
    for perm, mask in found:
        say("     lineas %s, mascara de complementacion %s  =  %s"
            % ("".join(str(k + 1) for k in perm), format(mask, "06b"),
               "la complementacion" if perm == tuple(range(LINES)) and mask == N - 1
               else "otra"))
    say("")

    emit("busqueda.familia.afin.aplicaciones", fam_total,
         "x -> permutacion de las seis lineas seguida de una mascara de complementacion")
    emit("busqueda.familia.afin.involuciones", fam_inv, "de esas, las que son involucion")
    emit("busqueda.involuciones.que.invierten.el.orden.binario", fam_rev,
         "solo puede haber una, y la busqueda lo confirma")
    emit("busqueda.involuciones.que.la.construccion.de.kingwen.respeta", fam_pres,
         "mandan todo par de King Wen sobre un par de King Wen")
    emit("busqueda.involuciones.que.cumplen.las.dos.cosas", fam_both,
         "interseccion: invierten el orden binario y la construccion las respeta")

    # --- 5. control ----------------------------------------------------------
    expected = DENOM // 2
    rng = random.Random(CONTROL_SEED)
    emit("control.semilla", CONTROL_SEED, "congelada en src/measure.py, declarada en el informe")
    emit("control.repeticiones", CONTROL_REPS, "por variante")

    variants = {
        "octetos.orden.de.familia": lambda: build_mawangdui(
            upper_order=rng.sample(MWD_UPPER, len(MWD_UPPER))),
        "octetos.orden.interno": lambda: build_mawangdui(
            lower_order=rng.sample(MWD_LOWER, len(MWD_LOWER))),
        "octetos.los.dos.ordenes": lambda: build_mawangdui(
            upper_order=rng.sample(MWD_UPPER, len(MWD_UPPER)),
            lower_order=rng.sample(MWD_LOWER, len(MWD_LOWER))),
        "palacios.orden.de.familia": lambda: build_jing_fang(
            head_order=rng.sample(JF_HEADS, len(JF_HEADS))),
    }
    for vname, make in variants.items():
        hits = 0
        seen = set()
        closure_checked, closure_ok = 0, True
        for _ in range(CONTROL_REPS):
            seq = make()
            inv = inversions_fenwick([ref(p) for p in seq])
            seen.add(inv)
            if inv == expected:
                hits += 1
            if closure_checked < 1000:       # muestra de comprobacion de clausura
                closure_checked += 1
                st = set(frozenset(b) for b in blocks_of(seq, 8))
                if not all(frozenset(complement(x) for x in b) in st for b in st):
                    closure_ok = False
        distinct = len(seen)
        emit("control.%s.aciertos" % vname, hits,
             "ordenaciones al azar cuyo recuento cae exactamente en el valor esperado")
        emit("control.%s.tasa" % vname, "%.5f" % (hits / CONTROL_REPS),
             "aciertos entre repeticiones")
        emit("control.%s.recuentos.distintos" % vname, distinct, "valores distintos observados")
        emit("control.%s.minimo" % vname, min(seen), "recuento mas bajo observado")
        emit("control.%s.maximo" % vname, max(seen), "recuento mas alto observado")
        emit("control.%s.clausura.se.mantiene" % vname, int(closure_ok),
             "en las %d primeras repeticiones el complemento sigue mandando bloque sobre bloque"
             % closure_checked)

    # enumeracion exhaustiva, que hace exacta la tasa anterior en dos variantes
    for ename, gen in (("octetos.orden.de.familia",
                        lambda perm: build_mawangdui(upper_order=list(perm))),
                       ("palacios.orden.de.familia",
                        lambda perm: build_jing_fang(head_order=list(perm)))):
        base = MWD_UPPER if ename.startswith("octetos") else JF_HEADS
        total = hits = 0
        for perm in itertools.permutations(base):
            total += 1
            if inversions_fenwick([ref(p) for p in gen(perm)]) == expected:
                hits += 1
        emit("exhaustivo.%s.ordenes" % ename, total, "todas las ordenaciones de familia posibles")
        emit("exhaustivo.%s.aciertos" % ename, hits, "las que dan exactamente el valor esperado")
        emit("exhaustivo.%s.tasa" % ename, "%.5f" % (hits / total), "aciertos entre ordenes")

    # --- escritura -----------------------------------------------------------
    os.makedirs(os.path.dirname(OUT_TSV), exist_ok=True)
    with open(OUT_TSV, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Cada linea es una cifra medida en esta ejecucion.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val_, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val_, note))
    with open(OUT_TXT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(TEXT) + "\n")

    print("escrito results/measurements.tsv con %d cifras" % len(ROWS))
    print("escrito results/permutations.txt")
    for key, val_, _ in ROWS:
        if key.startswith("inv.") or key.startswith("control.") or key.startswith("exhaustivo."):
            print("  %-60s %s" % (key, val_))
    return 0


if __name__ == "__main__":
    sys.exit(main())
