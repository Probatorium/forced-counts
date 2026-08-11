# 7. The landscape B(n,k)

<!-- ENSAMBLAJE. Cada afirmacion con su fichero de origen en comentario. Cero
     cifras sin procedencia. Regla de PAPER.md. -->

The three orderings of section 6 live in one dimension and carry historical
weight. This section removes both features: it varies the dimension and replaces
the received orderings by a family with a parameter, to see what the apparatus
does when nothing is inherited.

## 7.1 One block system with a parameter, and what it does not cover

<!-- origen: DEFINICIONES-GENERAL.md 2, declarado antes de medir -->
For a dimension n and a level k between 1 and n minus 1, let **B(n, k)** be the
partition of the vertices into the cosets of the subspace spanned by the k low
coordinates. Two vertices share a block when they differ only in low
coordinates. Every level is reported; the level was not chosen after seeing
results.

<!-- origen: DEFINICIONES-GENERAL.md 2, con la razon de la eleccion -->
This single family covers two things at once. At the middle level it is the
analogue of the first historical ordering, whose blocks are the fibres of the
upper trigram. Running over all levels it is the tower of recursion levels of the
reflected Gray code. For odd n there is no middle level, and rather than force
the analogy we say that the analogue is simply not defined there.

<!-- origen: results/general-n6.tsv, claves de Jing Fang y King Wen, comprobadas
     no supuestas -->
**What the family does not cover, checked and not assumed.** The palaces of the
second historical ordering are the cosets of a set that is **not a subspace**,
and the pairs of the third are the orbits of the half turn, whose differences are
not a single vector but several. Neither is a B(n, k), and putting them in the
table would be forcing the analogy. They keep their own treatment in section 6
and have no row here.

## 7.2 The table

<!-- origen: TABLA-GENERAL.md, catorce filas; cifras en
     results/general-landscape.tsv y results/general-n6.tsv. LA TABLA SE IMPRIME
     ENTERA: un paisaje del que solo se dice que existe no es un paisaje. Las
     casillas llevan aqui el nombre ingles de la seccion 1; en los ficheros de
     results son FORZADO, INTERVALO y PROHIBIDO. -->
