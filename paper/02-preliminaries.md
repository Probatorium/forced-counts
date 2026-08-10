# 2. Preliminaries

<!-- ENSAMBLAJE. Cada afirmacion lleva en comentario el fichero y el sitio del
     repositorio de donde viene. Cero cifras sin procedencia. Regla heredada de
     PAPER.md: esto es ensamblaje verificable, no redaccion de memoria. -->

## 2.1 The cube and its vertices

<!-- origen: PROOFS.md, seccion "Convenios y nombre" -->
A hexagram is a vector of six binary coordinates. We number the coordinates
1 to 6, calling coordinate 1 the bottom line and coordinate 6 the top line, and
we write yang for the value one and yin for the value zero. There are 2^6 = 64
of them, and they are the vertices of the 6-cube.

<!-- origen: PREREGISTRATION-GENERAL.md (d); todo lo general se enuncia para n -->
Everything below is stated for a general dimension n, with N = 2^n vertices, and
specialised to n = 6 only where the object under study requires it.

## 2.2 The group

<!-- origen: PROOFS.md pieza 4, verificado en results/proofs.tsv:112 a :116 -->
The maps we consider are those that permute the n coordinates and then
complement a subset of them. There are n! 2^n of them, which for n = 6 is 46080.
This is the **hyperoctahedral group B_n**, the symmetry group of the n-cube.

**Correspondence, in one line:** the vertices of the n-cube are the binary
vectors, permuting lines is permuting coordinate axes, and complementing a subset
of lines is reflecting in the corresponding coordinate hyperplanes.

<!-- origen: PROOFS.md pieza 4; comprobado que la escritura es unica -->
Every element of B_n is written uniquely as a coordinate permutation followed by
a complementation mask, so this parametrisation counts no element twice, and the
action preserves adjacency of the cube, that is, the relation of differing in a
single coordinate.

## 2.3 Orderings, reference orders, and the four conventions

<!-- origen: PREREGISTRATION.md (d) y PREREGISTRATION-GENERAL.md (d) -->
An **ordering** is a bijection from positions 0, ..., N-1 to the vertices. To
compare an ordering with a numerical order we must fix how a vertex is read as a
number, and there are two independent binary choices: whether yang counts as one
or as zero, and whether the bottom line is the most or the least significant bit.
That gives **four conventions**, fixed in advance, and every count in this work
is reported under all four rather than under the most favourable one.

<!-- origen: PRIOR-ART.md 5.3; Schoter, The Oracle Vol 2 No 7, Summer 1998,
     Definition 6, "Sequence Parameters". Interseccion declarada en NOVELTY.md -->
The second of those two choices is not ours. Schöter [Sc] parametrises the counting
orders of the hexagrams by, among other things, "whether the lower or upper line
is the least significant bit", and names the two readings Rising Yang and Sinking
Yang. We use that parameter and do not present it as new.

<!-- origen: PREREGISTRATION.md (d): denominador C(64,2) -->
The **reference order** throughout is the binary order induced by the convention
in use, and the denominator for every rate is C(N, 2), the number of unordered
pairs of distinct positions. For n = 6 that is 2016, and its half is 1008.

## 2.4 Discordant pairs

<!-- origen: NOVELTY.md, vocabulario vinculante; TITLE.md, deslinde obligatorio -->
Given an ordering and the reference order, a pair of distinct positions is
**discordant** when the two orders disagree on it: the vertex placed earlier by
the ordering is the larger one under the reference order. The statistic of this
paper is the number of discordant pairs.

<!-- DESLINDE OBLIGATORIO EN PRIMERA APARICION. origen: TITLE.md, veredicto del
     termino discordance; y Bjorner y Brenti verificado en PRIOR-ART.md 8 -->
**First appearance, and what the term already means.** Discordant pairs are
counted **between the ordering and a fixed reference order**, in the standard
sense of rank correlation, where a pair is concordant when two rankings agree on
it and discordant when they disagree. It is the same object as the combinatorial
inversion number: Björner and Brenti [BB] define, in their equation (1.25),
inv(x) = card{(i, j) : i < j, x(i) > x(j)}, which is exactly the count above with
the reference order as the second ranking. It is also the quantity in the
numerator of Kendall's tau, whose denominator is the same C(N, 2), so the value
C(N, 2)/2 that we will call the **tie** is precisely the point where that tau is
zero. We do not use tau anywhere; we count the pairs.

## 2.5 Three names that are taken, and are not this

<!-- origen: NOVELTY.md, vocabulario vinculante; PRIOR-ART.md 6, 8 y 2 -->
Three words that appear near this work already have owners, and we separate them
here, once, rather than in a closing note.

<!-- origen: PRIOR-ART.md 6, medido en cuatro artefactos: Gritter p. 3 con el
     termino chino, Cook, Drasny con zonggua, Moore con invertible -->
**Inversion.** In the sinological literature on the Yijing, *inversion* names the
180 degree turn of a hexagram, *fandui*, which is a symmetry of the figure and
not a discordant pair. Gritter [Gr] states the two pairing principles as inversion and
opposition and gives the Chinese terms; Cook [Co] devotes a chapter to inversion and
obversion; Drasny [Dr] writes of inverses of hexagrams, *zonggua*; Moore [Mo]
speaks of invertible pairs. In this paper *inversion* is never used for the statistic.

<!-- origen: PRIOR-ART.md 2 y 7; Radisic 4.3 y Mutze 3.2, los dos verificados
     contra su PDF -->
**Balance.** The word is occupied twice over in the neighbourhood. Radisic [Ra] uses
it for Hamming weight, writing that weight preservation "may be viewed as
preservation of yin-yang balance" and adding at once that formally it is Hamming
weight. In the Gray code literature Mütze [Mu] defines a *balanced* Gray code by the
condition that the transition counts satisfy |c_i - 2^n/n| < 2, that is, a
condition on how often each coordinate flips. Neither is the quantity studied
here, and we therefore call C(N, 2)/2 the **tie** and not the balance point.

<!-- origen: PRIOR-ART.md 8; Bjorner y Brenti secciones 8.1 y 8.2, verificadas -->
**Length in type B.** This is the subtlest of the three, because we name B_n and
we count inversions in the same breath. In Coxeter theory the length function of
a group of type B is a count of certain inversions of signed permutations, as
Björner and Brenti [BB] describe in their sections 8.1 and 8.2. That is not our
count. Here B_n is only the group acting on the vertices, and the discordant
pairs are those of the ordering against the binary reference order, not the
Coxeter length of any element of B_n.

## 2.6 Block systems and what it means to respect one

<!-- origen: DEFINICIONES-GRUPO.md, nocion R1, declarada antes de enumerar -->
A construction partitions the ordering into contiguous **blocks**: eight octets
for one of the sequences below, eight palaces for another, thirty two adjacent
pairs for the third. We say that a map **respects** the construction when it
sends every block onto a block, as a set. This is the notion fixed in advance,
and where a stronger one is used, namely that the map also preserves the index
within the block, it is said explicitly.

<!-- origen: PROOFS.md 2.1, 2.6, 3.2; los tres ordenes son teoremas, no
     mediciones -->
For each construction, the set of elements of B_n that respect it is a subgroup,
being the stabiliser of a structure, and we compute it exactly rather than
sampling it.
