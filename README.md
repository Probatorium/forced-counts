# forced-counts

Cuando el numero de pares discordantes de una ordenacion construida, contado
contra el orden binario, esta determinado por el grupo de simetrias que su
construccion respeta.

Este repositorio contiene el manuscrito, el codigo que produce cada cifra que el
manuscrito imprime, los ficheros de resultados de los que salen, las
preinscripciones firmadas antes de medir y el registro de esfuerzo de todas las
sesiones de trabajo.

## Como citar

> García Hurtado, A. (2026). *Forced counts: when a symmetry group determines
> the discordance of a constructed ordering* (Version 1). Zenodo.
> https://doi.org/10.5281/zenodo.21889328

**El estado depositado es la etiqueta `zenodo-v1`.** La cabeza de `main` sigue
avanzando; lo que se deposito, y por tanto lo que la cita nombra, es el arbol de
esa etiqueta. Para ver exactamente lo publicado:

    git checkout zenodo-v1

**El bundle del deposito lleva la historia filtrada y sus identificadores de
commit son propios.** No coinciden con los de este remoto, y no es un error: al
filtrar del paquete el material de terceros y el PDF de vista previa se
reescribe el identificador de todos los commits. El contenido es el mismo
trabajo. La politica que lo decide, con sus dos niveles y su razon, esta escrita
en la enmienda 4 de [CONTACT-RULES.md](CONTACT-RULES.md), y lo que el bundle no
trae esta fichado en `dist/THIRD-PARTY.md`, dentro del propio bundle.

## Por donde empezar

| si quieres | mira |
|---|---|
| el articulo | `paper/PAPER.pdf`, compilado con LaTeX |
| el manuscrito ensamblado | `paper/PAPER.md` |
| lo que se declaro antes de medir | `PREREGISTRATION.md` y `PREREGISTRATION-GENERAL.md` |
| lo que se afirma como nuevo, y lo que no | `NOVELTY.md` |
| la revision de antecedentes | `PRIOR-ART.md` |
| como se comprueba todo esto | la seccion 9 del manuscrito, y `tools/package.py` |

## Reproducir

Todo el analisis es determinista, con la unica semilla congelada en la fuente y
declarada en los informes. `python tools/package.py` clona el repositorio en un
directorio limpio, corre la cadena entera desde cero, coteja cada fichero de
resultados contra el commiteado, pasa los comprobadores y construye el paquete.
