# Scutoid Frusta: definition and enumeration (24 November 2026)

DICTO · project V SF A (Vacuus, Scutoid Frusta, Aequus), row SF of the Map: define, enumerate. Term "Scutoid Frusta" (singular
scutoid frustum) and the Map are DICTO's. "Scutoid" alone below means only the 2018 biology term (Gómez-Gálvez et al., Nat. Commun. 9, 2960, 2018).

> **Status box.** Study note, not published. Definition SETTLED by DICTO's decisions (below, 25 Nov). All counts exact;
> every listed solid realised with rational coordinates and checked in exact arithmetic. Literature on counting scutoid types not yet searched (LEAD 5).

**Verdict.** With the proposed convex definition, there are exactly **45 combinatorial types of Scutoid Frusta with end side counts
n, m ≤ 8 and at most two Y-corners** (58 if mirror images count separately): 6 frusta (no Y-corner), 5 with one Y-corner, 34 with two.
All 45 are realised exactly as convex polyhedra with parallel ends. A side-count law holds for every scutoid frustum: **Y-corners ≥ |n − m|,
and Y-corners ≡ n + m (mod 2)**. Two types tile space together (exact construction), one type with four Y-corners tiles space alone. Almost all
resin pieces of our amber cells fall **outside** the convex definition (not convex, or not simple), so DICTO's choice in Question 1 decides
whether they are Scutoid Frusta.

## 1. Definition (proposal for DICTO's approval)

**Scutoid frustum (convex).** A convex polyhedron with two disjoint faces chosen as its **ends** (top: n-gon, bottom: m-gon); all other
faces are **lateral faces**, such that
1. every vertex has exactly three edges (the solid is simple);
2. every lateral face meets at least one end along an edge;
3. a vertex on neither end is a **Y-corner**; let k be their number.

It is a **frustum** when k = 0 (then, by the law below, n = m and every lateral face is a quadrilateral: a prism-type piece), and a
**scutoid frustum proper** when k ≥ 1 (side count changed, or kept with Y-corners in between).

**Law (Proposition 1).** Lateral faces = (n + m + k)/2; lateral faces meeting both ends = (n + m − k)/2. Hence k ≥ |n − m| and
k ≡ n + m (mod 2).
*Proof.* Euler for a solid with V = n + m + k vertices, all of degree 3 (so E = 3V/2), and F = lateral + 2 faces gives lateral = V/2.
A planar end meets a convex lateral face in at most one edge, and each end edge lies in exactly one lateral face; so
lateral = n + m − t, t = number of lateral faces meeting both ends, with 0 ≤ t ≤ min(n, m). ∎

**Parallel ends cost nothing (Lemma 2).** Every convex scutoid frustum has a combinatorially equal one with parallel ends.
*Proof.* If the end planes meet in a line L, the solid lies in the wedge they bound and misses L (the ends are disjoint). A plane through L
outside the wedge misses the solid; a projective map sending that plane to infinity keeps the solid convex, keeps every face, and makes the end
planes parallel. ∎ So the enumeration may take parallel ends, without loss.

**Against the 2018 paper (checked against the text itself, open-access copy PMC6063940).** Gómez-Gálvez et al. give no formal
definition. They model epithelial cells as Voronoi cells between two curved surfaces (apical and basal: cylinders, spheroids) and
contrast them with "prisms" (flat tissue) and "frusta" (bent tissue). When neighbours change between the two surfaces, "the exchange of
neighbours involved the appearance of a vertex along the apico-basal axis of these solids"; "We coin the term scutoid to name this
geometrical solid"; "Scutoids, in contrast to prisms/frusta, are not necessarily convex, and present non-planar lateral faces". So their
scutoid has curved ends and curved, possibly non-convex walls, and is marked by at least one vertex between the surfaces. (The often-quoted
sentence "a geometrical solid between two parallel surfaces ... joined by either a curve or a Y-shaped connection" is NOT in the paper; it
comes from secondary sources. Our earlier wording followed it; corrected here.) Our convex definition is therefore a flat-faced, convex,
simple subclass, which the paper itself places on the prism/frustum side for k = 0; it adds condition 2 (no lateral face lying wholly between
the ends), which the paper does not discuss. The wider tier below (bent walls, curved ends) matches the paper's scutoids.

**Against our own pieces** (scripts/amber_types.py, data/amber_types.json; stored data of the three studies, nothing recomputed):

