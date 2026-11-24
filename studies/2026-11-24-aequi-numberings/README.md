# Aequi numberings: four face numberings and a name for each of the 1232 Aequi (24 November 2026)

For DICTO's Aequi picker (chosen 22 Nov: all four numberings, switchable per die). DATA ONLY: no app change yet.
App UI waits for DICTO's choice of syllable set (names below are a proposal).

**Status (09:15 JST): complete for all 1232 dice; checks.py FINAL ok (logs/checks.out).** The balanced refinement (limits
60 + 20) reached the dice up to N = 62 (624 dice, 571 improved); the larger dice keep their 8 + 4 (or 120 + 40) result. Continuing
it is optional; see "Resume".

## Counts (all 1232 dice; checks.py FINAL ok)

| scheme | dice | notes |
|---|---|---|
| plain | 1232 | |
| opposite (sum N + 1) | 276 | exactly the centrally symmetric dice (Ih 4, Oh 57, Th 215); 956 marked unavailable |
| spin-down | 1232 | a Hamiltonian **cycle** on every die (so N is also next to 1); no die needs a path |
| balanced | 1232 | corner spread **proved optimal for 14**; both stages proved for 2 (nos. 5, 9); the rest best found with the gap stated |

Proved optimal corner spread (no., N, spread): (5, 14, 5) (6, 18, 6) (7, 20, 9) (9, 10, 8) (10, 16, 10) (12, 18, 6) (13, 18, 6)
(59, 16, 9) (60, 16, 11) (61, 16, 9) (62, 16, 11) (63, 18, 6) (154, 36, 12) (240, 48, 98; mixed corner degrees).

The rest: the solver's lower bounds are weak, so the gaps are wide (one corner degree, 1043 dice: median gap 27, largest 163; mixed
corner degrees, 189 dice: median gap 10, largest 155). Best found is never claimed optimal. Smallest corner spreads: 5 (No.5),
6 (nos. 6, 12, 13, 63 with N = 18; nos. 24, 25 with N = 30). Where corners of different degree meet (189 dice), raw sums differ by
degree, so the spread there is large by construction (as asked: raw sums).

History of the run: the first 105 dice (largest N) ran with limits 120 + 40, 4 workers; the rest with 8 + 4, 2 workers, 50000 swap
steps, smallest N first. Stage 2 can lower the corner spread below the stage-1 value; the stored `corner_spread` is the spread of the
stored numbers (`corner_spread_stage1` keeps the stage-1 value; scripts/fix_spreads.py corrected the first runs, which had stored
the stage-1 value for 62 dice). Each die records its own limits (`det_time`, and `refined` if the refinement pass ran on it). Refinement keeps the better
numbering (corner spread, then neighbour spread) and the larger proved corner bound of the two runs.

## Data

- `src/dice.json`: the picker's data, byte-identical to the app's `aequi/dice.json` (1232 dice).
- `data/dice/NNNN.json`, one per die, NNNN = the picker number n (1..1232, the row of the classification CSV of study
  2026-11-24-aequi-vacuus-scutoids). Fields: `name`, `name_shown` ("Minana (No.377)"), `N`, `corners`, `face_direction`
  (picker direction index of each face), `face_vertices` (corner cycle of each face), `corner_faces` (faces at each corner),
  `lattice_check`, `schemes` with `plain`, `opposite`, `balanced`, `spin_down`: each `numbers[i]` = the number on face i.
- Face i = the picker's face order: the planes of the die's orbits in the order of `o`, each orbit's directions in the group's
  listed order (every plane is a face, checked).
- `names.csv`: n, name, name shown.

## Method (scripts/numberings.py)

Face lattice: directions exact in Q(φ)³, depths the 60-digit fair depths of the search records; candidate corners in float64, each
recomputed at 70 digits: its planes pass through it (residual < 1e-45), every other plane clears it by at least the recorded
`min_slack` (> 1e-12 required). Then F = N, corners = catalogue, side counts = catalogue, every edge on two faces, V − E + F = 2.

