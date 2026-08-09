# PROOFS

Lo que en los informes anteriores quedo enumerado se separa aqui en dos
montones, sin tercero. Cada pieza lleva su comprobador mecanico en
`src/proofs.py`, cuya salida es `results/proofs.tsv`, y cada cifra se cita con
fichero y linea.

**DEMOSTRADO** quiere decir: la afirmacion se sigue de un teorema demostrado en
este fichero, aplicado a una hipotesis que o bien se argumenta en prosa aqui, o
bien se exhibe como testigo concreto y se verifica sobre un conjunto finito
explicito. En cada caso se dice cual de las dos, y los testigos exhibidos estan
listados uno a uno en `results/certificates.txt`, cada linea verificable por
separado.

**ENUMERATIVO** quiere decir: la afirmacion sale de calcular la propia respuesta
recorriendo el espacio, sin teorema por medio. No se disfraza de otra cosa.

Sin afirmaciones de novedad: la revision de antecedentes no ha empezado.

## Convenios y nombre

Un hexagrama es un vector de F_2 elevado a 6. La linea 1 es la inferior. Bajo la
convencion de referencia, yang igual a uno y linea inferior como bit mas
significativo, el valor es v igual a 8 por lambda mas ipsilon, donde lambda es el
trigrama inferior leido con la linea 1 como bit mas significativo e ipsilon el
superior leido igual.

La familia de aplicaciones que se viene recorriendo, permutar las seis lineas y
despues complementar un subconjunto de ellas, es el **grupo hiperoctaedrico
B6**, el grupo de simetrias del 6-cubo, de orden 2 elevado a 6 por 6 factorial,
igual a 46080. **Correspondencia:** los 64 hexagramas son los vertices del
6-cubo, permutar lineas es permutar ejes de coordenadas, y complementar un
subconjunto de lineas es reflejar en los hiperplanos coordenados
correspondientes. A partir de aqui se le llama B6, y no aparece ninguna otra
alusion a literatura en este documento.

Notacion: sigma es la secuencia, pi_g la permutacion de posiciones inducida por
g, kappa la complementacion, rho el giro de media vuelta, y
epsilon(g, p) = A XOR B como quedo definido en DEFINICIONES-GRUPO.md. Las
mascaras se escriben por las lineas que complementan.

---

# Pieza 1. El lema del empate

## Lema 0, relacion de estado

