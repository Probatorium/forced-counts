# REGLA DE CONTACTO

Este repositorio es nuevo y esta aislado a proposito. Lo que sigue delimita con
que se le permite tener contacto y en que modo.

## kingwen-orderings-replication

- Es de SOLO LECTURA para este repositorio.
- Se consulta unicamente en la etiqueta `zenodo-v3`, commit `d6afae20`. Nunca en
  `main` y nunca en `HEAD`.
- Su texto esta depositado en Zenodo. No se toca: ni edicion, ni reescritura de
  historia, ni commits, ni etiquetas nuevas, ni ramas.
- Si en algun momento parece necesario modificarlo, la accion correcta es PARAR
  y reportarlo, no modificarlo.

## Repositorios de Stasis

- No se tocan. Hay un codecheck de terceros en curso y cualquier escritura
  contamina esa revision.
- Vale la misma salida que arriba: si parece necesario tocarlos, PARAR y
  reportar.

## Este repositorio

- Nace sin remoto. No se crea remoto sin que se pida de forma explicita.
- No se importa nada del repositorio del paper 1. Si se necesita un dato de
  aquel trabajo, se cita por referencia y se vuelve a derivar aqui desde cero.
- El commit raiz es la preinscripcion. No contiene codigo de analisis, ni
  datos, ni cifras medidas.

## Enmiendas

Se anaden aqui, con su motivo, en vez de reescribir el texto de arriba.

**Enmienda 1, en el commit de la medicion.** La regla decia que no se importa
nada del repositorio del paper 1. La medicion necesita las tres secuencias
historicas, que solo estan ahi. Se hace asi:

- Acceso de solo lectura y solo en la etiqueta `zenodo-v3`, sin tocar la fuente,
  con `git archive` sobre el arbol de la etiqueta. Queda constancia del commit,
  del arbol y del sha256 del fichero leido en `data/PROVENANCE.md`.
- El despliegue vive en `_source/`, fuera de la historia de este repositorio.
- Solo entran en la historia las tres secuencias, en forma neutral respecto de
  la convencion de bits. No entra ninguna cifra de resultados de la fuente, ni
  como dato ni como entrada de ningun computo.
- Las dos construcciones se vuelven a derivar aqui desde sus reglas, y el
  programa se detiene si la rederivacion no reproduce la secuencia extraida. La
  tercera, King Wen, es un dato recibido y no se puede derivar de nada.

Lo que la regla protegia sigue protegido: ninguna cifra medida se hereda. Lo que
la regla prohibia en su letra, traer el dato en bruto, se hace de forma
declarada y trazable porque sin el no hay medicion posible.

**Enmienda 2, 2026-08-09, en este commit.** La regla decia que este repositorio
nace sin remoto y que no se crea remoto sin que se pida de forma explicita. La
regla se cierra aqui, y se cierra por cumplida, no por saltada.

- **Motivo.** El remoto estaba condicionado a congelar el nombre. El nombre
  queda congelado, `forced-counts`, despues de la comprobacion de termino que
  esta escrita en NAME.md con sus cinco consultas, su resultado y sus limites,
  y con el deslinde obligatorio respecto de zero forcing, de
  quasirandom-forcing y del forcing de teoria de conjuntos.
- **Autorizacion.** Explicita, del autor, en la sesion que produce este commit.
  Queda tambien en el registro de esfuerzo.
- **Lo que cambia.** Se crea el remoto `github.com/Probatorium/forced-counts` y
  se empuja `main`. Antes del primer empuje se comprueba con `git ls-remote` que
  el remoto esta vacio, para que el primer empuje no pise nada.
- **Lo que no cambia.** Todo lo demas de este fichero sigue vigente sin tocar:
  `kingwen-orderings-replication` sigue siendo de solo lectura y solo en la
  etiqueta `zenodo-v3`, los repositorios de Stasis siguen sin abrirse, y los
  textos firmados siguen sin enmendarse.
- **Lo que el remoto no autoriza.** Publicar no es difundir. Que el repositorio
  este en un remoto no autoriza a anunciarlo, ni a enviarlo a nadie, ni a
  reclamar nada de lo que contiene. La revision de antecedentes sigue sin
  empezar.

**Enmienda 3, 2026-08-10: herencia de verificaciones.** Esta enmienda no es de
contacto con otros repositorios; es una regla de metodo, y entra aqui porque
aqui es donde viven las reglas del repositorio que no son texto firmado.

> **Una reimplementacion de un objeto ya construido hereda las verificaciones
> del original, o declara por escrito por que no.**

Que quiere decir en la practica. Si un objeto ya existe en el repositorio con
comprobaciones que lo atan a su definicion, y se vuelve a implementar en otro
sitio, la reimplementacion arrastra esas mismas comprobaciones. No basta con que
el codigo nuevo parezca correcto: tiene que pasar las pruebas que el viejo ya
pasaba. Si alguna no se puede heredar, se dice cual y por que en el propio
fichero.

**Caso que origina la regla, y por eso se cita.** El codigo de Gray reflejado se
construyo primero en `src/gray.py`, para n igual a 6, con dos comprobaciones
pegadas a su definicion: que reproduce la forma cerrada, el numero XOR el mismo
desplazado uno bajo la convencion de referencia, y que cada paso cambia
exactamente una linea. Al reimplementarlo en `src/general_landscape.py` para n
variable, **la reimplementacion solto las dos**. La funcion nueva construia otra
ordenacion, la que anade el bit mas alto en vez de la linea inferior, y nadie lo
noto hasta que la tabla unica de n de 3 a 6 puso las dos mitades en la misma
pagina y salieron dos resultados distintos para el mismo objeto. El detalle esta
en la enmienda 1 de PROOFS-GENERAL.md y en la enmienda 2 de INFORME-GENERAL.md,
y el coste esta anotado en el registro de esfuerzo como callejon sin salida.

