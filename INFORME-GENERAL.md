# Informe: primera medicion de la fase general

Todo lo medido aqui quedo declarado antes en DEFINICIONES-GENERAL.md, y la
preinscripcion de la fase, con lo que se sabia y lo que no, esta en
PREREGISTRATION-GENERAL.md. Las cifras salen de `src/general_landscape.py` y se
citan con fichero y linea.

**El objetivo declarado era ver la forma de la clasificacion, no afirmarla.** Lo
que sigue describe lo medido y no concluye una clasificacion. Sin afirmaciones
de novedad: la revision de antecedentes sigue ABIERTA.

## 1. Lo que se verifico primero

- El orden binario contra si mismo da cero pares discordantes, en las tres
  dimensiones. Control de que el aparato no inventa nada.
- **La cifra predicha en la seccion b.4 de la preinscripcion se cumple en todos
  los casos**: el grupo que respeta el sistema de bloques B(n, k) tiene orden
  k! por (n-k)! por 2^n. Se comprobo en las 9 combinaciones de n y k, y en las
  dos ordenaciones fijas de cada una. Como estaba en (b) y no en (c), esto es
  verificacion de un resultado previo y no un hallazgo.
- **El orden del grupo no depende de la ordenacion**, solo de la particion: en
  cada combinacion, los miles de ordenaciones muestreadas o enumeradas dieron un
  unico orden de grupo.

## 2. La rejilla, ordenacion por ordenacion

Denominadores y empates: n igual a 3 da C(8,2) igual a 28 y empate 14
(`results/general-landscape.tsv:6`, `:7`); n igual a 4 da 120 y 60 (`:87`,
`:88`); n igual a 5 da 496 y 248 (`:204`, `:205`).

Casilla de las dos ordenaciones fijas, con el grupo entero de cada B(n, k):

| n | k | orden del grupo | Gray | tipo Mawangdui canonica |
|---|---|---|---|---|
| 3 | 1 | 16 | PROHIBIDO | PROHIBIDO |
| 3 | 2 | 16 | PROHIBIDO | PROHIBIDO |
| 4 | 1 | 96 | PROHIBIDO | PROHIBIDO |
| 4 | 2 | 64 | PROHIBIDO | **INTERVALO** |
| 4 | 3 | 96 | PROHIBIDO | PROHIBIDO |
| 5 | 1 | 768 | PROHIBIDO | PROHIBIDO |
| 5 | 2 | 384 | PROHIBIDO | PROHIBIDO |
| 5 | 3 | 384 | PROHIBIDO | PROHIBIDO |
| 5 | 4 | 768 | PROHIBIDO | PROHIBIDO |

Origen: `results/general-landscape.tsv:28`, `:42`, `:64`, `:78`, `:109`, `:123`,
`:145`, `:159`, `:181`, `:195`, `:226`, `:240`, y las homologas de n igual a 5.

La fila de n igual a 4 con k igual a 2 es la unica donde las dos ordenaciones se
separan: **mismo grupo, misma particion, distinta casilla**. Es la ilustracion
mas corta de que la casilla no la decide el grupo por si solo.

## 3. La familia de tipo Mawangdui, recorriendo sus ordenaciones

Para cada B(n, k) se recorren las ordenaciones de la familia O3, que es la
parametrizada por el orden de bloques y el orden interno. Donde el espacio cabia
se enumero entero, y donde no, se muestreo con la semilla 20260809
(`results/general-landscape.tsv:3`) y 2000 repeticiones (`:4`), tal y como se
declaro antes de correr.

