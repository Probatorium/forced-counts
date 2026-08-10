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

<!-- origen: INFORME.md, PROOFS.md piezas 2 y 3; los tres desenlaces, ahora con
     sus cifras: un resumen que anuncia tres desenlaces y no dice ninguno
     obliga al lector a creerse la palabra. -->
<!-- CIFRAS: 2016 = results/measurements.tsv:6 denominador;
     1008 = results/measurements.tsv:7 valor.esperado.por.azar;
     1013 = results/measurements.tsv:19 inv.KingWen.yang1.bottomMSB;
     3836 = results/measurements.tsv:93 exhaustivo.octetos.orden.de.familia.aciertos;
     40320 = results/measurements.tsv:92 exhaustivo.octetos.orden.de.familia.ordenes;
     484 = results/group-measurements.tsv:34 cuenta.solo.complementacion.Mawangdui.aportacion_forzada;
     957 = results/group-measurements.tsv:169 cuenta.R1.KingWen.minimo;
     1059 = results/group-measurements.tsv:170 cuenta.R1.KingWen.maximo;
     52 = results/group-measurements.tsv:174 cuenta.R1.KingWen.totales_alcanzables -->
Applied to three constructed orderings of the 6-cube that have come down to us,
with 2016 pairs and a midpoint of 1008, the three outcomes all occur. Two of the
constructions force the count to **1008**, and for one of them the demonstration
is complete with no enumerative residue; a mechanism previously claimed for the
other is refuted here, since the closure it rests on forces only 484 of the 2016
pairs and survives rearrangements that destroy the result, the midpoint coming
out in 3836 of the 40320 of them. The third construction makes 1008 impossible by
the parity obstruction: its structure leaves the interval [957, 1059] and exactly
**52** compatible totals within it, 1008 is not among them, and the observed count
is **1013**.

<!-- origen: INFORME-RESIDUO5.md, desenlace y declaracion de frontera -->
<!-- CIFRAS: 5 = results/residuo5.tsv:89 f1.suma.de.desviaciones;
     19 = results/residuo5.tsv:6 orbitas.libres -->
That difference of **5** is decomposed completely over the **19** free orbits and
has no culprit: every free orbit deviates, and the deviations nearly cancel. Against a list of
candidate structures declared before measuring, one narrows the interval, namely
the construction's own pairing involution, which is not affine and so was absent
from a group that is exactly its centraliser; none explains the difference. We
therefore declare the residue informative relative to that list, and stop.

<!-- origen: TABLA-GENERAL.md; PROOFS-GENERAL.md pieza 1 y enmienda 1 -->
A landscape of 14 rows over block systems in dimensions three to six populates
the three outcomes away from the historical cases and records two refutations of
shapes we tried to raise into theorems, one of them of an error of our own.

<!-- origen: EFFORT.md, PREREGISTRATION.md, PREREGISTRATION-GENERAL.md -->
Every measurement was preceded, in an earlier commit of a public repository, by a
written statement of what would be measured and what would refute it, and that
ordering is checkable.
