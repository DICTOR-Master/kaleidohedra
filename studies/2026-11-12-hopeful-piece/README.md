# The hunt for a hopeful piece (12 Nov 2026, aim 3: one piece, any stacking)
DICTO: "put more work on dbb aim 3". Keying stays PAUSED (DICTO 12 Nov, "until another hopeful piece comes to us"), so this study
does not refine or key any marked set; it hunts for the new piece itself: ONE piece whose shape alone (bumps and dents, no colour
labels) admits no periodic filling.

**Conclusion:** no hopeful piece. Among 6 385 243 keyed RDs (every symmetry class with |G| >= 3, exhaustive) plus 40 000 random
paired ones, and all 14 102 unkeyed poly-RDs up to 7 cells, every piece is either untileable or periodic. In these families every keyed RD that fills
a ball of radius 2 repeats with at most 8 pieces per period; every poly-RD up to 7 cells repeats with at most 4 pieces per period.
Status: SETTLED for these families (a closed route, not a proof for keyed RDs with no symmetry). Keying stays paused.

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
