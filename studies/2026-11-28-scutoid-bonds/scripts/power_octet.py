"""Scutoid bonds, pilot (DICTO 27 Nov: "is there a possibility of including scutoid-frusta bonds in the web of bonds"; plan yes 1,2,3).
With Claude (Anthropic). #51's cut planes are the power bisectors of the octet's centres (#51 §9, ref [6] Aurenhammer), so every member
is a power diagram: convex cells filling space face to face, whatever the weights. Here the two tetrahedron orientations (up: cube k with
sum(k) even; down: odd) get their own weights w_up, w_dn; octahedra weight 0. w_up = w_dn is #51's slider (2 kinds of piece). Splitting
them may turn #51's single all-at-once change (the octet, t = 1/3) into separate swaps. Numerical pilot: cell of each kind, its face
sizes, along paths in (w_up, w_dn). Output: the combinatorial type of each cell at each point, and where it changes."""
import itertools, numpy as np, sys
from scipy.spatial import HalfspaceIntersection, ConvexHull
R = range(-3, 4)
cent = []
for k in itertools.product(R, R, R):
    cent.append((np.array(k) + 0.5, 'up' if sum(k) % 2 == 0 else 'dn'))
    if sum(k) % 2: cent.append((np.array(k, float), 'oct'))
P = np.array([c for c, _ in cent]); K = [k for _, k in cent]
def cell(c0, W):
    hs = []
    for p, k in zip(P, K):
        if np.allclose(p, c0) or np.linalg.norm(p - c0) > 2.6: continue
        # power bisector: |x-c0|^2 - w0 <= |x-p|^2 - wp  <=>  2(p-c0).x <= |p|^2-|c0|^2 - (wp - w0)
        a = 2 * (p - c0); b = p @ p - c0 @ c0 - (W[k] - W[kind[tuple(c0)]])
        hs.append(np.r_[a, -b])
    hs = np.array(hs); h = HalfspaceIntersection(hs, c0 + 1e-3 * np.array([1, 2, 3]) / 10)
    V = h.intersections; ch = ConvexHull(V); fs = {}
    for eq, sm in zip(ch.equations, ch.simplices): fs.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
    # merge numerically duplicate corners
    Vu = np.unique(np.round(V, 7), axis=0)
    return len(Vu), tuple(sorted(len(set(map(tuple, np.round(V[list(f)], 7)))) for f in fs.values())), ch.volume
kind = {tuple(c): k for c, k in cent}
reps = {'up': np.array([0.5, 0.5, 0.5]), 'dn': np.array([1.5, 0.5, 0.5]), 'oct': np.array([1.0, 0.0, 0.0])}
def types(wu, wd):
    W = {'up': wu, 'dn': wd, 'oct': 0.0}; out = {}
    for k, c in reps.items():
        try: n, f, v = cell(c, W); out[k] = (n, f, round(v, 6))
        except Exception as e: out[k] = None
    return out
# control: per two unit cubes there are one up, one down tetrahedron centre and one octahedron centre, so up + dn + oct = 2.
# (earlier draft line: (weights giving t = 1/3: tet cell = regular tetrahedron of the octet, volume 1/3, oct cell volume 4/3... in this unit
# the cube of side 1 holds one tetrahedron (vol 1/3) and 2/3 of octahedra; check volumes sum: up + dn + 2 oct per 2 cubes = 2) -- WRONG count, fixed above)
print('PROGRESS 0 controls')
for w in np.linspace(-0.6, 0.6, 13):
    T = types(w, w); vs = T['up'][2] + T['dn'][2] + T['oct'][2] if all(T.values()) else None
    print(f"diag w={w:+.2f} up {T['up'][:2] if T['up'] else None} oct {T['oct'][:2] if T['oct'] else None} vol(up+dn+oct)={vs}")
print('PROGRESS 0.5 split')
seen = {}; bad = 0
for wu in np.linspace(-0.6, 0.6, 25):
    for wd in np.linspace(-0.6, 0.6, 25):
        T = types(wu, wd)
        if not all(T.values()): continue
        bad += abs(T['up'][2] + T['dn'][2] + T['oct'][2] - 2) > 1e-6
        key = tuple((k, T[k][0], T[k][1]) for k in ('up', 'dn', 'oct'))
        seen.setdefault(key, []).append((round(wu, 3), round(wd, 3)))
print('combinatorial types found:', len(seen))
for key, pts in sorted(seen.items(), key=lambda x: -len(x[1])):
    print(len(pts), 'pts e.g.', pts[0], '|', ' ; '.join(f"{k}: {n} corners, faces {dict(zip(*np.unique(f, return_counts=True)))}" for k, n, f in key))
print('volume control failures (up+dn+oct != 2 per two unit cubes):', bad)
print('FINAL ok' if len(seen) >= 1 and bad == 0 else 'FINAL FAIL')
