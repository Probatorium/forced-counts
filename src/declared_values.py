#!/usr/bin/env python3
"""
El congelador de cifras del manuscrito.

Una cifra impresa en la prosa del manuscrito tiene que salir de un fichero de
results, y tiene que seguir saliendo de ahi cuando alguien vuelva a correr las
mediciones. Este comprobador es lo que ata las dos cosas.

Cada cifra publicable lleva en el fichero de su seccion una DECLARACION:

    <!-- CIFRAS: 1013 = results/measurements.tsv:19 inv.KingWen.yang1.bottomMSB -->

y el comprobador exige las cuatro cosas a la vez:

  1. que el fichero de results exista, que esa linea exista, y que la clave de
     esa linea sea exactamente la declarada, no otra que se le parezca;
  2. que el valor de esa linea sea exactamente el valor declarado;
  3. que el valor declarado aparezca de verdad impreso en la prosa de esa misma
     seccion, para que no queden declaraciones de adorno apuntando a cifras que
     el texto no imprime;
  4. que ninguna cifra impresa en la prosa quede SIN declarar.

Y una quinta, que es la leccion de la sesion anterior escrita como codigo:

  5. que el cotejo no pase en vacio. Si no se extrae ninguna cifra de la prosa,
     o no hay ninguna declaracion, el comprobador falla en vez de dar un uno.
     Una comprobacion que pasa en vacio no comprueba nada.

Para el punto 4 hay que decidir que es una cifra publicable y que es un digito
que aparece por otra razon: el numero de una seccion, un identificador de arXiv,
un exponente. Esas razones estan abajo en MASCARAS, cada una con su motivo, y el
informe dice cuantas veces ha aplicado cada una, para que ninguna exencion sea
silenciosa. Lo que no cae bajo una mascara declarada, se declara o falla.

Modos:

    python src/declared_values.py            comprueba
    python src/declared_values.py --rellenar  resuelve los ':?' a su linea real

El modo rellenar existe para que los numeros de linea de las declaraciones no se
cuenten a mano nunca. Se escribe la declaracion con ':?' y la herramienta la
resuelve buscando la clave. El modo de comprobacion NO acepta ':?'.

Salida: results/declared-values.tsv
"""

import ast
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")
OUT = os.path.join(ROOT, "results", "declared-values.tsv")

# Los ficheros de prosa. PAPER.md queda fuera a proposito: es la salida del
# ensamblador y comprobarlo seria comprobar dos veces lo mismo.
FUENTES = ["00-abstract.md"] + ["0%d-%s" % (i, s) for i, s in [
    (1, "introduction.md"), (2, "preliminaries.md"), (3, "orbit-accounting.md"),
    (4, "parity-obstruction.md"), (5, "characterisation.md"),
    (6, "three-historical-orderings.md"), (7, "landscape.md"),
    (8, "open-problems.md"), (9, "verification.md"),
]]

DECL = re.compile(r"<!--\s*CIFRAS?:(.*?)-->", re.S)

# Una cifra derivada es la que el texto obtiene a la vista, con una cuenta, a
# partir de cifras ya declaradas en la misma seccion. No sale de results, sale de
# la aritmetica, asi que el comprobador la hace: evalua la expresion, exige que
# de el valor impreso, y exige ademas que cada operando este declarado aqui. Sin
# esto, la unica salida seria no imprimir la cuenta, y el texto perderia
# justamente el paso que el lector quiere seguir.
DERIV = re.compile(r"<!--\s*CIFRAS?\s+DERIVADAS?:(.*?)-->", re.S)
ENTRADA_DERIV = re.compile(r"([\d.]+)\s*=\s*([\d\s+\-*/().]+?)(?=;|$)")
# El valor puede ir entre comillas cuando lleva espacios, que es el caso de las
# claves que miden un vector, como las multiplicidades linea por linea. Cuando el
# valor es un vector, cada una de sus componentes cuenta tambien como declarada,
# porque la prosa las imprime sueltas.
ENTRADA = re.compile(
    r"(\"[^\"]+\"|[^\s=;]+)\s*=\s*(results/[\w.\-]+):(\d+|\?)\s+([^\s;]+)")

