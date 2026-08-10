# 3. The orbit accounting

<!-- ENSAMBLAJE. Misma disciplina que la seccion 2: cada afirmacion con su
     fichero de origen en comentario. Las citas de homomesia van DONDE VIVE el
     resultado, no agrupadas al final. Regla fijada en PAPER.md. -->

Let G be a group acting on the vertices, sigma an ordering, and let pi_g denote
the permutation of positions induced by g, that is, sigma composed with g and
with the inverse of sigma. The group acts on the C(N, 2) pairs of positions
through pi_g. Everything in this section is a theorem about that action.

## 3.1 The state relation

<!-- origen: PROOFS.md pieza 1, Lema 0, con su demostracion -->
For a pair p of positions and an element g, write A for the bit that is one when
pi_g reverses the order of the two positions, and B for the bit that is one when
g reverses the binary order of the two vertices. Both are computable without
knowing whether p is discordant.

> **Lemma 0.** state(g p) = state(p) XOR A XOR B.

*Proof.* Write x and y for the vertices at the two positions of p, taken in
position order, so that state(p) is the truth value of v(x) > v(y). Since sigma
of pi_g of a position is g of the vertex at that position, the image pair carries
the vertices g(x) and g(y). If pi_g preserves the position order, state of the
image is the truth value of v(g(x)) > v(g(y)); if it reverses it, state of the
image is its negation. In both cases state of the image equals that truth value
XOR A. And by the definition of B, that truth value equals state(p) XOR B.
Substituting gives the formula. No value can tie, because x and y are distinct
and v is injective. QED

<!-- origen: PROOFS.md pieza 1, Lema 0b, y su consecuencia -->
> **Lemma 0b, and why chains give nothing.** epsilon(gh, p) = epsilon(g, h p)
> XOR epsilon(h, p), where epsilon(g, p) := A XOR B.

*Proof.* Apply Lemma 0 to h, to g, and to gh, and equate. QED

A chain of group elements applied to a pair therefore accumulates its epsilon,
and that accumulation is exactly the epsilon of the product, which is another
element of the group. Chaining reaches no further than a single element. The
useful generalisation of what follows is not longer chains; it is weaker
hypotheses.

## 3.2 The tie lemma

<!-- origen: PROOFS.md pieza 1, Lema 1, con su demostracion -->
Fix a representative in each orbit and let parity(p) be the sum of the epsilon
along any path from the representative to p, which is well defined because the
state exists. Let c denote the number of pairs of the orbit with parity one. Call
the orbit **forced** when c is half its cardinality.

> **Lemma 1.** If every orbit is forced, the total number of discordant pairs is
> C(N, 2)/2.

*Proof.* By Lemma 0, state(p) = state(rep) XOR parity(p) throughout the orbit, so
the orbit contributes c or its cardinality minus c according to the single free
bit. If the orbit is forced the two quantities coincide and equal half the
cardinality, whatever the state of the representative. Summing over orbits, and
since the orbits partition the set of pairs, the total is half of C(N, 2). QED

> **Corollary.** A group can only ever force the tie. It cannot determine the
> count and have it come out at some other value.

<!-- CITA, DONDE VIVE EL RESULTADO. origen: PRIOR-ART.md 14.1 y 14.4, artefacto
     Propp y Roby arXiv:1310.5201v6, seccion 2.1 verificada contra el PDF -->
**Prior owner of the germ.** The idea that an involution which sends the count to
its complement forces the average to one half on every orbit is the founding
example of the homomesy literature. Propp and Roby, in section 2.1 of
arXiv:1310.5201v6, take the permutations of {1, ..., n}, let tau send a
permutation to its reversal and f be the number of inversions, and observe that
since tau squared is the identity and f(pi) + f(tau(pi)) = n(n-1)/2, the
statistic f is c-mesic with c = n(n-1)/4. For n = 64 those two numbers are 2016
and 1008, which are our denominator and our tie: this is not an analogy, it is
the same arithmetic.

The difference is where the involution acts. Theirs reverses the permutation, so
it acts on positions and leaves the labels, and the identity is clean because
every pair is an inversion in exactly one of the two permutations. Ours is
complementation, which acts on the values and, by inducing a permutation of
positions, moves both at once. That is precisely why Lemma 0 needs the bit
epsilon = A XOR B, and why Lemma 1 is their argument restricted to the class of
pairs on which the position permutation preserves the order.

