#!/usr/bin/env python3
"""
Constructor del manuscrito en LaTeX y en PDF, desde paper/PAPER.md.

paper/PAPER.md es la fuente unica: la produce src/assemble_paper.py juntando las
nueve secciones, y sus cifras estan congeladas contra results por
src/declared_values.py. Este programa no vuelve a redactar nada: parsea ese
fichero a un modelo intermedio y emite desde el modelo las dos formas de salida,
de manera que las dos digan lo mismo por construccion y no por cuidado.

  paper/PAPER.tex   fuente LaTeX, para compilar donde haya cadena de LaTeX
  paper/PAPER.pdf   PDF compuesto aqui, sin depender de una instalacion de LaTeX

COLOFON. Las dos salidas llevan el mismo colofon: el commit, la fecha, el sha256
del manuscrito del que salieron y el recuento de comprobaciones que estaban en
verde cuando se construyeron. El del PDF va ademas en el diccionario de
informacion del fichero, que es lo que lee el puente de src/pdf_bridge.py.

COMPROBACION DE EQUIVALENCIA. No basta con generar: hay que exigir que las tres
formas digan lo mismo. Se extraen del markdown las cifras, las claves de cita y
las filas de tabla, y se exige que aparezcan en el .tex y en el TEXTO REALMENTE
EXTRAIDO DEL PDF, no en el modelo con que se construyo, que seria circular. Para
que esa extraccion sea posible el PDF se escribe sin comprimir.

SOLO DESDE ARBOL LIMPIO. Este programa SE NIEGA a construir si el arbol de
trabajo tiene cambios sin commitear, y la razon es el colofon. El colofon dice de
que commit sale el PDF, y con el arbol sucio eso es mentira: sale de ese commit
mas lo que hubiera encima sin registrar, que nadie puede reconstruir despues. Un
PDF que dice venir de un commit tiene que venir de ese commit y de nada mas.

Es la misma disciplina que ya rige en el otro sentido para los comprobadores: un
verificador nunca escribe, y un constructor nunca construye desde un estado que
no se pueda nombrar.

  python src/build_paper.py
  python src/build_paper.py --sucio-a-proposito

La segunda forma existe para un caso concreto y declarado: tools/package.py
corre la cadena de analisis dentro de un clon antes de correr los
comprobadores, y esa cadena reescribe el reloj de pared de hall-search.tsv, de
modo que el clon queda sucio por una linea que ya esta declarada como no
determinista. Ahi lo que se comprueba es que el constructor corra, no que el PDF
sea de deposito, y el colofon lo dice: arbol_limpio queda en no.

Salidas: paper/PAPER.tex, paper/PAPER.pdf, results/build-paper.tsv
"""

import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "paper", "PAPER.md")
TEX = os.path.join(ROOT, "paper", "PAPER.tex")
PDF = os.path.join(ROOT, "paper", "PAPER.pdf")
OUT = os.path.join(ROOT, "results", "build-paper.tsv")

ROWS = []
FALLOS = []


def emit(k, v, n=""):
    ROWS.append((k, str(v), n))


def check(k, cond, n=""):
    emit(k, int(bool(cond)), n)
    if not cond:
        FALLOS.append(k + ("  " + n if n else ""))


# --- estado del repositorio, para el colofon --------------------------------

