# Palomar score estimate: the octahedral constant 3 (#43 Theorem 4) (15 November 2026)

**Conclusion. Notability 2 out of 5. That is below Palomar's floor of 4, so the outcome would be `rejected`.** Every other dimension reaches 4 or more:
- classification 5;
- clarity 4, provenance 5;
- statement alignment 4;
- definition fidelity 5, auditability 5 (trust high);
- literature 4;
- proof alignment 5.

**Do not submit this entry.** The score is an estimate (see Method), but it agrees with the estimate made before packaging (LITERATURE.md of study 2026-11-14-lean-loop-equality: "2 out of 5, 3 at best"), and no reading of the rubric puts it at 4.

**Status:** estimate only. The production reviewer could not be run. Nothing was submitted.

## Method

Palomar's production reviewer (`palomar-review`, PalomarReviewer @ ba9b26c, model `codex:gpt-6-sol`) reads private submission state through Palomar's credentials and broker, so it cannot be run here. As for the first entry:

1. **Blind replay.** A fresh Claude agent (Opus 5.5) was given only the pinned policy (PalomarPolicy @ 28bd48b: CONTRIBUTING.md, rubric.json, prompts 00–06, materiality.md, schemas, taxonomies) and the package (Challenge, Solution, proof library, comparator.json, formalization.yaml, README). It was not given our literature notes or our estimate. It ran the seven steps, searched the web on its own, and returned each step's JSON (`replay-review.json`).
2. **Own reading** of the rubric, point by point (below).

The replay is a different model from production, run outside the broker; Palomar's own audit found that model tiers disagree on outcome in 2–3 of 5 cases, and the policy notes one point of run-to-run noise per dimension. Here the margin is two points on notability, so the outcome is not in doubt.

## Replay result, step by step

| Step | Outcome | Scores |
|---|---|---|
| classification | neutral | classification 5 (math.MG; 52B15, 52A40, 52B11 all fit) |
| metadata | neutral | clarity 4, provenance 5 |
| statement alignment | neutral | 4 (all four theorems match; not vacuous; c ≥ 0 and the frame disclosed) |
| definition fidelity | neutral | definition fidelity 5, auditability 5, trust high (Mathlib-only Challenge) |
| **literature and notability** | **failure** | **notability 2**, literature 4 |
| proof account | neutral | proof alignment 5 |
| synthesis | **rejected** | scores copied from the steps |

### The reviewer's reasons for notability 2

- The covering lemma is the known diameter of S²/O (Dunbar–Greenwald–McGowan–Searle 2009, Table 2; the reviewer checked the table itself).
- The containment follows from it by two uses of the covering lemma and separation, as the package itself says; the cube's sharpness is one line.
- The foot-point hull P(S) has no research literature the reviewer could find, and the only source is an unrefereed preprint, so neither paper-worthiness nor a research audience is established. It chose 2 ("routine") over 3 ("not established"); both fail the floor.
- What would be needed is "mathematics beyond what is selected (for example a general-group or higher-dimensional theory with independent reception)".

### Literature 4

All citations check out, and no novelty or priority is overclaimed. Not 5 because the containment's only source is the author's own preprint. No omitted prior result was found.

### Minor points (private notes, not findings)

1. "Equivalent to the known diameter" was loose: the lemma is the upper bound, and the value is attained. **Fixed** in README and formalization.yaml (package commit d65b977; text only, metadata validator re-run).
2. The Challenge's module docstring repeats the paper's "sharp (cube, octahedron)", while only the cube is formalised; the scope section says so. Left as is.

## Own reading, point by point

- **Classification 5, metadata 4/5, alignment 4, fidelity 5, proof account 5.** Agreed. The Challenge is 89 lines of Mathlib-only Lean with a docstring on every definition; the divergences (standard frame, half-space family, c ≥ 0, unused hᵢ > 0) are all listed.
- **Literature 4.** Agreed. The known part (orbit-space diameter; spherical 3-designs) is credited at the point of use, in the Challenge docstring and in the sources.
- **Notability 2.** Agreed, and on the evidence 2 is the more accurate anchor, not 3:
  - What is new is the statement for foot-point hulls (DICTO's construction) and its sharp constant. We did not find it stated elsewhere.
  - But given the known diameter, the proof is half a page, and the result has one group and one dimension. An editor would see an exercise, not a note.
  - The research audience for foot-point hulls is not yet there: #43 is the only place they are studied as a family (the Smarandache face pedal polyhedron is posed as a problem, not studied).
  - The Lean proof, however clean, does not count (prompt 04: "Formal verification, effort, length, and polish do not by themselves establish research interest").

**Honest outcome: rejected, notability 2.** This is lower than the Loop Equality entry (3).

## What would raise notability to 4 (new mathematics, not better prose)

In order of best chance:

1. **The constant for every finite group, in dimensions 3 and 4, with sharpness.** Define t(G) as the supremum of t_min(S) = min{t : S ⊆ t·P(S)} over G-invariant polytopes. The formal proof already shows, almost word for word in any dimension, that t(G) ≤ sec²ρ(G), where ρ(G) is the diameter of S^{d−1}/G (the covering angle of the worst orbit); for reducible G no constant exists. The real content is **sharpness, or the exact gap**: for which G is t(G) = sec²ρ(G), which polytopes attain it, and what is t(G) when it is not attained. In dimension 3 this covers T, T_d, T_h, O, O_h, I, I_h (#43 already has 9, 3, 3, 15 − 6√5). In dimension 4, the diameters of quotients S³/G are the subject of Dunbar–Greenwald–McGowan–Searle and the works they cite (which groups they cover was not checked here), so upper bounds are partly at hand, and the sharpness question for the 4D symmetry groups (A₄, B₄, D₄, F₄, H₄ and their rotation and chiral subgroups; the 24-cell and 600-cell) is open as far as we know. A complete table with proofs of attainment would be a short paper with a definite audience (symmetric convex bodies, orbit polytopes, John-type positions).
2. **Equality and stability.** Prove that t_min(S) = 3 for an octahedrally symmetric S only for the cube and the octahedron (and say exactly which polytopes reach 9 and 15 − 6√5), and give a stability version: t_min(S) ≥ 3 − ε forces S to be close to a cube or an octahedron. Rigidity results of this kind are what turns a constant into a theorem people cite.
3. **Beyond polytopes.** Extend to all convex bodies containing O, with P(S) the closed hull of the pedal points of all supporting planes, and relate it to the classical pedal surface; then the constants become statements about pedal bodies, an old object with a literature.
4. **Outside evidence.** Peer review of #43, or use of the foot-point hull by others. On its own this would not lift a two-line corollary, but it would support items 1–3.

Formalising Theorem 2 (the icosahedral constant) or Corollary 7 in the same entry would not help: the reviewer would group them as further corollaries of known orbit-space diameters.

## Recommendation

Keep the package local; it is ready and mechanically green. Do not submit it as it stands. Item 1 is the route with the best chance; if it is proved, the entry should be rebuilt around the general theorem, with Theorem 4 as one row of the table.
