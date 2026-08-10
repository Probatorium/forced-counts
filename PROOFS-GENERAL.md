# PROOFS GENERAL

Elevar a teorema, donde se pueda, las formas vistas en la primera medicion
general. Mismo reparto de siempre y sin zona gris: **DEMOSTRADO** es lo que se
sigue de un teorema aplicado a una hipotesis argumentada o exhibida y
verificada; **ENUMERATIVO** es lo que sale de recorrer el espacio; y
**REFUTADO** es lo que se intento elevar y cayo, con su testigo.

Comprobadores en `src/general_theorems.py`, salida en
`results/general-theorems.tsv`. Sin afirmaciones de novedad: la revision sigue
ABIERTA.

---

# Pieza 1. Los extremos: la conjetura CAE

## 1.1 Lo que se intentaba demostrar

Que para el sistema de bloques B(n, k) con k igual a 1 o a n-1, **ninguna
ordenacion** queda forzada al empate. La forma venia de la primera medicion: en
las nueve combinaciones de n y k, la casilla FORZADO solo aparecio con k
intermedio.

## 1.2 REFUTADA, y por enumeracion entera

Para n igual a 3 se recorrieron **las 40320 ordenaciones** de los ocho vertices,
no una muestra:

| caso | ordenaciones | forzadas | origen |
|---|---|---|---|
| B(3, 1) | 40320 | **472** | `results/general-theorems.tsv:3`, `:4` |
| B(3, 2) | 40320 | **600** | seccion p1.n3.k2 |

Testigo exhibido para B(3, 1), la primera ordenacion forzada en orden de
recorrido: `0 1 6 7 3 2 5 4` (`results/general-theorems.tsv:5`). Y en n igual a
4 con k igual a 1, una de 3000 ordenaciones muestreadas tambien queda forzada,
con su testigo listado (`results/general-theorems.tsv:65`).

**Conclusion: la conjetura es falsa.** No hay teorema de los extremos.

## 1.3 Que queda en pie, dicho con precision

Lo medido en la primera medicion **no era falso, era mas estrecho de lo que la
frase sugeria**. Alli se recorrio la familia O3, la parametrizada por el orden
de bloques y el orden interno, y dentro de esa familia la casilla FORZADO no
aparecio nunca en los extremos. Eso sigue siendo cierto y esta medido.

Lo que ahora se sabe es que **la propiedad es de la familia O3 y no de los
extremos**: si se sale de esa familia y se recorren ordenaciones cualesquiera,
en los extremos si hay ordenaciones forzadas. Queda como **forma medida de la
familia O3**, no como teorema, y en INFORME-GENERAL.md se anade la enmienda
visible correspondiente.

---

# Pieza 2. Que decide el grupo y que decide la ordenacion

## 2.1 El lema de sigma, ya demostrado

De PREREGISTRATION-GENERAL.md b.3: la accion sobre pares de posiciones es
conjugada por sigma de la accion sobre pares de vertices, luego **los cardinales
de las orbitas no dependen de la ordenacion**. Solo dependen del grupo.

## 2.2 Lo que es funcion del grupo solo. DEMOSTRADO

**Teorema.** Los cardinales de orbita, y en consecuencia **la paridad de las
diferencias entre totales compatibles**, son funcion del grupo y no de la
ordenacion.

**Demostracion.** Los cardinales lo son por 2.1. Para las diferencias: el
conjunto de totales compatibles es el minimo mas todas las sumas de los huecos
de las orbitas libres, y el hueco de una orbita es el valor absoluto de su
cardinal menos dos veces su c. Modulo dos, ese hueco es congruente con el
cardinal de la orbita, porque el termino con c es par. Luego la paridad de cada
hueco, y por tanto la de cualquier diferencia entre dos totales compatibles, la
fija el cardinal de la orbita, que no depende de la ordenacion. Fin.

**Corolario.** Si todas las orbitas tienen cardinal par, todas las diferencias
entre compatibles son pares. Ese es el caso cubierto por la obstruccion de
paridad de b.2 y explica la progresion de paso dos de b.5.

## 2.3 Lo que necesita la ordenacion. DEMOSTRADO por testigo

