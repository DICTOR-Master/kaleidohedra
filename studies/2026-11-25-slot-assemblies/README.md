# Slot assemblies of three perpendicular cards: octahedron cut and cube cut (25 Nov 2026)

Purpose: DICTO asked for "a pull apart model like my octahedron one showing the different assembly cuts". His cardboard octahedron
(study 2026-11-24-vacuus-build-renders, build 1) is three SOLID flat square cards in the planes x = 0, y = 0, z = 0, each with its
corners on the two axes in its plane (for z = 0: (+-1, 0, 0), (0, +-1, 0)): the octahedron cut. The cube's Resonus uses the same three
planes, cut as the cube's middle squares (sides along the axes, corners (+-1, +-1, 0), so the shared axis segments are the same): the
cube cut. Any two cards meet along a whole axis segment [-1, 1]. This study lists every way to cut slots so that the three cards can be
put together, proves which ways work and which cannot, and renders four of them whole and pulled apart.
Pass condition (DICTO's real target): every scheme ends PROVED POSSIBLE (with an assembly order), PROVED IMPOSSIBLE (with its exact
scope) or OPEN, for both cuts; pictures he can read at a glance.

STATUS (25 Nov 2026): all schemes settled; exhaustive search FINAL ok at N = 4 and N = 6, identical scheme by scheme (data/compare
in data/slot-search3.job.log); renders and Figure 1(a) done. Awaiting DICTO's look at the two PREVIEW sheets. Not published.

## Results

- Theorem 1, PROVED IMPOSSIBLE: three whole cards can never be put together by sliding, whatever their slots (any number, any
  length, closed or open), both cuts. One card must be cut.
- Theorem 0, PROVED IMPOSSIBLE: with simple half-slots (each from a rim to the centre) three whole cards cannot even be cut out:
  some card falls apart; at least 6 pieces.
- Theorem 2, PROVED POSSIBLE: DICTO's construction (A, B whole, C in two halves C1, C2, slots as on his templates) goes together, both
  forms, and with 4 pieces it is the fewest possible. Variant (a2): one half without a slot (B slotted to the centre on that side).
- Theorem 3 (b), PROVED POSSIBLE: A, B whole and C in four quarters with no slots in C (pure half-slots, 6 pieces).
- Theorem 4 (c), PROVED IMPOSSIBLE (scope: shared segment reaching both rims, as here): a closed central slot locks its two cards.
- Exhaustive search (both cuts, 56 425 schemes each after removing sliver pieces): outcome identical for the octahedron cut and the
  cube cut scheme by scheme; every possible scheme has a one-piece-at-a-time order; no scheme needs a subassembly moved.
