# Verificaciones de terceros

Este fichero registra comprobaciones hechas **fuera de este repositorio y por
alguien que no es su autor**. Existe separado de los informes por una razon de
metodo: todo lo demas que este repositorio afirma se puede volver a correr aqui,
y esto no. Lo que sigue se registra con la misma disciplina que la revision de
antecedentes aplica a lo que no ha leido de primera mano: **se dice quien lo
hizo, cuando, sobre que, y se marca como reportado y no como comprobado aqui**.

Ninguna cifra de este fichero entra en el manuscrito. `src/declared_values.py`
exige que toda cifra impresa en `paper/` salga de una linea de `results/`
producida por un programa de este repositorio, y estas no lo son. Esa frontera
es deliberada.

---

## 1. Compilacion de `paper/PAPER.tex`, 10 de agosto de 2026

**Quien.** El auditor externo del proyecto.

**Sobre que.** `paper/PAPER.tex` tal y como esta en el remoto publico
`github.com/Probatorium/forced-counts`, clonado por el auditor. No sobre el arbol
de trabajo de esta maquina, ni sobre un fichero enviado por correo.

**Con que.** latexmk con pdfTeX.

**Que reporta.**

| lo comprobado | lo reportado |
|---|---|
| codigo de salida de la compilacion | 0 |
| errores | 0 |
| paginas del PDF resultante | 22 |
| cifras del manuscrito en el texto extraido | presentes |
| la tabla del paisaje en el texto extraido | presente |
| rayas compuestas por LaTeX | 0 |

**Por que importa.** Cierra el unico hueco que la sesion 26 dejo abierto y
declarado. En esta maquina no hay ninguna cadena de LaTeX: ni pdflatex, ni
xelatex, ni lualatex, ni tectonic, ni latexmk, ni pandoc, ni una instalacion de
TeX Live o MiKTeX en las rutas habituales, comprobado antes de escribir el
generador. El `.tex` se entrego generado y cotejado contra el manuscrito, pero
**sin compilar**, y asi se dijo en el mensaje del commit y en el informe. Ahora
consta que compila, y consta quien lo comprobo.

La ultima fila tambien cierra algo. El barrido de guiones de esta casa prohibe la
raya tambien en ingles, y en LaTeX una raya se escribe con dos o tres guiones
seguidos, de modo que un fichero sin guiones largos unicode todavia podria
componer rayas al pasar por TeX. `src/build_paper.py` lo comprueba sobre la
fuente y da cero; el auditor lo confirma sobre la salida compuesta, que es donde
de verdad se ve.

**Estatus.** REPORTADO, no comprobado aqui. No se puede reproducir en esta
maquina por falta de la cadena de LaTeX, y no se presenta como si se hubiera
podido. Cualquiera que tenga latexmk puede repetirlo: clonar el remoto y
compilar `paper/PAPER.tex`.

**Lo que no dice.** No dice que el PDF compilado por el auditor sea igual al
`paper/PAPER.pdf` de este repositorio, y no lo es: aquel lo compone pdfTeX desde
el `.tex`, y este lo compone reportlab desde el mismo modelo intermedio. Son dos
composiciones del mismo contenido, y lo que `src/build_paper.py` exige de las dos
formas es que lleven las mismas cifras, las mismas citas y la misma tabla, no que
tengan el mismo aspecto ni el mismo numero de paginas.
