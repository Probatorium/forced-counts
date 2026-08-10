# 4. The parity obstruction

<!-- ENSAMBLAJE. Cada afirmacion con su fichero de origen en comentario. Cero
     cifras sin procedencia. Regla de PAPER.md. -->

The accounting of section 3 leaves each orbit either forced or free, and the
free ones make the total an interval rather than a number. This section proves a
constraint that cuts across that freedom: under two hypotheses on the group, the
parity of the total is fixed by the structure, whatever the free bits do. When
that fixed parity differs from the parity of the tie, the tie becomes impossible.

## 4.1 The lemma that makes the whole section independent of the ordering

<!-- origen: PREREGISTRATION-GENERAL.md b.3, y comprobado en
     results/parity-hypotheses.tsv, clave t0 -->
> **Lemma.** The action on pairs of positions is conjugate, by the ordering, to
> the action on pairs of vertices. Hence the cardinalities of the orbits do not
> depend on the ordering at all: they depend only on the group.

*Proof.* The ordering is a bijection from positions to vertices, and it carries
one action to the other by conjugation. Conjugate actions have the same orbit
cardinalities. QED

<!-- origen: PROOFS-GENERAL.md pieza 2, con el reparto exacto -->
**The exact scope of this, because it is easy to overstate.** What is independent
of the ordering is the list of orbit cardinalities, and therefore also, as
section 5 shows, the parity of the differences between compatible totals. What is
**not** independent of the ordering are the values of c, and with them the
absolute parity of the count and which of the three outcomes the ordering
falls into. The group fixes the shape of the accounting; the ordering fills it.

## 4.2 The theorem, with two hypotheses

<!-- origen: PREREGISTRATION-GENERAL.md b.2, teorema general; y PROOFS.md 3.3
     para el caso n = 6 -->
> **Theorem.** Let G be a subgroup of B_n acting on the vertices, and suppose G
> contains the translations by a subspace V with dim V >= 2. Then every orbit of
> G on unordered pairs has even cardinality.

*Proof.* Write T for the group of translations by V, of order 2^k with
k = dim V. First, T is normal in G: conjugating the translation by v gives the
translation by P(v), where P is the linear part of the conjugating element, so
the set of translation vectors of G is closed under the linear parts. If V itself
is not invariant, replace it by W, the span of all images of V under the linear
parts of G; the translations by W lie in G, since conjugates of translations are
translations and products of translations are translations, W is invariant by
construction, and dim W >= dim V. So we may assume T normal.

Second, T acts freely on the vertices, since a nonzero translation fixes nothing.
Now take a pair p = {x, y}. A nonzero translation fixing the set {x, y} must swap
its two elements, so the stabiliser of p inside T contains the identity and at
most the translation by x + y, and its order is one or two. The T orbit of p
therefore has cardinality 2^k or 2^(k-1), and both are even because k >= 2.
Finally, since T is normal, G permutes the T orbits, so all T orbits inside a
single G orbit have the same cardinality. A G orbit is thus a disjoint union of
T orbits of equal even size, and its cardinality is even. QED

> **Corollary.** Under the same hypothesis, the two options of each orbit have
> the same parity, since they differ by the cardinality minus twice c, which is
> even. Hence the total is congruent modulo two to the sum of the c over the
> orbits, **whatever the free bits are**. The parity of the count is fixed by the
> structure.

## 4.3 The second hypothesis is necessary, and here is the witness

<!-- origen: results/parity-hypotheses.tsv, seccion t1, exhibido para n = 2, 3
     y 4; y PREREGISTRATION-GENERAL.md b.2 -->
<!-- CIFRAS: 2 = results/parity-hypotheses.tsv:8 t1.n2.orbitas.de.cardinal.impar;
     4 = results/parity-hypotheses.tsv:17 t1.n3.orbitas.de.cardinal.impar;
     8 = results/parity-hypotheses.tsv:26 t1.n4.orbitas.de.cardinal.impar -->
The condition dim V >= 2 cannot be dropped. Take G to be the two element group
consisting of the identity and the translation by a nonzero vector v. It
satisfies everything else: its elements are translations by a subspace contained
in G, they act freely, and T is normal in G because G is abelian. And the
conclusion fails at once: for any vertex x, the pair {x, x + v} is fixed by the
translation, so its orbit has cardinality one, which is odd.

<!-- origen: results/parity-hypotheses.tsv, seccion t1, tres dimensiones -->
The witness is exhibited for three dimensions, and it is the same witness in all
three: the pair whose two vertices differ exactly by v. It produces 2 orbits of
odd cardinality in the first dimension checked, 4 in the second and 8 in the
third, so the failure is not an artefact of one small case.

## 4.4 The normality hypothesis is redundant, and that is a theorem

<!-- origen: results/parity-hypotheses.tsv, seccion t2; PREREGISTRATION-GENERAL
     b.2, donde la depuracion de hipotesis quedo registrada antes de firmar -->
An earlier formulation of the theorem asked for three hypotheses: that T be the
translations by a subspace contained in G, that T be normal in G, and that the
dimension be at least two. The middle one is not needed, and the proof above
already contains the reason: given the translations by V inside G, the group also
contains the translations by W, the span of the images of V under the linear
parts of G. That W is invariant by construction, so its translations are normal,
and its dimension is at least that of V. The theorem then applies with W in place
of V.

<!-- origen: results/parity-hypotheses.tsv, seccion t2, caso con T no normal -->
<!-- CIFRAS: 16 = results/parity-hypotheses.tsv:32 t2.orden.del.grupo;
     2 = results/parity-hypotheses.tsv:33 t2.dim.V;
     3 = results/parity-hypotheses.tsv:35 t2.dim.W;
     5 = results/parity-hypotheses.tsv:39 t2.orbitas.de.pares;
     0 = results/parity-hypotheses.tsv:40 t2.orbitas.de.cardinal.impar -->
This is checked on an instance where T is genuinely not normal: a group of order
**16** built from a V of dimension 2 and a coordinate permutation that moves it.
The subgroup T fails to be normal, the closure argument produces an invariant
subspace W of dimension **3**, and of the **5** orbits of pairs, **0** have odd
cardinality.

<!-- origen: results/parity-hypotheses.tsv, seccion t3 -->
<!-- CIFRAS: 50 = results/parity-hypotheses.tsv:42 t3.casos.comprobados -->
A declared family of **50** further cases, over two dimensions and every subspace
of dimension at least two together with every coordinate permutation, produces no
orbit of odd cardinality either.

## 4.5 When the obstruction bites

<!-- origen: PROOFS.md 3.3, corolario del empate imposible -->
The tie is C(N, 2)/2. If the structural parity of the count differs from the
parity of that number, then no choice of the free bits can reach it, and the tie
is not merely unattained but **impossible**. This is the mechanism that
distinguishes one of the three historical orderings of section 6 from the other
two.

<!-- origen: PROOFS-GENERAL.md pieza 3, enmienda 1; refutacion medida -->
It is worth saying what this mechanism does **not** explain, since we tried it
and it failed. The parity argument is not what excludes the tie in every case
where the tie is excluded: there are orderings whose compatible totals share the
parity of the tie, whose interval contains the tie, and which still do not reach
it, because the set of compatible totals is coarse. Parity is one obstruction
among others, and we claim only what it proves.
