# La clase forzada en B(3,1)

Espacio enumerado entero: las **40320** ordenaciones de los ocho vertices, todas
con el mismo grupo de orden 16. **472 forzadas y 39848 no**
(`results/b31-characterization.tsv:5` a `:8`). Los candidatos a invariante se
declararon antes de mirar, en DEFINICIONES-B31.md, y solo se probaron esos.

Reparto de siempre: **DEMOSTRADO**, **ENUMERATIVO** y **REFUTADO**. Sin
afirmaciones de novedad: la revision sigue ABIERTA.

---

# 1. Dos teoremas que quitan el aparato de en medio

## 1.1 Una orbita esta forzada si y solo si aporta la mitad. DEMOSTRADO

**Teorema.** Una orbita esta forzada si y solo si el numero de pares discordantes
que contiene es exactamente la mitad de su cardinal.

**Demostracion.** La aportacion de una orbita vale c o cardinal menos c, segun el
unico bit libre. Si vale la mitad del cardinal, entonces c o cardinal menos c es
la mitad, y las dos cosas dan c igual a la mitad, que es la definicion de
forzada. Y si c es la mitad, las dos opciones coinciden en la mitad. Fin.

**Lo que este teorema quita.** Para saber si una ordenacion esta forzada no hace
falta propagar paridades ni calcular epsilon: basta contar. La contabilidad de
DEFINICIONES-GRUPO.md sigue haciendo falta para saber **que intervalo** queda
cuando no esta forzada, pero no para la pregunta de si lo esta.

## 1.2 La caracterizacion por clases de diferencia. DEMOSTRADO

**Teorema.** Sea G un subgrupo que contiene **todas** las traslaciones. Entonces
las orbitas de G sobre pares de vertices son las clases de diferencia, es decir
los conjuntos de pares cuya diferencia recorre una orbita de las partes lineales.
En consecuencia, y por 1.1:

> una ordenacion esta forzada **si y solo si, en cada clase de diferencia,
> exactamente la mitad de sus pares son discordantes**.

**Demostracion.** Las traslaciones actuan transitivamente sobre los pares de una
diferencia fija, porque el par en x va al par en x mas v. Y las partes lineales
mandan la diferencia d a su imagen. Luego la orbita de un par es el conjunto de
los pares cuya diferencia esta en la orbita de d bajo las partes lineales, que
es lo que se llama aqui clase de diferencia. Aplicando 1.1 orbita por orbita sale
el enunciado. Fin.

**El argumento no usa n igual a 3** ni la particion concreta: vale para cualquier
n y cualquier G que contenga todas las traslaciones, que es el caso de todos los
B(n, k) por la identificacion ya demostrada. Comprobado en 100 casos de los dos
lados (`results/b31-characterization.tsv:41`).

En B(3,1) las clases de diferencia son cinco, con 4, 8, 8, 4 y 4 pares, y la
condicion es 2, 4, 4, 2 y 2 discordantes respectivamente.

---

# 2. Los candidatos declarados, uno por uno

| candidato | separa exacto | veredicto |
|---|---|---|
| C1, emparejamiento del Lema 3 en toda orbita | **si** | util, y medio demostrado |
| C2, perfil de desplazamiento de bloques | no | REFUTADO como invariante |
| C3, perfil de orbitas | si, pero es la definicion disfrazada | no informativo |
| C4, recuento total igual al empate | no | necesario y no suficiente |
| C5, perfil de paridad de posiciones | no | REFUTADO, y del todo |
| C6, cierre de la clase bajo simetrias | no aplica, es otra cosa | resultado parcial |

## 2.1 C1, el emparejamiento del Lema 3. Separa exacto

Las 472 forzadas tienen emparejamiento perfecto en **todas** sus orbitas, y
ninguna de las 472 no forzadas probadas lo tiene
(`results/b31-characterization.tsv:33` a `:37`).

**Una direccion es teorema y la otra es enumerativa, y conviene separarlas.**

- **DEMOSTRADO:** si una orbita no esta forzada, **no** puede haber
  emparejamiento perfecto. Razon: toda arista del grafo de relaciones une pares
  de paridad contraria, luego el grafo es bipartito entre las dos clases de
  paridad; si la orbita no esta forzada, esas clases tienen cardinales distintos
  y ningun emparejamiento perfecto existe. Por eso el lado negativo no necesita
  recorrer las 39848: es imposible por construccion.