# Mascaras: trozos de texto donde un digito no es una cifra medida. Cada una con
# su motivo, y el informe cuenta cuantas veces aplica cada una. Nada se exime en
# silencio.
MASCARAS = [
    ("cita.numerica",
     r"\[\d{1,2}(?:\s*,\s*\d{1,2})*\]",
     "el numero entre corchetes es una referencia, no una medicion; desde que "
     "las claves alfabeticas se cambiaron por numeros, una cita se parece a "
     "una cifra y hay que separarlas"),
    ("titulo.de.seccion",
     r"^#+\s.*$",
     "el numero de un encabezado es el de la seccion, no una medicion"),
    ("cita.verbatim",
     r"^>\s*\".*(?:\n>.*)*",
     "linea de cita literal de otro autor: sus cifras no son nuestras"),
    ("identificador.bibliografico",
     r"arXiv:\S+|doi\s+10\.\S+|ISBN\s+\S+|Oracle Paper\s+No\.\s*\d+|Lean\s+\d+"
     r"|(?:printed\s+)?pages?\s+\d+(?:\s+(?:and|to)\s+\d+)*",
     "identificador de un artefacto, no una medicion"),
    ("referencia.cruzada",
     r"(?:[Ss]ection|[Ll]emma|[Tt]heorem|[Cc]orollary|[Pp]roposition|[Aa]ppendix"
     r"|[Ee]xample|[Dd]efinition|[Ee]quation|[Pp]art|[Aa]mendment)s?\s+"
     r"\(?\d+[a-z]?(?:\.\d+)*\)?(?:\s*(?:,|and|to)\s*\d+(?:\.\d+)*)*",
     "puntero interno o a otro texto, no una medicion"),
    ("simbolo",
     r"[A-Za-z_]\w*\([^)]*\)"
     r"|2\^[\w()+-]+|2 to the n|[Nn]\s*minus\s*\w+|N-1"
     r"|\{1, \.\.\., n\}|\|c_i[^|]*\|\s*<\s*\d+"
     r"|dim\s+V\s*>=\s*\d+|\bk\s*>=\s*\d+|XOR\s+[01]|=\s*[01](?![\d.])"
     r"|n\(n-1\)/\d+|\d+/\d+-mesic|size\s+two|of\s+two\b",
     "la cifra es parte de un simbolo matematico, no una medicion"),
    ("indice",
     r"coordinates?\s+\d+(?:\s+to\s+\d+)?|positions?\s+\d+"
     r"|n\s*=\s*\d+|k\s*=\s*\d+|B\(\d+,\s*\d+\)|B_\d"
     r"|between\s+\d+\s+and|line\s+\d+|dimensions?\s+\w+",
     "indice, coordenada o dimension nombrada, no una medicion"),
    ("indice.de.tabla",
     r"^\|\s*\d+\s*\|\s*\d+\s*\|"
     r"|^\|\s*[A-Za-z][^|]*\|\s*\d+\s*\|\s*\d+\s*\|",
     "las columnas n y k de una fila de tabla son indices, no mediciones"),
    ("recuento.de.filas",
     r"\d+\s+rows\b",
     "numero de filas de una tabla impresa en la propia seccion: el lector lo "
     "cuenta en la pagina, no sale de results"),
    ("fecha",
     r"(?:January|February|March|April|May|June|July|August|September|October"
     r"|November|December|Summer|Winter|Spring|Autumn)\s+\d{4}",
     "fecha de publicacion, no una medicion"),
    ("grado",
     r"\d+\s+degree",
     "medida angular de una simetria descrita en palabras"),
]

DIGITOS = re.compile(r"(?<![\w.,:/-])\d+(?:\.\d+)?(?![\w:/-])(?!\.\d)")

ROWS = []
FALLOS = []
total_deriv = [0]
constantes = [0]


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def fallo(msg):
    FALLOS.append(msg)


