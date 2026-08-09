# Informe: el grupo completo

Continuacion de INFORME.md. Las definiciones estan en DEFINICIONES-GRUPO.md,
commiteadas antes de esta ejecucion. Todas las cifras salen de una sola
ejecucion de `src/group.py` y se citan con fichero y linea. Sin afirmaciones de
novedad: la revision de antecedentes sigue sin empezar.

La pregunta que quedo abierta era si la diferencia entre las tres
construcciones vive en el grupo entero de simetrias respetadas, y no en la sola
complementacion. La respuesta es que si, y que separa las tres de una manera que
no se veia con una involucion suelta.

## 1. Los tres grupos

Familia recorrida entera: 46080 aplicaciones afines
(`results/group-measurements.tsv:4`).

| construccion | bloques | R1 | R2 | contiene el complemento | contiene el giro |
|---|---|---|---|---|---|
| Mawangdui | 8 octetos | 2304 | 1 | si | no |
| Jing Fang | 8 palacios | 8 | 8 | si | no |
| King Wen | 32 pares | 384 | 1 | si | si |

Ordenes: `results/group-measurements.tsv:5`, `:7`, `:13`, `:15`, `:21`, `:23`.
Complemento y giro: `:9`, `:11`, `:17`, `:19`, `:25`, `:27`.

Generadores exhibidos en `results/group-structure.txt:5` a `:43`. Y ademas cada
grupo admite una descripcion cerrada, comprobada elemento a elemento contra la
enumeracion:

- **Mawangdui.** R1 es exactamente el conjunto de aplicaciones que permutan
  lineas dentro del trigrama inferior y dentro del superior, con cualquier
  mascara. Orden 6 por 6 por 64 igual a 2304, y coincide con lo enumerado
  (`results/group-measurements.tsv:263`, `:264`). El motivo es que sus bloques
  son los ocho conjuntos de hexagramas con un trigrama superior dado, la
  particion mas simetrica de las tres.
- **Jing Fang.** R1 es exactamente el conjunto de aplicaciones que no mueven
  ninguna linea y complementan la misma linea en los dos trigramas. Orden 8, y
  coincide (`results/group-measurements.tsv:265`, `:266`). Es el grupo mas
  pequeno de los tres.
- **King Wen.** R1 resulta ser exactamente el centralizador del giro de media
  vuelta dentro de la familia afin: todos sus elementos conmutan con el giro, y
  no hay ningun otro que lo haga (`results/group-measurements.tsv:267`, `:268`,
  `:269`). Era de esperar, porque sus bloques son las orbitas del giro, pero
  aqui queda medido en vez de supuesto.

Continuidad con el commit anterior: alli se contaron 112 involuciones que la
construccion de King Wen respeta. Aqui salen 111
(`results/group-measurements.tsv:28`), y la diferencia es la identidad, que
ahora se excluye del recuento. Las dos cifras dicen lo mismo.

R2, que exige ademas conservar el indice dentro del bloque, es el grupo trivial
en Mawangdui y en King Wen, y coincide con R1 en Jing Fang. Es decir que solo
Jing Fang respeta sus simetrias posicion a posicion.

## 2. La contabilidad por orbitas

Con el grupo generado solo por la identidad y la complementacion, la
contabilidad reproduce exactamente las cifras del commit anterior, que era la
comprobacion declarada de que el aparato nuevo no se ha desviado:

| secuencia | orbitas forzadas | aportacion forzada | aportacion libre observada | anchura | origen |
|---|---|---|---|---|---|
| Mawangdui | 484 | 484 | 524 | 1048 | `results/group-measurements.tsv:31`, `:34`, `:35`, `:39` |
| Jing Fang | 496 | 496 | 512 | 1024 | `:88`, `:91`, `:92`, `:96` |
| King Wen | 687 | 687 | 326 | 642 | `:145`, `:148`, `:149`, `:153` |

Con el grupo entero R1 la imagen cambia por completo:

| secuencia | orbitas | forzadas | libres | intervalo | anchura | observado | fuerza el empate |
|---|---|---|---|---|---|---|---|
| Mawangdui | 15 | 15 | 0 | [1008, 1008] | 0 | 1008 | si |
| Jing Fang | 280 | 280 | 0 | [1008, 1008] | 0 | 1008 | si |
| King Wen | 36 | 17 | 19 | [957, 1059] | 102 | 1013 | no |

Origen: Mawangdui `results/group-measurements.tsv:49` a `:66`; Jing Fang `:106`
a `:123`; King Wen `:163` a `:180`. La relacion epsilon se comprobo ademas
elemento a elemento sobre el grupo, no solo sobre los generadores: 929376
comprobaciones en Mawangdui sobre una muestra de 461 elementos de 2304 por
coste, 16128 sobre los 8 de Jing Fang, y 774144 sobre los 384 de King Wen
(`:67`, `:124`, `:181`).

**Respuesta a la pregunta 2 del encargo.** En Mawangdui y en Jing Fang el grupo
reduce la clase libre a cero: no aprieta hasta 1008, lo fuerza. En King Wen
quedan 19 orbitas libres y una anchura de 102, y el exceso de 5 cabe dentro de
esa holgura.

### Un lema que conviene tener a mano

Si todas las orbitas quedan forzadas, cada una aporta la mitad de su tamano, y
la suma de los tamanos es C(64,2). Luego el total es forzosamente la mitad de
C(64,2). Es decir: el grupo solo puede forzar el empate; nunca puede forzar otro
valor. Determinar el recuento y dar 1008 son la misma cosa. El programa lo
comprueba en cada caso antes de escribir nada.

