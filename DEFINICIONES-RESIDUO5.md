# El residuo de 5: lista cerrada de estructuras candidatas

**Fase 0.** Este fichero se escribe y se commitea **antes de medir nada**. La
lista de abajo es **cerrada**: en el commit de la medicion no se prueba ninguna
estructura que no este aqui. Si despues aparece otra, entra en documento nuevo y
en commit posterior, y se vera en la historia que entro despues.

No enmienda ningun texto firmado.

## El objeto

King Wen da 1013 pares discordantes contra el orden binario, y el empate es 1008.
El grupo que su construccion respeta, de orden 384, deja 19 orbitas libres y un
intervalo de 957 a 1059. La desviacion de 5 vive entera en esa clase libre y no
esta explicada. El objetivo de este tramo es **convertir el 5 en anatomia o en
frontera declarada**.

## La lista cerrada

### A1. Hexagramas nucleares, hu gua

**Definicion exacta que se va a usar**, fijada aqui para que no se pueda cambiar
despues: numerando las lineas de 1, la inferior, a 6, la superior, el nuclear de
un hexagrama tiene por **trigrama inferior las lineas 2, 3 y 4** y por **trigrama
superior las lineas 3, 4 y 5**.

**Fuente de la definicion:** es la operacion clasica, y la forma concreta que se
usa aqui es la del paquete de replicacion leido en la etiqueta `zenodo-v3`, donde
aparece como `nuclear(v)` tomando `b[1:4]` y `b[2:5]` de la cadena de seis bits
con la linea 1 primera. La operacion **no es biyectiva**, asi que no aporta
ningun elemento de grupo; aporta la **particion por fibras** y el rasgo binario
"los dos hexagramas de un par tienen el mismo nuclear".

### A2. La division en dos mitades, 1 a 30 y 31 a 64

**Definicion exacta:** el corte de la secuencia recibida entre la posicion 30 y
la 31, es decir entre el par numero 15 y el numero 16. Las dos mitades tienen 30
y 34 hexagramas y **no son iguales**, de modo que no definen ninguna traslacion
de posiciones.

**Dueno del tema, citado y no leido:** Hacker y Moore 2003, "A Brief Note on the
Two-Part Division of the Received Order of the Hexagrams in the Zhouyi", Journal
of Chinese Philosophy 30(2), pp. 219-221, registrado en PRIOR-ART.md 12.5 como
segunda mano y **pendiente de artefacto**. De ahi no se toma ningun contenido:
solo se deja constancia de que el tema tiene dueno localizado. Lo que se usa aqui
es el corte, que es un hecho de la secuencia recibida.

**Aporta:** el rasgo binario "los dos hexagramas de un par estan en la misma
mitad", y el rasgo por par de posiciones. **No aporta biyeccion.**

### A3. Desplazamiento ciclico de pares

**Definicion exacta:** la biyeccion de los 64 hexagramas inducida por mover la
posicion 2k a la 2(k+1) modulo 64 y la 2k+1 a la 2(k+1)+1. Manda el par numero k
al k+1 modulo 32 conservando el orden interno.

**Fuente:** propuesta aqui. Respeta el sistema de pares por construccion.
**Aporta biyeccion**, y no es afin en general.

### A4. Inversion del orden de la secuencia

**Definicion exacta:** la biyeccion inducida por mandar la posicion i a la 63
menos i. Manda el par k al par 31 menos k e intercambia sus dos miembros.

**Fuente:** propuesta aqui, y ya aparecio como simetria en PROOFS-B31.md 2.4,
donde se demostro que la clase forzada es cerrada bajo ella. **Aporta
biyeccion.**

### A5. El intercambio dentro del par

**Definicion exacta:** la involucion tau que manda cada hexagrama a su companero
de par, que es el giro fuera de los palindromos y el complemento sobre ellos.

**Fuente:** es la propia regla de emparejamiento de King Wen, ya demostrada en
PROOFS.md 3.1. **No es afin**, y por eso no estaba en el grupo de orden 384, que
es su centralizador dentro de B6. **Aporta biyeccion.**

## Como se van a probar, declarado

**Fase 1, la anatomia.** Se descompone el 1013 sobre las 19 orbitas libres: para
cada una, cardinal, mitad, aportacion observada y desviacion. **El vector
completo, no un resumen.** Despues se cruzan las orbitas desviadas contra los
rasgos de A1 y A2, y el cruce se reporta como tabla **sin lenguaje de
significancia**: recuentos con su procedencia y nada mas.

**Fase 2, las simetrias extendidas.** Para cada candidata: (a) si la construccion
de King Wen la respeta como sistema de pares o de bloques; (b) si anadirla
reduce las 19 orbitas libres o estrecha el intervalo.

**Advertencia declarada sobre (b), para que no se lea de mas.** Dentro de B6 el
grupo **no puede crecer**: el de orden 384 ya es el estabilizador completo del
sistema de pares. Luego cualquier estrechamiento tiene que venir de biyecciones
**fuera** de B6, que son las que aportan A3, A4 y A5. Y esas tres estan definidas
**a traves de las posiciones**, no del espacio de hexagramas, de modo que usarlas
cambia el objeto: se pasa de preguntar que fuerza la simetria del cubo a
preguntar que fuerza la simetria de la propia disposicion. Se hara, y se dira
cada vez, y el orden del grupo resultante se reportara siempre. **Un
estrechamiento obtenido con un grupo grande y sin estructura no es un hallazgo**,
y si sale asi se dira asi.

## Desenlaces, escritos antes de correr

- **Si alguna candidata fuerza o estrecha:** es hallazgo, con su teorema si el
  argumento sale, o con su enumeracion declarada si no.
- **Si ninguna:** el residuo queda **DECLARADO INFORMATIVO relativo a esta
  lista**, con la frase de que la matematica toca fondo donde empieza la eleccion
  editorial, y esa declaracion va a la seccion 6 del manuscrito como cierre
  honesto.

En los dos casos, sin afirmaciones de novedad.
