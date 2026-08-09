# INSTRUMENTACION DEL ESFUERZO

Este repositorio nace instrumentado a proposito, desde el minuto uno, es decir
desde este commit raiz. La instrumentacion no se anade despues ni se reconstruye
de memoria: empieza antes de que exista una sola linea de analisis.

## Por que

Por la conclusion del estudio de esfuerzo de Stasis: el esfuerzo no se puede
reconstruir a posteriori sin contaminarlo. Cuando se intenta reconstruir, lo que
se obtiene es una racionalizacion del recorrido, no el recorrido.

## Que se va a registrar

**Marcas de tiempo de sesion.**

- Apertura y cierre de cada sesion de trabajo.
- Los sellos temporales de cada commit, que quedan en la propia historia de git
  y no se reescriben.
- Interrupciones largas dentro de una sesion, cuando las haya, anotadas como
  tales.

**Lineas de aparato frente a lineas de analisis.**

- Lineas de aparato: infraestructura, formato, empaquetado, documentacion de
  proceso, verificacion, scripts de conveniencia, tooling.
- Lineas de analisis: lo que produce o transforma resultados sobre el objeto de
  estudio.
- Se cuentan por separado y se registra el reparto en cada corte, para que la
  proporcion entre ambas sea observable en vez de anecdotica.

**Quien escribio que.**

- Atribucion por bloque de trabajo entre autor humano y asistente automatico.
- Se registra tambien quien decidio, que no siempre coincide con quien tecleo.
- La atribucion se anota en el momento, no al final.

**Callejones sin salida.**

- Intentos abandonados, con el motivo del abandono. Un intento descartado es
  esfuerzo real y se contabiliza como tal.

## Alcance declarado

Los datos de esfuerzo se acumulan. NO se declara ninguna relacion entre este
registro y el paper de Stasis. Su uso, si lo hay, se decide despues, y esa
decision quedara escrita con su fecha cuando se tome.

Esta seccion existe para impedir la lectura contraria: que la instrumentacion
se presente mas tarde como si hubiera sido disenada desde el principio para un
destino concreto que en realidad no estaba fijado.