Sea g una biyeccion cualquiera de los hexagramas, p = {i, j} un par de
posiciones con i menor que j, y p' su imagen. Sean A igual a uno si pi_g invierte
el orden de las dos posiciones, y B igual a uno si g invierte el orden binario de
los dos hexagramas. Entonces

    estado(p') = estado(p) XOR A XOR B

**Demostracion.** Escribase x = sigma(i), y = sigma(j), de modo que
estado(p) = [v(x) mayor que v(y)]. Como sigma(pi_g(i)) = g(x) y
sigma(pi_g(j)) = g(y), si pi_g(i) es menor que pi_g(j) entonces
estado(p') = [v(g(x)) mayor que v(g(y))], y si es mayor entonces estado(p') es
su negacion; en los dos casos estado(p') = [v(g(x)) mayor que v(g(y))] XOR A. Y
por definicion de B, [v(g(x)) mayor que v(g(y))] = estado(p) XOR B. Sustituyendo
sale la formula. Ningun valor puede empatar, porque x e y son distintos y v es
inyectiva. Fin.

## Lema 1, el lema del empate

Sea G un grupo que actua sobre los hexagramas, con la accion inducida sobre los
C(64,2) pares de posiciones. Fijado un representante en cada orbita, sea
paridad(p) la suma de los epsilon a lo largo de cualquier camino desde el
representante hasta p, y sea c_O el numero de pares de la orbita con paridad
uno. Digase que la orbita esta FORZADA cuando c_O es la mitad del cardinal de O.

**Si toda orbita esta forzada, el recuento total es C(64,2) partido por dos.**

**Demostracion.** Por el Lema 0, estado(p) = estado(rep) XOR paridad(p) para todo
p de la orbita, luego la aportacion de la orbita vale c_O si estado(rep) es cero
y cardinal de O menos c_O si es uno. Si la orbita esta forzada las dos
cantidades coinciden y valen la mitad del cardinal, sea cual sea el estado del
representante. Sumando sobre orbitas, y como las orbitas parten el conjunto de
pares, el total es la mitad de C(64,2). Fin.

**Corolario.** Un grupo solo puede forzar el empate. Nunca puede determinar el
recuento y que salga otro valor: si lo determina, lo determina en C(64,2)
partido por dos. Esto sale de la demostracion, sin calcular nada.

## Lema 2, criterio de orbita forzada

**Si existe g en G con epsilon(g, p) igual a uno para todo p de la orbita O,
entonces O esta forzada.**

**Demostracion.** Por el Lema 0 el estado se alterna a lo largo de cada ciclo de
g dentro de O. Un ciclo de longitud impar obligaria a que un estado fuese igual
a su negacion, luego todos los ciclos tienen longitud par y en cada uno hay
tantos pares con estado uno como con estado cero. Sumando sobre los ciclos, la
aportacion de O es la mitad de su cardinal, y eso vale para cualquier eleccion
del bit libre. Fin.

A un g asi se le llama aqui **testigo** de la orbita. Un testigo es una
certificacion finita y verificable por separado: basta recorrer la orbita y
comprobar que epsilon vale uno.

## Lema 0b, cocadena, y por que las cadenas no dan nada nuevo

**epsilon(gh, p) = epsilon(g, h por p) XOR epsilon(h, p).**

**Demostracion.** Por el Lema 0 aplicado a h, a g y a gh:
estado(gh por p) = estado(p) XOR epsilon(gh, p), y tambien
estado(gh por p) = estado(h por p) XOR epsilon(g, h por p) =
estado(p) XOR epsilon(h, p) XOR epsilon(g, h por p). Igualando sale la formula.
Fin.

**Consecuencia.** Una cadena de elementos del grupo aplicada a un par acumula
sus epsilon, y esa acumulacion es exactamente el epsilon del producto, que es
otro elemento del grupo. Encadenar no llega mas lejos que un solo elemento. La
generalizacion util del Lema 2 no esta en alargar la cadena, sino en dejar de
exigir la hipotesis sobre toda la orbita.

## Lema 3, forzado por emparejamiento

Sea S un conjunto de pares de posiciones. **Si S admite un emparejamiento
perfecto en parejas {p, q} tales que para cada una hay algun g en G con
g por p igual a q y epsilon(g, p) igual a uno, entonces la aportacion de S al
recuento es exactamente la mitad del cardinal de S.**

**Demostracion.** Por el Lema 0, epsilon(g, p) igual a uno da
estado(q) = estado(p) XOR 1, de modo que de los dos pares de la pareja
exactamente uno es inversion, sin saber cual. Como las parejas parten S, la
aportacion es el numero de parejas, que es la mitad del cardinal. Fin.

**El Lema 2 es el caso particular** en que un mismo g sirve para todas las
parejas: sus ciclos dentro de la orbita tienen longitud par y se parten en
parejas consecutivas. Lo que el Lema 3 anade es que el testigo puede cambiar de
pareja en pareja, y que la hipotesis solo se exige sobre la mitad elegida, no
sobre la orbita entera.

**El Lema 3 no es gratis.** Si un conjunto no aporta exactamente la mitad, sus
dos clases de paridad tienen cardinales distintos y ningun emparejamiento
perfecto puede existir, porque toda arista une paridades contrarias. La
contraprueba esta hecha: en las 19 orbitas libres de King Wen no hay
emparejamiento perfecto en ninguna (`results/proofs.tsv:142` a `:144`).

## Comprobador

`src/proofs.py`, funcion `pieza_1`. Los tamanos de orbita suman C(64,2) en las
tres secuencias (`results/proofs.tsv:5`, `:7`, `:9`); la aportacion de toda
orbita es una de las dos opciones y no hay tercera (`:11`); donde la hipotesis
se cumple, el total sale la mitad (`:6`, `:10`); donde no se cumple, el lema no
se aplica (`:8`).

---

# Pieza 2. Mawangdui y Jing Fang

## 2.1 Mawangdui: el grupo, DEMOSTRADO

**Los bloques son las fibras del trigrama superior.** Por la regla de
construccion, el octeto de trigrama superior U contiene el hexagrama doblado
(U, U) y los (L, U) para los otros siete trigramas inferiores, es decir los ocho
hexagramas cuyas lineas 4, 5 y 6 forman U (`results/proofs.tsv:13`).

Sea V el subespacio de los vectores soportados en las lineas 1, 2 y 3. Dos
hexagramas caen en el mismo bloque si y solo si su diferencia esta en V
(`results/proofs.tsv:14`, `:15`).

**Teorema.** El grupo R1 de Mawangdui es el conjunto de los f(x) = P(x) XOR m de
B6 tales que P no mezcla el trigrama inferior con el superior, y su orden es
6 por 6 por 64, igual a 2304.

**Demostracion.** Para f = P XOR m se tiene f(x) XOR f(y) = P(x XOR y), porque la
mascara se cancela. Luego f conserva la relacion de estar en el mismo bloque si
y solo si P(V) = V. Como P solo permuta coordenadas, P(V) = V equivale a que P
deje invariante el conjunto de las tres lineas inferiores, es decir a que no
mezcle trigramas: son 3 factorial por 3 factorial igual a 36 permutaciones
(`results/proofs.tsv:16`, `:17`). Todas las mascaras son admisibles: trasladar
por m manda la fibra sobre U a la fibra sobre U XOR m_superior, que es otra
fibra; y como f es biyeccion y las fibras tienen ocho elementos, mandar dentro es
mandar sobre. El orden es 36 por 64 igual a 2304 (`results/proofs.tsv:18`), y
coincide con la enumeracion de B6 (`:19`). Fin.

## 2.2 Mawangdui: las orbitas, DEMOSTRADO

**Teorema.** Las orbitas de pares de posiciones bajo R1 son exactamente las
clases (a, b), con a el peso de la diferencia de los trigramas inferiores y b el
de los superiores, excluido el par (0, 0). Son 15, la clase (a, b) tiene
32 por C(3,a) por C(3,b) pares, y la mayor tiene 288.

**Demostracion.** Por 2.1, R1 es el producto directo de dos copias del grupo
generado por traslaciones y permutaciones de coordenadas de F_2 elevado a 3, una
actuando sobre el trigrama inferior y otra sobre el superior. Los pesos a y b son
invariantes: las traslaciones se cancelan en la diferencia y las permutaciones de
coordenadas conservan el peso. Reciprocamente, dados dos pares con los mismos
(a, b), se traslada cada uno hasta que su primer hexagrama sea el cero en las dos
coordenadas, con lo que el segundo queda descrito por su diferencia, y una
permutacion de coordenadas en cada factor lleva una diferencia de peso a en otra
de peso a, y lo mismo con b. Luego la accion es transitiva sobre cada clase. El
recuento sale de elegir el primer hexagrama de 64 maneras y la diferencia de
C(3,a) por C(3,b) maneras, dividido por dos por ser el par no ordenado. Fin.
Comprobado en `results/proofs.tsv:20` a `:24`.

## 2.3 Mawangdui: nueve clases, DEMOSTRADAS con testigo argumentado

**Teorema.** Las nueve clases con a mayor o igual que uno y b mayor o igual que
uno estan forzadas. Cubren 1568 de los 2016 pares y aportan 784.

**Demostracion.** Tomese g igual a complementar el trigrama inferior, esto es la
mascara de las lineas 1, 2 y 3, que esta en R1 por 2.1
(`results/proofs.tsv:25`). Sobre los valores, g manda lambda a 7 menos lambda y
deja ipsilon quieto. Si a es mayor o igual que uno, los dos lambda difieren, el
orden binario del par lo decide lambda porque v es 8 por lambda mas ipsilon con
ipsilon menor que ocho, y g lo invierte: B es uno. Sobre las posiciones, g no
cambia el trigrama superior, luego no cambia el bloque; si b es mayor o igual
que uno los dos hexagramas estan en bloques distintos y el orden de las
posiciones lo decide el bloque, que no se mueve: A es cero. Asi que epsilon es
uno en todos los pares de esas clases. Ademas g no fija ninguno, porque fijarlo
exigiria intercambiar dos posiciones de bloques distintos y g conserva el
bloque. Por el Lema 2, las nueve clases estan forzadas. Fin.
Comprobado par a par en `results/proofs.tsv:26` a `:29`.

## 2.4 Mawangdui: cinco clases mas, DEMOSTRADAS con testigo exhibido

La reduccion siguiente si se argumenta. Si a es cero, los dos hexagramas
comparten trigrama inferior, el orden binario lo decide ipsilon y el de
posiciones el indice de octeto, luego el estado depende solo del par de
trigramas superiores (`results/proofs.tsv:36`). Si b es cero, los dos estan en el
mismo octeto, el orden binario lo decide lambda y el de posiciones el indice
interno, luego el estado depende solo del octeto y del par de trigramas
inferiores (`results/proofs.tsv:37`).

Para cinco de las seis clases restantes hay testigo, y con el basta el Lema 2:

| clase | tamano | testigo (mascara por lineas) |
|---|---|---|
| (0, 2) | 96 | 4, 5, 6 |
| (0, 3) | 32 | 5 |
| (1, 0) | 96 | 1, 2, 3, 4, 5, 6 |
| (2, 0) | 96 | 1, 2, 3, 4, 5, 6 |
| (3, 0) | 32 | 1, 2, 4, 5 |

Los testigos estan en `results/certificates.txt` y su verificacion en
`results/proofs.tsv:117` a `:119`: 14 de las 15 clases tienen testigo, cubren
1920 pares y aportan 960. Estos cinco testigos se exhiben y se verifican; no se
argumentan en prosa, y por eso su uniformidad depende del orden de familia y del
orden interno recibidos, no solo de B6.

## 2.5 Mawangdui: la clase (0, 1), DEMOSTRADA por el Lema 3

La clase (0, 1), de 96 pares, **no tiene testigo uniforme**: se recorrieron los
2304 elementos del grupo y ninguno da epsilon igual a uno sobre toda la clase
(`results/proofs.tsv:120`). El Lema 2 no llega. El Lema 3 si.

**El cierre de relaciones.** Sobre los 96 pares de la clase se levanta el grafo
cuyas aristas son las parejas {p, q} para las que existe algun g del grupo con
g por p igual a q y epsilon(g, p) igual a uno. Tiene 2304 aristas
(`results/proofs.tsv:130`).

**Ese numero solo ya fija la cifra.** Toda arista une paridades contrarias, luego
si la clase de paridad uno tiene c elementos, el numero de aristas no puede pasar
de c por 96 menos c, cuyo maximo es 2304 y se alcanza solo en c igual a 48. Como
hay 2304 aristas, c vale 48 y la aportacion es 48. Comprobado recorriendo los
valores posibles de c (`results/proofs.tsv:131`, `:132`).

**El certificado explicito, mas corto de lo esperable.** El cierre admite
emparejamiento perfecto (`results/proofs.tsv:133`), y no hace falta variar el
testigo: 576 de los 2304 elementos bastan por si solos, cada uno con sus propias
48 parejas (`:134`, `:135`). El certificado que se deposita usa uno solo, el
primero en orden determinista: permutacion que intercambia las lineas 5 y 6,
seguida de complementar la linea 5 (`results/proofs.tsv:136`). Sus 48 parejas
parten la clase entera (`:137`, `:138`) y cada una verifica epsilon igual a uno
(`:139`).

El objeto esta en `results/certificate-mwd-01.txt`, una linea por pareja, con las
dos posiciones de origen, las dos de destino y los bits A y B que dan epsilon.
Cada linea se verifica por separado y ninguna mira ningun estado.

**Teorema.** La clase (0, 1) aporta exactamente 48 (`results/proofs.tsv:140`),
por el Lema 3 aplicado a ese emparejamiento. La cifra que antes estaba contada
ahora esta demostrada, y las dos coinciden (`:141`).

**Corolario.** Las 15 clases de Mawangdui estan forzadas con demostracion, luego
por el Lema 1 el recuento vale C(64,2) partido por dos, igual a 1008. **El empate
de Mawangdui queda demostrado entero, sin residuo enumerativo.**

## 2.6 Jing Fang: el grupo, DEMOSTRADO

**El palacio como traslacion de un conjunto fijo.** De las reglas se lee que las
ocho posiciones de un palacio de cabeza H son el hexagrama doblado (H, H) mas las
mascaras

    vacio, {1}, {1,2}, {1,2,3}, {1,2,3,4}, {1,2,3,4,5}, {1,2,3,5}, {5}

donde las cinco primeras son las generaciones que van cambiando lineas de abajo
arriba, la septima es el alma errante, que vuelve a cambiar la linea 4, y la
octava es el alma que vuelve, que restituye el trigrama inferior de la cabeza.
Ese conjunto M es el mismo en los ocho palacios (`results/proofs.tsv:38` a
`:40`), y las cabezas son exactamente la diagonal D, el subespacio de los
hexagramas cuyos dos trigramas coinciden (`:41`, `:42`).

**Los palacios parten los 64.** Ninguna de las 28 diferencias de M cae en D
(`results/proofs.tsv:43`, `:50`). Razon: la linea 6 no aparece en ninguna
diferencia, luego una diferencia en D no puede tocar la linea 3; y las
diferencias que no tocan la linea 3 son {1}, {1,2}, {2}, {1,5}, {5}, {4} y
{4,5}, ninguna de las cuales cumple que la linea 4 acompane a la 1 y la 5 a la
2. Luego los ocho por ocho sumandos son distintos y recorren los 64 (`:51`).

**Teorema.** El grupo R1 de Jing Fang es exactamente el de las traslaciones por
D, de orden 8.

**Demostracion.** Que las traslaciones por D estan dentro es inmediato: si m esta
en D, (p XOR M) XOR m = (p XOR m) XOR M, y p XOR m sigue en D por ser D
subespacio. Para el reciproco, sea f = P XOR m que respeta la particion. Las
diferencias dentro de un bloque son las de M, iguales en todos los bloques, y f
manda diferencias a P de las diferencias, luego P deja invariante el multi
conjunto de las 28 diferencias de M. La linea 6 no aparece en ninguna diferencia
y las demas si, luego P fija la linea 6. Las multiplicidades por linea son 12,
15, 16, 12, 15 y 0 (`results/proofs.tsv:44`, `:45`), asi que P fija la linea 3 y
a lo sumo puede intercambiar la 1 con la 4 y la 2 con la 5. Las multiplicidades
de las diferencias de una sola linea son 1, 1, 1, 2, 3 y 0
(`results/proofs.tsv:46`, `:47`): la de la linea 1 vale uno y la de la 4 vale
dos, la de la 2 vale uno y la de la 5 vale tres, luego ninguno de los dos
intercambios es admisible. El estabilizador es trivial y P es la identidad
(`:48`, `:49`). Queda f como traslacion por m, y una traslacion manda el bloque
p XOR M al bloque (p XOR m) XOR M, que es un bloque si y solo si m esta en D.
Orden 8 (`:52`, `:53`). Fin.

## 2.7 Jing Fang: las orbitas, DEMOSTRADO

Por 2.6 el grupo actua sobre las posiciones permutando los ocho palacios segun la
accion regular de D y dejando quieto el indice dentro del palacio.

**Teorema.** Hay 280 orbitas: 28 de pares dentro de un mismo palacio, de tamano
8; 56 de pares en palacios distintos con el mismo indice interno, de tamano 4; y
196 de pares en palacios distintos con indices distintos, de tamano 8.

**Demostracion.** Un par queda descrito por (b, k) y (b', k'). Trasladar por d
manda b a b XOR d y b' a b' XOR d, y no toca k ni k'. Si b es igual a b', los
ocho traslados dan ocho pares distintos y las orbitas quedan clasificadas por el
par de indices internos: C(8,2) igual a 28 orbitas de tamano 8, o sea 224 pares.
Si b es distinto de b' y k es igual a k', el traslado por d = b XOR b'
intercambia los dos elementos y deja el par igual, luego el estabilizador tiene
orden dos y la orbita tamano 4; hay 8 indices por C(8,2) igual a 28 pares de
palacios, o sea 224 pares en 56 orbitas. Si b es distinto de b' y k es distinto
de k', el estabilizador es trivial y la orbita tiene tamano 8; los pares son
8 por 8 por 7 por 7 partido por dos, igual a 1568, en 196 orbitas. Total 2016
pares y 280 orbitas. Fin.
Comprobado en `results/proofs.tsv:54` a `:57`.

## 2.8 Jing Fang: el empate, DEMOSTRADO

**Las 28 orbitas de dentro del palacio, con testigo argumentado.** La
complementacion es la traslacion por el elemento de D con todas las lineas, luego
esta en R1 (`results/proofs.tsv:58`). Sobre los valores manda v a 63 menos v, asi
que invierte el orden binario de cualquier par: B es uno siempre. Sobre las
posiciones manda cada palacio al de cabeza complementaria conservando el indice
interno; en el orden de familia recibido eso es sumar 32 a la posicion modulo 64.
Si los dos elementos del par estan en el mismo palacio, sus posiciones distan
menos de ocho, luego caen en la misma mitad y sumar 32 modulo 64 conserva su
orden: A es cero. Entonces epsilon es uno, y la complementacion no fija ninguno
de esos pares porque eso exigiria una distancia de 32. Por el Lema 2 esas 28
orbitas estan forzadas (`results/proofs.tsv:59` a `:62`).

**Las 252 restantes, con testigo exhibido.** Cada una tiene testigo dentro del
grupo, y el conjunto de testigos usados se reduce a tres elementos distintos.
Estan listados orbita por orbita en `results/certificates.txt` y verificados en
`results/proofs.tsv:123` a `:127`.

**Teorema.** Las 280 orbitas de Jing Fang estan forzadas, luego por el Lema 1 el
recuento vale C(64,2) partido por dos, igual a 1008.

Comprobado en `results/proofs.tsv:128`. El empate de Jing Fang queda demostrado
por completo, sin residuo enumerativo.

## 2.9 Lo que sigue siendo ENUMERATIVO en esta pieza

Nada.

| secuencia | pares demostrados | aportacion demostrada | pares contados | total |
|---|---|---|---|---|
| Mawangdui | 1920 por el Lema 2, mas 96 por el Lema 3 | 960 mas 48 | 0 | 1008 |
| Jing Fang | 2016 por el Lema 2 | 1008 | 0 | 1008 |

Origen: `results/proofs.tsv:118`, `:119`, `:125`, `:126`, `:129`, `:140`.

Los dos empates estan demostrados. Lo que queda abierto en este repositorio es
el residuo de 5 de King Wen, y solo eso.

---

# Pieza 3. King Wen

## 3.1 El sistema de bloques

Los 32 bloques son las 28 orbitas de tamano dos del giro rho mas los 4 pares que
forman por complementacion los 8 hexagramas que el giro deja quietos
(`results/proofs.tsv:71` a `:73`). Es una propiedad de la secuencia recibida,
medida en el commit de la medicion y vuelta a comprobar aqui. Todo lo que sigue
se demuestra a partir de ella.

Sea tau el companero de bloque: vale rho fuera de los palindromos y kappa sobre
ellos. Respetar los bloques equivale exactamente a conmutar con tau
(`results/proofs.tsv:74`), porque f manda el bloque {x, tau x} al conjunto
{f x, f(tau x)}, y ese conjunto es un bloque si y solo si f(tau x) es igual a
tau(f x).

## 3.2 El grupo es el centralizador del giro, DEMOSTRADO

**Observacion previa.** Toda aplicacion de B6 conmuta con la complementacion:
f(x XOR todo) = P(x) XOR P(todo) XOR m = f(x) XOR todo, porque P permuta
coordenadas y deja quieto el vector de todo unos (`results/proofs.tsv:75`).

**Teorema.** R1 de King Wen es exactamente el centralizador de rho en B6, de
orden 48 por 8, igual a 384.

**Demostracion.**

Primero, quien conmuta con rho respeta los bloques. Si f rho es igual a rho f,
entonces f manda orbitas del giro en orbitas del giro y palindromos en
palindromos; y por la observacion previa f({x, kappa x}) es {f x, kappa(f x)},
que para x palindromo vuelve a ser un bloque de la segunda familia.

Segundo, quien respeta los bloques conmuta con rho. Sea f = P XOR m que los
respeta. La diferencia de un bloque {x, tau x} vale x XOR rho x cuando x no es
palindromo, vector fijo por rho, y vale el vector de todo unos cuando si lo es,
que tambien es fijo por rho. El conjunto de diferencias de bloque es exactamente
Fix(rho) sin el cero (`results/proofs.tsv:76`), y f manda la diferencia de un
bloque a P de esa diferencia, luego P deja invariante Fix(rho). Ese subespacio
tiene ocho elementos y sus unicos elementos de peso dos son los tres vectores que
juntan la linea 1 con la 6, la 2 con la 5 y la 3 con la 4
(`results/proofs.tsv:77`, `:78`); como P conserva el peso, P permuta esos tres
vectores, y por tanto respeta el emparejamiento de lineas que define rho, es
decir P conmuta con rho: son 2 elevado a 3 por 3 factorial igual a 48
permutaciones (`:79`, `:80`). Falta la mascara. Para x no palindromo con f(x) no
palindromo, respetar el bloque obliga a f(rho x) = rho(f x), o sea
rho(P x) XOR m = rho(P x) XOR rho(m), luego m es fijo por rho. Tales x existen de
sobra, porque solo hay ocho palindromos y f es biyectiva. Las mascaras fijas por
rho son ocho (`:81`).

En total 48 por 8 igual a 384, que coincide con la enumeracion de B6
(`results/proofs.tsv:82` a `:84`). Fin.

## 3.3 La obstruccion de paridad, DEMOSTRADA

Sea T el grupo de las traslaciones por Fix(rho), de orden 8. Esta contenido en R1
(`results/proofs.tsv:85`) y es normal en el, porque conjugar la traslacion por v
da la traslacion por P(v) y P deja invariante Fix(rho) (`:86`). Ademas T actua
libremente sobre los hexagramas, porque una traslacion no nula no fija nada
(`:87`).

**Teorema.** Toda orbita de pares de posiciones bajo R1 tiene cardinal par.

**Demostracion.** Sea p = {x, y} un par, visto sobre hexagramas. Una traslacion
no nula que deje fijo el conjunto {x, y} tiene que intercambiar sus dos
elementos, luego el estabilizador de p dentro de T contiene la identidad y, a lo
sumo, la traslacion por x XOR y cuando ese vector este en Fix(rho): su orden es
uno o dos, y la T orbita de p tiene cardinal 8 o 4
(`results/proofs.tsv:100`, `:101`). Como T es normal en R1, el grupo permuta las
T orbitas y todas las contenidas en una misma R1 orbita tienen igual cardinal
(`:102`). Por tanto el cardinal de una R1 orbita es multiplo de 4, y en
particular par. Fin.

El mismo argumento vale para Mawangdui y para Jing Fang con sus respectivos
grupos de traslaciones, que tambien son normales y libres, y alli tambien sale
que ninguna orbita tiene cardinal impar (`results/proofs.tsv:88`, `:92`, `:96`).

**Corolario, la paridad esta determinada por la estructura.** La aportacion de
una orbita vale c_O o cardinal de O menos c_O, y como el cardinal es par las dos
opciones tienen la misma paridad. Luego el recuento total es congruente con la
suma de los c_O modulo dos, sea cual sea la eleccion de los bits libres. Para
King Wen esa suma es impar (`results/proofs.tsv:97`), y coincide con la paridad
del recuento observado (`:98`, `:99`).

**Corolario, el empate es imposible.** C(64,2) partido por dos es 1008, que es
par, y el recuento de King Wen es impar por el corolario anterior. Luego ninguna
eleccion de los bits libres da el empate, y el empate no esta entre los totales
compatibles con la estructura (`results/proofs.tsv:110`). Para Mawangdui y Jing
Fang la paridad estructural sale par (`:89`, `:93`), que es la de 1008 y no
contradice nada.

## 3.4 El residuo de 5, ABIERTO

Lo que la estructura deja: intervalo de 957 a 1059 (`results/proofs.tsv:103`,
`:104`), 52 totales compatibles (`:105`), todos de la misma paridad (`:106`), el
mas cercano al empate es 1007 (`:107`), y por tanto la desviacion minima posible
respecto del empate es 1 (`:108`). El recuento observado es 1013 (`:109`).

El residuo sobre el empate vale 5 (`results/proofs.tsv:111`). **No queda
demostrado ni explicado.** B6 se recorrio entero y el subgrupo respetado se tomo
completo; la estructura fija la paridad y acota el intervalo, y dentro de el
caben 52 valores. Por que el recibido es 1013 y no otro de los 52 es una
pregunta abierta, y se deja escrita como abierta.

---

# Pieza 4. Terminologia

La familia recorrida es el grupo hiperoctaedrico B6, grupo de simetrias del
6-cubo. **Correspondencia con la definicion local:** un elemento se escribe de
manera unica como permutacion de las seis lineas seguida de la complementacion de
un subconjunto de lineas, lo que en el 6-cubo es una permutacion de los ejes de
coordenadas seguida de reflexiones en hiperplanos coordenados.

Comprobado: el orden es 2 elevado a 6 por 6 factorial, igual a 46080
(`results/proofs.tsv:112`, `:113`); la escritura como permutacion y mascara es
unica, de modo que la parametrizacion no cuenta dos veces ningun elemento
(`:114`); la complementacion y el giro estan dentro (`:115`); y la accion
conserva la adyacencia del 6-cubo, es decir la relacion de diferir en una sola
linea (`:116`).

Ninguna otra alusion a literatura aparece en este documento.

---

# Medicion del control

Se recoge como medicion, con su procedencia, y sin lectura.

El grupo R1 depende solo de la particion en bloques, y barajar el orden de
familia no cambia esa particion; en las 300 repeticiones del control el grupo R1
salio identico al de la secuencia recibida, en octetos y en palacios
(`results/group-measurements.tsv:203`, `:209`). Semilla 20260809 (`:201`), 300
repeticiones por variante, muestra de los 40320 ordenes (`:202`).

| variante | anchura cero | recuento observado igual a 1008 | repeticiones | origen |
|---|---|---|---|---|
| octetos | 8 | 27 | 300 | `results/group-measurements.tsv:204`, `:206` |
| palacios | 0 | 3 | 300 | `:210`, `:212` |

Las dos secuencias recibidas tienen anchura cero
(`results/group-measurements.tsv:58`, `:115`).

---

# Resumen del reparto

| afirmacion | estado |
|---|---|
| Lema 0, relacion de estado | DEMOSTRADO, argumento |
| Lema 0b, cocadena, y el colapso de las cadenas | DEMOSTRADO, argumento |
| Lema 1, el empate como unico valor forzable | DEMOSTRADO, argumento |
| Lema 2, criterio de orbita forzada | DEMOSTRADO, argumento |
| Lema 3, forzado por emparejamiento | DEMOSTRADO, argumento |
| Mawangdui, grupo de orden 2304 | DEMOSTRADO, argumento |
| Mawangdui, 15 orbitas y sus tamanos | DEMOSTRADO, argumento |
| Mawangdui, 9 clases forzadas | DEMOSTRADO, testigo argumentado |
| Mawangdui, 5 clases mas forzadas | DEMOSTRADO, testigo exhibido |
| Mawangdui, la clase (0,1) forzada | DEMOSTRADO, Lema 3 con certificado |
| Mawangdui, el empate en 1008 | DEMOSTRADO |
| Jing Fang, grupo de orden 8 | DEMOSTRADO, argumento |
| Jing Fang, 280 orbitas y sus tamanos | DEMOSTRADO, argumento |
| Jing Fang, 28 orbitas forzadas | DEMOSTRADO, testigo argumentado |
| Jing Fang, las otras 252 forzadas | DEMOSTRADO, testigo exhibido |
| Jing Fang, el empate en 1008 | DEMOSTRADO |
| King Wen, grupo igual al centralizador del giro | DEMOSTRADO, argumento |
| King Wen, toda orbita de cardinal par | DEMOSTRADO, argumento |
| King Wen, paridad del recuento fijada por la estructura | DEMOSTRADO, argumento |
| King Wen, empate imposible | DEMOSTRADO, argumento |
| King Wen, residuo de 5 | ABIERTO |
| B6, orden y correspondencia | DEMOSTRADO |

## Reproducir

    python src/measure.py
    python src/group.py
    python src/proofs.py
