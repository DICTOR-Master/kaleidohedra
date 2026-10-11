# Seeding patterns (DICTO 2026-10-12: does any form other than the icosahedron multiply?). For each form X and each axis family
# (5-fold: 12 directions, 3-fold: 20, 2-fold: 30), copies X(1) in the same turn are pushed out along each axis until they touch the
# outer X(phi^k) (k = 1..4). Kept when the copies lie inside and do not overlap (separating axes with real edges); then the largest
# centred X that misses them, flagged when its edge is an exact power of phi. Volumes reported (copies + centre vs outer).
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open(__file__.replace('seeding.py', 'network_screen.py')).read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def faces(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
def edgevecs(V):
    H = ConvexHull(V); E = set(); F = faces(V)
    for s in H.simplices:
        for a, b in itertools.combinations(s, 2):
            on = [f for f in F if abs(V[a] @ f[:3] + f[3]) < 1e-9 and abs(V[b] @ f[:3] + f[3]) < 1e-9]
            if len(on) >= 2: E.add((min(a, b), max(a, b)))
    return [V[a] - V[b] for a, b in E]
EV = {X: edgevecs(ref[X]) for X in FORMS}; FC = {X: faces(ref[X]) for X in FORMS}
def overlap(A, B, X):
    axes = list(FC[X][:, :3])
    for u in EV[X]:
        for v in EV[X]:
            w = np.cross(u, v)
            if np.linalg.norm(w) > 1e-9: axes.append(w / np.linalg.norm(w))
    for ax in axes:
        a, b = A @ ax, B @ ax
        if a.max() <= b.min() + 1e-7 or b.max() <= a.min() + 1e-7: return False
    return True
I = ref['I']
AX = {'5-fold (12)': I / np.linalg.norm(I, axis=1)[:, None]}
D = ref['D']; AX['3-fold (20)'] = D / np.linalg.norm(D, axis=1)[:, None]
ID = ref['ID']; AX['2-fold (30)'] = ID / np.linalg.norm(ID, axis=1)[:, None]
for X in FORMS:
    V = ref[X]; vX = ConvexHull(V).volume
    for axname, U in AX.items():
        for k in range(1, 5):
            outer = V * PHI ** k; FO = faces(outer)
            def place(u):
                t = min((-f[3] - (V @ f[:3]).max()) / (f[:3] @ u) for f in FO if f[:3] @ u > 1e-9)
                return V + t * u
            copies = [place(u) for u in U]
            if any(np.linalg.norm(c.mean(0)) < 1e-6 for c in copies[:1]): continue
            n_ov = sum(overlap(copies[0], c, X) for c in copies[1:])
            room = vX * PHI ** (3 * k) - len(U) * vX
            if n_ov:
                print(f'{X:2s} {axname:12s} outer phi^{k}: copies overlap ({n_ov} neighbours of copy 0)', flush=True); continue
            lo, hi = 0.0, PHI ** k
            for _ in range(40):
                m = (lo + hi) / 2
                if overlap(V * m, copies[0], X): hi = m
                else: lo = m
            kk = np.log(lo) / np.log(PHI) if lo > 1e-9 else float('nan')
            tag = f'= phi^{round(kk)}' if lo > 1e-9 and abs(kk - round(kk)) < 1e-4 else ''
            print(f'{X:2s} {axname:12s} outer phi^{k}: {len(U)} copies fit (volume {len(U) * vX:.3f} of {vX * PHI ** (3 * k):.3f}); centred copy fits up to edge {lo:.5f} {tag}', flush=True)
