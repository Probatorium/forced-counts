# Revision de antecedentes

**Estado: ABIERTA.** Abierta no es cerrada. Mientras este fichero diga ABIERTA,
en este repositorio no se afirma novedad de nada, ni siquiera de lo que aqui
aparezca sin antecedente localizado. Que una busqueda no encuentre dueno no es
prueba de que no lo haya.

Fecha de apertura: 2026-08-09.

## Doctrina, escrita antes de registrar nada

Las reglas de los carriles anteriores, aplicadas aqui:

1. **Veredictos solo desde artefactos leidos.** Decir que una pieza dice tal
   cosa exige haber leido la pieza. No vale el resumen de un buscador, ni el
   resumen de un tercero, ni la memoria.
2. **Lo demas es segunda mano, con cadena de cita declarada.** Una pieza de
   segunda mano se registra diciendo de quien viene la noticia y por que via.
   Se puede registrar; no se puede usar para un veredicto.
3. **Toda cifra con puntero o se devuelve.** Una cifra sin fuente localizable no
   entra. Si entra citada de segunda mano, se marca como tal y no se usa en
   ningun computo.
4. **Coincidencia no es derivacion.** Que dos trabajos den con el mismo hecho no
   dice por si solo quien lo tomo de quien. Cuando hay fecha anterior, se dice
   quien la tiene, y se dice tambien si la via fue independiente.
5. **La interseccion se declara aunque duela.** Si un artefacto anterior ya
   tiene un resultado de este repositorio, se escribe, se cita en el sitio donde
   ese resultado vive, y no se maquilla.

## Estado de cada pieza

| pieza | estado | registro |
|---|---|---|
| Radisic, arXiv:2601.07175v3 | **ARTEFACTO LEIDO**, entero, 11 paginas | seccion 1 |
| Colision de "balance": Radisic 4.3 | **ARTEFACTO LEIDO** | seccion 2 |
| Colision de "balance": codigos de Gray | **SEGUNDA MANO**, pendiente de artefacto | seccion 2 y 3 |
| Cook 2006, STEDT Monograph 5 | **SEGUNDA MANO**, pendiente | seccion 3 |
| Gritter, "The Hidden Pattern" | **SEGUNDA MANO**, pendiente | seccion 3 |
| Moore, "Structural Elements" | **SEGUNDA MANO**, pendiente | seccion 3 |
| Resena de Drasny | **SEGUNDA MANO**, pendiente | seccion 3 |
| Schoter, "Boolean algebra and the Yijing" | **SEGUNDA MANO**, pendiente | seccion 3 |
| Mutze, survey de codigos de Gray | **SEGUNDA MANO**, pendiente | seccion 3 |
| Observacion folk de paridad de transiciones | **SEGUNDA MANO**, pendiente | seccion 3 |

Nada mas se ha buscado todavia. La lista de pendientes no pretende ser completa.

---

# 1. Registro de artefacto leido: Radisic 2026

## 1.1 Identidad completa

- Autor: Alejandro Radisic. Correo impreso en la portada: `aleloid@proton.me`.
- Titulo: "Optimal Equivariant Matchings on the 6-Cube: With an Application to
  the King Wen Sequence".
- Identificador: arXiv:2601.07175v3 [math.GM]. La marca lateral de la portada
  dice 25 de mayo de 2026; la fecha bajo el autor dice 27 de mayo de 2026.
- Extension: 11 paginas, apendice A incluido.
- Referencias del articulo: dos. [1] Wilhelm y Baynes, *The I Ching or Book of
  Changes*, Princeton University Press, 1967. [2] Leibniz, *Explication de
  l'arithmetique binaire*, 1703.
- Como se leyo: el PDF descargado de arXiv en la sesion anterior, leido pagina a
  pagina, las once. La sesion anterior habia leido solo resumen, introduccion y
  paginas 9 a 11; esta lectura completa la cubre entera.

## 1.2 Que demuestra

Notacion del articulo: un hexagrama es un elemento de {0,1} elevado a 6, con las
posiciones indexadas de 0, la inferior, a 5, la superior (Definicion 2.1).
`comp(h)(i) = 1 - h(i)` y `rev(h)(i) = h(5-i)` (Definicion 2.5). Las dos
conmutan y generan el grupo de Klein K4 (Proposicion 2.6).

