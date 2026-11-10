# Icosahedra filling space with Cleo-Icos and Antonius (DICTO 10 Nov 2026)
Motivation (DICTO): to make the icosahedron tile space, "as it was said not possible". The Cleo-Icos (#29, Aristotle's pyramid #44)
and Antonius (D65, #44) came from that search. Earlier status: icosahedra alone or with face pyramids are excluded (Dehn); icosahedra
with Antonius were left open (study 2026-10-27-five-pyramids).

**Step 1, Dehn balance (proof).** Dehn invariants add under dissection. The golden rhombohedron Cleo + Antonius + Cleo fills space by
translation, so D(rhombohedron) = 0 and D(Antonius) = −2 D(Cleo-Icos). The icosahedron is 20 Cleo-Icos round its centre (inner edges
close full turns, contributing rational multiples of π), so D(icosahedron) = 20 D(Cleo-Icos). Hence D(icosahedron) + 10 D(Antonius) = 0:
a filling must use icosahedra and Antonius in the ratio 1 : 10 (plus any Cleo–Antonius–Cleo groups). Necessary, not sufficient.

**Step 2 plan.** (a) which golden rhombohedron is Cleo + Antonius + Cleo (prolate or oblate); can the other split into Cleo-Icos and
Antonius (or what further piece it needs); (b) in Ammann–Kramer–Neri 3D Penrose tilings, the corners surrounded by 20 prolate
rhombohedra (a rhombic triacontahedron) each hold a full icosahedron of 20 inner Cleo-Icos: confirm they occur and their frequency;
(c) periodic version: do the cubic approximants (1/1, 2/1, …; study 2026-11-10-ab-line step 4) contain them.

**Step 2(a) (volumes, exact).** The prolate golden rhombohedron spanned by the three corners a, b, c of one icosahedron face (from
the centre) is Cleo + Antonius + Cleo: its acute corners are the Cleo-Icos conv(0, a, b, c) and its opposite; volume 6 Cleo, so
Antonius = 4 Cleo (#44). The oblate golden rhombohedron has volume (prolate)/φ = 6/φ ≈ 3.708 Cleo volumes, while every union of
Cleo-Icos (1), Antonius (4) and icosahedra (20) has a whole-number volume: the oblate rhombohedron cannot be cut into these pieces.
So the Ammann–Kramer–Neri tilings (both rhombohedra) do not decompose into DICTO's pieces as they stand.
Twenty prolate rhombohedra round one point (spanned by the 20 face triples) form the rhombic hexecontahedron (the '20 + 20 + 20' of
study 2026-10-27-five-pyramids): 20 inner Cleo-Icos = a whole icosahedron, then 20 Antonius, then 20 outer Cleo-Icos.
**Refined question.** Can space be filled by prolate golden rhombohedra alone, including rhombic-hexecontahedron stars? Each star holds
a whole icosahedron; everything else splits into Cleo-Icos and Antonius. Obstacle: de Bruijn (grid) tilings in the six icosahedral
directions always contain oblate tiles, so such a filling must be non-zonotopal. Next: exact search for a prolate-only surround of
one hexecontahedron star (icosahedral orientations, face-to-face).

**Step 2(b) result (10 Nov 2026).** surround.py (prolate tiles only, corners in Z<e1..e6>, nearest-open-face-first, backtracking):
the hexecontahedron star is surrounded to search radius 1.9/2.2 (+60 tiles), 2.6/3.0 (+180), 3.4 (+320), with almost no backtracking
(nodes = tiles + 14). verify_exact.py, exact in Q(√5) (separating axes, edge length 1): witnesses 2.6 (200 tiles, 2524 close pairs) and
3.4 (340 tiles, 4572 pairs): no two tiles overlap; no face is used by more than two tiles; no open face has its centre inside the radius.
Covered ball: at least radius 3.4 − (half the longest face diagonal, ≈ 0.85) ≈ 2.5 for the 3.4 witness. So locally a whole icosahedron
(20 Cleo-Icos) sits inside a filling of Cleo-Icos + Antonius. Open: all of space (periodic star arrangement, or a proof the shells close
for ever). DICTO 10 Nov: "octet and gyrated octet could both be used": restated to him, awaiting his confirmation.

**Step 3, the icosahedral (gyrated) octet (DICTO 10 Nov 2026, confirmed: "so new pieces for icosahedral gyrated octet").**
octet_gap.py (exact, sympy). Regular octahedron, corners (±1,0,0)…, edge √2. The regular icosahedron with its 12 corners on the 12 edges,
each edge divided in the golden ratio: icosahedron edge 3 − √5, volume 70/3 − 10√5 ≈ 0.97265 of the octahedron's 4/3. Eight
icosahedron faces lie in the eight octahedron faces; the other 12 come in 6 folded pairs, one pair facing each octahedron corner.
NEW PIECE (placeholder name: corner piece; name is DICTO's): octahedron minus icosahedron = 6 congruent corner pieces, each the octahedron
corner plus the 4 icosahedron corners on its 4 edges; volume (5√5 − 11)/3 ≈ 0.06011. Faces: 4 triangles in the octahedron faces + 2
icosahedron faces as a folded base. It is NOT convex: at the fold (an icosahedron edge) its inside angle is 360° − 138.19° = 221.81°.
It is two mirror-image tetrahedra glued on the triangle (corner, fold edge).
Filling: octet or gyrated octet, each octahedron = 1 icosahedron + 6 corner pieces, tetrahedra whole. Each octahedron's icosahedron has
two positions (the two golden divisions); octahedra meet only at corners, so the choice is free per octahedron, in both octets.
So icosahedra + corner pieces + tetrahedra fill space (immediate, exact). Dehn: the corner pieces carry the icosahedron's golden angles.
Next: corner piece angles and whether it relates to Cleo-Icos/Antonius; whether tetrahedron + corner pieces merge into nicer pieces.

**Step 4, stars on the octet and the gyrated octet (DICTO 10 Nov 2026: both, in order, each tested on its own; corner piece aside).**
octet_stars.py: stars at fcc points x(i,j,k), i+j+k even, cube axes = icosahedron 2-fold axes; x = 2m + 2nφ (unnormalised axis units).
Star spacings 1.05, 2.41, 2.97: stars overlap. 3.89 (1,1) and 4.46 (3,0): IMPOSSIBLE face to face (search exhausted in 3 nodes; rechecked
with the faster version). 4.81, 5.38, 6.30: 25-minute runs (oct2-*.log on the compute machine).
gyro_stars.py: hcp stars (layers ⟂ (1,1,1), ABAB, period c = (4x/3)(1,1,1)). Exact grid condition: every star centre must lie in the
module of the first star (face-to-face tiles never leave it); c is in the module only when 3 divides both m and n in the tested cases
((1,1), (0,2), (2,1), (1,2) excluded exactly; (3,0), (0,3), (3,3) pass). Runs: spacings 4.46, 7.22, 8.92, 11.68 (gyro-*.log).

**Step 5, Dehn check: Cleo-Icos + Antonius + dodecahedron face pyramids (DICTO 10 Nov 2026: "yes add the Dehn check with antonius").**
Angles: θ_D = arccos(−1/√5) (dodecahedron), θ_I = arccos(−√5/3) (icosahedron). Pentagonal (dodecahedron face) pyramid, base edge a:
base edges carry θ_D/2, side edges 120° (rational): D = (5a/2) ⊗ θ_D. Cleo-Icos: base θ_I/2, sides 72°: D = (3s/2) ⊗ θ_I. Antonius
(middle of the golden rhombohedron): angles θ_I/2-type and multiples of 36° only, so D(Antonius) ∈ R ⊗ θ_I (= −2 D(Cleo) at equal size).
Lemma: θ_D, θ_I, π are linearly independent over Q. Proof: a relation pθ_D + qθ_I = rπ makes z = ((−1+2i)/√5)^p ((−√5+2i)/3)^q a root of
unity in Q(i, √5). −√5 + 2i and −√5 − 2i have product 9 and are coprime (their difference 4i and sum −2√5 share no factor with 9), so
(−√5+2i)/3 has valuation +1 at a prime above 3 where its conjugate has −1: q = 0. Then (−1+2i)/√5 would be a root of unity; but
−1 + 2i = −(1 − 2i) is one prime factor of 5 = (1+2i)(1−2i) and √5 holds both halves, so its valuations above 5 are unequal: p = 0. ∎
(Numerical check: PSLQ finds no integer relation with coefficients up to 10¹², 80 digits.)
Theorem: no space filling (any sizes, any arrangement, periodic or not) uses dodecahedron face pyramids together with only Cleo-Icos and
Antonius. Proof: in a filling, frequency-weighted Dehn invariants sum to zero (Debrunner; Lagarias–Moews), and by the lemma the θ_D part
(5/2) Σ a_j ⊗ θ_D must vanish by itself; every term is positive, so there are no pentagonal pyramids. ∎
A partner with a NEGATIVE θ_D part is needed (as Antonius is the negative θ_I partner of the Cleo-Icos): the #47 connectors.
DICTO 10 Nov: "they fill an icosidodecahedron together": the centre cut gives 20 triangle pyramids twice the Cleo-Icos height and 12 pentagonal pyramids 2/φ the dodecahedron-pyramid height (the core of the icosahedron + dodecahedron compound); DICTO: "doesnt help icosahedron situation just broadens question": closed as a side note.

**Step 4 job plan (DICTO 11-10: "strategize the job too"; written BEFORE launch, checked at every 20-minute attention check).**
Lesson from the first SAT launch: candidate enumeration never ended (the golden grid is dense); now bounded by a hidden-space window W.
Stages per run, each printing PROGRESS lines (fraction of the whole job) so the stall guard can project the finish:
| stage | what | size from the pilot | budget | on overrun |
|---|---|---|---|---|
| 1 enumerate | candidate tiles inside radius and window | control pilot sets it | 20 % of cap | shrink WMARGIN or radius; never let it grow open-ended |
| 2 clauses | cover/match + overlap pairs (kd-tree, separating axes) | ≈ 30 overlap pairs per candidate | 20 % | parallelise the pair tests |
| 3 solve | CaDiCaL | unknown: first solve sets it | 60 % | split by the first face's choices (cube-and-conquer) |
Order: control (must be SAT) → octet 4.81 → 5.38 → 6.30 → gyrated 7.22 → 8.92 → 11.68, launched together only after the control passes.
Outcomes: SAT → exact check (verify_exact.py) → then the next radius out; UNSAT at window W → widen WMARGIN 0.5 → 1.0 → 1.5 once
(a filling outside the window is still possible); UNSAT at the widest → record 'no face-to-face filling within window', move on.
Control failing (UNSAT on a single star to radius 3.4, known fillable) = the window is too tight: widen before anything else runs.
