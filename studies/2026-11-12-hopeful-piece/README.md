# The hunt for a hopeful piece (12 Nov 2026, aim 3: one piece, any stacking)
DICTO: "put more work on dbb aim 3". Keying stays PAUSED (DICTO 12 Nov, "until another hopeful piece comes to us"), so this study
does not refine or key any marked set; it hunts for the new piece itself: ONE piece whose shape alone (bumps and dents, no colour
labels) admits no periodic filling.

**Conclusion:** no hopeful piece. Among 6 385 243 keyed RDs (every symmetry class with |G| >= 3, exhaustive) plus 40 000 random
paired ones, and all 14 102 unkeyed poly-RDs up to 7 cells, every piece is either untileable or periodic. In these families every keyed RD that fills
a ball of radius 2 repeats with at most 8 pieces per period; every poly-RD up to 7 cells repeats with at most 4 pieces per period.
Status: SETTLED for these families (a closed route, not a proof for keyed RDs with no symmetry). Keying stays paused.

## PAUSED 13 Nov (DICTO): "pause the RDs search indefinitely"
Leads 1 and 2 were run on 13 Nov; jobs hp-ks and hp-ksdeep2 were stopped cleanly at DICTO's word. Lead 3 (keyed poly-RDs of 6 or
more cells) was not started. Retry only on DICTO's word.

**Deep check of the 73 (13 Nov, below):** all 73 are periodic (index 96); no hopeful piece.

**One-line conclusion:** all 144 158 unkeyed 8-RD clusters are periodic (COMPLETE); the directed keyed-RD search was PARTIAL. It found
221 keyed RDs with no torus up to index 32. Of these, 83 were re-checked: none has a torus up to index 48, and 73 of 82 congruence
classes fill the ball R8 with no torus up to index 64. Nothing is claimed aperiodic: these are unexplained candidates, not hopeful
pieces.

| family | candidates | untileable | killed (periodic) at torus index | passed the cap |
|---|---|---|---|---|
| P8 poly-RD, no keys, n = 8, COMPLETE (job hp-n8, FINAL ok) | 144 158 free pieces | 0 | 8: 61 413, 16: 82 391, 24: 167, 32: 185; the 2 that passed 32 were killed at 40 and 48 | 0 |
| KS keyed RD, heights -1..1, no symmetry assumed, directed search, PARTIAL (hp-ks stopped after about 2 h of its 2.5 h cap; 0 of 81 cubes exhausted) | 5970 | 841 (840 R3, 1 R4) | 3: 15, 4: 1133, 6: 99, 8: 2375, 12: 136, 16: 889, 24: 141, 32: 120 | 221 (no torus <= 32, fill R4) |
| KS deep, PARTIAL (hp-ksdeep, FINAL ok, on the 83 logged by then; hp-ksdeep2 stopped at 92%) | 83 (82 up to congruence) | 0 to R5; 0 to R8 among 73 checked | none to index 48; none to index 64 among 73 checked | 73 classes fill R8 with no torus to 64; 9 classes unfinished; 138 later survivors unchecked |

- **Lead 1, cap.** Pieces per period for n <= 7 grew to 4 (index 28 at n = 7), so the cap was set in pieces per period, not cells:
  4 pieces (index 32) for all of n = 8, then 5 to 8 pieces (index 40 to 64) for the survivors. The worst case grew again to 6 pieces
  (index 48), so a ninth-cell run would need a cap of at least 8 to 12 pieces. Faster engine `poly8.py` (integer torus reduction); control: it
  reproduced hp-main's counts for n <= 6 exactly before the run (data/n8/ctl6.log).
- **Lead 2, method** (`keysearch.py`). One SAT model asks for the piece and a filling of the ball R2 together. Periods of index 1 and
  2 are excluded completely. Each period met on a torus (index <= 32) becomes a learned clause, "some contact of this pattern fails",
  added in all 48 turns. Control (data/ks/ctl.log): 31/31 test pieces agree; a blocked witness refuses its piece. The search drives
  periods up: symmetric keyed RDs repeat by index 8 (hp-main), while here periods of 12 to 32 are common.
- **Checks on the 83 deep candidates (13 Nov).** The fit table is symmetric and O_h-equivariant, which licenses one torus per orbit
  and the fixed centre turn. All 1325 tori to index 12, with no orbit reduction: no filling (3 pieces, `check_equiv.py`). Every candidate
  has 48 viable turns, 1 to 32 partners per face and no symmetry; the sum of heights is 0. Counting tests (`lp_check.py`): the
  orientation-frequency LP and the neighbour-pair LP are feasible for all 83. So no counting obstruction is known; periods above 64,
  or untileability beyond R8, stay open.
