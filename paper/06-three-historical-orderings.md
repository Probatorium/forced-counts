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
<!-- CIFRAS: 64 = results/corroboration.tsv:11 posiciones.comparadas -->
That third sequence has since been checked against an independent artefact, the
full binary table printed in the appendix of another paper, under that paper's
own bit convention. All 64 positions agree. What is corroborated is the
transcription, that is, that the list carries no error peculiar to a single
source; nothing historical is corroborated by it.

<!-- origen: PREREGISTRATION.md (d), denominador congelado antes de medir -->
<!-- CIFRAS: 2016 = results/measurements.tsv:6 denominador;
     1008 = results/measurements.tsv:7 valor.esperado.por.azar -->
Every count below is a number of discordant pairs out of 2016, the number of
unordered pairs of the 64 positions, and the tie is 1008.

## 6.1 Mawangdui: forced, and the mechanism that was claimed for it is false

<!-- origen: INFORME.md, tabla de la seccion 1; las cuatro convenciones dan lo
     mismo, y por eso se declaran las cuatro y no la mas favorable -->
<!-- CIFRAS: 1008 = results/measurements.tsv:11 inv.Mawangdui.yang1.bottomMSB;
     1008 = results/measurements.tsv:12 inv.Mawangdui.yang1.bottomLSB;
     1008 = results/measurements.tsv:13 inv.Mawangdui.yang0.bottomMSB;
     1008 = results/measurements.tsv:14 inv.Mawangdui.yang0.bottomLSB -->
The count is 1008 in all four conventions, which is the tie exactly.

<!-- origen: PROOFS.md 2.1 y 2.2, teoremas -->
<!-- CIFRAS: 2304 = results/group-measurements.tsv:5 grupo.R1.Mawangdui.orden;
     36 = results/proofs.tsv:16 p2.mwd.permutaciones.que.preservan.V;
     15 = results/proofs.tsv:21 p2.mwd.numero.de.orbitas -->
The block system is the fibres of the upper trigram, that is, the cosets of the
subspace spanned by the three lower lines. The group of elements of B_6
respecting it is exactly the set of maps whose linear part does not mix the two
trigrams, with any mask: 36 such permutations with all 64 masks, of order
2304. Its orbits of pairs are exactly the classes given by the pair of
difference weights, one for each trigram, and there are 15 of them.

<!-- origen: PROOFS.md 2.3 a 2.5, con los testigos; el certificado esta en
     results/certificate-mwd-01.txt -->
<!-- CIFRAS: 9 = results/proofs.tsv:26 p2.mwd.orbitas.demostradas.forzadas;
     1568 = results/proofs.tsv:27 p2.mwd.pares.cubiertos.por.la.demostracion;
     784 = results/proofs.tsv:28 p2.mwd.aportacion.demostrada;
     15 = results/group-measurements.tsv:50 cuenta.R1.Mawangdui.orbitas_forzadas;
     0 = results/group-measurements.tsv:51 cuenta.R1.Mawangdui.orbitas_libres;
     1008 = results/group-measurements.tsv:53 cuenta.R1.Mawangdui.aportacion_forzada -->
Every one of those classes is forced, and the demonstration is in two parts. 9
of them, covering 1568 pairs and contributing 784, are forced by a witness that
is argued rather than exhibited: complement the lower trigram, and the value
order of the pair reverses while the block, and therefore the position order,
does not. The remaining classes are forced by witnesses that are exhibited and
verified, and one of them has no uniform witness at all in the whole group and
needed the matching lemma, with a certificate that is deposited pair by pair and
can be checked line by line. All 15 orbits are forced and 0 are free, so
by Lemma 1 the forced contribution is the whole count, 1008, and the width of the
interval is zero.

<!-- REFUTACION. origen: INFORME.md seccion 3, y el control exhaustivo de
     results/measurements.tsv. No se esconde: se cuenta como refutacion. -->
<!-- CIFRAS: 484 = results/group-measurements.tsv:34 cuenta.solo.complementacion.Mawangdui.aportacion_forzada;
     540 = results/group-measurements.tsv:32 cuenta.solo.complementacion.Mawangdui.orbitas_libres;
     1049 = results/group-measurements.tsv:41 cuenta.solo.complementacion.Mawangdui.totales_alcanzables;
     40320 = results/measurements.tsv:92 exhaustivo.octetos.orden.de.familia.ordenes;
     3836 = results/measurements.tsv:93 exhaustivo.octetos.orden.de.familia.aciertos;
     0.09514 = results/measurements.tsv:94 exhaustivo.octetos.orden.de.familia.tasa -->
