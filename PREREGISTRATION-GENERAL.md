# PREINSCRIPCION DE LA FASE GENERAL

Mismo contrato que el commit raiz. Este documento se escribe **antes de computar
nada del paisaje general**, y su commit no contiene ninguna medicion de ese
paisaje. Es **texto firmado y no se enmienda**: lo que aqui quede mal escrito se
queda mal escrito, y se corrige por documento nuevo, nunca editando este.

Autorizacion de apertura de la fase: Alexis, en la sesion que produce este
commit. En la sesion anterior la misma apertura se pidio y se denego, y esa
denegacion tambien esta en el registro de esfuerzo.

Las cuatro secciones siguientes tienen estatus epistemico distinto y estan
rotuladas para que no se confundan despues.

---

## (a) LA PREGUNTA, fijada

**Para que subgrupos G del grupo hiperoctaedrico B_n, actuando sobre
ordenaciones de los 2^n vertices del n-cubo, y bajo que condiciones sobre la
ordenacion, el recuento de pares discordantes contra el orden binario queda**

1. **forzado al empate**, es decir determinado y con valor C(2^n, 2) partido por
   dos;
2. **acotado en un intervalo** de totales compatibles, sin quedar determinado;
3. **prohibido en el empate por paridad**, es decir con el valor central fuera
   del conjunto de totales compatibles.

Esas son las tres casillas. La pregunta es que las decide.

Se fija tambien que la respuesta buscada es una **clasificacion**, no un
teorema suelto: que se pueda decir, dado el par formado por el grupo y la
ordenacion, en cual de las tres casillas cae, y por que.

Nomenclatura, por la decision registrada en PRIOR-ART.md 11: el estadistico se
llama **pares discordantes**, y es el inversion number en sentido combinatorio.

---

## (b) RESULTADO PREVIO, NO ES PREDICCION

Todo lo de esta seccion **ya esta demostrado antes de firmar**. No se apunta
ningun credito predictivo por nada de ello, y donde se verifique mas adelante,
se reportara como verificacion y no como hallazgo.

### b.1 Los Lemas 0 a 3 no dependen de la dimension

Los cuatro lemas de PROOFS.md pieza 1 estan demostrados para n = 6 sin usar en
ningun paso que n valga 6. Con N igual a 2^n en lugar de 64 y C(N,2) en lugar de
C(64,2), los enunciados y sus demostraciones valen igual:

- **Lema 0**, relacion de estado: estado del par imagen igual a estado del par
  mas A mas B, con A el bit de si la permutacion de posiciones invierte el orden
  del par y B el de si la aplicacion invierte el orden binario de sus dos
  vertices.
- **Lema 0b**, cocadena, y su consecuencia: encadenar elementos del grupo no
  llega mas lejos que un solo elemento, porque la cadena compone en un elemento
  y los epsilon se acumulan en el suyo.
- **Lema 1**, el lema del empate: si toda orbita esta forzada, el total es
  C(N,2) partido por dos. Y su corolario: un grupo solo puede forzar el empate,
  nunca otro valor.
- **Lema 2**, criterio de orbita forzada por testigo uniforme.
- **Lema 3**, forzado por emparejamiento, con testigo posiblemente distinto en
  cada pareja.

### b.2 La obstruccion de paridad general, con sus hipotesis ya depuradas

**Teorema.** Sea G un subgrupo de B_n actuando sobre F_2^n. Si G contiene las
traslaciones por un subespacio V de F_2^n con **dim V al menos 2**, entonces
**toda orbita de G sobre pares no ordenados tiene cardinal par**.

**Corolario.** Bajo esa hipotesis, las dos opciones de aportacion de cada orbita
tienen la misma paridad, luego el recuento total es congruente modulo dos con la
suma de los c de cada orbita, **sea cual sea la eleccion de los bits libres**. La
paridad del recuento queda determinada por la estructura.