<!-- CIFRAS: 16 = results/general-landscape.tsv:16 n3.k1.Gray.grupo.orden;
     0 = results/general-landscape.tsv:47 n3.k1.O3.FORZADO;
     24 = results/general-landscape.tsv:48 n3.k1.O3.INTERVALO;
     24 = results/general-landscape.tsv:49 n3.k1.O3.PROHIBIDO;
     48 = results/general-landscape.tsv:46 n3.k1.O3.casos;
     16 = results/general-landscape.tsv:52 n3.k2.Gray.grupo.orden;
     0 = results/general-landscape.tsv:83 n3.k2.O3.FORZADO;
     24 = results/general-landscape.tsv:84 n3.k2.O3.INTERVALO;
     24 = results/general-landscape.tsv:85 n3.k2.O3.PROHIBIDO;
     48 = results/general-landscape.tsv:82 n3.k2.O3.casos;
     96 = results/general-landscape.tsv:97 n4.k1.Gray.grupo.orden;
     0 = results/general-landscape.tsv:128 n4.k1.O3.FORZADO;
     827 = results/general-landscape.tsv:129 n4.k1.O3.INTERVALO;
     1173 = results/general-landscape.tsv:130 n4.k1.O3.PROHIBIDO;
     2000 = results/general-landscape.tsv:127 n4.k1.O3.casos;
     64 = results/general-landscape.tsv:133 n4.k2.Gray.grupo.orden;
     36 = results/general-landscape.tsv:164 n4.k2.O3.FORZADO;
     228 = results/general-landscape.tsv:165 n4.k2.O3.INTERVALO;
     312 = results/general-landscape.tsv:166 n4.k2.O3.PROHIBIDO;
     576 = results/general-landscape.tsv:163 n4.k2.O3.casos;
     96 = results/general-landscape.tsv:169 n4.k3.Gray.grupo.orden;
     0 = results/general-landscape.tsv:200 n4.k3.O3.FORZADO;
     828 = results/general-landscape.tsv:201 n4.k3.O3.INTERVALO;
     1172 = results/general-landscape.tsv:202 n4.k3.O3.PROHIBIDO;
     2000 = results/general-landscape.tsv:199 n4.k3.O3.casos;
     768 = results/general-landscape.tsv:214 n5.k1.Gray.grupo.orden;
     0 = results/general-landscape.tsv:245 n5.k1.O3.FORZADO;
     781 = results/general-landscape.tsv:246 n5.k1.O3.INTERVALO;
     1219 = results/general-landscape.tsv:247 n5.k1.O3.PROHIBIDO;
     2000 = results/general-landscape.tsv:244 n5.k1.O3.casos;
     384 = results/general-landscape.tsv:250 n5.k2.Gray.grupo.orden;
     10 = results/general-landscape.tsv:281 n5.k2.O3.FORZADO;
     794 = results/general-landscape.tsv:282 n5.k2.O3.INTERVALO;
     1196 = results/general-landscape.tsv:283 n5.k2.O3.PROHIBIDO;
     2000 = results/general-landscape.tsv:280 n5.k2.O3.casos;
     384 = results/general-landscape.tsv:286 n5.k3.Gray.grupo.orden;
     9 = results/general-landscape.tsv:317 n5.k3.O3.FORZADO;
     753 = results/general-landscape.tsv:318 n5.k3.O3.INTERVALO;
     1238 = results/general-landscape.tsv:319 n5.k3.O3.PROHIBIDO;
     2000 = results/general-landscape.tsv:316 n5.k3.O3.casos;
     768 = results/general-landscape.tsv:322 n5.k4.Gray.grupo.orden;
     0 = results/general-landscape.tsv:353 n5.k4.O3.FORZADO;
     771 = results/general-landscape.tsv:354 n5.k4.O3.INTERVALO;
     1229 = results/general-landscape.tsv:355 n5.k4.O3.PROHIBIDO;
     2000 = results/general-landscape.tsv:352 n5.k4.O3.casos;
     7680 = results/general-n6.tsv:11 n6.k1.Gray.grupo.orden;
     3072 = results/general-n6.tsv:39 n6.k2.Gray.grupo.orden;
     2304 = results/general-n6.tsv:67 n6.k3.Gray.grupo.orden;
     3072 = results/general-n6.tsv:110 n6.k4.Gray.grupo.orden;
     7680 = results/general-n6.tsv:138 n6.k5.Gray.grupo.orden;
     2304 = results/general-n6.tsv:95 n6.k3.Mawangdui.historica.grupo.orden;
     0 = results/general-n6.tsv:100 n6.k3.Mawangdui.historica.libres;
     1 = results/general-n6.tsv:106 n6.k3.Mawangdui.historica.alcanzables;
     1008 = results/general-n6.tsv:105 n6.k3.Mawangdui.historica.observado -->
Table 2 gives dimensions three to six, every level, with the same columns
throughout. The order of the group respecting B(n, k) is k factorial times n
minus k factorial times 2 to the n, which was stated in the general
preregistration before any of this was run and is verified in all 14 rows. The order of the group depends only
on the partition and not on the ordering, which the same table confirms across
thousands of orderings.

**Table 2.** *The landscape B(n, k) in dimensions three to six.*

