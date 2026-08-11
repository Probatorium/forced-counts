# 1. Introduction

<!-- ENSAMBLAJE. Escrita al final, cuando las ocho restantes ya estaban fijas,
     para que prometa exactamente lo que el resto cumple y nada mas. Cada
     afirmacion con su fichero de origen en comentario. -->

## 1.1 The question

<!-- origen: PREREGISTRATION-GENERAL.md (a), la pregunta fijada -->
Take an ordering of a finite set and a fixed reference order on the same set, and
count the pairs on which the two disagree. If the ordering is not arbitrary but
built by a rule, that rule usually has symmetries, and those symmetries constrain
the count. The question of this paper is how far the constraint goes:

> **When is the number of discordant pairs of a constructed ordering determined
> by the symmetry group that its construction respects?**

<!-- origen: PREREGISTRATION-GENERAL.md (a), las tres casillas -->
The answer is not a single dichotomy. A group can leave the count completely
free, or pin it down to a single value, or do something in between that is more
interesting than either: leave an interval of possible values and, inside that
interval, make one particular value **impossible**. Those three outcomes, forced,
bounded, and barred, are what the paper measures and, where it can, proves.

## 1.2 The object

<!-- origen: PROOFS.md, convenios; PREREGISTRATION-GENERAL.md (d) -->
The set is the vertex set of the n-cube, the reference order is the binary order
induced by reading a vertex as a number, and the symmetries available are the
hyperoctahedral group B_n, which permutes coordinates and complements subsets of
them. An ordering is a bijection from positions to vertices; a construction
partitions it into blocks; and the group of interest is the subgroup of B_n that
sends every block onto a block.

<!-- JERARQUIA DE CONTRIBUCION, dicha una vez y aqui, para que el lector sepa
     desde el principio que pesa mas. origen: NOVELTY.md, alcance -->
What the paper contributes is the general apparatus: the orbit accounting, the
parity obstruction and the two characterisation theorems of sections 3 to 5,
which are stated and proved for an arbitrary dimension and an arbitrary subgroup.
The three constructed orderings below are the motivation for that apparatus and
its first application, not the result it is built to deliver.

<!-- origen: data/PROVENANCE.md; INFORME.md -->
Three orderings of the 6-cube carry the concrete weight of the paper. They come
from a published replication package, read at a fixed tag, and they are of
interest here for a structural reason rather than a historical one: each is built
by a documented rule with a visible symmetry, and the three rules are different
enough that they populate all three outcomes. Two of them force the count to the
midpoint of its range. The third bars that midpoint entirely.

<!-- origen: TABLA-GENERAL.md; INFORME-GENERAL.md -->
To see whether those results are about the constructions or about the dimension,
the same apparatus is run over a family of block systems in dimensions three to
six, with a reference ordering that has nothing to do with the historical ones.

## 1.3 What this paper does not claim

<!-- origen: NOVELTY.md, seccion NO SE AFIRMA; y PRIOR-ART.md -->
The three orderings named above have a long history and a long literature, and
this paper is not a contribution to it. Nothing here is claimed about who built
those sequences, when, with what knowledge or with what intent. What is measured
is a property of a received list of sixty four objects, and the measurement is
silent about its origin.

<!-- CITA VERBATIM desde el artefacto local. origen:
     scratchpad common/proyecto-bibliografias/Moore_Structural_Elements.pdf,
     Moore, "Structural Elements in the King Wen Sequence of Hexagrams", Oracle
     Paper No. 1, February 2005, pagina impresa 6, pagina 8 del PDF, seccion
     "Context: Alternative Sequences". Leida de la pagina renderizada del PDF,
     que es el canal fuerte, y no de la conversion OCR. -->
The caution is not ours to invent, and it is worth quoting from the literature
itself. Discussing an alternative arrangement, Moore (2005) writes:

> "Shao Yong's 'Fu Xi' order of the hexagrams, being a Song dynasty production,
> is too late to concern us here; besides, it was never intended to order the
> actual text of the *Zhouyi*, and the notion of ordering the text in this
> fashion (and in particular that such a textual-ordering has priority to the
> King Wen sequence) is a 20th century invention [Moore 2005]."

<!-- origen: PRIOR-ART.md 5.2, identidad del artefacto; leido en esta maquina -->
Moore, *Structural Elements in the King Wen Sequence of Hexagrams*, Oracle Paper
No. 1, February 2005, printed page 6.

The warning there is about attributing a modern way of ordering to an ancient
source. Our version of the same caution runs in the other direction and is
stricter: we attribute nothing at all. A symmetry that a construction respects is
a property of the construction as it has reached us, and to say that a count is
forced by that symmetry is a statement about the arithmetic of the list, not
about anybody's design.

## 1.4 What the paper contains, section by section

<!-- origen: los propios ficheros de paper/, escritos antes que esta seccion -->
**Section 2** fixes the cube, the group, the four bit conventions and the
denominator, defines discordant pairs, and separates that term from three
neighbours that already own words we use: the sinological *inversion*, the two
established senses of *balance*, and the Coxeter length in type B.

**Section 3** builds the accounting. Lemma 0 relates the discordance of a pair to
that of its image under a group element by two computable bits. Lemma 1 shows
that if every orbit is forced then the total is exactly half the number of pairs,
with the corollary that a group can only ever force that midpoint and no other
value. Lemmas 2 and 3 give sufficient conditions for an orbit to be forced, by a
uniform witness and by a matching. The germ of Lemma 1 and the mechanism of Lemma
2 belong to the homomesy literature and are cited where they are used.

**Section 4** proves the parity obstruction: if the group contains the
translations by a subspace of dimension at least two, every orbit has even
cardinality, so the parity of the count is fixed by the structure whatever the
free choices do. The dimension hypothesis is necessary, by an exhibited witness,
and a normality hypothesis that an earlier formulation carried is proved
redundant.

**Section 5** removes the apparatus again. Being forced is equivalent to
contributing exactly half, and when the group contains all translations it is
equivalent to every difference class splitting exactly in two. It also separates,
with proof, what the group decides from what the ordering decides.

**Section 6** applies all of it to the three orderings, including a mechanism
previously claimed for one of them which the measurements refute, the anatomy of
the residue left by the third, and the point at which we stop and say so.

**Section 7** varies the dimension over a parametrised family of block systems,
and reports two refutations that came out of trying to raise measured shapes into
theorems, one of them of an error of our own.

**Section 8** lists what is open, each item with what was measured and with the
specific task that would close it.

**Section 9** describes what a reader can verify, and how the order in which
things were fixed and measured is itself checkable.

## 1.5 A note on how this paper was made

<!-- origen: EFFORT.md, PREREGISTRATION.md, PREREGISTRATION-GENERAL.md -->
Every measurement in this paper was preceded, in a separate and earlier commit of
a public repository, by a written statement of what was going to be measured
and, where predictions were made, of what would count as a refutation of them. Several of those statements were then refuted
by the measurements, including one prediction whose refutation criterion turned
out to be unfailable and is reported as a defect rather than cashed as a success.
Section 9 explains the arrangement. It is mentioned here because it changes how
the results below should be read: where this paper says that something was
declared in advance, that is a checkable claim and not a rhetorical one.
