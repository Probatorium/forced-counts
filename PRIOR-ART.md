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

Actualizado en la sesion 9. Las filas que cambiaron de estado lo dicen.

| pieza | estado | registro |
|---|---|---|
| Radisic, arXiv:2601.07175v3 | **ARTEFACTO LEIDO**, entero, 11 paginas | seccion 1 |
| Colision de "balance": Radisic 4.3 | **ARTEFACTO LEIDO** | seccion 2 |
| Colision de "balance": codigos de Gray | **ARTEFACTO LEIDO** en la sesion 9, antes segunda mano | seccion 7 |
| Cook 2006, STEDT Monograph 5 | **ARTEFACTO LEIDO** en parte: resena entera mas barridos del texto completo | seccion 5.4 |
| Gritter, "The Hidden Pattern" | **ARTEFACTO LEIDO**, entero | seccion 5.1 |
| Moore, "Structural Elements" | **ARTEFACTO LEIDO**, canal OCR | seccion 5.2 |
| Resena de Drasny | **ARTEFACTO LEIDO**, entera | seccion 5.4 |
| Schoter, "Boolean algebra and the Yijing" | **ARTEFACTO LEIDO** | seccion 5.3 |
| Mutze, survey de codigos de Gray | **ARTEFACTO LEIDO** en la parte citada, verificada contra el PDF | seccion 7 |
| Bjorner y Brenti, Coxeter groups | **ARTEFACTO LEIDO** en la parte citada, verificada contra el PDF | seccion 8 |
| Colision de "inversion" en el Yijing | **MEDIDA** en cuatro artefactos | seccion 6 |
| Observacion folk de paridad de transiciones | **MEDIDA AQUI** en la sesion 11; la observacion sigue sin dueno localizado | secciones 3.7, 9 y 13 |
| Propp y Roby, arXiv:1310.5201v6 | **ARTEFACTO LEIDO** en las partes citadas, verificadas contra el PDF | seccion 14.1 |
| Roby, survey de homomesia (IMA) | **ARTEFACTO LEIDO** en las partes citadas, verificadas contra el PDF | seccion 14.2 |
| Reiner, Stanton y White, cyclic sieving | **ARTEFACTO LEIDO** en identidad y definicion | seccion 14.3 |
| Goldenberg 1975, Davis 1998, Higgins 1998, Hacker y Moore 2003, Hacker, Moore y Patsco 2002, Mesker 2002, Moore 1989 | **SEGUNDA MANO**, pendientes | secciones 9 y 12 |

La lista de pendientes no pretende ser completa.

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

> **SUPERADA EN PARTE en la sesion 9.** Gritter, Moore, Schoter, Cook por la via
> de su resena, y Mutze pasaron a artefacto leido en la seccion 5 y siguientes.
> Esta seccion se deja tal cual se escribio, sin corregir, para que se vea que
> entraron primero como noticia y despues como lectura. Solo sigue viva la 3.7,
> la observacion folk, que no tiene dueno localizado.

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
> **MEDIDA en la sesion 11.** La nota aritmetica de arriba queda resuelta:
> la observacion cierra el ciclo y cuenta 64 transiciones. Ver la seccion 13.
> Lo demas de este apartado sigue en pie, el deslinde incluido.

- **Deslinde obligatorio cuando se lea, y ya desde ahora:** aunque las dos cosas
  lleven la palabra paridad, **la observacion folk y la obstruccion de paridad
  de PROOFS.md 3.3 son objetos distintos**. La folk habla de **transiciones
  entre hexagramas consecutivos** de la secuencia. La obstruccion de PROOFS.md
  habla de la **paridad del recuento de inversiones sobre pares de posiciones no
  adyacentes**, que sale de que toda orbita del grupo tenga cardinal par. No
  comparten objeto, ni unidad de conteo, ni demostracion. Cualquier texto que
  las ponga cerca lleva esta frase al lado.

---

# 5. La tanda de la sesion 9: cuatro piezas del Yijing

## 5.0 Fuente y canal, declarados antes de los veredictos

Todo lo de esta seccion sale de `github.com/Probatorium/common`, carpeta
`proyecto-bibliografias`, clonada en el area temporal de la sesion. Su README
declara el canal, y se copia lo que importa: los `.md` son conversion verbatim
de cada PDF, extraccion de texto ordenada por posicion en la pagina, con
marcadores `--- pagina N ---` para poder situar cualquier pasaje contra el PDF;
`Moore_Structural_Elements.md` es **OCR con Tesseract**, porque su PDF es un
escaneo de imagen sin capa de texto; y `Drasny_Marshall_Resena_Cook.md` es
conversion de la pagina web `https://www.biroco.com/yijing/cook.htm`, sin PDF
equivalente.

El mismo README advierte, y se respeta aqui, que en los ficheros largos con
matematica (Cook, Mutze, Bjorner y Brenti, Yu) **la prosa se verifico pero las
formulas, diagramas y ejemplos numericos no tienen garantia de orden**, porque
la tipografia bidimensional no tiene un orden de lectura lineal unico. Regla que
se aplica en consecuencia: **para cualquier formula que se cite, el canal fuerte
es el PDF**, y asi se ha hecho en las secciones 7 y 8.

Los barridos de esta seccion se corrieron sobre los `.md`, que es donde se puede
buscar. Un barrido negativo sobre un `.md` es evidencia buena para palabras de
prosa y evidencia debil para simbolos.

## 5.1 Gritter, "The Hidden Pattern", ARTEFACTO LEIDO entero

- Identidad: Gert Gritter, *The Hidden Pattern in the classical sequence of the
  I Ching*. Cierre del texto: "Groningen, 2015". Dice que noto el patron en
  diciembre de 2010. 13 paginas en la conversion.
- Que hace: reordena los 32 pares de King Wen en una figura que llama **the
  Grid**, con los 16 hexagramas de trigramas identicos u opuestos en la columna
  central, y lee en ella simetria, complementariedad entre los dos canones, y
  una serie de correspondencias numericas con 360, 72, 60, 30, 12 y 6.
