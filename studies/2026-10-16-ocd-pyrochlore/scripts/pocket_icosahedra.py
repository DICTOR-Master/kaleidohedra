# Partner icosahedra in the holes (DICTO 2026-10-16: "trying partner with icosahedron differently?"). The body K (the stella cut, or the
# companion) on its bcc lattice spread by λ ≥ 1; an icosahedron in the copies' own icosahedral frame at every hole of one kind: the joint
# midpoints (4 per cell), the square-wall centres (3 per cell, octahedral holes) or the cell corners (6 per cell, tetrahedral holes). For each
# λ the icosahedron grows until it touches a copy or another icosahedron; report the best fill over λ. Float (LP overlap test).
# -> data/pocket-icosahedra.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
D = json.load(open('data/stella-cut-exact.json')); B = np.array(D['basis']).T if np.array(D['basis']).shape == (3, 3) else None
B = np.array(D['basis']).T                      # columns = basis vectors
CV = np.array(D['cell']['v']); Vcell = ConvexHull(CV).volume
R = {r['name']: np.array(r['v']) for r in json.load(open('data/companion-variants.json'))}
S = np.array(D['S']['v'])
# the companion in this frame: hull of the exact data's corners is in companion-variants (network frame = same as stella-cut-exact? check)
C = R['companion']
phi = (1 + 5 ** .5) / 2
def frame_ico(K):
    r = np.linalg.norm(K, axis=1); five = K[r > r.max() - 1e-6]; return five / np.linalg.norm(five, axis=1)[:, None]   # 12 five-fold directions
def eqs(V):
    E = ConvexHull(V).equations; n = E[:, :3] / np.linalg.norm(E[:, :3], axis=1)[:, None]; return n, -E[:, 3] / np.linalg.norm(E[:, :3], axis=1)
def depth(EA, sa, EB, sb):
    (na, da), (nb, db) = EA, EB; n = np.vstack([na, nb]); d = np.r_[da + na @ sa, db + nb @ sb]
    r = linprog([0, 0, 0, -1], A_ub=np.hstack([n, np.ones((len(n), 1))]), b_ub=d, bounds=[(None, None)] * 4, method='highs'); return -r.fun
def sites(kind):
    f = {'joints': [(.25, .25, .25)], 'square walls': [(.5, 0, 0)], 'cell corners': [(.5, .25, 0)]}[kind]
    return f
def run(name, K, kind):
    U = frame_ico(K); EK = eqs(K); vK = ConvexHull(K).volume
    # the lattice in cubic form: find the conventional cube from the basis (bcc: shortest vectors are the 8 joints ±(a/2)(±1,±1,±1))
    L = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3) if any(m)]
    L.sort(key=np.linalg.norm); short = L[:8]; a2 = np.linalg.norm(short[0]) * 2 / 3 ** .5   # a/2·√3 = |short|
    axes = []                                                            # cube axes: next-shortest vectors (length a)
    for v in L[8:14]:
        if not any(abs(abs(v @ w) / np.linalg.norm(v) / np.linalg.norm(w) - 1) < 1e-6 for w in axes): axes.append(v)
    A = np.array([v / np.linalg.norm(v) for v in axes[:3]]).T; a = np.linalg.norm(axes[0])
    # hole positions (all symmetry copies) in one conventional cell, via the cubic frame
    base = {'joints': [(.25, .25, .25)], 'square walls': [(.5, 0, 0)], 'cell corners': [(.5, .25, 0)]}[kind]
    H = set()
    for p in base:
        for perm in itertools.permutations(range(3)):
            for sg in itertools.product((1, -1), repeat=3):
                q = tuple(round((sg[i] * p[perm[i]]) % 1.0, 6) for i in range(3)); H.add(q)
    holes = [A @ (np.array(q) * a) for q in H]
    # keep holes modulo the bcc lattice
    uniq = []
    Binv = np.linalg.inv(B)
    for h in holes:
        f = Binv @ h; f = f - np.floor(f + 1e-9)
        if not any(np.allclose(f, g, atol=1e-6) for g in uniq): uniq.append(f)
    holes = [B @ f for f in uniq]
    ico0 = U[[0]] if False else None
    def ico(e):   # icosahedron of edge e, corners on the 12 five-fold directions
        I = U.copy(); s = e / np.min([np.linalg.norm(I[0] - I[j]) for j in range(1, 12)]); return I * s
    best = None
    for lam in np.linspace(1.0, 1.6, 25):
        Bl = B * lam; Lat = [Bl @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3)]
        hs = [lam * h for h in holes]
        if depth(EK, np.zeros(3), EK, Lat[0] if np.linalg.norm(Lat[0]) > 1e-9 else Lat[1]) > 1e-9 and lam == 1.0: pass
        # copies must not overlap: check nearest
        if max(depth(EK, np.zeros(3), EK, t) for t in Lat if 1e-9 < np.linalg.norm(t) < 3) > 1e-9: continue
        lo, hi = 0.0, 3.0
        for _ in range(28):
            e = (lo + hi) / 2; I = ico(e); EI = eqs(I); ok = True
            h0 = hs[0]
            for t in Lat:
                if np.linalg.norm(t - h0) < 2.6 and depth(EI, h0, EK, t) > 1e-9: ok = False; break
            if ok:
                for h in hs:
                    for t in Lat:
                        q = h + t
                        if 1e-9 < np.linalg.norm(q - h0) < 2.6 and depth(EI, h0, EI, q) > 1e-9: ok = False; break
                    if not ok: break
            lo, hi = (e, hi) if ok else (lo, e)
        e = lo; vI = ConvexHull(ico(e)).volume if e > 1e-6 else 0
        fill = (vK + len(holes) * vI) / abs(np.linalg.det(Bl))
        if best is None or fill > best[0]: best = (fill, lam, e, len(holes), (vK) / abs(np.linalg.det(Bl)))
    return best
out = ['DICTO · dictospheres.com', 'Partner icosahedra in the holes of the bcc packing (float)']
for name, K in (('stella cut', S), ('companion', C)):
    for kind in ('joints', 'square walls', 'cell corners'):
        f, lam, e, nh, fk = run(name, K, kind)
        out.append(f'  {name:10s} + icosahedra at the {kind:12s} ({nh} per cell): best fill {f:.4f} at spread λ = {lam:.3f}, icosahedron edge {e:.4f} (the body alone {fk:.4f})')
        print(out[-1], flush=True)
open('data/pocket-icosahedra.txt', 'w').write('\n'.join(out) + '\n')
