# DICTO Spheroid-13 RD, the centre piece (DICTO 2026-10-13: "nothing about the 13th block"): its symmetry, its kinds of face and
# corner, and how far it is from a rhombic dodecahedron of the same volume. Usage: python3 centre.py rd13-round-m0.08.json ...
import sys, json, itertools, numpy as np
ops = []
for perm in itertools.permutations(range(3)):
    for s in itertools.product([1, -1], repeat=3):
        M = np.zeros((3, 3)); [M.__setitem__((i, p), s[i]) for i, p in enumerate(perm)]; ops.append(M)
NB = [np.array(v, float) for v in itertools.product([-1, 0, 1], repeat=3) if sorted(map(abs, v)) == [0, 1, 1]]
def rd():   # the plain centre cell, same corner order as the honeycomb's
    out = []
    for n in NB:
        i, j = [k for k in range(3) if n[k]]; k = 3 - i - j; e = np.eye(3)
        out.append([n[i] * e[i], (n[i] * e[i] + n[j] * e[j] + e[k]) / 2, n[j] * e[j], (n[i] * e[i] + n[j] * e[j] - e[k]) / 2])
    return out
for fn in sys.argv[1:]:
    R = json.load(open(fn)); faces = [np.array(f) for f in R['cells'][0]]; plain = rd()
    V = np.unique(np.round(np.concatenate(faces), 7), axis=0); c = V.mean(0); faces = [f - c for f in faces]; V = V - c
    sym = [M for M in ops if all(np.min(np.linalg.norm(V - M @ v, axis=1)) < 1e-5 for v in V)]
    proper = sum(1 for M in sym if np.linalg.det(M) > 0)
    # face kinds: sorted side lengths and diagonals
    def sig(f):
        s = sorted(round(float(np.linalg.norm(f[i] - f[(i + 1) % 4])), 4) for i in range(4)); d = sorted(round(float(np.linalg.norm(f[i] - f[i + 2])), 4) for i in range(2))
        return tuple(s + d)
    kinds = {}
    for f in faces: kinds.setdefault(sig(f), 0); kinds[sig(f)] += 1
    # corners: where four faces meet (the cube-type six) and three (the eight); distances from the middle
    cnt = {tuple(np.round(v, 5)): 0 for v in V}
    for f in faces:
        for p in f: cnt[tuple(np.round(p, 5))] += 1
    four = [np.linalg.norm(v) for v, n in zip(V, [cnt[tuple(np.round(v, 5))] for v in V]) if n == 4]
    three = [np.linalg.norm(v) for v, n in zip(V, [cnt[tuple(np.round(v, 5))] for v in V]) if n == 3]
    vol = R['volumes'][0]
    # distance from a rhombic dodecahedron: same corner correspondence, scaled to the same volume, best turn (Kabsch)
    A = np.concatenate([np.array(f) for f in plain]); B = np.concatenate(faces)
    A = A * (vol / 2) ** (1 / 3)
    H = A.T @ B; U, S, Vt = np.linalg.svd(H); Rm = Vt.T @ np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]) @ U.T
    dev = np.linalg.norm(A @ Rm.T - B, axis=1)
    edge = 0.866 * (vol / 2) ** (1 / 3)
    print(f"thickness {R['margin']}: volume {vol:.4f} (= {vol/2:.3f} RD) | symmetry order {len(sym)} ({proper} turns) | "
          f"{len(kinds)} kinds of face: {sorted(kinds.values(), reverse=True)} | four-face corners at {min(four):.3f}-{max(four):.3f}, three-face at {min(three):.3f}-{max(three):.3f} | "
          f"farthest corner from the matching RD's: {dev.max():.3f} ({100 * dev.max() / edge:.0f}% of that RD's edge)")