<!-- origen: NOVELTY.md, alcance; PRIOR-ART.md 14.5 -->
In the vocabulary of that literature, the corollary above says that the indicator
of discordance is 1/2-mesic on the forced orbits, in the sense of Definition 1 of
Propp and Roby. We use the term and do not present it as ours.

## 3.3 Forcing by a uniform witness

<!-- origen: PROOFS.md pieza 1, Lema 2, con su demostracion -->
> **Lemma 2.** If some g in G has epsilon(g, p) = 1 for every p in an orbit, that
> orbit is forced.

*Proof.* By Lemma 0 the state alternates along every cycle of g inside the orbit.
A cycle of odd length would force a state to equal its own negation, so every
cycle has even length and contains as many pairs of state one as of state zero.
Summing over cycles, the orbit contributes half its cardinality, and it does so
for either value of the free bit. QED

Such a g is called a **witness**. A witness is a finite certificate that can be
checked on its own: run through the orbit and verify that epsilon is one.

<!-- CITA, DONDE VIVE EL RESULTADO. origen: PRIOR-ART.md 14.2, punto 1, survey
     de Roby, Example 4, pagina 4, verificado contra el PDF -->
**Prior owner of the mechanism.** The mechanism of this lemma is stated in one
line in Roby's survey of homomesy, in his Example 4 on inversions under the
ninety degree rotation of permutation matrices, whose average is again n(n-1)/4:
"the proof of homomesy is easy: Q takes inversions to non-inversions, and
vice-versa." That is the witness argument, said there for another object.

<!-- origen: PRIOR-ART.md 14.2, punto 2, Lema 1 del survey de Roby -->
The same survey also contains the direction from a subgroup to the group: if a
triple exhibits homomesy for a subgroup, it does for the whole group, because
merging orbits with equal averages gives a larger orbit with that average. That
is the direction we use whenever a larger group is compared with a smaller one.

## 3.4 Forcing by a matching

<!-- origen: PROOFS.md pieza 1, Lema 3, con su demostracion, y los certificados
     de results/certificates.txt y results/certificate-mwd-01.txt -->
> **Lemma 3.** Let S be a set of pairs of positions. If S admits a perfect
> matching into couples {p, q} such that for each couple there is some g in G
> with g p = q and epsilon(g, p) = 1, then the contribution of S is exactly half
> its cardinality.

*Proof.* By Lemma 0, epsilon(g, p) = 1 gives state(q) = state(p) XOR 1, so
exactly one of the two pairs of a couple is discordant, without knowing which.
Since the couples partition S, the contribution is the number of couples. QED

Lemma 2 is the special case in which one and the same g serves for every couple:
its cycles inside the orbit have even length and split into consecutive couples.
What Lemma 3 adds is that the witness may change from couple to couple, and that
the hypothesis is required only on the chosen half rather than on the whole
orbit.

<!-- origen: PROOFS.md pieza 1, ultimo parrafo; contraprueba en
     results/proofs.tsv:142 a :144 -->
The lemma is not free. If a set does not contribute exactly half, its two parity
classes have different cardinalities and no perfect matching can exist, because
every edge of the relation graph joins opposite parities. The check has been
carried out where it matters: in the nineteen free orbits of the third historical
ordering there is no perfect matching in any of them.

## 3.5 What this accounting is for

<!-- origen: NOVELTY.md, punto 1 de SE AFIRMA COMO NUEVO -->
The four lemmas turn a question about one ordering into a question about the
orbits of a group action on pairs. Each orbit is either forced, and then its
contribution is fixed by the structure, or free, and then it contributes one of
two values. The total therefore lies in an interval, and the set of totals
compatible with the structure is the minimum plus the subset sums of the gaps.

<!-- origen: PRIOR-ART.md 14.4, limite del veredicto; NOVELTY.md -->
This is where the present work parts company with the literature just cited. In
homomesy, a case in which the average is not constant on orbits is a case to be
discarded: the phenomenon is the constancy. Here it is the case that is measured.
The free orbits are not failures of a phenomenon; they are the quantity of
freedom that the construction leaves, and the interval they define is the object
of the sections that follow.