- Que no hace: no hay recuento de inversiones, ni ordenacion de referencia, ni
  grupo, ni nada forzado por simetria. Es un trabajo de disposicion visual y
  lectura numerologica.
- **Veredicto: no cuenta inversiones contra el binario y no conoce forzado por
  grupo.**

## 5.2 Moore, "Structural Elements", ARTEFACTO LEIDO, canal OCR

- Identidad, leida en la propia portada: Steve Moore, *Structural Elements in
  the King Wen Sequence of Hexagrams*, **Oracle Paper No. 1, February 2005**,
  copyright 2005 Steve Moore. El canal es OCR, con el ruido que el README
  anuncia; se cita prosa, no cifras sueltas.
- Que hace: analiza la estructura de la secuencia recibida por pares. Recoge que
  56 hexagramas forman 28 pares invertibles y los otros ocho van por oposicion.
  Clasifica los 32 pares por reparto de lineas yin y yang y por posicion par o
  impar del par. Discute ademas a Jing Fang y la disposicion de Mawangdui, que
  son objetos de este repositorio.
- Vecino peligroso, que se registra: Moore hace un recuento de tipo paridad,
  pero de **otro objeto**. Cuenta cuantos pares tienen reparto de lineas
  equilibrado y cuantos estan en posicion correcta segun preponderancia de yin o
  de yang. Nada de eso es la paridad del recuento de inversiones de PROOFS.md
  3.3, que sale del cardinal par de las orbitas del grupo.
- **Veredicto: no cuenta inversiones contra el binario y no conoce forzado por
  grupo.**

## 5.3 Schoter, "Boolean Algebra and the Yi Jing", ARTEFACTO LEIDO

- Identidad, tomada de la nota al titulo del propio articulo: Andreas Schoter,
  *Boolean Algebra and the Yi Jing*, publicado en **THE ORACLE: THE JOURNAL OF
  YIJING STUDIES, Vol 2, No 7, Summer 1998, pp 19 a 34. ISSN 1463-6220**.
- Que hace: monta un algebra de Boole sobre los gua, con not, or, and y xor,
  define el orden parcial inducido `x <= y` si y solo si `x|y = y`, dibuja los
  reticulos de bigramas y trigramas, y aplica todo ello a las relaciones de
  Cleary y a la representacion del cambio.
- **Vecindad fuerte, que hay que declarar.** Su seccion 2.4, Definicion 6,
  "Sequence Parameters", parametriza las ordenaciones por conteo con tres
  variables, y la primera es literalmente **"whether the lower or upper line is
  the least significant bit"**. Eso es exactamente el parametro de orientacion
  de las cuatro convenciones de PREREGISTRATION.md. Schoter llama **Rising
  Yang** a la lectura con la linea inferior como bit menos significativo y
  **Sinking Yang** a la contraria. La eleccion de polaridad, yang como uno o
  como cero, no la parametriza. **Este repositorio no puede presentar el
  parametro de orientacion como algo suyo.**
- Coincidencia de numero que conviene no leer de mas: Schoter escribe que hay
  "8! or 40,320 possible ways of arranging the gua into sequences", y 40320
  aparece tambien en el control de este repositorio como el numero de ordenes de
  familia. Son 8 factorial las dos veces y objetos distintos las dos veces.
- Que no hace: su orden es el **parcial del reticulo**, no un orden total de
  referencia contra el que medir; y no hay recuento de discordancias, ni grupo
  actuando, ni nada forzado.
- **Veredicto: no cuenta inversiones contra el binario y no conoce forzado por
  grupo.**

## 5.4 Cook 2006, por la resena de Drasny y por barridos del texto completo

- Identidad, tomada de la cabecera de la resena: Richard S. Cook, *Classical
  Chinese Combinatorics: Derivation of the Book of Changes Hexagram Sequence*,
  University of California, Berkeley, STEDT Monograph Series, Vol. 5, 2006,
  **xviii + 642 paginas**, ISBN 0-944613-44-6. El PDF de la conversion tiene 664
  paginas. La cifra de 660 que circulaba es la suma xviii mas 642.
- Resena: Jozsef Drasny, *The solution of the King Wen sequence?*, en Yijing
  Dao, `https://www.biroco.com/yijing/cook.htm`, con agradecimiento a Steve
  Marshall. **Leida entera.**
- Que hace Cook, segun la resena: inventa una "n-gram science", clasifica
  monogramas, digramas, trigramas, tetragramas y hexagramas por invertibilidad,
  genero, pureza, nucleares y numero de lineas, y con esas reglas construye un
  procedimiento que, partiendo del orden natural binario de Shao Yong comprimido
  en 36 clases HEC, regenera la secuencia recibida. Es un programa de
  **derivacion**.
- Veredicto de la resena sobre Cook, que se recoge como lo que es, la opinion de
  Drasny y no la de este repositorio: que el resultado final era conocido al
  empezar, que el procedimiento no es una demostracion matematica, y que la
  teoria le queda sin probar. Drasny cita al propio Cook, pagina 505: "This
  sequence derivation is not a formal mathematical proof of the kind to which
  modern mathematicians are accustomed."
- **Distincion que este repositorio sostiene:** aqui **no se deriva** la
  secuencia. Se computa que fuerza la simetria que su construccion respeta, y
  se deja escrito y abierto por que el recuento es 1013 y no otro de los 52
  compatibles. Derivar y computar lo forzado son programas distintos.
- **Barridos sobre el texto completo convertido**, 1.36 MB. Apariciones:
  Kendall 0, discordant 0, "pairwise disagreement" 0, "transposition distance"
  0, "inversion count" 0, "number of inversions" 0, "rank correlation" 0,
  "permutation distance" 0, "sortedness" 0.
- **Cifras nuestras dentro de Cook, miradas una a una y ninguna es un recuento:**
  1008 aparece una vez y es la referencia de diccionario `HDZ:1008`; 1017
  aparece una vez y es un fragmento de un diagrama que la extraccion dejo
  ilegible; 496 aparece cuatro veces y son una columna de una tabla de recuentos
  de n-gramas para n igual a 10, otra referencia `HDZ:496`, un marcador de
  pagina, y la entrada del glosario que dice que 496 es el tercer numero
  perfecto. Ninguna de las tres cifras es un recuento de inversiones. 1013 no
  aparece.
