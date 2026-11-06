"""Football scutoid study, step 3b part 2: the four-cell corners of the move, solved from exact distances.
Candidates from move_refine.py: a gained pair and a lost pair with no cell in common, at most 0.015 of a period apart (pixel thresholds
split one corner's gain and loss over a few slices). For each: start at the slice point where the four distances agree best, solve
dist equal for all four (bounded least squares), and ACCEPT only if the spread is < 1e-9 and no other cell is nearer than the four
(so it is a true corner of the partition). Reports the corner height (fraction of a period and length above the middle plane) and the
nearest feature of each body (face / edge / corner).
Run: STACK=tight python3 tools/runjob.py <this> <data file> <events json>"""
import os, sys, json, itertools, numpy as np
from scipy.optimize import least_squares
EVF = sys.argv[1]; EV = json.load(open(EVF)); sys.argv = sys.argv[:1]
src = open('move_vertex.py').read()
exec(src.split('# ---- the moves seen in cell_track')[0])
Mb = np.array([P1, P2, T]).T
cache = {}
def B(c):
    c = tuple(c)
    if c not in cache: cache[c] = body(c[0], c[1], c[2], c[3])
    return cache[c]
nm = lambda c: f"{'XY'[c[0]]}({c[1]:+d},{c[2]:+d},{c[3]:+d})"
ev = EV['events']; cand = []
imgs_l = [(kind, p, q, r) for p, q, r in itertools.product(range(-2, 3), range(-2, 3), range(-1, 3)) for kind in (0, 1)]   # same order as cut_cells.py
for e1_, e2_ in itertools.product(ev, ev):
    if abs(e1_['w'] - e2_['w']) > 0.015: continue
    for g in e1_['gained']:
        for l in e2_['lost']:
            if set(g) & set(l): continue
            q = tuple(sorted([imgs_l[g[0]], imgs_l[g[1]]])) + tuple(sorted([imgs_l[l[0]], imgs_l[l[1]]]))
            cand.append(((e1_['w'] + e2_['w']) / 2, q))
seen = set(); cands = []
for w, q in cand:
    key = frozenset(q)
    if key not in seen: seen.add(key); cands.append((w, q))
print(f"candidate quartets {len(cands)}")
near = [(k, p, q, r) for k in (0, 1) for p in range(-2, 3) for q in range(-2, 3) for r in (-1, 0, 1)]
acc = []
for w0, q in cands:
    bs = [B(c) for c in q]
    # start: scan the slice near the four centres
    cs = [np.mean(np.vstack([F_[1] for F_ in b[0]]), 0) for b in bs]
    mid = np.mean(cs, 0); best = None
    for du, dv in itertools.product(np.linspace(-0.25, 0.25, 41), repeat=2):
        x = mid + du * P1 + dv * P2
        c = np.linalg.solve(Mb, x); c[2] = w0; x = Mb @ c
        ds = [dist(x, b)[0] for b in bs]; s = np.ptp(ds)
        if best is None or s < best[0]: best = (s, c)
    c0 = best[1]
    f = lambda c: [dist(Mb @ c, bs[0])[0] - dist(Mb @ c, bs[i])[0] for i in (1, 2, 3)]
    r = least_squares(f, c0, bounds=(c0 - [0.1, 0.1, 0.03], c0 + [0.1, 0.1, 0.03]), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    x = Mb @ r.x; ds = [dist(x, b) for b in bs]; d0 = ds[0][0]; spread = np.ptp([d[0] for d in ds])
    others = [c for c in near if c not in q]
    dmin = min(dist(x, B(c))[0] for c in others)
    ok = spread < 1e-9 and dmin > d0 + 1e-9
    print(f"{' + '.join(nm(c) for c in q[:2])} gain / {' + '.join(nm(c) for c in q[2:])} lose, near w {w0:+.4f}: "
          f"{'CORNER' if ok else 'rejected'} at w = {r.x[2]:+.10f} ({r.x[2] * h:+.8f} above the middle plane); "
          f"common distance {d0:.10f} (spread {spread:.1e}; nearest other cell {dmin:.6f}); features {[d[1] for d in ds]}", flush=True)
    if ok: acc.append(dict(w=r.x[2], z=r.x[2] * h, cells=[nm(c) for c in q], dist=d0, features=[d[1] for d in ds], x=list(x)))
json.dump(acc, open(EVF.replace('data-move-events', 'data-corners'), 'w'), indent=1)
print(f"true corners {len(acc)} of {len(cands)} candidates")
print("FINAL ok" if acc else "FINAL FAIL (no candidate is a true corner)")