- **Proposicion 2.8**, tipos de orbita bajo K4: 48 hexagramas genericos en 12
  orbitas de tamano 4; 8 palindromos en 4 orbitas de tamano 2; 8 antisimetricos
  en 4 orbitas de tamano 2.
- **Proposicion 2.11**: la distancia de Hamming a comp es siempre 6; a rev es a
  lo sumo 6, con igualdad si y solo si el hexagrama es antisimetrico.
- **Lema 2.12**, No-Conflict: para cada hexagrama, o rev es estrictamente mas
  barato que comp, o coinciden, o rev es trivial por ser palindromo. Nunca
  compiten de verdad.
- **Teorema 3.3**, Complete Equivariance: todo par de King Wen cumple
  `h2 = comp(h1)` o `h2 = rev(h1)`, y los 32 pares se reparten en 4 palindromos
  emparejados por complemento a distancia 6, 4 antisimetricos emparejados por
  reversion, que ahi coincide con complemento, a distancia 6, y 24 genericos
  emparejados por reversion a distancia 2 o 4. La prueba impresa es
  computacional sobre los 32 pares, con la tactica `decide` de Lean 4.
- **Corolario 3.4**: el emparejamiento de King Wen respeta K4, los dos miembros
  de un par caen siempre en la misma orbita.
- **Teorema 4.2**: la funcion companero de la regla de prioridad de reversion es
  una involucion.
- **Teorema 4.4** y **Teorema 1.1**: entre los emparejamientos equivariantes que
  usan solo comp o rev, el de prioridad de reversion minimiza el coste total de
  Hamming, y es unico.
- **Corolario 4.10**: coste 24 por los palindromos, 24 por los antisimetricos,
  72 por los genericos, total **120**, frente a **192** del emparejamiento que
  usa solo complemento.
- **Proposicion 4.6**: si se admiten los tres emparejamientos no triviales de
  K4, el minimo puro de Hamming baja a **96**, luego King Wen no es el optimo de
  Hamming sin restricciones (Observacion 4.5).
- **Proposicion 4.7**: la regla falla la conservacion del peso de Hamming
  exactamente en los 8 extremos palindromicos, y ese fallo es inevitable para
  cualquier emparejamiento K4 equivariante no trivial.
- **Teorema 4.8**, optimalidad lexicografica: primero minimizar fallos de
  conservacion del peso de Hamming, despues minimizar coste total de Hamming.
  Ese criterio selecciona la regla de prioridad de reversion.
- **Teorema 4.9** y **Teorema 1.3**, estabilidad de fase: con la energia
  `E(h,h') = alfa por |w(h) - w(h')| + beta por d_H(h,h')`, en toda orbita de
  tamano 4 con `d_H(h, rev h) = 4` la arista de reversion gana exactamente
  cuando alfa es mayor que beta, y empatan en alfa igual a beta.
- **Teorema 4.11** y **Corolario 4.12**: unicidad, y King Wen como el
  emparejamiento comp/rev equivariante canonico.
- **Seccion 5.3**, verificacion formal en Lean 4 con Mathlib, con los modulos
  `IChing/Hexagram.lean`, `Symmetry.lean`, `KingWenOptimality.lean`,
  `WeightConservation.lean` y `RobustOptimality.lean`.
- **Seccion 5.4**: solo complemento da emparejamiento valido de coste 192; solo
  reversion no da emparejamiento valido, porque los 8 palindromos no pueden
  emparejarse consigo mismos.
- **Seccion 5.5**: la extension a n general no se demuestra; se senala que el
  perfil de empate exigiria `d_H(h, rev h) = m` y `w(h) = m` en n igual a 2m, lo
  que ocurre exactamente cuando 8 divide a n, y que n igual a 6 cae en el lado
  rigido.
- **Apendice A**: la tabla binaria completa de King Wen, ya transcrita y cotejada
  en el commit anterior, con las 64 posiciones coincidentes.

## 1.3 Que NO hace

Comprobado por lectura de las once paginas, no por ausencia en un resumen:

- **No define ninguna nocion de orden de posiciones.** La secuencia de King Wen
  entra solo por su emparejamiento, los pares `(h_2k, h_2k+1)` de la Definicion
  3.2. El orden en que van los 32 pares entre si no juega ningun papel en ningun
  enunciado.
