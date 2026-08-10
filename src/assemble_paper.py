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

# Las referencias, con la identidad TAL COMO LA FIJO LA REVISION. Cada una dice
# si se leyo aqui o si entra como segunda mano, y esa marca es parte de la
# referencia, no una nota al pie.
REFERENCIAS = [
    ("BB", "Anders Bjorner and Francesco Brenti, *Combinatorics of Coxeter Groups*. "
           "Equation (1.25) and Proposition 1.5.2 on printed page 20; Sections 8.1 "
           "and 8.2 on printed pages 245 and 252.",
     "read, and the cited pages verified against the PDF"),
    ("PR", "James Propp and Tom Roby, *Homomesy in products of two chains*, "
           "arXiv:1310.5201v6 [math.CO], 19 June 2015. Definition 1 on page 1 and "
           "Section 2.1 on page 4.",
     "read, and Section 2.1 verified against the PDF; its journal identity is "
     "second hand, since the artefact read is the arXiv version"),
    ("Ro", "Tom Roby, *Dynamical Algebraic Combinatorics and the Homomesy "
           "Phenomenon*. Example 1 on page 3, Section 2.1 and Example 4 on page 4.",
     "read, and the cited pages verified against the PDF; its volume identity is "
     "second hand"),
    ("RSW", "V. Reiner, D. Stanton and D. White, *The cyclic sieving phenomenon*, "
            "Journal of Combinatorial Theory, Series A 108 (2004) 17 to 50, "
            "doi 10.1016/j.jcta.2004.04.009.",
     "read in identity and definition; cited for context, since it counts fixed "
     "points and not orbit averages"),
    ("Ra", "Alejandro Radisic, *Optimal Equivariant Matchings on the 6-Cube: With "
           "an Application to the King Wen Sequence*, arXiv:2601.07175v3 "
           "[math.GM]. Theorem 3.3, and the full binary table in Appendix A.",
     "read in full, eleven pages; its Appendix A was transcribed and collated "
     "against our data, all sixty four positions agreeing"),
    ("Mu", "Torsten Mutze, *Combinatorial Gray codes, an updated survey*, The "
           "Electronic Journal of Combinatorics 30(3) (2023), Dynamic Survey "
           "#DS26. Section 3.2 on printed page 11.",
     "read in the cited part, verified against the PDF"),
    ("Sc", "Andreas Schoter, *Boolean Algebra and the Yi Jing*, The Oracle: The "
           "Journal of Yijing Studies, Vol 2, No 7, Summer 1998, pages 19 to 34, "
           "ISSN 1463-6220. Definition 6, Sequence Parameters.",
     "read"),
    ("Mo", "Steve Moore, *Structural Elements in the King Wen Sequence of "
           "Hexagrams*, Oracle Paper No. 1, February 2005. Quoted passage on "
           "printed page 6.",
     "read; the quoted passage taken verbatim from the rendered PDF page, not "
     "from the OCR conversion"),
    ("Gr", "Gert Gritter, *The Hidden Pattern in the classical sequence of the I "
           "Ching*, Groningen, 2015.",
     "read in full"),
    ("Co", "Richard S. Cook, *Classical Chinese Combinatorics: Derivation of the "
           "Book of Changes Hexagram Sequence*, STEDT Monograph Series, Vol. 5, "
           "University of California, Berkeley, 2006, xviii plus 642 pages, "
           "ISBN 0-944613-44-6.",
     "read through its review in full, plus full text sweeps of the converted "
     "text; the book itself was not read cover to cover"),
    ("Dr", "Jozsef Drasny, review of the preceding, *The solution of the King Wen "
           "sequence?*, Yijing Dao, biroco.com/yijing/cook.htm.",
     "read in full"),
    ("HM", "Edward Hacker and Steve Moore, *A Brief Note on the Two-Part Division "
           "of the Received Order of the Hexagrams in the Zhouyi*, Journal of "
           "Chinese Philosophy 30(2), June 2003, pages 219 to 221.",
     "SECOND HAND: bibliographic identity taken from the bibliography of [Mo]; "
     "not read"),
    ("NL", "*Uninformative rungs: an order-theoretic stopping criterion for nested "
           "reference sets*, doi 10.5281/zenodo.21750029.",
     "SECOND HAND: cited as a pointer to the framework that would govern the "
     "inferential question of Section 8.3; not read in the course of this work"),
]

CLAVES = {k for k, _, _ in REFERENCIAS}


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
    for clave, cita, estatus in REFERENCIAS:
        ref.append("- **[%s]** %s  \n  *Status:* %s." % (clave, cita, estatus))
    partes.append("\n".join(ref) + "\n")
    emit("referencias", len(REFERENCIAS), "")
    emit("referencias.de.segunda.mano",
         sum(1 for _, _, e in REFERENCIAS if e.startswith("SECOND HAND")), "")

    texto = "\n".join(partes)

    # --- comprobaciones sobre el ensamblado -------------------------------
    guiones = len(re.findall(DASHES, texto))
    emit("guiones.largos.en.el.ensamblado", guiones, "en cualquiera de sus formas")
    check("cero.guiones.largos", guiones == 0)

    # toda cita del texto resuelve a una referencia
    cuerpo = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    cuerpo = cuerpo.split("# References")[0]
    citas = set(re.findall(r"\[([A-Z][A-Za-z]{1,3})\]", cuerpo))
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
