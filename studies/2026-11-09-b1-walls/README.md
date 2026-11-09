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