- **No mide inversiones contra ninguna ordenacion de referencia.** No aparece el
  orden binario como objeto de comparacion, ni Kendall, ni ningun recuento de
  pares discordantes. Su unica magnitud sobre pares es la distancia de Hamming,
  y su unico agregado es el coste total del emparejamiento.
- **Su grupo es K4, de orden 4, no un subgrupo de B6.** El articulo trabaja con
  `{id, comp, rev, comp o rev}` y no considera otras permutaciones de las seis
  lineas. La relacion exacta, que se dice aqui y no esta en el articulo: K4 es
  un subgrupo de orden 4 del grupo hiperoctaedrico B6, y esta contenido en el
  centralizador de rev en B6, que es el grupo de orden 384 que este repositorio
  enumera en PROOFS.md 3.2.
- **No aparecen ni Mawangdui ni Jing Fang.** El articulo es solo sobre King Wen.
- **No aparece el codigo de Gray.**
- **No aparece ningun empate ni ninguna cifra cercana a 1008 ni a 1013.**

## 1.4 La interseccion, declarada

**Hay interseccion, y es exacta en un punto.**

El **Teorema 3.3** de Radisic y la caracterizacion que este repositorio usa en
PROOFS.md 3.1 son **el mismo hecho estructural**. Aqui se escribe como 28
orbitas de reversion de tamano dos mas 4 pares de palindromos emparejados por
complemento; alli se escribe como 24 genericos mas 4 antisimetricos mas 4
palindromos. Las dos particiones describen los mismos 32 bloques: los 28 de aqui
son los 24 genericos mas los 4 antisimetricos de alli, que tambien son orbitas
de reversion de tamano dos, separados por Radisic porque en ellos reversion y
complemento coinciden.

**Dueno anterior: Radisic**, por fecha, y ademas con verificacion formal en Lean
4, que aqui no hay. La via de este repositorio fue independiente, porque la
caracterizacion se obtuvo y se commiteo antes de abrir esta revision y antes de
tener noticia del articulo, y la historia de git lo deja fechado. Independiente
no quiere decir primero: quiere decir que no se tomo de alli.

**Consecuencia registrada:** PROOFS.md pieza 3 recibe una linea de cita, en
commit propio, y esa es la unica edicion que se le hace.

**Lo que NO esta en la interseccion**, y conviene tenerlo separado: la
identificacion del grupo respetado como el centralizador de rev dentro de B6 y
su orden 384; la contabilidad forzado frente a libre por orbitas de pares de
posiciones; la obstruccion de paridad y la imposibilidad del empate; y todo lo
que tiene que ver con recuentos de inversiones. Nada de eso aparece en el
articulo. **Y nada de eso se afirma nuevo**, porque la revision esta abierta y
solo se ha leido un artefacto.

---

# 2. Colision terminologica medida: la palabra "balance"

Dos ocupantes impresos, vecinos del objeto que aqui se mide, y ninguno de los
dos es ese objeto.

**Ocupante 1, ARTEFACTO LEIDO.** Radisic, seccion 4.3, pagina 7, define el peso
`w(h)` como el numero de posiciones a uno y escribe, literalmente: "In the I
Ching interpretation, this counts the number of yang lines, so Hamming-weight
preservation may be viewed as preservation of yin-yang balance. Formally, it is
Hamming weight." Es decir que alli **balance es peso de Hamming**, y el propio
autor aclara acto seguido que formalmente es peso de Hamming y nada mas.

**Ocupante 2, SEGUNDA MANO.** En la literatura de codigos de Gray, *balanced*
refiere a los recuentos de transicion por coordenada, esto es a repartir por
igual cuantas veces cambia cada bit a lo largo del ciclo. **Esta afirmacion es
de segunda mano y no tiene artefacto leido detras**: entro en este repositorio
en INFORME-GRAY.md como frase de deslinde y su cadena de cita es el conocimiento
general del asistente que la escribio, no una fuente localizada. Queda pendiente
de artefacto, con el survey de Mutze como candidato, en la seccion 3.

**Regla que se fija aqui.** El empate en C(64,2) partido por dos **no se llamara
balance** en ningun texto de este repositorio sin frase de deslinde inmediata
que lo separe de los dos ocupantes de arriba. El nombre preferido sigue siendo
empate, y donde haga falta precision, empate del recuento de inversiones contra
el orden binario. INFORME-GRAY.md ya lleva su deslinde contra el ocupante 2;
ningun texto lleva todavia deslinde contra el ocupante 1, que aparece aqui por
primera vez.