| our pieces | fit the convex definition? |
|---|---|
| slanted rhombic prism S (scutoid stand-in, step 2) | yes: frustum SF 4-4-0 |
| amber-cell sweep, Amber-Ammann, Aequi cells: 2389 kinds (counted per cell; the Aequi cell files were absent from their study folder at the rerun, so only sweep and Ammann are counted) | 1894 kinds not convex (a dihedral angle over 180°; walls folded where they pinch to a Y vertex) |
| same, side-count law | 454 kinds break k ≥ \|n − m\|, k ≡ n + m: their vertices are not all of degree 3 (walls end at core or mould vertices, fins), so "Y vertex" there is not a Y-corner of a simple solid |
| convex, law-respecting, with Y | Amber-Ammann C1 (Fullerene Star) cells: 20 kinds 3 → 4, one Y (type SF 3-4-1); C2 (Rollerball) cells: 10 Ammann kinds + 1 sweep kind (fcc, s0) 3 → 5, two Y (SF 3-5-2.1 or .2); truncated dodecahedron, sc 6/5: one kind 3 → 6, three Y. These fit **if** the mould-side end is one flat polygon: not checked (the stored data has no face planes; LEAD 3). Their ends are not parallel; Lemma 2 shows that does not matter. |
| central (cone) division of Proposition 12, #117 | k = 0 pieces; frusta if the mould end is flat (not checked) |

So the convex definition misses nearly all amber pieces. A second, wider tier would hold them: **scutoid frustum (general)**: a solid
topologically a ball, with two disjoint end discs, a band of lateral faces between them (faces may be bent), each lateral face meeting an
end; Y-corners = vertices in the band. Question 1 asks which tier is "the" definition.


**DECISIONS (DICTO, 24-25 Nov 2026).** 1 two tiers: Scutoid-Frusta = the general piece (amber pieces included); convex Scutoid-Frusta =
the enumerated class (24 Nov). 2 flat ends for the convex tier; the general tier may have a bent mould end. 3 convexity for the convex tier
only. 4 parallel ends not required. 5 every lateral face meets an end (required). 6 three edges at every corner required for the count;
merged four-edged corners listed separately as limiting cases. 7 a type is the solid with its two chosen end faces; solids with more
than one reading are noted. 8 mirror images one type, the two-handed count shown beside it (45 types; 58 with both hands).

## 2. Questions for DICTO

1. **Tier.** Is a scutoid frustum (a) the convex flat-faced solid above, or (b) the general piece with bent walls (which includes our amber
   pieces)? Proposal: name both: "Scutoid Frusta" = (b), "convex Scutoid Frusta" = (a), the enumerated class.
2. **Planar ends?** Amber pieces have their mould end on the mould surface, which can bend over a mould edge. Must both ends be flat?
3. **Convex?** 1894 of 2389 amber kinds are not convex.
4. **Parallel ends?** Lemma 2: for convex pieces this changes no type; it matters only for the shape. Require it or not?
5. **Every lateral face meets an end?** Without this, a face can start and end between the ends (a "hidden" face).
6. **Simple (three edges at every vertex)?** Without it, two Y-corners can merge into one four-edged corner, and edges can run straight to an end vertex.
7. **Ends chosen or given?** The same solid can be a scutoid frustum in more than one way (Section 4); e.g. the pentagonal prism is SF 5-5-0 with its
   pentagons as ends and SF 4-4-2.3 with two non-adjacent side squares as ends.
8. **Mirror images:** one type or two? (Table gives both counts.)

## 3. Enumeration (scripts/sf_enum.py; data/types_n8_k2.json, data/type_list.csv; log data/run_n8_k2.log)

Method. With parallel ends (Lemma 2) the cross-section at height t is a convex polygon with fixed edge directions whose edge offsets change
linearly in t. As t rises, a Y-corner is the moment one lateral face ends (its edge shrinks to a point) or starts. Condition 2 forbids a face
that both starts and ends, so only bottom faces can end and only new faces can start. Every type is therefore a sequence of k such events
applied to the bottom m-gon. Simple solids are stable under small changes of their face planes, so Y-corners at equal heights can be
separated: the sequences give **all** types (complete for k ≤ 2, n, m ≤ 8, and checked to 14). For each sequence: a small linear programme
(floating point) gives edge directions and offsets; these are rounded to rationals and the solid is rebuilt and checked in **exact**
arithmetic (all vertices, three edges at each, every plane a face, n, m, k, condition 2), then reduced to a canonical code of its face map
(mirror images and end swap allowed). 118 sequences, 45 types, 0 failures. One sequence (start a face, then end the face opposite, from a
triangle) is not a polyhedron: two lateral faces would share two edges (graph not 3-connected; Steinitz), excluded.

