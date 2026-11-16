# Walls of Silence: independent attack and restructuring (16 Nov 2026)

Reviewer: Claude (Anthropic), for DICTO. Read cold: `papers/2026-11-16-walls-of-silence/paper.html`, `papers/2026-11-16-silent-running/paper.html`, the seven studies of 16 Nov named in the draft's meta line, and DICTO's #104, #105 and #107. Nothing in the paper or the studies was edited. Every count below marked "recomputed" comes from new code written for this review (floating point, tolerance 1e-7 on unit vectors, run as pilots on the compute machine; none of the studies' code was reused). Those runs confirm counts; they do not confirm the word "exact".

## 1. Verdict

The numbers are sound: every count I recomputed agrees with the draft, including the two large chamber counts by a different method, with one exception, a swapped pair of volumes in the proof of Theorem 3. Nothing is fatal. The weakness is in what the numbers are said to mean and in how the results are ranked. Three definitions do not hold still between the paper and the studies (the centre of a Vacuus, what a wall is a wall of, and "twist"). The rule of the three kinds is false as worded. The Main theorem is true, but its plates lie on walls because A and B are made of the 600-cell's corners, not because of the twist: three short lemmas about small faces on those corners prove it by hand and also explain why most symmetric shapes on the corners are hidden. Theorem 6 is true by definition for every viewing direction, and the "by solids" answers are true for a trivial reason. The strongest new mathematics is §6, the copies in the 120-cell with their three classes of wall and the exact split of the triangles, and after that the chamber counts. The paper should be rebuilt round those, with the Main theorem as an opening theorem that follows from the face lemmas.

**What is solid (recomputed, all agree with the draft).**

