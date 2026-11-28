# Hollow-straw criterion (27 November 2026)

DICTO · study. The question is DICTO's ("attack gap 1, the Hollow-straw criterion"; map MAP-VACUUS-AND-KNOWN-MATHEMATICS-2026-11-27).
With Claude (Anthropic). **Question:** for a core K and a fair die D with the same number of faces and a pairing of their faces, when is
DICTO's Hollow-straw transformation (both ends fixed; every face plane of K moves and turns into its partner plane of D, all together:
a_k(lam) = (1 - lam) a_k + lam m_sigma(k)) NESTED (each intermediate solid inside the next, so the straws fill the shell without
overlap), and when does it make exactly the needed neighbour changes?

Known case: C116 -> Minana #377, nested, exactly the 18 floor swaps, proved exactly (study 2026-11-24-aequi-vacuus-scutoids).

## Step 1: exploration (scripts/hs_general.py, run_explore.sh; logs/hs_*.log; data/hs_*.json) — numerical
Pilot: C116/#377 nested and minimal at core sizes 0.6 and 0.8 (also under a second pairing, 24 changes); C60/#1 (same pattern) no
changes; C60/#18 nested at size 0.6, NOT nested at 0.8 (first sign of a size condition). Full run: C60 x 354, C80 x 283, C140 x 28
dice, sizes 0.5, 0.7, 0.9 (core circumradius / die inradius). Results: below when the run ends.

## Sources checked for the gap (27 Nov)
Search "morphing between convex polyhedra of different combinatorial type, face-plane interpolation, flips, nested": closest found
A. Shapiro, A. Tal, Polyhedron realization for shape transformation (Technion; record only: vertex correspondence by merging the two
edge structures, then interpolating vertices; lists non-self-intersection as open); Gregory et al. (UNC TR 98-014, feature-based
morphing, record only); Erickson and Lin (planar morphs of one fixed graph, record only). Scutoids: Gómez-Gálvez et al. 2018 (opened):
Voronoi seeds on two surfaces. Nothing found on interpolating paired FACE PLANES between two fixed polyhedra, or on when that is nested.
Not a proof that it is new.

## Lemma (proved, 27 Nov): nested exactly when every intermediate solid lies inside the die
Planes a . x = 1; a_k(lam) = (1 - lam) a_k + lam m_k (m_k the partner plane of the die D). For x on face k of P(lam):
(1 - lam) a_k . x + lam m_k . x = 1, so a_k . x = (1 - lam m_k . x)/(1 - lam), and the rate at which face k moves at x is
d/dlam [a_k(lam) . x] = (m_k - a_k) . x = (m_k . x - 1)/(1 - lam)   (lam < 1).
So face k moves outward at x (the nesting condition checked numerically and exactly) iff m_k . x <= 1: the corner lies inside the
die's partner half-space. Hence: if every P(lam) lies inside D, the transformation is nested; conversely, if it is nested, then
P(lam) lies inside P(1) = D. **Nested <=> P(lam) is inside the die for every lam.** (Elementary; any core, any die, any pairing.)

## Step 1 data (C60 x 14, C80 x 28, C140 running; core sizes 0.5, 0.7, 0.9; numerical)
- Smallest core (0.5): nested in every pair so far (45/45). Middle (0.7): one C60 failure (die 91). Largest (0.9): many fail
  (C60 4 of 14, C80 14 of 28). Consistent with the lemma: a bigger core bulges the intermediate solids out through the die.
- Fewest changes ("minimal"): fails mainly for dice whose corners are not all three-way (they change by more than swaps) and for
  pairings where a neighbour pair is lost and later regained.
- Same pattern (no change needed): C60 always nested; C80 die 112 (same pattern) not nested at 0.9: nesting is not only about swaps.
Next: (1) test the FACING condition: each core face's normal points through its partner die face (the floating-resin aim); conjecture:
facing => nested for every small enough core; (2) finish C140; (3) exact proofs for the clean cases.

## Step 2: facing and the largest nested core size (logs/facing_C60.log, facing_C80.log; numerical, bisection to 1/128)
For each pair: how many core faces point through their partner die face (facing), and the largest core size (core circumradius /
die inradius) at which the transformation is still nested, rho*.
- C60 x 14 dice: facing 32/32 in all; rho* from 0.66 (die 91) to 0.99 (the top of the range tested: dice 1, 27, 90, 152, 242).
- C80 x 28 dice: facing 42/42 in 25, 30/42 in 3 (dice 347-349); rho* from 0.75 (die 164) to 0.99 (dice 2, 334, 557, 558).
- In all 42 pairs the transformation is nested for every core size up to rho* (>= 0.66): a small enough core always works.
Facing alone does not explain rho* (all-facing pairs range from 0.66 to 0.99; the three 30/42 pairs still reach about 0.78).
Conjecture (open): for every face pairing there is a core size below which DICTO's Hollow-straw transformation is nested; by the
lemma this says every intermediate solid stays inside the die once the core is small enough. Next: an argument via the polar
(the polar of P(lam) is the hull of the points (1 - lam) a_k + lam m_k), and the exact check of a few cases.