La comprobacion de la forma cerrada habria cazado el error en el momento de
escribir la funcion, sin gastar una sesion entera en explicar una anomalia que
no existia. De ahi la regla.

**Donde viven las demas reglas del repositorio**, para que esta no quede suelta:

- **Textos firmados, que no se enmiendan:** PREREGISTRATION.md y
  PREREGISTRATION-GENERAL.md.
- **Reglas de contacto y de politica del repositorio:** este fichero, con sus
  enmiendas al pie.
- **Instrumentacion del esfuerzo:** EFFORT.md y effort/README.md.
- **Doctrina de la revision de antecedentes:** PRIOR-ART.md, seccion de
  doctrina, y la decision de vocabulario en su seccion 11.
- **Como se escribe el control:** enmienda 1 de INFORME-GRUPO.md.
- **Nociones y construcciones declaradas antes de medir:** DEFINICIONES-GRUPO.md
  y DEFINICIONES-GENERAL.md.


**Enmienda 4, 2026-08-10: politica de filtrado en dos niveles.** Decision de
Alexis, tomada en la sesion 27 con las dos opciones puestas por escrito antes de
elegir. Entra aqui porque es politica del repositorio y no texto firmado.

El arbol contiene dos ficheros que no se escribieron aqui:

- `data/sequences.json`, extraido del paquete de replicacion
  kingwen-orderings-replication en la etiqueta `zenodo-v3`, commit
  `d6afae20bbefba56728251f34f8e3870c43e2cbd`;
- `artifacts/radisic-2601.07175v3-appendix-A.tsv`, transcripcion del apendice A
  de arXiv:2601.07175v3.

Los dos reciben trato distinto segun donde vayan, y la diferencia es deliberada:

> **Nivel 1, el paquete depositado.** Un deposito es inmutable: una vez
> publicado con su DOI no se puede corregir, solo sustituir por una version
> nueva que convive con la anterior. Lo que no se puede retirar se filtra antes
> de entrar. Los dos ficheros salen de toda la historia empaquetada, y en su
> lugar viaja `dist/THIRD-PARTY.md` con la identidad de cada uno, su sha256, sus
> bytes y como se consigue por cuenta propia. Los programas que los consumen no
> se filtran, de modo que la cadena se rehace entera en cuanto el material se
> repone.
>
> **Nivel 2, la historia publica en el remoto.** Un remoto es corregible: si
> manana hubiera que retirar algo, se retira. Por eso conserva los dos ficheros,
> con su manifiesto y su atribucion en `data/PROVENANCE.md` y en la cabecera del
> propio artefacto transcrito. Lo que se gana con ello es que un tercero pueda
> repetir la cadena entera sin reunir material por su cuenta, que es justo lo
> que la seccion 9 del manuscrito le promete.

**Que esta diferencia es decision y no descuido.** Se escribe precisamente
porque un lector que compare el bundle con el remoto vera dos contenidos
distintos y tiene derecho a saber cual de las dos cosas es la intencionada. Las
dos lo son, y por razones distintas: la inmutabilidad del deposito manda filtrar,
la corregibilidad del remoto permite conservar.

**Lo que esta enmienda NO autoriza.** No autoriza reescribir la historia
publicada. Esa era la otra opcion sobre la mesa y se descarto con sus costes a la
vista: cambiaria el hash de los setenta y siete commits, incluido el commit raiz
que contiene la preinscripcion firmada, invalidaria todo clon existente, y
debilitaria la afirmacion de la seccion 9 de que el orden de la historia es
comprobable sin fiarse de nadie. Si algun dia hubiera que reescribir, sera con su
propia decision escrita y no al amparo de esta.

**Enmienda 5, 2026-08-10: una cifra comprobada caduca cuando cambia su objeto.**
Refina la regla de la sesion 22, que decia que ninguna cifra entra en un mensaje
de commit antes de que un comprobador la haya impreso. Esa regla es necesaria y
no es suficiente:

> **Una cifra que un comprobador imprimio sigue siendo cierta solo mientras su
> objeto no cambie. Reutilizarla despues es reportarla sin comprobador, aunque
> lo hubiera habido en su dia.**

**Caso que origina la regla, y por eso se cita.** El tamano de `paper/PAPER.pdf`.
En el commit `286d99b` se reporto en **139580** bytes, y era correcto: esa era la
cifra que `results/build-paper.tsv` traia impresa en ese momento, y la aritmetica
que la acompanaba cuadraba con ella, 139580 mas 3421 retornos de carro igual a
143001 en el clon. Despues, en `fbeee9b`, el PDF se reconstruyo con un colofon
distinto, porque el colofon nombra su propio commit y su propio recuento de
comprobaciones, y el fichero paso a medir **139581** bytes. La cifra vieja se
repitio en el informe de cierre de la sesion 26 cuando ya no era la del fichero.
Lo detecto una auditoria externa, no un comprobador de aqui.

No se reescribe nada: ni el mensaje del commit, que era cierto cuando se
escribio, ni el informe. Se anota la correccion, que es lo que este repositorio
hace con sus errores.

**En la practica.** Una cifra que se saca de un fichero de comprobador y se
vuelve a usar en otro momento se vuelve a leer del fichero, no de la memoria ni
del mensaje anterior. Las cifras que el manuscrito imprime ya tienen esto
resuelto por construccion, porque `src/declared_values.py` las coteja contra su
linea de `results` en cada ensamblado y se niega a ensamblar si han caducado. Lo
que esta enmienda cubre es el resto: los mensajes de commit y los informes, que
no pasan por ningun congelador.
