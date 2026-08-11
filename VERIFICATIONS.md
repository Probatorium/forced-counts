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


---

## 2. Triaje de tres auditorias externas, 10 de agosto de 2026

**Quien.** Tres auditorias externas al proyecto, sobre el manuscrito publicado en
el remoto en la cabeza `534ebba`.

**Que se hizo aqui.** Se triaron punto por punto. Lo que se sostiene se reparo en
la sesion 32; lo que no se sostiene se refuta con su recibo; lo que no se puede
comprobar se registra como pista sin verificar en PRIOR-ART.md y no se usa.

### 2.1 Sostenidos, y reparados

Nueve puntos, todos de redaccion o de definicion. **Ninguno tocaba matematica ni
cifra medida**, y eso importa para leer el resto: las auditorias no encontraron
un error de calculo.

| lo senalado | la reparacion |
|---|---|
| el alcance del Teorema 2 decia "todos los sistemas de bloques considerados aqui" | acotado a los B(n, k) de la seccion 7, y dicho que los otros dos grupos no contienen todas las traslaciones y se tratan con la contabilidad por orbitas |
| "de lo que se iba a medir y que lo refutaria" prometia mas de lo que hubo | suavizado en el resumen y en la introduccion a "y, donde se hicieron predicciones, de que las refutaria" |
| "el mecanismo que se afirmaba" sin decir donde | puntero anadido: se afirmo en la preinscripcion de este repositorio |
| el "miembro canonico" de B(n, k) sin definir | definicion formal, extraida de la funcion que lo construye y comprobada contra ella para todo n y todo k |
| "half turn" sin definir en su primera aparicion | definido como el elemento de B_6 de permutacion (1 6)(2 5)(3 4) y mascara nula, verificado contra la funcion del codigo |
| Gritter sin editorial | autoedicion, conforme a APA, con la nota de que si un ejemplar nombra otra, manda el artefacto |
| la semilla y el esquema de muestreo sin imprimir | impresos y congelados: semilla, tamano, uniforme e independiente, con reemplazo, y el umbral por debajo del cual se enumera entero |
| el emparejamiento llamado "la caracterizacion" | reescrito: es el criterio de 5.3, con una direccion demostrada y la otra enumerativa; la caracterizacion es el Teorema 2 |
| "un caso a descartar" y el adjetivo "informativo" | reescritos: "un caso que cae fuera del fenomeno que se recoge", e "informativo en sentido estructural, sin afirmacion inferencial" |

### 2.2 Refutado, con su recibo

Una de las auditorias afirmo que el registro de esfuerzo estaba roto. **Es
falso, y el recibo es reproducible por cualquiera:**

    $ git checkout 534ebba
    $ python tools/effort.py verify
    registros: 154
    cadena integra, append only sin roturas
    sesion abierta: ninguna

La cadena de sha256 del registro liga cada linea con la anterior. Una edicion
retroactiva de cualquier linea la rompe y el verificador la delata, y eso es
justo lo que no ocurre. La afirmacion no venia acompanada de la linea que
supuestamente fallaba ni de la salida del verificador, que es lo que habria
hecho falta para sostenerla.

### 2.3 Cuatro pistas sin verificar

Las auditorias apuntaron cuatro antecedentes posibles. No entran en el
manuscrito, no cambian ninguna afirmacion y no se citan.

**Y hay que decir en que punto estan de verdad: su texto literal no llego a la
sesion en la que se escribio este asiento.** Se sabe que son cuatro y de donde
vienen; no se sabe a que apuntan. La seccion 16 de PRIOR-ART.md queda abierta
con ese hueco declarado y sin rellenar, porque anotar de memoria cuatro fichas
bibliograficas seria inventarlas, y una ficha inventada es peor que un hueco: el
hueco se ve.

**Estatus del conjunto.** REPORTADO por terceros y triado aqui. Los nueve puntos
sostenidos estan reparados en esta sesion y se pueden ver en el diff; el
refutado tiene su recibo arriba; las cuatro pistas estan donde se guarda lo que
no se ha leido.