- **Veredicto: no cuenta inversiones contra el binario y no conoce forzado por
  grupo.** Con el limite de que el veredicto se apoya en la resena entera mas
  barridos del texto completo, no en la lectura completa de 642 paginas.

## 5.5 Lo que las cuatro tienen en comun

Ninguna de las cuatro mide una discordancia entre la secuencia recibida y una
ordenacion de referencia, y ninguna hace actuar un grupo sobre pares de
posiciones para ver que queda determinado. El objeto de este repositorio no
aparece en ellas. **Eso no autoriza a llamarlo nuevo**: son cuatro piezas de una
lista que sigue abierta.

---

# 6. Quinta colision: la palabra "inversion"

**Medida en cuatro artefactos.** En la literatura del Yijing, inversion nombra
el **giro de 180 grados** del hexagrama, que es lo que este repositorio llama
giro y escribe rho. No nombra el par discordante.

| artefacto | lema que aparece | apariciones | termino chino |
|---|---|---|---|
| Gritter | "inversion" | 4 | *fandui*, en la nota 2 de la pagina 3 |
| Cook | "inversion" y "obversion" | 92 y 100 | capitulo "Hexagram inversion and obversion" |
| Drasny | "inverses of hexagrams" | 1 | *zonggua*, y *cuogua* para el obverso |
| Moore | "invertible", "inverted" | 9 | no da termino chino |

Precision que hay que hacer, porque el barrido tonto engana: la cadena exacta
"inversion" **solo** aparece en Gritter y en Cook. En Moore y en Drasny la misma
nocion viene con otro lema. Contar por la cadena y no por la nocion habria dado
dos, y el resultado correcto es cuatro.

Cita de Gritter, pagina 3, nota 2: "The Chinese terms are pangtong (opposition)
en fandui (inversion)." Cita de Drasny: "There are inverses of hexagrams
(*zonggua*), 'obverses' of hexagrams (*cuogua*, 'obverse' being an odd word to
use for complementary)".

**Decision de vocabulario: RESERVADA a Alexis.** Las opciones sobre la mesa son
llamarlos "discordant pairs" o seguir con "inversions" acompanado de deslinde en
primera aparicion. **Hasta que decida, ninguna prosa nueva de este repositorio
usa el termino.** Los textos ya commiteados se quedan como estan; esta es una
regla para lo que se escriba desde aqui.

> **RESUELTA.** La decision se tomo y esta registrada en la seccion 11. Este
> parrafo se deja como se escribio, con su reserva, para que se vea que la
> decision no la tomo quien escribia.

---

# 7. Cerrado el pendiente de Mutze: que es *balanced* en codigos de Gray

**ARTEFACTO LEIDO**, y la formula verificada contra el PDF, que es el canal
fuerte, no contra la conversion.

- Identidad: Torsten Mutze, *Combinatorial Gray codes, an updated survey*, The
  Electronic Journal of Combinatorics 30(3) (2023), Dynamic Survey #DS26.
- **Cita literal, seccion 3.2 "Transition counts", pagina impresa 11:**
  "Specifically, let c_i denote the number of times that bit i is flipped along
  a given Gray cycle, where we number bits from right to left with i = 1, ..., n.
  Clearly, each transition count c_i must be an even number, and they sum up to
  2^n, so we require that each c_i is approximately equal to 2^n/n. Formally, in
  a *balanced Gray code*, we require that |c_i - 2^n/n| < 2 for i = 1, ..., n."
- **Segundo sentido en el mismo survey**, seccion 2.2: la *balancedness
  constraint* de un grafo de flips, que compara los tamanos de las clases de una
  particion bipartita o k-partita como obstruccion a la hamiltonicidad. Aparece
  ademas en otras variantes a lo largo del survey, como los posets balanceados y
  las transposiciones balanceadas.
- **Dato que toca directamente a nuestra cuarta ordenacion:** el propio survey
  dice del codigo de Gray reflejado que "in the BRGC, we have c_i = 2^{n-i} for
  i = 1, ..., n-1 and c_n = 2, i.e., it is very unbalanced". Es decir que la
  ordenacion de comparacion que este repositorio anadio es, en el sentido de
  Mutze, muy desbalanceada.

Con esto queda cerrado el pendiente. La marca de segunda mano que llevaba el
deslinde de INFORME-GRAY.md se resuelve **por enmienda visible al pie de ese
fichero**, sin tocar la frase original.

---

# 8. Punteros de Bjorner y Brenti, para el deslinde del sentido B6

**ARTEFACTO LEIDO** en las partes citadas, verificadas contra el PDF.

- Identidad: Anders Bjorner y Francesco Brenti, *Combinatorics of Coxeter
  Groups*.
- **Pagina impresa 20, ecuacion (1.25):** el numero de inversiones de x en S_n
  se define como `inv(x) = card{(i,j) : i < j, x(i) > x(j)}`.
- **Pagina impresa 20, Proposicion 1.5.2, ecuacion (1.27):** `l_A(x) = inv(x)`,
  es decir que en tipo A la funcion de longitud coincide con el numero de
  inversiones.
- **Secciones 8.1, tipo B, pagina 245, y 8.2, tipo D, pagina 252:** las
  descripciones combinatorias de los grupos de tipo B y D como permutaciones con
  signo y permutaciones con signo pares, y de sus funciones de longitud como
  recuento de ciertas inversiones de esas permutaciones. El texto lo resume asi
  en la seccion 7.1: "the combinatorial descriptions of the Coxeter groups of
  types B and D as signed permutations and even signed permutations and of their
  length functions as counting certain inversions of these permutations (see
  Sections 8.1 and 8.2 for details)".

