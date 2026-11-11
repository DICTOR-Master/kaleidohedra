# og_vacuus4d.py, DICTO 11 Nov 2026 ("most likely a 4D vacuus that is very sophisticated", "c the permutahedron 4D vacuus", "yes go ahead").
# The hop's 4D sweep P = {(y, lam): X_j.y - lam <= b_j} (og_sweep.py, og_exchanges.py). Its 2-faces are the WALLS (i, j) between cells.
# As for the 4D permutohedron (central 3D slices carrying all 2-faces), take a centre c = (0, 0, 0, lc) on the slider axis (the only
# I_h-fixed points) and the central hyperplane through c containing wall (i, j): normal nu(lc) = (lc + b_j)(X_i, -1) - (lc + b_i)(X_j, -1)
# = lc*A + C with A = (X_i - X_j, 0), C = (b_j X_i - b_i X_j, b_i - b_j). Two walls share a slice where nu1 || nu2: all 2x2 minors of
# [nu1; nu2] vanish; each minor is quadratic in lc, so the SPECIAL HEIGHTS are exact roots (a grid scan would miss them).
# Per level: walls; N(lc) = number of distinct central slices at generic lc and at every special height; the heights where N drops most;
# there: slice classes by what they carry (walls between active-active, active-cut, cut-cut cells) and whether a slice class separates
# cut from surviving cells. Control: N(generic) = walls minus identically-coincident pairs; counts invariant under I_h.
# usage: python -u og_vacuus4d.py <five-fold-octet dir> <kmin> <kmax> <out.json>
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'og_exchanges.py')).read().split('for k in range(KMAX + 1):')[0]
exec(src)
import numpy as np
t0 = time.time(); rows = []; ok_all = True
def slice_normals(lc, Wp, X, b):
    i, j = Wp[:, 0], Wp[:, 1]
    nu = np.hstack([(lc + b[j])[:, None] * X[i] - (lc + b[i])[:, None] * X[j], (-(lc + b[j]) + (lc + b[i]))[:, None]])
    nu /= np.linalg.norm(nu, axis=1)[:, None]
    s = np.sign(nu[np.arange(len(nu)), np.argmax(np.abs(nu) > 1e-9, axis=1)]); nu *= s[:, None]
    return nu
