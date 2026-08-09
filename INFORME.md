# Informe de medicion

Todas las cifras de este informe salen de una sola ejecucion de
`src/measure.py`, y cada una se cita con su fichero y su linea de origen. No hay
ninguna afirmacion de novedad en este documento: la revision de antecedentes no
ha empezado, y por tanto no se sabe ni se insinua que nada de lo que sigue sea
nuevo.

## Procedencia

Las tres secuencias vienen de `kingwen-orderings-replication`, leido solo en la
etiqueta `zenodo-v3`, commit `d6afae20bbefba56728251f34f8e3870c43e2cbd`
(`results/measurements.tsv:3`), arbol
`18e55dd409b97c8794b1aa74d11a6bd892860bfd` (`results/measurements.tsv:4`), sobre
`verify_paper.py` con sha256 `1efd0521f3f3e31a718504fdf1a9fa42b9a015d709fdaaf0b2f4a76b88ac2a9e`
(`results/measurements.tsv:5`). El detalle del acceso esta en
`data/PROVENANCE.md`. Ninguna cifra de resultados de la fuente entra como
entrada del computo.

Las dos construcciones se vuelven a derivar aqui desde sus reglas y reproducen
la secuencia extraida: Mawangdui (`results/measurements.tsv:8`) y Jing Fang
(`results/measurements.tsv:9`). King Wen no se deriva: es el dato recibido
(`results/measurements.tsv:10`).

Denominador: C(64,2) = 2016 (`results/measurements.tsv:6`). Valor esperado de
una ordenacion al azar: 1008 (`results/measurements.tsv:7`).

## 1. La tabla completa

Inversiones contra el orden binario, bajo las cuatro convenciones fijadas en
PREREGISTRATION.md.

| secuencia | yang=1, inferior MSB | yang=1, inferior LSB | yang=0, inferior MSB | yang=0, inferior LSB |
|---|---|---|---|---|
| Mawangdui | 1008 | 1008 | 1008 | 1008 |
| Jing Fang | 1008 | 1008 | 1008 | 1008 |
| King Wen  | 1013 | 1013 | 1003 | 1003 |

Origen: Mawangdui `results/measurements.tsv:11` a `:14`; Jing Fang `:15` a
`:18`; King Wen `:19` a `:22`. Las tasas sobre C(64,2) van en la columna de nota
de esas mismas lineas: 0.500000 para las dos primeras filas, 0.502480 y
0.497520 para King Wen.

Las cuatro convenciones son cuatro aplicaciones realmente distintas: sobre una
ordenacion barajada dan cuatro recuentos distintos
(`results/measurements.tsv:23`). Que dos de ellas coincidan en King Wen es un
hecho de King Wen, no una degeneracion de la definicion.

Dos regularidades visibles en la tabla, ambas explicables sin medir nada mas:
cambiar la polaridad manda el recuento a 2016 menos el recuento, porque invierte
el orden binario entero; y cambiar la orientacion no mueve ninguna de las tres
secuencias.

## 2. Que fuerza la clausura, y que no

Sea sigma una ordenacion de los 64 hexagramas y pi la permutacion de posiciones
inducida por la complementacion. Para cualquier par de posiciones, la
complementacion invierte el orden binario de los dos hexagramas. Entonces:

- si pi conserva el orden relativo del par, el par imagen tiene el estado de
  inversion contrario. La involucion sobre pares empareja cada inversion con una
  no inversion, sin puntos fijos, y esa clase aporta exactamente la mitad de sus
  pares. Esto es lo que la clausura fuerza, y vale para cualquier ordenacion.
- si pi invierte el orden relativo del par, el estado se conserva y la clausura
  no dice nada. Esa clase queda libre.

Medido, con la convencion de referencia yang = uno e inferior mas significativa:

