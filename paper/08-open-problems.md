# 8. Open problems

<!-- ENSAMBLAJE. Cada afirmacion con su fichero de origen en comentario. Regla de
     PAPER.md: esto no es una lista de deseos. Cada abierto va con lo que se
     midio y con lo que faltaria para cerrarlo. -->

Four things are open. Each is stated with what was measured, and with what would
close it, so that the section is a list of specified tasks rather than of wishes.

## 8.1 Does Hall's condition ever fail on a forced orbit?

<!-- origen: PROOFS-B31.md 2.1, la direccion demostrada -->
**What is proved.** One direction needs no search: if an orbit is not forced, no
perfect matching of the relation graph can exist, because every edge joins pairs
of opposite parity and the two parity classes then have different cardinalities.

<!-- origen: PROOFS-B31.md 4, y results/hall-search.tsv -->
<!-- CIFRAS: 472 = results/hall-search.tsv:7 n3.k1.forzadas;
     600 = results/hall-search.tsv:12 n3.k2.forzadas;
     200 = results/hall-search.tsv:20 n4.k2.forzadas.encontradas;
     6960 = results/hall-search.tsv:26 orbitas.forzadas.verificadas;
     0 = results/hall-search.tsv:27 fallos.de.Hall -->
**What is measured.** The converse, that a forced orbit always admits such a
matching, requires Hall's condition, which could fail. A bounded search was
declared in advance, with its space, its seed and both outcome branches fixed
before running: the 472 and 600 forced orderings of two block systems in
the smallest dimension, taken whole, and 200 forced orderings of a third
system in the next dimension, found using Theorem 2 of section 5. That is
6960 forced orbits in which the matching was verified, across three block
systems and two dimensions, and 0 failures.

<!-- origen: PROOFS-B31.md 4.4, la rama del desenlace escrita antes -->
**What was deliberately not done.** The status was not promoted. Absence of a
failure in a finite search is not a theorem, and the branch that said so was
written before the search ran.

**What would close it.** Either a proof that the relation graph of a forced orbit
always satisfies Hall's condition, or a single counterexample: a forced orbit
whose two parity classes admit no perfect matching. A counterexample would also
refute the equivalence between the matching criterion and forcedness, which is
currently the informative half of the characterisation of section 5.

## 8.2 How many orderings are forced?

<!-- origen: PROOFS-B31.md 1.2, y results/b31-characterization.tsv -->
<!-- CIFRAS: 40320 = results/general-theorems.tsv:3 p1.n3.k1.ordenaciones.recorridas;
     472 = results/general-theorems.tsv:4 p1.n3.k1.ordenaciones.forzadas;
     600 = results/general-theorems.tsv:34 p1.n3.k2.ordenaciones.forzadas -->
**What is measured.** In the smallest dimension the space of all 40320
orderings is enumerable, and the number of forced ones is known exactly for both
block systems, under a single group in each case: 472 for one and 600 for
the other. Theorem 2 of section 5 says exactly which orderings those are: the
ones in which every difference class splits in two.

**What is missing.** A formula, or even an asymptotic. The characterisation turns
membership into a countable condition but does not count the members. The
condition is a system of simultaneous exact-halving constraints, one per
difference class, over the symmetric group on the vertices, and nothing here
says how many permutations satisfy such a system.

**What would close it.** A count, in closed form or asymptotically, of the
permutations satisfying the difference-class conditions of Theorem 2, in terms of
n and of the block system.

## 8.3 The residue of the third historical ordering

<!-- origen: INFORME-RESIDUO5.md, desenlace; NOVELTY.md punto 4 -->
<!-- CIFRAS: 5 = results/residuo5.tsv:89 f1.suma.de.desviaciones;
     19 = results/residuo5.tsv:6 orbitas.libres;
     1013 = results/residuo5.tsv:7 observado -->
**What is measured.** The count, 1013, differs from the tie by 5, that
difference is decomposed completely over the 19 free orbits, and the
decomposition has no culprit: every free orbit deviates and the deviations very
nearly cancel. A closed list of five candidate structures was declared before
measuring; one of them narrows the interval and none explains the difference. The
residue is declared **informative relative to that list**.

**What would close it, structurally.** A structure, outside the declared list,
that the construction respects and that absorbs the difference. The declaration
is relative to the list precisely so that this remains possible.

### The one principled route that remains, named as future work

<!-- origen: PRIOR-ART.md 1.2, artefacto Radisic leido entero; el emparejamiento
     de prioridad de reversion y su unicidad -->
There is one route we can name rather than gesture at. Radisic [10] proves that the
pairing of the third ordering is the unique cost-minimising equivariant matching
under his criteria. Conditioning on that matching leaves a family of orderings:
all those that realise it, differing only in the order of the pairs and in the
orientation within each pair. Inside that family, the received ordering is one
point, and its count could be located among the counts of the rest.

<!-- GUARDA. origen: INFORME-GRUPO.md enmienda 1, que es ley tambien aqui -->
**That is an inferential question, and it is not asked in this paper.** Locating
a value inside a family and reading anything from where it falls requires a null
declared before looking, a family of comparisons fixed before looking, and
discipline of multiplicity over everything that could have been looked at and was
not. This work builds none of the three, and therefore cannot support such a
reading with these numbers or with larger ones.

<!-- origen: la instruccion de la sesion nombra el metodo; el articulo NO se ha
     leido aqui y se cita como referencia y no como artefacto leido -->
The method that would govern it has a name and a citable version, given here as a
pointer and not as a read artefact: the stopping-criterion work of the same
author on nested reference sets, *Uninformative rungs: an order-theoretic
stopping criterion for nested reference sets* [4], deposited at
doi 10.5281/zenodo.21750029. We have not read it in the course of this work and
make no claim about its contents; we name it as the framework under which the
question above would have to be posed.

## 8.4 The shape of the classification

<!-- origen: PREREGISTRATION-GENERAL.md (a) y c.2 -->
**What was asked.** For which subgroups, and under which conditions on the
ordering, is the count forced to the tie, bounded in an interval, or barred from
the tie by parity. The general preregistration fixed that question and declared,
before any measurement, that no prediction would be made about its answer.

<!-- origen: TABLA-GENERAL.md; PROOFS-GENERAL.md pieza 2 -->
**What is measured.** The 14 rows in four dimensions of section 7, the three
outcomes populated, and a proved split of what belongs to the group and what to
the ordering: the orbit cardinalities and the parity of the differences between
compatible totals are functions of the group; the values of c, the absolute
parity and the outcome are not.

**What would close it.** A criterion that, given the group and the ordering,
returns the outcome, and that reduces on the historical cases to what sections 4
to 6 prove. Section 5 gives such a criterion for the forced outcome alone,
through the difference classes; nothing here separates the other two outcomes in
the same way.

## 8.5 One thing that is not open

<!-- origen: PROOFS-GENERAL.md enmienda 1 -->
For the record: the apparent anomaly of the reference ordering, which an earlier
draft listed as a question, is not open. It was an error in our own construction
of that ordering, it was corrected, and it is documented as an error in the
amendments cited in section 7 rather than removed from the record.
