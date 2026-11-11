# og_topslice.py, DICTO 11 Nov 2026 ("derive and reduce possibilities" -> "yes run possibility 1"). §35: step A1 <=> 6 - m_cut > m_survive
# - 6 + 12/a at the TOP of the sweep. The top slice is D_k with its corners split by the weights b_j = |X_j|^2. Per face (orbit class):
# sides in D_k (the unperturbed limit), sides at the top (just above the highest event), extra = top - D_k (sides gained from corner
# splits), and whether it dies (cut). Tables: (sides in D_k, sides at top) -> faces dying / surviving; look for the rule.
# Controls: top slice simple (sum of sides = 6n - 12), all faces present at the top; cut set = hull test.
# usage: python -u og_topslice.py <five-fold-octet dir> <kmin> <kmax> <out.json>
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__)); ARGS = list(sys.argv)
sys.argv = [ARGS[0], ARGS[1], ARGS[2], ARGS[3], '/dev/null']
exec(open(os.path.join(here, 'og_exchanges.py')).read().split('for k in range(KMAX + 1):')[0])
import numpy as np
OUTJ = os.path.abspath(ARGS[4]); rows = []; ok_all = True; t0 = time.time()
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    if k < KMIN: V, FF = W, FN; continue
    act = np.zeros(len(W), bool); act[cor2] = True
    X = W / np.einsum('ij,ij->i', W, W)[:, None]; X /= np.linalg.norm(X, axis=1).max(); b = np.einsum('ij,ij->i', X, X); n = len(X)
    LAM, toplam = choose_LAM(X, b)
    lam_top = min(LAM * 0.9, max(toplam * 2, toplam + 0.1))
    s_top, Vt, Et, Ft = slice_sides(X, b, lam_top)
    s_dk, _, _, _ = slice_sides(X, np.zeros(n), 1.0)                       # unperturbed: {X_j.y <= 1} = D_k (up to scale)
    simple = bool(int(s_top.sum()) == 6 * n - 12 and (s_top > 0).all()); allpresent = bool((s_top > 0).all()); ok_all &= allpresent   # symmetric ties stay degenerate without a random tie-break (og_exchanges), so "simple" is reported, not required
    tree = cKDTree(X); perms = [tree.query(X @ g.T)[1] for g in Gf]; orb = -np.ones(n, int); reps = []
    for i in range(n):
        if orb[i] < 0:
            for p_ in perms: orb[p_[i]] = len(reps)
            reps.append(i)
    tab = {}; per_orbit = []
    for o, i in enumerate(reps):
        size = int((orb == o).sum()); key = (int(s_dk[i]), int(s_top[i]))
        e = tab.setdefault(key, [0, 0]); e[0 if not act[i] else 1] += size
        per_orbit.append(dict(size=size, sides_Dk=int(s_dk[i]), sides_top=int(s_top[i]), extra=int(s_top[i] - s_dk[i]), dies=bool(not act[i]),
                              radius=float(np.linalg.norm(X[i]))))
    cut = ~act; mc = s_top[cut].mean() if cut.any() else float('nan'); ma = s_top[act].mean(); a = int(act.sum())
    rows.append(dict(k=k, n=n, cut=int(cut.sum()), table={f'{kk[0]}->{kk[1]}': v for kk, v in sorted(tab.items())}, orbits=per_orbit, m_cut=float(mc), m_surv=float(ma), simple=simple))
    print(f'PROGRESS {(k - KMIN + 1) / (KMAX - KMIN + 1):.3f}', flush=True)
    print(f'k {k:2d}: n {n} cut {int(cut.sum())} | top simple {simple} | m_cut {mc:.3f} m_surv {ma:.3f} | deficit {6 - mc:.3f} vs excess {ma - 6 + 12 / a:.3f}', flush=True)
    print('      (sides in D_k -> sides at top): [dying, surviving] faces  ' + '  '.join(f'{kk[0]}->{kk[1]}: {v}' for kk, v in sorted(tab.items())), flush=True)
    die_o = [p for p in per_orbit if p['dies']]; srv_o = [p for p in per_orbit if not p['dies']]
    print(f'      dying orbits: ' + ', '.join(f"{p['size']}x({p['sides_Dk']}->{p['sides_top']}, |X| {p['radius']:.4f})" for p in die_o), flush=True)
    print(f'      radius |X| of dying orbits min {min([p["radius"] for p in die_o], default=float("nan")):.4f} | surviving orbits max {max(p["radius"] for p in srv_o):.4f}', flush=True)
    V, FF = W, FN
json.dump(rows, open(OUTJ, 'w'), indent=1)
# candidate rules
allp = [(r['k'], p) for r in rows for p in r['orbits']]
for name, rule in (('top sides <= 5', lambda p: p['sides_top'] <= 5), ('extra == 0', lambda p: p['extra'] == 0), ('top sides < sides in D_k', lambda p: p['sides_top'] < p['sides_Dk']),
                   ('sides in D_k == 3', lambda p: p['sides_Dk'] == 3)):
    tp = sum(p['size'] for k_, p in allp if rule(p) and p['dies']); fp = sum(p['size'] for k_, p in allp if rule(p) and not p['dies']); fn = sum(p['size'] for k_, p in allp if not rule(p) and p['dies'])
    print(f'rule "{name}" -> dies: right {tp}, wrongly flagged survivors {fp}, missed dying {fn}')
print('FINAL ok' if ok_all else 'FINAL FAIL: a face missing at the top')
