---
title: "Formal prior art — Alexandrov/Minkowski, Aristotle's error, Matsumoto's theorem"
date: 24 November 2026
---

**Question.** For three of DICTO's new Lean formalisations: did anyone check these results by machine before us (Lean 3/4 and Mathlib with its PRs and Zulip archive, Isabelle AFP, Coq/Rocq, HOL Light/HOL4, Mizar, Metamath)? And which papers should we cite for the hand proofs?

**Conclusion in one line.** (1) Alexandrov and Minkowski: we found no earlier formal proof. (2) Aristotle's error: we found no earlier formal proof. (3) Matsumoto's theorem: **there is an earlier formal proof.** Sylvestre's Isabelle AFP entry *Buildings* (2016) proves it for every Coxeter system, and a Lean master's thesis (Álvarez Sánchez, Bonn 2024) proves it under extra assumptions. Neither Mathlib nor anyone else has it in full in Lean. We must cite both and present ours as the first Lean proof (state its scope exactly).

This search does not repeat `studies/2026-11-24-questions-answered` (§1c and §2 there). That study already covered Niven in Mathlib, tiling proofs in general, and the first pass on Aristotle's error. Here we add the targeted checks.

# 1. Alexandrov's theorem on prescribed curvature; Minkowski's theorem for polytopes

**Sources checked.**

