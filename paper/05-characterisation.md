# 5. The characterisation

<!-- ENSAMBLAJE. Cada afirmacion con su fichero de origen en comentario. Cero
     cifras sin procedencia. Regla de PAPER.md. -->

Sections 3 and 4 build an apparatus: orbits, parities, forced and free. This
section removes it again. Two theorems turn the question of whether an ordering
is forced into a plain count, and a third tells exactly how much of the outcome
belongs to the group and how much to the ordering.

## 5.1 Forced means contributing half

<!-- origen: PROOFS-B31.md 1.1, teorema con su demostracion -->
> **Theorem 1.** An orbit is forced if and only if the number of discordant pairs
> it contains is exactly half its cardinality.

*Proof.* The contribution of an orbit is c or its cardinality minus c, according
to the single free bit. If it equals half the cardinality then c or the
cardinality minus c equals half, and either equation gives c equal to half, which
is the definition of forced. Conversely, if c is half then the two options
coincide at half. QED

<!-- origen: PROOFS-B31.md 1.1, parrafo "Lo que este teorema quita" -->
This removes the apparatus from the question of **whether**. To decide if an
ordering is forced one need not propagate parities or compute any epsilon: one
counts. The accounting is still needed to say **what interval** remains when the
ordering is not forced, but not to answer whether it is.

## 5.2 Forced means every difference class splits in two

<!-- origen: PROOFS-B31.md 1.2, teorema con su demostracion; el argumento no usa
     n = 3 ni la particion concreta -->
> **Theorem 2.** Let G contain all the translations. Then the orbits of G on
> pairs of vertices are the difference classes, that is, the sets of pairs whose
> difference runs over an orbit of the linear parts. Consequently an ordering is
> forced **if and only if, in every difference class, exactly half of its pairs
> are discordant**.

*Proof.* The translations act transitively on the pairs with a fixed difference,
since the pair at x goes to the pair at x plus v. The linear parts send a
difference d to its image. Hence the orbit of a pair is the set of pairs whose
difference lies in the orbit of d under the linear parts. Applying Theorem 1
orbit by orbit gives the statement. QED

<!-- origen: PROOFS-B31.md 1.2, nota de generalidad -->
The argument uses neither a particular dimension nor a particular partition, so
it holds for every group containing the full translation group, which covers all
the block systems considered here.

## 5.3 Forcing by a matching, and what is proved versus counted

<!-- origen: PROOFS-B31.md 2.1, con las dos direcciones separadas -->
Lemma 3 of section 3 gives a sufficient condition for an orbit to be forced: a
perfect matching of its pairs into couples, each couple carrying a witness. The
converse question, whether every forced orbit admits such a matching, has two
directions with different status, and we keep them apart.

<!-- origen: PROOFS-B31.md 2.1, direccion demostrada -->
**One direction is a theorem.** If an orbit is not forced, no perfect matching
can exist. Every edge of the relation graph joins pairs of opposite parity, so
the graph is bipartite between the two parity classes; if the orbit is not
forced those classes have different cardinalities, and no perfect matching
exists. This direction needs no search at all.

<!-- origen: PROOFS-B31.md 2.1 y 4.4, con el estatus declarado y su N. La cifra
     que faltaba: el 6960 es el tamano exacto de lo enumerado, y sin el la
     palabra "enumerativo" no dice cuanto. -->
<!-- CIFRAS: 1272 = results/hall-search.tsv:25 ordenaciones.forzadas.recorridas;
     6960 = results/hall-search.tsv:26 orbitas.forzadas.verificadas;
     0 = results/hall-search.tsv:27 fallos.de.Hall;
     200 = results/hall-search.tsv:20 n4.k2.forzadas.encontradas -->
