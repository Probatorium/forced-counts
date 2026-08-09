# El instrumento de registro de esfuerzo

Este directorio contiene el mecanismo que EFFORT.md declaro en el commit raiz.
El commit raiz declaro que se iba a registrar; este commit crea con que.

## Piezas

- `log.jsonl`: el registro. Una linea JSON por evento, en orden de aparicion.
- `classification.tsv`: la clase de cada fichero del repositorio, aparato o
  analisis, con su origen y su motivo.
- `../tools/effort.py`: la unica via por la que se escribe en el registro.

## Append only, y por que es comprobable

Cada registro guarda el campo `prev`, que es el sha256 del registro anterior, y
su propio `hash`, que es el sha256 de su contenido. Editar una linea antigua
cambia su hash y rompe el `prev` de todas las siguientes.

    python tools/effort.py verify

recorre la cadena y falla si alguna linea fue tocada, si falta un eslabon, si
un `seq` no coincide con su posicion, o si hay sesiones abiertas anidadas o
cierres sin apertura. Ninguna orden de la herramienta reescribe ni borra: solo
anaden linea al final.

Esto no impide fisicamente una reescritura completa del fichero y de la cadena
entera. Lo que hace es que una reescritura parcial y silenciosa deje huella, y
que una reescritura total tenga que ser deliberada y quede en la historia de
git.

## Eventos

- `session_open` y `session_close`: apertura y cierre de sesion, con actor,
  decisor y nota. Los dos llevan `live: true`.
- `retroactive`: entrada reconstruida. Lleva `live: false` y un `caveat` fijo
  que dice que un registro reconstruido no equivale a uno tomado en vivo.
- `note`, `decision`, `dead_end`, `provenance`: anotaciones dentro de sesion.
  Un callejon sin salida es esfuerzo real y por eso tiene evento propio.
- `classification`: instantanea del reparto de lineas entre aparato y analisis
  en el momento de tomarla.

Cada registro guarda ademas el `head` de git y si el arbol estaba sucio en ese
instante, para poder situar el evento en la historia sin depender de la memoria
de nadie.

## Cuentas de linea

`classify` exige que todo fichero presente este declarado en
`classification.tsv` y falla si aparece uno sin clasificar. Separa ademas lo
propio de lo extraido, para que lineas traidas de fuera no inflen la cuenta de
analisis escrito aqui.

Una advertencia de lectura: el recuento de `log.jsonl` que aparece dentro de un
evento `classification` es el previo a escribir ese mismo evento. El
instrumento no puede medirse a si mismo despues de crecer.
