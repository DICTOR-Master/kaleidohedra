# DICTO · partial Vacuus 1b, checks (26 Nov 2026): distinct depths per solid, closed forms, and whether the pits are interior-disjoint
# (the excavated body is a solid). With Claude (Anthropic).
import json, os, sys, itertools
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])   # the solids in their canonical frames
found = json.load(open(os.path.join(HERE, '../data-special-all.json')))
rng = np.random.default_rng(1)
def pits(P, s):
    V, F, N, D = S[P]; out = []
    for fi, f in enumerate(F): out.append((V[f], s * D[fi] * N[fi]))
    return out
def inside_pyr(x, base, apex):
    # point strictly inside the pyramid with polygon base and apex: on the inner side of every wall and of the base plane
    c = (base.mean(0) * len(base) + apex) / (len(base) + 1)
    planes = [(base[i], base[(i + 1) % len(base)], apex) for i in range(len(base))] + [(base[0], base[1], base[2])]
    for a, b, d in planes:
        n = np.cross(b - a, d - a)
        if np.sign(n @ (x - a)) != np.sign(n @ (c - a)) or abs(n @ (x - a)) < 1e-9 * np.linalg.norm(n): return False
    return True
res = {}
for f in found:
    key = (f['P'], round(f['s'], 7))
    res.setdefault(key, []).append(f['Q'])
out = []
for (P, s), Qs in sorted(res.items()):
    pl = pits(P, s); ok = True
    for i, (bi, ai) in enumerate(pl):
        for _ in range(60):
            w = rng.dirichlet(np.ones(len(bi) + 1)); x = w[:-1] @ bi + w[-1] * ai
            for j, (bj, aj) in enumerate(pl):
                if j != i and inside_pyr(x, bj, aj): ok = False; break
            if not ok: break
        if not ok: break
    r2, r5 = sp.sqrt(2), sp.sqrt(5)
    cf = None
    for basis in ([r2], [r5], [r2, r5], [sp.sqrt(3)]):
        g = sp.nsimplify(s, basis, tolerance=1e-7)
        if len(str(g)) < 30: cf = str(g); break
    out.append(dict(P=P, s=s, closed_form=cf, pits_disjoint=ok, on=Qs))
    print(f"{P:28s} s = {s:.7f} = {cf}  pits disjoint: {ok}  walls on: {', '.join(Qs)}", flush=True)
json.dump(out, open(os.path.join(HERE, '../data-special-distinct.json'), 'w'), indent=1)
print('FINAL ok' if out else 'FINAL FAIL')
