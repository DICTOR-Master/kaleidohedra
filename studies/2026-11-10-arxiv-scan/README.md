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