- Pilot fault fixed (13 Nov): the first keysearch control reused one model for its blocking tests, so an earlier witness (rightly)
  blocked later control pieces. Each blocking test now uses a fresh model (hp2-pilotb, 31/31).
- Data: data/n8 (counts, survivors, deep), data/ks (shard logs, counts at the stop), data/ksdeep (deep48 json, deep2 logs, LP).
  Scripts: poly8.py, keysearch.py, run_n8.sh, run_ks.sh, run_ksdeep.sh, run_ksdeep2.sh, check_equiv.py, lp_check.py,
  inspect_surv.py, deep3.py (written, not run: box tori of index 65..128 and the ball R10).
- Next if DICTO resumes: finish deep2 (9 classes) and deep2 for the 138 later survivors; deep3; a 2x2-patch LP; then report any piece
  still standing to DICTO first (not keyed).

## Deep check of the 73 (13 Nov, DICTO's exception)
DICTO approved one check while the hunt stays paused: "73 keyed jobs". No new search, no keying.

**One-line conclusion:** all 73 classes are periodic. Each one fills an fcc torus of index 96, so each one has a period of 96
pieces. The three checked by witness all use the period vectors (4, 4, 0), (6, 0, 6), (2, 4, 6). None is untileable: every class fills the ball R16 (14 993 RDs).
There is no hopeful piece among the 73. Status: SETTLED for these 73 classes. The 9 unfinished classes and the 138 later
survivors of hp-ks stay unchecked (paused).

- **Cap, and why.** The 7-cell lesson was a cap one step too low: tori were checked to 3 pieces per period, and the period was 4.
  So the cap here follows the periods actually seen. Every keyed-RD kill so far came at a 3-smooth index (2^a 3^b): hp-main 1, 2, 4,
  6, 8; hp-ks 3, 4, 6, 8, 12, 16, 24, 32 (4 908 kills, complete tori to 32). In hp-ks the largest period doubled to 32 when the
  search pushed periods up. Indices 48 and 64 were already clear (deep, deep2). So the run checked every torus of index 65..72
  (complete, 3 833 orbits), then the next two rungs of that ladder, 96 = 3 x 32 (1 761 orbits) and 128 = 4 x 32 (2 090 orbits).
  The pilot timings were 0.09, 0.14 and 0.20 s per torus, so this was the most that fitted the 10 h overnight cap on 2 cores.
  Indices 73..95 were not checked, so 96 is a period, not proved to be the least one.
- **Order.** Tiers, with every class through a tier before any class starts the next: balls R10, R12, R16; tori 65..72; index 96;
  index 128. Checkpoint per (class, tier) in data/d73/p_K.jsonl.
- **Controls (same code, data/d73/ctl.log, ctl_surv.log).**
  - The per-index torus orbits equal hunt.py's tori() for every index 1..24.
  - Known kill (README, hp-deep): the heptomino's first torus is at index 28, with none at 7, 14, 21.
  - Plain RD fills a torus; all-bump RD fills no ball R1.
  - Known survivor 0.0: no torus 49..64 (as deep2), fills R16.
- **Witness (job hp-d73-witness, data/d73/witness.log).** For classes 0.0, 3.5 and 7.8, the index-96 filling was rebuilt and checked
  point by point from the raw heights, without the fit table: 4 608 point contacts each, 0 mismatches. All three use the same
  period lattice, HNF ((4,0,0),(0,6,0),(0,2,4)). The fillings use 24, 36 and 24 of the 48 orientations.
- **Structure (step 4).** No class survived, so no ball filling was examined for hierarchy or substitution. The period lattice shared by
  the three witnessed classes (index 96 = 3 x 32) answers why indices 48 and 64 found nothing. It is not a forced hierarchy.
- Ledger [213]. Jobs: hp-d73-pilot, hp-d73 (FINAL ok, about 6.5 h), hp-d73-witness (FINAL ok). Script: scripts/deep4.py (modes list, tori, ctl,
  pilot, run, struct, witness), scripts/run_d73.sh. Data: data/d73 (classes.json = the 73 height fields; the torus tables are
  rebuilt by `deep4.py tori`, not stored).