**Por que esto importa aqui, dicho con precision.** La definicion (1.25) es
**literalmente la misma** que la de este repositorio: pares con i menor que j y
valores en orden contrario. No es un falso amigo, es el mismo objeto, y nuestro
recuento contra el orden binario es el `inv` de la permutacion que lleva
posiciones a rangos binarios. El riesgo es otro y es real: este repositorio
nombra **B6**, y en la literatura de Coxeter la longitud en tipo B **es un
recuento de ciertas inversiones de permutaciones con signo**, que **no** es la
nuestra. Quien lea "B6" e "inversiones" en la misma frase puede entender
longitud de Coxeter. **Deslinde obligatorio en cualquier texto que ponga las dos
cosas juntas:** aqui B6 es solo el grupo que actua sobre los hexagramas, y el
recuento de inversiones es el de la secuencia contra el orden binario, no la
longitud de ningun elemento de B6.

---

# 9. Segunda mano nueva, pendiente de artefacto

Misma cadena de cita que la seccion 3: el autor del repositorio las nombro en la
instruccion que abrio esta tanda. No se han leido y no se ha verificado ningun
dato bibliografico.

- **Goldenberg 1975.** Aparece ademas citado dentro de un artefacto leido:
  Schoter discute su algebra y anota que Goldenberg no define formalmente una
  operacion de complemento. Ese es el puntero por donde empezar.
- **Davis 1998**, del mismo numero de The Oracle que Schoter.
- **Higgins 1998.**
- **Hacker y Moore 2003.**
- **Mesker 2002.**
- **Moore 1989.**

**La observacion folk de paridad de transiciones sigue sin dueno localizado.**
Se busco en los cuatro artefactos del Yijing de esta tanda las cadenas "3:1",
"48 pairs", "16 pairs", "48 even" y "16 odd": **cero apariciones en los
cuatro**. Lo unico cercano es la clasificacion de pares de Moore descrita en
5.2, que es otro objeto. La observacion se queda como estaba: cifras sin
puntero, sin usar en ningun computo, y con su deslinde obligatorio de la
seccion 3.7.

---

# 10. Que NO autoriza esta revision

(Esta seccion se escribio en la sesion 8 con el numero 4. Al insertarse las
secciones 5 a 9 en la sesion 9, se renumero para que el orden de lectura sea el
del fichero. No se ha cambiado ni una palabra de su contenido, salvo la adicion
del ultimo punto.)

- **No autoriza a afirmar novedad de nada.** Abierta no es cerrada. Se ha leido
  un artefacto de una lista que ni siquiera esta completa.
- **No autoriza a dar por libre lo que no se ha buscado.** El silencio de esta
  lista sobre un resultado no dice nada sobre ese resultado.
- **No autoriza a cerrar la interseccion con Radisic con la linea de cita.** La
  linea deja constancia; cerrar exigiria haber leido lo suficiente como para
  saber que mas hay.
- Cuando se cierre, se dira aqui, con fecha, y con la lista de lo leido.
- **Anadido en la sesion 9.** Que cuatro piezas del Yijing no midan nuestro
  objeto no lo hace nuestro. Que Schoter ya parametrice la orientacion de la
  lectura binaria si quita una cosa de la lista de lo que se podria haber
  llamado propio. La revision sigue ABIERTA.

---

# 11. Decision de vocabulario, tomada y registrada

**Decisor: Alexis.** **Fecha declarada: 10 de agosto de 2026**, en el carril de
chat. (Nota de reloj, que se deja en vez de alinearla: la maquina que produce
este commit marca 2026-08-09, asi que el commit cae el dia anterior a la fecha
declarada por el decisor. Se registran las dos.)

Resuelve la reserva de la seccion 6. Tres reglas, y las tres valen **de aqui en
adelante y para el manuscrito**. **La prosa ya commiteada no se reescribe.**

## 11.1 El estadistico se llama "discordant pairs"

El objeto que este repositorio mide, el numero de pares de posiciones cuyo orden
en la secuencia contradice su orden en la ordenacion de referencia, se nombra
**discordant pairs**.

Nota que acompana a la primera aparicion: *es el inversion number en sentido
combinatorio*, el mismo objeto que Bjorner y Brenti definen en su ecuacion
(1.25) como `card{(i,j) : i < j, x(i) > x(j)}`. La nota es obligatoria porque el
lector combinatorio tiene derecho a saber que no se le esta ofreciendo un
estadistico nuevo, sino el de siempre con otro nombre.

## 11.2 "Inversion" queda reservado al giro, en contexto sinologico

En contexto sinologico, **inversion** nombra el giro de 180 grados del
hexagrama, *fandui*, que es el uso medido en los cuatro artefactos de la seccion
6. Este repositorio no lo usa para otra cosa, y cuando lo use llevara
**deslinde en primera aparicion** dejando claro que es el giro y no el par
discordante.

## 11.3 "Balance" no se usa para el empate sin deslinde

El empate en C(64,2) partido por dos **no se llama balance** sin deslinde
inmediato de los dos sentidos ya ocupados y documentados en la seccion 2 y en la
seccion 7:

- **peso de Hamming**, en Radisic, seccion 4.3, que lo glosa como *yin-yang
  balance* y aclara acto seguido que formalmente es peso de Hamming;
- **recuentos de transicion por coordenada**, en Mutze, seccion 3.2, con la
  condicion `|c_i - 2^n/n| < 2`.

El nombre preferido sigue siendo **empate**, y donde haga falta precision,
empate del recuento de pares discordantes contra el orden binario.

## 11.4 Que no cambia esta decision

No cambia ninguna cifra, ningun teorema y ningun fichero de resultados. Es una
regla de escritura. Los ficheros ya commiteados que dicen inversiones siguen
diciendolo, y esa inconsistencia entre lo viejo y lo nuevo es deliberada: quien
lea la historia vera cuando se decidio y por que, en vez de encontrar un
vocabulario uniforme que finja no haber tenido nunca dudas.

---

# 12. Estado de cierre, preparado y NO cerrado

Esta seccion **no cierra la revision**. Prepara la decision de cerrarla, que no
es de quien escribe. Lista lo que queda y, para cada pieza, una linea de riesgo:
que se sabe de ella por cadena de cita, y por que es o no es plausible que
contenga recuentos de pares discordantes contra ordenes de referencia, o forzado
por grupo.