def aritmetica(expr):
    """Evalua una expresion aritmetica y solo aritmetica.

    Se recorre el arbol de ast admitiendo unicamente numeros y las cuatro
    operaciones con parentesis y signo. Nada de nombres, llamadas ni atributos:
    lo que entra aqui son comentarios de un fichero del propio repositorio, pero
    un comprobador que ejecuta texto arbitrario deja de ser un comprobador.
    """
    permitidos = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                  ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Pow,
                  ast.USub, ast.UAdd)
    arbol = ast.parse(expr.strip(), mode="eval")
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, permitidos):
            raise ValueError("nodo no permitido: %s" % type(nodo).__name__)
        if isinstance(nodo, ast.Constant) and not isinstance(nodo.value,
                                                             (int, float)):
            raise ValueError("constante no numerica")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else +v
        a, b = ev(n.left), ev(n.right)
        if isinstance(n.op, ast.Add):
            return a + b
        if isinstance(n.op, ast.Sub):
            return a - b
        if isinstance(n.op, ast.Mult):
            return a * b
        if isinstance(n.op, ast.Div):
            return a / b
        if isinstance(n.op, ast.FloorDiv):
            return a // b
        return a ** b

    return ev(arbol)


def leer_seccion(nombre, overrides=None):
    """El texto de una seccion, o el que se le pase en lugar del suyo.

    Existe este rodeo para que la prueba por mutacion pueda correr el
    comprobador entero sobre un texto alterado sin escribir esa alteracion en el
    arbol de trabajo. Una prueba que deja el repositorio sucio si falla a la
    mitad no es una prueba, es un riesgo.
    """
    if overrides and nombre in overrides:
        return overrides[nombre]
    ruta = os.path.join(PAPER, nombre)
    if not os.path.exists(ruta):
        return None
    return open(ruta, encoding="utf-8").read()


def prosa(texto):
    """El texto sin comentarios de ensamblaje: lo que el lector ve."""
    return re.sub(r"<!--.*?-->", " ", texto, flags=re.S)


def leer_results(rel):
    ruta = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(ruta):
        return None
    return open(ruta, encoding="utf-8").read().split("\n")


def linea_de_clave(lineas, clave):
    """Numero de linea, base 1, de la clave pedida. None si no esta o repite."""
    hits = [i + 1 for i, l in enumerate(lineas)
            if l.split("\t")[0] == clave]
    if len(hits) != 1:
        return None
    return hits[0]


def declaraciones(texto):
    for bloque in DECL.findall(texto):
        for val, fich, lin, clave in ENTRADA.findall(bloque):
            yield val.strip('"'), fich, lin, clave


def rellenar():
    """Resuelve los ':?' de las declaraciones al numero de linea real."""
    cambios = 0
    for nombre in FUENTES:
        ruta = os.path.join(PAPER, nombre)
        t = open(ruta, encoding="utf-8").read()
        original = t
        for val, fich, lin, clave in list(declaraciones(t)):
            lineas_actuales = leer_results(fich)
            if lin != "?":
                # RERESOLUCION. Un puntero ya resuelto se vuelve a resolver si
                # ha dejado de apuntar a su clave, que es lo que pasa en cuanto
                # un fichero de results gana una fila por encima. La clave manda
                # sobre el numero de linea; el numero es un atajo para el lector.
                if lineas_actuales is None:
                    continue
                i = int(lin)
                if (1 <= i <= len(lineas_actuales)
                        and lineas_actuales[i - 1].split("\t")[0] == clave):
                    continue
                n = linea_de_clave(lineas_actuales, clave)
                if n is None:
                    print("clave no encontrada o repetida: %s en %s (%s)"
                          % (clave, fich, nombre))
                    continue
                for escrito in ('"%s"' % val, val):
                    patron = (re.escape("%s = %s:%s %s" % (escrito, fich, lin, clave))
                              + r"(?![\w.])")
                    t, k = re.subn(patron, "%s = %s:%d %s" % (escrito, fich, n, clave), t)
                    if k:
                        cambios += k
                        break
                continue
            lineas = leer_results(fich)
            if lineas is None:
                print("no existe %s (en %s)" % (fich, nombre))
                continue
            n = linea_de_clave(lineas, clave)
            if n is None:
                print("clave no encontrada o repetida: %s en %s (%s)"
                      % (clave, fich, nombre))
                continue
            # La clave se ancla con un limite por la derecha: una clave puede
            # ser prefijo de otra, y sin el ancla el reemplazo se comeria la
            # declaracion larga al resolver la corta.
            for escrito in ('"%s"' % val, val):
                patron = (re.escape("%s = %s:? %s" % (escrito, fich, clave))
                          + r"(?![\w.])")
                nuevo_txt = "%s = %s:%d %s" % (escrito, fich, n, clave)
                t, k = re.subn(patron, nuevo_txt.replace("\\", "\\\\"), t)
                if k:
                    cambios += k
                    break
        if t != original:
            open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    print("lineas resueltas: %d" % cambios)
    return 0