Per class: 48 heights, + bump, - dent, 0 flat. They are grouped by face, 4 points per face, in hunt.py's face order. The table
gives the ball tier, the tori of index 65..72 and the torus of index 96.

| class | heights | balls R10/R12/R16 | tori 65..72 | index 96 | verdict |
|---|---|---|---|---|---|
| 0.0 | `+--- -++- +0-0 0-0+ +--+ 0-0+ -0+0 +++- -0+0 0+0- +--+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.1 | `+--+ -0+0 --++ ++-- +++0 ++-- ++-- 0+0- ++-- --++ +--+ 0---` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.2 | `+--0 +--+ +0-0 0-0+ 0-0+ 0-0+ -0+0 +--+ -0+0 0+0- +-0+ -0+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.3 | `+--0 -++- +--+ +--+ -++- +--+ +0-+ +--+ -++- +--+ +--+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.4 | `+--+ 0+0- -++- -0+0 -++- 0-0+ -+-0 +--+ 0-0+ +--+ +-+0 -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.5 | `+--+ --++ +--+ ++-- ++-- ---+ +--+ ++-- ++-- ++-+ --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.6 | `+--0 +--+ +-00 00-+ 0-0+ 00-+ 00+- 0++- 00+- -+00 +0-0 +--+` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.7 | `+--0 0000 +0-0 0000 0000 0000 +0-+ 0000 0000 0000 0000 -0+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 0.8 | `+--- 0000 ++-- 0000 0000 ++-- ++-+ 0000 0000 --++ 0000 --++` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.0 | `+--- -0+0 0-0+ +0-0 +--+ +0-0 0+0- +++- 0+0- -0+0 +--+ 0+0-` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.1 | `+--+ -0+0 --++ ++-- -0++ ++-- ++-- 0+0- ++-- --++ +--+ --0+` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.2 | `+--+ --++ +--- ++-- ++-- --++ +--+ ++-- ++-- ++-- --++ -+++` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.3 | `+--0 -++- --++ +--+ -++- -++- ++-- +--+ -++- -++0 +--+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.4 | `+--- -++- +0-0 +--+ -++- +0-0 0-0+ +--+ -++- -+++ +--+ +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.5 | `+--+ -0+0 --++ ++-- --+0 ++-- ++-- 0+0- ++-- --++ +--+ 0-++` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.6 | `+--+ --++ +--+ ++-- ++-- 0-+- +--+ ++-- ++-- +0+- --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.7 | `+--0 0000 0+0- 0000 0000 +0-0 -0+0 0000 0000 -++0 0000 +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.8 | `+--0 0000 -++- -++- 0000 -++- +--+ 0++- +--+ +--+ 0000 0000` | fills R16 | none | SAT, 96 | killed at 96 |
| 1.9 | `+--- +0-0 0000 0000 +0-0 0000 0000 0-0+ 0000 0000 +-++ 0+0-` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.0 | `+--- ++-- 0000 0000 ++-- 0000 0000 +++- 0000 0000 --++ --++` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.1 | `+--+ 0000 +-0- 0000 0000 +0-0 +-+0 0000 0000 -++- 0000 +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.2 | `+--+ --++ +--+ ++-- ++-- -+++ +--+ ++-- ++-- -+-- --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.3 | `+--0 0000 -0+0 0000 0000 -++- 0+0- 0000 0000 -++0 0000 -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.4 | `+--- 0-0+ -++- -++- 0-0+ -++- +--+ +0-0 +--+ +--+ +-++ -0+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.5 | `+--+ -0+0 --++ ++-- 0-++ ++-- ++-- 0+0- ++-- --++ +--+ --+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.6 | `+--+ -0+0 --++ ++-- +-+0 ++-- ++-- 0+0- ++-- --++ +--+ 0-+-` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.7 | `+--0 +--+ +-+- -+-+ 0-0+ -+-+ +-+- 0++- +-+- -+-+ +0-0 +--+` | fills R16 | none | SAT, 96 | killed at 96 |
| 2.8 | `+--0 0000 0-0+ 0000 0000 +0-0 +0-0 0000 0000 -++0 0000 +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.0 | `+--0 -++- -++- +--+ -++- ++-- -++- +--+ -++- -++0 +--+ ++--` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.1 | `+--- -0+0 00+- -+00 0+0- -+00 +-00 0+0- +-00 00-+ +-++ +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.2 | `+--+ -0+0 --++ ++-- +0+0 ++-- ++-- 0+0- ++-- --++ +--+ 0-0-` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.3 | `+--0 ++-- +--+ +--+ ++-- +--+ -++- --++ -++- -++- +-0+ ++--` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.4 | `+--0 -++- +0-0 +--+ -++- +0-0 +0-+ +--+ -++- 0-0+ +--+ -0+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.5 | `+--- -0+0 +--+ +--+ -0+0 +--+ -++- +++- -++- -++- 0+0- 0+0-` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.6 | `+--+ -0+0 --++ ++-- 0-+0 ++-- ++-- 0+0- ++-- --++ +--+ 0-+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.7 | `+--+ --++ +--+ ++-- ++-- --0+ +--+ ++-- ++-- ++-0 --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 3.8 | `+--0 +--+ +-+- -+-+ +--+ -+-+ +-+- 0++- +-+- -+-+ +--+ +--+` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.0 | `+--0 0000 -++- 0000 0000 -++- -++- 0000 0000 -++0 0000 -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.1 | `+--- -++- 0-0+ +0-0 +--+ +0-0 0+0- +++- 0+0- -0+0 +--+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.2 | `+--+ -0+0 --++ ++-- -+++ ++-- ++-- 0+0- ++-- --++ +--+ ---+` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.3 | `+--+ --++ +--+ ++-- ++-- --+0 +--+ ++-- ++-- ++0- --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.4 | `+--0 0-0+ -++- -++- 0-0+ -++- +--+ 0++- +--+ +--+ +0-0 +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.5 | `+--- 0000 -+00 00+- -++- 00+- 00-+ 0000 00-+ +-00 +-++ +--+` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.6 | `+--+ -0+0 --++ ++-- --+- ++-- ++-- 0+0- ++-- --++ +--+ +-++` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.7 | `+--+ -0+0 --++ ++-- +-++ ++-- ++-- 0+0- ++-- --++ +--+ --+-` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.8 | `+--+ --++ +--+ ++-- ++-- -00+ +--+ ++-- ++-- 0+-0 --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 4.9 | `+--0 ++-- ++-- --++ +--+ --++ --++ --++ --++ ++-- +-0+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.0 | `+--0 +--+ +0-0 0-0+ --++ 0-0+ -0+0 +--+ -0+0 0+0- +-0+ --++` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.1 | `+--0 -++- +0-0 +--+ -++- +0-0 0-0+ +--+ -++- -++0 +--+ +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.2 | `+--+ 0+0- -++- -++- -++- +--+ -+-0 +--+ 0-0+ +--+ +-+0 -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.3 | `+--+ --++ +--+ ++-- ++-- -+0+ +--+ ++-- ++-- -+-0 --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.4 | `+--0 0000 -0+0 0000 0000 --++ 0+0- 0000 0000 -++0 0000 --++` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.5 | `+--0 -++- ++-- +--+ -++- ++-- +0-+ +--+ -++- --++ +--+ --++` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.6 | `+--- --++ +--+ +--+ --++ +--+ -++- +++- -++- -++- ++-- ++--` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.7 | `+--+ -0+0 --++ ++-- 0++0 ++-- ++-- 0+0- ++-- --++ +--+ 0--0` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.8 | `+--+ -0+0 --++ ++-- +0++ ++-- ++-- 0+0- ++-- --++ +--+ --0-` | fills R16 | none | SAT, 96 | killed at 96 |
| 5.9 | `+--0 +--+ +-00 00-+ +--+ 00-+ 00+- 0++- 00+- -+00 +--+ +--+` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.0 | `+--+ --++ +--0 ++-- ++-- --++ +--+ ++-- ++-- ++-- --++ -++0` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.1 | `+--0 -++- -0+0 +--+ -++- -++- 0+0- +--+ -++- -++0 +--+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.2 | `+--- --++ 00+- -+00 0+0- -+00 +-00 ++-- +-00 00-+ +-++ +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.3 | `+--+ -0+0 --++ ++-- 00+0 ++-- ++-- 0+0- ++-- --++ +--+ 0-00` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.4 | `+--0 +--+ +--+ -++- +--+ +--+ +--+ -++- +--+ -++0 -++- +--+` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.5 | `+--0 0000 0000 0000 0-0+ 0000 0000 0000 0000 0000 +-0+ -0+0` | fills R16 | none | SAT, 96 | killed at 96 |
| 6.6 | `+--- 0000 -+00 00+- 0+0- 00+- 00-+ 0000 00-+ +-00 +-++ +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.0 | `+--+ --++ +--+ ++-- ++-- -0-+ +--+ ++-- ++-- 0+-+ --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.1 | `+--0 0000 --++ 0000 0000 --++ ++-- 0000 0000 -++0 0000 --++` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.2 | `+--- 0000 ++-- --++ -0+0 --++ --++ 0000 --++ ++-- +-++ 0-0+` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.3 | `+--+ -0+0 --++ ++-- 0+++ ++-- ++-- 0+0- ++-- --++ +--+ ---0` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.4 | `+--+ --++ +--+ ++-- ++-- --+- +--+ ++-- ++-- +++- --++ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.5 | `+--0 0000 0000 0000 0000 +0-0 0000 0000 0000 -++0 0000 +0-0` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.6 | `+--0 -++- 0+0- +--+ -++- 0+0- +0-+ +--+ -++- -0+0 +--+ 0-0+` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.7 | `+--- -++- -++- +--+ -++- -++- -++- +--+ -++- -+++ +--+ -++-` | fills R16 | none | SAT, 96 | killed at 96 |
| 7.8 | `+--+ -0+0 --++ ++-- 0-+- ++-- ++-- 0+0- ++-- --++ +--+ +-+0` | fills R16 | none | SAT, 96 | killed at 96 |

