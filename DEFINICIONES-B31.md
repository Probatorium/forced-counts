# Candidatos a invariante de la clase forzada en B(3,1)

Declarado **antes de mirar**. Lista cerrada: solo se prueban los candidatos que
estan abajo, y si despues aparece otro, entra en un documento nuevo y en un
commit posterior, nunca colandose en este.

## El problema

El espacio es enumerable entero: las **40320** ordenaciones de los ocho vertices,
todas con el **mismo grupo** de orden 16, el que respeta B(3,1), cuyos bloques
son los cuatro pares de vertices que difieren en la linea 1. De esas
ordenaciones, **472 quedan forzadas** al empate y **39848 no**. La pregunta es
que las separa.

Un invariante **vale** si separa exactamente esa particion. Una separacion
parcial no se descarta en silencio: se reporta con su matriz de confusion.

## Los candidatos

**C1. El emparejamiento del Lema 3, orbita por orbita.** Para cada orbita se
levanta el grafo cuyas aristas son las parejas con testigo de epsilon uno, y se
pregunta si admite emparejamiento perfecto. La pregunta concreta: **es la
existencia del emparejamiento en todas las orbitas exactamente equivalente a que
la ordenacion quede forzada**, o hay ordenaciones forzadas donde el grafo no
tiene emparejamiento perfecto porque falla la condicion de Hall.

**C2. El perfil de desplazamiento de los bloques.** Cada bloque es un par de
vertices; en la ordenacion sus dos elementos ocupan dos posiciones. Se toma el
multiconjunto de las cuatro distancias entre posiciones de un mismo bloque.

**C3. El perfil de orbitas.** El multiconjunto de los pares formados por el
cardinal de cada orbita y su c. Es lo mas cercano al aparato interno, y sirve
para saber si la separacion se ve ya en la contabilidad o hace falta mirar mas
abajo.

**C4. El recuento total.** Si la ordenacion da exactamente el empate, 14 pares
discordantes. Es condicion necesaria y la pregunta es si tambien es suficiente.

**C5. El perfil de paridad de posiciones por bloque.** Para cada bloque, la
paridad de la suma de las dos posiciones que ocupan sus elementos; se toma el
multiconjunto de las cuatro paridades.

**C6. Cierre de la clase forzada bajo simetrias.** No es un invariante de una
ordenacion sino una propiedad del conjunto de las 472. Se prueba si ese conjunto
es cerrado bajo tres cosas: relabelar los vertices por un elemento del grupo,
relabelar los vertices por un elemento cualquiera de B_3, e invertir el orden de
la ordenacion.

## Lo que se hara con el resultado

- Si algun candidato separa exacto, se intenta elevar a teorema, primero en
  B(3,1) y despues en general si el argumento no usa n igual a 3.
- Si ninguno separa, la caracterizacion queda **abierta**, con la lista de
  descartados escrita. Eso tambien es resultado.

Todo lo enumerativo de aqui es legitimo porque el espacio se recorre entero. El
reparto entre demostrado y enumerativo se declara igual que siempre.