Independent checks (scripts/checks.py, checks/checks.log, FINAL ok): every stored solid re-read from its planes: vertices inside all planes exactly,
V − E + F = 2, three edges at every vertex, 3-connected (removing any two vertices leaves it connected), n, m, k as recorded, Proposition 1,
types pairwise distinct; counts against the formulas below for n ≤ 14.

**Table: number of types** (mirror pairs as one; in brackets counting both hands where different). Ends n ≤ m ≤ 8, k ≤ 2.

| ends | k = 0 | k = 1 | k = 2 |
|---|---|---|---|
| 3, 3 | 1 | | 1 |
| 3, 4 | | 1 | |
| 3, 5 | | | 2 (3) |
| 4, 4 | 1 | | 3 (4) |
| 4, 5 | | 1 | |
| 4, 6 | | | 3 (4) |
| 5, 5 | 1 | | 4 (5) |
| 5, 6 | | 1 | |
| 5, 7 | | | 3 (4) |
| 6, 6 | 1 | | 4 (6) |
| 6, 7 | | 1 | |
| 6, 8 | | | 4 (5) |
| 7, 7 | 1 | | 5 (7) |
| 7, 8 | | 1 | |
| 8, 8 | 1 | | 5 (8) |
| **all** | **6** | **5** | **34 (47)** |

Total 45 types (58 counting both hands). No other (n, m, k) occurs, as Proposition 1 requires.

**Formulas** (proved for k ≤ 1 and for (n, n+2, 2); computed for n ≤ 14 in the other case):
- (n, n, 0): 1 (the n-gonal prism type). (n, n+1, 1): 1 (one bottom face ends; all positions alike).
- (n, n+2, 2): ⌊(n+2)/2⌋ types, one more counting both hands. Two of the n+2 bottom faces end; the type is their distance d = 1 … ⌊(n+2)/2⌋
  around the bottom; for d = 1 the order of ending gives a mirror pair, otherwise the pair is mirror-symmetric.
- (n, n, 2): ⌊(n+3)/2⌋ types for 4 ≤ n ≤ 14 (n = 3: 1); counting both hands exactly n for 4 ≤ n ≤ 14. A proof for all n is LEAD 4.

**Type list** (ids SF n-m-k.j; events read from the smaller end upward; full data in data/type_list.csv):

| id | V | lateral face sides | from the n-end upward | chiral |
|---|---|---|---|---|
| SF 3-3-0 | 6 | 4 4 4 | (triangular prism) | |
| SF 3-3-2 | 8 | 4 4 5 5 | a face starts, then a neighbouring old face ends | |
| SF 3-4-1 | 8 | 3 4 5 5 | one face starts | |
| SF 3-5-2.1 | 10 | 3 4 4 5 6 | two faces start, the second beside the first | yes |
| SF 3-5-2.2 | 10 | 3 3 5 5 6 | two faces start, one face apart | |
| SF n-n-0, n = 4…8 | 2n | all 4 | prism types | |
| SF n-(n+1)-1, n = 4…7 | 2n+2 | 3, 5, 5, rest 4 | one face starts | |
| SF n-(n+2)-2.j | 2n+4 | | two faces start at distance j (j = 1: chiral pair) | j = 1 |
| SF n-n-2.j | 2n+2 | | one face ends and one starts; positions as in the csv | see csv |

The 2018 scutoid with one Y-corner between a pentagon and a hexagon is **SF 5-6-1**. The classic neighbour swap (T1 transition: a face ends,
a face starts between the same two neighbours) is SF 4-4-2.2, 5-5-2.3, 6-6-2.3, 7-7-2.4, 8-8-2.4; its two Y-corners are joined by one edge.

**Minimal examples.** The smallest proper scutoid frustum has 8 vertices and 6 faces (sides 3, 3, 4, 4, 5, 5): it is both SF 3-4-1 and
SF 3-3-2, the same solid with different ends. No smaller one exists: k ≥ 1 needs V = n + m + k ≥ 8 with n, m ≥ 3 and k ≡ n + m (mod 2).

## 4. Same solid, other ends (checks.log)

Solids that are Scutoid Frusta in more than one way (code without end marks): {SF 3-3-2, SF 3-4-1}, {SF 3-5-2.1, SF 4-4-2.1},
{SF 4-4-2.3, SF 5-5-0 = pentagonal prism}, {SF 4-6-2.2, SF 5-5-2.3}, {SF 4-6-2.3, SF 5-5-2.1}.

## 5. Which types tile space (only cheap checks; no tests of non-filling)

- Known: SF 3-3-0, 4-4-0, 5-5-0, 6-6-0 tile space alone (right prisms over a triangle, parallelogram, a tiling convex pentagon, the regular
  hexagon). SF 4-4-2.3 is the pentagonal prism read with other ends, so it tiles as well. The stand-in S (rhombohedron, SF 4-4-0) tiles.
