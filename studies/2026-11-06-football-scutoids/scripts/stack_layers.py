"""Football scutoid study, step 2a (DICTO 11-06 "A please first"; overnight): stack the pentagon-hexagon grid layers (grid_layer.py,
gap 0.6). A layer repeats in its plane by 2D (e1 + e2) and 2D (e1 - e2) (the checkerboard's period); the next layer is the same layer moved
by t = h n + a u + b w (n the layer normal). Search (a, b) over the layer's cell and the smallest h with no overlap between balls of
neighbouring layers (separating planes); then the share of space filled by balls (and bridges)."""
import itertools, sys, numpy as np
from scipy.spatial import ConvexHull
sys.argv = [sys.argv[0], '0.6']
exec(open('grid_layer.py').read().split('# overlap test')[0].replace('print(', '(lambda *a, **k: None)('))
n = np.cross(e1, e2); n /= np.linalg.norm(n)
P1, P2 = 2 * D * e1, D * (e1 + e2)                       # in-plane periods of the checkerboard layer (both orientations per cell)
def layer(shift, R=2):
    out = []
    for i, j in itertools.product(range(-R, R + 1), repeat=2):
        Vb, Rm = ball(i, j); out.append(Vb + shift)
    return out
def disjoint(P, Q):
    if np.linalg.norm(P.mean(0) - Q.mean(0)) > 5.0: return True
    for X, Y in ((P, Q), (Q, P)):
        for eq in ConvexHull(X).equations:
            if ((Y @ eq[:3] + eq[3]) >= -1e-9).all(): return True
    return False
base = layer(np.zeros(3), 1)
best = None
for a, b in itertools.product(np.linspace(0, 1, 9, endpoint=False), repeat=2):
    lo, hi = 0.5, 6.0
    for _ in range(30):
        h = (lo + hi) / 2; t = h * n + a * P1 + b * P2
        up = layer(t, 2)
        if all(disjoint(p, q) for p in base for q in up): hi = h
        else: lo = h
    if best is None or hi < best[0]: best = (hi, a, b)
h, a, b = best
cellvol = abs(np.linalg.det(np.array([P1, P2, h * n + a * P1 + b * P2])))
vball = ConvexHull(ball(0, 0)[0]).volume
f_ball = 2 * vball / cellvol                              # two balls per in-plane cell (checkerboard)
print(f"layer periods |P1| {np.linalg.norm(P1):.4f}, |P2| {np.linalg.norm(P2):.4f}; best stacking: h = {h:.4f} at shift ({a:.3f}, {b:.3f}) of the cell")
print(f"balls fill {f_ball:.4f} of space (ball volume {vball:.4f}); the rest, {1 - f_ball:.4f}, is bridges + gap to cut into pieces")
print("FINAL ok" if np.isfinite(h) and 0.5 < h < 6.0 else "FINAL FAIL (no stacking found in range)")