Aviso sobre el valor de estas lineas: **la plausibilidad no es un veredicto**.
Un veredicto exige leer la pieza. Lo que hay aqui es lo que permite decidir por
donde empezar y cuanto arriesga cada hueco.

## 12.1 Lo que queda

Seis piezas de segunda mano y una observacion sin dueno. Nada mas se ha
localizado como pendiente, y esa lista tampoco pretende ser completa.

## 12.2 Goldenberg 1975

- **Cadena de cita:** Schoter, artefacto leido, lo cita como Gol75 y le dedica
  parrafo propio. Titulo, segun Schoter: "The Algebra of the I Ching and its
  Philosophical Implications". Schoter dice que tiene "significant parallels
  with the work presented here", que Goldenberg lo plantea desde el algebra
  matematica tradicional y no desde la computacional, que **usa aritmetica
  modular linea a linea** para definir sus operaciones, y que **no define
  formalmente una operacion de complemento**. En su nota 3 Schoter anade que
  supo de este trabajo por Steve Moore, ya avanzado el suyo.
- **Riesgo de pares discordantes:** bajo. Lo descrito es un algebra de
  operaciones sobre lineas, no un estadistico sobre pares de posiciones.
- **Riesgo de forzado por grupo:** bajo, y con evidencia concreta: sin
  complemento formalmente definido no hay involucion que invierta el orden
  binario, que es la pieza de la que sale todo el aparato de este repositorio.
- **Prioridad:** media. Es el antecedente del antecedente y conviene leerlo, pero
  lo que se sabe de el no apunta a nuestro objeto.

## 12.3 Davis 1998

- **Cadena de cita:** Moore 2005, artefacto leido, escribe que "the leading
  scholar of the King Wen sequence is probably Scott Davis" y lo describe asi:
  enfoque holistico y antropologico que combina lo estructural y lo textual, y
  que senala "a number of interesting local symmetries in the arrangement of the
  hexagrams at certain points in the sequence".
- **Riesgo de pares discordantes:** bajo. Simetrias locales en puntos concretos
  de la secuencia no es un recuento global sobre los C(64,2) pares.
- **Riesgo de forzado por grupo:** bajo por lo mismo. Que hable de simetrias no
  lo acerca: aqui el grupo actua y se mide que determina, y lo descrito es
  descripcion de configuraciones.
- **Prioridad:** media alta, no por riesgo de solape sino porque es, segun un
  artefacto leido, la referencia principal del tema.

## 12.4 Higgins 1998

- **Cadena de cita:** Schoter, artefacto leido, lo cita como Hig98 dentro de la
  corriente de aplicar tecnicas analiticas modernas al sistema, y precisa en su
  nota 5 que Higgins situa los trigramas en el espacio polinomico de (a+i) al
  cubo, cuyo desarrollo tiene un termino por cada capa del reticulo de
  trigramas.
- **Riesgo de pares discordantes:** bajo. Un desarrollo polinomico de los
  trigramas por peso no es un estadistico de orden.
- **Riesgo de forzado por grupo:** bajo.
- **Prioridad:** baja.

## 12.5 Hacker: son DOS obras, no una

- **Cadena de cita:** Moore 2005, artefacto leido, cita **"Hacker, Moore &
  Patsco 2002"** y da la entrada de un volumen publicado por Routledge en Nueva
  York y Londres en **2002**, con un indice cuya entrada "Textual Sequence
  (Received Order) of Hexagrams" recomienda consultar. Cita ademas "Hacker 1993"
  paginas 101 a 122 como resumen del trabajo previo hasta 1993.
- **RESUELTA en la sesion 12, por artefacto y no por eleccion.** No habia
  discrepancia: **son dos obras distintas y las dos estan en la misma
  bibliografia de Moore 2005**. La sesion 10 solo habia encontrado una y la
  presento como correccion de la otra, y eso estuvo mal. Las dos entradas, tal
  como las da Moore:
  - **Hacker y Moore 2003:** Edward Hacker y Steve Moore, "A Brief Note on the
    Two-Part Division of the Received Order of the Hexagrams in the Zhouyi",
    *Journal of Chinese Philosophy*, Vol. 30, No. 2, junio de 2003, pp. 219-221.
  - **Hacker, Moore y Patsco 2002:** Edward Hacker, Steve Moore y Lorraine
    Patsco, *I Ching: An Annotated Bibliography*, Nueva York y Londres,
    Routledge, 2002.
- **Que sabemos del contenido de Hacker y Moore 2003**, por lo que el propio
  Moore cuenta en 2005: propone una hipotesis para explicar la division en dos
  mitades desiguales de la secuencia recibida, apoyada en un diagrama del
  *Zhouyi Qimeng Yizhuan* de Hu Yigui, y el argumento arranca de que 56
  hexagramas forman 28 pares invertibles y los otros ocho no son invertibles.
- **Riesgo de pares discordantes en Hacker y Moore 2003:** bajo. Usa el mismo
  reparto estructural que este repositorio usa en PROOFS.md 3.1, los 28 mas los
  8, pero para explicar el corte 30 y 34 entre los dos canones, que es otro
  objeto. No hay ordenacion de referencia ni recuento sobre pares.
- **Riesgo de forzado por grupo en Hacker y Moore 2003:** bajo, por lo mismo.
- **Prioridad de Hacker y Moore 2003:** media alta. Son tres paginas y tocan la
  misma particion estructural, asi que conviene leerlas.
- **Riesgo de pares discordantes en la bibliografia de 2002:** muy bajo. Es una
  bibliografia anotada, es decir un instrumento para encontrar piezas, no una
  pieza con resultados.
- **Riesgo de forzado por grupo en la bibliografia de 2002:** muy bajo, por lo
  mismo.
- **Prioridad de la bibliografia de 2002:** alta, pero como **mapa** y no como
  fuente. Si en algun sitio
  hay un antecedente de nuestro objeto, el indice de esa bibliografia es el
  camino mas corto para dar con el. Es la pieza que mas puede reducir el hueco
  de la revision, y la que menos puede colisionar por si misma.

## 12.6 Mesker 2002