**The mechanism that was previously claimed for this count does not hold, and
saying so is part of the result.** It was claimed in the preregistration of this
repository, in the section that listed a prior result to be verified and
reported as a retrodiction, and that is where the reader can find it stated
before any measurement was taken. The claim was that closure under
complementation forces the count. Closure does hold, and it is concrete: the
complement sends each octet onto another octet. But the group generated by
complementation alone forces only 484 of the 2016 pairs, leaves 540 orbits
free, and admits 1049 different compatible totals: an interval, not a value. The
control settles it exhaustively rather than by sample. The family order of the
octets can be permuted in every one of the 40320 possible ways, all such
rearrangements keep the closure intact, and the tie comes out in 3836 of
them, a rate of 0.09514. Closure is true of the construction and is not what
forces the count. What forces it is the full group of order 2304 together with
the received family order.

## 6.2 Jing Fang: forced, and the demonstration is complete

<!-- origen: INFORME.md, tabla de la seccion 1; las cuatro convenciones -->
<!-- CIFRAS: 1008 = results/measurements.tsv:15 inv.JingFang.yang1.bottomMSB;
     1008 = results/measurements.tsv:16 inv.JingFang.yang1.bottomLSB;
     1008 = results/measurements.tsv:17 inv.JingFang.yang0.bottomMSB;
     1008 = results/measurements.tsv:18 inv.JingFang.yang0.bottomLSB -->
The count is again 1008 in all four conventions.

<!-- origen: PROOFS.md 2.6, teorema con su demostracion -->
<!-- CIFRAS: 28 = results/proofs.tsv:43 p2.jf.diferencias.de.M -->
Each palace is a translate of one and the same set of masks, read off the
construction rules, and the palace heads are exactly the diagonal subspace. None
of the 28 differences of that mask set lies in the diagonal, which is why the
palaces partition the vertices.

<!-- origen: PROOFS.md 2.6, unicidad del estabilizador, con las multiplicidades
     de las diferencias -->
<!-- CIFRAS: 8 = results/group-measurements.tsv:13 grupo.R1.JingFang.orden;
     "12 15 16 12 15 0" = results/proofs.tsv:44 p2.jf.multiplicidad.por.linea -->
The group respecting the palaces is exactly the translations by the diagonal, of
order 8, and this is proved rather than enumerated: any respecting map must
preserve the multiset of differences of the mask set, whose multiplicities line
by line are 12 15 16 12 15 0, so one line never appears in any difference and the
remaining multiplicities are distinct enough to pin the permutation down to the
identity, after which the mask is forced into the diagonal.

<!-- origen: PROOFS.md 2.7 y 2.8, con los certificados de
     results/certificates.txt -->
<!-- CIFRAS: 280 = results/group-measurements.tsv:107 cuenta.R1.JingFang.orbitas_forzadas;
     0 = results/group-measurements.tsv:108 cuenta.R1.JingFang.orbitas_libres;
     1 = results/group-measurements.tsv:117 cuenta.R1.JingFang.totales_alcanzables -->
The 280 orbits are classified by hand into three families, and every one of
them is forced: those inside a single palace by an argued witness, the
complement, which here is the translation by the all ones vector of the diagonal;
and the rest by exhibited witnesses, deposited orbit by orbit. There are 0
free orbits and exactly 1 compatible total, so by Lemma 1 that total is the
tie. **For this ordering the demonstration is complete: there is no enumerative
residue.**

## 6.3 King Wen: the tie is impossible

<!-- origen: INFORME.md, tabla de la seccion 1. AQUI SI DIFIEREN las convenciones,
     y por eso se imprimen las dos cifras y no una. -->
<!-- CIFRAS: 1013 = results/measurements.tsv:19 inv.KingWen.yang1.bottomMSB;
     1013 = results/measurements.tsv:20 inv.KingWen.yang1.bottomLSB;
     1003 = results/measurements.tsv:21 inv.KingWen.yang0.bottomMSB;
     1003 = results/measurements.tsv:22 inv.KingWen.yang0.bottomLSB -->
