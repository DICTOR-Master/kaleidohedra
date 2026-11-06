# Independent check of candidate 13931 (edge key `0R0000N0NN0NN00R00`, mirror copies allowed)

Fable, 6 Nov 2026, as the skeptic. Nothing in the study was edited; scratch scripts live in `/tmp/cand` on dicto-big-brother.

## Verdict: PERIODIC FOUND (a gap in the periodic test, not a geometry bug)

The candidate has a periodic keyed filling of the all-straight stacking. Its period lattice is
`<3 a1, a1 + a2, (a1, 2H)>`: in-plane index 3 (the familiar three-site rotation), vertical period two slabs,
and the second double-slab shifted sideways by one site `a1`. The cell holds 12 pieces (3 sites x down/up x 2 slabs).
The filling was verified directly, placement by placement, on an 11 x 11 x 6-slab patch: 0 of its interior edge lines break the rod/notch rule.

`spiral_keys.py` cannot see this period. Its torus classes always use the vertical translation `(t0, pH)` with the
in-plane part `t0` chosen as the first match found (for the straight word this is `t0 = 0`), so for an in-plane sublattice
of index i it tests only 1 of the i lattices that share that sublattice. The skewed lattices are never tested, and their
unskewed multiples (`(0, 2iH)`) are not tested either, because `periodic_words` stops at the first vertical period that
closes (`SS`). The "no period up to index 12 (and 30, running)" results are therefore statements about unskewed lattices only.
The hnf30 job now running will not change this; it can be stopped (it is not mine, so I left it).

## Model audit

Independent code (`/tmp/cand/audit_geom.py`, run on the Pi; logs `audit_geom.log`, `audit_geom_STTS.log`), words `SSSS` and `STTS`, n = 3, 490 pieces each:

- (a) Edge lines. For every edge of every interior piece (144 and 216 edges) the pieces containing the quarter points of the edge were found by
  hull inequalities, and the dihedral angle of each piece at the edge was measured by sampling a small circle round the midpoint.
  Incidence lists agree with `structure()`'s `inner` in every case; every circle is covered exactly once (sum 1.000 within 2e-3); every model
  angle matches the sampled angle. Valences: hexagon edges (length 0.5774) 4, the twelve others (0.7071, 0.4082) 3, as `edge_census.py` found.
  No line key is split by rounding (no non-inner line whose edge points lie in more pieces than it lists).
- (b) Labels. For every placement `p` (reference corner i goes to corner p[i]) the explicit construction "reference edge (i, j) lands on (p[i], p[j])
  and carries lab[(i, j)]" agrees with `label_of` (which uses the inverse permutation) on all 18 edges of 20 pieces x 6 placements. Every
  placement is an exact isometry of the 10 corners (least-squares affine fit reproduces all corners to 1e-8), and the sign of its determinant equals
  `handed()`. Each piece has exactly 3 proper and 3 mirror alignments.
- (c) Torus identification. Classes are exact translates (corner offsets compared), boundary pieces only add lines that are fully surrounded, so
  nothing spurious is imposed; UNSAT on an unskewed torus is sound. The gap is the one above: skews are not enumerated. The control
  `00000000R000N000N0` is caught at (3,1,1) with skew 0 AND at skews a1, 2a1; the candidate is caught only at skews a1 and 2a1.
- (d) Mirror placements occupy the same cell (same corner set, improper isometry): valid for an achiral piece whose mirror-image keyed copy is allowed.

The SAT model itself (one-of-six placement per class; per line all plain, or one rod and the rest notches) encodes the stated rule correctly.

## Search

`/tmp/cand/skew.py LABELS imax n p mirrors`: same model, every HNF sublattice of index <= imax, every coset representative as skew, then a direct
re-check of each SAT torus on a patch two sites wider and one slab taller. Candidate, straight word, p = 2, index <= 6 (149 tori, log `cand-skew6.log`):
SAT at (3,1,1) skews a1, 2a1; (3,2,2) skews a2, a1, 2a1, 2a1+a2; (6,1,1) and (6,4,1) skews a1, 2a1, 4a1, 5a1. All are sublattices of the
index-3 one, so there is one period and its multiples. `describe.py` lists the filling: on the (3,1,1)/a1 torus there are exactly 3 solutions
(one pattern and its two in-plane translates). In slab 0 the down pieces are proper placements cycling through the three turns along a1 and
the up pieces are mirror placements cycling the other way; slab 1 has the roles swapped (down pieces mirrored, up pieces proper); then the
pair repeats with the a1 shift. Six of the twelve classes are mirror placements, which is why proper motions alone give no patch at all.

Nothing beyond index 6 was needed; task 2 (structure of large patches, strip transfer matrix, other stacking words) was not run.

## Other candidates

The scan (`all/w*.log`, still running at 22:10, 79 distinct CANDIDATE labels so far, all with mirror copies only, all with patch word SSSS)
was spot-checked on 12 labels (`spot.log`): every one is SAT on the same skewed torus (3,1,1) with skew a1 or 2a1, verified on the larger patch.
The labels are already canonical under the C3v symmetry of N (`canon`), so they are not symmetry copies of 13931; they are distinct keys that all
settle into the same shifted three-site rotation. Expect every CANDIDATE of the scan to fall this way: the scan's periodic test has the same gap.

## What would make it a theorem

- Fix the periodic test: enumerate skews (i per HNF of index i) or, equivalently, vertical periods up to 2i slabs; keep the direct re-check on a larger patch for every SAT torus.
- Then any design surviving tori up to a modest index deserves the structural work: extract a large patch filling and look for a hierarchy (substitution) or Sturmian rows; a 2D Wang-tile reduction of the straight stacking with a strip transfer matrix for periodic orbits.
- A real theorem needs an aperiodicity proof (hierarchical structure or a Kari-type invariant), not an absence of small periods.
- The three-site rotation with a per-double-slab shift is a cheap escape route for every three-fold edge key seen so far; a key that forces aperiodicity must break it, probably with labels that distinguish the a1 shift between slab pairs.

## Sources and scripts

- Study: `README.md`, `scripts/spiral_keys.py`, `scripts/n_slabs.py`, `scripts/edge_census.py` (this folder); `spiral_keys_hnf.py` on dicto-big-brother is byte-identical to `spiral_keys.py`.
- Logs read: `~/study-runs/2026-11-06-spiral/cand13931.log`, `cand13931-hnf.log`, `cand13931-big.log`, `cand13931-hnf30.log` (running), `control-hnf.log`, `all/w*.log`.
- Scratch (dicto-big-brother `/tmp/cand`): `cand_lib.py` (model copied from spiral_keys.py plus `classes_for_skew`), `audit_geom.py` + logs, `skew.py` + `cand-skew6.log`, `describe.py`, `spot.log`, `scan-cands.txt`. No job of mine is left running.
