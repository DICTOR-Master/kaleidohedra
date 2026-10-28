# Keyed HexOct, step 1 (2026-10-29): which tiles a HexOct tile shares faces with, and how much face area each.
# A face shared with a neighbour is where a key can go. Sampling (floats), on top of the exact tiles of tiles.py:
# points on every face of every piece of tile T0, pushed a hair outward, are looked up in the pieces of all tiles
# of layers L-2..L+2 (lateral range +-3); area is summed per neighbour (layer offset d, lattice offset du, dv).
import sys, itertools, math
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
from tiles import tile, types
from stackings import POS

H = math.sqrt(2 / 3)
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * math.sqrt(3) / 2, float(p[2]) * H])

def pieces_of(word, L, lam, shift):
    out = []
    for k, up, s, P, J in tile(word, L % len(word), lam)[0]:
        X = np.array([cart(p) for p in P]) + shift
        out.append(ConvexHull(X))
    return out

def inside(hull, q, tol=1e-9):
    return np.all(hull.equations[:, :3] @ q + hull.equations[:, 3] <= tol)

def contacts(word, L, lam, N=4000, eps=1e-6, seed=1):
    n = len(word); rng = np.random.default_rng(seed)
    T0 = pieces_of(word, L, lam, np.zeros(3))
    b0 = POS[word[L % n]]
    nb = []
    for d in range(-2, 3):
        bd = POS[word[(L + d) % n]]
        for i, j in itertools.product(range(-3, 4), repeat=2):
            if d == 0 and i == 0 and j == 0: continue
            du, dv = bd[0] - b0[0] + i, bd[1] - b0[1] + j
            nb.append(((d, du, dv), pieces_of(word, L + d, lam, cart((du, dv, d)))))
    area, gap, total = {}, 0.0, 0.0
    for h in T0:
        for simp, eq in zip(h.simplices, h.equations):
            A, B, C = h.points[simp]; a = np.linalg.norm(np.cross(B - A, C - A)) / 2
            if a < 1e-12: continue
            m = max(3, int(N * a))
            r = rng.random((m, 2)); f = r.sum(1) > 1; r[f] = 1 - r[f]
            pts = A + r[:, :1] * (B - A) + r[:, 1:] * (C - A) + eps * eq[:3]
            for q in pts:
                w = a / m
                if any(inside(g, q) for g in T0): continue
                total += w
                for key, ps in nb:
                    if any(inside(g, q) for g in ps):
                        area[key] = area.get(key, 0) + w; break
                else:
                    gap += w
    return area, gap, total

if __name__ == '__main__':
    cases = [('ABC', 1), ('AB', 0), ('ABAC', 0), ('ABAC', 1), ('ABABC', 2), ('ABACBC', 1)]
    lams = [Fr(-2, 5), Fr(-1, 3), Fr(0), Fr(1, 10), Fr(1, 4)]
    if len(sys.argv) > 1: cases = [cases[int(sys.argv[1])]]
    for word, L in cases:
        T = types(word); ctx = ''.join(T[(L + j) % len(word)] for j in range(-2, 3))
        for lam in lams:
            area, gap, total = contacts(word, L, lam, N=1500)
            print(f'\n{word} layer {L} type {T[L]} context {ctx} lambda {lam}: outer area {total:.4f}, unmatched {gap:.2e}')
            for d in range(-2, 3):
                row = sorted((k, v) for k, v in area.items() if k[0] == d and v > 1e-4 * total)
                if row:
                    print(f'  d={d:+d}: {len(row)} tiles: ' + ', '.join(f'({k[1]},{k[2]}) {v:.4f}' for k, v in row))
        sys.stdout.flush()
