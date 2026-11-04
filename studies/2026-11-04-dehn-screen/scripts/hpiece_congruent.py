import os, sys, math, itertools, numpy as np
from fractions import Fraction as Fr
lams = sys.argv[1:]
HEX = os.path.expanduser('~/kres-tmp/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as T
os.chdir(here); H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
def congruent(A, B):
    """find an isometry (rotation or reflection) mapping corner set A onto B; brute force on a base triple"""
    if len(A) != len(B): return None
    ca, cb = A.mean(0), B.mean(0); A0, B0 = A - ca, B - cb
    i, j, k = 0, 1, 2
    while abs(np.linalg.det(np.array([A0[i], A0[j], A0[k]]))) < 1e-6: k += 1
    for p, q, r in itertools.permutations(range(len(B)), 3):
        M1 = np.array([A0[i], A0[j], A0[k]]).T; M2 = np.array([B0[p], B0[q], B0[r]]).T
        R = M2 @ np.linalg.inv(M1)
        if not np.allclose(R.T @ R, np.eye(3), atol=1e-7): continue
        img = A0 @ R.T
        if all(np.min(np.linalg.norm(B0 - x, axis=1)) < 1e-7 for x in img): return R, cb - R @ ca
    return None
for l in lams:
    os.chdir(HEX); pieces, tz = T.tile('AB', 0, Fr(l)); os.chdir(here)
    S = [np.unique(np.round(np.array([cart(p) for p in P]), 10), axis=0) for k, up, s_, P, J in pieces]
    kinds = [k for k, *_ in pieces]
    for a, b in itertools.combinations(range(len(S)), 2):
        if kinds[a] != kinds[b]: continue
        r = congruent(S[a], S[b])
        print(f"λ={l}: {kinds[a]}#{a} ≅ {kinds[b]}#{b}:", 'NO' if r is None else f"yes, det {np.linalg.det(r[0]):+.0f}, translation {np.round(r[1], 6).tolist()}")
    # also: the h-tile as a whole = the period of the layer; tile volume vs per-ball volume
    print('  volumes', [round(float(__import__('scipy.spatial', fromlist=['ConvexHull']).ConvexHull(s).volume), 6) for s in S])
