# PREINSCRIPCION

Este documento se escribe en el commit raiz de este repositorio, antes de
ejecutar nada. El commit raiz no contiene codigo de analisis, ni datos, ni
cifras medidas. Su unica funcion es dejar fijado por escrito, y con sello
temporal de version, que se afirma antes de medir y que no.

Las tres secciones siguientes tienen estatus epistemico distinto y estan
rotuladas para que no se confundan despues.

---

## (a) RESULTADO PREVIO, NO ES PREDICCION

**Enunciado.** El recuento de inversiones de la ordenacion de Mawangdui contra
el orden binario esta forzado por la clausura de su construccion bajo
complementacion. No es una regularidad empirica que se descubra al contar: es
una consecuencia de como esta construida la secuencia.

**Argumento.**

- El orden binario es un orden total sobre los hexagramas, inducido por la
  lectura de sus lineas como bits bajo una convencion fijada.
- La construccion de Mawangdui esta cerrada bajo complementacion: la imagen de
  cualquier hexagrama de la construccion al intercambiar yang por yin vuelve a
  pertenecer a la construccion.
- La complementacion invierte el orden binario: si un hexagrama precede a otro
  en el orden binario, sus complementos aparecen en el orden contrario.
- Al estar la construccion cerrada bajo una operacion que invierte el orden de
  comparacion, la contabilidad de pares concordantes y discordantes contra el
  orden binario queda determinada por la propia clausura, y no por una eleccion
  historica libre de quien fijo la secuencia. El recuento sale forzado.

**Estatus.** Este argumento fue obtenido ANTES de abrir este repositorio. No se
declara aqui como prediccion. Si en este repositorio se verifica, esa
verificacion es RETRODICCION y se reportara con esa etiqueta, sin credito
predictivo de ningun tipo.

---

## (b) PREDICCION, SIN MEDIR

**Enunciado.** La construccion de Jing Fang admite la misma clausura bajo
complementacion, y por tanto su recuento de inversiones contra el orden binario
queda igualmente forzado, por el mismo argumento de la seccion (a).

**Estatus.** Se declara ANTES de ejecutar nada. En el momento de escribir este
documento no se ha medido, ni en este repositorio ni fuera de el, el recuento de
Jing Fang. No se adelanta ninguna cifra.

**Que contaria como refutacion.** Exhibir un hexagrama de la construccion de
Jing Fang cuya imagen bajo complementacion no pertenezca a la construccion. Un
solo caso asi rompe la clausura y con ella la prediccion. Si aparece, se
reportara como refutacion y no se reinterpretara la prediccion para salvarla.

---

## (c) SIN PREDICCION, DISCREPANCIA ABIERTA

**Enunciado.** El recuento de inversiones de la secuencia de King Wen contra el
orden binario esta sin resolver en este repositorio.

**Estado de la discrepancia.** En los registros del proyecto circulan dos
cifras, 1013 y 1017. Ninguna de las dos ha sido medida en este repositorio.

**Estatus.** NO se apuesta por ninguna de las dos. No hay prediccion en esta
seccion, y la ausencia de prediccion es deliberada y queda registrada aqui para
que no se pueda reclamar despues un acierto que no se enuncio. La discrepancia
se resolvera por medicion dentro de este repositorio, bajo las convenciones
fijadas mas abajo, y la cifra que salga es la que existe. Si la medicion no
coincide con ninguna de las dos cifras en circulacion, eso mismo es el
resultado, y se reportara asi.

---

## CONVENCIONES FIJADAS AHORA

Se fijan en este commit raiz, antes de cualquier ejecucion, para que la eleccion
no pueda hacerse despues de ver resultados.

**Convenciones de bits que se van a probar.** Se probaran las cuatro que
resultan de cruzar polaridad y orientacion, y se reportaran las cuatro siempre,
no solo la que resulte mas favorable:

- yang como uno y yin como cero, con la linea inferior como bit mas
  significativo.
- yang como uno y yin como cero, con la linea inferior como bit menos
  significativo.
- yang como cero y yin como uno, con la linea inferior como bit mas
  significativo.
- yang como cero y yin como uno, con la linea inferior como bit menos
  significativo.

**Unidad de recuento.** Una inversion es un par no ordenado de hexagramas
distintos de la secuencia cuyo orden relativo en la secuencia es contrario a su
orden relativo bajo el orden binario de la convencion en uso.

**Denominador.** C(64,2), el numero de pares no ordenados de hexagramas
distintos. Toda tasa de inversiones que se publique en este repositorio usara
ese denominador y ningun otro.

**Enmiendas.** Cualquier cambio posterior a estas convenciones no se hara
editando esta seccion en silencio. Se anadira como enmienda, con su motivo y
con el commit en el que se introduce, y quedara visible que se introdujo
despues del commit raiz.
