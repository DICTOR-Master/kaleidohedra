# The RD bridge: how many marked rhombic dodecahedra carry the chair hierarchy (12 Nov 2026)
DICTO: "go ahead with the bridge count" (aim 1, one piece; his 11-09 method: build on the credited chair, carry it to the RD packing).

**Conclusion:** the isometric bridge works and needs **118 differently marked RDs** (7 for RDs inside a chair cube, 111 for RDs on cube
edges), the same at supertile levels 3 to 6. CORRECTION (12 Nov, same day): the first count, 558 (551 edge), numbered the chairs
round an RD in the world order of its cubes, so one configuration could count as several types; ids are now renumbered by first
appearance. All results below are from the corrected run (first-run files in data/superseded-idorder/). This is an upper bound with full information on every RD; it carries
the chair's strong aperiodicity onto the fcc RD packing (all layers c), so it serves DICTO's transfer principle, not the c/h stacking.
Status: SETTLED (count). Next: cut 558 down (what does each RD really need to know?).

Credit: the mechanism is Tsiokos's (Chair44, arXiv 2609.19214); the frame marking, the certified frame assignment and the code are
Kamenetsky's (arXiv 2610.00916; `scripts/vendor/` copied unchanged, MIT). The bridge and the count are ours.

## Method (`scripts/bridge_count.py`)
- Kamenetsky's coordinates: unit cubes of side 2 with odd centres. The fcc sites = integer points with odd coordinate sum: each cube
  centre (an RD wholly inside its cube; its 4-valent corners are the cube's face centres) and each cube-edge midpoint (an RD shared by
  the 4 cubes round that edge). Every chair motion (signed permutation, even translation) keeps this set, so no shear is needed.
- A hierarchical chair tiling = the level-k supertile with the certified frames (rerun of Theorem A in `studies/2026-11-10-arxiv-scan`).
- Label of an RD = for each cube that holds part of it: offset from the RD, chair frame, cell, which chair; taken up to the RD's 24
  proper turns (minimum over the turns).
## Result (dbb job rd-bridge, `data/bridge_count.log`, `data/bridge_count.json`, FINAL ok)
| level | chairs | centre types | edge types (by chairs met 1/2/3/4) |
|---|---|---|---|
| 3 | 512 | 7 | 111 (3/40/24/44) |
| 4 | 4096 | 7 | 111 (same) |
| 5 | 32768 | 7 | 111 (same) |
| 6 | 262144 | 7 | 111 (same) |
Controls: every cube once, 7 per chair; centre RDs give exactly the 7 cells; stable from level 4 to 6. (A first version counted
face-centre points as sites; the "every site is fcc" control caught it and it was fixed before any count was used.)
## Reading
- 118 is far above Narcissus Keyed (#97: 17 pieces, and those force the c/h stacking). As a set of tiles the bridge is no gain; its
  value is the transfer principle (DICTO 11-09): the RD packing inherits strong aperiodicity from a credited chair with an exact,
  local, rotation-respecting relabelling.
- The capacity is there: an RD has 24 proper turns, like the chair. Narcissus has 3 (the wall behind the vertical-plane wave, 12 Nov).
## LEADS
1. Cut down: the edge RD labels repeat what the 4 surrounding chairs already say. Test: is an edge RD's label fixed by the 4 centre RDs
   round it (then edge RDs carry only a relay) and how few relay kinds suffice; then whether the centre RD's cell (7) can be read from its
   neighbours so that one centre kind with 24 turns is enough.
2. The c/h aim is not touched: all layers stay c. The stacking needs a carrier off one lattice (Kamenetsky's open item 2).

## Cutting the 118 down (12 Nov; `scripts/cut_down.py`, dbb job rd-cut2, level-4 rules, every fcc torus of index <= 8 = 390 tori)
| scheme (what each RD is told) | types | full label readable from the 12 neighbours | SAT on tori |
|---|---|---|---|
| PLAIN (nothing; control) | 1 | no | periodic, index 1 |
| FRAME (centre: chair turn) | 2 | no | periodic, index 1 |
| CELL (centre: cell) | 8 | no | periodic, index 1 |
| CELL+EPART (centre: cell; edge: which cubes share a chair) | 12 | no | periodic, index 4 |
| **CELLFRAME (centre: cell + chair turn; edge: which cubes share a chair)** | **12** | **yes** | **no torus up to index 8** |
| FRAME+EFR | 90 | yes | no torus up to index 8 |
| CELL+ECELLS | 91 | yes | periodic, index 4 |
| CELL+EPC | 102 | yes | periodic, index 4 |
| FULL (control) | 118 | yes | no torus up to index 8 |
Controls held (FULL no torus, PLAIN periodic). Two solver faults found and fixed on the way (at-most-one per site was missing; a
pysat one-literal encoding returns nv 0) before any result was used.
**Chair contacts (`scripts/contact_test.py`):** under the 12-type rules two chairs may touch in 99 of the 1194 proper touching poses:
all 30 that occur in hierarchical tilings, 32 of Kamenetsky's 44, and 67 OUTSIDE his certified set. So Theorem A does not apply at once.
Running: the two-shell test (do the 67 extra contacts ever survive a full second shell of chairs?), dbb job rd-encl.
