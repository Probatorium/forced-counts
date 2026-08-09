# Procedencia de data/sequences.json

## De donde sale

Repositorio fuente: `kingwen-orderings-replication`, en la maquina local, sin
remoto por medio.

- Etiqueta: `zenodo-v3`
- Commit: `d6afae20bbefba56728251f34f8e3870c43e2cbd`
- Arbol: `18e55dd409b97c8794b1aa74d11a6bd892860bfd`
- Fichero leido: `verify_paper.py`
- sha256 del fichero leido:
  `1efd0521f3f3e31a718504fdf1a9fa42b9a015d709fdaaf0b2f4a76b88ac2a9e`

## Como se hizo

    git --git-dir=<fuente>/.git archive --format=tar zenodo-v3 | tar -x -C _source/zenodo-v3
    python tools/extract_sequences.py

`git archive` lee el arbol de la etiqueta y escribe un archivo. No toca el
indice, ni la rama, ni el arbol de trabajo del repositorio fuente. El despliegue
vive en `_source/`, que esta fuera de la historia de este repositorio por
`.gitignore`.

Se comprobo antes y despues que la fuente sigue en `HEAD`
`726c1e994d216195ffa0f449323657736e028aab`, rama `errata`, arbol limpio, y que
la fecha de modificacion de su indice no cambio.

## Que se extrajo, y que no

Se extrajeron solo las tres secuencias: la lista de sus 64 hexagramas en orden.
Cada hexagrama se guarda como una cadena de seis caracteres, indice 0 la linea
inferior, `y` yang y `n` yin. Esa forma es neutral respecto de la convencion de
bits, para que la eleccion de convencion se haga aqui y en las cuatro variantes
fijadas en PREREGISTRATION.md, y no venga heredada de la fuente.

No se extrajo ninguna cifra de resultados. Ningun numero de la fuente entra como
entrada del computo de `src/measure.py`.

De las tres secuencias, dos son construcciones con reglas documentadas
(Mawangdui y Jing Fang) y una es un dato recibido (King Wen). Las dos
construcciones se vuelven a derivar desde cero en `src/measure.py` a partir de
sus reglas, y el programa se detiene si la rederivacion no reproduce la
secuencia extraida.

## Nota de contacto

La regla de contacto de CONTACT-RULES.md se cumplio: acceso de solo lectura y
solo en la etiqueta `zenodo-v3`. Una llamada intermedia de comprobacion se
escribio mal, con `--git-dir` apuntando a la fuente y el arbol de trabajo
apuntando a este repositorio; era una orden de lectura, no escribio nada, y se
verifico despues que el indice de la fuente conserva su fecha anterior. Queda
anotada en el registro de esfuerzo como lo que fue.
