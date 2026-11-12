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
Two-shell test (Kamenetsky's live(), per extra contact): 49 of the 67 extra contacts survive a full shell round both chairs, so the
12-type set is NOT certified this way.

## The 90-type set is strongly aperiodic (12 Nov; DICTO: "second first", "go ahead with the whole chair test")
Scheme FRAME+EFR: every RD is told the turn (frame) of each chair whose cubes it touches and which of its cubes share a chair; no
cells. 90 marked RDs (1 centre kind, 89 edge kinds), each placed in any of its 24 turns; rules = the face-to-face pairs (type,
direction, type, relative turn) of a hierarchical tiling: 2104 pair rules, the same at levels 4 and 5 (`scripts/rule_stability.py`).
The chain:
1. Tiling exists: the hierarchical chair tilings, read through the bridge, obey the rules (rules complete by level 4).
2. Grid (`scripts/integrity_test.py` part G): no allowed pair places cubes on two different grids, so every filling has one cube grid.
3. Whole chairs (part C, ball of radius 2 grid steps: 665 sites, 387 480 choices): no rule-obeying filling fails to read a whole chair,
   turned as its RDs say, round a cube (UNSAT). Controls: a filling with a whole chair exists; with blank edges (FRAME) whole chairs
   are NOT forced.
4. Contacts (`scripts/contact_test.py`): two whole chairs may touch only in the 30 contacts that occur, all inside Kamenetsky's P*.
5. So every filling by the 90 marked RDs is a P*-tiling of marked chairs, hence uniquely hierarchical (Kamenetsky's Theorem A, which we
   reproduced with our own code, studies/2026-11-12-repro-kamenetsky), hence strongly aperiodic: no translation, no screw motion.
Same contact verdict for CF+EFRAME (96) and CF+ECELL (102); FULL (118) the control. Credit: mechanism Tsiokos; frame marking,
certified assignment and Theorem A Kamenetsky; the RD bridge, the reductions and the tests ours. The c/h stacking is NOT touched
(all layers c). Next: search between 12 and 90 for the smallest certified set; then a keyed RD shape (Grogan's / Kamenetsky's key
constructions as templates).

## The 12-90 search (12 Nov; `scripts/search_H.sh`, dbb job rd-searchH, FINAL ok; summary data/searchH-summary.txt)
Edge RDs told each touching chair's turn only up to a subgroup H of the 24 rotations (centre RDs keep the full turn). All 30 subgroups:
contact test (one shell), and for those with no contact outside P* the whole-chair test at R = 2. Controls held: H00 (trivial) = the
90-type set certified; H29 (all 24) = 6 types, 115 contacts outside P*.
- Certified (contacts inside P* AND whole chairs forced): H00 90, H01 90, H03 90, H02 87, H05 83, H07 83, **H18 62** (H18 = the
  quarter turns about the y axis, the axis of the certified assignment's own (02) symmetry).
- Contacts inside P* but whole chairs NOT forced at R = 2: 11 schemes of 35-85 types (H25, H26 35; H22, H23 36; H24 43; H15, H19 48;
  H17 50; H04, H06 52; H08 57; and 69-85). Retest at R = 3 running (job rd-searchR3), with the rule check of H18.
- Contacts outside P*: H13 28 (10), H21 15 (10), H27 32 (2), H28 14 (19), H29 6 (115).
