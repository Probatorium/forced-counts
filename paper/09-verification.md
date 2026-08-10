# 9. Methods of verification

<!-- ENSAMBLAJE. Cada afirmacion con su fichero de origen en comentario. Regla de
     PAPER.md. -->

<!-- origen: EFFORT.md, commit raiz; y la historia entera del repositorio -->
The repository is not an appendix to this paper. Its history is part of the
result, because most of what is claimed here is a claim about **when** something
was known: what was fixed before a measurement, what was measured afterwards, and
what changed when the two disagreed. A reader who wants to check that ordering
has the commit history, and the ordering is what a finished text cannot show.

## 9.1 The two preregistrations, and the defect in the first

<!-- origen: PREREGISTRATION.md, commit raiz, sin codigo ni datos ni cifras -->
The root commit of the repository contains a preregistration and nothing else: no
analysis code, no data, no measured figure. It separates three things by name: a
prior result that was to be verified and reported as retrodiction, a prediction
made before running anything with its refutation criterion attached, and an open
discrepancy on which no bet was placed. It also fixes, in advance, the bit
conventions to be tried and the denominator, so that neither could be chosen
after seeing results.

<!-- origen: PREREGISTRATION-GENERAL.md, con su fase previa y su seccion c.1 -->
The second preregistration, for the general phase, was signed after a phase whose
only permitted activity was proving things: two hypotheses that had been in doubt
were settled by theorem before signing, which is why its prediction section is
almost empty and says so. The temptation it records having avoided is worth
naming: a prediction could have been manufactured by narrowing the space until
the answer became unknown again, and that is choosing the question after seeing
the answer.

<!-- origen: INFORME.md seccion 4, defecto del criterio de refutacion. Se cuenta
     como defecto y no se retira. -->
**The refutation criterion of the first preregistration was defective, and this
is the place to say so.** It asked, for the prediction, that a hexagram be
exhibited whose image under complementation lay outside the construction. Since
every ordering contains all the vertices, that image is always the same set: no
sequence could ever have failed the criterion. A preregistered criterion that
cannot be failed is not a criterion. It was reported as a defect in the very
report that would have benefited from claiming the prediction as confirmed, the
preregistration was left unamended, and the prediction was not cashed.

## 9.2 The effort log

<!-- origen: EFFORT.md y effort/README.md; el instrumento se creo antes de medir
     nada del objeto de estudio -->
Every working session opens and closes an entry in an append only log. Each
record carries the previous record's hash, so editing an old line breaks the
chain and a verifier reports it; the tool that writes the log has no operation
that rewrites or deletes. The first entry is marked retroactive and says that a
reconstructed record is not equivalent to one taken live, which is the only
honest thing to do with a log that begins one commit late.

<!-- origen: effort/classification.tsv y effort/README.md -->
The log also classifies every file as apparatus or analysis, separating what was
written here from what was extracted, so that the proportion between building
instruments and producing results is visible rather than anecdotal.

<!-- origen: los registros de tipo dead_end del propio log -->
Dead ends are recorded as their own kind of entry, with their cost. There are
several: a command written with the wrong working tree, a process left running
after its replacement had been launched, an analysis that hung because a group
closure exploded exactly as a declaration had warned it might.

## 9.3 Rules that were born during the work, with their origin

<!-- origen: CONTACT-RULES.md enmienda 3, con el caso de Gray citado -->
**A reimplementation inherits the verifications of the original, or states in
writing why it does not.** This rule exists because of a specific failure. The
reference ordering of section 7 was first built with two checks tied to its
definition, and when it was reimplemented for a variable dimension the
reimplementation dropped both, built a different ordering, and cost a full
session explaining an anomaly that did not exist. The check it dropped would have
caught the error at the moment the function was written.

<!-- origen: registro de esfuerzo, correcciones de la sesion 21 -->
**No figure enters a commit message before a checker has printed it.** This rule
exists because two commit messages in one day carried counts that had been
written from memory rather than counted, in a repository whose whole point is
that figures come with provenance. The counts were small and harmless; the habit
was not.

<!-- origen: CONTACT-RULES.md, enmiendas 1 y 2, y NAME.md y TITLE.md -->
Two further rules predate the work but were exercised by it: contact with the
source of the data is read only and at a fixed tag, and the name of anything
that leaves this work passes a term check before it is frozen. The repository
name and the title of this paper each have their own record of that check, with
the queries declared before running and the limits of the check declared after.

## 9.4 What a third party can verify today

<!-- origen: los ficheros de reproduccion de cada informe; el repositorio es
     publico -->
Clone the repository and run the programs. Every figure in this paper comes from
a results file in it, every results file is produced by a program in it, and
every program is deterministic: the only source of randomness is a seed that is
frozen in the source and declared in the reports. The declarations that were made
before each measurement are separate commits, earlier in the history than the
measurements they govern, and that ordering is checkable without trusting anyone.

<!-- origen: PRIOR-ART.md, doctrina y cierre; NOVELTY.md -->
What a third party cannot verify by running anything is the literature review,
which is a matter of what was read. That is why it carries its own doctrine,
verdicts only from artefacts actually read, second hand marked as second hand
with its chain of citation, and every figure with a pointer or returned; why the
intersections found are recorded next to the results they touch rather than in a
closing note; and why the single novelty declaration is a signed file with its
scope stated as relative to a review whose limits are written down.
