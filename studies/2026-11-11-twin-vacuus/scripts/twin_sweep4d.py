# twin_sweep4d.py, DICTO 11 Nov 2026 ("sometimes extra fins are hidden in 4D bodies" -> "run the 4D sweep test"). For hops k = 0 .. K of the
# OG family, the 4D sweep P = {(y, lam): X_j.y - lam <= |X_j|^2} built from the REAL candidates X_j (polar corners n/d of D_k's faces) and
# from their TWINS X'_j (sqrt5 -> -sqrt5, exact). Walls = 2-faces of P between two cells (= pairs of cells adjacent in some slice); each
# carries one 4D fin (cone from the centre over the wall). A wall that is an edge of the TOP slice (all cells present) or of the BOTTOM
# slice (lam = 0) shows as a fin of a 3D Angelus/Vacuus; a wall present only in between (born and ending at exchanges) is HIDDEN: a fin
# of the 4D body that no end slice shows. Per hop and side: cells, cells at top/bottom, walls, top-slice edges, bottom-slice edges,
# hidden walls. Control: real hop 0 bottom = active set of the hull test; slices pass Euler (og_exchanges.slice_sides).
# usage: python -u twin_sweep4d.py <five-fold-octet dir> <K> <out.json>
import sys, os, json, time
ARGS = list(sys.argv); ARGS[3] = os.path.abspath(ARGS[3]); here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
sys.argv = [ARGS[0], ARGS[1], '0', '0', '/dev/null']
exec(open(os.path.join(here, 'og_exchanges.py')).read().split('for k in range(KMAX + 1):')[0])
_keep = dict(faces=faces, symmetrise=symmetrise)
sys.argv = [ARGS[0], ARGS[1], '0', '/dev/null']; exec(open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0])
faces, symmetrise = _keep['faces'], _keep['symmetrise']
import numpy as np
K, OUTJ = int(ARGS[2]), os.path.abspath(ARGS[3])
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
def sweep_counts(X, tag):
    X = X / np.linalg.norm(X, axis=1).max(); b = np.einsum('ij,ij->i', X, X); n = len(X)
    LAM, toplam = choose_LAM(X, b); ev0 = events(X, b, LAM, TOL)
    lv = np.array(sorted(set(np.round([e[0] for e in ev0], 9)), reverse=True))
    cuts = list((lv[:-1] + lv[1:]) / 2) if len(lv) > 1 else []
    top = min(LAM * 0.9, max(toplam * 2, toplam + 0.1)); levels = [top] + cuts + ([lv[-1] / 2] if len(lv) else []) + [0.0]
    adj = [set(tuple(sorted(p)) for p in adjacency(X, b, l)[0]) for l in levels]
    alive_top = (slice_sides(X, b, top)[0] > 0); alive_bot = (slice_sides(X, b, 0.0)[0] > 0)
    walls = set().union(*adj); vis_top = adj[0]; vis_bot = adj[-1]; hidden = walls - vis_top - vis_bot
    r = dict(tag=tag, cells=n, cells_top=int(alive_top.sum()), cells_bottom=int(alive_bot.sum()), walls=len(walls), top_edges=len(vis_top),
             bottom_edges=len(vis_bot), hidden_walls=len(hidden), events=len(ev0))
    print(f"   {tag:5s}: cells {n} (top {r['cells_top']}, bottom {r['cells_bottom']}) | walls (4D fins) {len(walls)} = top-slice edges {len(vis_top)} + bottom-slice edges {len(vis_bot)} (shared {len(vis_top & vis_bot)}) + HIDDEN {len(hidden)} | events {len(ev0)}", flush=True)
    return r, alive_bot
rows = []; ok = True; t0 = time.time(); W = [tuple(cv(x) for x in v) for v in OG]
for k in range(K + 1):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    feet = []
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet.append(tuple(s_ * x for x in n_))
    feet = list(dict.fromkeys(feet))
    Wr = np.array([fl(v) for v in feet]); Wt = np.array([[twinf(x) for x in v] for v in feet])
    Xr = Wr / np.einsum('ij,ij->i', Wr, Wr)[:, None]; Xt = Wt / np.einsum('ij,ij->i', Wt, Wt)[:, None]
    print(f'hop {k}: {len(feet)} candidates ({time.time() - t0:.0f}s)', flush=True)
    rr, bot = sweep_counts(Xr, 'real'); rt, _ = sweep_counts(Xt, 'twin')
    if k == 0:
        h = ConvexHull(Wr); act = np.zeros(len(Wr), bool); act[h.vertices] = True; ok &= bool((bot == act).all())
    rows.append(dict(k=k, real=rr, twin=rt)); print(f'PROGRESS {(k + 1) / (K + 1):.3f}', flush=True)
    W = feet
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('hidden 4D fins by hop (real, twin):', [(r['k'], r['real']['hidden_walls'], r['twin']['hidden_walls']) for r in rows])
print('FINAL ok' if ok else 'FINAL FAIL: real hop-0 bottom slice differs from the hull test')
