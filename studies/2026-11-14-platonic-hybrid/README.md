# The hybrid: one golden slab for the Platonic mixes (14 Nov 2026) - DICTO · dictospheres.com

**Verdict (14 Nov 2026): every tested claim of the hybrid (handoff section B: B2, B3, B4 a-d, B5) is CONFIRMED, exactly in Q(sqrt5) and by exact random-point covering; all five Platonic solids of edge 1 fill space in 3 slabs with the 5 connectors A, cap, S, R, Z (against #47's 4 slabs and 6), and D + I with A, cap, S and no slab faces. B6 (other edgings need two kinds) was not tested: UNDECIDED.**

Proposed in DICTO's working session of 13-14 November 2026 (source: studies/2026-11-14-chat-handoff, 03-session-addendum.md,
section B, marked "derived; to test"); checked here against #47 (Every Mix of the Platonic Solids Fills Space, v3, DICTO DOI
10.5281/zenodo.23551326) and #106 (One World for the Platonic Solids, DICTO DOI 10.5281/zenodo.24126400). Written into
Space-Fillers and Lattice Moves, Chapter 8, section 6 (Propositions 8.1-8.3, Theorem 8.3, Corollary 8.4, Table 8.2, Figure 8.5).

## Verdict per claim

| claim | verdict | how |
|---|---|---|
| B2: the icosahedron of edge 1 with its skin (6 Admiral Caps + 8 caps) is exactly the dodecahedral cell of edge 1 | CONFIRMED | exact: octahedron corners = the 6 ridge midpoints (E5), octahedron inside the dodecahedron (E6), ico + 6 A + 8 caps = dodecahedron by exact volumes (E8); caps convex, images of one under the sign changes, (27 + 13 sqrt5)/96 each |
| B2: it can stand wherever a dodecahedron stands in #47's slab; large octet and Q' not needed; worlds 4 -> 3 | CONFIRMED | exact covering, 60 000 points: golden slab with X/Y and mixed cells, 0 bad, 0 ties |
| B3: octet cut on its triangle planes removes P for every mix with T and O (P still for T without O, Q for O without T) | CONFIRMED | Theorem 2 of #47 (Theorem 8.2 of the book); exact covering of one layer, 60 000 points, whole T and O |
| B4(a): all roofs and hollows on the slab face have parallel ridges | CONFIRMED | exact over 49 columns (all along y); note: Z is one shape under a quarter turn, so (a) is not needed for the count |
| B4(b): roof height exactly 1/2 | CONFIRMED | phi^2/2 - phi/2 = 1/2 (exact) |
| B4(c): Z volume phi^2/2 - (7 + 3 sqrt5)/24 | CONFIRMED | = (11 + 3 sqrt5)/24 ~ 0.73784 (exact) |
| B4(d): columns Z (over a cell) and R + Z + R (over a Dogstar) make the face flat | CONFIRMED | exact covering, 60 000 points, mixed cells and icosahedra-only cells, 0 bad; slab thickness phi + 1 = phi^2 |
| random-point test of the stack (as mixes3.py) | CONFIRMED | float, 40 000 points through golden slab R/Z + cube slab + octet layer on triangle planes, 0 bad; pieces exactly D I C T O A cap S R Z |
| controls | as expected | + #47 Lemma 5 slab (exact) and #47's mixes3.py from its file (31/31 mixes); - quarter-turned plate (218/4992 bad), no R in hollows (163), X/Y swapped (819), skin without caps (646), float stack with turned plate (959) |
| B5: all five, counts 6 / 5 / 5 / 5 for published / triangle-plane octet / hybrid / hybrid with partial skins; worlds 4 / 4 / 3 / 3 | CONFIRMED | by construction (hybrid.py, K lines) |
| B5: D + I with A, cap, S (3), no edging, against A, Q', S, X, Y (5) | CONFIRMED | exact covering of the 3D golden tiling with mixed cells, 60 000 points, 0 bad |
| B5: I alone: the old slab is cheaper (A, Q') | CONFIRMED (count) | hybrid gives A, cap, S |
| B6: other edgings tried need two kinds; C, T, O skins at edge 1 need about eight kinds | UNDECIDED | not tested; listed as open in the book |
| B7 (why X, Y appear in #106 Table 2) | not addressed | outside this check |

Side result: over all 31 mixes the kit stays at seven (P, Q, A, cap, S, R, Z with the hybrid; #47: P, Q, Q', A, S, X, Y); the
per-mix connector sets of the four constructions are the K lines of data/hybrid-full.log.

## Files
- scripts/golden.py: exact field Q(sqrt5), exact hulls and volumes, the solids in the cell frame, Admiral Caps (2 tetrahedra each), the 8 caps, integer half-spaces for exact point tests.
- scripts/hybrid.py: all checks (E exact facts, exact covering with controls, float stack, #47's mixes3.py control, counts). Logs: data/hybrid-pilot.log (pilot, 600 points), data/hybrid-full.log (60 000 points per configuration, 12 workers, 62 s, 30/30 checks, FINAL ok); JSON beside them.
- scripts/render_hybrid.py: Figure 8.5 (depth-buffered faces, crisp edges, 3x supersampling, element colours, DICTO mark); data/hybrid-slab.png, data/render.log.
- Runs on the compute host through the job gate (jobs phybrid-pilot, phybrid, phybrid-render), each FINAL ok.
