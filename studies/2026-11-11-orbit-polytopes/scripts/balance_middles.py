"""The balance law (#104 Theorem 4) at every chain's middle (DICTO 11 Nov: "go on with the balance law in B4"). For the bitruncated
5-cell, tesseract, 24-cell and 600-cell: the two cell kinds are the two Wythoff types (cells of type {1,2,3} and {2,3,4}, from the
fundamental weights at the two ends of the chain; in B4 and H4 they differ in shape, in A4 and F4 they are congruent). Prediction:
in every generic sweep, W-W -> R-R swaps = R-R -> W-W swaps = (R-R faces) - (R cells) + 1 = (W-W faces) - (W cells) + 1.
Sweep: at a corner with exactly 2 downward edges, the contact lost is between the two cells whose shared face is spanned by the two
down edges, and the contact gained is between the two cells whose shared face is spanned by the two up edges (#104 Theorem 1)."""
import sys, itertools
import numpy as np
from collections import Counter
sys.argv = ['x', '--no-h4']
exec(open('vacuus_middles.py').read().split('def run(')[0])
def build(R, lab):
    R, bonds = chain(R); G = group(R); Rm = np.array(R)
    x = np.linalg.solve(Rm, np.array(lab, float))
    P = []
    for y in (g @ x for g in G):
        if not P or np.linalg.norm(np.array(P) - y, axis=1).min() > 1e-6: P.append(y)
    P = np.array(P); W = np.linalg.inv(Rm); cells = {}
    for j in (0, 3):                                     # the cells of the two end types: normals in the orbits of w_1 and w_4
        seen = []
        for g in G:
            d = unit(g @ W[:, j])
            if seen and (np.array(seen) @ d).max() > 1 - 1e-9: continue
            seen.append(d); hv = P @ d; top = frozenset(np.where(hv > hv.max() - 1e-7)[0])
            if len(top) >= 4 and np.linalg.matrix_rank(P[list(top)] - P[list(top)].mean(0), tol=1e-7) == 3: cells[top] = 'W' if j == 0 else 'R'
    return P, cells, bonds
def sweep_counts(P, cells, dirs):
    nn = np.min([np.linalg.norm(P - p, axis=1)[np.linalg.norm(P - p, axis=1) > 1e-9].min() for p in P[:50]])
    nb = [np.where(np.abs(np.linalg.norm(P - p, axis=1) - nn) < 1e-6)[0] for p in P]
    assert all(len(b) == 4 for b in nb), Counter(len(b) for b in nb)
    by_v = {}
    for c, k in cells.items():
        for v in c: by_v.setdefault(v, []).append((c, k))
    out = []
    for u in dirs:
        h = P @ u; cnt = Counter()
        for v in range(len(P)):
            down = [w for w in nb[v] if h[w] < h[v]]; up = [w for w in nb[v] if h[w] > h[v]]
            if len(down) != 2: continue
            def pair(e2):     # the two cells at v containing both edges v-e2[0], v-e2[1]
                return tuple(sorted(k for c, k in by_v[v] if e2[0] in c and e2[1] in c))
            lost, gained = pair(down), pair(up)
            cnt[''.join(lost) + '->' + ''.join(gained)] += 1
        out.append(cnt)
    return out
rng = np.random.default_rng(11); ok = True
for name, R in [('A4 bitruncated 5-cell', A4), ('B4 bitruncated tesseract', B4), ('F4 bitruncated 24-cell', F4), ('H4 bitruncated 600-cell (control: 601)', H4)]:
    P, cells, bonds = build(R, (0, 1, 1, 0)); kinds = Counter(cells.values())
    faces = Counter()
    for (c1, k1), (c2, k2) in itertools.combinations(cells.items(), 2):
        sh = c1 & c2
        if len(sh) >= 3: faces[''.join(sorted((k1, k2)))] += 1
    predW = faces['WW'] - kinds['W'] + 1; predR = faces['RR'] - kinds['R'] + 1
    dirs = [unit(rng.normal(size=4)) for _ in range(4 if 'H4' in name else 9)]
    res = sweep_counts(P, cells, dirs)
    swaps = [(c['WW->RR'], c['RR->WW']) for c in res]
    good = predW == predR and all(a == predW and b == predW for a, b in swaps); ok &= good
    print(f"{name}: chain {bonds}, {len(P)} corners, cells W {kinds['W']} R {kinds['R']}, faces {dict(faces)}; predicted {predW} = {predR}; "
          f"sweeps (WW->RR, RR->WW) {swaps}; mixed swaps {[c['RW->RW'] for c in res]}: {'BALANCED as predicted' if good else 'MISMATCH'}", flush=True)
print('FINAL ok' if ok else 'FINAL FAIL')