| secuencia | pares conservados | forzadas | pares libres | libres observadas | mitad de los libres | desviacion | total |
|---|---|---|---|---|---|---|---|
| Mawangdui | 968 | 484 | 1048 | 524 | 524 | 0 | 1008 |
| Jing Fang | 992 | 496 | 1024 | 512 | 512 | 0 | 1008 |
| King Wen | 1374 | 687 | 642 | 326 | 321 | 5 | 1013 |

Origen: Mawangdui `results/measurements.tsv:24` a `:30`; Jing Fang `:31` a
`:37`; King Wen `:38` a `:44`.

Tres lecturas de esta tabla, todas medidas y ninguna interpretativa:

1. La mitad forzada se cumple en las tres, King Wen incluida. No distingue nada.
2. La clausura no fuerza el total en ninguna de las tres. En Mawangdui fuerza
   484 de 1008 y en Jing Fang 496 de 1008. El resto cae en la clase libre.
3. La desviacion de King Wen respecto del valor esperado vive entera en la clase
   libre, y vale 5, que es exactamente 1013 menos 1008.

## 3. Seccion (a), Mawangdui: RETRODICCION

Se reporta como retrodiccion, no como hallazgo. El argumento existia antes de
abrir este repositorio y aqui solo se comprueba.

La parte numerica se confirma: 1008 en las cuatro convenciones
(`results/measurements.tsv:11` a `:14`), es decir exactamente la mitad de
C(64,2).

La parte mecanica no se sostiene tal y como estaba enunciada. La seccion (a)
decia que el recuento esta forzado por la clausura. La clausura existe y es
concreta: el complemento manda cada octeto entero sobre otro octeto
(`results/measurements.tsv:45`), y el octeto de trigrama superior U va al de
trigrama superior complementario, que en el orden de familia recibido esta
cuatro mas alla (`results/measurements.tsv:46`). La permutacion completa y las
posiciones internas octeto por octeto estan en `results/permutations.txt:17` a
`:30`, y pi entero en `results/permutations.txt:5`.

Pero esa clausura solo fuerza 484 de las 1008 inversiones
(`results/measurements.tsv:25`). Las otras 524 caen en la clase libre
(`results/measurements.tsv:27`), y que esa clase se parta tambien exactamente
por la mitad no se sigue de la clausura. La seccion 6 lo confirma por control:
hay 40320 ordenes de familia posibles para los octetos, todos con la clausura
intacta, y solo 3836 dan el valor esperado (`results/measurements.tsv:92` a
`:94`).

Lectura honesta: la cifra retrodicha aparece; el mecanismo retrodicho es
insuficiente para producirla.

## 4. Seccion (b), Jing Fang: PREDICCION

### La clausura, demostrada

El complemento manda el palacio de cabeza H sobre el palacio de cabeza
complementaria, termino a termino y sin mover la posicion interna. Comprobado
en los ocho palacios (`results/measurements.tsv:41`,
`results/permutations.txt:46`).

La razon no depende de la secuencia recibida. Cada generacion de un palacio es
la cabeza doblada mas una mascara de lineas fija, y complementar conmuta con
anadir una mascara. El alma errante anade otra mascara fija. El alma que vuelve
restituye el trigrama inferior de la cabeza, y el complemento de esa restitucion
es la restitucion del complemento. Luego el palacio complementado es, termino a
termino, el palacio de la cabeza complementada.

La permutacion concreta que pedia el enunciado:

- Sobre palacios: el desplazamiento de cuatro. Qian va a Kun, Zhen a Xun, Kan a
  Li, Gen a Dui, y sus inversos (`results/measurements.tsv:39`,
  `results/permutations.txt:34` a `:41`).
- Dentro del palacio: la identidad. La posicion p va a la posicion p
  (`results/measurements.tsv:40`, `results/permutations.txt:43`).
- Sobre las 64 posiciones: pi(8b + p) = 8((b+4) mod 8) + p, es decir
  pi(i) = (i + 32) mod 64, verificado posicion a posicion
  (`results/permutations.txt:9` y `:11`).