La formulacion de PROOFS.md 3.3 pedia **tres** hipotesis: que T fuesen las
traslaciones por un subespacio contenido en G, que T fuese normal en G, y que la
dimension fuese al menos dos. La fase previa a esta firma decidio las dos que
estaban en duda, y por eso el teorema de arriba solo pide dos:

- **La normalidad es redundante y se elimina. DEMOSTRADO.** Si G contiene las
  traslaciones por V, entonces contiene tambien las traslaciones por W, el span
  de todas las imagenes de V bajo las partes lineales de G, porque los
  conjugados de una traslacion son traslaciones y los productos de traslaciones
  son traslaciones. Ese W es invariante bajo las partes lineales por
  construccion, luego sus traslaciones si son normales en G, y su dimension es
  al menos la de V. El teorema se aplica entonces con W en lugar de V.
- **La dimension al menos dos NO se puede eliminar. DEMOSTRADO por testigo.**
  Tomese G igual al grupo de dos elementos formado por la identidad y la
  traslacion por un vector v no nulo. Cumple las otras hipotesis: son
  traslaciones por un subespacio contenido en G, actuan libremente, y T es
  normal en G por ser G abeliano. Y la conclusion falla: el par formado por
  cualquier vertice x y por x mas v queda fijo, luego su orbita tiene cardinal
  1, que es impar.

Registro de la fase previa: `src/parity_hypotheses.py`, salida en
`results/parity-hypotheses.tsv`, commiteado **antes** que este documento. Alli
estan el testigo exhibido para n igual a 2, 3 y 4, la comprobacion de que en el
caso no normal la conclusion se mantiene por paso al cierre normal, y 50 casos
declarados sin ninguna orbita impar.

### b.3 Los tamanos de orbita no dependen de la ordenacion

**DEMOSTRADO y comprobado.** La accion sobre pares de posiciones es conjugada
por sigma de la accion sobre pares de vertices, luego los cardinales de las
orbitas son los mismos. Toda la discusion de paridad es por tanto independiente
de la ordenacion, y solo depende del grupo. Lo que si depende de la ordenacion
es el bit epsilon, y con el el reparto entre parte forzada y parte libre.

### b.4 El analogo de Mawangdui a n igual a 2m

**DEMOSTRADO**, por el mismo argumento de PROOFS.md 2.1 con las constantes
cambiadas. Si los bloques son las fibras de las m coordenadas altas, es decir
las clases laterales del subespacio V generado por las m coordenadas bajas,
entonces el grupo que respeta esa particion es el conjunto de las aplicaciones
cuya parte lineal deja V invariante, con cualquier mascara, y su orden es
**m! por m! por 2^n**. La verificacion mecanica de esa cifra se hara en la fase
de medicion; el argumento no la necesita.

### b.5 Los totales compatibles forman una progresion de paso dos

**DEMOSTRADO.** Bajo la hipotesis de b.2 todas las orbitas tienen cardinal par,
luego el hueco de cada orbita libre, el valor absoluto del cardinal menos dos
veces c, es par, y el conjunto de totales compatibles es el minimo mas sumas de
huecos pares. Todos comparten paridad y estan separados por multiplos de dos.

### b.6 Los tres desenlaces de n igual a 6

Se recuerdan aqui como resultado previo, no como prediccion sobre nada:
Mawangdui y Jing Fang con el empate forzado y demostrado; King Wen con
intervalo de 957 a 1059, 52 totales compatibles y el empate prohibido por
paridad; y el codigo de Gray reflejado, como ordenacion de comparacion, sin
forzado en ninguno de los cinco niveles de su torre de particiones.

---

## (c) PREDICCIONES

### c.1 La casilla de predicciones sobre las hipotesis queda VACIA, y se dice por que

El diseno de esta fase preveia una prediccion por cada hipotesis de la
obstruccion de paridad que siguiera sin decidir, cada una sobre un espacio
enumerable declarado. **No queda ninguna.** Las dos que estaban en duda se
decidieron por demostracion en la fase previa, y estan en b.2 con su registro:
la normalidad resulto redundante y la dimension al menos dos resulto necesaria
por testigo directo.

