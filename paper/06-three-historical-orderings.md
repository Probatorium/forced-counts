# 6. The three historical orderings

<!-- ENSAMBLAJE. Cada afirmacion con su fichero de origen en comentario.
     GUARDA DE ESTA SECCION: la enmienda 1 de INFORME-GRUPO.md es ley aqui. Ni
     una frase de significancia, de diseno o de intencion. Los recuentos van con
     su procedencia y no se leen mas alla. Y la declaracion de no anacronismo de
     NOVELTY.md rige el conjunto. -->

<!-- origen: data/PROVENANCE.md, procedencia del dato -->
The three orderings are taken from a published replication package, read at a
fixed tag, and only the sequences themselves are taken from it: no figure of that
package enters any computation here. Two of the three are constructions with
documented rules and are rebuilt from those rules in our own code, which halts if
the rebuild fails to reproduce the extracted sequence. The third is a received
datum and cannot be derived from anything.

<!-- origen: data/PROVENANCE.md, corroboracion; results/corroboration.tsv -->
That third sequence has since been checked against an independent artefact, the
full binary table printed in the appendix of another paper, under that paper's
own bit convention. All sixty four positions agree. What is corroborated is the
transcription, that is, that the list carries no error peculiar to a single
source; nothing historical is corroborated by it.

## 6.1 Mawangdui: forced, and the mechanism that was claimed for it is false

<!-- origen: INFORME.md, tabla de la seccion 1; cuatro convenciones -->
The count is the tie, in all four conventions.

<!-- origen: PROOFS.md 2.1 y 2.2, teoremas -->
The block system is the fibres of the upper trigram, that is, the cosets of the
subspace spanned by the three lower lines. The group of elements of B_6
respecting it is exactly the set of maps whose linear part does not mix the two
trigrams, with any mask, and the orbits of pairs are exactly the classes given by
the pair of difference weights, one for each trigram.

<!-- origen: PROOFS.md 2.3 a 2.5, con los testigos; el certificado esta en
     results/certificate-mwd-01.txt -->
Every one of those classes is forced, and the demonstration is in two parts. Nine
of them are forced by a witness that is argued rather than exhibited: complement
the lower trigram, and the value order of the pair reverses while the block, and
therefore the position order, does not. The remaining classes are forced by
witnesses that are exhibited and verified, and one of them has no uniform witness
at all in the whole group and needed the matching lemma, with a certificate that
is deposited pair by pair and can be checked line by line. By Lemma 1, the total
is the tie.

<!-- REFUTACION. origen: INFORME.md seccion 3, y el control exhaustivo de
     results/measurements.tsv. No se esconde: se cuenta como refutacion. -->
**The mechanism that was previously claimed for this count does not hold, and
saying so is part of the result.** The claim was that closure under
complementation forces the count. Closure does hold, and it is concrete: the
complement sends each octet onto another octet. But closure alone forces fewer
than half of the discordant pairs, and the rest fall in the class it leaves free.
The control settles it: the family order of the octets can be permuted in every
possible way, all such rearrangements keep the closure intact, and the tie comes
out in fewer than one in ten of them. Closure is true of the construction and is
not what forces the count. What forces it is the full group together with the
received family order.

## 6.2 Jing Fang: forced, and the demonstration is complete

<!-- origen: PROOFS.md 2.6, teorema con su demostracion -->
Each palace is a translate of one and the same set of masks, read off the
construction rules, and the palace heads are exactly the diagonal subspace. No
difference of that mask set lies in the diagonal, which is why the palaces
partition the vertices.

<!-- origen: PROOFS.md 2.6, unicidad del estabilizador, con las multiplicidades
     de las diferencias -->
The group respecting the palaces is exactly the translations by the diagonal, and
this is proved rather than enumerated: any respecting map must preserve the
multiset of differences of the mask set, one line never appears in any
difference, the multiplicities of the remaining lines are pairwise distinct
enough to pin the permutation down to the identity, and the mask is then forced
into the diagonal.

<!-- origen: PROOFS.md 2.7 y 2.8, con los certificados de
     results/certificates.txt -->
The orbits are classified by hand into three families, and every one of them is
forced: those inside a single palace by an argued witness, the complement, which
here is the translation by the all ones vector of the diagonal; and the rest by
exhibited witnesses, deposited orbit by orbit. By Lemma 1 the total is the tie.
**For this ordering the demonstration is complete: there is no enumerative
residue.**

## 6.3 King Wen: the tie is impossible

<!-- origen: PROOFS.md 3.1, propiedad de la secuencia recibida -->
The construction pairs the sequence into thirty two adjacent blocks. Those blocks
are the orbits of size two of the half turn, together with the pairs formed by
complementation among the hexagrams that the half turn leaves fixed.

<!-- CITA, DONDE VIVE EL RESULTADO. origen: PRIOR-ART.md 1.4 y PROOFS.md 3.1,
     linea de cita; artefacto Radisic arXiv:2601.07175v3, Teorema 3.3 -->
