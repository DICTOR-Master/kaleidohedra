# Independent attack on "Scutoids in Four Dimensions" (draft of 10 Nov 2026, 22:40 version)

Referee: Claude (Fable), adversarial pass after the four-reviewer panel. I read paper.html, the panel files and judgement, the four study
READMEs, every script named in the brief, the filed logs (flips61.log, cells2/*.txt, the bitruncated JSON) and #61's own text, and ran two
small independent power-diagram checks (scipy, this machine; scripts in my scratchpad, nothing written into the studies).

What I verified and found RIGHT (so the fixes below are about wording, scope and one figure, not the mathematics):
- h-vectors from face numbers, with f_k = sum_i h_i C(i,k): 120-cell (1,116,366,116,1), truncated 120-cell (1,716,966,716,1), bitruncated
  600-cell (1,716,2166,716,1), checked also against f_1 and f_2 (e.g. 7200 edges, 4320 faces for the bitruncated). The three random
  polytopes, the 4D/5D permutohedra and the 5-cube likewise.
- Theorem 4's bookkeeping: 720 - 118 - 1 = 601 (start corner, 118 R births, swaps); the W-W triangles 1200 = 601 + 598 + 1; mixed = 964;
  the hexagons too (4 + 2*716 + 964 = 2400). The proof is general: for any simple 4-polytope 2-coloured with 2 + 2 at every corner,
  #(W-W -> R-R) = #(R-R -> W-W) = (R-R faces) - (R cells) + 1.
- Cell-first "1782 each": summed from the filed JSON (1782 lost, 1782 gained).
- Theorem 3's closed forms: continuous at -(4-s)/24 (both roles), vanishing at -5s/8, equal to the s = 1/5 pilot polynomials, and the
  cells2 logs print them as rational identities; walls at s = 1/5 are -9/40, -19/120, -1/8, -1/40 as stated.
- The wall exchange counts in the paper match flips61.log (but see point 11: they are double counts).

## Numbered points, most serious first

### 1. "The same move one dimension up" is not what Section 1 shows (serious; false as written, in the title's own terms)
Quote: "Here the same move appears one dimension up." / title "Scutoids in Four Dimensions" / "every simple 4-polytope is a scutoid build".
Problem: in Section 1 the scutoids are the CELLS of the 4-polytope, which are 3-dimensional; their sections are 2-dimensional polygons
tiling the slice's boundary surface; the move is the 2-2 flip of a 2D tiling. That is exactly the 2018 setting (3D cells, 2D sections,
T1 move) with the tissue curved into the 3-sphere that bounds a 4-polytope. Nothing in Section 1 is "one dimension up"; only Section 3
(4D cells over lambda, 3D sections) is, and there the move is a different one (point 2). The paper currently calls both "the same move".
Fix: say what is true and still striking: "the facets of a simple 4-polytope, swept by a hyperplane, are scutoids in the 2018 sense:
flat-faced cells whose polygon sections exchange neighbours; the polytope's boundary is a closed scutoid tissue, and h_2 counts its
moves." Keep the title only if Section 3's object is what it refers to, and say so in the first paragraph; otherwise "Scutoids on the
4-polytope" / "Scutoid tissues in four dimensions" is accurate.

### 2. The #61 walls are NOT the simple scutoid swap of Theorem 1; by the paper's own Theorem 1' they cannot be (serious; overclaim)
Quote: subtitle "the Swap Rule of close packing, whose walls are those swaps"; "find the same move at the walls of the Swap Rule";
"Each wall is a swap"; "The symmetry of the lattice makes the swaps come in batches, as in a symmetric sweep of Theorem 1."
Problem: the lambda-stack of 3D power diagrams is a 4D cell complex whose 3D slices are 3D tilings. Theorem 1' (the d = 5 case, and the
same local argument for a simple 4D tiling, 5 cells per corner) says a simple corner either GAINS one contact (index 2) or LOSES one
(index 3), never both. A one-for-one exchange at a single point is therefore a non-simple (degenerate) corner. I checked this directly:
at s = 1/5, word ACABC, wall -5s/8, every lost oct(k)-oct(k+2) contact and its partner gained tetX(k+1)-tetY(k+1) contact have the SAME
six sites in their stars (4 tetrahedra before, 4 after): the degenerate 4-4 flip, six cells meeting at the exchange point; the four
exchanging sites are exactly coplanar (det = 0) with a common midpoint (central symmetry). At -(4-s)/24 the same, with 6-9 sites. This
is the analogue of the truncated 600-cell's clumped moves, not of the bitruncated 600-cell's pure swaps. In the 2D cut of Figure 3
(the plane of those four coplanar sites) it IS a 2-2 flip: that is the correct, and still nice, statement.
Fix: replace "the same move" by: "in the 3D tiling the generic moves are gain-only and loss-only (Theorem 1', d = 5; the 3D foam T1);
at the walls the lattice's central symmetry forces the loss and the gain onto one point (a 4-4 flip, six cells meeting; the four
exchanging holes are coplanar), and in that plane the exchange is the scutoid's 2-2 flip." Change the subtitle accordingly.

### 3. Theorem 1' is false as written in its first clause, and "moves" is wrong for d >= 6 (serious; false as written)
Quote: "for 2 <= i <= d - 2 the facets containing all the corner's downward edges stop touching in pairs and those containing all its
upward edges start: a pair stops touching iff ... (i = d - 2), a pair starts iff they all go up (i = 2)." and "The numbers of these moves
are h_1, ..., h_{d-1}."
Problem: for d = 5, i = 2, the three facets containing both down edges do NOT stop touching (their ridges still carry an up edge); only
the gain happens. For d >= 6 and 3 <= i <= d - 3 NO facet contact changes at all (no ridge has the corner as top or bottom), so h_3 of a
6-polytope counts corners at which the facet tiling's contact graph does not move. The box contradicts its own iff clause, and the
proof (correct) proves only the iff clause.
Fix: state it through the dual move. At a simple corner the k-faces correspond to k-subsets of its d edges; a face has the corner as top
iff all its edges go down. Passing an index-i corner is the bistellar i -> (d - i) move on the dual triangulation of the slice's
boundary (i top simplices below, d - i above). Facet contacts change only at i = 1 (facet born, d - 1 contacts), i = 2 (one contact
gained), i = d - 2 (one lost), i = d - 1 (facet dies); d = 4 makes 2 and d - 2 coincide (the swap); for d >= 6 the middle indices move
lower faces only. The number of index-i corners is h_i.

### 4. Figure 3's caption contradicts Figure 2 and describes a section artefact as a contact change (serious; false as written)
Quote (Fig. 3): "At the wall the gold cell gains two green neighbours (red: the new contacts)". Quote (Fig. 2, same hole, same wall):
"17 faces before, 14 after" and "Gold: faces towards octahedral holes two layers away; they end at the wall".
Problem: in 3D, at -5s/8, flips61.log shows only oct-oct (two layers apart) lost and tetX-tetY gained; no oct-tet contact is gained
anywhere. The gold cell's faces to the green tetrahedral holes of its own gap exist on both sides of the wall; at the wall they reach
the cut plane and so appear in the section. The real 3D event in that picture is the two BLUE cells (octahedral holes one layer below
and one above the gold one, two layers apart) ceasing to touch, and a tet-tet face opening off the cut. The gold cell is one of the
six cells at the point and is a bystander.
Fix: recaption: "At the wall the two blue cells (octahedral holes two layers apart) stop touching; the tetrahedral holes of the gold
cell's gap start touching (off this cut); the gold cell's faces to the green cells, present throughout, enter the cut here." Keep the
figure; it is a good picture of the symmetry plane once the caption is right.

### 5. Theorem 3's box claims more than its proof: locality is a hypothesis, the range is undefined, "key" is undefined (serious; gap)
Quote: "For every s in [1/8, 1/4], along #61's range of lambda, the Swap defect D ... of each piece, with the outer layers held fixed, is
the same for all four outer contexts and equals ..."; later "for every stacking the result needs that a piece depends only on the four
layers round its gap (no clash between words was found; not proved)".
Problem: the box is stated for pieces of any stacking (that is what V(t|t') with outer contexts means), but what is proved is the
statement for the six words ABC, AC, ACBC, ACABC, ACBCAC, ACBABC. For a general stacking even V(t|t') is undefined without locality.
"#61's range" is never given (it is -1/4 - s/8 <= lambda <= 3s/8 for s <= 1/4, since U(s) = min(1/3 + s/24, 3s/8) = 3s/8 there).
"four-layer keys" / "outer contexts" are undefined: the key is the TYPES (c/h) of the four layers round the gap, two below and two
above, i.e. six letters; the outer context is the types of the outer two. "(the outer layers held fixed below)" is garbled.
Fix: in the box: "in the six stackings ..., and in every stacking whose pieces are fixed by the types of the four layers round the gap";
give the range explicitly; define key and context in the setup paragraph in one sentence each.

### 6. The neighbourhood step is not exact, and its evidence is not filed (serious; gap in a proof called exact)
Quote: "on every cell the farthest corner lies within rho <= 0.55 of its site ... (rho measured on a 9 x 9 grid of each cell, with a 5%
margin)" and "the cells were built from all sites within squared distance 24".
Problem: a grid maximum with a 5% margin is a numerical estimate inside an otherwise exact proof. Also the study folder's cells2 logs are
from the earlier script version (D^2 = 12, no "neighbourhood:" line); the D^2 = 24 run exists only as a README sentence.
Fix (exact, two lines): any point x of cell i satisfies |x - p_i|^2 - w_i <= |x - p_k|^2 - w_k for the nearest site k; the octahedral
holes of each gap alone form a triangular lattice of spacing 1 (covering radius 1/sqrt3 in-plane, vertical offset <= d/2, d^2 <= 1/6), so
|x - p_k|^2 <= 1/3 + 1/24 = 3/8, hence rho^2 <= 3/8 + 0.29 < 0.67, rho < 0.82, and (sqrt24 - 0.82)^2 - 0.82^2 > 15.9 > 0.29 >= |w_j - w_i|.
No grid, valid on the whole range. And file the D^2 = 24 logs in data/ (or drop the 0.55 claim).

### 7. The "cut the corners back" remark is false for the truncated 600-cell itself (serious as a statement; minor to fix)
Quote: "cutting such corners slightly back makes the polytope simple and splits each clump."
Problem: at a corner of the truncated 600-cell the vertex figure is a pentagonal pyramid; its apex corresponds to the edge lying in
five truncated tetrahedra. Truncating the corner puts a new vertex on that edge in 5 + 1 = 6 cells: still not simple. One truncation
simplifies a corner only if its vertex figure is simplicial.
Fix: "a generic small shift of the facet hyperplanes makes any polytope simple and splits each clump" (standard), or truncate corners,
then edges, etc.

### 8. "No pure swap" can be a theorem, not a five-direction observation (minor; strengthening, ready to use)
Quote: "in the five directions tested its moves are clumped and no pure swap occurs."
A pure swap at a corner needs the vertex-figure graph split into down/up vertex sets with exactly one edge inside each (one ridge with
the corner as top, one as bottom) and no face wholly on one side. The pentagonal pyramid's graph is the wheel W_5 (10 edges); its
largest cut is 7 (hub with two non-adjacent rim vertices), so at least three edges stay inside: at least three contacts change at
every corner of the truncated 600-cell, in every direction. State it as a lemma; the table row then needs no hedge.

### 9. Credit: the scutoid-T1-flip identification is not the paper's (credit; serious for the status box)
Quote (status box): "Ours: the identification of the scutoid's neighbour exchange with the 2-2 flip (so h_2 counts scutoid moves)".
Problem: the 2018 paper itself compares the apico-basal change to the T1 transition, and T1 = the 2-2 (Delaunay/edge) flip of the dual
triangulation is textbook foam physics; the 3D T1 (an edge shrinking to a point and opening into a triangular face, and the reverse) is
exactly Theorem 1' for d = 5 and the generic move of Section 2/3. What is the paper's: reading the index-2 corners of a simple
4-polytope sweep as scutoid moves and h_2 as their count; the balance law; the #61 walls and their chamber map; the name.
Sources to check and cite (do not cite unseen): Weaire and Rivier, "Soap, cells and statistics" (Contemp. Phys. 1984); Weaire and
Hutzler, The Physics of Foams (1999), 3D T1; Lickorish, "Simplicial moves on complexes and manifolds" (Geom. Topol. Monogr. 2, 1999):
bistellar moves as what a level set does at a critical point, the mechanism of Theorem 1'; Edelsbrunner and Shah, "Incremental
topological flipping works for regular triangulations" (Algorithmica 1996) and Gelfand-Kapranov-Zelevinsky's secondary fan: a weight
walk of a power diagram crosses walls by flips, the 4-4 flip being the degenerate case; Aurenhammer, "Power diagrams" (SIAM J. Comput.
1987). Verify the 2018 paper's exact term ("apico-basal transition" vs "apico-basal intercalation").
Fix: rewrite the "Ours" sentence as above; add the sources that check out.

### 10. "Reviewed by a panel of four" reads as human peer review (honesty; serious in public text)
Quote: "Reviewed by a panel of four (polytope combinatorics, computational geometry, scutoid biophysics, a hostile referee) before this
version."
Problem: the panel was four automated referee passes of a language model. A reader will take this for human review.
Fix: "Checked before this version by four automated referee passes and one independent attack (reports kept with the paper)", or drop.

### 11. The wall exchange counts are double counts (minor; wrong numbers)
Quote: "114 contacts between octahedral holes in one layer are exchanged for 114 ...; at -5s/8, 42 ... for 42 ...; at -s/8, 252 for 252".
Problem: flips61.py counts every shared face once from each of its two cells (the log's 21 + 21 for one set of oct-oct faces, keyed
(0,+2) and (-2,0), shows it). The faces are 57 <-> 57, 21 <-> 21, 126 <-> 126, and at -9s/8 31 lost / 173 gained, all summed over the
six words' unit cells (the numbers depend on the chosen words, not on the lattice).
Fix: halve the numbers and say "faces, summed over the six words' unit cells".

### 12. "Exact sweeps" are floating-point sweeps (minor; wording)
Quote: "sweeping each polytope exactly along a generic direction"; status box "confirmed by exact sweeps".
Problem: t600_scutoid.py and sweep5d.py use float coordinates (sqrt5) and merge heights rounded to 1e-9. The integer counts are robust,
but "exact" means rational arithmetic in this paper's other sections.
Fix: "by computer (floating point, heights merged at 1e-9)".

### 13. Theorem 4's opening claim is loose (minor; unclear)
Quote: "The bitruncated 600-cell is the one polytope on the path where both Queens' cells meet".
Problem: every stage between the Queens has 120 + 600 cells; the truncated 600-cell has 600 truncated tetrahedra too. The mathematical
hypothesis is "simple, with 2 W + 2 R at every corner", and that is what the proof uses.
Fix: state the hypothesis in the box and keep "where the Queens communicate" in DICTO's reading. Add the general one-line law
(R-R faces - R cells + 1) since the proof is general.

### 14. The "4D scutoid" definition does not match its own example (minor; unclear)
Quote: "a 4-cell whose 3D slices exchange neighbours along one direction".
Problem: a single cell loses or gains (Figure 2's cell loses three faces and gains none); the exchange is between two pairs of cells.
Fix: "a 4-cell whose 3D slices change neighbours at a wall where two cells stop touching and two others start".

### 15. Small gaps and loose ends (minor)
- Theorem 1 proof, "nothing else": say in one line that at a simple corner the faces correspond to subsets of its edges, so the only
  faces with the corner as top are those spanned by down edges (one ridge for i = 2, no cell). The "at most one 2-face" step is fine.
- Section 3: the stacked cell is a polytope only with lambda_a <= lambda <= lambda_b; say so.
- Figure 1's bottom line "lines through them fitted" is outdated: the walls are now the proved cell boundaries for all s in [1/8, 1/4].
- swap_cells2.nonneg_on: an even-multiplicity root of a denominator inside [s_a, s_b] would pass silently (a corner escaping to
  infinity = a degeneracy in s). Add "denominator has no root in the interval" to the fallback; the Bernstein path already has it.
- sweep5d.py's comment "two facets sharing >= d - 1 corners share a ridge" is false in general for d >= 5 (four coplanar corners); it
  happens to hold for the 5-cube and permutohedra used. Not in the paper; note it in the README.
- "the 600-cell (the White Queen) to the 120-cell (the Red Queen)" is fine; but "DICTO's reading" of the channel should stay outside the
  theorem box (it is).

## Verdict
Must change before release: points 1-7 and 9-11 (framing of dimension; the walls are degenerate 4-4 exchanges, the 2-2 flip only in the
symmetry plane; Theorem 1' restated via the i -> (d - i) move; Figure 3 caption; Theorem 3 box with the locality hypothesis, the explicit
range and definitions; the exact neighbourhood bound and the filed D^2 = 24 logs; the false truncation remark; the "Ours" sentence and
the review-panel sentence; halved wall counts). Point 8 is a free strengthening.
The core results stand: Theorem 1 (classical, correctly credited once point 9 is fixed) with its scutoid reading; Theorem 2's counts;
Theorem 4's balance law (proved, general); Theorem 3's closed forms and chamber map for the six words on the whole s-range, with locality
as a stated hypothesis for other stackings. Section 3's 4D cells are real; what they do at the walls is a symmetric 4-4 exchange, which
the paper should say and can still draw as a scutoid in the plane of the four coplanar holes.