def count_slices(nu, tol=1e-8):
    key = np.round(nu / tol).astype(np.int64)
    u, inv = np.unique(key, axis=0, return_inverse=True); return len(u), inv.ravel()
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    if k < KMIN: V, FF = W, FN; continue
    act = np.zeros(len(W), bool); act[cor2] = True
    X = W / np.einsum('ij,ij->i', W, W)[:, None]; X /= np.linalg.norm(X, axis=1).max()
    b = np.einsum('ij,ij->i', X, X); n = len(X)
    LAM, toplam = choose_LAM(X, b)
    ev0 = events(X, b, LAM, TOL)
    lv = np.array(sorted(set(np.round([e[0] for e in ev0], 9)), reverse=True))
    cuts = np.array([0.0] + list((lv[:-1] + lv[1:]) / 2) + [lv[-1] / 2]) if len(lv) else np.array([0.0, LAM / 2])
    cuts[0] = min(LAM * 0.9, max(toplam * 2, toplam + 0.1))
    walls = set()
    for l in list(cuts) + [0.0]:
        for pr in adjacency(X, b, l)[0]: walls.add(tuple(sorted(pr)))
    Wp = np.array(sorted(walls)); nW = len(Wp)
    i, j = Wp[:, 0], Wp[:, 1]
    A = np.hstack([X[i] - X[j], np.zeros((nW, 1))]); C = np.hstack([b[j][:, None] * X[i] - b[i][:, None] * X[j], (b[i] - b[j])[:, None]])
    # special heights: for each wall w1 (orbit reps would suffice; all walls, vectorised per w1) and every w2: minor (0,1)..(2,3)
    cand = {}
    for w1 in range(nW):
        a1, c1 = A[w1], C[w1]
        best = None
        for (p, q) in ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)):
            # det [[l a1p + c1p, l a1q + c1q], [l a2p + c2p, l a2q + c2q]] = alpha l^2 + beta l + gamma
            al = a1[p] * A[:, q] - a1[q] * A[:, p]
            be = a1[p] * C[:, q] + c1[p] * A[:, q] - a1[q] * C[:, p] - c1[q] * A[:, p]
            ga = c1[p] * C[:, q] - c1[q] * C[:, p]
            if best is None or np.abs(np.stack([al, be, ga])).sum() > np.abs(np.stack(best)).sum(): best = (al, be, ga)
        al, be, ga = best
        sc = np.abs(np.stack([al, be, ga])).max(0) + 1e-300
        al, be, ga = al / sc, be / sc, ga / sc
        roots = []
        quad = np.abs(al) > 1e-12
        disc = be ** 2 - 4 * al * ga
        okq = quad & (disc >= -1e-12); sq = np.sqrt(np.maximum(disc, 0))
        for sgn in (1, -1):
            r = np.where(okq, (-be + sgn * sq) / np.where(quad, 2 * al, 1), np.nan); roots.append(r)
        lin = ~quad & (np.abs(be) > 1e-12); roots.append(np.where(lin, -ga / np.where(lin, be, 1), np.nan))
        for r in roots:
            for w2 in np.where(np.isfinite(r) & (np.arange(nW) > w1))[0]:
                lc = float(r[w2])
                if abs(lc) > 50: continue
                nu1 = lc * A[w1] + C[w1]; nu2 = lc * A[w2] + C[w2]
                if np.linalg.norm(nu1) < 1e-12 or np.linalg.norm(nu2) < 1e-12: continue
                if abs(abs(nu1 @ nu2) / (np.linalg.norm(nu1) * np.linalg.norm(nu2)) - 1) < 1e-11:
                    key = round(lc, 7); cand[key] = cand.get(key, 0) + 1
    gen = [0.12345, 0.4321, -0.2718]
    Ngen = [count_slices(slice_normals(g, Wp, X, b))[0] for g in gen]
    gen_ok = len(set(Ngen)) == 1; ok_all &= gen_ok
    top = sorted(cand.items(), key=lambda kv: -kv[1])[:8]
    best_rows = []
    for lc, npairs in top:
        Nn, inv = count_slices(slice_normals(lc, Wp, X, b))
        typ = act[i].astype(int) + act[j].astype(int)                 # 2 = active-active, 1 = active-cut, 0 = cut-cut
        mix = {}
        for s_ in range(Nn):
            ts = tuple(sorted(set(typ[inv == s_].tolist())));
            mix[ts] = mix.get(ts, 0) + 1
        best_rows.append(dict(lc=lc, pairs=npairs, N=Nn, slice_mix={str(kk): v for kk, v in mix.items()}))
    rows.append(dict(k=k, n=n, cut=int((~act).sum()), walls=nW, N_generic=Ngen[0], special=best_rows, n_special_heights=len(cand)))
    print(f'PROGRESS {(k - KMIN + 1) / (KMAX - KMIN + 1):.3f}', flush=True)
    print(f'k {k:2d}: cells {n} (cut {int((~act).sum())}) | walls {nW} | generic slices {Ngen[0]} (same at 3 heights: {gen_ok}) | special heights {len(cand)}', flush=True)
    for r_ in best_rows[:5]:
        print(f'      lc {r_["lc"]:+.6f}: {r_["pairs"]} coinciding wall pairs -> {r_["N"]} slices (drop {Ngen[0] - r_["N"]}) | slices by carried wall types (2 aa,1 ac,0 cc): {r_["slice_mix"]}', flush=True)
    V, FF = W, FN
json.dump(rows, open(OUT, 'w'), indent=1)
print('FINAL ok' if ok_all else 'FINAL FAIL: generic slice count differs between generic heights')