Esa es la permutacion concreta de los ordenes de la construccion. No hay
contraejemplo: cero hexagramas de la construccion cuya imagen bajo
complementacion salga de ella (`results/measurements.tsv:50`).

### El recuento

1008 en las cuatro convenciones (`results/measurements.tsv:15` a `:18`).

### Veredicto, separando lo que se demuestra de lo que no

- La clausura predicha existe y queda demostrada, no solo comprobada.
- El recuento predicho aparece.
- El enunciado de que la clausura fuerza el recuento NO queda demostrado, y la
  medicion apunta a que es falso: la clausura fuerza 496 de 1008
  (`results/measurements.tsv:32`), y de los 40320 ordenes de palacios posibles,
  todos con la misma clausura, solo 464 dan el valor esperado
  (`results/measurements.tsv:95` a `:97`). La coincidencia de la cifra no basta,
  y por eso aqui no se dice.
- El criterio de refutacion que la seccion (b) declaro resulta ser inservible.
  Pedia exhibir un hexagrama de la construccion cuya imagen bajo complementacion
  no perteneciese a la construccion. Como toda ordenacion contiene los 64
  hexagramas, su imagen bajo complementacion es siempre el mismo conjunto: el
  criterio no lo podia fallar ninguna secuencia, ni esta ni otra. Queda
  registrado como defecto de la preinscripcion, no como prediccion superada.

## 5. Seccion (c), King Wen: la cifra y la simetria

### La cifra

1013 (`results/measurements.tsv:19`, `:20`), bajo las dos convenciones con yang
como uno, con las dos orientaciones. Con yang como cero, 1003
(`results/measurements.tsv:21`, `:22`), que es 2016 menos 1013, la misma medida
leida contra el orden binario invertido.

La discrepancia de la seccion (c) queda resuelta asi: la cifra que existe es
1013. La otra cifra en circulacion, 1017, no aparece bajo ninguna de las cuatro
convenciones fijadas, ni como recuento ni como su complemento a 2016. No se
apostaba por ninguna de las dos y no se apuesta ahora: se reporta lo medido.
De donde salio 1017 es una pregunta sobre los registros del proyecto, no sobre
esta secuencia, y este repositorio no la responde.

### Que simetria falta

Ninguna, y ese es el resultado.

Primero, la busqueda no necesita ser ciega. La unica biyeccion que invierte un
orden total finito es la que manda el elemento de rango r al de rango n-1-r, y
sobre los hexagramas, con cualquiera de las cuatro convenciones, esa biyeccion
es exactamente la complementacion. Luego solo hay una candidata.

Segundo, la construccion de King Wen la respeta. Los 32 pares adyacentes
(`results/measurements.tsv:51`) van bajo complementacion a pares adyacentes, los
32 de 32 (`results/measurements.tsv:55`), con cero testigos en contra
(`results/measurements.tsv:56`). Y esto tambien se demuestra sin mirar la
secuencia: los pares son las 28 orbitas de tamano dos del giro de media vuelta
(`results/measurements.tsv:57`) mas los 4 pares que forman por complementacion
los 8 hexagramas que el giro deja quietos (`results/measurements.tsv:58`), las
dos familias agotan los 32 pares (`results/measurements.tsv:59`), y el giro y la
complementacion conmutan (`results/measurements.tsv:60`).

Tercero, la busqueda se hizo igualmente, y queda documentada. Familia recorrida:
toda aplicacion que permuta las seis lineas y luego complementa un subconjunto
de ellas, 46080 en total (`results/measurements.tsv:61`), de las cuales 1384 son
involuciones (`results/measurements.tsv:62`). Invierten el orden binario: 1
(`results/measurements.tsv:63`). Las respeta la construccion de King Wen: 112
(`results/measurements.tsv:64`). Cumplen las dos cosas: 1
(`results/measurements.tsv:65`), y esa una es la complementacion, exhibida como
permutacion de lineas identidad con mascara de complementacion completa
(`results/permutations.txt:82`).