def comprobar(overrides=None):
    del ROWS[:]
    del FALLOS[:]
    total_deriv[0] = 0
    constantes[0] = 0
    total_decl = 0
    total_cifras = 0
    mascaradas = {k: 0 for k, _, _ in MASCARAS}

    for nombre in FUENTES:
        t = leer_seccion(nombre, overrides)
        if t is None:
            fallo("falta la seccion %s" % nombre)
            continue
        cuerpo = prosa(t)

        # --- las declaraciones de esta seccion ---------------------------
        declaradas = set()
        for val, fich, lin, clave in declaraciones(t):
            total_decl += 1
            if lin == "?":
                fallo("%s: declaracion sin resolver, %s = %s:? %s"
                      % (nombre, val, fich, clave))
                continue
            lineas = leer_results(fich)
            if lineas is None:
                fallo("%s: %s no existe" % (nombre, fich))
                continue
            i = int(lin)
            if i < 1 or i > len(lineas):
                fallo("%s: %s:%d fuera del fichero" % (nombre, fich, i))
                continue
            campos = lineas[i - 1].split("\t")
            if campos[0] != clave:
                fallo("%s: %s:%d dice la clave '%s' y la declaracion dice '%s'"
                      % (nombre, fich, i, campos[0], clave))
                continue
            real = campos[1] if len(campos) > 1 else ""
            if real != val:
                fallo("%s: la prosa imprime %s y %s:%d (%s) mide %s"
                      % (nombre, val, fich, i, clave, real))
                continue
            if val not in cuerpo:
                fallo("%s: se declara %s (%s) pero la prosa no lo imprime"
                      % (nombre, val, clave))
                continue
            declaradas.add(val)
            if " " in val:
                declaradas.update(val.split())

        # --- las cifras derivadas de esta seccion -------------------------
        for bloque in DERIV.findall(t):
            for valor, expr in ENTRADA_DERIV.findall(bloque):
                total_deriv[0] += 1
                operandos = re.findall(r"[\d.]+", expr)
                faltan = [o for o in operandos
                          if o not in declaradas and len(o) > 1]
                constantes[0] += sum(1 for o in operandos
                                     if o not in declaradas and len(o) == 1)
                if faltan:
                    fallo("%s: la derivada %s = %s usa operandos no declarados: %s"
                          % (nombre, valor, expr.strip(), " ".join(faltan)))
                    continue
                try:
                    obtenido = aritmetica(expr)
                except Exception as e:
                    fallo("%s: la derivada %s = %s no evalua (%s)"
                          % (nombre, valor, expr.strip(), e))
                    continue
                if float(obtenido) != float(valor):
                    fallo("%s: la prosa imprime %s y la cuenta %s da %s"
                          % (nombre, valor, expr.strip(), obtenido))
                    continue
                if valor not in cuerpo:
                    fallo("%s: se declara la derivada %s pero la prosa no la imprime"
                          % (nombre, valor))
                    continue
                declaradas.add(valor)

        # --- las cifras que la prosa imprime -----------------------------
        enmascarado = cuerpo
        for clave_m, patron, _ in MASCARAS:
            def _tapa(m):
                mascaradas[clave_m] += 1
                return re.sub(r"\d", "#", m.group(0))
            enmascarado = re.sub(patron, _tapa, enmascarado, flags=re.M)

        sueltas = []
        for m in DIGITOS.finditer(enmascarado):
            cifra = m.group(0)
            total_cifras += 1
            if cifra not in declaradas:
                ctx = enmascarado[max(0, m.start() - 45):m.end() + 25]
                sueltas.append((cifra, " ".join(ctx.split())))
        for cifra, ctx in sueltas:
            fallo("%s: la cifra %s se imprime sin declaracion de procedencia "
                  "(...%s...)" % (nombre, cifra, ctx))

        emit("declaradas.%s" % nombre, len(declaradas), "")

    emit("declaraciones.totales", total_decl, "")
    emit("derivadas.comprobadas", total_deriv[0],
         "cifras que el texto obtiene con una cuenta a la vista")
    emit("constantes.aritmeticas.en.derivadas", constantes[0],
         "digitos sueltos que son la operacion y no una cifra publicable")
    emit("cifras.impresas.en.la.prosa", total_cifras, "")
    for k, _, motivo in MASCARAS:
        emit("enmascaradas.%s" % k, mascaradas[k], motivo)

    # --- la quinta comprobacion: nada de pasar en vacio -------------------
    vacio = total_decl == 0 or total_cifras == 0
    emit("el.cotejo.pasa.en.vacio", int(vacio),
         "si vale uno, el comprobador no ha comprobado nada")
    if vacio:
        fallo("el cotejo pasa en vacio: %d declaraciones, %d cifras impresas"
              % (total_decl, total_cifras))

    emit("desajustes", len(FALLOS), "")
    emit("toda.cifra.impresa.sale.de.results", int(not FALLOS), "")

    if overrides:
        return 1 if FALLOS else 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Congelador de cifras del manuscrito.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        for f in FALLOS:
            fh.write("DESAJUSTE\t1\t%s\n" % f)

    for k, v, _ in ROWS:
        if not k.startswith("declaradas."):
            print("  %-42s %s" % (k, v))
    if FALLOS:
        print("\nDESAJUSTES:")
        for f in FALLOS:
            print("  " + f)
        return 1
    return 0


