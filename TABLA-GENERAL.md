# La tabla general, una sola

n de 3 a 6 en el mismo sistema de bloques B(n, k) y con las mismas columnas, tal
y como quedo declarado en DEFINICIONES-GENERAL.md. Cifras de
`results/general-landscape.tsv` para n de 3 a 5 y de `results/general-n6.tsv`
para n igual a 6.

Sin afirmaciones de novedad: la revision de antecedentes sigue ABIERTA.

## La tabla

B(n, k) son las clases laterales del subespacio de las k coordenadas bajas. El
orden del grupo que respeta esa particion es k! por (n-k)! por 2^n, verificado en
las catorce filas. La columna O3 da el reparto entre las tres casillas al
recorrer la familia parametrizada por el orden de bloques y el orden interno.

| n | k | orden del grupo | Gray | tipo MWD canonica | O3: FORZADO / INTERVALO / PROHIBIDO | casos O3 |
|---|---|---|---|---|---|---|
| 3 | 1 | 16 | INTERVALO | PROHIBIDO | 0 / 24 / 24 | 48, enumerado |
| 3 | 2 | 16 | INTERVALO | PROHIBIDO | 0 / 24 / 24 | 48, enumerado |
| 4 | 1 | 96 | INTERVALO | PROHIBIDO | 0 / 827 / 1173 | 2000, muestra |
| 4 | 2 | 64 | INTERVALO | INTERVALO | **36** / 228 / 312 | 576, enumerado |
| 4 | 3 | 96 | INTERVALO | PROHIBIDO | 0 / 828 / 1172 | 2000, muestra |
| 5 | 1 | 768 | INTERVALO | PROHIBIDO | 0 / 781 / 1219 | 2000, muestra |
| 5 | 2 | 384 | INTERVALO | PROHIBIDO | **10** / 794 / 1196 | 2000, muestra |
| 5 | 3 | 384 | INTERVALO | PROHIBIDO | **9** / 753 / 1238 | 2000, muestra |
| 5 | 4 | 768 | INTERVALO | PROHIBIDO | 0 / 771 / 1229 | 2000, muestra |
| 6 | 1 | 7680 | INTERVALO | PROHIBIDO | no muestreada | por coste |
| 6 | 2 | 3072 | INTERVALO | PROHIBIDO | no muestreada | por coste |
| 6 | 3 | 2304 | INTERVALO | INTERVALO | no muestreada | por coste |
| 6 | 4 | 3072 | INTERVALO | PROHIBIDO | no muestreada | por coste |
| 6 | 5 | 7680 | INTERVALO | PROHIBIDO | no muestreada | por coste |

**Fila aparte, la unica secuencia historica que encaja en el sistema:** la de
Mawangdui contra B(6, 3), porque sus octetos son las fibras del trigrama
superior, que es exactamente esa particion. Grupo de orden 2304, cero orbitas
libres, un solo total compatible, recuento observado 1008: **FORZADO**. Es la
misma cifra y el mismo desenlace que PROOFS.md 2.5 ya demostraba, ahora leido
dentro de la tabla general.

## Por que Jing Fang y King Wen no estan en la tabla

Porque no encajan en B(n, k), y meterlas seria forzar la analogia:

- los palacios de **Jing Fang** son las clases laterales de un conjunto M que
  **no es subespacio**, comprobado (`results/general-n6.tsv`, clave
  `n6.los.palacios.de.jing.fang.son.clases.de.un.subespacio`, que vale cero);
- los pares de **King Wen** son las orbitas del giro, y sus 32 pares presentan
  **siete** diferencias distintas, no una sola, de modo que tampoco son las
  clases de un subespacio de dimension uno (clave
  `n6.diferencias.distintas.entre.los.pares.de.king.wen`).

Las dos siguen medidas en su sitio, en INFORME-GRUPO.md y en PROOFS.md. Lo que
no tienen es fila en esta tabla.

## Lo que la tabla unica deja ver, y que estaba escondido entre dos informes

**El codigo de Gray reflejado cae en INTERVALO en las catorce filas.** No hay
diferencia entre n igual a 6 y las dimensiones pequenas. La supuesta anomalia de
Gray, que el informe anterior daba por medida y la pieza 3 de PROOFS-GENERAL.md
intentaba explicar, **no existia**: venia de que la funcion que construia el
codigo en `src/general_landscape.py` anadia el bit mas alto cuando
DEFINICIONES-GENERAL.md declara que se anade la linea inferior. Corregido,
vuelto a correr, y documentado en la enmienda 1 de PROOFS-GENERAL.md y en la
enmienda 2 de INFORME-GENERAL.md.

Esa es exactamente la razon por la que se pidio una tabla sola: **la
contradiccion solo era visible con las dos mitades en la misma pagina**.

## Lo que la tabla no dice

- No afirma ninguna clasificacion. Sigue declarada SIN PREDICCION en la seccion
  c.2 de PREREGISTRATION-GENERAL.md.
- No dice que la columna de tipo MWD canonica sea PROHIBIDO por una razon: es un
  recuento, no un teorema, y en dos filas de las catorce no lo es.
- No dice nada de las filas de n igual a 6 en la columna O3, porque no se
  midieron. Cada caso cuesta del orden de un segundo por los 2016 pares, y 2000
  repeticiones por nivel serian horas.
- No afirma novedad de nada.

## Reproducir

    python src/general_landscape.py
    python src/general_n6.py
    python src/general_theorems.py