**The other direction is enumerative, and stays enumerative.** If an orbit is
forced, the two classes have equal cardinality, but that alone does not give a
matching: Hall's condition is needed and could fail. It does not fail in any case
we examined, and the search was declared in advance, bounded, and reported with
its outcome branch fixed beforehand. Its size is the whole content of the word
*enumerative*, so it is printed here rather than left to the results file:
**1272** forced orderings traversed across three block systems and two dimensions,
of which 200 were found by search in the larger one, giving **6960** forced orbits
in which the matching was verified, and **0** failures of Hall's condition. That
is a count, not a proof. **We do not promote it to a theorem.** A failure could
occur in a higher dimension, in another partition, or in a case the search did
not reach.

## 5.4 The forced class is closed under reversing the ordering

<!-- origen: PROOFS-B31.md 2.4, teorema con su demostracion -->
> **Theorem.** If an ordering is forced, so is the ordering read backwards.

*Proof.* Reversing sends position i to N minus 1 minus i. This conjugates the
induced permutation of every group element, so orbits of pairs go to orbits of
pairs of the same cardinality. And within each pair, the vertex that was earlier
is now later, so its discordance is negated. The contribution of an orbit becomes
its cardinality minus the contribution, and being half is preserved. By Theorem
1, forced goes to forced. QED

<!-- origen: PROOFS-B31.md 2.4, los dos noes medidos -->
The corresponding statement for relabelling the vertices by a group element is
**false**, and measured to be false. That is not an anomaly: the group acts on
the vertices while the value function stays fixed, so relabelling produces a
genuinely different ordering, and there is no reason for the forced class to be
invariant under it.

## 5.5 What the group decides and what the ordering decides

<!-- origen: PROOFS-GENERAL.md pieza 2, con su teorema y su demostracion -->
> **Theorem.** The orbit cardinalities, and therefore the parity of the
> differences between compatible totals, are functions of the group alone. The
> values of c, the absolute parity of the count, and which of the three outcomes
> occurs, are not.

*Proof of the first half.* The cardinalities are independent of the ordering by
the lemma of section 4.1. For the differences: the set of compatible totals is
the minimum plus all subset sums of the gaps of the free orbits, and the gap of
an orbit is the absolute value of its cardinality minus twice its c. Modulo two
that gap is congruent to the cardinality, since the term in c is even. So the
parity of every gap, and hence of every difference between two compatible totals,
is fixed by the cardinality, which does not depend on the ordering. QED

<!-- origen: PROOFS-B31.md 1.2 y 2.1, el espacio entero de B(3,1); y
     PROOFS-GENERAL.md 2.3, donde este testigo sustituyo al anterior -->
<!-- CIFRAS: 16 = results/b31-characterization.tsv:3 grupo.orden;
     40320 = results/b31-characterization.tsv:7 ordenaciones;
     472 = results/b31-characterization.tsv:8 forzadas;
     39848 = results/b31-characterization.tsv:9 no.forzadas -->
*Proof of the second half, by witness.* Take the smallest block system in the
smallest dimension we enumerate, where the space of orderings is small enough to
be traversed in full: all **40320** of them, under one and the same group of
order 16. Of those, **472** are forced and **39848** are not. One group, two
outcomes; therefore the outcome is not a function of the group. QED

<!-- origen: PROOFS-B31.md 1.2, y results/b31-characterization.tsv. GUARDA: son
     el testigo del teorema y no se leen para nada mas. -->
Those two counts partition the space exactly, which the results file checks. They
are the witness of the theorem above and are not read for anything else.

## 5.6 What the characterisation is, and what it is not

<!-- origen: PROOFS-B31.md 3 -->
There **is** a characterisation, and it is Theorem 2: forced if and only if every
difference class splits exactly in two. It is proved, it is general, and it turns
the question into a count with no apparatus in the way.

<!-- origen: PROOFS-B31.md 2, la lista cerrada de candidatos y su desenlace -->
What there is **not** is a simpler invariant behind it. A closed list of
candidate invariants was declared in advance and tested against the full
partition of the enumerated space. Three of them fail to separate the forced
orderings from the rest. One separates, but only because it encodes the
definition. The one that separates informatively is the matching of section 5.3,
whose two directions have the mixed status described there. That is the state of
the question, and the negative half of it is a result too.