The count is 1013 under the two conventions that read yang as one, and
1003 under the two that read yang as zero. The two are symmetric about the
tie, since exchanging the roles of yang and yin turns every discordant pair into a
concordant one, and 1013 plus 1003 is twice 1008. Neither is the tie. Everything
below explains why neither could have been.

<!-- origen: PROOFS.md 3.1, propiedad de la secuencia recibida. DEFINICION EN
     PRIMERA APARICION: el giro se comprobo contra src/proofs.py, funcion rho,
     que manda la linea k a la linea 7 menos k. -->
The **half turn** is the element of B_6 whose coordinate permutation is
(1 6)(2 5)(3 4), reversing the order of the six lines, and whose complementation
mask is zero. It is an involution, it fixes the vertex of all yin, and a
hexagram it fixes is a palindrome.

<!-- origen: PROOFS.md 3.1, propiedad de la secuencia recibida -->
<!-- CIFRAS: 28 = results/proofs.tsv:72 p3.orbitas.del.giro.de.tamano.dos;
     8 = results/proofs.tsv:73 p3.palindromos -->
<!-- CIFRAS DERIVADAS: 32 = 28 + 8/2 -->
The construction pairs the sequence into 32 adjacent blocks of two: the 28
orbits of size two of the half turn, together with the 8 hexagrams that the
half turn leaves fixed, paired among themselves by complementation.

<!-- CITA, DONDE VIVE EL RESULTADO. origen: PRIOR-ART.md 1.4 y PROOFS.md 3.1,
     linea de cita; artefacto Radisic arXiv:2601.07175v3, Teorema 3.3 -->
**Prior owner of this characterisation.** It is the complete equivariance of
Radisic (2026), Theorem 3.3 of arXiv:2601.07175v3, which states that every King
Wen pair
is either the complement or the reversal of its partner and splits the 32
pairs into palindromes paired by complement, anti-symmetric ones where reversal
and complement coincide, and generic ones paired by reversal. That statement has
prior date and a formal verification in Lean 4, which we do not have. We reached
it independently and before opening our review of the literature, which the
commit history dates, and independent does not mean first.

<!-- origen: PROOFS.md 3.2, teorema con su demostracion -->
<!-- CIFRAS: 384 = results/group-measurements.tsv:21 grupo.R1.KingWen.orden;
     8 = results/proofs.tsv:77 p3.Fix(giro).tamano;
     3 = results/proofs.tsv:78 p3.elementos.de.peso.dos.en.Fix(giro);
     48 = results/proofs.tsv:79 p3.permutaciones.que.preservan.Fix(giro) -->
<!-- CIFRAS DERIVADAS: 384 = 48 * 8 -->
From that block system, the group respecting it is exactly the centraliser of the
half turn inside B_6, of order 384, and this is proved rather than counted:
the block differences are precisely the nonzero vectors of the subspace of size
8 fixed by the half turn, a respecting map must preserve that subspace, its
only 3 elements of weight two are the ones that pair the mirror lines, so the
linear part commutes with the half turn and there are 48 such permutations, and
the mask is then forced to be fixed by the half turn, which leaves 8 masks. The
predicted order 48 times 8 is 384, and it agrees with the enumeration.

<!-- origen: PROOFS.md 3.3, teorema de paridad y sus dos corolarios -->
Every orbit of that group on pairs has even cardinality, by the theorem of
section 4 applied to the translations by the fixed subspace. Hence the parity of
the count is fixed by the structure. That parity is odd, and the tie is even.
**The tie is therefore impossible for this ordering**: not merely unattained, but
outside the set of totals compatible with the structure.

<!-- origen: results/group-measurements.tsv, via INFORME-GRUPO.md. Es la cifra
     que el auditor externo echaba en falta: la seccion explicaba el 1013 sin
     imprimirlo. -->
