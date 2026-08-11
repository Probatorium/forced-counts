# Comprobaciones hechas fuera de esta maquina

Este fichero registra comprobaciones sobre los artefactos del repositorio que
**no se pueden reproducir aqui**, con la unica razon por la que existen: sin
ellas quedaria un hueco en lo que se puede afirmar del paquete.

Se registra el hecho tecnico y nada mas. Todo lo demas de este repositorio se
puede volver a correr; lo que entre aqui, no, y por eso se marca como
**REPORTADO** y se dice que herramienta lo produjo, con que resultado y sobre
que fichero. Ninguna cifra de este fichero entra en el manuscrito:
`src/declared_values.py` exige que toda cifra impresa en `paper/` salga de una
linea de `results/` producida por un programa de este repositorio, y estas no lo
son. Esa frontera es deliberada.

---

## 1. Compilacion de `paper/PAPER.tex` con pdfTeX

**El hecho.** `paper/PAPER.tex` se ha compilado con latexmk sobre pdfTeX, fuera
de esta maquina, con este resultado:

| lo comprobado | lo reportado |
|---|---|
| codigo de salida de la compilacion | 0 |
| errores | 0 |
| cajas desbordadas o vacias | 0 |

**Por que hace falta que conste.** En esta maquina no hay ninguna cadena de
LaTeX: ni pdflatex, ni xelatex, ni lualatex, ni tectonic, ni latexmk, comprobado
antes de escribir el generador del `.tex` y vuelto a comprobar despues. El `.tex`
se genera y se coteja aqui contra el manuscrito, cifra a cifra, cita a cita y
celda a celda, pero **no se compila aqui**, y sin este registro no habria nada
que dijera que compila.

La ultima fila cierra ademas lo que el barrido de esta casa no alcanza. El
generador comprueba sobre la FUENTE que no queden rachas de guion que LaTeX
compondria como raya, y que ningun hash viaje sin puntos de corte; que no haya
cajas desbordadas o vacias solo se ve en la SALIDA compuesta, y eso pide un
compilador.

**Estatus: REPORTADO, no reproducible aqui.** Cualquiera con latexmk puede
repetirlo: clonar el repositorio y compilar `paper/PAPER.tex`.

**El alcance, que conviene acotar.** El resultado corresponde al `.tex` tal y
como estaba al correrse, y este fichero no fija de que commit se trataba. El
manuscrito ha seguido cambiando despues, asi que la compilacion **no certifica
el `.tex` de ahora**. Nada depende de que lo haga: el estado del PDF canonico,
declarado en `paper/PDF-STATE.tsv`, sigue siendo `esperando`, y sera la
compilacion que produzca ese PDF la que quede atada a un commit por el colofon y
comprobada por `src/pdf_bridge.py`.

**Lo que no dice.** No dice que el PDF asi compilado sea igual a
`paper/PAPER-preview.pdf`, y no lo es: aquel lo compone pdfTeX desde el `.tex` y
este lo compone reportlab desde el mismo modelo intermedio. Son dos
composiciones del mismo contenido, y lo que `src/build_paper.py` exige de las dos
formas es que lleven las mismas cifras, las mismas citas y las mismas celdas de
tabla, no que tengan el mismo aspecto ni el mismo numero de paginas.