Se deja constancia de la tentacion evitada: se podria haber fabricado una
prediccion restringiendo el espacio hasta que la respuesta volviese a ser
desconocida. Eso no es predecir, es escoger la pregunta despues de ver la
respuesta, y no se hace.

### c.2 Lo que se declara SIN PREDICCION, con la razon escrita

**No se apuesta por nada de esto.** La ausencia de prediccion es deliberada y
queda registrada aqui para que no se pueda reclamar despues un acierto que no se
enuncio.

- **Si el empate queda forzado para los analogos de las construcciones
  historicas a n general.** Razon: en n igual a 6 el forzado dependia del orden
  de familia recibido, no solo del grupo, y el control midio que entre las
  reordenaciones es poco frecuente. Para n general no hay orden recibido, asi
  que la pregunta se convierte en otra, la de que da una eleccion canonica, y no
  hay base para apostar.
- **La forma de la clasificacion**, es decir que combinaciones de grupo y
  ordenacion caen en cada una de las tres casillas de (a). Razon: es exactamente
  lo que la medicion tiene que ensenar. Predecirla antes de mirar seria
  inventarla.
- **La monotonia del intervalo respecto del orden del grupo.** Razon: no hay ni
  un caso fuera de n igual a 6, y con un solo punto no se conjetura una
  tendencia.

### c.3 Que contaria como refutacion de lo que si se afirma

Lo unico que se afirma en firme esta en (b) y es demostrado, asi que su
refutacion es la ordinaria de un teorema: exhibir un contraejemplo. En concreto,
para el teorema de b.2, exhibir un subgrupo G de algun B_n que contenga las
traslaciones por un subespacio de dimension al menos dos y tenga una orbita de
pares de cardinal impar. Si aparece, el teorema es falso y se dira, sin
reinterpretarlo para salvarlo.

---

## (d) CONVENCIONES, fijadas ahora

- **n es variable.** Todo enunciado dice de que n habla. Donde no se diga, es
  general.
- **Cuatro convenciones de bits por dimension**, las mismas de
  PREREGISTRATION.md trasladadas a n lineas: yang como uno o como cero, cruzado
  con la linea inferior como bit mas significativo o como menos significativo.
  Se reportan siempre las cuatro, no solo la mas favorable.
- **Denominador C(2^n, 2)** para toda tasa. Y el valor central, el del empate,
  es C(2^n, 2) partido por dos.
- **Unidad de conteo:** un par discordante es un par no ordenado de posiciones
  distintas cuyo orden relativo en la ordenacion es contrario a su orden
  relativo bajo el orden binario de la convencion en uso.
- **Nocion de respetar:** la R1 de DEFINICIONES-GRUPO.md, trasladada a n. Una
  aplicacion respeta una construccion cuando manda cada bloque entero sobre un
  bloque entero. Si en algun momento se usa la R2, se dira.
- **Las construcciones analogas que se vayan a medir se declaran antes de
  correr nada**, en documento propio y en commit anterior al de la medicion,
  igual que se hizo con DEFINICIONES-GRUPO.md.
- **Muestreos con semilla congelada y declarada** donde el espacio no se pueda
  enumerar. Donde se pueda, se enumera y se dice que se enumero.

---

## Revision de antecedentes

**Se hereda la hecha, y sigue ABIERTA.** PRIOR-ART.md cubre ya el territorio de
la homomesia, que es donde vive la parte general de este trabajo: la Definicion
1 y la seccion 2.1 de Propp y Roby, y el survey de Roby con su seccion 2.1 sobre
acciones de grupos generales y su lema de que la homomesia sube de un subgrupo
al grupo. Nada de lo que se mida en esta fase se afirmara nuevo mientras la
revision siga abierta.

**Todo termino nuevo pasa por la puerta de la revision antes de fijarse**, con
la regla de la seccion 11 de PRIOR-ART.md: si el termino ya tiene dueno, se cita
y no se presenta como propio.
