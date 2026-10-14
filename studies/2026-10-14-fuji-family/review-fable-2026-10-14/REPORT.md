# Review: "The FUJI Family: Pyramids on Flat-Ended Triangles" (draft of 14 October 2026)

Reviewer: Fable (Claude), read-only review for DICTO, 2026-10-14. All the work under review is DICTO's. Each check script in this
folder builds its shapes from coordinates and does not import the study's own scripts. (Saved here by the main session; the reviewer
could not write files. The review predates the golden-and-silver remark and Figure 5.)

Check scripts and raw output: `check_core.py/.out` (family formulas, antiprisms, face-plane members, Odom, k-family limits),
`check_spheres.py/.out` (dictosphere, CLEO sphere, Icosahedral Cleo, wheel counting), `check_octagonal_wheels.py/.out` (five
octagonal wheels?), `check_corner_fuji.py/.out` (the cube-corner explanation in Insight A).

## 1. Verdict

The mathematics that carries the paper is right. Re-derived from coordinates and agreeing to machine precision: the base-angle
formulas, the height, the volume, the antiprism dihedral and r = 2cos(π/n) − 1, the face-plane members, Odom's hexagon, the
dictosphere's equal-depth solid and its spherical Voronoi version, and the CLEO-sphere volumes.

Weak points: one false sentence in §5.6; several claims stated more strongly than shown ("four is the most", "for every r", "Twenty
Icosahedral Cleo fill an icosahedron exactly", the "theorem" label, "every member is an Odom hexagon"); selective use of the
dictosphere measurements; prior-art wording that reads as a discovery claim where it only reports a search that found nothing. All
fixable in the text; none breaks the family. Two results would strengthen it: why the dictosphere's r equals the cuboctahedral member
(Insight A), and a proof of the breathing tiling for every r (Insight D).

## 2. Cracks, ranked by severity

**2.1 §5.6, last paragraph: false as written (high).** "no combination of 72° and 69.09° completes to 360°", but 5 × 72° = 360°.
True statement: a·72° + b·69.09° + c·180° ≠ 360° when b ≥ 1 (searched small a, b, c: none). Conclusion stands. Fix: "...and no
combination that includes a base edge (69.09°), with 72° angles and flat 180° faces, makes 360°."

**2.2 §5.6: "Twenty Icosahedral Cleo fill an icosahedron exactly" (high, credibility).** The Icosahedral Cleo is the icosahedron's
central pyramid on one face; every polyhedron splits into such pyramids. The cut across the outer tips removes part of every CLEO and
Penta-cleo (CLEO's outer corners at radius 1; the face plane is 0.676 from the centre). Fix: keep as a picture of the route; say it is
the icosahedron's central pyramid (side 0.851, base 2/√5) cut from CLEO + 3 Penta-cleo; drop the bold "exactly".

**2.3 §5.5: "Four is the most" (medium-high).** False as worded: any number of planes through one line meet along a spoke. True
version: wheels meeting along different spokes; a wheel with 2m spokes has m spoke lines, so n − 1 ≤ m: at most 4 hexagonal, 6
decagonal. Equality puts every spoke line in exactly two wheels. Fix: state the condition, give the proof, prove or soften "only".

**2.4 §5.3: "fills space exactly for every r" (medium).** Checked at r = 0.2, 0.382, 0.5, 0.618, 0.8, 1 only. Proof options: Wythoff
(Insight D); or corners are affine in r, so cell volumes are polynomials of degree ≤ 3 and equality at 6 values proves it. Fix: add
an argument or say "checked for r = ...".

**2.5 §5.4: dictosphere evidence firmer than the data (medium).** "About 4 cm" and "about 1.5 cm" (±0.25) allow r = 0.29–0.47, so
cannot separate 0.356, 0.366, 0.375. Left out: sphere ~7.5 cm vs 8.8 cm model; port gaps 3 / 4 cm vs model 2.41 / 3.91 cm along the
surface (2.08 / 3.22 straight), triangle gap ~20% off; "holes 1.46 vs 3 cm" unresolved. Squares are not bigger than triangles in the
model (1.072 vs 1.206 at inradius 1; 16 vs 18.3 cm² with measured sides). Fix: "the even-margin rule predicts 0.356 (sphere) and
0.366 (flat); hand measurement gives about 0.375 ± 0.1, consistent"; mention the port-gap mismatch or re-measure with callipers.

**2.6 §4, §6: "antiprism theorem" novelty (medium).** Standard dihedral formula (OEIS) composed with the base-angle formula; new
content is one line of algebra. Proof correct (n = 3–12 to 10⁻¹²). Fix: call it a Proposition/Corollary; say the dihedral is standard.

**2.7 §4: face-plane condition not defined precisely (medium-low).** Antiprisms have triangle–triangle and triangle–n-gon edges; only
the first is meant; for the cuboctahedron the base continues a square. Fix: define once ("glued by an equilateral face to a unit
triangle of X, base continues the plane of X's face across that edge: L + D = 180°"), name the edge type per table row; same in
PROOFS.md §2.

**2.8 §3 and abstract: "every member's base is an Odom hexagon" (medium-low).** A reparametrisation (r = e/(1 + e)), missing r = 1.
Odom's contribution is the golden case; the usually cited Odom construction is a different one (Amer. Math. Monthly E3007, 1983).
Check the Wolfram Demonstration's author and credit precisely. Fix: "Odom's golden hexagon is FUJI's base; the same construction with
extension e gives every member with r < 1."

**2.9 §6: prior-art wording (medium-low).** Alternating-bond hexagons in breathing kagome lattices are standard; base-angle formulas are
elementary. New: the pyramid family as an object, Insight A, the FUJI and Lotus-seed results. Fix: keep "we did not find", state the
search scope (where, terms, date); present identifications as synthesis.

**2.10 §1: logo r ≈ 0.79, ring r ≈ 0.48 (low).** No script/data/image in the study; README's first ring estimate was r ≈ 0.1; rounded
triangles are not flat-ended, so the fit rule decides. Fix: add the measurement or drop the numbers.

**2.11 Smaller points (low).** §5.4 "same face angles" should be dihedral angles. Figure 7a (now 8a) caption says FUJI's triangles,
but any r > 0 works; say which r is drawn. "29%": 28.6%. §2 table: footnote that the r = 0 short-side angle is undefined (formula
gives 54.74°). References [2], Papadopolos–Ogievetsky and Koca et al. not cited in the text. Ba₃Yb₂Zn₅O₁₁ (README only): keep out until
checked; primary source K. Kimura, S. Nakatsuji, T. Kimura, PRB 90, 060414(R) (2014), arXiv:1404.6439; self-test: small + large Yb–Yb
distances = a/√2. `great-dodeca-cut.json`: "8 cells, 7 corners" and "12 cells, 4 corners" (same volume 0.022776) are 20 congruent cells;
merge near-duplicate corners before quoting counts (volumes sum to the icosahedron, 1.56109).

## 3. Confirmed (re-derived independently)

- Family formulas at r = 0, 1/4, 1/2, 1/φ, (√3−1)/2, 0.8, 0.99: base concyclic, radius² (1 + r + r²)/3; h² = (2 − r − r²)/3;
  cos L = (1 + 2r)/3; cos² S = (2 + r)/(3(2 − r)); volume (√3/12)(1 + 4r + r²)h. Every table value matches.
- Cuboctahedral member: height exactly 1/√2, L = 54.74°.
- Lotus-seed big face: base + three unit triangles makes a triangle of side 2 + r (φ² for FUJI).
- Antiprisms: cos D_n = (1 − 4cos(π/n))/3 and r = 2cos(π/n) − 1, n = 3–12; PROOFS.md §3 right line by line.
- Face-plane members 1/φ, (√3−1)/2, (√6−1)/2, 0. Odom: sides e and 1 + e, all 120°, r = e/(1 + e).
- STT: Damasceno's 2:1 hexagons (checked in the PDF); at r = 1/2 the small-triangle cell of the breathing pyrochlore is the STT.
- k-families: cos L formula, flat limits 1, 2 sin 15°, 2 sin 6°, nothing for k ≥ 6.
- Dictosphere solid sides 1.0353 / 0.3789 at inradius 1 (r = (√3−1)/2); spherical Voronoi of the 14 ports is exactly its central
  projection; arc ratio 0.3562; 1.35/3.79 cm on the sphere, 1.67/4.55 cm flat (R = 4.396 cm); equal clearance ⇔ equal face distances;
  every rhombic dodecahedron edge on a three-fold axis.
- CLEO sphere: circumradius 1, volume (11√5−5)/6 = 3.26612 = 20 CLEO + 12 × √5/12; Penta-cleo √5/60. Icosahedral Cleo: icosahedron
  edge 2/√5, dihedrals 72° and 69.09°. Cuboctahedron central pyramids: 8 regular tetrahedra + 6 J1. Six circles cross every 36°, make
  20 triangles + 12 pentagons. Wheel search: 4 hexagonal and 6 decagonal with zero error.

## 4. Extra insights (kept separate)

**A. Why the dictosphere's r is the cuboctahedral member (README: open).** In |x|, |y|, |z| ≤ 1, |x| + |y| + |z| ≤ S, put an apex at
the cube corner (1, 1, 1) over the triangle on x + y + z = S. All six side edges are √((2 − S)² + 1) for any S; the long faces lie in
cube faces; they are equilateral exactly when 2(S − 1)² = (2 − S)² + 1, i.e. S² = 3, the equal-depth solid. So the even-margin rule is
the same as "the cube's corners are FUJI((√3−1)/2) apexes (scale 1.035) over the triangles". The same fact explains the cuboctahedron
match: long faces in {100}, base in {111}, so L = 54.74° and r = (√3−1)/2.

**B. Cleaner antiprism form.** 1 + r = 2cos(π/n), the short diagonal d_n of the unit n-gon; silver, golden, √3 for n = 4, 5, 6. The
Lotus seed's face edge φ² = 1 + d_5.

**C. One closed form for the k-family flat limit.** r_flat = 2 sin(π/k − π/6): 1, 2 sin 15°, 2 sin 6°; shows why k ≥ 6 is empty.

**D. The breathing pyrochlore is a Wythoff construction.** In Ã₃ ring two adjacent nodes at distances d₀, d₁: two tetrahedra and two
truncated-tetrahedron kinds, tiling for any distances, r = d₁/d₀. Proves "every r". r → 0 gives the tetrahedral–octahedral honeycomb.
The two truncated-tetrahedron kinds are twin members of Damasceno's truncation family with the same hexagon (tetrahedron side and
octahedron side); at r = 1/2 the tetrahedron-side cell is the STT. Reference: Coxeter, *Regular Polytopes*.

**E. Wheels and rings.** Square, hexagonal, decagonal wheels give 3, 4, 6: the equatorial great-circle systems of the octahedron,
cuboctahedron, icosidodecahedron (classical, Coxeter, quasi-regular polyhedra). Five octagonal wheels (crossing every 45°) not found:
300 random starts, best error 6.8° (numerical, not proof). One ring template always works: any great-circle arrangement is a 4-valent
map, so an alternating slot pattern exists (as for alternating knot diagrams); with equal crossing angles and spacing the six rings are
identical.

**F. Next questions.** Does any n ≠ 5 close a Lotus-seed-like cluster with FUJI(2cos(π/n) − 1)? (Face-plane condition is necessary
only.) Dodecahedron–icosahedron analogue of Insight A: face-plane rule suggests r ≈ 0.692 (icosidodecahedral member); numerical attempt
inconclusive, open. A callipered re-measurement of one dictosphere would settle 2.5.

DICTO · dictospheres.com
