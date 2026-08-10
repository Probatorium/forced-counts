#!/usr/bin/env python3
"""
Ensamblador y comprobador del manuscrito.

Junta portada, resumen, las nueve secciones y las referencias en un solo fichero,
y comprueba lo que hay que comprobar antes de creerselo:

  - que esten las nueve secciones, en orden y sin duplicados;
  - que toda cita del texto resuelva a una entrada de las referencias;
  - que no haya guiones largos en ninguna forma, tambien en ingles;
  - que ninguna seccion haya perdido sus comentarios de ensamblaje;
  - y, llamando a src/declared_values.py, que toda cifra impresa en la prosa
    siga saliendo de la linea de results que su comentario declara.

Herencia de verificaciones, por la enmienda 3 de CONTACT-RULES.md: el barrido de
guiones es el mismo que se viene aplicando a cada seccion por separado, y aqui se
aplica al ensamblado entero.

Salida: paper/PAPER.md y results/assembly-check.tsv

  python src/assemble_paper.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")
OUT = os.path.join(PAPER, "PAPER.md")
CHECK = os.path.join(ROOT, "results", "assembly-check.tsv")

ROWS = []
# La clase se escribe con escapes para que este fichero no contenga el mismo
# caracter que persigue y no se delate a si mismo en el barrido.
DASHES = "[\u2010-\u2015\u2212\ufe58\ufe63\uff0d]"

# Usos en los que una raya no es una raya del texto. Hoy hay uno solo, y entra
# porque el estilo de la casa paso a APA 7: los rangos de pagina se escriben con
# raya corta entre los dos numeros. Fuera de esto la prohibicion sigue entera,
# tambien en ingles.
EXENTOS = [
    ("raya.corta.de.rango.de.pagina",
     "\\d+\u2013\\d+",
     "rango de paginas en una referencia APA, unico uso admitido"),
]

SECCIONES = [
    ("01-introduction.md", "1", "Introduction"),
    ("02-preliminaries.md", "2", "Preliminaries"),
    ("03-orbit-accounting.md", "3", "The orbit accounting"),
    ("04-parity-obstruction.md", "4", "The parity obstruction"),
    ("05-characterisation.md", "5", "The characterisation"),
    ("06-three-historical-orderings.md", "6", "The three historical orderings"),
    ("07-landscape.md", "7", "The landscape B(n,k)"),
    ("08-open-problems.md", "8", "Open problems"),
    ("09-verification.md", "9", "Methods of verification"),
]

# LAS REFERENCIAS, en estilo APA 7 y en orden alfabetico de primer autor.
#
# Cada entrada es (clave_alfa, orden, apa, estatus):
#
#   clave_alfa  el identificador interno estable con el que se escribieron las
#               citas antes de numerarlas. Se conserva porque es lo que permite
#               a tools/renumber_citations.py renumerar sin tocar nada a mano.
#   orden       la cadena por la que se alfabetiza, con los diacriticos ya
#               plegados, porque en APA la dieresis no altera el orden: Mütze se
#               alfabetiza como Mutze, y por eso Moore va antes.
#   apa         la entrada, con los DIACRITICOS correctos y los rangos de pagina
#               con raya corta, que es el uso convencional de APA.
#   estatus     la marca de leido o de segunda mano que fijo la revision. NO es
#               una nota al pie: es parte de la referencia y se imprime como
#               segunda linea de la entrada.
#
# LO QUE NO SE INVENTA. APA pide ano, editorial y volumen. Donde la revision no
# los verifico contra el artefacto leido, NO se ponen, y el estatus dice cual
# falta. Este repositorio prefiere un hueco declarado a una ficha completa a
# base de memoria.
REFERENCIAS = [
    ("BB", "Bjorner",
     "Björner, A., & Brenti, F. *Combinatorics of Coxeter groups*. "
     "Equation (1.25) and Proposition 1.5.2, p. 20; Sections 8.1 and 8.2, "
     "pp. 245, 252.",
     "read, and the cited pages verified against the PDF; year and publisher "
     "were not verified against the artefact and are therefore not printed"),

    ("Co", "Cook",
     "Cook, R. S. (2006). *Classical Chinese combinatorics: Derivation of the "
     "Book of Changes hexagram sequence* (STEDT Monograph Series, Vol. 5). "
     "University of California, Berkeley. ISBN 0-944613-44-6.",
     "read through its review in full, plus full text sweeps of the converted "
     "text; the book itself was not read cover to cover"),

    ("Dr", "Drasny",
     "Drasny, J. *The solution of the King Wen sequence?* [Review of the book "
     "*Classical Chinese combinatorics*, by R. S. Cook]. Yijing Dao. "
     "http://www.biroco.com/yijing/cook.htm",
     "read in full; the review carries no date on the page read, so none is "
     "printed"),

    ("Gr", "Gritter",
     "Gritter, G. (2015). *The hidden pattern in the classical sequence of the "
     "I Ching*. Groningen.",
     "read in full"),

    ("HM", "Hacker",
     "Hacker, E., & Moore, S. (2003). A brief note on the two-part division of "
     "the received order of the hexagrams in the Zhouyi. *Journal of Chinese "
     "Philosophy*, *30*(2), 219–221.",
     "SECOND HAND: bibliographic identity taken from the bibliography of "
     "reference 6; not read"),

    ("Mo", "Moore",
     "Moore, S. (2005). *Structural elements in the King Wen sequence of "
     "hexagrams* (Oracle Paper No. 1).",
     "read; the quoted passage taken verbatim from the rendered PDF page, "
     "p. 6, and not from the OCR conversion"),

    ("Mu", "Mutze",
     "Mütze, T. (2023). Combinatorial Gray codes: An updated survey. *The "
     "Electronic Journal of Combinatorics*, *30*(3), Dynamic Survey DS26.",
     "read in the cited part, Section 3.2 on p. 11, verified against the PDF"),

    ("PR", "Propp",
     "Propp, J., & Roby, T. (2015). *Homomesy in products of two chains* "
     "(Version 6) [Preprint]. arXiv. https://arxiv.org/abs/1310.5201v6",
     "read, and Section 2.1 on p. 4 verified against the PDF; its journal "
     "identity is second hand, since the artefact read is the arXiv version"),

    ("Ra", "Radisic",
     "Radisic, A. *Optimal equivariant matchings on the 6-cube: With an "
     "application to the King Wen sequence* (Version 3) [Preprint]. arXiv. "
     "https://arxiv.org/abs/2601.07175v3",
     "read in full, eleven pages; its Appendix A was transcribed and collated "
     "against our data, all sixty four positions agreeing"),

    ("RSW", "Reiner",
     "Reiner, V., Stanton, D., & White, D. (2004). The cyclic sieving "
     "phenomenon. *Journal of Combinatorial Theory, Series A*, *108*(1), "
     "17–50. https://doi.org/10.1016/j.jcta.2004.04.009",
     "read in identity and definition; cited for context, since it counts "
     "fixed points and not orbit averages"),

    ("Ro", "Roby",
     "Roby, T. *Dynamical algebraic combinatorics and the homomesy "
     "phenomenon*. Example 1, p. 3; Section 2.1 and Example 4, p. 4.",
     "read, and the cited pages verified against the PDF; its volume identity "
     "is second hand, since the cover of the PDF read does not carry it, and "
     "no year is printed here for the same reason"),

    ("Sc", "Schoter",
     "Schöter, A. (1998). Boolean algebra and the Yi Jing. *The Oracle: The "
     "Journal of Yijing Studies*, *2*(7), 19–34. ISSN 1463-6220.",
     "read; Definition 6, Sequence Parameters"),

    ("NL", "Uninformative",
     "*Uninformative rungs: An order-theoretic stopping criterion for nested "
     "reference sets*. https://doi.org/10.5281/zenodo.21750029",
     "SECOND HAND: cited as a pointer to the framework that would govern the "
     "inferential question of Section 8.3; not read in the course of this "
     "work"),
]

REFERENCIAS.sort(key=lambda r: r[1])

# La clave publica es el numero, en el orden alfabetico de arriba. La clave
# alfabetica sobrevive solo como identificador interno para la renumeracion.
NUMERO = {r[0]: str(n) for n, r in enumerate(REFERENCIAS, start=1)}

CLAVES = set(NUMERO.values())


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def check(key, cond, note=""):
    emit(key, int(bool(cond)), note)
    assert cond, "fallo el comprobador de ensamblado: " + key


def main():
    partes = []

    # --- portada ---------------------------------------------------------
    portada = """# Forced counts: when a symmetry group determines the discordance of a constructed ordering