- Web searches on Alexandrov / prescribed curvature / Minkowski problem together with Lean, Isabelle, Coq, "formalized" and "proof assistant": no formal work was found. The results were all papers on the mathematics: Bobenko–Izmestiev; Kane–Price–Demaine; arXiv 1712.00825 (reconstruction from normals and areas); arXiv 1101.0823.
- Lean Zulip archive, "Is there code for X?" → *Main Theorem of Polytope Theory* (<https://leanprover-community.github.io/archive/stream/217875-Is-there-code-for-X%3F/topic/Main.20Theorem.20of.20Polytope.20Theory.html>). This thread covers V/H-polytopes only (a dissertation by V. Hernández, supervised by L. Theran). The maths thread *Sofa problem may have been solved* lists Brunn–Minkowski theory, mixed volumes, surface area measure and Alexandrov–Fenchel only as a **wish list** (<https://leanprover-community.github.io/archive/stream/116395-maths/topic/Sofa.20problem.20may.20have.20been.20solved.html>). The *convex polytopes* thread holds no Minkowski or Alexandrov result.
- Isabelle: HOL-Analysis `Polytope.thy` (faces, extreme points, polytopes; Krein–Milman–Minkowski, ported from HOL Light by Paulson; <https://isabelle.in.tum.de/repos/isabelle/file/default/src/HOL/Analysis/Polytope.thy>). AFP *Euler's Polyhedron Formula* (Paulson). Neither covers prescribed facet areas or curvature. We found no AFP entry on Minkowski–Weyl, discrete Gauss–Bonnet or discrete curvature.
- Coq/Rocq: Coq-Polyhedra (Allamigeon–Katz; simplex method, face lattice, Balinski; arXiv 1706.10269, LMCS). It has no Minkowski or Alexandrov theorem.
- HOL Light: polytope library (source of the Isabelle port) only.
- Mizar and Metamath: no hit in web search.

**Finding.** **No earlier formal proof found to our search** of either Alexandrov's curvature theorem or Minkowski's theorem for polytopes, in any system. The nearest formal work is basic polytope theory: faces, Euler's formula and Krein–Milman in Isabelle/HOL Light, and Coq-Polyhedra.

**Recommended citations for the hand proofs.**

- A. D. Alexandrov, *Convex Polyhedra*, Springer 2005 (English translation of the 1950 Russian book). Chapters on prescribed curvature and on Minkowski-type theorems; chapter numbers to be checked against the library copy.
- V. Oliker, "Embedding Sⁿ into Rⁿ⁺¹ with given integral Gauss curvature and optimal mass transport on Sⁿ", *Adv. Math.* 213 (2007) 600–620, arXiv math/0701398. This is the variational proof we follow.
- J. Bertrand, "Prescription of Gauss curvature using optimal mass transport", *Geom. Dedicata* 183 (2016) 81–99, arXiv 1505.04821 (<https://arxiv.org/abs/1505.04821>). This is the clean polyhedral and optimal-transport version.
- H. Minkowski, "Allgemeine Lehrsätze über die konvexen Polyeder", *Nachr. Ges. Wiss. Göttingen* (1897) 198–219. Uniqueness via Brunn–Minkowski / Alexandrov's lemma. A modern proof: D. Klain, "The Minkowski problem for polytopes", *Adv. Math.* 185 (2004) 270–288. Overview: <https://en.wikipedia.org/wiki/Minkowski_problem_for_polytopes>.

# 2. Aristotle's error: regular tetrahedra do not tile space

**Sources checked.** These add to the earlier study, which found no formal proof in Lean, Isabelle, Coq or HOL.

- Web search for formal proofs of tetrahedra non-tiling (Lean, Isabelle, arccos(1/3)): nothing formal. The results were expository: the dihedral angle arccos(1/3) ≈ 70.53° lies strictly between 360°/6 and 360°/5. History notes (UC Riverside, <https://math.ucr.edu/~res/math153/s05/history08b.pdf>) credit **Regiomontanus** with the refutation and Maurolico with computing the angle.
- *Formalizing 100 Theorems* (<https://www.cs.ru.nl/~freek/100/>), #50 "The Number of Platonic Solids": formalised in Lean (D. Cappello), HOL Light (J. Harrison) and Isabelle (E. Finken). This **classifies** the five solids. It is **not** a tiling result, but cite it as the nearest formal neighbour.
- Mathlib: `Mathlib.NumberTheory.Niven` (already noted in the earlier study). We found no tiling-by-polytopes development.
- Flyspeck (HOL Light, Kepler conjecture): it handles tetrahedra and dihedral angles inside the packing proof. It does not state that regular tetrahedra fail to tile.

**Finding.** **No earlier formal proof found to our search** that regular tetrahedra fail to tile space, nor of any Platonic non-tiling result proved through dihedral angles.

**Recommended citations.**

- J. C. Lagarias, C. Zong, "Mysteries in packing regular tetrahedra", *Notices AMS* 59 (2012) 1540–1549, DOI 10.1090/noti918. This is the history (Aristotle, *De Caelo* III.8; the refutation).
- Aristotle, *De Caelo* III.8 (the claim).
- I. Niven, *Irrational Numbers*, Carus Math. Monographs 11 (1956), for the angle step (Mathlib `niven`). The Mathlib theorem is credited at its point of use.
- Optional, for the other Platonic angles: Conway–Radin–Sadun, *Discrete Comput. Geom.* 22 (1999) 321–332 (already cited in the earlier study).

# 3. Matsumoto's theorem (Tits' word problem) for Coxeter groups

**Sources checked.**

- Mathlib `Mathlib/GroupTheory/Coxeter/Basic.lean`, current master. The TODO list still reads "State and prove Matsumoto's theorem" and "Classify the finite Coxeter groups" (<https://leanprover-community.github.io/mathlib4_docs/Mathlib/GroupTheory/Coxeter/Basic.html>). `Coxeter/Matrix.lean` defines the Coxeter matrices Aₙ, Bₙ, Dₙ, I₂(m), E₆–E₈, F₄, G₂, **H₃**, H₄ only as matrices. It proves no facts specific to those groups.
- Lean Zulip archive, *Progress on Coxeter groups* (<https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Progress.20on.20Coxeter.20groups.html>). Mitchell Lee (2024; PRs #11406, #11465, #11466, #11526) supplied the length function, reflections and the geometric representation. The work was "set up with a view toward Matsumoto's theorem", but as of Dec 2024 the project was "not actively being worked on". Also read: *Rewriting vs. lifting* (maths stream; Lee's reformulation).
- **Isabelle AFP, *Chamber Complexes, Coxeter Systems, and Buildings*, J. Sylvestre, 1 July 2016** (<https://isa-afp.org/entries/Buildings.html>; theory `Coxeter`, <https://isa-afp.org/browser_info/current/AFP/Buildings/Coxeter.html>). It proves `reduced_word_problem`: if w ≠ 1 and ss, ts are reduced words for w, then a chain of `flip_altsublist_adjacent` steps joins them. Each step replaces an alternating half-relator subword (s t s …, length m(s,t)) by (t s t …), so each step is a braid move. The proof is stated in the locale `PreCoxeterSystemWithDeletion`, and `sublocale CoxeterSystem < PreCoxeterSystemWithDeletion` gives it to **every Coxeter system**. **This is Matsumoto's theorem (reduced-word part), machine-checked in 2016.** The entry also builds Coxeter complexes as chamber complexes, then buildings. We read the theory file directly (lines on the word problem, the deletion condition and the sublocale).
- **Lean thesis: Ó. Álvarez Sánchez, *Demazure operators and Lean*, Master's thesis, Univ. Bonn, 25 Oct 2024** (advisors C. Stroppel, J. Flake; <https://florisvandoorn.com/theses/OscarAlvarez.pdf>). §4.8 proves `matsumoto_reduced`: reduced words with equal products are joined by braid moves. It assumes the class `MatsumotoCondition`: every m(i,j) ≥ 1, and (sᵢsⱼ)ᵖ ≠ 1 for 0 < p < m(i,j). The thesis notes that the second fact holds in all Coxeter groups but was not proved there. It targets Sₙ₊₁ (type A). Code is on GitHub (reference [Ála] in the thesis).
- Other Lean projects: gitee `hoxide/coxeter4` (Lean 4; aims at the strong exchange property; last updated Nov 2024; no Matsumoto seen). A Coxeter / Hecke / Kazhdan–Lusztig Lean project (majiajun.org) is cited in arXiv 2611.09787; we could not open its page, so its status is not checked. arXiv 2603.00896 notes that Mathlib had built no non-trivial `CoxeterSystem` term when it was written.
- Coq/Rocq, HOL Light/HOL4, Mizar, Metamath: web searches found no Coxeter word-problem development.
- A3/B3/H3 with permutahedra or Coxeter complexes: we found **no formal treatment** of these particular finite groups, of their permutahedra (Cayley graphs as polytopes) or of their concrete Coxeter complexes. The nearest are the Mathlib matrices (no group facts) and AFP *Buildings* (abstract Coxeter complex, no examples). §2 of the earlier study already lists "Platonic solids count" as formalised.

**Finding.** **There is an earlier formal proof.**
(a) Sylvestre, Isabelle AFP 2016: Matsumoto's theorem (the reduced-word statement) for every Coxeter system.
(b) Álvarez Sánchez, Lean 4 thesis 2024: the same statement under the `MatsumotoCondition` assumptions, applied to type A.
Mathlib has neither (still a TODO). Our claim must be worded accordingly. If our proof is for all Coxeter systems and has no extra assumptions, it is the first **complete Lean** proof to our search, not the first formal proof. If it covers only A3/B3/H3 (finite, decided by computation), say that, and claim novelty only for the concrete groups with their permutahedra and Coxeter complexes. For those we found no earlier formal work.

**Recommended citations for the hand proofs.**

- H. Matsumoto, "Générateurs et relations des groupes de Weyl généralisés", *C. R. Acad. Sci. Paris* 258 (1964) 3419–3422.
- J. Tits, "Le problème des mots dans les groupes de Coxeter", *Symposia Mathematica* 1 (1969) 175–185.
- P. Abramenko, K. S. Brown, *Buildings: Theory and Applications*, GTM 248, Springer 2008 (the proof followed in the Álvarez thesis, cited there as [AB05]; theorem number to be checked). Also: A. Björner, F. Brenti, *Combinatorics of Coxeter Groups*, GTM 231 (2005), Thm. 3.3.1. J. E. Humphreys, *Reflection Groups and Coxeter Groups* (1990), for A3/B3/H3.
- Formal: J. Sylvestre, "Chamber Complexes, Coxeter Systems, and Buildings", *Archive of Formal Proofs*, July 2016. Ó. Álvarez Sánchez, *Demazure operators and Lean*, MSc thesis, Bonn 2024. Mathlib `GroupTheory.Coxeter` (N. Jensen, M. Lee) as the base we build on, credited at point of use.

# Summary table

| Work | Earlier formal proof? | Cite (hand proof) | Cite (formal) |
|---|---|---|---|
| Alexandrov curvature + Minkowski | **None found to our search** | Alexandrov 1950/2005; Oliker 2007; Bertrand 2016; Minkowski 1897; Klain 2004 | none (Isabelle Polytope.thy / Coq-Polyhedra only as background) |
| Aristotle's error (tetrahedra) | **None found to our search** | Lagarias–Zong 2012; Aristotle; Niven 1956 | Mathlib `niven`; "Number of Platonic Solids" (Lean/HOL Light/Isabelle) as nearest neighbour |
| Matsumoto's theorem | **Yes: Isabelle AFP *Buildings* (Sylvestre 2016), all Coxeter systems; Lean thesis (Álvarez Sánchez 2024), under extra assumptions** | Matsumoto 1964; Tits 1969; Abramenko–Brown 2008 | Sylvestre 2016; Álvarez Sánchez 2024; Mathlib TODO |
| A3/B3/H3 + permutahedra / Coxeter complexes | **None found to our search** | Humphreys 1990; Björner–Brenti 2005 | Mathlib `CoxeterMatrix.H₃` etc. (definitions only) |

# Sources checked (complete list)

Web searches (10 query groups). Pages read in text: Mathlib `Coxeter/Basic` docs and `Coxeter/Matrix.lean` source; Lean Zulip *Progress on Coxeter groups*; AFP *Buildings* theory `Coxeter` (full text, by grep); Álvarez Sánchez thesis (contents, §4.8). Results seen only as snippets: Formalizing 100 Theorems (#50); Zulip *Main Theorem of Polytope Theory*, *Sofa problem*, *convex polytopes*, *Rewriting vs. lifting*; Isabelle `Polytope.thy`; AFP *Euler's Polyhedron Formula*; Coq-Polyhedra (arXiv 1706.10269); gitee `hoxide/coxeter4`; arXiv 2611.09787, 2603.00896, 1505.04821, math/0701398, 1712.00825, 1101.0823; UC Riverside history notes. Not reachable or not checked: the majiajun.org Lean Coxeter/Hecke project page; Mizar and Metamath indexes (web search only); Alexandrov chapter numbers (to check against the library copy).
