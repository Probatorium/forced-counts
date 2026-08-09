# Definiciones fijadas antes de enumerar el grupo

Este fichero se escribe y se commitea ANTES de ejecutar la enumeracion. Su
objeto es que la nocion de "la construccion respeta una simetria", el grupo que
se va a enumerar y la contabilidad que se va a hacer con el queden cerrados
antes de ver ningun resultado. La historia de git deja constancia del orden.

No enmienda ningun texto firmado. PREREGISTRATION.md, CONTACT-RULES.md y
EFFORT.md se quedan como estan.

## 1. La familia recorrida

Un hexagrama es una cadena de seis lineas, indice 0 la linea inferior. La
familia afin es el conjunto de aplicaciones

    f(x) = permutar las seis lineas segun P, y despues complementar las lineas
           marcadas por una mascara m

con P cualquiera de las 720 permutaciones de las seis posiciones de linea y m
cualquiera de las 64 mascaras. Son 46080 aplicaciones. Es la misma familia que
se recorrio en el commit de la medicion, y contiene la identidad, la
complementacion, el giro de media vuelta y toda relectura de las lineas.

La familia es un grupo con la composicion.

## 2. Que quiere decir que la construccion respeta f

Cada construccion trae su propia particion de los 64 hexagramas en bloques
contiguos de la secuencia:

- Mawangdui: los ocho octetos, bloques de ocho por trigrama superior.
- Jing Fang: los ocho palacios, bloques de ocho.
- King Wen: los treinta y dos pares adyacentes, bloques de dos.

**Nocion R1, sistema de bloques.** f respeta la construccion cuando manda cada
bloque entero sobre un bloque entero:

    para todo bloque B, el conjunto f(B) es tambien un bloque.

Es exactamente la nocion que se uso para King Wen en el commit anterior, donde
dio 112 involuciones. Aqui se aplica igual a las tres construcciones y ya no se
limita a involuciones: se enumera el grupo completo.

**Nocion R2, sistema de posiciones.** f respeta la construccion en el sentido
fuerte cuando ademas conserva el indice dentro del bloque:

    si x ocupa la posicion p de su bloque, f(x) ocupa la posicion p del bloque
    imagen.

R2 implica R1. Las dos se reportan por separado.

Para cada construccion y cada nocion, el conjunto de aplicaciones afines que la
cumplen es un subgrupo de la familia afin, por ser el estabilizador de una
estructura. Se reportara su orden y un conjunto de generadores.

## 3. La contabilidad por orbitas

Sea sigma la secuencia, v el valor binario bajo una convencion fijada, y para
cada f del grupo sea pi_f la permutacion de posiciones inducida,
pi_f = sigma^-1 . f . sigma.

Un par de posiciones {i, j} con i menor que j es una inversion cuando
v(sigma(i)) es mayor que v(sigma(j)). El recuento es la suma sobre los C(64,2)
pares.

Para un par p y un elemento f del grupo, sea p' el par imagen y definanse dos
bits, los dos calculables sin saber si p es inversion:

    A = 1 si pi_f invierte el orden de las dos posiciones del par
    B = 1 si f invierte el orden binario de los dos hexagramas del par

Entonces el estado de inversion cumple

    estado(p') = estado(p) XOR (A XOR B)

Esa relacion, y no otra cosa, es lo que la simetria fuerza. Escribiendo
epsilon(f, p) = A XOR B, el estado queda determinado en toda la orbita de p en
cuanto se fija en un solo representante.

Para cada orbita O:

- se calcula la paridad de cada par respecto de un representante, propagando
  epsilon. Si apareciera una contradiccion, el programa se detiene: seria un
  error, porque el estado existe.
- sea c el numero de pares de la orbita con paridad uno. La aportacion de la
  orbita al recuento vale c o bien el cardinal de O menos c, segun el unico bit
  libre que queda, el estado del representante.
- la orbita esta FORZADA cuando las dos opciones coinciden, es decir cuando c es
  la mitad del cardinal. Entonces su aportacion no depende de nada mas que de la
  estructura.
- la orbita esta LIBRE en caso contrario, y aporta un rango de dos valores.

Sumando: el grupo fuerza el recuento a caer en el intervalo entre la suma de los
minimos y la suma de los maximos, con a lo sumo dos elevado al numero de orbitas
libres valores posibles.

## 4. Que se declara ahora como criterio de lectura

- **El grupo fuerza el empate** si y solo si la suma de los minimos y la suma de
  los maximos coinciden y valen C(64,2) partido por dos. Cualquier otra cosa no
  es forzar.
- **El grupo aprieta** si el intervalo se estrecha respecto del que deja la sola
  complementacion, sin llegar a un punto.
- **El grupo no basta** si el intervalo sigue conteniendo valores distintos del
  observado. Eso se reportara como resultado, no como fracaso: acota donde no
  vive la explicacion.
- La contabilidad con el grupo generado solo por la identidad y la
  complementacion tiene que reproducir las cifras del commit anterior. Si no las
  reproduce, hay un error en el nuevo aparato y se reporta como tal.

## 5. Alcance y limites, declarados de antemano

- La familia afin no agota las biyecciones de los 64 hexagramas. Un resultado
  negativo acota la explicacion dentro de esta familia y no fuera de ella.
- La particion en bloques es la que da cada construccion. Otra manera de trocear
  la misma secuencia daria otro grupo. La eleccion se fija aqui y no se cambia
  despues de ver resultados.
- La convencion de referencia para los valores es yang como uno y linea inferior
  como bit mas significativo. Las cuatro convenciones fijadas en
  PREREGISTRATION.md se recorren igualmente para los totales.
- El espacio de la familia afin es de 46080 elementos y se enumera entero. No
  hay muestreo, y por tanto no hay semilla que declarar en esta parte.

## 6. Prohibiciones vigentes en este tramo

Sin afirmaciones de novedad: la revision de antecedentes sigue sin empezar.
Sin tocar kingwen-orderings-replication fuera de la etiqueta zenodo-v3. Sin
tocar Stasis. Sin enmendar textos firmados.