| n | k | casos | modo | FORZADO | INTERVALO | PROHIBIDO | origen |
|---|---|---|---|---|---|---|---|
| 3 | 1 | 48 | enumerado | 0 | 24 | 24 | `:45` a `:48` |
| 3 | 2 | 48 | enumerado | 0 | 24 | 24 | `:81` a `:84` |
| 4 | 1 | 2000 | muestra | 0 | 827 | 1173 | `:126` a `:129` |
| 4 | 2 | 576 | enumerado | **36** | 228 | 312 | `:162` a `:165` |
| 4 | 3 | 2000 | muestra | 0 | 828 | 1172 | `:198` a `:201` |
| 5 | 1 | 2000 | muestra | 0 | 781 | 1219 | seccion n5 k1 |
| 5 | 2 | 2000 | muestra | **10** | 794 | 1196 | seccion n5 k2 |
| 5 | 3 | 2000 | muestra | **9** | 753 | 1238 | seccion n5 k3 |
| 5 | 4 | 2000 | muestra | 0 | 771 | 1229 | seccion n5 k4 |

## 4. La forma que se ve, dicha como forma y no como clasificacion

Cuatro rasgos, los cuatro descriptivos. **Ninguno se afirma como regla**, y cada
uno se puede caer con una dimension mas.

1. **La casilla FORZADO aparece solo con k intermedio.** En las nueve
   combinaciones, los unicos casos forzados salieron con n igual a 4 y k igual a
   2, y con n igual a 5 y k igual a 2 o 3. En k igual a 1 y en k igual a n-1 no
   aparecio ninguno, ni enumerando ni muestreando.
2. **PROHIBIDO es la casilla mas poblada** en todas las combinaciones excepto en
   n igual a 3, donde el reparto enumerado sale exactamente por mitades.
3. **La casilla depende de la ordenacion y no solo del grupo.** El grupo es el
   mismo dentro de cada fila, y las casillas cambian dentro de la fila.
4. **El codigo de Gray reflejado sale PROHIBIDO en las nueve combinaciones**, y
   eso lo separa de lo medido en n igual a 6, donde el empate si estaba entre
   los totales compatibles en los cinco niveles de su torre. La diferencia esta
   medida y **no se explica aqui**.

## 5. Lo que este informe no dice

- **No afirma ninguna clasificacion.** La preinscripcion declaro esta pregunta
  SIN PREDICCION en su seccion c.2, y sigue sin respuesta: lo que hay son nueve
  combinaciones en tres dimensiones.
- **No afirma que el patron de k intermedio se mantenga.** Con tres dimensiones y
  un solo caso enumerado por debajo de n igual a 5, es una forma observada, no
  una tendencia establecida.
- **No lee nada de las proporciones entre casillas.** Son recuentos con su
  procedencia y su semilla, y nada mas.
- **No afirma novedad.** La revision de antecedentes sigue ABIERTA, y la parte
  general de este trabajo vive en el territorio de la homomesia, ya registrado
  en PRIOR-ART.md 14.

## Reproducir

    python src/parity_hypotheses.py
    python src/general_landscape.py

Deterministas las dos. La unica fuente de azar es la semilla declarada.

---

# Enmiendas

Se anaden al pie, con fecha y motivo. No se toca el texto de arriba.

## Enmienda 1, 2026-08-10: el rasgo 1 de la seccion 4 era mas estrecho de lo que parecia

**Motivo.** El rasgo 1 dice que la casilla FORZADO aparece solo con k intermedio
y que en k igual a 1 y en k igual a n-1 no aparecio ninguno. La frase es cierta
de lo que se midio, que fue la familia O3 y las dos ordenaciones fijas, y asi
esta escrita en la seccion 3. Pero invita a leerla como una propiedad de los
extremos, y no lo es.

**Medido despues, en PROOFS-GENERAL.md pieza 1:** recorriendo las 40320
ordenaciones de los ocho vertices, B(3,1) tiene 472 ordenaciones forzadas y
B(3,2) tiene 600, con testigo exhibido. En n igual a 4 con k igual a 1 tambien
aparece una entre 3000 muestreadas.

**Alcance.** Las cifras de las tablas de arriba siguen siendo validas: son de la
familia O3 y ahi no hay forzado en los extremos. Lo que queda retirado es la
lectura general del rasgo 1, sin borrarla, para que se vea que estuvo ahi. La
propiedad es de la familia O3, no de los extremos.