**Alexis Garcia Hurtado**

ORCID 0009-0003-4636-8206

<!-- El titulo quedo congelado el 10 de agosto de 2026 tras pasar su puerta de
     termino; el registro de esa puerta esta en TITLE.md. -->
"""
    partes.append(portada)

    # --- resumen ---------------------------------------------------------
    resumen = open(os.path.join(PAPER, "00-abstract.md"), encoding="utf-8").read()
    partes.append(resumen.rstrip() + "\n")

    # --- secciones -------------------------------------------------------
    vistas = []
    for fichero, numero, titulo in SECCIONES:
        ruta = os.path.join(PAPER, fichero)
        check("existe.%s" % fichero, os.path.exists(ruta))
        t = open(ruta, encoding="utf-8").read()
        cabecera = re.match(r"#\s*(\d+)\.\s*(.+)", t.strip())
        check("cabecera.%s" % fichero, cabecera is not None)
        check("numero.correcto.%s" % fichero, cabecera.group(1) == numero,
              "la cabecera del fichero dice el numero que le toca")
        check("comentarios.de.ensamblaje.%s" % fichero, "<!--" in t,
              "la seccion conserva sus comentarios de origen")
        vistas.append(cabecera.group(1))
        partes.append("\n---\n\n" + t.rstrip() + "\n")

    check("las.nueve.secciones.en.orden", vistas == [n for _, n, _ in SECCIONES])
    check("sin.duplicados", len(set(vistas)) == len(vistas))
    emit("secciones.ensambladas", len(vistas), "")

    # --- referencias ------------------------------------------------------
    ref = ["\n---\n\n# References\n",
           "Each entry records the identity as the literature review fixed it, and "
           "whether the artefact was read here or enters as second hand. That mark "
           "is part of the reference.\n"]
    for n, (clave, _orden, cita, estatus) in enumerate(REFERENCIAS, start=1):
        ref.append("%d. %s  \n   *Status:* %s." % (n, cita, estatus))
    partes.append("\n".join(ref) + "\n")
    emit("referencias", len(REFERENCIAS), "")
    emit("referencias.de.segunda.mano",
         sum(1 for _, _, _, e in REFERENCIAS if e.startswith("SECOND HAND")), "")

    texto = "\n".join(partes)

    # --- comprobaciones sobre el ensamblado -------------------------------
    # USOS EXENTOS, listados con su motivo y contados, porque una exencion sin
    # nombre es una manera elegante de que el barrido no encuentre nada.
    limpio = texto
    for nombre, patron, motivo in EXENTOS:
        limpio, k = re.subn(patron, lambda m: re.sub(DASHES, "#", m.group(0)),
                            limpio, flags=re.M)
        emit("exentos.%s" % nombre, k, motivo)
    guiones = len(re.findall(DASHES, limpio))
    emit("guiones.largos.en.el.ensamblado", guiones,
         "en cualquiera de sus formas, fuera de los usos exentos")
    check("cero.guiones.largos", guiones == 0)

    # toda cita del texto resuelve a una referencia
    cuerpo = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    cuerpo = cuerpo.split("# References")[0]
    citas = set(re.findall(r"\[(\d{1,2})\]", cuerpo))
    huerfanas = sorted(c for c in citas if c not in CLAVES)
    emit("citas.distintas.en.el.texto", len(citas), "")
    emit("citas.sin.referencia", " ".join(huerfanas) if huerfanas else "ninguna", "")
    check("toda.cita.resuelve", not huerfanas)
    # La comprobacion anterior pasa en vacio si el texto no tiene ninguna clave,
    # asi que se exige que haya citas y que ninguna referencia quede sin citar.
    check("el.texto.tiene.citas", len(citas) > 0,
          "una comprobacion que pasa en vacio no comprueba nada")
    sin_citar = sorted(CLAVES - citas)
    emit("referencias.sin.citar", " ".join(sin_citar) if sin_citar else "ninguna", "")
    check("ninguna.referencia.queda.sin.citar", not sin_citar)

    # --- el congelador de cifras, dentro del mismo ensamblado -------------
    # No basta con que el manuscrito este bien montado: hay que exigir que las
    # cifras que imprime sigan siendo las que miden los ficheros de results. Se
    # corre aqui, y su resultado entra en este mismo informe, para que no exista
    # un ensamblado que pase mientras el congelador falla.
    import declared_values
    salida = declared_values.comprobar()
    for k, v, n in declared_values.ROWS:
        if k.startswith(("declaraciones.", "cifras.", "derivadas.",
                         "el.cotejo.", "desajustes", "toda.cifra.")):
            emit("cifras." + k, v, n)
    for f in declared_values.FALLOS:
        emit("cifras.DESAJUSTE", 1, f)
    check("las.cifras.impresas.siguen.saliendo.de.results", salida == 0)

    # --- las tablas, numeradas y referenciadas -----------------------------
    # Una tabla que el texto no menciona es una tabla que el lector se encuentra
    # sin saber que hace ahi. Se exige rotulo para cada una y mencion para cada
    # rotulo, y las dos direcciones se cuentan.
    sin_com = re.sub(r"<!--.*?-->", " ", texto, flags=re.S)
    bloques_tabla = len(re.findall(r"(?:\A|\n)(?:[^|\n].*\n|\n)\|",
                                   "\n" + sin_com))
    rotulos = [int(n) for n in re.findall(r"\*\*Table (\d+)\.\*\*", sin_com)]
    emit("tablas.en.el.manuscrito", bloques_tabla, "")
    emit("tablas.con.rotulo", len(rotulos), "")
    check("toda.tabla.lleva.rotulo", bloques_tabla == len(rotulos),
          "hay %d tablas y %d rotulos" % (bloques_tabla, len(rotulos)))
    check("los.rotulos.van.de.uno.en.uno",
          rotulos == list(range(1, len(rotulos) + 1)),
          "numeracion esperada 1..n en orden de aparicion, encontrada %r"
          % (rotulos,))

    sin_rotulos = re.sub(r"\*\*Table \d+\.\*\*", " ", sin_com)
    huerfanas_t = [n for n in rotulos
                   if not re.search(r"\bTable %d\b" % n, sin_rotulos)]
    emit("tablas.sin.referencia.en.la.prosa",
         " ".join(str(n) for n in huerfanas_t) if huerfanas_t else "ninguna", "")
    check("toda.tabla.numerada.se.referencia.en.el.texto", not huerfanas_t,
          "una tabla que el texto no menciona no tiene por que estar")

    emit("palabras.aproximadas", len(texto.split()), "")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)
    os.makedirs(os.path.dirname(CHECK), exist_ok=True)
    with open(CHECK, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Comprobador de ensamblado del manuscrito.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in ROWS:
            fh.write("%s\t%s\t%s\n" % (k, v, n))

    print("escrito paper/PAPER.md y results/assembly-check.tsv")
    for k, v, _ in ROWS:
        if not k.startswith(("existe.", "cabecera.", "numero.", "comentarios.")):
            print("  %-44s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
