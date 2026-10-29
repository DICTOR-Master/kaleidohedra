# HexOct-K: the stacking as the clock (study, 2026-10-29)

DICTO's request: "can we do more research on HexOct-K first" (before #75 v2). Open problem of the keyed study: keyed sets that use
the interlocking joints, where each tile touches four to six tiles above.

**One-line conclusion.** In the whole interlocking range (λ > −7/24), in every close-packed stacking, every HexOct tile touches the
tiles of the layer below, and of the layer above, at exactly three positions across the layers' common diagonal, s − 1, s, s + 1
(s = du − dv, unchanged from layer to layer because every layer shift lies along (1, 1)), and at no others. So keyed HexOct tiles
(HexOct-K) run any elementary cellular automaton with one step per layer: the stacking itself is the clock, whatever the order of c-
and h-tiles; with Rule 110 (Cook 2004) the stack is a universal computer.

**Status:** checked (sampled face areas on exact tiles) in all 32 five-layer contexts at 6 interlocking weights, 192 cases, 0 failures,
no face area unmatched. Face areas sampled, not exact; the CA statement follows from the contact pattern by construction (below).

## Results (out/ctx_*.jsonl, out/summary.txt)

| λ | cases | smallest side face (s ± 1), below / above | smallest centre (s) | for physical keys |
|---|---|---|---|---|
| −1/4 | 32 | 0.0135 / 0.0114 | 0.86 | too small |
| −1/6 | 32 | 0.118 / 0.111 | 0.86 | marginal |
| 0 | 32 | 0.334 / 0.331 | 0.70 | good |
| 1/10 | 32 | 0.403 / 0.407 | 0.60 | good |
| 1/4 | 32 | 0.480 / 0.480 | 0.52 | very good |
| 1/3 | 32 | 0.497 / 0.497 | 0.50 | very good (sides ≈ centre) |

(ball spacing 1). Lateral contacts (same layer) are at s ∈ {±1, ±2} and sometimes 0; they carry no keys (blank).

## The construction (why this computes)
Take a configuration constant along the diagonal (1, 1) of each layer (the direction of every layer shift), so a layer is a row of
states indexed by s. Give a tile one state; on every face it shares with a tile ABOVE it writes its own state; on every face it shares
with tiles BELOW it reads theirs; same-layer faces are blank. The tiles below a tile sit at s − 1, s, s + 1 (the two at s, when two
touch, carry the same state), so a tile set with one tile per input triple (left, centre, right) → output state is exactly an elementary
cellular automaton, and the filling is forced layer by layer. With two states and Rule 110 this is universal (M. Cook, Complex Systems
15, 2004). The order of c- and h-layers does not matter: every context has the same three-position contact.

## Prior art (sources checked)
- Web searches: "space-time diagram of cellular automaton as three-dimensional tiling polyhedra layers stacking computation"
  (results: arXiv 2108.13094 universal CA on the hyperbolic dodecagrid; arXiv 2307.13075 universal 18-Wang-tile schema for any
  elementary CA; Törmä et al. fixed-point tilings); "Wang cubes simulate cellular automata Culik Kari aperiodic 3D tiles" (Culik and
  Kari 1995, JUCS 1(10), aperiodic Wang cubes); "close-packed stacking sequence layers as computation cellular automaton polytypes
  rule" (Varn and Crutchfield, arXiv cond-mat/0307296: rule 232 as a model of the 2H→3C change of the stacking itself).
- Known: Wang tiles (and cubes) run cellular automata; space-time diagrams of a CA are tilings.
- Not found: close-packed layers, or space-filling tiles cut from their holes, carrying a CA with the stacking as the clock.
  What is new here is the geometry: one tile shape per layer type, any stacking order, and the three-position contact.

## Files
scripts/clock_contacts.py (per context; contacts.py, tiles.py and the census engine copied from studies/2026-10-29-keyed-hexoct);
run on dicto-big-brother, 16 in parallel; out/ctx_0..31.jsonl, out/summary.txt.
