"""Third PV option (DICTO 4 Nov): one block for any stacking — the classical 60° rhombohedron (octahedron + two tetrahedra) laid slab by slab.
Same 8-layer Fibonacci word as the Narcissus block. Slab k (layers k, k+1): rhombohedra with corner a layer-k ball and edges s·a, s·b (in the layer) and
c to the layer-(k+1) ball over the triangle (0, s·a, s·b); s = ±1 picked by the offset of layer k+1. Checks: no overlaps, volume = one ball each."""
import os, sys, math, json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
sys.path.insert(0, 'scripts/_lib'); import methods as Mt
HEX = os.path.expanduser('~/kres-tmp/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as T
os.chdir(here); H = math.sqrt(2/3); s3 = math.sqrt(3)
W = json.load(open('data/narcissus-together.json'))['word'][:9]
def cart(u, v, z): return np.array([u + v/2, v*s3/2, z*H])
pieces = []; cols = []
for k in range(8):
    p0 = np.array([float(x) for x in T.POS[W[k]]]); p1 = np.array([float(x) for x in T.POS[W[k + 1]]])
    d = (p1 - p0) % 1; s = 1 if np.allclose(d, [1/3, 1/3]) else -1; assert np.allclose(d, [1/3, 1/3]) or np.allclose(d, [2/3, 2/3]), d
    a, b, c = cart(s, 0, 0), cart(0, s, 0), cart(s/3, s/3, 1)
    for i, j in itertools.product(range(-2, 2), repeat=2):
        o = cart(p0[0] + i, p0[1] + j, k)
        X = np.array([o + x*a + y*b + z*c for x in (0, 1) for y in (0, 1) for z in (0, 1)])
        if np.linalg.norm((X.mean(0) - cart(0, 0, k))[:2]) < 1.9: pieces.append(X); cols.append(0x4fa3a5)
vol = [ConvexHull(X).volume for X in pieces]; assert all(abs(v - 1/math.sqrt(2)) < 1e-9 for v in vol)
cen = [X.mean(0) for X in pieces]; ov = sum(1 for i, j in itertools.combinations(range(len(pieces)), 2) if np.linalg.norm(cen[i] - cen[j]) < 2 and Mt.overlap(pieces[i], pieces[j]))
print('rhombohedra', len(pieces), 'overlaps', ov, 'word', W[:8])
allV = np.vstack(pieces); c0 = allV.mean(0); sc = 1.6/np.max(np.linalg.norm(allV - c0, axis=1))
V_all, F_all, FC, PR = [], [], [], []
for X, col in zip(pieces, cols):
    Y = (X - c0)*sc; h = ConvexHull(Y); fs = {}
    for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 7)), set()).update(sm)
    base = len(V_all); V_all += np.round(Y, 10).tolist(); st = len(F_all)
    for kk, idx in fs.items():
        n = np.array(kk[:3]); idx = list(idx); cc = Y[idx].mean(0); uu = Y[idx[0]] - cc; ww = np.cross(n, uu)
        F_all.append([base + int(i) for i in sorted(idx, key=lambda i: math.atan2((Y[i] - cc) @ ww, (Y[i] - cc) @ uu))]); FC.append(col)
    PR.append([st, len(F_all)])
json.dump({'word': W[:8], 'vertices': V_all, 'faces': F_all, 'faceColours': FC, 'parts': PR}, open('data/rhombo-stack.json', 'w'))
