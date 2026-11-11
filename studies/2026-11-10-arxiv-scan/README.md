# arXiv scan for the open gaps (DICTO 10 Nov 2026: "a quick scan may be worth identifying anything useful for closing our gaps")
Quick scan, Aug–Nov 2026 (agent report, judged here). [R] abstract read, [L] listing only.

| gap | item | use for us | action |
|---|---|---|---|
| threshold proof (certified) | Park, Topological transition sets for line-line-circle trisectors, arXiv 2603.29540 [R] | walls from discriminants + one certified point per chamber + constancy between walls: the shape of our proof, without box enclosures | adopt the method: compute the wall of the threshold triple exactly, certify the other walls do not enter the region |
| | K. Lee, certified homotopy with interval arithmetic (ICMS 2026 talk, Julia) [R] | track the 27 lines along certified paths instead of boxes | keep as plan B |
| one piece (aim 3) | Kamenetsky, Towards strongly aperiodic monotiles in higher dimensions, arXiv 2610.00916 [R]; Goodman-Strauss, Notes on a strongly aperiodic monotile in E^3, arXiv 2609.24779 [R]; Flicker 2609.23783 v2 [R] | frame-marking: matching rules generated from the substitution, a finite search: reusable for markings on RD / TRD / Narcissus pieces | read Kamenetsky in full before the Chair44 regrouping step; credit |
| laws (aim 2) | Mazzucchelli & Raman, Canonical forms as dual volumes, arXiv 2509.02239 (v2 1 Nov 2026) [R] | canonical form = Laplace transform on the dual: direct tool (and PRIOR ART) for "canonical form = volume of the polar" | credit in every laws text; use for the C–O line |
| | Winter, Mahler volume and flag number, arXiv 2610.09990 [R]; Chen–Li–Xi–Xu, Mahler conjecture in 3D, arXiv 2605.09334 [R, unrefereed] | bounds and a one-parameter 'shadow flow' for volume × polar volume | cite beside our Mahler sweeps |
| #43 OG hop orbit | Demyanov–Ryabova iterated dualisation conjecture, arXiv 1702.00168 [L]; Schreiber–Veselov–Ward 'Buffon transformation', arXiv 1402.5354 [L] | PRIOR ART for iterating dual/polar operations on polytopes | read both before any #43 novelty claim |
| Sri Yantra, approximant lines, close packing on surfaces | nothing new in the window | | |

Sources checked: the agent's 13 web queries and 8 arXiv abstract pages (2610.00916, 2609.24779, 2609.23783, 2509.02239, 2603.29540,
2508.04275, 2610.09990, 2605.09334), icms-conference.org/2026/abstracts/Lee.txt, arXiv API query "Sri Yantra"/"yantra".

## Read for #43 (10 Nov 2026, DICTO: "yes start with the reading")
**Demyanov–Ryabova (Daniilidis & Petitjean, arXiv 1702.00168, v2 Sep 2017; full text read, §1).** The operation F acts on a
finite FAMILY of polytopes: for each direction d, Ω(d) = conv of the d-active extreme points of all members; F(ℜ) = {Ω(d)}.
F never creates new extreme points, so the sequence is finite and must cycle; the conjecture is that the cycle has length 1 or 2
(proved in 1D, under affine independence (their ref. [7]), and under 'enough well-placed minimal polytopes'). VERDICT: a different
process (families, no new corners, finite cycles) from DICTO's hop (one solid, antipol then polar, new corners every step,
conjectured convergence to the sphere). Not prior art for #43; no tool for its Decay Lemma.
**Buffon transformation (Schreiber, Veselov, Ward, arXiv 1402.5354, 2014; text read).** Linear: on a simplicial polyhedron with
FIXED combinatorics each vertex is replaced by an average (centroids of the faces round it); the limit shape comes from the
subdominant eigenspace of the Buffon operator (subspace iteration); the main theorem is the existence of star-shaped 'affine
B-regular' polyhedra (Colin de Verdière, Lovász). VERDICT: different (linear, fixed vertex count, limit affine-regular, not the
sphere). Not prior art for #43. Possible borrowing only for a linearised local model near the sphere (spectral gap = contraction).

## Forward citations + Bridges (10 Nov 2026, DICTO: "yes run it")
- Tsiokos (Chair44) is cited by Flicker 2609.23783, Goodman-Strauss 2609.24779, Kamenetsky 2610.00916 (all in the library, gaps/),
  and Hartshorn & Romanov, "The Internal Space and Boundary Growth of the Spectre and Tsiokos's Chair44 Tilings" (Research Square,
  no DOI found) [L]. None treats fcc/hcp or c/h stacking.
- Śrī Yantra: no outside work since mid-2025 on exact geometry. TO READ BEFORE ANY FURTHER #103 CLAIM: G. D. Chapati & R. Chapati,
  "Verified Reconstruction of the Śrī Yantra: Constraint Solving, Feasibility Prediction and Spectral Analysis", Zenodo 2026,
  doi 10.5281/zenodo.23188649 [L] (not a citer of Chiodo in OpenAlex; a direct neighbour).