## C140 (Goldberg GP(2,1), insphere form) x 28 dice of 72 faces: nested 28/28 at core sizes 0.5 and 0.7, 11/28 at 0.9;
fewest changes 21/28 at 0.5 (failures mostly dice whose corners are not all three-way).
**Overall (C60, C80, C140; 70 pairs): at core size 0.5 every pair is nested (70/70).** Numerical; the conjecture above stands.

## Step 3 (28 Nov): EXACT certificates for the next Scutoid-Frusta bridging solids (DICTO: "deploy yes and parallel testing")
scripts/hs_exact.py generalises the C116 -> Minana #377 certificate (2026-11-24-aequi-vacuus-scutoids/scripts/c116_transform_exact.py)
to any core and die, with the floating-resin pairing of hs_general.py (same seed, NST=150 as the sample runs). (A) start and end
patterns exact and closed, (B) every event isolated exactly, (C) nested, (D) the events are exactly the needed neighbour changes,
one swap each. Candidates (from the sample runs: nested at core size 0.9, exactly the needed changes, fewest changes > 0):
C60 -> Kuo #90 (6 changes), C80 -> Nioku #209 (12), C140 = GP(2,1) -> Kuomu #906 (12); all at core size 0.7.
Negative control: C60 -> die 18 at core size 0.8 (numerically not nested) must fail (C).
Note: the first runs' (A) lines print "pattern = C116 / Minana #377 under the pairing" (a label left from the C116 script, fixed
afterwards); in these logs they mean the core and the die.
RESULTS (28 Nov): C60 -> Kuo #90 at core size 0.7: EXACT (FINAL ok, logs on host hsx-kuo90b): (A) both end patterns exact and
closed; (B) 6 events, every state exact and closed; (C) nested; (D) exactly the 6 needed swaps, one per event (all near lam 0.9408:
the core's 1e-9 rounding splits the symmetric group into swaps about 1e-10 apart; states are now got by the four-face flip and
verified exactly, as float labels could not resolve them). Negative control C60 -> die 18 at 0.8: FAILS (C) as required.
C80 -> Nioku #209 and C140 -> Kuomu #906: rerunning with the fix.
C80 -> Nioku #209 at core size 0.7: EXACT (FINAL ok, hsx-nioku209b): (A)-(D) hold, 12 events, exactly the 12 needed swaps. C140 -> Kuomu #906 running.
C140 (Goldberg GP(2,1)) -> Kuomu #906 at core size 0.7: EXACT (FINAL ok, hsx-kuomu906b): (A)-(D), 12 events, exactly the 12 needed swaps. All three candidates exact. Next (DICTO decision 2): full search per face count to confirm each is the best die; then a page each for the Scutoid-Frusta bridging solids dropdown.
FULL SEARCH (28 Nov, hs-full-C60 / hs-full-C80): only dice that amber_aequus can build (the 1232 finished dice) can be tested; all
340 further 32-face dice (and the further 42-face dice) of the 10 725 catalogue were skipped (cannot build: IndexError). So the
sample runs already covered EVERY buildable die of these face counts: Kuo #90, Nioku #209 and Kuomu #906 are the picks among all
buildable dice. To widen: build the remaining dice as solids first (their fair depths exactly, as for the 1232), then rerun.

## Step 4 (28 Nov): the REVERSE (DICTO: "reversing changes from Aequi to Goldberg"; yes to the restatement: the fair die as the
inner core, its faces growing out into the Goldberg/fullerene solid). hs_exact.py SWAP=1: inner = the die turned back by R^T and
scaled so its circumradius is 0.7 of the core solid's inradius; outer = the core solid; same face pairing; both solids' planes
rounded to 1e-9 (exact certificate for these inputs).
- Kuo #90 -> C60: EXACT (hsr-kuo90): (A)-(D), 6 events, exactly the 6 needed swaps.
- Nioku #209 -> C80: EXACT (hsr-nioku209): (A)-(D), 12 events, exactly the 12 needed swaps.
(Their logs print the forward wording "pattern = the core / the die" and "GPc -> die ... core planes rounded"; in these runs the start
is the die and the end the core solid, both rounded. Labels fixed afterwards.)
- Kuomu #906 -> C140: EXACT (hsr-kuomu906): (A)-(D), 12 events, exactly the 12 needed swaps. All three reverses exact.
Context (DICTO 28 Nov: "a scope investigation said that goldberg polyhedra were non-starters"): the 21 Nov Goldberg study
(2026-11-21-amber-goldberg, 152 runs) found Goldberg cores in LATTICE moulds give 0 scutoids (their faces are the Voronoi cells of their
tangent points; scutoids need large faces meeting small ones). Here the outer solid is a fair die, whose different face pattern forces
the swaps: both directions exact for C60, C80, C140. Closed gap -> #124 next version (now numerical only there, Section on other cores).
