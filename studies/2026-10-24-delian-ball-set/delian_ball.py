# Delian Ball set (DICTO 10-24, "similar to our dimpled octet set"): grow the rounded tetrahedron of DICTO Ball set 1 (roundtet_octet.py,
# the app's ball set) evenly about its hole centre by a factor k (corner balls, face balls, their radii all times k). Per cell (one ball,
# two tetrahedra, volume 2): ball + 2 tet = 2, so the two are equal exactly when tet = 2/3 (= Samson = Delilah in #51's frame).
# For each k: tet volume, and the largest overlap between neighbouring tetrahedra (they must not overlap for the set to stay a partition).
import itertools, sys, numpy as np, manifold3d as m3
sys.argv = ['x']; src = open('roundtet_octet.py').read().split("if __name__ == '__main__':")[0]; exec(src)
base = dict(S=S_CORNER, R=R_CORNER, D=D_FACE, RF=R_FACE)
def filler_k(V, k):
    V = np.array(V, float); t = V.mean(0); P = []
    for j in range(4):
        P.append(balls(t + k * base['S'] * (V[j] - t), k * base['R']))
        n = t - V[j]; n /= np.linalg.norm(n); P.append(balls(t + k * base['D'] * n, k * base['RF']))
    return hull(np.vstack(P))
t0 = np.array([.5, .5, .5]); V0 = tet_around(t0)
neigh = [t0 + np.array(d) for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
def row(k):
    F0 = filler_k(V0, k); v = F0.volume(); ov = 0.0
    for t in neigh:
        o = (F0 ^ filler_k(tet_around(t), k)).volume(); ov = max(ov, o)
    return v, ov
for k in [1.0, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0]:
    v, ov = row(k); print(f'k {k:.2f}: tet {v:.5f}  ball {2 - 2 * v:.5f}  ratio ball/tet {(2 - 2 * v) / v:6.3f}  worst overlap with a neighbour {ov:.2e}')
lo, hi = 1.0, 2.5
for _ in range(40):
    mid = (lo + hi) / 2; v, _ = row(mid)
    if v < 2 / 3: lo = mid
    else: hi = mid
v, ov = row(lo); print(f'\nDELIAN: k = {lo:.5f}: tet {v:.6f} = ball {2 - 2 * v:.6f} (target 2/3 = {2/3:.6f}); worst overlap {ov:.2e}')