- **ENUMERATIVO:** si una orbita esta forzada, el emparejamiento existe. Aqui
  las clases tienen igual cardinal, pero eso solo no basta: hace falta la
  condicion de Hall, que podria fallar. **No falla en ninguna de las 472**, y
  eso es lo comprobado. No se demuestra en general.

Lectura: en B(3,1), **el Lema 3 alcanza toda orbita forzada**, sin excepcion. Es
el mismo fenomeno que ya se habia visto en la clase (0,1) de Mawangdui, donde el
grafo resulto ser completo bipartito.

## 2.2 C3, el perfil de orbitas. Separa, pero no dice nada

El multiconjunto de cardinales con su c separa exacto
(`results/b31-characterization.tsv:15` a `:20`), y **no es un hallazgo**: por
1.1, estar forzada se lee directamente de ese perfil. Es la definicion escrita de
otra manera. Se reporta porque estaba en la lista declarada y porque descartarlo
en silencio seria justo lo que la lista cerrada existe para impedir.

## 2.3 C2, C4 y C5. REFUTADOS como invariantes

- **C2, desplazamiento de bloques:** 54 valores distintos, y **las 472 forzadas
  caen todas en valores mezclados** (`:9` a `:14`). Ninguna configuracion de
  distancias entre los dos elementos de un bloque decide nada por si sola.
- **C4, recuento total igual a 14:** condicion **necesaria**, porque una
  ordenacion forzada da el empate por el Lema 1. **No suficiente**: las 472
  forzadas estan en valores mezclados, y hay **3364** ordenaciones no forzadas
  que tambien caen en valores mezclados (`:21` a `:26`). Dar el empate no es
  estar forzada.
- **C5, paridad de posiciones por bloque:** solo tres valores distintos y todo
  mezclado en los dos lados (`:27` a `:32`). Es el candidato mas pobre de los
  declarados.

## 2.4 C6, cierre de la clase forzada. Resultado partido

| simetria | cerrada | estatus |
|---|---|---|
| relabelar vertices por el grupo que respeta los bloques | **no** | medido, `:38` |
| relabelar vertices por B_3 entero | **no** | medido, `:39` |
| invertir el orden de la ordenacion | **si** | medido `:40`, y DEMOSTRADO abajo |

**Teorema.** La clase forzada es cerrada bajo invertir la ordenacion.

**Demostracion.** Invertir manda la posicion i a la N menos 1 menos i. Eso
conjuga la permutacion inducida de cada elemento del grupo, luego las orbitas de
pares van a orbitas de pares del mismo cardinal. Y en cada par, el que estaba
antes pasa a estar despues, de modo que su estado de discordancia se invierte.
La aportacion de una orbita pasa por tanto a ser su cardinal menos la aportacion,
y ser la mitad se conserva. Por 1.1, forzada va a forzada. Fin.

**Que no ser cerrada bajo el grupo es interesante y no es un error.** Relabelar
los vertices por g cambia que vertice esta en cada posicion, mientras que la
funcion de valor se queda fija; la ordenacion resultante es otra de verdad. El
grupo actua sobre los vertices, no sobre las ordenaciones, y la clase forzada no
tiene por que respetarlo.

---

# 3. Donde queda la caracterizacion

**Hay caracterizacion, y es la de 1.2**: forzada si y solo si cada clase de
diferencia aporta exactamente la mitad. Es demostrada, es general, y convierte la
pregunta en un recuento sin aparato.

**Lo que no hay es un invariante mas simple que ella.** De los cinco candidatos
declarados que eran invariantes de una ordenacion, tres quedan refutados, uno
separa por ser la definicion disfrazada, y el que separa de verdad, C1, es
equivalente a la propia condicion en una direccion por teorema y en la otra por
enumeracion de las 472.

**Lo que queda abierto**, y se deja escrito como tal:

- **Si el Lema 3 alcanza siempre a toda orbita forzada**, o si existe algun caso
  donde la condicion de Hall falla. En B(3,1) no falla nunca, y en la clase
  (0,1) de Mawangdui tampoco, pero eso son dos casos.
- **Contar las forzadas.** Que sean 472 en B(3,1) y 600 en B(3,2) esta medido y
  no explicado. No hay formula aqui.
- **Por que la clase no es cerrada bajo el grupo.** Medido, con las dos
  respuestas en cero, y sin caracterizar que le pasa a una ordenacion forzada al
  relabelarla.

## Reproducir

    python src/b31_characterization.py