<!-- CIFRAS: 17 = results/group-measurements.tsv:164 cuenta.R1.KingWen.orbitas_forzadas;
     19 = results/group-measurements.tsv:165 cuenta.R1.KingWen.orbitas_libres;
     374 = results/group-measurements.tsv:167 cuenta.R1.KingWen.aportacion_forzada;
     957 = results/group-measurements.tsv:169 cuenta.R1.KingWen.minimo;
     1059 = results/group-measurements.tsv:170 cuenta.R1.KingWen.maximo;
     52 = results/group-measurements.tsv:174 cuenta.R1.KingWen.totales_alcanzables;
     1007 = results/group-measurements.tsv:178 cuenta.R1.KingWen.alcanzable_mas_cercano_al_esperado -->
<!-- CIFRAS DERIVADAS: 36 = 17 + 19; 103 = 1059 - 957 + 1 -->
Here is the whole account in figures. Of the 36 orbits of that group on pairs,
17 are forced and contribute 374, and 19 are free. The structure
therefore leaves the interval [957, 1059], and inside it exactly 52 totals
are compatible, of the 103 integers the interval contains. The observed 1013 is
one of the 52. The tie, 1008, lies well inside the interval and is **not** one of
them: the nearest compatible total to it is 1007, one below. The tie is not
missed by a small amount, it is absent from the list.

## 6.4 One structure narrows it, and it is the construction's own rule

<!-- origen: DEFINICIONES-RESIDUO5.md, lista cerrada declarada antes de medir -->
A closed list of five candidate structures was declared before measuring
anything: the nuclear hexagram operation with its exact definition, the two part
division of the received sequence, whose literature has a located owner (Hacker
& Moore, 2003), and three maps defined through the positions.
Nothing outside that list was tried.

<!-- origen: INFORME-RESIDUO5.md 2.1 y 2.2 -->
Two of the five contribute no bijection at all, so they cannot narrow anything,
and that was known before running. Two of the remaining three narrow a great
deal but generate groups beyond a bound that was declared in advance, and a
narrowing obtained with a large unstructured group was declared in advance not to
count. It does not count.

<!-- origen: INFORME-RESIDUO5.md 2.2, tabla de A5 -->
<!-- CIFRAS: 768 = results/residuo5.tsv:187 f2.A5.orden.del.grupo.generado;
     17 = results/residuo5.tsv:191 f2.A5.orbitas.libres;
     961 = results/residuo5.tsv:192 f2.A5.intervalo.minimo;
     1055 = results/residuo5.tsv:193 f2.A5.intervalo.maximo;
     94 = results/residuo5.tsv:194 f2.A5.anchura;
     0 = results/residuo5.tsv:195 f2.A5.empate.alcanzable -->
<!-- CIFRAS DERIVADAS: 102 = 1059 - 957 -->
The one that counts is the pairing involution itself, the map that sends each
hexagram to its partner in the construction. **It is not affine**, which is why
it was not in the group at all, even though that group is precisely its
centraliser. Adding it takes the group from 384 to 768, cuts the free orbits
from 19 to 17, and narrows the interval from [957, 1059] to
[961, 1055], that is, from a width of 102 to one of 94. It does not
force, the tie is still not reachable, which the table records as 0, and the
observed count does not move: changing the group changes neither the sequence nor
its discordance.

## 6.5 The anatomy of the residue, as a table

<!-- origen: INFORME-RESIDUO5.md 1.1, vector completo; se reporta como tabla y
     no se lee mas alla. GUARDA: cero lenguaje de significancia. -->
<!-- CIFRAS: 5 = results/residuo5.tsv:89 f1.suma.de.desviaciones -->
<!-- CIFRAS DERIVADAS: 5 = 1013 - 1008 -->
The count differs from the tie by 5, that being 1013 minus 1008, and the
natural question is where those 5 sit. Each free orbit contributes its half plus
a deviation, and the deviations sum to exactly 5. Table 1 gives the whole
decomposition over the 19 free orbits, one row each, with cardinality, half,
contribution and deviation. Two things can be read off Table 1 directly, and
nothing else is read off it here:

