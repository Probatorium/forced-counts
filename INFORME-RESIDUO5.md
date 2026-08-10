# El residuo de 5: anatomia y frontera

Fases 1 y 2 de lo declarado en DEFINICIONES-RESIDUO5.md, cuya lista de
candidatas es **cerrada** y se commiteo antes de medir nada. Cifras de
`src/residuo5.py`, salida en `results/residuo5.tsv`. Sin afirmaciones de novedad.

Heredado y vuelto a comprobar al arrancar: grupo de orden 384, recuento
observado 1013, 19 orbitas libres, intervalo de 957 a 1059
(`results/residuo5.tsv:4`, `:10` a `:12`).

---

# Fase 1. La anatomia del 1013

## 1.1 El vector completo

Las 19 orbitas libres, ordenadas por cardinal. Ninguna se resume ni se omite.

| orbita | cardinal | mitad | aportacion | desviacion | A1: pares con el mismo nuclear | A2: pares dentro de una misma mitad | pares que son un par de King Wen |
|---|---|---|---|---|---|---|---|
| 0 | 192 | 96 | 90 | **-6** | 0 | 104 | 0 |
| 1 | 96 | 48 | 50 | +2 | 0 | 40 | 0 |
| 2 | 96 | 48 | 52 | +4 | 0 | 40 | 0 |
| 3 | 96 | 48 | 46 | -2 | 0 | 40 | 0 |
| 4 | 96 | 48 | 46 | -2 | 0 | 52 | 0 |
| 5 | 96 | 48 | 46 | -2 | 0 | 48 | 0 |
| 6 | 96 | 48 | 46 | -2 | **32** | 48 | 0 |
| 7 | 96 | 48 | 46 | -2 | 0 | 44 | 0 |
| 8 | 96 | 48 | 54 | **+6** | 0 | 44 | 0 |
| 9 | 96 | 48 | 52 | +4 | 0 | 40 | 0 |
| 10 | 48 | 24 | 28 | +4 | 0 | 28 | 0 |
| 11 | 48 | 24 | 22 | -2 | **16** | 28 | 0 |
| 12 | 48 | 24 | 22 | -2 | **16** | 28 | 0 |
| 13 | 24 | 12 | 16 | +4 | 0 | 8 | 0 |
| 14 | 12 | 6 | 5 | **-1** | 0 | 12 | **12** |
| 15 | 12 | 6 | 8 | +2 | 0 | 4 | 0 |
| 16 | 12 | 6 | 4 | -2 | 0 | 8 | 0 |
| 17 | 4 | 2 | 3 | **+1** | 0 | 4 | **4** |
| 18 | 4 | 2 | 3 | **+1** | 0 | 4 | **4** |

Suma de desviaciones: **5** (`results/residuo5.tsv:89`), que es 1013 menos 1008,
como tiene que ser.

## 1.2 Lo primero que se ve, y es lo contrario de lo que se buscaba

**El 5 no esta localizado.** Las **19** orbitas libres tienen desviacion no nula,
las diecinueve (`results/residuo5.tsv:91`). No hay una orbita culpable ni un
punado: hay diecinueve desviaciones que se cancelan casi del todo y dejan 5.

Las mayores en valor absoluto son de 6, con signos contrarios, en las orbitas 0
y 8. Si se buscaba una anatomia con un culpable, no la hay.

## 1.3 La parte par y la parte impar

Diecisiete desviaciones son pares y tres son impares, y las tres impares estan
exactamente en las tres orbitas que **contienen pares de King Wen**, las orbitas
14, 17 y 18. Suman menos uno mas uno mas uno, es decir **mas 1**. Las otras
dieciseis suman **mas 4**.

Es la unica particion del 5 que sale sola de la tabla: **1 de las orbitas que
llevan los pares de la propia construccion, y 4 del resto**. Se reporta como
lectura de la tabla y no como explicacion de nada.

## 1.4 El cruce contra A1 y A2, sin lenguaje de significancia

**A1, nuclear.** Solo tres orbitas contienen pares cuyos dos hexagramas comparten
nuclear: la 6 con 32, la 11 con 16 y la 12 con 16. Las tres tienen desviacion
**menos 2**. Las otras dieciseis orbitas no contienen ningun par de esos.

**A2, las mitades.** Las diecinueve orbitas contienen pares dentro de una misma
mitad, entre 4 y 104. Ninguna columna separa nada.

Eso es lo que hay en la tabla. **No se dice mas**: son recuentos con su
procedencia, sin nula declarada, sin familia de comparaciones fijada de antemano
y sin disciplina de multiplicidad, y en este repositorio eso significa que no se
leen como evidencia de nada.

---

# Fase 2. Las simetrias extendidas

## 2.1 Las que no aportan biyeccion

