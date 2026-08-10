# Esqueleto del manuscrito

**Sin titulo.** No se propone todavia: el titulo pasa su propia puerta de
termino, igual que la paso el nombre del repositorio en NAME.md, y eso es un paso
propio y posterior. Asi queda escrito en NOVELTY.md.

**Sin prosa.** Este fichero tiene, por seccion, **una frase** de que contendra y
**la lista de ficheros del repositorio de donde saldra**. La escritura sera
ensamblaje verificable y no redaccion de memoria: cada afirmacion del manuscrito
tendra que poder senalar la linea del repositorio de la que viene.

**Reglas que el manuscrito hereda.** Ninguna afirmacion de novedad fuera de lo
declarado en NOVELTY.md. Vocabulario vinculante de NOVELTY.md. Deslindes
obligatorios en primera aparicion. Las dos preinscripciones y NOVELTY.md son
texto firmado y no se enmiendan.

---

## 1. Introduccion

**Que contendra:** la pregunta de cuando el recuento de discordant pairs de una
ordenacion contra el orden binario queda determinado por la simetria que su
construccion respeta, el objeto concreto sobre el que se plantea, y la
declaracion de no anacronismo que separa medir una secuencia recibida de afirmar
algo sobre quien la ordeno.

**De donde sale:** `PREREGISTRATION.md` (a), `PREREGISTRATION-GENERAL.md` (a),
`NOVELTY.md` (seccion NO SE AFIRMA), `PRIOR-ART.md` 5.2.

## 2. Preliminares

**Que contendra:** el n-cubo y sus vertices, el grupo hiperoctaedrico B_n con la
correspondencia entre permutar lineas y permutar ejes, las ordenaciones, las
cuatro convenciones de bits con su denominador, y **discordant pairs** con sus
tres deslindes: del inversion number combinatorio al que es igual, del giro
sinologico *fandui* del que no lo es, y de la longitud de Coxeter en tipo B con
la que comparte nombre y no objeto.

**De donde sale:** `PROOFS.md` (convenios y pieza 4), `PREREGISTRATION.md` (d),
`PREREGISTRATION-GENERAL.md` (d), `PRIOR-ART.md` 6, 8 y 11, `NOVELTY.md`
(vocabulario).

## 3. La contabilidad por orbitas

**Que contendra:** los Lemas 0, 0b, 1 y 2 con sus demostraciones y el corolario
de que un grupo solo puede forzar el empate, con las dos citas de homomesia
puestas donde tocan y no al final.

**De donde sale:** `PROOFS.md` pieza 1, `PROOFS-GENERAL.md` pieza 2,
`DEFINICIONES-GRUPO.md`, `PRIOR-ART.md` 14.

## 4. La obstruccion de paridad

**Que contendra:** el teorema de que toda orbita tiene cardinal par bajo dos
hipotesis, el corolario de que la paridad del recuento queda fijada por la
estructura, y la necesidad de dim mayor o igual que 2 demostrada por testigo
junto con la redundancia de la normalidad.

**De donde sale:** `PROOFS.md` 3.3, `PREREGISTRATION-GENERAL.md` b.2,
`src/parity_hypotheses.py` y `results/parity-hypotheses.tsv`.

## 5. La caracterizacion

**Que contendra:** el Lema 3 con sus certificados, los Teoremas 1 y 2 que
convierten estar forzada en un recuento por clases de diferencia, y el reparto
demostrado entre lo que decide el grupo, los cardinales de orbita y la paridad
de las diferencias, y lo que necesita la ordenacion, los valores de c y la
casilla.

**De donde sale:** `PROOFS.md` pieza 1 y 2.5, `PROOFS-B31.md` 1 y 2,
`PROOFS-GENERAL.md` pieza 2, `results/certificates.txt`,
`results/certificate-mwd-01.txt`.

## 6. Los tres ordenes historicos

**Que contendra:** Mawangdui y Jing Fang con el empate demostrado entero, King
Wen con el empate demostrado imposible por paridad, el estrechamiento que aporta
A5 sin explicar nada, la anatomia completa del residuo de 5 sobre las 19 orbitas
libres, y su declaracion de informativo relativo a la lista cerrada de
estructuras probadas, con la frase de que la matematica toca fondo donde empieza
la eleccion editorial.

**De donde sale:** `PROOFS.md` piezas 2 y 3, `INFORME.md`, `INFORME-GRUPO.md`,
`DEFINICIONES-RESIDUO5.md`, `INFORME-RESIDUO5.md`, `data/PROVENANCE.md`,
`artifacts/radisic-2601.07175v3-appendix-A.tsv`.

## 7. El paisaje B(n,k)

**Que contendra:** la tabla unica de n de 3 a 6 con las tres casillas, el codigo
de Gray reflejado como ordenacion de referencia y no como pariente, y las dos
refutaciones que salieron de intentar elevar sus formas: la de los extremos y la
de la anomalia que no existia.

**De donde sale:** `TABLA-GENERAL.md`, `INFORME-GENERAL.md` con sus dos
enmiendas, `PROOFS-GENERAL.md` con la suya, `INFORME-GRAY.md`,
`DEFINICIONES-GENERAL.md`.

## 8. Problemas abiertos

**Que contendra:** los cuatro que quedan escritos como abiertos y no como
pendientes de redaccion: el fallo de Hall, enumerativo en 6960 orbitas y sin
teorema; la cuenta de ordenaciones forzadas, 472 y 600, medida y sin formula; el
residuo de 5; y la forma de la clasificacion, que la preinscripcion general
declaro sin prediccion y sigue sin respuesta.

**De donde sale:** `PROOFS-B31.md` 3 y 4, `PROOFS.md` 3.4,
`PREREGISTRATION-GENERAL.md` c.2, `results/hall-search.tsv`.

## 9. Metodos de verificacion

**Que contendra:** que todo lo anterior se puede volver a correr, con el
repositorio publico y su historia, las dos preinscripciones firmadas antes de
medir, el registro de esfuerzo con su cadena de sha256 append only, y la lista
de lo que se declaro antes de mirar cada vez.

**De donde sale:** `EFFORT.md`, `effort/README.md`, `effort/log.jsonl`,
`CONTACT-RULES.md` con sus tres enmiendas, `NAME.md`, `PRIOR-ART.md` con su
cierre, y los cuatro ficheros de definiciones previas.

---

## Lo que este esqueleto ya deja fijado

- **Los deslindes van en la seccion 2 y en primera aparicion**, no en una nota
  al final.
- **Las intersecciones van donde vive el resultado**, no agrupadas en un
  apartado de agradecimientos: la de Propp y Roby en la seccion 3, la de Radisic
  en la 6, la de Schoter en la 2.
- **La seccion 6 termina en la declaracion de frontera**, y no en una promesa de
  trabajo futuro.
- **La seccion 8 no es una lista de deseos:** cada abierto va con lo que se
  midio y con lo que faltaria para cerrarlo.