- **Cadena de cita:** Moore 2005, artefacto leido, lo cita al hablar de la
  disposicion de las Ocho Casas de Jing Fang, y da la entrada: Harmen Mesker,
  "The Eight Houses: A Preliminary Survey", version 1.2, mayo de 2002. Moore
  describe la disposicion asi: ordena los hexagramas por grupos de ocho, en una
  secuencia que depende sobre todo del cambio de una linea de un hexagrama al
  siguiente, y es un ordenamiento puramente estructural.
- **Riesgo de pares discordantes:** bajo, pero **es la pieza pendiente que toca
  mas de cerca un objeto nuestro**: Jing Fang es una de las tres construcciones
  medidas, y aqui hay un survey dedicado a ella.
- **Riesgo de forzado por grupo:** bajo. Un survey de la disposicion describe la
  construccion; nada en lo citado sugiere que haga actuar un grupo sobre pares.
- **Prioridad:** alta. Es donde mas facil seria encontrar ya escrito algo sobre
  la estructura de los palacios que este repositorio demuestra en PROOFS.md 2.6
  y 2.7.

## 12.7 Moore 1989

- **Cadena de cita:** Moore 2005, artefacto leido, se autocita: Steve Moore,
  "The Trigrams of Han", Wellingborough, Aquarian Press, 1989.
- **Riesgo de pares discordantes:** bajo. Por titulo y por lo que hace el mismo
  autor en 2005, es un trabajo sobre trigramas y su tradicion.
- **Riesgo de forzado por grupo:** bajo.
- **Prioridad:** baja.

## 12.8 La observacion folk de paridad de transiciones

- **Cadena de cita:** ninguna localizada. Entro por la instruccion que abrio la
  revision, con las cifras 48 pares y 16 impares, razon 3 a 1.
- **Evidencia negativa acumulada:** cero apariciones de "3:1", "48 pairs", "16
  pairs", "48 even" y "16 odd" en los cuatro artefactos del Yijing leidos.
- **Riesgo:** no es riesgo de solape, es riesgo de **contaminacion**. Si alguien
  pone esa observacion al lado de la obstruccion de paridad de PROOFS.md 3.3, se
  leera como la misma cosa y no lo es: aquella cuenta transiciones entre
  hexagramas consecutivos, esta cuenta la paridad de un recuento sobre pares de
  posiciones. El deslinde de la seccion 3.7 es obligatorio.
- **Nota aritmetica que sigue en pie:** 48 mas 16 son 64, y una secuencia de 64
  hexagramas tiene 63 transiciones consecutivas.
- **RESUELTA en la seccion 13**, por medicion propia: la variante ciclica da
  48 y 16 en razon 3 a 1, y la lineal da 48 y 15. La observacion cerraba el
  ciclo. Sigue sin dueno localizado.
- **Prioridad:** media. No por lo que pueda contener, sino porque una cifra sin
  puntero circulando cerca del trabajo es una fuente de error para terceros.

## 12.9 Lectura del conjunto

De las siete, **ninguna** tiene, por lo que se sabe de ella por cadena de cita,
pinta de contener un recuento de pares discordantes contra una ordenacion de
referencia ni un argumento de forzado por grupo. Las dos que mas cerca pasan de
un objeto nuestro son **Mesker**, por Jing Fang, y **Hacker, Moore y Patsco**,
no por contenido propio sino por ser el mapa que llevaria a cualquier otra
pieza.

Y la advertencia que hay que repetir: esto son lineas de plausibilidad, no
veredictos. El unico solape encontrado hasta ahora, el de Radisic con
PROOFS.md 3.1, **no habria salido de un juicio de plausibilidad**: la pieza no
estaba en ninguna lista, aparecio al ir a buscar otra cosa, y solo se supo al
leerla entera. Esa es la razon exacta por la que estas lineas no cierran nada.

## 12.10 Quien cierra

**Cerrar la revision es decision de Alexis.** Esta seccion solo la prepara.
Mientras la cabecera de este fichero siga diciendo ABIERTA, no se afirma novedad
de nada. Cuando se cierre, se dira en la seccion 10, con fecha, con la lista de
lo leido, y con lo que se decidio no leer y por que.

---

# 13. La observacion folk, medida en vez de atribuida

La observacion informal decia 48 pares y 16 impares, razon 3 a 1, sin dueno
localizado y sin puntero. En vez de seguir discutiendo la cifra ajena, se mide
la propia sobre la secuencia King Wen de `data/sequences.json`. Programa:
`src/transitions.py`. Salida: `results/transitions.tsv`.

**Que se mide.** Para cada transicion entre hexagramas consecutivos, el numero
de lineas que cambian, y despues el reparto entre transiciones con numero par de
cambios y transiciones con numero impar. Dos variantes, porque la observacion no
decia cual: la **lineal**, con 63 transiciones de la posicion 1 a la 64, y la
**ciclica**, con 64, cerrando de la 64 a la 1.

## 13.1 El resultado

| variante | transiciones | par | impar | razon | coincide con 48 y 16 |
|---|---|---|---|---|---|
| lineal | 63 | 48 | 15 | 3.2000 | **no** |
| ciclica | 64 | **48** | **16** | **3.0000** | **si** |

Origen: `results/transitions.tsv:6` a `:10` y `:20` a `:24`.

**La variante ciclica reproduce exactamente la observacion**, 48 y 16 en razon 3
a 1. La lineal no: da 48 y 15, razon 3.2. La transicion que las separa es la de
cierre, de la posicion 64 a la 1, que cambia 3 lineas y por tanto es impar
(`results/transitions.tsv:42`, `:43`).

## 13.2 La nota aritmetica de la sesion 9 queda resuelta

Aquella nota decia: 48 mas 16 son 64, mientras que 64 hexagramas dan 63
transiciones consecutivas, luego o la observacion cuenta otra cosa, o cierra el
ciclo, o viene mal transmitida. **Era la segunda: cierra el ciclo.** La
observacion no estaba mal transmitida y no contaba otra cosa; contaba 64
transiciones porque tomaba la secuencia como cerrada.