**Los valores de c, y con ellos la paridad absoluta del recuento y la casilla,
no son funcion del grupo.**

**Testigo, ya medido y citado:** la fila de n igual a 4 con k igual a 2. El
grupo es el mismo, de orden 64, y la particion es la misma; el codigo de Gray
cae en PROHIBIDO y la ordenacion canonica de tipo Mawangdui cae en INTERVALO
(`results/general-landscape.tsv:145`, `:159`, con el orden del grupo en `:134` y
`:148`). Dos ordenaciones, un grupo, dos casillas. Luego la casilla no es
funcion del grupo.

**Segundo testigo, mas fuerte, de la pieza 1:** dentro de B(3, 1) hay 472
ordenaciones forzadas y 39848 que no lo estan, todas con el mismo grupo.

## 2.4 El reparto, resumido

| magnitud | depende de | estatus |
|---|---|---|
| cardinales de orbita | solo del grupo | DEMOSTRADO, b.3 |
| paridad de las diferencias entre compatibles | solo del grupo | DEMOSTRADO, 2.2 |
| numero de orbitas libres | de las dos cosas | medido |
| valores de c, paridad absoluta, casilla | necesitan la ordenacion | DEMOSTRADO por testigo, 2.3 |

---

# Pieza 3. La anomalia de Gray

## 3.1 La pregunta exacta

En n igual a 6, en los cinco niveles de la torre del codigo de Gray reflejado,
el empate **si** estaba entre los totales compatibles. En las nueve
combinaciones de n igual a 3, 4 y 5, el empate **no** lo esta. La pregunta es
que decide esa diferencia.

## 3.2 Lo que la paridad puede decidir. DEMOSTRADO

**Teorema.** Si la paridad del empate difiere de la paridad comun de los totales
compatibles, el empate es imposible.

**Demostracion.** Bajo la hipotesis de b.2 todas las orbitas tienen cardinal
par, luego por 2.2 todos los compatibles comparten paridad. Un valor de paridad
distinta no puede estar entre ellos. Fin.

## 3.3 Lo que la paridad NO decide aqui. MEDIDO, y descarta el mecanismo

El teorema de 3.2 **no es lo que ocurre en las nueve combinaciones**. Medido caso
por caso:

- en las nueve, la paridad del empate y la de los compatibles **coinciden**, las
  dos pares;
- en las nueve, el empate esta **dentro** del intervalo;
- y en las nueve, el empate **no es alcanzable**.

Origen: seccion p3 de `results/general-theorems.tsv`, con la etiqueta de
mecanismo repetida nueve veces como "dentro del intervalo pero no alcanzable".

**El mecanismo de exclusion no es la paridad. Es la resolucion del conjunto de
compatibles.** En estos casos el conjunto es extremadamente grueso: por ejemplo
en n igual a 3 con k igual a 1 el intervalo es de 12 a 16 y hay **solo dos**
totales compatibles, 12 y 16, con el empate 14 justo en el hueco
(`results/general-theorems.tsv:183`, `:186` a `:190`). Lo mismo en n igual a 4
con k igual a 2: intervalo de 56 a 64, dos compatibles, empate 60 en el hueco
(`:210`, `:213` a `:217`).

## 3.4 Que queda abierto, y con que mecanismos ya descartados

**Abierta.** Por que la torre de n igual a 6 tiene el conjunto de compatibles
fino y la de n igual a 3, 4 y 5 lo tiene grueso, no se explica aqui.

**Descartados, con evidencia:**

- **La paridad**, por 3.3: coincide en las nueve y no excluye nada.
- **Estar fuera del intervalo**, por 3.3: el empate esta dentro en las nueve.
- **El tamano o el orden del grupo**, por la pieza 2: el grupo fija los
  cardinales de orbita pero no los valores de c, y son estos los que reparten
  entre forzada y libre y con ello la resolucion del conjunto.

**Lo que queda como sospecha medible y no como afirmacion:** la resolucion la da
el numero de orbitas libres y el tamano de sus huecos. Donde hay una sola orbita
libre con un hueco grande, el conjunto tiene dos elementos y el empate cae en
medio. Eso se puede contar, y se contara al unir n igual a 6 a la misma tabla.

