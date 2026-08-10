# Abstract

<!-- ENSAMBLAJE. Escrito el ultimo, cuando las nueve secciones ya estaban fijas.
     GUARDA: cero lenguaje de significancia, diseno o intencion, que en un
     resumen es donde mas tienta. Primera frase nombrando el referente del
     titulo, que es lo que el propio titulo deja implicito. -->

<!-- origen: TITLE.md, nota para el decisor; el referente se nombra aqui -->
We count the **discordant pairs of an ordering against the binary order** of the
vertices of the n-cube, in the standard sense of rank correlation, and ask when
that count is determined by the subgroup of the hyperoctahedral group B_n that
the construction of the ordering respects.

<!-- origen: PROOFS.md pieza 1, Lema 1 y su corolario; PROOFS-B31.md 1.1 -->
The apparatus is an accounting over the orbits of that subgroup acting on pairs
of positions. Each orbit is either **forced**, contributing exactly half its
cardinality whatever else happens, or **free**, contributing one of two values.
A group can therefore only ever force the midpoint of the range, never any other
value; equivalently, it can only force Kendall's tau against the binary order to
be exactly zero.

<!-- origen: PROOFS.md 3.3, obstruccion de paridad y su corolario -->
<!-- origen: PROOFS-B31.md 1.1 y 1.2, Teoremas 1 y 2 -->
Two theorems remove the apparatus once it has been built. An orbit is forced
precisely when it contains as many discordant pairs as concordant ones; and when
the subgroup contains all translations, an ordering is forced precisely when
every difference class splits exactly in two. A third result cuts the other way:
if the subgroup contains the translations by a subspace of dimension at least
two, every orbit has even cardinality, so the parity of the count is fixed by the
structure, and when that parity differs from the parity of the midpoint the
midpoint becomes **impossible** rather than merely unattained. The dimension
hypothesis is necessary, by an exhibited witness.

<!-- origen: INFORME.md, PROOFS.md piezas 2 y 3; los tres desenlaces -->
Applied to three constructed orderings of the 6-cube that have come down to us,
the three outcomes all occur. Two of the constructions force the count to the
midpoint, and for one of them the demonstration is complete with no enumerative
residue; a mechanism previously claimed for the other is refuted here, since the
closure it rests on forces less than half of the count and survives rearrangements
that destroy the result. The third construction makes the midpoint impossible by
the parity obstruction, and its count differs from the midpoint by a small
amount.

<!-- origen: INFORME-RESIDUO5.md, desenlace y declaracion de frontera -->
That difference is decomposed completely over the free orbits and has no culprit:
every free orbit deviates, and the deviations nearly cancel. Against a list of
candidate structures declared before measuring, one narrows the interval, namely
the construction's own pairing involution, which is not affine and so was absent
from a group that is exactly its centraliser; none explains the difference. We
therefore declare the residue informative relative to that list, and stop.

<!-- origen: TABLA-GENERAL.md; PROOFS-GENERAL.md pieza 1 y enmienda 1 -->
A landscape over block systems in dimensions three to six populates the three
outcomes away from the historical cases and records two refutations of shapes we
tried to raise into theorems, one of them of an error of our own.

<!-- origen: EFFORT.md, PREREGISTRATION.md, PREREGISTRATION-GENERAL.md -->
Every measurement was preceded, in an earlier commit of a public repository, by a
written statement of what would be measured and what would refute it, and that
ordering is checkable.
