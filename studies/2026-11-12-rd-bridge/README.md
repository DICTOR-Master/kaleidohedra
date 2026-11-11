# The RD bridge: how many marked rhombic dodecahedra carry the chair hierarchy (12 Nov 2026)
DICTO: "go ahead with the bridge count" (aim 1, one piece; his 11-09 method: build on the credited chair, carry it to the RD packing).

**Conclusion:** the isometric bridge works and needs **558 differently marked RDs** (7 for RDs inside a chair cube, 551 for RDs on cube
edges), a count that is the same at supertile levels 4, 5 and 6. This is an upper bound with full information on every RD; it carries
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
| 3 | 512 | 7 | 483 (3/80/144/256) |
| 4 | 4096 | 7 | 551 (3/80/144/324) |
| 5 | 32768 | 7 | 551 (same) |
| 6 | 262144 | 7 | 551 (same) |
Controls: every cube once, 7 per chair; centre RDs give exactly the 7 cells; stable from level 4 to 6. (A first version counted
face-centre points as sites; the "every site is fcc" control caught it and it was fixed before any count was used.)
## Reading
- 558 is far above Narcissus Keyed (#97: 17 pieces, and those force the c/h stacking). As a set of tiles the bridge is no gain; its
  value is the transfer principle (DICTO 11-09): the RD packing inherits strong aperiodicity from a credited chair with an exact,
  local, rotation-respecting relabelling.
- The capacity is there: an RD has 24 proper turns, like the chair. Narcissus has 3 (the wall behind the vertical-plane wave, 12 Nov).
## LEADS
1. Cut down: the edge RD labels repeat what the 4 surrounding chairs already say. Test: is an edge RD's label fixed by the 4 centre RDs
   round it (then edge RDs carry only a relay) and how few relay kinds suffice; then whether the centre RD's cell (7) can be read from its
   neighbours so that one centre kind with 24 turns is enough.
2. The c/h aim is not touched: all layers stay c. The stacking needs a carrier off one lattice (Kamenetsky's open item 2).