---

# Resumen del reparto

| afirmacion | estado |
|---|---|
| Los extremos nunca fuerzan | **REFUTADO**, con testigo y enumeracion entera en n igual a 3 |
| La ausencia de forzado en los extremos dentro de la familia O3 | ENUMERATIVO, sigue en pie |
| Cardinales de orbita, funcion del grupo solo | DEMOSTRADO |
| Paridad de las diferencias entre compatibles, funcion del grupo solo | DEMOSTRADO |
| Casilla, no es funcion del grupo | DEMOSTRADO por testigo |
| Paridad distinta implica empate imposible | DEMOSTRADO |
| La paridad explica la anomalia de Gray | **REFUTADO**, coinciden en las nueve |
| Por que el conjunto de compatibles es grueso o fino | ABIERTO |

## Reproducir

    python src/general_landscape.py
    python src/general_theorems.py

---

# Enmiendas

Se anaden al pie, con fecha y motivo. No se toca el texto de arriba, ni siquiera
la parte que esta mal, para que se vea que estuvo ahi.

## Enmienda 1, 2026-08-10: la pieza 3 se retira. La anomalia de Gray no existia

**Motivo.** Al unir n igual a 6 a la misma tabla B(n, k), con el mismo aparato y
las mismas columnas, la anomalia se deshizo. No porque se explicase, sino porque
**no habia anomalia**: era un error mio.

**El error.** DEFINICIONES-GENERAL.md declara, en su seccion 3, que en el codigo
de Gray reflejado "la linea que se anade en cada paso es la mas significativa de
la convencion de referencia", que es la linea 1, la inferior. La funcion `gray`
de `src/general_landscape.py` anadia en cada paso el **bit mas alto**, que bajo
la convencion de referencia es la linea **menos** significativa. Es decir que la
implementacion no era la ordenacion declarada, sino otra.

**Como se detecto.** Al medir n igual a 6 con el mismo aparato, la torre de Gray
salio PROHIBIDA en los cinco niveles, cuando en el informe de n igual a 6 el
empate si era alcanzable en los cinco. Dos resultados distintos para el mismo
objeto obligan a mirar el objeto, y los dos programas construian secuencias
distintas. La comprobacion decisiva: la version declarada reproduce la forma
cerrada del codigo de Gray, el numero XOR el mismo desplazado uno, bajo la
convencion de referencia, y la implementada no.

**Lo corregido.** `src/general_landscape.py` construye ahora la ordenacion
declarada, con la comprobacion contra la forma cerrada. Se volvieron a correr
los tres programas.

**Lo que sale con la ordenacion declarada:** el codigo de Gray reflejado cae en
**INTERVALO en las catorce combinaciones**, n de 3 a 6 y todos los k. No hay
diferencia entre n igual a 6 y los demas, y por tanto **no hay anomalia que
explicar**.

**Que queda en pie de la pieza 3.** Solo su seccion 3.2, que es un teorema y no
depende de esto: si la paridad del empate difiere de la paridad comun de los
totales compatibles, el empate es imposible. Todo lo demas de la pieza 3, la
pregunta, los mecanismos descartados y la sospecha sobre la resolucion del
conjunto, **queda retirado por esta enmienda**: describia un fenomeno que no
existe.

**Lo que no cambia.** La pieza 1 y la pieza 2 no usan la funcion `gray`. La
refutacion de la conjetura de los extremos, con sus 472 y 600 ordenaciones
forzadas en la enumeracion entera de n igual a 3, sigue en pie sin tocar. El
reparto de la pieza 2 tambien, y su testigo de n igual a 4 con k igual a 2 sigue
siendo valido porque la casilla de la ordenacion canonica de tipo Mawangdui no
depende de `gray`; lo que cambia es que ahora las dos casillas de esa fila son
INTERVALO, asi que **el testigo de la pieza 2 pasa a ser el otro**, el de las 472
ordenaciones forzadas y las 39848 no forzadas de B(3,1), todas con el mismo
grupo. Ese testigo nunca dependio de `gray`.
