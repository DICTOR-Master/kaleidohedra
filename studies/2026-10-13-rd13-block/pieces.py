# DICTO Spheroid-13 RD, research batch 2 (2026-10-13): each piece kind's faces (side lengths), dihedral angles and volume, its own
# roundness, and how the pieces meet: within the block and across blocks.
# Usage: python3 pieces.py rd13-round-m0.15.json
import sys, json, itertools, numpy as np
R = json.load(open(sys.argv[1])); L = np.array(R['L'], float)
def cell(ci):
    V, F = [], []
    for f in R['cells'][ci]:
        idx = []
        for p in f:
            k = next((i for i, w in enumerate(V) if np.allclose(w, p, atol=1e-7)), None)
            if k is None: V.append(p); k = len(V) - 1
            idx.append(k)
        F.append(idx)
    V = np.array(V); c = V.mean(0)
    F = [f if np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]) @ (V[f].mean(0) - c) > 0 else f[::-1] for f in F]
    return V, F
def area(V, F): return sum(0.5 * np.linalg.norm(np.cross(V[f[i]] - V[f[0]], V[f[i + 1]] - V[f[0]])) for f in F for i in range(1, len(f) - 1))
def vol(V, F):
    c = V.mean(0); return sum(abs(np.linalg.det(np.array([V[f[0]] - c, V[f[i]] - c, V[f[i + 1]] - c]))) / 6 for f in F for i in range(1, len(f) - 1))
def normal(V, f): n = np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]); return n / np.linalg.norm(n)
def dihedrals(V, F):
    out = []
    for a, b in itertools.combinations(range(len(F)), 2):
        if len(set(F[a]) & set(F[b])) == 2: out.append(180 - np.degrees(np.arccos(np.clip(normal(V, F[a]) @ normal(V, F[b]), -1, 1))))
    return out
kinds = {}
for ci, v in enumerate(R['volumes']):
    k = 'centre' if ci == 0 else ('outer A' if abs(v - R['volumes'][1]) < 1e-3 else 'outer B')
    kinds.setdefault(k, ci)
print(f"thickness {R['margin']}")
for k, ci in kinds.items():
    V, F = cell(ci); d = dihedrals(V, F); a = area(V, F); vv = vol(V, F)
    sides = sorted(round(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % 4]])), 4) for f in F for i in range(4))
    print(f"  {k:8s} volume {vv:.4f}  surface {a:.4f}  roundness {36*np.pi*vv**2/a**3:.3f}  edges {min(sides):.3f}-{max(sides):.3f}  dihedrals {min(d):.1f}-{max(d):.1f} deg  (an RD: 120 exactly)")
# contacts: which pieces share a face, within the block and with the six neighbouring blocks
allc = [(b, ci) for b in range(7) for ci in range(13)]
shift = [np.zeros(3)] + [s * t for t in L for s in (1, -1)]
faces = {}
for b, ci in allc:
    for f in R['cells'][ci]:
        key = tuple(sorted(tuple(np.round(np.array(p) + shift[b], 5)) for p in f))
        faces.setdefault(key, []).append((b, ci))
pairs = [v for v in faces.values() if len(v) == 2]
inner = sum(1 for (b1, c1), (b2, c2) in pairs if b1 == b2 == 0)
cross = [(c1 if b1 == 0 else c2) for (b1, c1), (b2, c2) in pairs if (b1 == 0) != (b2 == 0)]
print('  faces shared inside one block:', inner, '| block faces meeting a neighbouring block:', len(cross), '| of those on the centre:', cross.count(0))
