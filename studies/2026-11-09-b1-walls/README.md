# Boulder B1: walls along the sliders (#86, #80/#81, #61), restarted 10 Nov 2026
Scripts: tower_walls.py (#86), chain_sym.py / chain_sym5.py (#80, #81, DICTO's growth rule T with the depth as a symbol),
swap4.py (#61 below s = 1/4). Run on the compute machine; logs in data/.

**#86 tower walls: DONE (FINAL ok).** On each chamber of the weight walk every combinatorial type is fixed between walls; the exact
check of #86 holds at every wall and at one point of every hop.
- c: chambers [−3/8, −1/8] (wall −7/24) and [−1/8, 3/8] (walls 1/24, 1/8); 15 exact checks.
- h: chambers [−1/8, 5/24] (10 walls: −5/72, −1/40, −1/72, 0, 1/24, 3/40, 7/72, 1/8, 11/72, 7/40) and [5/24, 3/8] (walls 1/4, 19/72);
  47 exact checks.
**#80 cube chain:** the sample s0 = 3/4 is itself a wall (the script stops by design); rerun at s0 = 5/7.
**#81 dodecahedron chain (s0 = 3/4):** steps 0–3: 32 → 60 → 32 → 30 corners, hops (1, (5 − √5)/2) then (1, 3/2); full run restarted.
**#61 swap rule below 1/4:** waits for its parameter lists (λ values, words) to be rebuilt from #61.
**10 Nov, attention check:** #80 cube chain (s0 = 5/7) stopped at step 6: the morning run died silently after step 5 (no watcher),
the watched rerun spent 25+ min in step 6 with no output; step 5 already needed a degree-19 hop polynomial (10 min). Exact symbolic
stepping is exhausted here (ledger: METHOD-FAILED at step 6). Next method: numerical steps at 60 digits for several s0 in the hop to
find the closure step, then an exact check of that one step. #81 dodecahedron chain: step 5 running (2.5 GB, 25 min); stop and switch
method too if no step 5 line by the next check.
**10 Nov, attention check:** #81 dodecahedron chain stopped at its deadline (step 5: 36 min, no output, 2.5 GB). Steps 0–4 exact; step 4
repeats step 0's corner count and kinds (32 corners, all 4-valent: {4: 30}) but is NOT similar to it by the exact test: a near-closure
worth a numerical look (is it the same shape up to a stretch?). Ledger: METHOD-FAILED at step 5. Both chains now wait for the
numerical-steps method (60 digits, several s0, then one exact check).

## #81 dodecahedron chain: ANSWER (10 Nov 2026, after the similarity-test fix)
- **Exact:** chain_sym5.py (depth s as a symbol, fixed value test): the chain CLOSES with period 4 from step 0; step 4 = step 0 scaled
  by 35 − 15√5 = 10/φ⁴, an identity in s on the combinatorial type at s0 = 3/4 (FINAL ok). chain_exact_fixed5.py confirms at s0 = 3/4
  in Q(√5). (The script's printed hop [1, (5−√5)/2] is an artefact: its range is clipped to the slider window [1, 3/2].)
- **Map of the depth (chain_num5.py, steps to 8–16, 0.02 grid):** s 0.40–1.00: period 4 from step 0; 1.02–1.08: period 4 entered
  at step 3; ≈1.10–1.24: NO closure, the chain grows without bound (corners 440 → 5292 by step 14) and rounds out (r/R → 0.97, the
  #43 behaviour); 1.26–1.38: period 4 from step 1; 1.40–1.48: period 2 from step 0.
- Earlier 'no closure' verdicts came from the representation-comparison bug (fixed, guarded, Concordance modus operandi).
Next: exact walls between the regimes (near 1.01, 1.09, 1.25, 1.39); the cube chain #80 rerun the same way (its 'no closure' had the
same bug).

## #80 cube chain: map (10 Nov 2026, chain_num.py, numerical; corner counts match the exact steps 0–5 at 5/7)
| depth s | behaviour | scale per cycle |
|---|---|---|
| 0.50 | period 4 from step 0 | 5/2 |
| 0.52–0.60 | period 4 from step 3 | varies (1.8667 at 0.56) |
| 0.62–0.74 | NO closure: grows without bound (1122 corners by step 12 at 5/7) | – |
| 0.76–0.98 | period 4 from step 1 | varies (2.0998 at 0.86, 2.5605 at 0.94) |
| 1.00 | period 2 from step 0 | 3 |
The paper's sample depth 5/7 ≈ 0.714 lies in the only non-closing window: that is why the exact chain ran for hours.
**Common pattern with #81:** the same five regimes in the same order (dodecahedron: ≤1.00 period 4 from 0 with constant scale 10/φ⁴;
1.02–1.08 from step 3; ≈1.10–1.24 none; 1.26–1.38 from step 1; ≥1.40 period 2). The period-2 scales are #80's gains: 3 (cube) and
15 − 6√5 = 1.583592… (dodecahedron, numerically 1.583592135), #43's constant. Exact check of the cube's step-1 regime at s = 43/50
running (plan b1-cube-exact).