---

# 3. Segunda mano, pendientes de artefacto

Ninguna de estas piezas se ha leido. Todas entran con la misma cadena de cita:
**el autor del repositorio las nombro en la instruccion que abrio esta
revision**, en la sesion 8. No se ha verificado ni su contenido ni sus datos
bibliograficos, y las cifras que aparecen abajo son las que dio esa instruccion,
no cifras medidas ni comprobadas contra ninguna fuente.

## 3.1 Cook 2006

- Datos tal como se recibieron: Cook, 2006, STEDT Monograph 5, ISBN
  0-944613-44-6, 660 paginas.
- Noticia recibida: pretende **derivar** la secuencia de King Wen.
- **Distincion que hay que sostener cuando se lea:** este repositorio **no
  deriva** la secuencia. Computa que fuerza la simetria que su construccion
  respeta, y deja explicitamente abierto por que el recuento es 1013 y no otro
  de los 52 compatibles. Derivar y computar lo forzado son dos programas
  distintos, y confundirlos seria un error de lectura en las dos direcciones.
- Prioridad de lectura: alta. Es la pieza que mas puede solaparse.

## 3.2 Gritter, "The Hidden Pattern"

Noticia recibida, sin mas datos. Pendiente de localizar edicion y de leer.

## 3.3 Moore, "Structural Elements"

Noticia recibida, sin mas datos. Pendiente de localizar edicion y de leer.

## 3.4 La resena de Drasny

Noticia recibida: existe una resena de Drasny, presumiblemente de alguna de las
piezas anteriores. Pendiente de localizar de que obra es resena y de leerla.

## 3.5 Schoter, "Boolean algebra and the Yijing"

Noticia recibida, sin mas datos. Por el titulo, es la pieza mas cercana al
tratamiento del hexagrama como vector booleano, que es el punto de partida de
todo lo que aqui se hace. Prioridad de lectura: alta.

## 3.6 El survey de Mutze sobre codigos de Gray

Noticia recibida. Es el candidato a artefacto para el ocupante 2 de la colision
de la seccion 2, es decir para fijar que significa *balanced* en esa literatura.
Hasta que se lea, la frase de deslinde de INFORME-GRAY.md sigue siendo de
segunda mano y asi queda marcada aqui.

## 3.7 La observacion folk de paridad de transiciones de King Wen

- Noticia recibida: circula la observacion de que las transiciones de King Wen
  se reparten en **48 pares y 16 impares, razon 3 a 1**.
- **Cifras sin puntero.** No hay fuente localizada. Se registran como recibidas
  y **no se usan en ningun computo**.
- **Nota aritmetica, para quien vaya a buscar el artefacto:** 48 mas 16 son 64,
  mientras que una secuencia de 64 hexagramas tiene 63 transiciones
  consecutivas. O la observacion cuenta otra cosa, o cuenta 64 transiciones
  cerrando el ciclo, o alguna de las dos cifras viene mal transmitida. No se
  resuelve aqui, se deja senalado.
- **Deslinde obligatorio cuando se lea, y ya desde ahora:** aunque las dos cosas
  lleven la palabra paridad, **la observacion folk y la obstruccion de paridad
  de PROOFS.md 3.3 son objetos distintos**. La folk habla de **transiciones
  entre hexagramas consecutivos** de la secuencia. La obstruccion de PROOFS.md
  habla de la **paridad del recuento de inversiones sobre pares de posiciones no
  adyacentes**, que sale de que toda orbita del grupo tenga cardinal par. No
  comparten objeto, ni unidad de conteo, ni demostracion. Cualquier texto que
  las ponga cerca lleva esta frase al lado.

---

# 4. Que NO autoriza esta revision

- **No autoriza a afirmar novedad de nada.** Abierta no es cerrada. Se ha leido
  un artefacto de una lista que ni siquiera esta completa.
- **No autoriza a dar por libre lo que no se ha buscado.** El silencio de esta
  lista sobre un resultado no dice nada sobre ese resultado.
- **No autoriza a cerrar la interseccion con Radisic con la linea de cita.** La
  linea deja constancia; cerrar exigiria haber leido lo suficiente como para
  saber que mas hay.
- Cuando se cierre, se dira aqui, con fecha, y con la lista de lo leido.