## Plan (written before computing)
Ledger read first (concordance.json): Narcissus with crest, edge or face decorations is CLOSED ([160]: "never on Narcissus ...; only a
carrier with more turns per site (RD bridge, 24) or several pieces"); keys on half-cells at the hexagon or the inter-layer rhombi are
CLOSED ([96], [97]); the hat on RD/TRD sectors as layer pieces is CLOSED ([49], [50]); the marked-RD keying is PAUSED ([178]). So the
Narcissus and half-RD bases of the brief are left out, and the hunt uses the open carrier: the RD (24 turns, 48 with mirror images)
and pieces made of several RDs.
1. Candidates.
   - **K, keyed RD.** One RD with tiny square pyramids (bumps up, dents down) at the 4 points of one generic orbit of the rhombus's
     symmetries on each face (as keyed_rd.py, (u, v) = (3/10, 1/7)): a height on each of the 48 points. The registration theorem
     (rd-bridge README) puts every tiling by congruent copies on one fcc lattice, face to face; mirror copies are allowed (congruent
     copies, as for Chair44), so each site takes one of the 48 orientations, and two neighbours fit iff every bump meets a dent of the
     same size. The 48 points are one free orbit of the RD's 48 symmetries, so a piece with symmetry group G is any G-invariant height
     field: 48/|G| free heights. Exhaustive for every class of subgroups with |G| >= 4 (heights -1, 0, 1; and -2..2 for |G| >= 8);
     random samples for |G| = 1, 2, 3. Counted up to the 48 symmetries and bump <-> dent exchange (same fillings).
   - **P, poly-RD (shape alone).** Every free polyform of n face-joined RDs, n <= 6, no keys.
   - **Transfer (DICTO's principle, Tsiokos's chair credited).** The marked-RD sets from the chair (rd-bridge) need many states per
     site; a single RD carries at most 48 (its orientations). We record which bridge markings fit that capacity and what a poly-RD
     piece would need; no chair-derived piece is claimed unless it is built and tested here.
2. Kill test: arc consistency of the 48 orientations, index 1, then SAT (pysat Cadical153) on every fcc torus of index <= 16 (poly-RD:
   indices that are multiples of n, up to min(24, 8n)), one torus per orbit of sublattices under the 48 symmetries (the piece set is
   closed under them, so congruent tori answer alike). Any SAT torus kills the candidate.
3. Survivors: a candidate with no torus that also fills the ball of radius 4 round a site (309 RDs) is a hopeful piece and is reported
   to DICTO, not keyed. A candidate that fails a ball is untileable (no filling of space at all).
4. Controls (same code): plain RD periodic at index 1; all-bump RD untileable; single-RD polyform periodic at 1; the cuboctahedral shell
   of 12 RDs round a hole untileable; marked-RD rule sets exported from the RD bridge: CELL+EPART periodic at 4, CELLFRAME no torus <= 16
   (job rd-cut16s), FRAME+EFR (certified strongly aperiodic, 90 types) no torus; the torus count 2961 up to index 16 as in rd-bridge.
Credit: any use of Chair44's mechanism is Tsiokos's (arXiv 2609.19214); the marked-RD control data use Kamenetsky's frames.

Scripts: `scripts/hunt.py` (modes control, K, P), `scripts/export_rules.py` (control data from rd-bridge's cut_down.py, unchanged).

## Result (dbb jobs hp-pilot, hp-main, hp-deep, all FINAL ok; data/main/summary.json, data/main/*.log, data/deep/s*.log)
Controls, same code (data/main/E_control.log): plain RD killed at 1; all-bump RD untileable (AC); a turned and inverted copy has the
same canonical form; 2961 tori up to index 16, as in rd-bridge (271 orbits under O_h, also 271 under O, because -I fixes every lattice);
single-RD polyform killed at 1; cuboctahedral shell of 12 RDs round a hole untileable (R1); marked-RD rules exported from rd-bridge:
CELL+EPART killed at 4 (expected), CELLFRAME no torus up to 16 (as job rd-cut16s), FRAME+EFR (90 types, certified strongly aperiodic)
no torus up to 16. The count check also held: the exact per-class enumeration gave 1216 candidates for |G| >= 8, the same as a
dictionary of canonical forms.

| family | distinct candidates (up to the 48 symmetries and bump <-> dent) | untileable | killed (periodic) at torus index | survivors |
|---|---|---|---|---|
| A keyed RD, 10 classes with \|G\| = 4 or 3, heights -1..1, exhaustive | 6 067 102 | 6 055 030 (5 922 814 AC, 132 216 ball R2) | 1: 1549, 2: 4245, 4: 4202, 6: 13, 8: 2063 | 0 |
| B keyed RD, 17 classes with \|G\| >= 6, heights -2..2, exhaustive | 318 141 | 316 250 (313 270 AC, 2980 R2) | 1: 525, 2: 462, 4: 634, 8: 270 | 0 |
| D keyed RD, no symmetry, faces paired at random (seeds 11, 12) | 40 000 | 39 999 (R2) | 8: 1 | 0 |
| P poly-RD, no keys, n = 1..7 (1, 1, 4, 20, 131, 1211, 12 734 free pieces) | 14 102 | 0 | 1..7: n = 1..7 mostly at index n; 8, 10, 12, 14, 21, 24 (2 to 4 pieces per period) | 6 at n = 7 -> all killed at 28 |
Per-class counts: data/main/summary.json. The keyed classes include chiral and mirror-symmetric pieces; mirror copies were allowed
in every filling (congruent copies).
The 6 heptomino survivors of hp-main (no torus of index 7, 14, 21, they fill a ball of radius 4) were rerun on tori of index 28-56
(job hp-deep): all six are periodic at index 28 (4 pieces per period). hp-main capped the poly-RD torus index at min(24, 8n); for
n = 7 that let 4-piece periods through, and the deep check closed them. (Fault of the deep check fixed afterwards: the six parts
wrote one shared deep_check.json; the logs data/deep/s*.log hold all six verdicts.)

## Reading
- A keyed RD carries at most 48 states per site (its orientations). The RD-bridge markings that fit that budget are PLAIN (1) and
  FRAME (25 states), both periodic at index 1; CELLFRAME needs 288 states, FRAME+EFR 2160 (all viable, control log). So a fixed
  site-by-site relabelling (DICTO's transfer principle at radius 0) cannot carry any bridge marking without small periods onto ONE keyed
  RD; it needs a piece of at least 6 RDs (288/48) for CELLFRAME, and 45 RDs (2160/48) for the certified FRAME+EFR. The chair itself is
  28 RDs in volume. This is a counting bound only, for radius-0 recipes.
- In the keyed families, almost every piece fails at once (arc consistency: some face has no partner in any orientation); the
  tileable ones repeat quickly (index <= 8). Symmetric keys, the only exhaustive ones here, give the piece too few distinct faces.
- Unkeyed poly-RDs to 7 cells all tile with at most 4 pieces per period.

## LEADS
1. A keyed RD with no symmetry is a 3D tiling problem with 48 orientation states per site, and is not ruled out; random sampling does
   not reach it (39 999 of 40 000 paired pieces are untileable). A directed search would start from a known strongly aperiodic
   rule set of at most 48 states that is rotation-equivariant; none is known to us.
2. Keyed poly-RDs of 6 or more cells: the capacity bound above allows CELLFRAME-sized information; to try only if DICTO wants it.
3. Unkeyed poly-RDs n = 8 (about 1.3 x 10^5 free pieces, from growth 131 -> 1211 -> 12 734): dbb-scale, torus index to 8n.
