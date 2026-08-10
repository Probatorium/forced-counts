# Construcciones analogas, declaradas antes de medir

Este fichero se escribe y se commitea **antes de correr la primera medicion
general**. Lo exige la seccion (d) de PREREGISTRATION-GENERAL.md: las
construcciones que se midan se declaran antes, en documento propio y en commit
anterior al de la medicion, igual que se hizo con DEFINICIONES-GRUPO.md.

No enmienda ningun texto firmado.

## 1. Que dimensiones

n igual a 3, 4 y 5. Son 8, 16 y 32 vertices, con 28, 120 y 496 pares. El grupo
afin B_n tiene 48, 384 y 3840 elementos. **Todo se enumera entero, sin muestreo,
salvo donde se diga explicitamente lo contrario.**

## 2. Los sistemas de bloques

Un solo sistema, con un parametro, que cubre de golpe los dos analogos que
interesan.

**B(n, k)**: los bloques son las clases laterales del subespacio V_k generado
por las k coordenadas bajas. Son 2^(n-k) bloques de 2^k vertices cada uno, y dos
vertices caen en el mismo bloque cuando difieren solo en coordenadas bajas.

Se recorre **k desde 1 hasta n-1**, y se reportan todos los k. La eleccion de k
no se hace despues de ver resultados.

Por que ese sistema y no otro. Con k igual a n partido por dos es el analogo de
Mawangdui, cuyos bloques son las fibras del trigrama superior. Recorriendo todos
los k es la torre de particiones del codigo de Gray reflejado, que ya se uso en
n igual a 6. Y para n impar, donde no hay mitades, el parametro sigue teniendo
sentido y el analogo de Mawangdui simplemente no esta definido: se dira asi y no
se forzara ninguna analogia.

## 3. Las ordenaciones

Tres familias, las tres declaradas aqui.

**O1, el orden binario.** La identidad sobre los 2^n vertices bajo la convencion
de referencia. Entra como control degenerado: su recuento de pares discordantes
contra si mismo es cero por definicion, y sirve para comprobar que el aparato no
inventa nada.

**O2, el codigo de Gray reflejado.** Construido por su definicion recursiva,
igual que en n igual a 6: G(0) es la palabra vacia, y G(j) es la lista de G(j-1)
con un cero delante, seguida de la lista de G(j-1) en orden inverso con un uno
delante. La linea que se anade en cada paso es la mas significativa de la
convencion de referencia.

**O3, la familia de tipo Mawangdui, con parametros.** Fijado k, una ordenacion
de esta familia queda determinada por dos permutaciones: **pi**, el orden en que
van los 2^(n-k) bloques, y **rho**, el orden en que van los 2^k vertices dentro
de cada bloque, el mismo para todos los bloques. La posicion numero
i por 2^k mas j lleva el vertice cuya parte alta es pi(i) y cuya parte baja es
rho(j).

- **O3 canonica:** pi y rho las identidades.
- **O3 muestreada:** pi y rho al azar. Espacio completo cuando se puede enumerar
  y muestra declarada cuando no.

Se declara ahora, antes de correr: **para n igual a 3 el espacio de pares
(pi, rho) se enumera entero**; para n igual a 4 y 5 se muestrea con la semilla
ya congelada del repositorio, **20260809**, y con **2000 repeticiones por
combinacion de n y k**. Las dos cosas se reportan diciendo cual se hizo.

## 4. El grupo y la contabilidad

Sin novedad respecto de lo ya fijado, y por eso se cita en vez de repetirse.

- **Nocion de respetar:** la R1 de DEFINICIONES-GRUPO.md trasladada a n. Una
  aplicacion de B_n respeta el sistema de bloques cuando manda cada bloque
  entero sobre un bloque entero. El grupo se **enumera entero** dentro de B_n.
- **Contabilidad:** la de DEFINICIONES-GRUPO.md. El bit epsilon igual a A XOR B,
  las orbitas de pares de posiciones bajo la accion inducida, la paridad
  propagada desde un representante, y el reparto entre orbitas forzadas y
  orbitas libres.
- **Convenciones de bits:** las cuatro de PREREGISTRATION-GENERAL.md (d). La de
  referencia para la contabilidad es yang como uno con la linea inferior como
  bit mas significativo; los totales se reportan en las cuatro.
- **Denominador:** C(2^n, 2). Valor central del empate: su mitad.

## 5. Las tres casillas, definidas de forma operativa

Cada caso medido cae en exactamente una, y el criterio se fija ahora:

- **FORZADO.** La anchura del intervalo es cero. Por el corolario del Lema 1 eso
  implica que el valor determinado es el empate, y no hace falta comprobarlo
  aparte: si sale otro valor, hay un error de aparato y se reporta como tal.
- **PROHIBIDO.** La anchura es mayor que cero y el empate **no** esta entre los
  totales compatibles con la estructura.
- **INTERVALO.** La anchura es mayor que cero y el empate **si** esta entre los
  compatibles.

Se reportan ademas, para cada caso: el orden del grupo, el numero de orbitas,
cuantas forzadas y cuantas libres, el intervalo, el numero de totales
compatibles, la paridad forzada y el recuento observado.

## 6. Que NO se hace en esta medicion

- No se afirma ninguna clasificacion. El objetivo declarado en
  PREREGISTRATION-GENERAL.md (c.2) es **ver la forma** de la clasificacion, y
  eso es lo que se hace.
- No se selecciona ningun caso despues de verlo. Se reporta la rejilla entera de
  n por k por familia de ordenacion.
- No se afirma novedad de nada. La revision de antecedentes sigue ABIERTA.