def git(*args):
    try:
        r = subprocess.run(["git", "-C", ROOT] + list(args),
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except Exception:
        return ""


def comprobaciones_en_verde():
    """Cuenta las comprobaciones que valen uno en los ficheros de comprobador.

    Es una cifra del colofon, y como toda cifra de este repositorio sale de un
    fichero y no de la memoria.
    """
    total = 0
    for nombre in ("assembly-check.tsv", "declared-values.tsv",
                   "mutation-test.tsv", "effort.tsv"):
        ruta = os.path.join(ROOT, "results", nombre)
        if not os.path.exists(ruta):
            continue
        for linea in open(ruta, encoding="utf-8"):
            if linea.startswith("#"):
                continue
            campos = linea.rstrip("\n").split("\t")
            if len(campos) >= 2 and campos[1] == "1":
                total += 1
    return total


def colofon(md_texto):
    return {
        "commit": git("rev-parse", "HEAD") or "sin commit",
        "fecha": git("log", "-1", "--format=%cd", "--date=short") or "sin fecha",
        "arbol_limpio": "si" if not git("status", "--porcelain") else "no",
        # el fin de linea se normaliza antes de resumir: lo que identifica al
        # manuscrito es su texto, no como lo haya dejado el sistema en disco
        "sha256_manuscrito": hashlib.sha256(
            md_texto.replace("\r\n", "\n").encode("utf-8")).hexdigest(),
        "comprobaciones_en_verde": str(comprobaciones_en_verde()),
    }


# --- parseo del markdown a un modelo ----------------------------------------

def parsear(texto):
    """Modelo intermedio: lista de bloques (tipo, contenido)."""
    # Los comentarios de ensamblaje son andamio: no son texto del articulo.
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    lineas = texto.split("\n")
    bloques = []
    i = 0
    while i < len(lineas):
        l = lineas[i]
        s = l.strip()

        if not s or s == "---":
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            bloques.append(("h%d" % len(m.group(1)), m.group(2).strip()))
            i += 1
            continue

        if s.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                celdas = [c.strip() for c in lineas[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in celdas):
                    filas.append(celdas)
                i += 1
            bloques.append(("tabla", filas))
            continue

        if s.startswith(">"):
            trozo = []
            while i < len(lineas) and lineas[i].strip().startswith(">"):
                trozo.append(lineas[i].strip().lstrip(">").strip())
                i += 1
            bloques.append(("cita", " ".join(trozo).strip()))
            continue

        # Una entrada de referencia empieza por "N. " y puede seguir en las
        # lineas de debajo, sangradas. Sin esta regla las trece entradas caian
        # en un unico parrafo corrido, que es como se compusieron hasta ahora.
        if re.match(r"^\d+\.\s", s):
            # Cada entrada es una lista de lineas: la cita y, debajo, su
            # Status. El Status se guarda aparte a proposito, porque es una
            # linea propia de la entrada y no una coletilla de la cita.
            entradas = []
            while i < len(lineas):
                l2 = lineas[i]
                s2 = l2.strip()
                if re.match(r"^\d+\.\s", s2):
                    entradas.append([s2])
                elif s2 and l2.startswith(" ") and entradas:
                    entradas[-1].append(s2)
                else:
                    break
                i += 1
            bloques.append(("referencias", entradas))
            continue

        if s.startswith("- "):
            trozo = []
            while i < len(lineas) and (lineas[i].strip().startswith("- ")
                                       or (lineas[i].strip()
                                           and not lineas[i].startswith(("#", "|", ">"))
                                           and trozo)):
                t = lineas[i].strip()
                if t.startswith("- "):
                    trozo.append(t[2:].strip())
                elif trozo:
                    trozo[-1] += " " + t
                i += 1
            bloques.append(("lista", trozo))
            continue

        trozo = []
        while i < len(lineas):
            t = lineas[i].strip()
            if not t or t == "---" or t.startswith(("#", "|", ">", "- ")):
                break
            trozo.append(t)
            i += 1
        bloques.append(("parrafo", " ".join(trozo)))
    return bloques


def separa_portada(bloques, titulo, autor, orcid):
    """Quita del cuerpo los bloques que son la portada.

    PAPER.md empieza con el titulo, el autor y el ORCID, y las dos salidas los
    componen por su cuenta, con maketitle en el .tex y con su equivalente en el
    PDF. Si no se quitan de aqui salen dos veces: una centrada arriba y otra
    como si fueran una seccion mas del texto. Se comprueba que lo que se quita
    es lo que se cree que se quita, para que este recorte no pueda tragarse una
    seccion de verdad.
    """
    esperado = [("h1", titulo), ("parrafo", "**%s**" % autor),
                ("parrafo", "ORCID %s" % orcid)]
    coincide = bloques[:len(esperado)] == esperado
    if not coincide:
        return False, bloques
    return True, bloques[len(esperado):]


# --- salida LaTeX ------------------------------------------------------------

ESCAPES = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
           "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
           "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def tex_escapa(s):
    return "".join(ESCAPES.get(c, c) for c in s)


# NOTACION. Los simbolos con subindice se componen en modo matematico y no como
# texto con un guion bajo escapado, que es lo que salia antes: B\_n en vez de
# B_n compuesto. El mapa se declara aqui entero, y el generador comprueba
# despues que no quede ni un guion bajo de texto en el .tex.
NOTACION = {
    "B_n": r"$B_n$", "B_3": r"$B_3$", "B_4": r"$B_4$", "B_5": r"$B_5$",
    "B_6": r"$B_6$", "F_2": r"$\mathbb{F}_2$",
    "pi_g": r"$\pi_g$", "c_i": r"$c_i$", "e_0": r"$e_0$", "e_1": r"$e_1$",
    "pi_1": r"$\pi_1$",
}
NOTACION_RE = re.compile(r"\b(?:%s)\b" % "|".join(
    sorted((re.escape(k) for k in NOTACION), key=len, reverse=True)))

# Un enlace no se escapa: va dentro de \url, que ademas le deja partir de linea
# y evita que se salga de la caja.
URL_RE = re.compile(r"https?://\S+")


def tex_llano(s):
    """Un trozo sin negrita ni cursiva: URLs, notacion y lo demas escapado."""
    salida = []
    for trozo in URL_RE.split(s):
        pass
    resto = []
    pos = 0
    for m in URL_RE.finditer(s):
        resto.append(("texto", s[pos:m.start()]))
        resto.append(("url", m.group(0)))
        pos = m.end()
    resto.append(("texto", s[pos:]))
    for clase, trozo in resto:
        if clase == "url":
            salida.append(r"\url{%s}" % trozo.rstrip(".,;"))
            salida.append(tex_escapa(trozo[len(trozo.rstrip(".,;")):]))
            continue
        pos2 = 0
        for m in NOTACION_RE.finditer(trozo):
            salida.append(tex_escapa(trozo[pos2:m.start()]))
            salida.append(NOTACION[m.group(0)])
            pos2 = m.end()
        salida.append(tex_escapa(trozo[pos2:]))
    return "".join(salida)


def tex_inline(s):
    """Negrita y cursiva a LaTeX, con el resto pasado por tex_llano.

    Se trocea primero por los marcadores y se trata cada trozo, para no escapar
    los propios comandos que se acaban de escribir.
    """
    partes = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", s)
    salida = []
    for p in partes:
        if p.startswith("**") and p.endswith("**") and len(p) > 4:
            salida.append(r"\textbf{%s}" % tex_llano(p[2:-2]))
        elif p.startswith("*") and p.endswith("*") and len(p) > 2:
            salida.append(r"\emph{%s}" % tex_llano(p[1:-1]))
        else:
            salida.append(tex_llano(p))
    return "".join(salida)


# El preambulo de la casa, el mismo que usa el otro articulo del autor. Se fija
# aqui entero y no por trozos para que se vea de un vistazo que carga y en que
# orden. hyperref va el ULTIMO a proposito: redefine comandos de otros paquetes
# y cargarlo antes rompe cosas en silencio. parskip NO se carga: el espaciado
# entre parrafos y entre secciones es el que produce este preambulo, que es
# sangria de primera linea y sin blanco entre parrafos.
PREAMBULO = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1in]{geometry}
\usepackage{microtype}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{longtable}
\setlength{\emergencystretch}{3em}

\title{%(titulo)s}
\author{%(autor)s\\ORCID %(orcid)s}
\date{}

\usepackage{hyperref}

\begin{document}
\maketitle
"""


def a_tex(bloques, colo, titulo, autor, orcid):
    salida = [PREAMBULO % {"titulo": tex_escapa(titulo),
                           "autor": tex_escapa(autor),
                           "orcid": tex_escapa(orcid)}]
    en_refs = False
    for tipo, cont in bloques:
        if tipo == "h1":
            if cont.strip().lower() == "abstract":
                salida.append(r"\begin{abstract}")
                salida.append("EMPIEZA-RESUMEN")
                continue
            en_refs = cont.strip().lower() == "references"
            salida.append(r"\section*{%s}" % tex_inline(cont))
        elif tipo == "h2":
            salida.append(r"\subsection*{%s}" % tex_inline(cont))
        elif tipo == "h3":
            salida.append(r"\subsubsection*{%s}" % tex_inline(cont))
        elif tipo == "parrafo":
            salida.append(tex_inline(cont))
        elif tipo == "cita":
            salida.append(r"\begin{quote}" + "\n" + tex_inline(cont)
                          + "\n" + r"\end{quote}")
        elif tipo == "lista":
            salida.append(r"\begin{itemize}")
            for it in cont:
                salida.append(r"\item " + tex_inline(it))
            salida.append(r"\end{itemize}")
        elif tipo == "referencias":
            # Sangria francesa: la primera linea al margen y las siguientes
            # metidas, que es como APA quiere una lista de referencias y como
            # se distingue una entrada de la siguiente de un vistazo.
            salida.append(r"\begingroup")
            salida.append(r"\setlength{\parindent}{0pt}")
            for lineas_it in cont:
                cuerpo_it = tex_inline(lineas_it[0])
                for extra in lineas_it[1:]:
                    cuerpo_it += r"\\ " + tex_inline(extra)
                salida.append(r"\hangindent=1.6em\hangafter=1 "
                              + cuerpo_it + r"\par\vspace{0.5ex}")
            salida.append(r"\endgroup")
        elif tipo == "tabla":
            if not cont:
                continue
            ncol = max(len(f) for f in cont)
            salida.append(r"\begin{center}\small")
            salida.append(r"\begin{longtable}{%s}" % ("l" * ncol))
            for j, fila in enumerate(cont):
                fila = fila + [""] * (ncol - len(fila))
                if j == 0:
                    # La cabecera va en negrita, y la pone el generador. Asi la
                    # negrita es una decision de formato en un sitio y no un
                    # asterisco repetido en cada celda del markdown.
                    celdas = [r"\textbf{%s}" % tex_escapa(c) for c in fila]
                else:
                    celdas = [tex_inline(c) for c in fila]
                salida.append(" & ".join(celdas) + r" \\")
                if j == 0:
                    salida.append(r"\hline")
            salida.append(r"\end{longtable}")
            salida.append(r"\end{center}")
        salida.append("")

    texto = "\n".join(salida)
    # el resumen se cierra donde empieza la primera seccion numerada
    texto = texto.replace("EMPIEZA-RESUMEN\n", "")
    texto = texto.replace(r"\section*{1. Introduction}",
                          "\\end{abstract}\n\n\\section*{1. Introduction}", 1)

    texto += ("\n" + r"\vfill" + "\n" + r"\begin{small}" + "\n"
              + r"\noindent\textbf{Colophon.}" + "\n"
              + "Built from the assembled manuscript at commit "
              + tex_escapa(colo["commit"]) + ", dated "
              + tex_escapa(colo["fecha"]) + ". Working tree clean: "
              + tex_escapa(colo["arbol_limpio"]) + ". sha256 of the manuscript: "
              + tex_escapa(colo["sha256_manuscrito"]) + ". Checks green at build "
              + "time: " + tex_escapa(colo["comprobaciones_en_verde"]) + ".\n"
              + r"\end{small}" + "\n" + r"\end{document}" + "\n")
    return texto


# --- salida PDF --------------------------------------------------------------

def a_pdf(bloques, colo, titulo, autor, orcid):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle)

    ss = getSampleStyleSheet()
    cuerpo = ParagraphStyle("cuerpo", parent=ss["BodyText"], fontSize=9.5,
                            leading=13, spaceAfter=6, alignment=4)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=14, spaceBefore=14)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11.5, spaceBefore=10)
    h3 = ParagraphStyle("h3", parent=ss["Heading3"], fontSize=10.5, spaceBefore=8)
    cita = ParagraphStyle("cita", parent=cuerpo, leftIndent=18, rightIndent=12,
                          spaceBefore=4, spaceAfter=8)
    peq = ParagraphStyle("peq", parent=cuerpo, fontSize=7.6, leading=10)
    # sangria francesa para las referencias, la misma que el .tex
    colgante = ParagraphStyle("colgante", parent=cuerpo, leftIndent=18,
                              firstLineIndent=-18, spaceAfter=4)

    def inline(s):
        s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        # El equivalente del modo matematico aqui es el subindice de verdad.
        s = NOTACION_RE.sub(
            lambda m: "%s<sub>%s</sub>" % tuple(m.group(0).split("_", 1)), s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)
        return s

    # La portada, centrada y una sola vez, como la que compone maketitle.
    centrado = ParagraphStyle("centrado", parent=cuerpo, alignment=1,
                              spaceAfter=2)
    hist = [Paragraph(inline(titulo), ss["Title"]),
            Paragraph("<b>%s</b>" % inline(autor), centrado),
            Paragraph("ORCID %s" % orcid, centrado),
            Spacer(1, 0.8 * cm)]

    for tipo, cont in bloques:
        if tipo == "h1":
            hist.append(Paragraph(inline(cont), h1))
        elif tipo == "h2":
            hist.append(Paragraph(inline(cont), h2))
        elif tipo == "h3":
            hist.append(Paragraph(inline(cont), h3))
        elif tipo == "parrafo":
            hist.append(Paragraph(inline(cont), cuerpo))
        elif tipo == "cita":
            hist.append(Paragraph(inline(cont), cita))
        elif tipo == "lista":
            for it in cont:
                hist.append(Paragraph("&bull; " + inline(it), cita))
        elif tipo == "referencias":
            for lineas_it in cont:
                hist.append(Paragraph("<br/>".join(inline(x) for x in lineas_it),
                                      colgante))
        elif tipo == "tabla":
            if not cont:
                continue
            ncol = max(len(f) for f in cont)
            filas_txt = [f + [""] * (ncol - len(f)) for f in cont]
            datos = [[Paragraph(inline(c), peq) for c in f] for f in filas_txt]
            # ANCHOS CALCULADOS, para que ninguna tabla se salga de la caja. Se
            # reparte el ancho disponible en proporcion a lo que ocupa la
            # columna mas larga de cada una, con un minimo por columna para que
            # una columna estrecha no quede en un hilo.
            disponible = A4[0] - 2 * 2.54 * cm
            anchos = [max(len(f[j]) for f in filas_txt) for j in range(ncol)]
            anchos = [max(a, 3) for a in anchos]
            escala = disponible / float(sum(anchos))
            col = [a * escala for a in anchos]
            tb = Table(datos, colWidths=col, repeatRows=1, hAlign="CENTER")
            tb.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]))
            hist.append(tb)
            hist.append(Spacer(1, 0.3 * cm))

    hist.append(Spacer(1, 0.6 * cm))
    hist.append(Paragraph(
        "<b>Colophon.</b> Built from the assembled manuscript at commit %s, "
        "dated %s. Working tree clean: %s. sha256 of the manuscript: %s. "
        "Checks green at build time: %s."
        % (colo["commit"], colo["fecha"], colo["arbol_limpio"],
           colo["sha256_manuscrito"], colo["comprobaciones_en_verde"]), peq))

    doc = SimpleDocTemplate(
        # Una pulgada por los cuatro lados, el mismo margen que geometry pone
        # en el .tex, para que las dos salidas no difieran ni en eso.
        PDF, pagesize=A4, leftMargin=2.54 * cm, rightMargin=2.54 * cm,
        topMargin=2.54 * cm, bottomMargin=2.54 * cm,
        title=titulo, author=autor,
        subject="colofon: commit=%s fecha=%s sha256=%s comprobaciones=%s "
                "arbol_limpio=%s" % (colo["commit"], colo["fecha"],
                                     colo["sha256_manuscrito"],
                                     colo["comprobaciones_en_verde"],
                                     colo["arbol_limpio"]),
        keywords="forced-counts colofon %s" % colo["sha256_manuscrito"],
        pageCompression=0)
    doc.build(hist)


# --- extraccion del texto del PDF, para el cotejo ----------------------------

def texto_del_pdf(ruta):
    """Saca el texto del PDF de sus propios flujos, sin comprimir.

    No se coteja el modelo con que se construyo el PDF, que seria darse la razon
    a uno mismo: se coteja lo que el fichero lleva dentro.
    """
    datos = open(ruta, "rb").read()
    trozos = []
    for m in re.finditer(rb"\((?:\\.|[^\\()])*\)", datos):
        s = m.group(0)[1:-1]
        s = re.sub(rb"\\([()\\])", rb"\1", s)
        # Los caracteres no ASCII viajan en el PDF como escapes
        # octales, y sin descodificarlos el cotejo no veria una
        # tilde ni una dieresis: creeria que falta lo que si esta.
        s = re.sub(rb"\\([0-7]{1,3})",
                   lambda mm: bytes([int(mm.group(1), 8) & 0xFF]), s)
        try:
            trozos.append(s.decode("latin-1"))
        except Exception:
            pass
    return " ".join(trozos)


# --- cotejo de equivalencia --------------------------------------------------

CIFRA = re.compile(r"(?<![\w.,:/-])\d+(?:\.\d+)?(?![\w:/-])(?!\.\d)")
CITA = re.compile(r"\[(\d{1,2})\]")


def cotejar(md, tex, pdf_txt, bloques):
    sin_com = re.sub(r"<!--.*?-->", "", md, flags=re.S)

    cifras = sorted(set(CIFRA.findall(sin_com)))
    citas = sorted(set(CITA.findall(sin_com)))
    filas = [f for tipo, cont in bloques if tipo == "tabla" for f in cont]
    # Los asteriscos de la negrita son marcado del markdown, no contenido: en el
    # .tex son \textbf y en el PDF son otra fuente, asi que se comparan sin
    # ellos. Lo que tiene que coincidir es la celda, no como se enfatiza.
    celdas = sorted({c.replace("*", "").strip() for f in filas for c in f
                     if c.replace("*", "").strip() not in (".", "")})

    emit("cifras.distintas.en.el.manuscrito", len(cifras))
    emit("citas.distintas.en.el.manuscrito", len(citas))
    emit("filas.de.tabla", len(filas))
    emit("celdas.distintas.de.tabla", len(celdas))
    check("hay.algo.que.cotejar", cifras and citas and filas,
          "un cotejo sobre nada pasaria en vacio")

    def falta(donde, texto, items, etiqueta):
        ausentes = [x for x in items if x not in texto]
        emit("%s.%s.ausentes" % (donde, etiqueta),
             " ".join(ausentes) if ausentes else "ninguno")
        check("%s.lleva.todas.las.%s" % (donde, etiqueta), not ausentes)

    falta("tex", tex, cifras, "cifras")
    falta("tex", tex, citas, "citas")
    falta("tex", tex, celdas, "celdas")

    # el PDF parte las palabras entre operadores de texto, asi que se compara
    # sobre una version sin espacios: lo que se exige es que la cadena este,
    # no que este con el mismo espaciado
    pdf_plano = re.sub(r"\s+", "", pdf_txt)
    falta("pdf", pdf_plano, [re.sub(r"\s+", "", c) for c in cifras], "cifras")
    falta("pdf", pdf_plano, ["[%s]" % c for c in citas], "citas")
    falta("pdf", pdf_plano, [re.sub(r"\s+", "", c) for c in celdas], "celdas")


# --- barrido de guiones sobre el .tex ----------------------------------------

LARGOS = "[\u2010-\u2015\u2212\ufe58\ufe63\uff0d]"

# Usos convencionales de LaTeX en los que un guion no es un guion largo del
# texto. Se listan aqui uno por uno y el informe dice cuantas veces aplico cada
# uno, para que ninguna exencion quede sin nombre.
EXENTOS_TEX = [
    ("raya.corta.de.rango.de.pagina",
     "\\d+\u2013\\d+",
     "raya corta entre dos numeros de pagina: es el uso convencional de APA "
     "para un rango, y es la unica raya que este repositorio admite"),
    ("regla.de.comentario", r"^%+[-\s]*$",
     "linea de comentario hecha de guiones para separar bloques de fuente"),
    ("opcion.de.paquete", r"\[[^\]]*\]\{[^}]*\}",
     "opciones de paquete y de clase, donde el guion es parte del nombre"),
    ("guion.de.palabra", r"(?<=[A-Za-z])-(?=[A-Za-z])",
     "guion dentro de una palabra compuesta, que no es raya"),
    ("signo.menos", r"(?<=[\d(])-(?=[\d\w])",
     "signo menos en una expresion"),
]


def barrer_tex(tex):
    # Primero se retiran los usos exentos, cada uno contado y con su motivo, y
    # solo despues se cuenta lo que queda. Antes el barrido de unicode iba antes
    # que las exenciones, y por eso no habia manera de admitir la raya corta de
    # un rango de paginas sin admitirla en todas partes.
    limpio = tex
    for nombre, patron, motivo in EXENTOS_TEX:
        def _tapa(m):
            return re.sub(LARGOS, "#", m.group(0)).replace("-", "#")
        limpio, k = re.subn(patron, _tapa, limpio, flags=re.M)
        emit("tex.exentos.%s" % nombre, k, motivo)

    largos = len(re.findall(LARGOS, limpio))
    emit("tex.guiones.largos.unicode", largos,
         "fuera de los usos exentos de arriba")
    check("tex.cero.guiones.largos.unicode", largos == 0)

    # lo que quede: rachas de dos o mas guiones, que LaTeX compone como raya
    rachas = re.findall(r"-{2,}", limpio)
    emit("tex.rachas.de.guion.que.LaTeX.compondria.como.raya", len(rachas))
    check("tex.ninguna.raya.compuesta", not rachas,
          "la regla de la casa prohibe la raya tambien en ingles, y en LaTeX "
          "una raya se escribe con dos o tres guiones seguidos")


# --- principal ---------------------------------------------------------------

def main():
    sucio = git("status", "--porcelain")
    if sucio and "--sucio-a-proposito" not in sys.argv:
        print("ARBOL SUCIO: no se construye.")
        print("El colofon tendria que decir de que commit sale este PDF, y con")
        print("cambios sin commitear eso no se puede decir. Commitea primero, o")
        print("pasa --sucio-a-proposito si sabes por que lo haces.")
        print("")
        for l in sucio.split("\n")[:12]:
            print("  " + l)
        return 1

    md = open(MD, encoding="utf-8").read()
    bloques = parsear(md)

    titulo = "Forced counts: when a symmetry group determines the discordance of a constructed ordering"
    autor = "Alexis García Hurtado"
    orcid = "0009-0003-4636-8206"
    check("el.titulo.del.manuscrito.es.el.congelado", bloques[0] == ("h1", titulo),
          "la portada de PAPER.md manda")
    portada_ok, cuerpo_bloques = separa_portada(bloques, titulo, autor, orcid)
    check("la.portada.se.separa.del.cuerpo", portada_ok,
          "los tres bloques de portada son los esperados y salen del cuerpo "
          "para no componerse dos veces")
    emit("bloques.de.portada.retirados", len(bloques) - len(cuerpo_bloques))

    colo = colofon(md)
    for k, v in sorted(colo.items()):
        emit("colofon." + k, v)

    tex = a_tex(cuerpo_bloques, colo, titulo, autor, orcid)
    open(TEX, "w", encoding="utf-8", newline="\n").write(tex)
    emit("tex.bytes", len(tex.encode("utf-8")))

    a_pdf(cuerpo_bloques, colo, titulo, autor, orcid)
    emit("pdf.bytes", os.path.getsize(PDF))
    pdf_txt = texto_del_pdf(PDF)
    emit("pdf.caracteres.extraidos", len(pdf_txt))
    check("el.pdf.se.deja.leer", len(pdf_txt) > 10000,
          "si no se puede extraer texto, no hay cotejo posible")

    cotejar(md, tex, pdf_txt, cuerpo_bloques)
    barrer_tex(tex)

    # DIACRITICOS. Si un acento se pierde por el camino, se pierde en silencio:
    # el fichero sigue abriendo y el nombre sigue pareciendose. Se exige que
    # esten en las dos salidas, y en el PDF sobre el texto extraido de sus
    # propios flujos, que es donde se veria la perdida.
    ACENTOS = ["García Hurtado", "Björner", "Mütze",
               "Schöter"]
    faltan_tex = [w for w in ACENTOS if w not in tex]
    faltan_pdf = [w for w in ACENTOS if w not in pdf_txt]
    emit("acentos.comprobados", len(ACENTOS), " ".join(ACENTOS))
    emit("acentos.ausentes.en.el.tex",
         " ".join(faltan_tex) if faltan_tex else "ninguno")
    emit("acentos.ausentes.en.el.pdf",
         " ".join(faltan_pdf) if faltan_pdf else "ninguno")
    check("los.diacriticos.se.componen.en.las.dos.salidas",
          not faltan_tex and not faltan_pdf)

    # NOTACION. Un guion bajo escapado en el .tex es notacion compuesta como
    # texto, que es justo lo que no se quiere. Se cuenta y se exige cero.
    bajos = tex.count(r"\_")
    emit("tex.guiones.bajos.compuestos.como.texto", bajos,
         "cada uno seria un subindice compuesto en redonda en vez de en modo "
         "matematico")
    check("tex.cero.notacion.compuesta.como.texto", bajos == 0)
    emit("tex.simbolos.en.modo.matematico",
         sum(tex.count(v) for v in set(NOTACION.values())), "")
    emit("tex.enlaces.en.url", tex.count(r"\url{"), "")
    check("todo.enlace.va.en.url", tex.count(r"\url{") >= 3,
          "las tres entradas con enlace tienen que llevarlo dentro de url")

    # que el colofon este de verdad en las dos salidas
    check("el.tex.lleva.colofon", colo["sha256_manuscrito"] in tex)
    check("el.pdf.lleva.colofon.en.su.informacion",
          colo["sha256_manuscrito"] in open(PDF, "rb").read().decode("latin-1"))

    emit("bloques.parseados", len(bloques))
    emit("desajustes", len(FALLOS))
    check("la.construccion.pasa", not FALLOS)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Construccion de PAPER.tex y PAPER.pdf desde PAPER.md.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))

    for k, v, _ in ROWS:
        print("  %-52s %s" % (k, v))
    if FALLOS:
        print("\nDESAJUSTES:")
        for f in FALLOS:
            print("  " + f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