- **New, exact (scripts/tilings.py, data/tilings.json, data/tilings.log).** Power diagrams (weighted Voronoi diagrams; Aurenhammer 1987) whose
  weights change linearly with height have flat cell walls: each wall inequality |X − p|² − w_p ≤ |X − q|² − w_q is linear in (x, y, z)
  when w is linear in z. So every slab 0 ≤ z ≤ 1 is tiled by convex scutoid frusta with parallel ends. Sites: the centred rectangular set
  (i + r/2 mod 1, r); even rows weighted d(z), odd rows 0.
  - **Pair:** d from 0 to −1. Even cells are **SF 4-6-2.3** (6 → 4: the two same-row walls end), odd cells **SF 6-8-2.4** (6 → 8). Both cells
    are mirror-symmetric; slabs stacked by reflection in z = 1, 2, … tile space with the two types.
  - **Alone:** d from 1 to −1. Even cells go 8 → 4 with **four Y-corners** (outside the k ≤ 2 table), odd cells 4 → 8; the map
    (x, y, z) → (x + ½, y + 1, 1 − z) carries the even cell exactly onto the odd cell, and the even cell is mirror-symmetric, so all cells are
    congruent. Slabs stacked by the translation (½, 1, 1) tile space with **one convex scutoid frustum, n = 4, m = 8, k = 4**.
  All coordinates rational; cell types computed in exact arithmetic with the same checks as Section 3.
- Not decided: which other types tile alone or in pairs (LEAD 2).

## 6. OEIS

No natural new sequence: the counts are linear in n (formulas above, e.g. n for (n, n, 2) counting both hands). Not submitted, not proposed.
A richer count, such as all types by number of faces with k free, could give one (LEAD 6).

## Sources checked
Gómez-Gálvez et al., Nat. Commun. 9, 2960 (2018), full text read (open-access copy PMC6063940) for the definition; our studies 2026-11-21-scutoid-stand-in, -amber-cell-sweep,
-y-junction-axes, -amber-ammann, 2026-11-24-aequi-vacuus-scutoids; paper #117 (Dehn packets, Proposition 12, 17). Methods borrowed:
Steinitz's theorem; projective transformations of polytopes; power diagrams (F. Aurenhammer, SIAM J. Comput. 16, 1987); linear programming
(HiGHS via SciPy) only to find coordinates, every result then checked exactly.

## LEADS
1. DICTO's answers to Questions 1–8; then fix the term in the concordance.
2. Tiling: run the linear-weight power-diagram method over small periodic site sets to find which table types tile alone or in pairs
   (positive constructions only).
3. Amber pieces: test whether the mould-side end of the 32 convex kinds with Y (Ammann C1, C2; sweep C2, truncated dodecahedron) is one flat
   polygon; if so, name their types (SF 3-4-1 expected for Ammann C1).
4. Prove the (n, n, 2) count for all n.
5. Literature: search for later papers (2019 on) that define scutoids formally, and for earlier counts of scutoid or "prismatoid with Y-junction" combinatorial types before any public claim.
6. General tier: enumerate k = 3, 4 (the method extends without change) and count by faces; check for an OEIS match.
7. V + SF: Vacuus plates as end faces: which table types occur between inner and outer Vacuus.

## Files
scripts/sf_enum.py (enumeration), scripts/checks.py (independent checks, type ids), scripts/tilings.py (power-diagram tilings),
scripts/amber_types.py (our pieces); data/types_n8_k2.json and data/types_n14_k2.json (every type: planes, vertices, faces, events),
data/type_list.csv/.json, data/tilings.json, data/amber_types.json and logs; checks/checks.log (FINAL ok).
Run: `python scripts/sf_enum.py 8 2 data/types_n8_k2.json` (also with 14), then tilings.py, checks.py (Python with SciPy).

## Decisions (24 Nov; DICTO: "make decisions instead of questions")
1. Two tiers: **Scutoid Frusta** = the general piece (bent walls allowed, includes the amber pieces); **convex Scutoid Frusta** = the enumerated class.
2. Ends flat in the convex class; may bend in the general class.
3. Convexity required only in the convex class.
4. Parallel ends not required (Lemma 2: no type changes).
5. Every lateral face meets an end: required (a face starting and ending between the ends makes the piece not a scutoid frustum).
6. Simple (three edges at every vertex): required in the enumerated class; merged Y-corners are recorded as degenerate cases.
7. A type is a solid with a chosen pair of ends; a solid with several choices is listed under each, and solids are also counted once.
8. Mirror images: one type, marked chiral; both counts kept in the table.
