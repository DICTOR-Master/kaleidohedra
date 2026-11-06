"""Align the 13 nests of the nested Dodeca-13 (DICTO 11-06 "align the turns"): the central nest keeps its octahedron on the axes; each
outer nest is the MIRROR IMAGE of the central nest in the pentagon the two dodecahedra share. Checks: the mirrored icosahedron is exactly
the outer dodecahedron's own (its face centres), and the mirrored O, C, T are among the outer dodecahedron's 10 nest choices (regular,
inside). Then the 13 octahedra / cubes / tetrahedra: how their axes meet across each shared face."""
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('nest13.py').read().split("dods = [V for r, V in parts")[0])
dods = [V for r, V in parts if r == 'dodeca']
ci = int(np.argmin([np.linalg.norm(V.mean(0)) for V in dods])); D0 = dods[ci]
def nest_axes(Dv):
    c = Dv.mean(0); I = np.array([f.mean(0) for f in faces(Dv)])
    mids = np.array([(I[i] + I[j]) / 2 for i, j in edges(I)]) - c; opts = []
    for a, b, e in itertools.combinations(range(len(mids)), 3):
        u = mids[[a, b, e]]; r = np.linalg.norm(u, axis=1)
        if np.allclose(r, r[0], atol=1e-6) and abs(u[0] @ u[1]) < 1e-5 and abs(u[0] @ u[2]) < 1e-5 and abs(u[1] @ u[2]) < 1e-5: opts.append(np.vstack([u, -u]) + c)
    return I, opts
I0, opts0 = nest_axes(D0)
O0 = min(opts0, key=lambda O: np.abs(np.abs(O - D0.mean(0)) - np.abs(O - D0.mean(0)).max(1, keepdims=True)).sum())  # most axis-aligned
C0 = np.array([f.mean(0) for f in faces(O0)])
E = edges(C0); T0 = [0]
for k in range(1, 8):
    if all((min(k, t), max(k, t)) not in E for t in T0): T0.append(k)
T0 = C0[T0[:4]]
def same(A, B): return len(A) == len(B) and all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-5 for a in A)
out = {'dodecahedra': [], 'nests': []}; okall = True
for k, Dv in enumerate(dods):
    if k == ci:
        out['dodecahedra'].append(Dv.tolist()); out['nests'].append({'I': I0.tolist(), 'O': O0.tolist(), 'C': C0.tolist(), 'T': T0.tolist()}); continue
    shared = np.array([p for p in Dv if np.min(np.linalg.norm(D0 - p, axis=1)) < 1e-5])
    assert len(shared) == 5, len(shared)
    c = shared.mean(0); n = np.cross(shared[1] - shared[0], shared[2] - shared[0]); n /= np.linalg.norm(n)
    M = lambda X: X - 2 * np.outer((X - c) @ n, n)
    I1, opts1 = nest_axes(Dv); O1, C1, T1 = M(O0), M(C0), M(T0)
    ok = same(M(I0), I1) and any(same(O1, o) for o in opts1) and inside(T1, C1) and inside(C1, O1) and inside(O1, I1) and inside(I1, Dv)
    okall &= ok
    out['dodecahedra'].append(Dv.tolist()); out['nests'].append({'I': I1.tolist(), 'O': O1.tolist(), 'C': C1.tolist(), 'T': T1.tolist()})
print("each outer nest = mirror of the centre's in the shared face, and one of its own choices:", okall)
# how the mirrored octahedra meet: angle between central and outer octahedron axes (should show their relation)
def axes(O): c = O.mean(0); return O[:3] - c
angs = set()
for nst in out['nests']:
    A = axes(np.array(nst['O'])); B = axes(O0)
    angs.add(tuple(sorted(round(float(np.degrees(np.arccos(min(1, abs(a @ b) / np.linalg.norm(a) / np.linalg.norm(b))))), 2) for a in A for b in B))[:3])
print("smallest angles between outer and central octahedron axes:", sorted(angs)[:4])
json.dump(out, open('../nest13-aligned.json', 'w')); print("FINAL", "ok" if okall else "FAIL")
