# Fable, pass 5: count check and a systematic search on G′ (2026-10-17)

DICTO · dictospheres.com

## Task 1: the counting step (exact)

Full write-up: `FABLE-GBPC-COUNT-CHECK.md`.

- **Face to face, one size: holds.** The homotopy step is valid. It works because every point of G′ lies within a bounded distance of a wall. That keeps the conjugate map within a bounded distance of a linear map, and so the O(N²) bound holds.
- **The check is now a theorem.** The value S = σ(vol G′) that pass 1 checked numerically follows from a triangulation argument.
- **Correction, one-size case.** The negative oblate count holds for every edge in ℚφ·|v|, not only for φ|v|/(9k).
- **Any sizes, face to face: holds,** using the connectivity of G′. That connectivity is checked in float only.
- **Periodic, edges in ℚφ·|v|: holds.** The oblate part must be −10/243 per cell. This is elementary.
- **Mudra / Crown Jewel bound: holds with a qualifier.** The 90 / 20 figures are right, but only when every piece's scale is in ℚφ·|v|. At scales in ℚ·|v|, for example φ-smaller oblates, or a Vajra at |v|/9, pieces can also have a negative part.

## Task 2: systematic search (launched, results pending)

**Script.** `scripts/gbpc_lns.py`, a large-neighbourhood search, which is a form of local backtracking. It starts from RB-22 (66.85%), then repeats three steps:

1. **Remove.** Take out every body within a random ball of radius 0.5–1.2 × the largest body reach, together with its lattice orbit.
2. **Refill.** Refill the hole 4 times, each time with an exhaustive greedy pass: at every anchor, every candidate is tried, the largest volume goes first, and ties go to the most face contacts with random tie-breaks. Keep the best of the 4 refills.
3. **Accept.** Keep the result if its volume is greater than or equal to the removed volume (exact comparison in ℚ(√5)). Equal-volume moves are kept so the search can drift.

**Pieces.** Golden rhombohedra at λ, λ/2 and λ/4, and the five Bodhi pieces at λ and λ/2. λ = φ|v|/9.

**Overlap test.** The exact separating-axis test from pass 4, shared code with `gbpc_search.py`.

**Run.**
- Job on dicto-node, single process: `~/gbpc4/logs/lns-RB-51.log`.
- Best build: `~/gbpc4/data/lns-RB-51.json`. It is rewritten on every strict gain, with the exact volume and the exact gap.
- The run stops by itself at 09:30 JST on 2026-10-18.

**How to read the log.** It has one JSON line per iteration, with these fields:
- `removed` / `added`: bodies taken out and put back;
- `delta`: volume change (float);
- `accepted`: whether the refill was kept;
- `fill`: fraction of G′ filled (float);
- `bodies`: bodies per cell after the move.

The final line is `done`. It gives the fill, the exact gap volume `a|b` (meaning a + b√5) and the counts per piece.

**Pruning.** Count pruning was not built into the move. The best builds already pay the oblate deficit (pass 4: the RB-22 gap has X = 349/17496 > 0), so the count does not cut any branch here. The exact gap in the output lets the count be checked afterwards.

**Status at writing.** The search has not been read yet. No result is claimed. A fill of 100% would be a real result, and it would need the exact and float checks of pass 4 before anything goes into the paper.

## For the paper

Only the Task 1 wording changes are needed now: see the end of `FABLE-GBPC-COUNT-CHECK.md`. "The search used restarts only, not backtracking" stays true until the LNS result is read.