SEIS = "06-three-historical-orderings.md"
NUEVE = "09-verification.md"

# Las secciones que se mutan. Son dos porque las cifras del manuscrito salen de
# dos clases de fichero distintas: las de results que produce una medicion, y la
# de results que produce el propio registro de esfuerzo. Una mutacion en la
# seccion 6 no prueba nada sobre la 9.
SECCIONES_MUTADAS = [
    (SEIS, "la cifra sale de una medicion"),
    (NUEVE, "la cifra sale del registro de esfuerzo"),
]


def objetivo(seccion):
    """Elige que cifra mutar, en vez de llevarla escrita a mano.

    Se toma la primera declaracion de la seccion cuyo valor aparezca en la prosa
    en negrita, y se muta a ese valor mas uno. Se hace asi porque una cifra
    escrita a mano en el codigo de la prueba caduca: las del registro de esfuerzo
    se refrescan cada vez que se cierra una sesion, y la prueba empezaria a
    fallar por estar desactualizada y no por haber encontrado nada.
    """
    t = leer_seccion(seccion)
    cuerpo = prosa(t)
    for val, fich, lin, clave in declaraciones(t):
        if not val.isdigit():
            continue
        marca = "**%s**" % val
        if marca in cuerpo:
            return val, str(int(val) + 1), fich, clave
    return None


