# Ficheros de terceros, y que se ha hecho con ellos

Este repositorio contiene material que no se escribio aqui. En el
bundle de la historia ese material **se filtra**, y en su lugar queda
esta ficha con lo necesario para conseguirlo por cuenta propia. Los
programas que lo consumen siguen en el paquete, de modo que la cadena
se puede rehacer entera en cuanto el material se repone.

## `data/sequences.json`

- **Que es:** Las tres secuencias, extraidas del paquete de replicacion kingwen-orderings-replication en la etiqueta zenodo-v3, commit d6afae20bbefba56728251f34f8e3870c43e2cbd.
- **sha256:** `430ead3acd34c060b4afdb164a1e62f318709b3dc398e44d92153e043a81cf8a`
- **Bytes:** 3307
- **Como se consigue:** Se obtiene clonando ese repositorio en esa etiqueta y corriendo tools/extract_sequences.py, que esta aqui y no se filtra.
- **Estado en el bundle:** filtrado de toda la historia.

## `artifacts/radisic-2601.07175v3-appendix-A.tsv`

- **Que es:** Transcripcion del apendice A de Alejandro Radisic, Optimal Equivariant Matchings on the 6-Cube, arXiv:2601.07175v3, pagina 11.
- **sha256:** `0964068b5efb56c918585ee412033726a1f8cabde91ce60f09ce4bae8102dbc2`
- **Bytes:** 2025
- **Como se consigue:** Se obtiene descargando ese articulo de arXiv y transcribiendo su apendice A. Aqui solo se usa como objeto de comparacion, nunca como fuente de ningun computo.
- **Estado en el bundle:** filtrado de toda la historia.

## `paper/PAPER-preview.pdf`

- **Que es:** PREVIEW compuesto aqui con reportlab desde el mismo modelo intermedio que el .tex. NO es el PDF canonico del articulo.
- **sha256:** `0b662ed889ee02a53a77091970663def2d421f8b3ab8e28dc14f0e4ddcfc1e8b`
- **Bytes:** 154542
- **Como se consigue:** Se regenera con python src/build_paper.py. El PDF canonico es paper/PAPER.pdf, que compila LaTeX desde paper/PAPER.tex y que no se puede producir en la maquina donde se escribio este repositorio.
- **Estado en el bundle:** filtrado de toda la historia.