- Approximants (citers of Baake–Grimm since 6/2025) [L]: Davies & Thalhammer (Proc. R. Soc. A 2025, supercell vs superspace
  convergence); Band, Beckus & Pogorzelski (J. Anal. Math. 2026, spectral approximation of substitution systems); Jagannathan (PRB 2026,
  metallic-mean quasicrystals); Say-awen & Coates (Acta Cryst. A 2026, octagonal tilings, three prototiles). Leads for aim 1.
- Goldberg: no citers since mid-2025 (latest Ebert, Kim & Akleman, CAD 2024).
- Bridges 2019–2026: nothing on yantras, RD/golden-rhombohedra sculpture or space-fillers in art; nearest: Djang 2025 (icosahedral
  quasicrystal paper-strip spheres), Moradzadeh & Nejad Ebrahimi 2020 (3D aperiodic girih), Jowers & Moat 2025, Kaplan 2024.
Sources checked: the agent's OpenAlex and Semantic Scholar queries (cites: filters for Chiodo, Tsiokos, Baake–Grimm, Goldberg works)
and the Bridges archive search plus year indexes 2019–2026.

## Chapati & Chapati 2026 read (10 Nov 2026) — CREDIT NEEDED in #103
G. D. Chapati, R. Chapati, "Verified Reconstruction of the Śrī Yantra: Constraint Solving, Feasibility Prediction and Spectral
Analysis", Zenodo dataset v1.0, 6 Oct 2026, doi 10.5281/zenodo.23188650 (concept 23188649); 45-page report read (§1–2, closing gate).
- Numerical reconstruction of Huet's construction (residual 1.9e-14, triple points 2.1e-15); states "no closed-form solution".
  → #103's exact results (Thms 1, 2, 9, 10, certificates) go beyond it; not prior art for them.
- 43 rule (their §2.1): the 43 = star points, one per convex vertex of each āvaraṇa circuit outline (8, 10, 10, 14) + trikoṇa 1;
  each tip caps one chamber (by the outline's directions at the tip); verified at four parameter points; Huet's arrangement has
  74 regions (50 triangles, 24 trapezoids). → DIFFERENT rule from #103 Prop. 3 (odd regions, parity), SAME circuits and counts
  (14, 10, 10, 8, 1). Prop. 3's parity statement remains new as stated; the circuit counts and a computed enumeration of the 43
  appeared first in Chapati (6 Oct 2026): credit both (rule: independent ideas count).
- Feasibility sampling of the four-parameter family (4.3–55 % valid by sampling width; 5,000-instance benchmark) → cite beside
  #103's open 'admissible region'.
Action: #103 credit sentence + sources-checked entry (DICTO to choose: Version 4 now, or with the next real version).

## Read for the one-piece aim (12 Nov 2026, DICTO: "read kamenetsky in full while it runs")
**Kamenetsky, "Towards Strongly Aperiodic Monotiles in Higher Dimensions", arXiv 2610.00916v1 (1 Oct 2026; full text read; AI-written on
Arena.ai, human-verified; code github.com/dimkadimon/Monotile-RN).** What it gives:
- Frame marking: the tile's marking IS its orientation frame (24 proper rotations for the 3D chair); the matching rule is not guessed but
  generated by the substitution (all contacts that occur inside supertiles at every level). The only free choice is the orientation of
  each child in the supertile, a finite list.
- A finite certificate (C1 the rule reproduces itself one level up; C2 it can be checked face by face; C3 every live one-shell
  neighbourhood forces one complete supertile) => every lattice-registered tiling is uniquely hierarchical, hence strongly aperiodic.
  3D: reproduces Chair44's numbers 2388 -> 44 -> 30, 33 -> 15, in about 2 s, without using the published rules.
- Theorem B: of the 2187 chiral child-orientation choices exactly one (up to relabelling axes) works: the 3D marking is FORCED.
- 4D chair: every symmetric family tested fails (C1); Problem 9.1 (a finite search) open.
- Assumptions: lattice registration (all tiles on one cubic lattice) and the central child a plain translate. Dropping lattice
  registration is their future-work item 2.
VERDICT for aim 1 (one RD/TRD piece forcing a non-repeating c/h stacking):
1. Capacity, made exact: a frame marking can carry only as many states as the piece has orientations at a site. Chair: 24.
   Narcissus: 3 proper (6 with mirrors). RD: 24 proper. This is the wall behind every Narcissus failure (edge keys 6 Nov, ABC wave
   9 Nov, vertical-plane wave 12 Nov): Narcissus is the right shape for the stacking but has the chair's capacity divided by 8.
2. The method needs a self-similar (rep-tile) substitution. RD, TRD and Narcissus are not rep-tiles, so the tool cannot be applied to
   them directly; it applies to a substitution whose cells are then shared out to RDs (the 11-09 bridge).
3. Isometric bridge (no shear needed): scale the chair so each unit cube is the conventional fcc cube (side 2). The chair's 24 proper
   rotations about a lattice point are symmetries of fcc, so a Chair44 tiling labels every RD of the fcc tiling (4 sites per cube, 28
   per chair) with a frame + position. Open: how many distinct marked RDs that needs (naive 28 positions) and whether neighbours can
   read the position so that frames alone suffice. This is the concrete next step for the bridge; cost: rerun their 2 s certificate as
   the control first.
4. The c/h aim breaks their lattice registration on purpose (hcp sites are not one lattice): it sits exactly on their open item 2.
Credit: any use of the frame formalism or certificate is Kamenetsky's (and the mechanism Tsiokos's).
