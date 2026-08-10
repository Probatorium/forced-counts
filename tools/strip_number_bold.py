#!/usr/bin/env python3
"""
Quita la negrita de las cifras de la prosa, y solo de las cifras.

Cuando el manuscrito paso a imprimir sus numeros, cada cifra publicable se puso
en negrita para que saltara a la vista. Con ciento y pico de ellas el efecto se
invierte: una pagina en la que resalta todo no resalta nada, y ademas no es el
estilo de la casa. La negrita se reserva para tres cosas:

  - las cabeceras y los rotulos de parrafo,
  - un termino en su primera aparicion, cuando se esta definiendo,
  - los nombres de las tres casillas, forced, bounded y barred, donde se definen.

Todo lo demas vuelve a texto normal.

La herramienta quita la negrita SOLO cuando lo que hay dentro es una cifra o una
expresion de cifras: 1008, 0, [957, 1059], 0.09514. Lo que no encaja en ese
molde no se toca, y el informe LISTA lo que ha conservado, para que la decision
se pueda revisar en lugar de tener que fiarse de ella.

  python tools/strip_number_bold.py [--comprobar]

Salida: results/bold-strip.tsv
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")
OUT = os.path.join(ROOT, "results", "bold-strip.tsv")

FUENTES = ["00-abstract.md", "01-introduction.md", "02-preliminaries.md",
           "03-orbit-accounting.md", "04-parity-obstruction.md",
           "05-characterisation.md", "06-three-historical-orderings.md",
           "07-landscape.md", "08-open-problems.md", "09-verification.md"]

NEGRITA = re.compile(r"\*\*([^*]+)\*\*")
# Una cifra o una expresion hecha solo de cifras, corchetes, comas, puntos y
# signos. Nada de letras: en cuanto hay una palabra, es un termino y se queda.
SOLO_CIFRA = re.compile(r"^[\d\s,.\[\]()+\-/]+$")


def main():
    comprobar = "--comprobar" in sys.argv
    rows, quitadas, conservadas = [], 0, {}

    for nombre in FUENTES:
        ruta = os.path.join(PAPER, nombre)
        t = open(ruta, encoding="utf-8").read()
        # Los comentarios de ensamblaje llevan las declaraciones de cifras y no
        # se tocan: ahi los asteriscos no existen y el texto no es del lector.
        partes = re.split(r"(<!--.*?-->)", t, flags=re.S)
        n_aqui = 0
        for i, p in enumerate(partes):
            if p.startswith("<!--"):
                continue

            def decide(m):
                nonlocal n_aqui
                dentro = m.group(1)
                if SOLO_CIFRA.match(dentro):
                    n_aqui += 1
                    return dentro
                conservadas.setdefault(dentro.strip(), 0)
                conservadas[dentro.strip()] += 1
                return m.group(0)

            partes[i] = NEGRITA.sub(decide, p)

        nuevo = "".join(partes)
        quitadas += n_aqui
        rows.append(("quitadas.%s" % nombre, n_aqui, ""))
        if nuevo != t and not comprobar:
            with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(nuevo)

    rows.append(("negritas.de.cifra.quitadas", quitadas, ""))
    rows.append(("negritas.conservadas.distintas", len(conservadas),
                 "terminos, rotulos y cabeceras: no son cifras"))
    rows.append(("modo", "comprobar" if comprobar else "escribir", ""))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Retirada de la negrita de las cifras de la prosa.\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in rows:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        fh.write("#\n# LO CONSERVADO, una linea por texto en negrita que se ha\n")
        fh.write("# dejado como estaba, con las veces que aparece.\n")
        for texto, n in sorted(conservadas.items(), key=lambda x: -x[1]):
            fh.write("conservada\t%d\t%s\n" % (n, texto))

    for k, v, _ in rows:
        if not k.startswith("quitadas."):
            print("  %-36s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