1. **plain**: face i gets i + 1.
2. **opposite** (opposites sum to N + 1): centrally symmetric dice only (exact, classification CSV); faces paired by exactly opposite
   directions; the k-th pair in face order gets k on its lower face, N + 1 − k on the other. Other dice: `available: false`.
3. **balanced**: stage 1 minimises the spread (max − min) of the corner sums (sum of the numbers on the faces at a corner; raw sums,
   also where corners of different degree meet); stage 2 keeps that corner spread and minimises the spread of the neighbour sums
   (numbers on the faces sharing an edge with each face). OR-tools CP-SAT (assignment model, 4 workers, interleaved deterministic
   search, seed 0, deterministic limits 120 + 40), started from a seeded swap search. OPTIMAL only with a proof (bound = value);
   otherwise FEASIBLE with the solver's lower bound: the gap is stated per die.
4. **spin_down**: consecutive numbers on adjacent faces. Hamiltonian cycle of the face-adjacency graph by CP-SAT AddCircuit (1 on face
   0, 2 on its lower-index neighbour on the cycle); if none is found, a Hamiltonian path (1 at the end with the lower face index), and
   `hamiltonian_cycle` says "proved absent" or "unknown".

## Names (APPROVED by DICTO 24 Nov)

Each die's name is its picker number read digit by digit in goroawase syllables: 0 o/re/maru, 1 i/hi, 2 ni/fu, 3 mi/sa, 4 yo/shi,
5 go/ko, 6 mu/ro, 7 na, 8 ya/ha, 9 ku (DICTO's candidate set, 22 Nov). **Rule:** the first reading of each digit, except that a
digit whose first reading would repeat the syllable just before it takes its second reading (7 has one reading, so "na na" stays).
First letter capitalised; shown with the number: "Minana (No.377)". The syllable sets of different digits are disjoint;
checks.py parses every name in every possible way and finds exactly its own number, and all 1232 names are distinct.

## Checks (scripts/checks.py → logs/checks.out)

Independent of numberings.py: the face lattice is rebuilt from the picker's float data and must give the same corners; then in
integers: every scheme a bijection onto 1..N; plain; opposite present exactly for centrally symmetric dice and each face plus its
opposite = N + 1; balanced spreads recomputed, bound ≤ value, OPTIMAL only when bound = value; spin-down steps on adjacent faces
(and N next to 1 for a cycle); names by the rule, distinct, decoding uniquely.

## Resume

Each die is written to its own file as soon as it is done; finished dice are skipped on restart. To resume on the compute host:

    cd <k-research>/studies/2026-11-24-aequi-numberings
    MODE=refine WORKERS=4 T1=60 T2=20 ITERS=200000 python scripts/numberings.py data/dice --procs 6 && python scripts/checks.py . | tee logs/checks.out

(MODE=fast fills plain/opposite/spin-down for any missing die with balanced pending; MODE=balanced fills every pending balanced; MODE=refine reruns every non-optimal die whose limits are below T1 and keeps the better
numbering and the larger proved bound.)

(Python with ortools, numpy, mpmath; the sibling study 2026-11-24-aequi-vacuus-scutoids and the two search studies must be present.)

- 24 Nov 09:08: refinement stopped for the 10:00 power cut at 626/1232 (smallest first); final checks FINAL ok (1232 dice, balanced optimal proved for 14, both measures for 2). Resume: same command, plan aequi-numrefine.
- 24 Nov afternoon: refinement resumed after the power cut (job aequi-numrefine2) and finished all 1232 dice (FINAL ok): balanced optimum proved for 14 dice, both stages for 2; the others keep the best found with bound and gap. Per-die name_shown changed to the decided format "Name (No.N)". No further refinement (DICTO decision 13, 24 Nov).
