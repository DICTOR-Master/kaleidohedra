# Amber keyed (21 Nov 2026)

DICTO's question: can the Fullerene-Amber Cell (the Fullerene Star, a truncated icosahedron with a regular-dodecahedron centre pyramid on
each pentagon, set in its resin inside a space-filling mould) be KEYED, so that it carries "changing orders in shells and in outward
translations"? Idea and names (Fullerene Star, Fullerene-Amber Cell): DICTO's. A and B are working labels.

## The hidden letter

I_h ∩ O_h = T_h, so inside a cubic mould the Fullerene Star stands in exactly two ways: A (its T_h axes on the cube axes, the setting of
the resin and amber-sweep studies) and B = R(A), R the quarter turn about a cube axis. The mould is O_h-symmetric, so cell B is cell A
turned by R: each cell carries one binary letter, invisible from its outline. The only way the letter can show is through the pattern
the resin pieces make on the mould faces. Two cells across a face key together when their pieces meet face to face there: the top
facets from the two sides coincide exactly.

## Theorem (the verdict)

For both division rules (DICTO's combined method, and the central division R1), in all three cubic moulds and at both scales tested
(s0 and 6/5 s0), the face-to-face rules are:

| mould (lattice) | face type | A\|A, B\|B | A\|B | allowed letter configurations |
|---|---|---|---|---|
| rhombic dodecahedron (fcc) | 12 rhombi | no | yes | (d) none: neighbours must always differ, and the fcc neighbour graph has triangles |
| truncated octahedron (bcc), including the Fullerene-Amber Cell itself (6/5 s0) | 6 squares | yes | no | (d) none: no pair matches on the hexagons |
| | 8 hexagons | no | no | |
| cube (sc) | 6 squares | yes | no | (b) exactly two, all-A and all-B; both periodic |

So no configuration is forced aperiodic, and none can be: under these face rules the letter forbids every stacking in the fcc and bcc
moulds, and in the cube mould it allows only one orientation throughout. The answer to "keyed to serve the aims" is no, for every division
whose face patterns keep exactly T_h (both rules here do).

Scope, exactly: the Fullerene Star C1 (edge 1); moulds = Voronoi cells of sc, bcc, fcc at s0 and 6/5 s0; division rules comb (centroid
seeds, as in branch E and the amber sweep) and R1 (as in branch D); face-to-face = equal sets of top polygons on the shared mould face,
exact in Q(√5); rules between nearest cells only (cells that share a face). Not covered: other seeds or division rules whose face
patterns have extra symmetry (see "Why", the last paragraph), and keys beyond the orientation letter (bumps, markings).

## Why (exact, and independent of the division rule)

Write P for the pattern of cell A on its mould face with outward normal direction v (the neighbour sits at v; v = 2c n/|n|²). T_h
contains the central inversion, so cell A's opposite face carries −P, and the neighbour's copy, moved by v, is v − P: the half-turn of P
about the face centre inside the face. Cell B's opposite face carries −k(P) for some k in the O_h face stabiliser but not in T_h, so A|B
compares P with v − k(P). With S_T and S_O the face stabilisers in T_h and O_h:

- Rhombus (fcc): S_T = {1, mirror in the long diagonal}. A|A needs the in-plane half-turn, which is not in S_T, so it fails. For A|B,
  k = the half-turn about v, and v − k(P) = P: A|B ALWAYS matches, whatever the division.
- Square (bcc, sc): S_T = C2v contains the half-turn, so A|A always matches; A|B needs the quarter turn, which is not in S_T, so it fails.
- Hexagon (bcc): S_T = C3. A|A needs the half-turn (C6), A|B needs the mirrors at right angles to the cubic ones; neither is in S_T,
  so both fail.

The computed in-plane symmetry of every face pattern is exactly its T_h stabiliser (rhombus 2 of 4, square 4 of 8, hexagon 3 of 6, in
every run), so the generic case holds, and the computed match table equals the table predicted above in all 12 runs. Escaping it needs a
face pattern with symmetry beyond T_h. That changes a rule only into "all pairs", "equal" or "unequal", never into anything that can force
aperiodicity (next section).

## The subshift, decided exactly

Every rule depends only on the face crossed and is symmetric under A↔B (turn the whole configuration by R), so each face class allows
all pairs, equal letters only, unequal letters only, or nothing. A configuration is then a 2-colouring of the lattice with equal or
unequal constraints along the constrained directions. Claim: if one exists on the infinite lattice, a periodic one exists. Proof: the
sign of a path depends only on its displacement, so the constraints define a character χ: L' → {±1} on the sublattice L' spanned by the
constrained directions. Take bases with L' = ⊕ d_i Z e_i (Smith normal form) and set c(Σ a_i e_i) = Π ε_i^⌊a_i/d_i⌋, with ε_i = χ(d_i e_i).
Then c obeys every constraint and has periods 2 d_i e_i. In these lattices every face class spans a sublattice of index 1 or 2, so the
torus Λ/4Λ decides existence exactly. When some class is constrained, the solution set is finite (every T_h face orbit spans R³), so
all its members are periodic. Free (uncountably many configurations, aperiodic ones allowed but not forced) happens only when every
class allows all pairs. So (c), forced aperiodic, cannot occur for any keying by the orientation letter alone. This is the 1D
obstruction of aim 3 again, now in 3D: one letter per cell with pair rules is too weak to force anything.

Check (scripts/subshift.py, logs/subshift.log, ends FINAL ok): all 4 + 16 + 4 rule tables for sc, bcc, fcc on tori N = 2..6. The SAT
solver (Glucose3) and an independent parity union-find count agree on every table and every N (0 disagreements). The real tables of the
12 runs are classified as in the theorem table.

## Shells, layer by layer

Only the cube mould allows a face-to-face configuration (all-A, or all-B, which is the same lattice turned).

1. Core: the Fullerene Star, icosahedral (I_h, 120 symmetries): 20 hexagons, 60 spike triangles.
2. Resin transition: 80 pieces, one per face of the core; the symmetry drops to T_h (24) and the pieces fall into the five T_h face
   orbits (hexagons 8 + 12, triangles 24 + 24 + 12). With the combined method every piece is a scutoid (sc s0: 80/80, 24 Y vertices):
   at the 30 hexagon-hexagon edges the two spike triangles beside the edge meet across it on the mould. R1 gives frusta, no scutoids.
3. Mould surface: the cube, O_h as a shape, but the pattern on each face (22 top facets, both rules, both scales) keeps only C2v, 4 of
   the square's 8 symmetries.
4. Outward translations: the simple cubic lattice with T_h at every point (space group Pm-3); the order is the same in every cell.

Do neighbouring transition layers join into larger shells? Across every cube face the 22 top facets from the two sides coincide, so the
pieces pair off into double pieces that bridge two cores. The resin of all the cells is one connected periodic region (the complement of
the cores), not a nested shell: just outside one cell's mould lie its neighbours' resin layers and then their cores. The order along
the translations never changes (one letter throughout), so the chain icosahedral → tetrahedral-cubic → cubic happens once, inside each
cell, and the lattice repeats it.

In the rhombic-dodecahedron and truncated-octahedron moulds, every letter configuration still tiles space (the cells tile; each cell is
partitioned exactly, as the earlier studies proved), but not face to face across the mould faces. Across every rhombus between equal
letters, and across every hexagon for every pair, the top facets disagree.

## Controls

- Each face pattern is an exact partition of its mould face (area vectors add up exactly in Q(√5)); every run.
- Each pattern is invariant under its T_h face stabiliser (asserted, every face, every run).
- Single-orientation lattice: face to face in the cube mould (A|A on all 6 squares). In the rhombic dodecahedron (rhombi) and the
  truncated octahedron (hexagons) the single orientation is NOT face to face. The symmetry proof above forces this for any division
  that keeps exactly T_h, so the result is not a fault of the method.
- A deliberately mismatched pair is rejected: the matching pair with one vertex moved by 1/1000 in the face (every run). The 6/5 s0
  combined pattern scaled by 5/6 against the s0 pattern: 0 matching faces. R1 against the combined method on the same mould: 0. Exact
  positive identity: R1 is a central projection, so its 6/5 s0 pattern scaled by 5/6 equals its s0 pattern on every face (accepted).

## Files

- scripts/keyed.py LATTICE FACTOR: face patterns (comb and R1) for A and B, the match table, the pattern symmetries, controls;
  data/keyed_<lat>_<fac>.json (match table per face, A polygons exact, pieces per face); logs/keyed_*.log. It imports amber.py and
  solids.py from ../2026-11-21-amber-cell-sweep and resin.py from ../2026-11-21-scutoid-stand-in (unchanged).
- scripts/subshift.py: every rule table on tori, SAT plus union-find, the real tables, the mismatch controls; logs/subshift.log (FINAL ok).
- All runs were short foreground jobs on the compute host (each under 3 s), so no long job and no plan file were needed.

LEADS
1. A key that can carry order outward needs more than one letter per cell with pair rules. Options: face patterns that see a second
   neighbour, or a marking that is not the orientation (bumps on the mould faces), as in the aim 3 notes. Either restarts keying,
   which is paused unless DICTO brings a hopeful piece; this study says the Fullerene-Amber Cell is not that piece.
2. The only face-to-face Fullerene-Amber stacking is cubic (Pm-3). In the truncated-octahedron mould of the Fullerene-Amber Cell
   itself, a face-to-face lattice needs hexagon face patterns with C6 symmetry (then only one orientation throughout) or with the
   cubic mirrors (then the two cubic sublattices alternate); neither rule tested gives one, as the T_h symmetry argument predicts.