def mutacion():
    """Rompe a proposito una cifra de la prosa y exige que salte el aviso.

    Una asercion que nunca se ha visto fallar no esta probada: puede estar
    comprobando otra cosa, o nada. Aqui se altera el texto de dos secciones de
    dos maneras cada una, se corre el comprobador entero sobre cada texto
    alterado, y se exige que el aviso NOMBRE la cifra. Despues se corre sin mutar
    y se exige que no quede ningun desajuste. Las corridas se registran todas,
    porque el valor de la prueba esta en que figure la que falla y no solo la que
    pasa.

    Nada de esto se escribe en el arbol de trabajo: el texto alterado vive en
    memoria y los ficheros se comprueban intactos al final.
    """
    originales = {s: leer_seccion(s) for s, _ in SECCIONES_MUTADAS}
    filas = []
    todas_saltan = True
    probadas = 0

    for seccion, porque in SECCIONES_MUTADAS:
        obj = objetivo(seccion)
        if obj is None:
            fallo("no hay cifra que mutar en %s" % seccion)
            todas_saltan = False
            continue
        val, roto_val, fich, clave = obj
        etiqueta = seccion.split("-")[0]

        casos = [
            ("%s.cifra.sin.declarar" % etiqueta,
             [("**%s**" % val, "**%s**" % roto_val)],
             "se cambia la cifra en la prosa y no en su declaracion: tiene que "
             "saltar como cifra impresa sin procedencia"),
            ("%s.la.prosa.contradice.a.results" % etiqueta,
             [("**%s**" % val, "**%s**" % roto_val),
              ("%s = %s" % (val, fich), "%s = %s" % (roto_val, fich))],
             "se cambian la cifra y su declaracion a la vez: tiene que saltar "
             "porque el valor declarado ya no es el que mide la linea"),
        ]

        for nombre, cambios, motivo in casos:
            mutado = originales[seccion]
            for viejo_txt, nuevo_txt in cambios:
                if viejo_txt not in mutado:
                    fallo("la mutacion %s no encuentra %r" % (nombre, viejo_txt))
                    todas_saltan = False
                    mutado = None
                    break
                mutado = mutado.replace(viejo_txt, nuevo_txt, 1)
            if mutado is None:
                continue

            probadas += 1
            comprobar(overrides={seccion: mutado})
            avisos = list(FALLOS)
            esperado = [a for a in avisos if roto_val in a]
            todas_saltan = todas_saltan and bool(esperado)
            filas += [
                ("%s.seccion" % nombre, seccion, porque),
                ("%s.cifra" % nombre, "%s por %s (%s)" % (val, roto_val, clave),
                 "elegida por la propia herramienta, no escrita a mano"),
                ("%s.desajustes" % nombre, len(avisos), motivo),
                ("%s.el.comprobador.nombra.la.cifra" % nombre,
                 int(bool(esperado)),
                 "si vale cero, el comprobador no vigila lo que dice vigilar"),
                ("%s.aviso" % nombre, esperado[0] if esperado else "ninguno", ""),
            ]

    limpio = comprobar()
    intactas = all(leer_seccion(s) == o for s, o in originales.items())
    filas += [
        ("mutaciones.probadas", probadas, ""),
        ("corrida.restaurada.desajustes", len(FALLOS), ""),
        ("corrida.restaurada.limpia", int(limpio == 0), ""),
        ("las.secciones.quedan.intactas", int(intactas),
         "el texto mutado vive en memoria y nunca se escribe"),
        ("la.prueba.por.mutacion.pasa",
         int(todas_saltan and limpio == 0 and intactas and probadas == 4),
         "la asercion se ha visto fallar cuando debia y callar cuando debia"),
    ]

    ruta = os.path.join(ROOT, "results", "mutation-test.tsv")
    with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Prueba por mutacion del congelador de cifras.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in filas:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
    for k, v, _ in filas:
        print("  %-46s %s" % (k, v))

    if not intactas:
        print("alguna seccion quedo alterada: eso no puede pasar")
        return 1
    return 0 if (todas_saltan and limpio == 0 and probadas == 4) else 1


def main():
    if "--rellenar" in sys.argv:
        return rellenar()
    if "--mutacion" in sys.argv:
        return mutacion()
    return comprobar()


if __name__ == "__main__":
    sys.exit(main())