| n | k | group order | Gray | canonical | forced | bounded | barred | cases |
|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 16 | bounded | barred | 0 | 24 | 24 | 48, enumerated |
| 3 | 2 | 16 | bounded | barred | 0 | 24 | 24 | 48, enumerated |
| 4 | 1 | 96 | bounded | barred | 0 | 827 | 1173 | 2000, sampled |
| 4 | 2 | 64 | bounded | bounded | 36 | 228 | 312 | 576, enumerated |
| 4 | 3 | 96 | bounded | barred | 0 | 828 | 1172 | 2000, sampled |
| 5 | 1 | 768 | bounded | barred | 0 | 781 | 1219 | 2000, sampled |
| 5 | 2 | 384 | bounded | barred | 10 | 794 | 1196 | 2000, sampled |
| 5 | 3 | 384 | bounded | barred | 9 | 753 | 1238 | 2000, sampled |
| 5 | 4 | 768 | bounded | barred | 0 | 771 | 1229 | 2000, sampled |
| 6 | 1 | 7680 | bounded | barred | . | . | . | not sampled |
| 6 | 2 | 3072 | bounded | barred | . | . | . | not sampled |
| 6 | 3 | 2304 | bounded | bounded | . | . | . | not sampled |
| 6 | 4 | 3072 | bounded | barred | . | . | . | not sampled |
| 6 | 5 | 7680 | bounded | barred | . | . | . | not sampled |

The last three columns of Table 2 are the distribution of the three outcomes
over the parametrised family, by block order and internal order; a dot means the
distribution was not measured. The **forced** column is empty in every row at an
extreme level and non empty only at the intermediate ones, which is the shape
that section 7.3 takes up and cuts down to size.

<!-- origen: TABLA-GENERAL.md; las tres casillas definidas en
     DEFINICIONES-GENERAL.md 5 -->
Each row reports the outcome for two fixed orderings, the reflected Gray code and
the canonical member of the parametrised family.

<!-- DEFINICION FORMAL, extraida de la funcion mawangdui_like de
     src/general_landscape.py y comprobada contra ella para todo n y todo k -->
The **parametrised family** of B(n, k) is indexed by a pair of permutations: one
of the 2^(n-k) blocks, which fixes the order in which the blocks are laid out,
and one of the 2^k positions inside a block, which is the same for every block.
Given the pair, the ordering places at position i times 2^k plus j the vertex
whose upper n minus k coordinates encode the image of i and whose lower k
coordinates encode the image of j. The **canonical member** is the one obtained
when both permutations are the identity, so that position i times 2^k plus j
carries the vertex whose integer code is exactly i times 2^k plus j: the map from
positions to vertices is the identity. That is not the binary reference order,
because the reference order reads the bottom line as the most significant bit
while the vertex code reads it as the least significant one, which is why the
canonical member has a discordance to report at all.

<!-- ESQUEMA DE MUESTREO, tomado del codigo y congelado contra results -->
<!-- CIFRAS: 20260809 = results/general-landscape.tsv:3 semilla;
     2000 = results/general-landscape.tsv:4 repeticiones.donde.se.muestrea;
     5000 = results/general-landscape.tsv:5 umbral.de.enumeracion.entera -->
Where the space of those pairs has at most 5000 members it is traversed in full,
and the row says *enumerated*. Where it is larger, 2000 pairs are drawn and the
row says *sampled*. Each draw takes one permutation of the blocks and one of the
inner positions, each uniform over its symmetric group and independent of the
other, from a Mersenne Twister seeded once per row at 20260809, a seed frozen in
the source before any of this was run. The draws are independent and are not
deduplicated, so the sample is with replacement and a pair can in principle come
up twice.

<!-- origen: TABLA-GENERAL.md, fila aparte de la Mawangdui historica.
     Es la unica secuencia historica que encaja en el sistema, y por eso va en
     su propia fila y no dentro de la tabla. -->
**One historical row belongs here and is kept apart.** The first historical
ordering does fit the family, at the middle level of dimension six, since its
octets are exactly those cosets. Its row is Table 3, kept out of Table 2 so
that the parametrised family and the received sequence are not read as one
population:

**Table 3.** *The one historical ordering that fits the family, reported apart.*

| ordering | n | k | group order | free orbits | compatible totals | count | outcome |
|---|---|---|---|---|---|---|---|
| Mawangdui, received | 6 | 3 | 2304 | 0 | 1 | 1008 | forced |

Table 3 reports 0 free orbits, exactly 1 compatible total, and that total is
1008: the forced outcome of section 6 read inside the general frame rather than beside it,
and the same figure that the demonstration there produces.