**Prior owner of this characterisation.** It is the complete equivariance of
Radisic [Ra], Theorem 3.3 of arXiv:2601.07175v3, which states that every King Wen pair
is either the complement or the reversal of its partner and splits the thirty two
pairs into palindromes paired by complement, anti-symmetric ones where reversal
and complement coincide, and generic ones paired by reversal. That statement has
prior date and a formal verification in Lean 4, which we do not have. We reached
it independently and before opening our review of the literature, which the
commit history dates, and independent does not mean first.

<!-- origen: PROOFS.md 3.2, teorema con su demostracion -->
From that block system, the group respecting it is exactly the centraliser of the
half turn inside B_6, and this is proved: the block differences are precisely the
nonzero vectors fixed by the half turn, a respecting map must preserve that
subspace, its only weight two elements are the three that pair the mirror lines,
so the linear part commutes with the half turn, and the mask is then forced to be
fixed by it.

<!-- origen: PROOFS.md 3.3, teorema de paridad y sus dos corolarios -->
Every orbit of that group on pairs has even cardinality, by the theorem of
section 4 applied to the translations by the fixed subspace. Hence the parity of
the count is fixed by the structure. That parity is odd, and the tie is even.
**The tie is therefore impossible for this ordering**: not merely unattained, but
outside the set of totals compatible with the structure.

<!-- origen: results/measurements.tsv y results/group-measurements.tsv, via
     INFORME.md e INFORME-GRUPO.md -->
The observed count, the interval left by the structure, the number of compatible
totals and the compatible total nearest to the tie are all reported in the
results files, with the interval containing the tie and the tie not among the
compatible values.

## 6.4 One structure narrows it, and it is the construction's own rule

<!-- origen: DEFINICIONES-RESIDUO5.md, lista cerrada declarada antes de medir -->
A closed list of five candidate structures was declared before measuring
anything: the nuclear hexagram operation with its exact definition, the two part
division of the received sequence, whose literature has a located owner [HM], and three maps defined through the positions.
Nothing outside that list was tried.

<!-- origen: INFORME-RESIDUO5.md 2.1 y 2.2 -->
Two of the five contribute no bijection at all, so they cannot narrow anything,
and that was known before running. Two of the remaining three narrow a great
deal but generate groups beyond a bound that was declared in advance, and a
narrowing obtained with a large unstructured group was declared in advance not to
count. It does not count.

<!-- origen: INFORME-RESIDUO5.md 2.2, tabla de A5 -->
The one that counts is the pairing involution itself, the map that sends each
hexagram to its partner in the construction. **It is not affine**, which is why
it was not in the group at all, even though that group is precisely its
centraliser. Adding it doubles the group, removes two of the free orbits and
narrows the interval. It does not force, and the tie remains impossible.

## 6.5 The anatomy of the residue, as a table

<!-- origen: INFORME-RESIDUO5.md 1.1, vector completo; se reporta como tabla y
     no se lee mas alla. GUARDA: cero lenguaje de significancia. -->
The count differs from the tie by a small amount, and the natural question is
where that difference sits. The full decomposition over the free orbits, with
cardinality, half, contribution and deviation for each one, is reported as a
table in the results and in the accompanying report. Two things can be read off
it directly, and nothing else is read off it here:

<!-- origen: INFORME-RESIDUO5.md 1.2 -->
first, **every free orbit deviates**; there is no orbit carrying the difference
and none carrying none of it, and the deviations very nearly cancel;

<!-- origen: INFORME-RESIDUO5.md 1.3 -->
second, the deviations of odd size are exactly those of the orbits that contain
the construction's own pairs, and the even ones are all the rest.

<!-- origen: INFORME-RESIDUO5.md 1.4; GUARDA explicita -->
The crossing of the deviating orbits against the two structural features of the
declared list is likewise reported as a table. It is a set of counts with their
provenance. There is no declared null, no family of comparisons fixed in advance
and no discipline of multiplicity behind it, and in this work that means it is
not read as evidence of anything.

## 6.6 Where this stops

<!-- origen: INFORME-RESIDUO5.md, desenlace; NOVELTY.md, punto 4 -->
None of the five declared structures explains the residue. After the one that
narrows, the residue is unchanged, the tie is still impossible, and the remaining
free orbits still spread the deviation across almost all of them.

> **The residue is therefore declared informative relative to this list.** The
> decomposition exists, it is complete, and it has no culprit.

<!-- origen: INFORME-RESIDUO5.md, desenlace; la frase de cierre -->
**The mathematics reaches bottom where editorial choice begins.** What remains of
the difference, once the symmetry that the construction respects has been
exhausted and the four additional declared structures have been tried, is not a
residue that structure can absorb. It is what the received sequence has of choice
rather than of rule.

<!-- GUARDA final. origen: NOVELTY.md, seccion NO SE AFIRMA -->
That sentence is about the limits of this method, not about the people who
ordered the sequence. Nothing here is claimed about design, about intention or
about ancient knowledge, and the declaration is relative to the declared list:
another structure, not tried here, could absorb what this one leaves.
