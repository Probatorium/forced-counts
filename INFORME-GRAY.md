# Informe: el codigo de Gray reflejado, ordenacion de comparacion

**Deslinde, en primera aparicion.** En la literatura de codigos de Gray la
palabra *balanced* se refiere a los recuentos de transicion por coordenada, esto
es a repartir por igual cuantas veces cambia cada bit a lo largo del ciclo. No se
refiere al empate que aqui se mide, que es que el recuento de inversiones contra
el orden binario caiga en C(64,2) partido por dos. Son dos cosas distintas, y en
este repositorio no se mezclan.

Esta ordenacion entra **solo como objeto de comparacion**. No es historica, no
esta en ninguna preinscripcion, y las tres historicas no se tocan. Se pone al
lado para tener una cuarta ordenacion construida, con reglas limpias, contra la
que leer las otras.

Todas las cifras salen de `src/gray.py` y se citan con fichero y linea. Sin
afirmaciones de novedad: la revision de antecedentes no ha empezado.

## 1. La construccion

Construido aqui desde su definicion recursiva, sin importar nada:

    G(0) = [la palabra vacia]
    G(k) = [n seguido de w, para w en G(k-1)]
        ++ [y seguido de w, para w en G(k-1) en orden inverso]

La linea que se anade en cada paso es la mas significativa de la convencion de
referencia, de modo que la linea 1 se anade en el ultimo paso.

Comprobado: son los 64 hexagramas sin repetir
(`results/gray-measurements.tsv:4`); la recursion reproduce la forma cerrada, el
numero XOR el mismo numero desplazado uno, bajo la convencion de referencia
(`:5`); cada paso cambia exactamente una linea (`:6`); y el coste de Hamming
adyacente es 63 (`:7`), que es el minimo posible para 64 palabras.

## 2. El recuento, con el mismo aparato y el mismo denominador

Denominador C(64,2) igual a 2016 (`results/gray-measurements.tsv:8`).

| convencion | inversiones | tasa | origen |
|---|---|---|---|
| yang=1, inferior MSB | 496 | 0.246032 | `results/gray-measurements.tsv:9` |
| yang=1, inferior LSB | 992 | 0.492063 | `:10` |
| yang=0, inferior MSB | 1520 | 0.753968 | `:11` |
| yang=0, inferior LSB | 1024 | 0.507937 | `:12` |

Dos observaciones de lectura directa, sin ir mas alla de la tabla. La primera:
cambiar la polaridad manda el recuento a 2016 menos el recuento, igual que en
las tres historicas. La segunda: cambiar la orientacion **si mueve** el recuento
de Gray, 496 frente a 992, mientras que en las tres historicas no lo movia.

## 3. El grupo, nivel a nivel

La recursion no da una particion en bloques, da una torre de particiones, una
por nivel. Se declaro antes de correr nada que se recorren **todos** los niveles,
tamanos 2, 4, 8, 16 y 32, y que se reportan todos, para que la eleccion de nivel
no pueda hacerse despues de ver resultados. La nocion de respetar es la misma R1
de DEFINICIONES-GRUPO.md, sin cambios.

En todos los niveles los bloques resultan ser cosets de un mismo subespacio,
comprobado y no supuesto, y el orden del grupo sale k factorial por 6 menos k
factorial por 64, tambien comprobado contra la enumeracion:

| tamano de bloque | R1 | R2 | orbitas | forzadas | aportacion forzada | intervalo | observado | fuerza el empate | origen |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 7680 | 3840 | 11 | 1 | 16 | [496, 1520] | 496 | no | `results/gray-measurements.tsv:15` a `:29` |
| 4 | 3072 | 384 | 14 | 2 | 48 | [496, 1520] | 496 | no | `:32` a `:46` |
| 8 | 2304 | 48 | 15 | 3 | 112 | [496, 1520] | 496 | no | `:49` a `:63` |
| 16 | 3072 | 8 | 14 | 4 | 240 | [496, 1520] | 496 | no | `:66` a `:80` |
| 32 | 7680 | 2 | 11 | 5 | 496 | [496, 1520] | 496 | no | `:83` a `:97` |

Con la sola complementacion: 336 orbitas forzadas, aportacion forzada 336,
anchura 1344, observado 496 (`results/gray-measurements.tsv:98` a `:101`).