## 13.3 De donde sale el reparto

La medicion da tambien la descomposicion, que no estaba en la observacion:

| clase de transicion | numero | par | impar | origen |
|---|---|---|---|---|
| dentro de un par de la construccion | 32 | 32 | 0 | `results/transitions.tsv:34`, `:35` |
| entre pares, variante ciclica | 32 | 16 | 16 | `results/transitions.tsv:39` a `:41` |

Es decir que el 48 se descompone en 32 mas 16, y el 16 en 0 mas 16. Las 32
transiciones de dentro de un par son **todas** de numero par de cambios, y eso
no es casualidad ni hallazgo: la regla de emparejamiento de la construccion es
giro o complemento, y las dos cambian un numero par de lineas. Lo que reparte a
la mitad es la otra clase, la de los saltos de un par al siguiente, y ahi la
medicion no ofrece ninguna explicacion.

Dato adicional que sale de la misma cuenta: el coste total, la suma de las
lineas que cambian, es 211 en la variante lineal y 214 en la ciclica
(`results/transitions.tsv:18`, `:32`).

## 13.4 Estatus de lo registrado

- **La medicion es propia**, hecha aqui, sobre el dato de este repositorio, y
  reproducible con `python src/transitions.py`.
- **La observacion sigue siendo informal y sin dueno localizado.** Que la
  medicion coincida con ella no le pone autor. Se busco en los cuatro artefactos
  del Yijing leidos y no aparece: cero apariciones de "3:1", "48 pairs", "16
  pairs", "48 even" y "16 odd".
- **No se afirma novedad.** Que una observacion circule sin fuente localizada no
  la convierte en propia por medirla. La revision sigue ABIERTA, y si alguien
  aporta el puntero, este registro se actualiza con el.
- **El deslinde de la seccion 3.7 sigue vigente y ahora hace mas falta que
  antes**, porque ya hay dos cifras de paridad medidas en este repositorio y no
  hablan de lo mismo. La de aqui es la paridad del **numero de lineas que
  cambian** en una transicion entre hexagramas consecutivos. La de PROOFS.md 3.3
  es la paridad del **recuento de pares discordantes** sobre pares de
  posiciones, que sale del cardinal par de las orbitas del grupo. Ni el objeto,
  ni la unidad de conteo, ni la demostracion son los mismos.

---

# 14. La tanda de homomesia

Tres artefactos nuevos, leidos en esta sesion. Fuente: `Probatorium/common`,
carpeta `proyecto-bibliografias`, segunda tanda. Su README dice que para estos
tres se subio **tambien el PDF original** junto a la extraccion, y avisa de que
en los tres las formulas de la conversion no tienen garantia de orden. Regla
aplicada en consecuencia: **toda formula citada aqui se verifico contra el PDF**.

## 14.1 Propp y Roby, "Homomesy in products of two chains"

- **Identidad, leida en la portada del PDF:** James Propp, Department of
  Mathematics, University of Massachusetts Lowell, y Tom Roby, Department of
  Mathematics, University of Connecticut. arXiv:1310.5201v6 [math.CO], con la
  marca lateral **19 Jun 2015**. 28 paginas.
- **Identidad de revista: SEGUNDA MANO.** La instruccion la situa en EJC. El
  artefacto leido es el arXiv y no lleva linea de revista, asi que esa parte no
  se verifica aqui y queda como noticia sin comprobar.
- **Definicion 1, pagina 1**, verificada: dado un conjunto S, una aplicacion
  invertible tau de S en si mismo con todas las orbitas finitas, y una funcion o
  estadistico f de S en un cuerpo K de caracteristica cero, el triple
  (S, tau, f) exhibe **homomesia** si existe una constante c en K tal que para
  toda orbita O el promedio de f sobre O vale c. Y entonces se dice que f es
  homomesico bajo la accion de tau, o mas concretamente **c-mesico**.
- **Seccion 2.1, "Inversions in permutations", pagina 4**, verificada contra el
  PDF y citada literalmente: "Let S be the set of permutations of {1, 2, . . . ,
  n}, let tau send pi1 pi2 ... pin (a permutation written in one-line notation)
  to its reversal pin pi(n-1) ... pi1 and let f(pi) be the number of inversions
  in pi. Since tau squared is the identity, and since f(pi) + f(tau(pi)) =
  n(n-1)/2, f is c-mesic under the action of tau, where c = n(n-1)/4."
- **Lo que eso vale en nuestras cifras:** para n igual a 64, n(n-1)/2 es 2016,
  que es nuestro denominador C(64,2), y n(n-1)/4 es 1008, que es nuestro valor
  esperado. No es analogia: es la misma aritmetica.
- **Barridos sobre el texto completo:** Kendall 0, discordant 0, King Wen 0,
  hexagram 0. Tampoco aparecen las palabras de nuestro aparato: forced 0,
  interval 0, parity 0, matching 0, stabilizer 0.
- **Que no hace:** el articulo va de rowmotion y promotion en productos de dos
  cadenas. La seccion 2.1 es un ejemplo introductorio de tres lineas, no un
  programa. No hay ordenacion de referencia fijada, ni reparto de una orbita
  entre parte forzada y parte libre, ni intervalos, ni paridad, ni enumeracion
  de subgrupos.

## 14.2 Roby, "Dynamical Algebraic Combinatorics and the Homomesy Phenomenon"

- **Identidad:** Tom Roby. PDF `homomesyIMA2015Revised.pdf`, survey de 26
  paginas. **Identidad de volumen: SEGUNDA MANO**, la portada del PDF leido no
  la trae.
- **Example 1, pagina 3**, "Number of inversions under cyclic rotation of binary
  strings": con S las cadenas binarias de longitud n con k unos, tau el
  desplazamiento ciclico y f el estadistico de inversiones, inv resulta
  c-mesico. El ejemplo trabajado que da el propio texto, n igual a 4 y k igual a
  2, produce las orbitas (0011, 1001, 1100, 0110) con inversiones (0, 2, 4, 2) y
  (0101, 1010) con inversiones (1, 3), y promedio 2 en las dos.