**A1, nuclear.** No es biyectiva, como quedo declarado. La operacion tiene 16
imagenes distintas (`results/residuo5.tsv:151`), y de los 32 pares de King Wen
solo **4** tienen sus dos miembros con el mismo nuclear (`:149`). No aporta
elemento de grupo y no puede estrechar nada (`:150`).

**A2, las mitades.** El corte respeta los pares: ninguno cruza la frontera entre
la posicion 30 y la 31 (`results/residuo5.tsv:153`). Pero las mitades son de 30 y
34, no definen ninguna traslacion, y no aportan biyeccion (`:154`), tal y como se
declaro. El tema tiene dueno localizado, Hacker y Moore 2003, **no leido**, y de
ahi no se toma nada.

## 2.2 Las que aportan biyeccion

Las tres respetan el sistema de pares y ninguna es afin, o sea que las tres estan
fuera de B6, que es lo que las hacia candidatas.

| candidata | orden del grupo generado | orbitas libres | intervalo | anchura | fuerza |
|---|---|---|---|---|---|
| ninguna, el grupo de partida | 384 | 19 | [957, 1059] | 102 | no |
| **A5**, el intercambio dentro del par | **768** | **17** | **[961, 1055]** | **94** | no |
| A3, desplazamiento ciclico de pares | mas de 200000 | 2 | [1003, 1013] | 10 | no |
| A4, inversion del orden | mas de 200000 | 2 | [1003, 1013] | 10 | no |
| A3 mas A4 mas A5 | mas de 200000 | 2 | [1003, 1013] | 10 | no |

Origen: `results/residuo5.tsv:155` a `:213`.

**A5 es el unico resultado que cuenta, y cuenta.** Anadir tau, la propia regla de
emparejamiento de King Wen, que no es afin y por eso no estaba en el grupo de
orden 384 aunque ese grupo sea justo su centralizador, **duplica el grupo a 768**,
baja las orbitas libres de 19 a 17 y estrecha el intervalo de 102 a 94. Es un
grupo pequeno, estructurado, y es la regla que la construccion ya tenia. Queda
como **ENUMERATIVO**: es un calculo sobre un caso, no un teorema.

**A3 y A4 no cuentan, y estaba escrito antes de correr.** Estrechan mucho mas,
hasta dejar dos orbitas y un intervalo de 10, pero el grupo que generan pasa del
tope declarado de 200000 (`results/residuo5.tsv:158`, `:173`). La declaracion de
la fase 0 decia que un estrechamiento obtenido con un grupo grande y sin
estructura no es un hallazgo, y esto es exactamente eso: dos permutaciones
definidas por posiciones generan casi todo el estabilizador del sistema de pares,
y con casi todo el estabilizador cualquier cosa se estrecha. Se reporta y no se
cobra.

## 2.3 Lo que ninguna hace

**Ninguna fuerza** (`:168`, `:183`, `:198`, `:213`). **Ninguna alcanza el
empate:** en las cuatro filas el empate sigue fuera de los totales compatibles
(`:165`, `:180`, `:195`, `:210`). Y el recuento observado sigue siendo 1013 en
todas, porque cambiar el grupo no cambia la secuencia.

---

# Desenlace

La rama que se cumple es la primera y la segunda a la vez, y conviene decirlo sin
redondear.

**Hay un estrechamiento, y es A5**, con su enumeracion declarada: el grupo pasa
de 384 a 768, las orbitas libres de 19 a 17, el intervalo de 102 a 94. Es un
hallazgo pequeno y honesto: la propia regla de emparejamiento, metida en la
estructura, aprieta un poco.

**Y no explica el 5.** Ni A5 ni ninguna otra. Despues de A5 el residuo sigue
siendo 5, el empate sigue prohibido, y las 17 orbitas libres que quedan siguen
repartiendo la desviacion entre casi todas ellas.

Por tanto, y en lo que toca a la pregunta que abria este tramo:

> **El residuo de 5 queda DECLARADO INFORMATIVO relativo a esta lista.** Ninguna
> de las cinco estructuras candidatas lo explica. La descomposicion existe, esta
> completa en la tabla de 1.1, y no tiene culpable: son diecinueve desviaciones
> que casi se cancelan.
>
> **La matematica toca fondo donde empieza la eleccion editorial.** Lo que queda
> del 5, despues de agotar la simetria que la construccion respeta y las cuatro
> estructuras adicionales declaradas, no es un residuo que la estructura pueda
> absorber: es lo que la secuencia recibida tiene de eleccion y no de regla.

Esta declaracion va a la seccion 6 del manuscrito como cierre, con la lista
cerrada de lo que se probo y con la advertencia de que es **relativa a esa
lista**: otra estructura, no probada aqui, podria absorberlo.

## Reproducir

    python src/residuo5.py