Lo que la tabla dice, y nada mas: en ningun nivel el grupo fuerza el empate. El
intervalo es el mismo en los cinco niveles, [496, 1520], y el recuento observado
cae en su extremo inferior. El empate esta dentro del intervalo en los cinco
niveles, es decir que la estructura no lo prohibe, al reves de lo que pasa en
King Wen.

## 4. Al lado de las tres historicas

Solo para tener las cuatro en una misma pagina, con la convencion de referencia
y el mismo denominador. Las tres primeras filas vienen de los informes
anteriores y no se han vuelto a calcular aqui.

| ordenacion | inversiones | intervalo que deja su grupo | fuerza el empate |
|---|---|---|---|
| Mawangdui | 1008 | [1008, 1008] | si |
| Jing Fang | 1008 | [1008, 1008] | si |
| King Wen | 1013 | [957, 1059] | no, y lo prohibe |
| Gray reflejado | 496 | [496, 1520] | no |

Origen de las tres primeras: `results/group-measurements.tsv:49` a `:180`, ya
citadas una a una en INFORME-GRUPO.md. Origen de la cuarta:
`results/gray-measurements.tsv:9` y `:56` a `:58`.

Una coincidencia de orden que conviene no leer de mas: el grupo de Gray al nivel
de bloques de ocho tiene orden 2304, el mismo que el de Mawangdui
(`results/gray-measurements.tsv:49`). Es el mismo tipo de estabilizador, el de
un subespacio de dimension tres, y por eso sale el mismo numero. No dice nada
sobre las dos ordenaciones.

## 5. Que no dice este informe

- No dice que el codigo de Gray tenga nada que ver con las tres historicas.
  Esta aqui como vara de medir, no como pariente.
- No dice nada sobre balanced en el sentido de la literatura de codigos de Gray,
  que es el de los recuentos de transicion por coordenada. Ese sentido no se
  mide aqui.
- No afirma novedad de nada. La revision de antecedentes no ha empezado.

## Reproducir

    python src/gray.py

Determinista, sin azar.

---

# Enmiendas

Se anaden al pie, con fecha y motivo. **No se toca el texto de arriba.**

## Enmienda 1, 2026-08-09: el deslinde de *balanced*, de segunda mano a artefacto leido

**Motivo.** La frase de deslinde con la que abre este informe afirma que en la
literatura de codigos de Gray *balanced* refiere a los recuentos de transicion
por coordenada. Cuando se escribio, esa afirmacion **no tenia artefacto detras**:
su cadena de cita era el conocimiento general del asistente que la redacto, y
PRIOR-ART.md la marco como segunda mano pendiente del survey de Mutze.

**Queda resuelta.** Se leyo el artefacto y se verifico la formula contra el PDF,
que es el canal fuerte. Torsten Mutze, *Combinatorial Gray codes, an updated
survey*, The Electronic Journal of Combinatorics 30(3) (2023), Dynamic Survey
#DS26, seccion 3.2 "Transition counts", pagina impresa 11, dice literalmente:

> "Specifically, let c_i denote the number of times that bit i is flipped along
> a given Gray cycle... Formally, in a *balanced Gray code*, we require that
> |c_i - 2^n/n| < 2 for i = 1, ..., n."

La frase de arriba, por tanto, **se sostiene**, y ahora con puntero.

**Dos cosas que la frase de arriba no decia y hay que anadir.**

Primera: el survey usa la palabra en **mas de un sentido**. Ademas del de los
recuentos de transicion, en su seccion 2.2 llama *balancedness constraint* a la
comparacion de tamanos entre las clases de una particion bipartita o k-partita
de un grafo de flips, como obstruccion a la hamiltonicidad, y de ahi salen los
posets balanceados y las transposiciones balanceadas del resto del survey. El
deslinde vale contra los dos.

Segunda, y toca a este informe de lleno: el mismo survey dice del codigo de Gray
reflejado que **"in the BRGC, we have c_i = 2^{n-i} for i = 1, ..., n-1 and
c_n = 2, i.e., it is very unbalanced"**. Es decir que la ordenacion de
comparacion que este informe mide es, en el sentido tecnico de Mutze,
**muy desbalanceada**. Eso no cambia ninguna cifra de las tablas de arriba, que
son de otro objeto, pero cierra la puerta a leer la palabra en las dos
direcciones a la vez.

Registro completo del artefacto en PRIOR-ART.md, seccion 7.