| item | recomputed |
|---|---|
| A, −A, C3, B, −B are 120 distinct points on one sphere, closed under reflection in themselves; 12 neighbours each | 720 edges, 1200 triangles, 600 cells |
| mirrors and cross walls | 60 and 300, no wall in both |
| 600-cell triangles; 120-cell pentagons | 1200 on 60 plates, 20 each; 720 on the same 60, 12 each |
| A; B; C3 (plates: mirror / cross / none) | 30 / 0 / 0; 40 / 40 / 0; 5 plates of 14 faces, 0 / 5 / 0 |
| mirrors of A and of B | share exactly the 10 mirrors of S5; union all 60 |
| ordinary orbits t = 3/2, 6/5 | 10 / 0 / 20 and 10 / 0 / 70 |
| union of the five hulls; core; A ∩ B (Monte Carlo, 966,280 points in the 600-cell) | 0.6511 ± 0.0005; 0.0552 ± 0.0002; 0.1308 ± 0.0003 |
| inscribed 600-cells of the 120-cell | exactly 10; every corner in 2; 25 pairs meet in 24 corners with the 24-cell's distances, 20 pairs in none; two states of 5 |
| walls of the ten 600-cells | 1560 = 60 (cross wall of all 10) + 300 (mirror of exactly 2) + 1200 (cross wall of exactly 2) |
| chambers, by inserting the walls one at a time (not Zaslavsky's sum) | mirrors 14400; 360 walls: 298 in a Coxeter chamber with 25 walls through it, and 4,291,200 counted over the whole space without the chamber step; A's 30 plates 3360; B's 80 plates 62,880; 1560 walls: 41,197 in a Coxeter chamber with 174 walls through it, and 593,236,800 over the whole space |
| S5-orbits of the 120-cell | 5, 5, 20 × 4, 30, 60 × 4, 120, 120; the two runcitruncated orbits have 120 faces on 75 plates, at most 10 on one, 30 / 5 / 40 |
| walls kept in the four views (mirrors, cross) | (15, 30), (6, 10), (4, 12), (6, 27) |
| chance baseline, 100 random subsets | 20 corners: 27.8% of plates on no wall; 30 corners: 20.3%; no all-wall sample |
| station, truncation at 1/2 − √5/10 of each edge | 2400 corner triangles, 8 on each of the 300 cross walls; at 1/3 and at 1/5, 1200 plates on no wall |
| Proposition 8's counting, by hand | 30 triangles per corner; no 4 corners of an icosahedron pairwise non-adjacent; 12k ≤ 3(120 − k) gives k ≤ 24; 1200 − 720 = 480 > 60 |
| cubic t³ − 359t² + 45959t − 2099281 | χ(−1) gives 4,291,200; 2099281 = 29 · 191 · 379 and no divisor is a root, so it is irreducible over Q |

Not recomputed: the copy counts 1200 / 1200 / 600 and the stabiliser orders 12 and 24 (only their arithmetic), the half-cat table (only its sums: 90,000 cases, 18 patterns, 1500 / 90,000 = 1/60), the skeleton coverage, the slices of Table 2, the 686 and 17,371 regions, the non-congruence and the 15 types of the 298 pieces, Proposition 9, the uniform-family census, the maximal-subgroup census and the atlases.

## 2. Findings

Severity counts: fatal 0, serious 10, minor 8, editorial 4.

**1. Serious. The centre of the Vacuus is not the same in the paper and in the studies. Paper §2; Proposition 8; Tables 1 and 5; §4 (GET).**
Problem: §2 says the centre O is "here the centre of its corners". The studies measure every shape on a Queen's corners from the Queen's centre (`qv_lib.py`: "centre = origin"; vicinity README: "centrally symmetric about the Queens' centre"). For a shape that is not balanced the two differ, and both the kind and the verdict "hidden" change.
Evidence (recomputed): the 600-cell less one corner, measured from the 600-cell's centre: 1170 faces on 60 plates (15 with 18 faces, 45 with 20), all mirrors. Measured from the centroid of its own 119 corners: 915 plates (900 single, 15 with 18 faces), 15 mirrors and 900 on no wall. So under the paper's own §2, Proposition 8 ("every diminished 600-cell is hidden") is false unless the removed corners sum to zero. The walls README says the same of GET: "Measured from GET's own corner centroid instead, only 2 of 54 (A) and 3 of 51 (B) plates are walls."
Fix: define the Vacuus of a pair (X, O). State that for a shape on a Queen's corners O is the Queen's centre (the host centre), and that for A, B, C3 and every S5-orbit this is also the centroid. Say in Proposition 8 and in both tables which centre is used. Report the GET centroid result in the paper, not only the favourable centre.

**2. Serious. The rule of the three kinds is false as worded. Paper §2 ("Which shapes are of which kind"), §9, status box item (2).**
Problem: "removing corners from a heart parent gives the inherited heart kind, and twisting a parent's corners into a new orbit gives the non-heart kind." The two operations are not distinct and neither half holds.
Evidence: (a) A is the 600-cell with 100 corners removed, and it is non-heart; the removing half holds only for the independent sets of Proposition 8. (b) In Silent Running, Theorem 2, all five S5-orbits of the 600-cell are twisted classes, C3 among them ("R, the third 20-point twisted class ... which is C3", paper §4), and C3 is heart with 14 faces on each plate. (c) For orbits of the 120-cell "twist" has no definition: Silent Running defines it for classes of the group 2I, which is the 600-cell's corner set.
Fix: drop the rule. Replace it by the index law of §4 below, which decides every case in Table 1.

**3. Serious. The Main theorem is true, but the twist is not what puts the plates on walls, and the controls do not test that. Paper abstract ("ordinary orbits are not hidden"), §4 ("The golden twist ... is what puts the rest of A's and B's plates on walls"), Main theorem (iii).**
Problem: the ordinary orbits (t = 3/2, 6/5) are not on the 600-cell's corners at all, so the control compares corners with non-corners, not twist with no twist. Shapes on the corners are hidden for a reason that has nothing to do with silence.
Evidence (recomputed): on the 600-cell's corners, every triangle of edge length (1200) lies on a mirror, 20 on each; every golden rectangle, edge by radius (1800), lies on a mirror, 30 on each; every triangle of side equal to the radius (2400) lies on a cross wall, 8 on each. A's faces are edge triangles and hexagons that a transposition of S5 fixes point by point; B's are edge triangles, golden rectangles and radius triangles. That proves the Main theorem (i) and (ii) by hand. The same lemmas explain the draft's own data: random 20-corner subsets already have 72% of their plates on walls; "every full-dimensional hull of an orbit of one of Koca et al.'s five maximal subgroups ... is hidden, except the 12- and 20-corner duopyramids" (§8); the snub 24-cell, the grand antiprism, the 24-cell and all the diminished 600-cells are hidden and are not silent shapes; the 60-point silence sets are "not distinctive" and the 240-point ones fail.
Fix: state the three face lemmas and derive the Main theorem from them, keeping the Q(√5) run as a check. Reword the claim: a shape on the corners with few faces per plate is usually hidden; hidden does not single out the silent shapes. Replace the control by one on the corners (the maximal-subgroup orbit hulls already in §8), and say what it shows. The 100-sample baseline supports only "rare among random subsets" (under about 3%), which the paper should say in those terms.

**4. Serious. The wall system was widened after the test failed for B. Walls README; paper §2.**
Problem: the first test used the 60 mirrors only, and B came out "half hidden": "B: 40 [walls], 40 (the φ√2 triangles) not walls". The cross walls were added afterwards by the ruling "cross walls also count". The paper gives the ruling but not the order of events, so Main theorem (ii) reads as a prediction when half of it was fitted.
Evidence: the README's first table and its sentence "B stays half hidden (40 of 80) even in the pair", followed by the section "Where B's 40 visible plates lie".
Fix: one sentence in §2 saying the cross walls were admitted after B's 40 plates were found on them, and that every later test used the fixed 360. Give the independent reason for them: the cross walls are the 600-cell's central sections taken cell-first, each holding 12 corners and 8 radius triangles (recomputed), which is the middle section of an inscribed 24-cell; with 25 inscribed 24-cells of 12 such sections each, 25 × 12 = 300. That reading should be checked against Coxeter's table of sections, which the draft lists as read.

**5. Serious. Two volumes are swapped. Paper §5, proof of Theorem 3 (c).**
Problem: "The hull volumes are (1 + 3φ)/40 of the 600-cell for A, (14 + 7φ)/60 for B and (3 + 5φ)/24 for C3."
Evidence (recomputed, hull volumes): A 0.146353 = (1 + 3φ)/40; B 0.462090 = (3 + 5φ)/24; C3 0.422104 = (14 + 7φ)/60. Independent check for C3: the hull of the A4 roots has volume 70√5/24 at radius √2, which is 0.42210 of the 600-cell. The construct README lists the three values in the order A, C3, B, which is where the swap came from.
Fix: B (3 + 5φ)/24, C3 (14 + 7φ)/60.

**6. Serious. Theorem 6 is true by definition, for every direction. Paper §3, §7; strength notes ("checked in all eight shadows, not proved in general").**
Problem: a wall with normal n is kept exactly when n·d = 0. A cross wall's normal is the centre direction of a pair of cells of the 600-cell, and a mirror's normal is the centre direction of a pair of cells of the 120-cell (Theorem 2). A cell is side-on exactly when its centre direction is perpendicular to d. So "the kept walls are the central planes parallel to the side-on cells" restates the definition of the walls, and it holds for all d, not only the eight standard views. It is both overclaimed (a law, a theorem) and underclaimed (unproved).
Evidence: the counts follow from it: each cross wall is two side-on tetrahedra (60, 20, 24, 54 hull faces against 30, 10, 12, 27 cross walls) and each mirror two side-on dodecahedra (30, 12, 8, 12 against 15, 6, 4, 6).
Fix: a remark with the one-line proof, then Table 4 and the reach and connectivity counts as observations.

**7. Serious. The "by solids" answers are trivial. Paper abstract; Theorem 3 (c); Theorem 4, last sentence; Theorem 5 (d).**
Problem: "Each contains the centre, so they overlap and cannot tile" and "Each is a cone from the centre, so none is a copy of A or B" need no computation: a region of walls through the centre can never be a solid with the centre inside it. "No chamber ... is congruent to A, B or one of their cells" compares a four-dimensional piece with three-dimensional cells. "None a named shape" is not a mathematical statement. So the third answer to the cat and the steak is not a finding.
Fix: keep the exact volumes, the core and A ∩ B as data in a table. Remove the "none is a copy" clauses from the theorems. In the story, say that walls through the centre cannot cut out a solid round the centre, and that the solids are unions of chambers (A of 3360, with 120 Coxeter chambers among them, is the real statement).

**8. Serious. "Wall" is relative to a host, and §6 changes the host without saying so. Paper §2, Theorem 5 (c), Table 3, abstract.**
Problem: in §2 the walls are the 360 of the dual pair. In §6 a wall is a wall of any of the ten inscribed 600-cells, 1560 in all, of which 1200 are walls of neither Queen of the dual pair. "Both use the same 1560 walls" then reads as if the copies were hidden in the 120-cell's walls. They are not: a B copy has plates on the 1200 new walls.
Evidence (recomputed): the 1560 split 60 + 300 + 1200 as in Table 3; the 60 and the 300 are the 120-cell's own 360 walls; the 1200 are cross walls of exactly two inscribed 600-cells and of nothing else.
Fix: write W(H) for the walls of a host H, and say "hidden in H". State the true result that Table 3 already contains: every A copy is hidden in the 120-cell's own walls (it uses only the 300); B and C3 copies are hidden only in the walls of their inscribed 600-cell.

**9. Serious. Results stated as new that are already DICTO's or classical. Paper Theorem 2, Table 1, §9 "Prior art".**
Problem and evidence: (a) #107, Corollary 2: "The 1200 triangles of the 600-cell and the 720 pentagons of the 120-cell lie on the same 60 central slices, the 60 mirrors of H4: 20 triangles on each, and 12 pentagons on each." That is the first two sentences of Theorem 2, which is labelled a theorem of this paper. (b) #105, Version 4, reports that #108 scanned the polytopes of A4, B4, F4 and H4 "for central slices off the mirrors that carry three or more faces: only the runcinated 5-cell and the 4D permutohedron have them"; C3's five plates of 14 faces are that result, and #108 is not cited. (c) The mirrors and cross walls as central sections of the 600-cell are in the sections of Coxeter that the draft lists as read. (d) The factorisation (t − 1)(t − 11)(t − 19)(t − 29) is the classical one over the exponents of H4 and carries no credit.
Fix: cite #107 Corollary 2 and #108 at the point of use and call Theorem 2 a restatement plus the one new clause (no cross walls from the 120-cell). Credit the sections and the exponents to a source that has been read.

**10. Serious. Prior art still open on the central credit. Paper Table 5 ("solids: DICTO 2026"), reference [8], status box.**
Problem: Koca, Ozdes Koca and Al-Ajmi 2012, on the branching of the W(H4) polytopes under W(A4), is "read in part (§4.1)". The construct README says "we did not check whether that paper names them" and its Lead 2 asks for exactly that check. The paper nevertheless states that the orbits were given "as orbit sets, not as solids".
Fix: read [8] in full before either paper claims the solids. To be checked as well, none of them read by me: Waegell and Aravind's papers on the 60 directions of the 600-cell and the 300 of the 120-cell (the same 60 + 300 normals as the walls); Blind and Blind on the regular-faced polytopes behind Dutour Sikirić and Myrvold's count; a source on free arrangements for the statement that an irreducible cubic factor rules out freeness. Dutour Sikirić and Myrvold [6] must be read past its abstract, since Proposition 8's proof starts from their description of the cells.

**11. Minor. "Exact" covers clauses that are not. Paper labels on Theorems 4, 5 and 7.**
Evidence: Theorem 5 (b) "exactly 1200" rests on a search that filters by floating-point distances (tolerance 1e-6) and then checks exactly; the filter can only let too much through, so the search is complete, but the paper should say why. Theorem 5 (d) is an exact count confirmed in floating point, the label Theorem 4 has. Theorem 4's "no two congruent" is a floating-point test (strength notes). Theorem 7's face lattices come from a floating-point hull.
Fix: label each clause; my recount of 298, 41,197, 3360 and 62,880 by another method can be cited as a third check.

**12. Minor. Proposition 8. Paper §8.**
Problem: the statement needs "about the 600-cell's centre" (finding 1). "Count 314,248,344 such sets" should read "up to symmetry", as in the abstract of [6]. The proof's first sentence (which cells remain) is taken from a paper read only in abstract. The grand antiprism removes adjacent corners and is outside the proposition; say so, since Theorem 7 lists it beside the diminished 600-cells.
Evidence (recomputed): three corners at 120° to each other on one hexagon sum to zero, are independent and are not antipodal; removing them gives 1110 faces on 60 mirrors (3 with 14, 36 with 18, 21 with 20), inherited heart with the centroid at the centre. A useful example for the text.

**13. Minor. The Galois twin clause of Theorem 2 says nothing. Paper Theorem 2, §4.**
Evidence (recomputed): the 20 permutations of (σ², σ², σ², σ, 0), centred, point along exactly the 20 corners of A. The "twin" is the same 600-cell at another size, so it has the same mirrors trivially.
Fix: cut the clause, or say that in these coordinates the twin is the 600-cell itself scaled.

**14. Minor. The sentence on the runcitruncated 5-cells hides the pattern. Paper §2.**
Problem: "carry up to 10 faces on one plate while 40 of their 75 plates lie on no wall" suggests the shared plates are off the walls.
Evidence (recomputed): the 75 plates are 30 single plates on mirrors, 40 single plates on no wall, and 5 plates of 10 faces each, and those 5 are cross walls, the same five (perpendicular to the 5-cell's corner axes) that carry C3's 14 faces each. In every non-centrally-symmetric shape of Table 1, every plate with two or more faces is a wall of the host.
Fix: say so. It rescues half of the first conjecture, plate by plate, and is worth stating as a conjecture (§3 below).

**15. Minor. The skeleton statements. Paper Theorem 5 (e), §6.**
Problem: in the 600-cell, "the fins cover every triangle" restates that each triangle is a face of some copy; the content is the count (each triangle in exactly one B copy and two A copies), which is solid and has a three-line proof. In the 120-cell the radial reading is a construction made to get an answer, and "the A and B fins cover none of the pentagons" needs a word on why B copies, which use all 60 pentagon plates, still miss every pentagon. Not recomputed.
Fix: keep the triangle partition as the result; move the radial coverage to an observation.

**16. Minor. Theorem 5 (a), "exactly 10". Paper §6.**
Problem: the proof cites the compound and checks closure; it does not say why there are no others.
Evidence (recomputed): each corner of the 120-cell has 24 corners at 36°, and they fall into two sets of 12 with no 36° pair between the sets. An inscribed 600-cell through the corner must take one whole set, and each set generates one 600-cell under reflection. So at most 2 pass through each corner, and 2 × 600 / 120 = 10.
Fix: add those two sentences.

**17. Minor. Proposition 9 is stated without proof. Paper §8.**
Problem: "Only the face type {2, 3} has stations" is a completeness claim labelled exact, with no argument in the paper. The status box already sends the cross walls and the station to the next version of #107.
Fix: move Proposition 9 there with its proof; keep here only the station shape of Theorem 7, whose mirror half is automatic (each hexagon lies inside a triangle of the 600-cell) and whose cross-wall half is the content.

**18. Minor. The files disagree with each other.**
Evidence: vicinity README calls the diminished 600-cells "non-heart" (the paper: inherited heart) and defines heart about "the Queens' centre" (the paper: the centre of the corners). Walls README: first table "B: 40 not walls", conclusion "every central plate ... is a 600-cell wall". Construct README: volumes in the order A, C3, B (finding 5).
Fix: a dated correcting line at the top of each README.

**19. Editorial. Nine headline results of unequal weight.** Main theorem, Theorems 2 to 7 and Propositions 8 and 9 mix one restatement (2), one tautology (6), censuses (7, 9) and the real results (5, 4). See §3.

**20. Editorial. The abstract carries more than twenty numbers and three stories.** Lead with the 120-cell result and the wall classes; leave the censuses to the body.

**21. Editorial. Open problem "the roots of the cubic".** It has one real root and a complex pair and is irreducible (table above); the question worth asking is which subsystems of cross walls are free.

**22. Editorial. The stories.** The cat and the steak and Nansen's cat are told from memory with no source read, as the status box says; they belong in the book chapter, where an edition can be cited.

## 3. Restructuring proposal

**Whether §6 should be the main result: yes.** Once the face lemmas are stated, the present Main theorem takes a few lines. §6 is the part that does not follow from classical facts: the counts of copies, the three classes of wall (60, 300, 1200) with how many hosts share each, the exact split of the 1200 triangles by the 120 B copies, and the half-cat patterns. DICTO's idea, hidden in the walls, stays as the frame and the title: Theorem A makes it exact and explains it, Theorem B is where it leads.

**Outline, in dependency order.**

1. *Definitions.* The Vacuus of (X, O); plate, fin; a plate is a full sheet (with each face its opposite), a shared sheet (two or more faces, not closed under the centre) or a single fin; the three kinds read from the plates; the walls W(H) of a host H; hidden in H.
2. *Lemma 1* (as now), with the converse: X is centrally symmetric about O exactly when every plate is a full sheet (the faces determine X).
3. *Proposition 2, the index law* (§4 below). Exact, proof by orbit and stabiliser.
4. *Lemma 3, the face lemmas.* On the 600-cell's corners: edge triangles and golden rectangles lie on mirrors (20 and 30 on each); radius triangles lie on cross walls (8 on each); the 120-cell's pentagons lie on mirrors. Credits: #107 Corollary 2 for the triangles and pentagons; Coxeter's sections.
5. *Theorem A (the silent solids are hidden).* Main theorem (i), (ii) with Theorem 3 (a), (b): A and B have every plate on a wall, share exactly the 10 mirrors of S5 and together carry all 60; C3's 70 faces lie on 5 cross walls. Proof from Lemma 3; the Q(√5) run as the check.
6. *Proposition 4* (the diminished 600-cells; now Proposition 8), a corollary of Lemma 3, with the centre stated.
7. *Theorem B, the main result (the cats in the Red Queen).* Theorem 5 (a), (b), (c) and the triangle partition from (e), with W(H) notation and the statement that A copies are hidden in the 120-cell's own walls. *Proposition 5:* the half-cat patterns (computed).
8. *Theorem C (the chambers).* 298 and 4,291,200; 41,197 and 593,236,800; the two characteristic polynomials; A's 3360 chambers with 120 Coxeter chambers among them; B's 62,880. Exact counts, three methods plus this review's.
9. *The kinds, applied.* Table 1 rebuilt with the stabiliser columns; the stations.
10. *What hidden does and does not show.* The chance baseline, the symmetric-subset baseline, the shapes that fail, the centre dependence of GET.
11. *Conjectures.* (i) In a shape on a Queen's corners that is not centrally symmetric, every shared sheet is a wall of the host. (ii) One choice of ten S5s matched on all 25 shared 24-cells. (iii) The 1200 new walls are the cross walls of the 225 inscribed 24-cells. (iv) The golden station is the only two-ring seed whose Vacuus misses no wall.
12. *Observations only.* The shadows (Table 4, with the one-line proof of the present Theorem 6); the radial skeleton coverage; the uniform-family census; the maximal-subgroup and atlas censuses; the volumes, the core and A ∩ B.

**Cut.** The Galois twin clause; "no chamber is a copy" in every form; the 686 and 17,371 regions (data, no consequence drawn); the split of the grand antiprism's complement (a separate note: it is off this paper's subject); the open problem on the cubic's roots.

**Where things go.**
- *This paper:* items 1 to 12 above.
- *Silent Running:* the test of the other silence sets (30, 60 and 240 points), as one remark and a pointer here; and one cautionary sentence, that all five twisted classes of the 600-cell have every plate on a wall while four are non-heart and one is heart, so the walls do not see the mechanism. The claim of A and B as solids waits there for the full reading of [8].
- *Book chapter "Twisted Walls of Silence":* the submarine on the sea bed, the cat and the steak with its three answers, Nansen's cat and the half-alive cats; the slotted-sheet figures; the shadows as windows on one wall system (Figures 9 and 10); the skeletons; the Hopscotch station as a place on the line between the Queens.
- *#107, next version:* Proposition 9 and the stations, with proof. *#105, next version:* the three kinds and the index law.

## 4. The twist question

**Answer: a third case, and "twist" cannot carry the rule at all.** The runcitruncated 5-cells on the 120-cell's corners are not a removal in the sense of Proposition 8 and not a twist in the sense of Silent Running, where a twist is a twisted class of the group 2I, that is, a set of corners of the 600-cell. On the 600-cell all five S5-orbits are twists, and they are of two kinds (A, −A, B, −B non-heart; C3 heart). So the kind is not decided by how the shape was made. It is decided by the symmetry of each plate.

**The definition that makes the rule exact (index law).** Let G be the symmetry group of X fixing O, f a face and H its plate. Write G_f for the symmetries that keep f and G_H for those that keep H. Then the faces in the orbit of f that lie on H number exactly |G_H| / |G_f|. Proof: g·f lies on H exactly when the plate of g·f is H, that is, when g keeps H; then count by orbit and stabiliser. Hence:
- X is non-heart exactly when G_H = G_f for every face and no two orbits of faces share a plate;
- X is heart exactly when the central inversion is in G;
- otherwise X is inherited heart, and the shared sheets are exactly the plates whose own symmetry is larger than their face's.

This is a restatement by orbit and stabiliser and should be presented as that; its use is that it turns the three kinds into something read off each plate.

Evidence (recomputed; the law held on every plate of every shape tried):

| shape | plates | faces on the plate | \|G_H\| | \|G_f\| of the faces | faces = sum of \|G_H\| / \|G_f\| |
|---|---|---|---|---|---|
| A | 20; 10 | 1; 1 | 6; 12 | 6; 12 | 1; 1 |
| B | 30; 40; 10 | 1; 1; 1 | 4; 6; 12 | 4; 6; 12 | 1; 1; 1 |
| C3 | 5 | 14 | 24 | 4 (six squares), 6 (eight triangles) | 6 + 4 + 4 = 14 |
| runcitruncated 5-cells on the 120-cell | 30; 40; 5 | 1; 1; 10 | 4; 6; 24 | 4; 6; 4 (six) and 6 (four) | 1; 1; 6 + 4 = 10 |
| bitruncated 5-cell on the 120-cell | 10; 10 | 2; 2 | 12; 12 | 12 and 12; 6 | 2; 2 |
| runcitruncated 5-cell, uniform (0, 1, 2, 2, 3) and two generic seeds | 120 | 1 | 4 or 6 | 4 or 6 | 1 |
| expanded 5-cell, generic seed (3.1, 1, 1, 1, 0) | 70 | 1 | 4 or 6 | 4 or 6 | 1 |

**So the open problem of §9 is answered: the runcitruncated 5-cell is inherited heart only at special seeds.** The uniform one and two generic seeds are non-heart, with 120 faces on 120 plates. S5 does not contain the central inversion, so a generic orbit is non-heart, and the kind changes only where a plate gains symmetry: a station, in the paper's word.

**Which station.** In all three shapes with shared sheets under S5, the shared plates are the five planes "coordinate k equals the mean", kept by the 24 permutations of the other four coordinates. A face lies on such a plate only if all its corners have k-th coordinate equal to the mean of the five, so one coordinate of the seed must equal the mean. Checked: C3, (φ, 0, 0, 0, −φ), mean 0; the two runcitruncated orbits of the 120-cell, (0, 0.809, 0.809, 1.118, 1.309) with mean 0.809 and (0, 0.191, 0.5, 0.5, 1.309) with mean 0.5. The orbits that fail it have no shared sheet: A, B, the expanded orbits of the 120-cell (mean 0.862 against 1), the uniform runcitruncated 5-cell (mean 1.6). The corners with that coordinate in place k then form a whole central section, a full slice through the heart made of the shape's own corners: a cuboctahedron for C3. This mean-value condition is necessary for these five plates; whether it is sufficient for every seed pattern is not checked and should be left as a question.

**On the name.** "Inherited heart" was coined for the conjecture that failed (walls inherited from a heart parent). With finding 14 it fits again plate by plate: in every case tested the shared sheets are walls of the host. Whether to keep the one name or to separate "inherited" sheets (on a host wall) from other shared sheets is DICTO's call; no case of the second sort has been found yet.

## Method note

Five short scripts were run as pilots on the compute machine, each under five minutes: hulls and plates by a floating-point hull with facets merged by their hyperplane; walls matched by direction; inscribed 600-cells by closing a corner and one of its two sets of 12 neighbours under reflection; S5 stabilisers by running through the 120 permutations; chamber counts by inserting the walls one at a time and counting, on each new wall, the regions cut by the traces of the earlier ones (inside a Coxeter chamber, and again over the whole space). The whole-space count for the 1560 walls first came out 1184 short (593,235,616) with a point-merging tolerance of 1e-8 and gave 593,236,800 at 1e-11; the in-chamber count was 41,197 at both. The scripts were not committed, as the brief allowed only this file; they are in the review's scratch folder on the compute machine.

DICTO · dictospheres.com
