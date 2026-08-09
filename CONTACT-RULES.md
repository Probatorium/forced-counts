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
