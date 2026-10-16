# Twelve OCD Stellas around a small icosahedron (DICTO 2026-10-16: "12 around a small icosa, filled out like Bodhi"). Float.
# The 12 sit on the 5-fold axes (their 12 farthest corners pointing in), pulled in until neighbours touch; the centre icosahedron (the
# crystal's icosahedron, corners on the 5-fold axes, scaled) grown until it touches them. Then the 20 three-fold gaps between the 12 are
# offered icosahedra flat on the centre's faces, as in the interlocking Atom 13. -> data/stella-ico13.txt, data/stella-ico13.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
R = json.load(open('data/crystal-render.json')); S = np.array(R['stella']['v']); I = np.array(R['ico']['v'])
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
PS, PI = planes(S), planes(I)
sc = lambda P, s: np.c_[P[:, :3], P[:, 3] * s]
def depth(PA, a, PB, b):
    H = np.vstack([np.c_[PA[:, :3], PA[:, 3] - PA[:, :3] @ a], np.c_[PB[:, :3], PB[:, 3] - PB[:, :3] @ b]]); A = H[:, :3]; bb = -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=bb, bounds=[(None, None)] * 3 + [(0, None)])
    return r.x[3] if r.success else 0
def bisect(bad, lo, hi, n=40):   # smallest value where bad() turns false (bad true at lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if bad(m): lo = m
        else: hi = m
    return hi
rr = np.linalg.norm(S, axis=1); U = S[rr > rr.max() - 1e-6]; U = U / np.linalg.norm(U, axis=1)[:, None]
i, j = next((i, j) for i, j in itertools.combinations(range(12), 2) if U[i] @ U[j] > 0.4)
t = bisect(lambda m: depth(PS, m * U[i], PS, m * U[j]) > 1e-6, 0.2, 3.0)
stel = [t * u for u in U]
worst = max(depth(PS, a, PS, b) for a, b in itertools.combinations(stel, 2))
s = bisect(lambda m: not (max(depth(sc(PI, m), np.zeros(3), PS, p) for p in stel) > 1e-6), 0.01, 2.0)   # largest centre without overlap
s = s if max(depth(sc(PI, s), np.zeros(3), PS, p) for p in stel) <= 1e-6 else s * 0.999
vS = ConvexHull(S).volume; vI = ConvexHull(I).volume
out = ['DICTO · dictospheres.com', 'Twelve OCD Stellas around a small icosahedron (float)',
       f'the 12 on the 5-fold axes pulled in until neighbours touch: distance {t:.5f} (the Atom 13 had 1.56743); worst overlap {worst:.1e}',
       f'centre icosahedron grown until it meets them: scale {s:.4f} of the crystal icosahedron']
h = ConvexHull(np.vstack([I * s] + [S + p for p in stel])).volume
out.append(f'13 solids fill {(12 * vS + vI * s ** 3) / h:.2%} of their outline')
# the 20 gaps over the centre's faces: icosahedra flat on its faces
rI = -PI[0, 3]; nf = [e[:3] for e in PI]
place = lambda k: [(s * rI + k * rI) * n for n in nf]
k = bisect(lambda m: not (max(max(depth(sc(PI, m), p, PS, q) for p in place(m) for q in stel),
                             max(depth(sc(PI, m), p, sc(PI, m), q) for p, q in itertools.combinations(place(m), 2))) > 1e-6), 0.0, 1.0)
k *= 0.999
h2 = ConvexHull(np.vstack([I * s] + [S + p for p in stel] + [I * k + p for p in place(k)])).volume
out += [f'20 icosahedra flat on the centre\'s faces in the gaps: largest scale {k:.4f}', f'33 solids fill {(12 * vS + vI * s ** 3 + 20 * vI * k ** 3) / h2:.2%} of their outline']
print('\n'.join(out)); open('data/stella-ico13.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'stella': R['stella'], 'ico': R['ico'], 'stel': [p.tolist() for p in stel], 'centre_scale': s, 'gap_scale': k, 'gaps': [p.tolist() for p in place(k)]}, open('data/stella-ico13.json', 'w'))