## 7.3 A shape that we tried to raise to a theorem, and could not

<!-- origen: INFORME-GENERAL.md 4, rasgo 1, y su enmienda 1 -->
Across the grid, the forced outcome appeared only at intermediate levels and
never at the extremes. That was a real observation about what had been measured,
and the temptation was to state it as a property of the extremes.

<!-- origen: PROOFS-GENERAL.md pieza 1, refutacion con enumeracion entera.
     Las cifras eran nuestras y refutaban una frase nuestra: se imprimen. -->
<!-- CIFRAS: 40320 = results/general-theorems.tsv:3 p1.n3.k1.ordenaciones.recorridas;
     472 = results/general-theorems.tsv:4 p1.n3.k1.ordenaciones.forzadas;
     600 = results/general-theorems.tsv:34 p1.n3.k2.ordenaciones.forzadas -->
**It is false, and the refutation is by exhaustive enumeration.** In the smallest
dimension the space of all orderings can be traversed in full, all 40320 of
them, and at both extreme levels it contains forced orderings, with a witness
exhibited: 472 of them at the lower extreme and 600 at the upper. One
also turns up at an extreme level in the next dimension. Note that neither count
is zero while the corresponding cell of the table above is: the forced orderings
exist, and they lie outside the family the table samples.

<!-- origen: PROOFS-GENERAL.md 1.3, la correccion precisa -->
What had been measured was not false, it was narrower than the sentence
suggested: within the parametrised family there is indeed no forced ordering at
the extremes, and that remains true. The property belongs to the family, not to
the extremes.

<!-- origen: PROOFS-GENERAL.md pieza 1, y results/general-theorems.tsv; leccion
     metodologica -->
**The lesson about sampling is worth stating, because it is general.** The forced
class is small, and at the extreme levels it lies entirely outside the family
that was being sampled. No amount of sampling inside that family would ever have
produced a counterexample: the sample was not too small, it was drawn from the
wrong set. Enumerating the whole space in the one dimension where that is
possible is what settled it.

## 7.4 The reflected Gray code as a reference, and an error of ours

<!-- origen: INFORME-GRAY.md; deslinde obligatorio -->
The reflected Gray code enters as a **reference ordering** and not as a relative
of anything. It is built from its recursive definition and checked against the
closed form. A separation is needed on first appearance: in the Gray code
literature *balanced* refers to the transition counts per coordinate, and not to
the tie measured here.

<!-- origen: PROOFS-GENERAL.md enmienda 1, y INFORME-GENERAL.md enmienda 2. El
     error se cuenta, no se esconde. -->
**Its results in this table are corrected ones, and the correction is ours to
report.** An earlier run used a construction that added the wrong coordinate at
each recursive step, so it was not the ordering that had been declared. The
discrepancy surfaced only when dimension six was brought into the same table as
the smaller ones and the same object produced two different outcomes. The
declared construction reproduces the closed form and the earlier one does not.
With the declared construction the reference ordering falls in the same outcome
in every row of the table, and the apparent anomaly that an earlier draft tried
to explain **did not exist**. Both reports carry a visible amendment saying so.

<!-- origen: CONTACT-RULES.md enmienda 3 -->
That episode produced a working rule that this paper follows: a reimplementation
of an object already built inherits the verifications of the original, or states
in writing why it does not.

## 7.5 What the landscape shows and what it does not

<!-- origen: INFORME-GENERAL.md 4 y 5; NOVELTY.md punto 4 -->
The table shows that the outcome is not a function of the group: within a row the
group is fixed and the outcomes differ. It shows that the forced outcome is
possible in this family only at intermediate levels, and that outside the family
it is possible at the extremes too. And it shows the reference ordering behaving
uniformly across four dimensions.

<!-- origen: PREREGISTRATION-GENERAL.md c.2, declarado sin prediccion -->
It does not show a classification. Which combinations of group and ordering fall
into which outcome was declared, before any of this was measured, as a question
on which no prediction would be made, and it remains unanswered. The 14 rows in
four dimensions are a shape, not a theorem.
