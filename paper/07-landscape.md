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
     results/general-landscape.tsv y results/general-n6.tsv -->
Dimensions three to six, every level, in one table with the same columns. The
order of the group respecting B(n, k) is k factorial times n minus k factorial
times 2 to the n, which was stated in the general preregistration before any of
this was run and is verified in all fourteen rows. The order of the group
depends only on the partition and not on the ordering, which the same table
confirms across thousands of orderings.

<!-- origen: TABLA-GENERAL.md; las tres casillas definidas en
     DEFINICIONES-GENERAL.md 5 -->
Each row reports the outcome for two fixed orderings, the reflected Gray code and
the canonical member of the parametrised family, and, where the space of
orderings of that family was small enough, the full distribution of the three
outcomes over it. Where it was not small enough, a sample with the frozen seed
was used and is labelled as a sample.

<!-- origen: TABLA-GENERAL.md, fila aparte de la Mawangdui historica -->
**One historical row belongs here and is kept apart.** The first historical
ordering does fit the family, at the middle level of dimension six, since its
octets are exactly those cosets. In the table it has **zero free orbits and a
single compatible total**, which is the forced outcome of section 6 read inside
the general frame rather than beside it.

## 7.3 A shape that we tried to raise to a theorem, and could not

<!-- origen: INFORME-GENERAL.md 4, rasgo 1, y su enmienda 1 -->
Across the grid, the forced outcome appeared only at intermediate levels and
never at the extremes. That was a real observation about what had been measured,
and the temptation was to state it as a property of the extremes.

<!-- origen: PROOFS-GENERAL.md pieza 1, refutacion con enumeracion entera -->
**It is false, and the refutation is by exhaustive enumeration.** In the smallest
dimension the space of all orderings can be traversed in full, and at both
extreme levels it contains forced orderings, with a witness exhibited. One also
turns up at an extreme level in the next dimension.

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
on which no prediction would be made, and it remains unanswered. Fourteen rows in
four dimensions are a shape, not a theorem.