- **Seccion 2.1, "General group actions", pagina 4**, verificada contra el PDF:
  la definicion original pedia una aplicacion invertible, equivalente a la
  accion de un grupo ciclico, pero "the definition of homomesy makes perfect
  sense if one considers the action of any finite group, cyclic or not", y la
  homomesia "can always be lifted from a cyclic subgroup of G to all of G".
- **Tres cosas de esta pieza que la instruccion no anticipaba y que hay que
  registrar, porque acercan el antecedente en vez de alejarlo:**
  1. **Example 4, pagina 4:** inversiones bajo giro de noventa grados de
     matrices de permutacion, homomesico con promedio **n(n-1)/4**, la misma
     constante que en 14.1. Y el texto da el mecanismo en una linea: "The proof
     of homomesy is easy: Q takes inversions to non-inversions, and vice-versa."
     **Eso es el mecanismo de nuestro Lema 2**, el testigo que manda inversiones
     a no inversiones, dicho alli para otro objeto.
  2. **Lema 1 de Roby, pagina 4:** si G actua sobre S, H es subgrupo de G, y el
     triple (S, H, f) exhibe homomesia, entonces tambien la exhibe (S, G, f). La
     prueba es que juntar orbitas con el mismo promedio da una orbita mayor con
     ese promedio. **Eso es adyacente a como este repositorio compara la
     contabilidad bajo la sola complementacion con la contabilidad bajo R1**, y
     hay que decirlo: la direccion de subgrupo a grupo ya esta escrita alli.
  3. **Seccion 3.4, "Refined homomesies and indicator functions":** la idea de
     descomponer una homomesia en homomesias mas finas, alli por ficheros de un
     poset. Adyacente en espiritu a nuestra descomposicion por orbitas, con
     objetos distintos.
- **Barridos:** Kendall 0, discordant 0, King Wen 0, hexagram 0, forced 0,
  parity 0, matching 0.

## 14.3 Reiner, Stanton y White, "The cyclic sieving phenomenon"

- **Identidad, leida en la propia cabecera del articulo:** V. Reiner, D. Stanton
  y D. White, *Journal of Combinatorial Theory, Series A* **108 (2004) 17-50**,
  doi 10.1016/j.jcta.2004.04.009.
- **Que es:** el fenomeno de cribado ciclico. Para un triple formado por un
  conjunto X, un polinomio X(q) y un grupo ciclico C que actua, el fenomeno dice
  que evaluar el polinomio en raices de la unidad cuenta **puntos fijos** de cada
  elemento del grupo, y equivalentemente que sus coeficientes cuentan orbitas
  segun el orden de su estabilizador.
- **Por que se registra y por que no compite:** es el otro gran fenomeno de la
  combinatoria algebraica dinamica y aparece citado en los dos artefactos
  anteriores, asi que conviene tenerlo situado. Pero cuenta puntos fijos, no
  promedios de un estadistico sobre orbitas. **No es nuestro objeto ni el de la
  homomesia.** Barridos: homomesy 0, Kendall 0, discordant 0, King Wen 0.

## 14.4 La interseccion, declarada

Igual que con Radisic, se declara sin maquillar.

**El germen del Lema 1 de PROOFS.md tiene dueno anterior.** La idea de que una
involucion que manda el recuento a su complementario fuerza el promedio a la
mitad sobre cada orbita es la seccion 2.1 de Propp y Roby, ejemplo fundacional
del campo, de 2015 o antes. Alli la involucion es la **reversion de la
permutacion, que actua sobre las posiciones y deja las etiquetas**, y por eso la
identidad sale limpia: todo par es inversion en exactamente una de las dos
permutaciones. Aqui la involucion es la **complementacion, que actua sobre los
valores** y, al inducir una permutacion de posiciones, mueve las dos cosas a la
vez. Esa es la diferencia tecnica, y es la razon de que nuestro Lema 0 necesite
el bit epsilon igual a A XOR B: nuestro Lema 1 es su argumento **restringido a
la clase de pares donde la permutacion de posiciones conserva el orden**.

**Tambien tiene dueno anterior el mecanismo del Lema 2**, en la frase de Roby
sobre que el giro manda inversiones a no inversiones (14.2, punto 1), y **la
direccion de subgrupo a grupo** que este repositorio usa al comparar
contabilidades esta escrita como Lema 1 de Roby (14.2, punto 2).

**Lo que no aparece en ninguno de los tres, por lo leido:** la contabilidad de un
objeto por **orbitas de pares de posiciones** bajo el subgrupo completo que una
construccion respeta; el reparto entre parte forzada y parte libre **cuando la
homomesia falla**, con su intervalo de totales compatibles; la **prohibicion por
paridad** del valor central; el **Lema 3** de forzado por emparejamiento con
testigo distinto en cada pareja; y la **enumeracion de subgrupos** de B6 con la
nocion de respetar una construccion. En homomesia, un caso no homomesico es un
caso que se descarta; aqui es el caso que se mide.

**Limite de este veredicto, declarado.** Se leyeron enteras las secciones
citadas, las paginas 1 a 6 de Propp y Roby y 1 a 5 de Roby, la estructura de
secciones de los dos, y barridos de texto completo. **No se leyeron los dos
articulos enteros.** El veredicto de "no aparece" es fuerte para las palabras
barridas y mas debil para una nocion escrita con otro vocabulario.

**Y lo de siempre: nada de esto se afirma nuevo.** La revision sigue ABIERTA.

## 14.5 Vocabulario: "homomesico" entra como termino disponible

**No sustituye a nada.** La decision de la seccion 11 sigue en pie: el
estadistico se llama **discordant pairs**.

Lo que se anade es que **"homomesico" y "c-mesico" quedan DISPONIBLES**, con
dueno citado, para nombrar la propiedad de que el promedio de un estadistico sea
constante sobre las orbitas. En particular, el corolario del Lema 1 de PROOFS.md
puede enunciarse diciendo que el indicador de discordancia es **1/2-mesico**
sobre las orbitas forzadas. Quien use el termino cita a Propp y Roby, Definicion
1, y no lo presenta como propio.