<!-- CIFRAS: 192 = results/residuo5.tsv:13 f1.orbita.00.cardinal;
     96 = results/residuo5.tsv:14 f1.orbita.00.mitad;
     90 = results/residuo5.tsv:15 f1.orbita.00.aportacion;
     -6 = results/residuo5.tsv:16 f1.orbita.00.desviacion;
     96 = results/residuo5.tsv:17 f1.orbita.01.cardinal;
     48 = results/residuo5.tsv:18 f1.orbita.01.mitad;
     50 = results/residuo5.tsv:19 f1.orbita.01.aportacion;
     2 = results/residuo5.tsv:20 f1.orbita.01.desviacion;
     96 = results/residuo5.tsv:21 f1.orbita.02.cardinal;
     48 = results/residuo5.tsv:22 f1.orbita.02.mitad;
     52 = results/residuo5.tsv:23 f1.orbita.02.aportacion;
     4 = results/residuo5.tsv:24 f1.orbita.02.desviacion;
     96 = results/residuo5.tsv:25 f1.orbita.03.cardinal;
     48 = results/residuo5.tsv:26 f1.orbita.03.mitad;
     46 = results/residuo5.tsv:27 f1.orbita.03.aportacion;
     -2 = results/residuo5.tsv:28 f1.orbita.03.desviacion;
     96 = results/residuo5.tsv:29 f1.orbita.04.cardinal;
     48 = results/residuo5.tsv:30 f1.orbita.04.mitad;
     46 = results/residuo5.tsv:31 f1.orbita.04.aportacion;
     -2 = results/residuo5.tsv:32 f1.orbita.04.desviacion;
     96 = results/residuo5.tsv:33 f1.orbita.05.cardinal;
     48 = results/residuo5.tsv:34 f1.orbita.05.mitad;
     46 = results/residuo5.tsv:35 f1.orbita.05.aportacion;
     -2 = results/residuo5.tsv:36 f1.orbita.05.desviacion;
     96 = results/residuo5.tsv:37 f1.orbita.06.cardinal;
     48 = results/residuo5.tsv:38 f1.orbita.06.mitad;
     46 = results/residuo5.tsv:39 f1.orbita.06.aportacion;
     -2 = results/residuo5.tsv:40 f1.orbita.06.desviacion;
     96 = results/residuo5.tsv:41 f1.orbita.07.cardinal;
     48 = results/residuo5.tsv:42 f1.orbita.07.mitad;
     46 = results/residuo5.tsv:43 f1.orbita.07.aportacion;
     -2 = results/residuo5.tsv:44 f1.orbita.07.desviacion;
     96 = results/residuo5.tsv:45 f1.orbita.08.cardinal;
     48 = results/residuo5.tsv:46 f1.orbita.08.mitad;
     54 = results/residuo5.tsv:47 f1.orbita.08.aportacion;
     6 = results/residuo5.tsv:48 f1.orbita.08.desviacion;
     96 = results/residuo5.tsv:49 f1.orbita.09.cardinal;
     48 = results/residuo5.tsv:50 f1.orbita.09.mitad;
     52 = results/residuo5.tsv:51 f1.orbita.09.aportacion;
     4 = results/residuo5.tsv:52 f1.orbita.09.desviacion;
     48 = results/residuo5.tsv:53 f1.orbita.10.cardinal;
     24 = results/residuo5.tsv:54 f1.orbita.10.mitad;
     28 = results/residuo5.tsv:55 f1.orbita.10.aportacion;
     4 = results/residuo5.tsv:56 f1.orbita.10.desviacion;
     48 = results/residuo5.tsv:57 f1.orbita.11.cardinal;
     24 = results/residuo5.tsv:58 f1.orbita.11.mitad;
     22 = results/residuo5.tsv:59 f1.orbita.11.aportacion;
     -2 = results/residuo5.tsv:60 f1.orbita.11.desviacion;
     48 = results/residuo5.tsv:61 f1.orbita.12.cardinal;
     24 = results/residuo5.tsv:62 f1.orbita.12.mitad;
     22 = results/residuo5.tsv:63 f1.orbita.12.aportacion;
     -2 = results/residuo5.tsv:64 f1.orbita.12.desviacion;
     24 = results/residuo5.tsv:65 f1.orbita.13.cardinal;
     12 = results/residuo5.tsv:66 f1.orbita.13.mitad;
     16 = results/residuo5.tsv:67 f1.orbita.13.aportacion;
     4 = results/residuo5.tsv:68 f1.orbita.13.desviacion;
     12 = results/residuo5.tsv:69 f1.orbita.14.cardinal;
     6 = results/residuo5.tsv:70 f1.orbita.14.mitad;
     5 = results/residuo5.tsv:71 f1.orbita.14.aportacion;
     -1 = results/residuo5.tsv:72 f1.orbita.14.desviacion;
     12 = results/residuo5.tsv:73 f1.orbita.15.cardinal;
     6 = results/residuo5.tsv:74 f1.orbita.15.mitad;
     8 = results/residuo5.tsv:75 f1.orbita.15.aportacion;
     2 = results/residuo5.tsv:76 f1.orbita.15.desviacion;
     12 = results/residuo5.tsv:77 f1.orbita.16.cardinal;
     6 = results/residuo5.tsv:78 f1.orbita.16.mitad;
     4 = results/residuo5.tsv:79 f1.orbita.16.aportacion;
     -2 = results/residuo5.tsv:80 f1.orbita.16.desviacion;
     4 = results/residuo5.tsv:81 f1.orbita.17.cardinal;
     2 = results/residuo5.tsv:82 f1.orbita.17.mitad;
     3 = results/residuo5.tsv:83 f1.orbita.17.aportacion;
     1 = results/residuo5.tsv:84 f1.orbita.17.desviacion;
     4 = results/residuo5.tsv:85 f1.orbita.18.cardinal;
     2 = results/residuo5.tsv:86 f1.orbita.18.mitad;
     3 = results/residuo5.tsv:87 f1.orbita.18.aportacion;
     1 = results/residuo5.tsv:88 f1.orbita.18.desviacion;
     5 = results/residuo5.tsv:89 f1.suma.de.desviaciones;
     19 = results/residuo5.tsv:6 orbitas.libres -->

