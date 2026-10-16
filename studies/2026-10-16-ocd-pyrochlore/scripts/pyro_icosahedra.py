# Pyrochlore partner (DICTO 2026-10-16: "pyrochlore network perhaps"): the body K (stella cut or companion) on ONE network of the OCD
# packing (the diamond network whose joints form the pyrochlore lattice: sites A and A + t0, A on the fcc lattice of network.json), and an
# icosahedron in the copies' own frame at every site of the empty second network (A + 2t0, A + 3t0). Positions spread by λ; for each λ the
# icosahedron grows until it touches; report the best fill. Float (LP overlap test). -> data/pyro-icosahedra.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T
D = json.load(open('data/stella-cut-exact.json')); S = np.array(D['S']['v'])
C = np.array({r['name']: r['v'] for r in json.load(open('data/companion-variants.json'))}['companion'])
def eqs(V):
    E = ConvexHull(V).equations; n = E[:, :3] / np.linalg.norm(E[:, :3], axis=1)[:, None]; return n, -E[:, 3] / np.linalg.norm(E[:, :3], axis=1)
def depth(EA, sa, EB, sb):
    (na, da), (nb, db) = EA, EB; n = np.vstack([na, nb]); d = np.r_[da + na @ sa, db + nb @ sb]
    return -linprog([0, 0, 0, -1], A_ub=np.hstack([n, np.ones((len(n), 1))]), b_ub=d, bounds=[(None, None)] * 4, method='highs').fun
cellv = abs(np.linalg.det(Lb))
def run(K, scan):
    EK = eqs(K); vK = ConvexHull(K).volume
    r = np.linalg.norm(K, axis=1); U = K[r > r.max() - 1e-6]; U = U / np.linalg.norm(U, axis=1)[:, None]
    assert len(U) == 12
    def ico(e): return U * (e / min(np.linalg.norm(U[0] - U[j]) for j in range(1, 12)))
    best = None
    for lam in scan:
        A = [lam * (Lb @ np.array(m, float)) for m in itertools.product(range(-2, 3), repeat=3)]
        net1 = [a for a in A] + [a + lam * T[0] for a in A]; net2 = [a + 2 * lam * T[0] for a in A] + [a + 3 * lam * T[0] for a in A]
        near1 = [p for p in net1 if np.linalg.norm(p) < 3.5]
        if max(depth(EK, np.zeros(3), EK, p) for p in near1 if np.linalg.norm(p) > 1e-9) > 1e-9: continue
        h0 = min(net2, key=np.linalg.norm)
        lo, hi = 0.0, 3.0
        for _ in range(26):
            e = (lo + hi) / 2; EI = eqs(ico(e)); ok = True
            for p in net1:
                if np.linalg.norm(p - h0) < 3.0 and depth(EI, h0, EK, p) > 1e-9: ok = False; break
            if ok:
                for q in net2:
                    if 1e-9 < np.linalg.norm(q - h0) < 3.0 and depth(EI, h0, EI, q) > 1e-9: ok = False; break
            lo, hi = (e, hi) if ok else (lo, e)
        vI = ConvexHull(ico(lo)).volume if lo > 1e-6 else 0
        fill = 2 * (vK + vI) / (lam ** 3 * cellv)
        row = (fill, lam, lo, 2 * vK / (lam ** 3 * cellv), 2 * vI / (lam ** 3 * cellv))
        if best is None or fill > best[0]: best = row
    return best
out = ['DICTO · dictospheres.com', 'Pyrochlore partner: body on one network, icosahedra on the empty second network (float)',
       f'  primitive fcc cell {cellv:.5f} holds 2 sites of each network; the OCD double network fills 0.7743, one network alone half of that']
for name, K in (('stella cut', S), ('companion', C)):
    b = run(K, np.linspace(0.9, 1.5, 25))
    out.append(f'  {name:10s}: best fill {b[0]:.4f} at spread λ = {b[1]:.3f} (body {b[3]:.4f} + icosahedra {b[4]:.4f}), icosahedron edge {b[2]:.4f}')
    print(out[-1], flush=True)
open('data/pyro-icosahedra.txt', 'w').write('\n'.join(out) + '\n')