- Renders: renders/PREVIEW-slot-assemblies-1-dicto-construction.png (his construction, both forms, whole and pulled apart, labelled
  A, B, C1, C2) and -2-other-schemes.png (whole cards, quarters, closed slot; both forms, pulled apart); single frames renders/*.jpg.
- Figure 1(a) of the Vacuus and Resonus paper v2 redrawn from his Template 2 (renders/fig1a-dicto-octahedron-four-pieces.jpg).

## The model

Names: card X is the plane x = 0 (DICTO's A), Z the plane z = 0 (his B), Y the plane y = 0 (his C, horizontal in the pictures).

Cards have thickness t and a slot has width t, so where two cards cross, the strip along their common axis belongs to one card or
the other (or to neither, a gap); at the centre O all three cards meet and the t x t x t cube there belongs to at most one card.
Every cut therefore lies on a line where two planes meet. Pieces are the connected parts of each card. As t -> 0 the centre is a
point: a card whose parts meet only at O is in several pieces (a neck of width t is not a card).
Moves are straight-line translations (a rigid piece or a rigid group of pieces slides off to infinity without passing through another).

Two facts do all the work (t -> 0, cards P and Q crossing along the line L, each with material on both sides of L along the whole
open segment, as every card piece that crosses L does):

**Lemma 1 (what a crossing allows).** Write a direction of P relative to Q as d = a e_L + b n_P + c n_Q (e_L along L, n_P the normal of
P, n_Q the normal of Q; n_P lies in Q's plane and n_Q in P's plane). Then P can move along d only if
- b = c = 0 (sliding along L), and the parts of L held by P all lie ahead of the parts held by Q in that sense (Lemma 2); or
- c = 0, b != 0 (P leaves along its own normal, inside Q's plane): only if P holds no point of the open segment of L; or
- b = 0, c != 0 (P slides in its own plane across L, along Q's normal): only if Q holds no point of the open segment of L.
If b != 0 and c != 0 the move is blocked: P's material just beside L crosses Q's plane at a point beside L, where Q has material.
Proof: Q's plane meets P only along L. If b != 0 the points of P on L (if any) move off L into Q's plane at once; Q has material
there (Q is only slit on L itself), so P must hold nothing on the open segment; if moreover c != 0, P's material on the side
facing the motion crosses Q's plane beside L as well. If b = 0 and c != 0, P stays in its own plane, and its material on one side of
L sweeps across L, meeting every point of L held by Q. If b = c = 0, P slides along L and only the held parts of L can meet. QED

**Lemma 2 (sliding along a line).** If P slides along L in the sense +, it is free from Q iff no point held by Q lies ahead (in +)
of a point held by P. In particular a closed slot (Q holds both ends of a segment and P a middle part) blocks both senses.

## Theorem 1: three whole cards cannot be put together (PROVED IMPOSSIBLE)

Scope: three rigid cards, each in one piece, any number and placement of slots along the three axes (half-slots, closed slots,
slots past the centre, anything), both cuts and any card outline that holds each axis segment from rim to rim; straight-line moves of
one card or of two cards together; t -> 0 and also any t > 0 with slots of width exactly t (voxel search below).

Proof. With three pieces, the first step of any taking-apart moves one card away from the other two (moving two together is the same
as moving the third the other way). Say card Z (plane z = 0) moves along d = (dx, dy, dz). Z crosses X along the y-axis and Y along
the x-axis, and every card crosses each of its two axes with material on both sides along the whole open segment.
- dz != 0: by Lemma 1 against X (n_Z = z, n_X = x) dx = 0 and Z holds no point of the open y-segment; against Y, dy = 0 and Z
  holds no point of the open x-segment. Then Z is slit along both axes from rim to rim: four pieces meeting at O. Not whole.
- dz = 0, dx != 0: Z slides in its plane across the y-axis along X's normal: X holds no point of the open y-segment, so X is slit
  along the y-axis from rim to rim: two pieces. Not whole.
- dz = 0, dx = 0, dy != 0: in the same way Y holds no point of the open x-segment: Y in two pieces. Not whole.
The same holds for X and Y by symmetry. So no card can leave first, and three whole cards can never be taken apart, nor (running the
moves backwards) put together. QED
Remark: each pair of whole cards alone can be put together (half-slots); it is always the third card that blocks.

## Theorem 0: three whole cards with simple half-slots cannot even be cut (PROVED IMPOSSIBLE)

Scope: "simple half-slots" = on each axis one card is slotted from one rim to the centre and the other card from the other rim to the
centre (the usual way two cards cross). Then each of the six half-axes is slit from rim to centre in one of its two cards. A card slit
along two of its four half-axes falls apart (two adjacent ones cut off a quarter; two opposite ones cut it in two), so a whole card
takes at most one of the six slits, and three whole cards at most three. So with simple half-slots some card is in pieces before any
question of moving: at least 6 pieces in all (a card with k >= 2 of the slits is in k pieces, and the k add to 6). Scheme (b) below is of
this kind (4 + 1 + 1). DICTO's construction (Theorem 2) is not: B's short slots and the halves' slots stop half way, and that is how it
gets by with four pieces.

## Theorem 2 (a): DICTO's construction, four pieces (PROVED POSSIBLE)

DICTO's two card models (photo and Templates 1 and 2 he sent on 25 Nov 2026, file three_planes_models.pdf, kept private): pieces 80 mm
across, slots 1.5 mm wide (the card thickness). Read from the template drawings (vector coordinates, 1 mm = 2.8346 pt): A (plane
x = 0) has one slot, from its lower edge or corner to the centre (40 mm); B (plane z = 0) has a slot from its upper edge or corner to the
centre (40 mm) and two short slots, 20 mm, from its left and right rims along the horizontal midline; C1 and C2 (plane y = 0) are the
two halves of the third square, cut along the line where it meets A (diagonal form: right isosceles triangles, legs 56.6 mm,
hypotenuse 80 mm; axial form: 40 x 80 mm rectangles), each with one 20 mm slot from its straight edge along its midline.
Assembly (his steps): A and B slide together along their centre slots (along y); C1 and C2 slide onto B from either side (along x),
their slots meeting B's short slots, straight edges against A. In the notation here (half-axis = 40 mm = 1): A holds the upper half of
the y-axis and B the lower (half-slots); A holds the whole z-axis (C is cut there, A unslotted there); on each half x-axis B holds the
inner half and the C half the outer half. This is scheme ['Bi', 'Bi', 'A', 'B', 'A', 'A'] of the search (centre to B; the two 40 mm
slots of A and B both end at the centre, so in a real model the 1.5 mm cube at the centre is shared; it affects no move).
Proof: by Lemma 2, A and B slide apart along y (all of A's part of the y-axis lies above B's). Each half C slides along the x-axis
relative to B; its part of the line (the outer half) lies wholly outside B's part (the inner half), so it slides off outward (Lemma 2).
Relative to A each half lies on one side of A's plane and moves parallel to it. So C1, C2 come off along x, then A off B along y; the
reverse is DICTO's assembly. The exhaustive search confirms it; it also finds that A can go on last (B, C1 along +x, C2 along -x, then A down onto B along -y). The same for both
forms: only the outlines differ. It is the smallest possible: no 3-piece scheme exists (Theorem 1), and his has 4.

Variant (a2) (found by the search): one half needs no slot if B is slotted along that half-axis from its corner all the way to the
centre; that half then slides in within its own plane across B's slot, along B's normal (z). For B to stay whole the A-B crossing then
changes: A slotted from the top past the centre to y = -1/2, B slotted from the bottom to y = -1/2. Only one half can go in this way:
slotting B fully on both half x-axes would cut B in two.

## Theorem 3 (b): two whole cards and one card in four (PROVED POSSIBLE)

X and Z as in (a); Y in four quarters (octahedron cut: four right isosceles triangles with legs 1; cube cut: four unit squares), no
slots in Y and no further slots in X or Z. Each quarter lies in an open quarter of the plane y = 0 and drops into its corner along
y, or slides in along its diagonal: nothing crosses its path.

## Theorem 4 (c): a closed central slot (PROVED IMPOSSIBLE where it is used)

A "full-length central slot" through which a whole card passes is impossible here, because both cards reach the rim at both ends of
the shared segment. A central slot as long as the segment cuts its card in two: that is not a slot but scheme (a) again. A shorter,
closed central slot leaves its card holding both ends of the segment while the partner holds the middle: by Lemma 2 they cannot
slide apart along the line in either sense, and by Lemma 1 neither can leave across it (each holds part of the open segment). So the
two pieces are locked; every assembly separates them at some step, so no assembly exists, whatever is done with the third card.
Scope: rigid pieces, straight-line moves, the shared segment reaching both rims (true for both cuts here). The obstruction is gone when
the partner card is narrower along the shared line than the slotted card, as in the three golden rectangles of the icosahedron (a
familiar three-card model, sources below): there the slot can cover the partner's whole width while the slotted card stays whole, and
by Lemma 1 the partner can pass through it along the slotted card's normal. That model is not analysed further here.

## Table

Both cuts give the same row (asserted scheme by scheme); pieces: octahedron cut / cube cut.

| scheme | pieces | octahedron cut pieces | cube cut pieces | outcome | assembly order (insertion) |
|---|---|---|---|---|---|
| W: three whole cards, any slots | 3 | 3 squares | 3 squares | PROVED IMPOSSIBLE (Theorem 1; all 7698 whole-card schemes of the search) | none |
| simple half-slots, all whole | 3 | - | - | PROVED IMPOSSIBLE to cut (Theorem 0) | none |
| (a) DICTO: A, B whole, C in two | 4 | 2 squares + 2 right isosceles triangles | 2 squares + 2 rectangles 1 x 2 | PROVED POSSIBLE | A onto B along their centre slots; C1, C2 onto B from either side along x (or B, C1, C2, then A) |
| (a2) one half unslotted | 4 | as (a) | as (a) | PROVED POSSIBLE | B; C1 along +x; C2 across B's deep slot along z; A down along y |
| (b) C in four quarters | 6 | 2 squares + 4 small right isosceles triangles | 2 squares + 4 unit squares | PROVED POSSIBLE | A and B together; quarters drop into the four corners (along y or a diagonal) |
| (c) closed central slot in A, C in two | 4 | as (a) | as (a) | PROVED IMPOSSIBLE (Theorem 4; all 3096 closed-slot schemes of the search) | none |

Exhaustive counts per cut (pieces per card, sorted: possible / impossible), from data/table-N4.log: (1,1,1) 0 / 7698; (1,1,2) 396 /
13314; (1,1,3) 528 / 4404; (1,2,2) 2166 / 7371; (1,1,4) 114 / 480; (1,2,3) 3000 / 4680; (2,2,2) 1744 / 784; (1,2,4) 498 / 510; (1,3,3)
948 / 720; (2,2,3) 2880 / 528; (1,3,4) 336 / 120; (2,2,4) 417 / 72; (2,3,3) 1572 / 96; (1,4,4) 30 / 0; (2,3,4) 480 / 24; (3,3,3) 304 / 0;
(2,4,4) 36 / 0; (3,3,4) 150 / 0; (3,4,4) 24 / 0; (4,4,4) 1 / 0. Fewest pieces in a possible scheme: 4. The many impossible 4-piece
schemes are slot choices that block (e.g. the halves' parts of the line inside B's), not other cuts.

## Method and checks

- scripts/schemes.py: exhaustive exact search in a voxel model (thickness = slot width = 1 voxel, cards of half-size N voxels,
  outlines |u| + |v| <= N or max(|u|, |v|) <= N). Every shared voxel goes to one card or to none: per half-axis 'A', 'B', 'Ai', 'Bi'
  (one card the inner half, the other the outer half) or '-', and the centre to X, Y, Z or none: 5^6 x 4 = 62500 schemes per cut;
  schemes with a sliver piece (only centre or line voxels) are left out. Moves: the 26 directions in {-1, 0, 1}^3, with the exact sweep
  test for a unit cube moved along d: it meets the cell at offset delta iff delta_i = 0 where d_i = 0, and m_i = delta_i d_i satisfy
  min m >= 0 and max m - min m <= 1. By Lemma 1 the free directions of any piece form unions of open cones of the coordinate fan, so
  one sign vector per cone (the 26) suffices. Taking apart: one piece at a time (greedy, complete), and where that fails the full
  two-handed search (any group of pieces moved as one) before IMPOSSIBLE is written.
- Resolution check: the same 62500 schemes at N = 4 and N = 6 give the same pieces and the same outcome (scripts/compare.py).
- Both cuts give the same outcome scheme by scheme (asserted): only the shapes of the pieces differ (triangles against rectangles).
- scripts/renders.py: the four rendered schemes are drawn from the same slot data, their pieces per card asserted against the search;
  pulled views checked in the drawn picture (projected convex hulls of the pieces pairwise apart by at least 1.5 % of the frame).
- House renderer render3d.py (study 2026-11-21-scutoid-stand-in) and its shots.mjs; scripts/compose.py makes the two sheets.
- Run as logged background jobs on the compute host (jobs slot-pilot, slot-search3, slot-renders). Logs in data/. The full results are
  data/schemes-N4.json.gz and schemes-N6.json.gz (gunzip before rerunning renders.py, table.py or compare.py).
- Two runs were stopped and redone (kept here as a record of the method, not of the result): the first full run let a card hang
  together only through the centre cube (a neck of width t), which made 24 'whole-card' schemes look possible; the centre now never
  joins two parts of a card (as t -> 0 it is a point), and it is given to the part with the least voxel, so both cuts are treated alike.

## Sources checked (prior art)

- DICTO's private geometry reference library (manifests and notes): no entry on slotted card models.
- Web (25 Nov 2026): Wolfram Demonstrations "Three Interpenetrating Golden Bricks"; Matematicas Visuales "The golden rectangle and the
  icosahedron" (cardboard template of three golden rectangles); cutoutfoldup.com "805 icosahedron from three golden rectangles";
  George Hart, "Slide-togethers" (georgehart.com; slotted card construction practice); Wikipedia "Golden rectangle" (three
  perpendicular golden rectangles, Borromean pattern); NRICH 5480 (slotted paper octahedron); makerworld "Interlocking impossible
  rectangles"; Tes "Slice action" (sliceforms).
- Found: slotting flat cards together is standard model-making practice (slide-togethers, sliceforms), and three perpendicular golden
  rectangles is a familiar three-card model. Not found: any statement of Theorem 1 (three whole cards cannot be put together) or
  Theorem 0, or a list of the schemes; the slot instructions of the golden-rectangle models were not reached. So: method standard,
  credited above; the theorems here are stated as ours with this list of sources checked, not as new to the world.

## Home

The Vacuus and Resonus paper, next version (#v2 draft, §2.3 and Figure 1a, done 25 Nov as asked: four pieces, one sentence that the
cut is needed, this study cited). The full scheme list and the impossibility proofs are a short note if DICTO wants them in print
(Theorems 0, 1, 4 with the table); his templates could go in as a figure with his credit.

## LEADS

1. DICTO: say whether Theorems 0/1 and the table go into the v2 paper (an appendix) or a short note of their own.
2. The golden-rectangle model (icosahedron): there the cards are narrower along the shared lines, so closed slots are allowed; the same
   exhaustive search can classify its schemes (the search takes any outlines; only the region function changes).
3. Rotations: Theorem 1 is for straight-line moves; whether a twisting motion could put three whole rigid cards together is OPEN
   (blocker: Lemma 1 is first-order for translations only).
4. Real cards bend: the study is for rigid cards; flexible card can be sprung into place, outside this scope.