Limite declarado de esta busqueda: cubre las involuciones que actuan
reordenando y complementando lineas. No cubre involuciones arbitrarias del
conjunto de los 64 hexagramas, que son demasiadas para enumerar. Para la
pregunta concreta esa limitacion no muerde, porque el argumento de unicidad de
arriba ya deja una sola candidata posible fuera de cualquier familia.

Conclusion de la seccion: la diferencia entre King Wen y las otras dos no es una
simetria ausente. La involucion esta, y esta respetada. Lo que cambia es el
tamano de la clase que la clausura deja libre, 642 frente a 1048 y 1024, y que
en King Wen esa clase no se parte por la mitad: 326 frente a 321, exceso de 5
(`results/measurements.tsv:40` a `:43`). El giro de media vuelta, que la
construccion tambien respeta, no invierte el orden binario y por tanto no fuerza
nada; el testigo esta en `results/permutations.txt:74` a `:76`.

## 6. Control

Semilla congelada y declarada: 20260809 (`results/measurements.tsv:66`), fijada
como constante en `src/measure.py`. Repeticiones por variante: 100000
(`results/measurements.tsv:67`). Cada repeticion construye la ordenacion con
ordenes de familia sorteados y cuenta sus inversiones contra el orden binario.
En las 1000 primeras repeticiones de cada variante se comprobo ademas que la
clausura sigue intacta, es decir que el complemento sigue mandando bloque entero
sobre bloque entero (`results/measurements.tsv:73`, `:79`, `:85`, `:91`).

| variante | aciertos | tasa | recuentos distintos | minimo | maximo | origen |
|---|---|---|---|---|---|---|
| octetos, orden de familia | 9623 | 0.09623 | 29 | 896 | 1120 | `results/measurements.tsv:68` a `:72` |
| octetos, orden interno | 9573 | 0.09573 | 28 | 924 | 1086 | `results/measurements.tsv:74` a `:78` |
| octetos, los dos ordenes | 1960 | 0.01960 | 154 | 854 | 1176 | `results/measurements.tsv:80` a `:84` |
| palacios, orden de familia | 1187 | 0.01187 | 292 | 704 | 1320 | `results/measurements.tsv:86` a `:90` |

Acierto quiere decir caer exactamente en 1008, el valor esperado por azar.

Como el espacio de ordenes de familia es pequeno, se enumero entero y la tasa
deja de ser una estimacion:

| variante | ordenes | aciertos | tasa | origen |
|---|---|---|---|---|
| octetos, orden de familia | 40320 | 3836 | 0.09514 | `results/measurements.tsv:92` a `:94` |
| palacios, orden de familia | 40320 | 464 | 0.01151 | `results/measurements.tsv:95` a `:97` |

Lo que el control establece: la clausura bajo complementacion sobrevive a
barajar el orden de familia, y el recuento no. Caer en el valor esperado ocurre
en menos de una de cada diez reordenaciones de los octetos y en poco mas de una
de cada cien de los palacios. Las dos ordenaciones historicas caen ahi; la
clausura, por si sola, no explica que caigan.

## 7. Lo que este informe no dice

- No dice que nada de esto sea nuevo. La revision de antecedentes no ha
  empezado. Es perfectamente posible que todo lo anterior este publicado.
- No dice por que la clase libre se parte exactamente por la mitad en Mawangdui
  y en Jing Fang. Eso queda medido y sin explicar.
- No dice de donde salio la cifra 1017.
- No dice nada sobre las otras propiedades de las tres secuencias. Solo se midio
  el recuento de inversiones contra el orden binario, con el denominador y las
  convenciones fijados de antemano.

## Reproducir

    git --git-dir=<fuente>/.git archive --format=tar zenodo-v3 | tar -x -C _source/zenodo-v3
    python tools/extract_sequences.py
    python src/measure.py

La ejecucion es determinista: la unica fuente de azar es la semilla declarada.
