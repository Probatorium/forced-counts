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