**Table 1.** *The residue of the third ordering, decomposed over its free orbits.*

| orbit | cardinality | half | contribution | deviation |
|---|---|---|---|---|
| o0 | 192 | 96 | 90 | -6 |
| o1 | 96 | 48 | 50 | 2 |
| o2 | 96 | 48 | 52 | 4 |
| o3 | 96 | 48 | 46 | -2 |
| o4 | 96 | 48 | 46 | -2 |
| o5 | 96 | 48 | 46 | -2 |
| o6 | 96 | 48 | 46 | -2 |
| o7 | 96 | 48 | 46 | -2 |
| o8 | 96 | 48 | 54 | 6 |
| o9 | 96 | 48 | 52 | 4 |
| o10 | 48 | 24 | 28 | 4 |
| o11 | 48 | 24 | 22 | -2 |
| o12 | 48 | 24 | 22 | -2 |
| o13 | 24 | 12 | 16 | 4 |
| o14 | 12 | 6 | 5 | -1 |
| o15 | 12 | 6 | 8 | 2 |
| o16 | 12 | 6 | 4 | -2 |
| o17 | 4 | 2 | 3 | 1 |
| o18 | 4 | 2 | 3 | 1 |

The rows are labelled o0 to o18 in the order the accounting produces them; the
label is a row name and not a measurement.

<!-- origen: INFORME-RESIDUO5.md 1.2 -->
first, **every free orbit deviates**; there is no orbit carrying the difference
and none carrying none of it, and the deviations very nearly cancel;

<!-- origen: INFORME-RESIDUO5.md 1.3 -->
second, the deviations of odd size are exactly those of the orbits that contain
the construction's own pairs, and the even ones are all the rest.

<!-- origen: INFORME-RESIDUO5.md 1.4; GUARDA explicita -->
The crossing of the deviating orbits against the two structural features of the
declared list is **not** printed here. It stays in results/residuo5.tsv, under
the keys that name each orbit against each feature, and the reason for leaving it
there rather than promoting it is the guard below: it is a set of counts with
their provenance and nothing is read from it. There is no declared null, no family of comparisons fixed in advance
and no discipline of multiplicity behind it, and in this work that means it is
not read as evidence of anything.

## 6.6 Where this stops

<!-- origen: INFORME-RESIDUO5.md, desenlace; NOVELTY.md, punto 4 -->
None of the five declared structures explains the residue. After the one that
narrows, the residue is unchanged, the tie is still impossible, and the remaining
free orbits still spread the deviation across almost all of them.

> **The residue is therefore declared informative relative to this list.**
> Informative in the structural sense, as the part of the count not determined
> by the declared structures; no inferential claim is attached to the word. The
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