## 3. King Wen: el grupo no fuerza el empate, y ademas lo prohibe

Esto es mas fuerte que un resultado negativo, y conviene no confundirlo con uno.

Las 36 orbitas de King Wen tienen todas tamano par
(`results/group-measurements.tsv:166`). Cada orbita libre aporta uno de dos
valores que difieren en un numero par. Luego todos los totales compatibles con
la estructura tienen la misma paridad. Son 52
(`results/group-measurements.tsv:174`), todos impares
(`:176`, `:177`), y 1008 no esta entre ellos (`:175`). El compatible mas cercano
al empate es 1007, a distancia 1 (`:178`, `:179`).

Dicho de otro modo: para King Wen, el empate exacto no esta descartado por
poco, esta descartado por paridad. El grupo explica por que el exceso no es
cero. No explica por que es 5.

## 4. R2, y por que casi no dice nada

R2 es trivial en Mawangdui y en King Wen, orden 1
(`results/group-measurements.tsv:7`, `:23`). Con el grupo trivial no hay
orbitas que junten pares, la contabilidad degenera en 2016 orbitas de un
elemento y el intervalo es [0, 2016] (`:74`, `:75`, `:188`, `:189`). No fuerza
nada, y no puede.

En Jing Fang R2 coincide con R1 y por tanto fuerza igual: intervalo
[1008, 1008] (`results/group-measurements.tsv:131`, `:132`, `:134`). Jing Fang
es la unica de las tres cuya simetria respeta el lugar dentro del bloque, no
solo el bloque.

## 5. Control: el grupo solo, sin el orden historico, no basta

El grupo R1 depende unicamente de la particion en bloques, y barajar el orden de
familia no cambia esa particion. Comprobado: en 300 de 300 barajados el grupo R1
sale identico al historico, en octetos y en palacios
(`results/group-measurements.tsv:203`, `:209`). Semilla 20260809, la misma ya
congelada en el commit anterior (`:201`); 300 repeticiones, que son una muestra
de los 40320 ordenes y no una enumeracion, porque la contabilidad por orbitas es
cara (`:202`).

| variante | el grupo fuerza un valor | recuento observado igual al esperado | anchuras distintas | anchura maxima |
|---|---|---|---|---|
| octetos | 8 de 300 | 27 de 300 | 12 | 176 |
| palacios | 0 de 300 | 3 de 300 | 84 | 952 |

Origen: `results/group-measurements.tsv:204` a `:208` y `:210` a `:214`.

Tres lecturas:

1. El mismo grupo, con otro orden de familia, casi nunca fuerza nada. Luego lo
   que fuerza el empate en Mawangdui y en Jing Fang no es el grupo por si solo,
   sino el grupo junto con el orden de familia recibido.
2. Forzar es mas raro que acertar. En octetos, 8 ordenes fuerzan y 27 dan 1008;
   en palacios, 0 fuerzan y 3 dan 1008. Los dos ordenes historicos caen en la
   clase estrecha, no en la ancha. Las tasas de acierto, 27 y 3 sobre 300,
   concuerdan con las del commit anterior, que eran exactas sobre los 40320
   ordenes: 0.09514 y 0.01151.
3. Cuando fuerza, fuerza 1008 y nada mas, que es el lema de la seccion 2, no un
   hallazgo del control.

## 6. Las cuatro convenciones

Bajo R1, el intervalo no depende de la convencion. Mawangdui y Jing Fang dan
[1008, 1008] con cero orbitas libres en las cuatro
(`results/group-measurements.tsv:215` a `:246`). King Wen da [957, 1059] con 19
orbitas libres en las cuatro, con observado 1013 en las dos de yang como uno y
1003 en las dos de yang como cero (`:247` a `:262`). Las dos cifras de King Wen
son impares, como exige la paridad forzada de la seccion 3.

## 7. Que queda acotado, y que no

**Lo que este tramo establece.** Para las dos construcciones que empatan, el
grupo afin que respetan, junto con su orden de familia recibido, determina el
recuento por completo. Para King Wen, el mismo tipo de estructura determina la
paridad y un intervalo de anchura 102, y prohibe el empate.

**Donde NO vive la explicacion del exceso de 5.** No vive en la familia afin.
Se enumeraron sus 46080 elementos, se tomo el subgrupo entero que la
construccion respeta, y queda holgura de sobra para 52 totales distintos. Ningun
refinamiento dentro de esta familia va a fijar el 5.

**Limites, los mismos declarados antes de medir y uno mas que conviene decir en
voz alta.**

- La familia afin no agota las biyecciones de los 64 hexagramas.
- La particion en bloques es la que da cada construccion; otra manera de trocear
  daria otro grupo.
- La contabilidad no deriva el recuento desde cero. El bit epsilon depende de la
  secuencia a traves del orden de las posiciones, asi que el aparato mide que
  parte del recuento queda determinada por las relaciones de simetria una vez
  puesta la secuencia, no que parte se podria haber predicho sin ella. El
  control de la seccion 5 esta precisamente para que ese limite no se lea de
  mas.
- Nada de esto se afirma como nuevo. La revision de antecedentes no ha empezado.

## Reproducir

    python src/measure.py
    python src/group.py

Deterministas las dos. La unica fuente de azar es la semilla declarada.
