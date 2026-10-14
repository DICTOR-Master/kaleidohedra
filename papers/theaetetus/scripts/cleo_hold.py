# DICTO 2026-10-15: hold the hollow DICTO-ICOSA star's core by 20 Cleo-Icos standing on the icosidodecahedron's triangles, points on
# the core's faces. Icosidodecahedron edge 1; Cleo-Ico = an icosahedron's face pyramid from its centre (edge-1 base, lateral edges
# = circumradius, height = inradius); core icosahedron of edge 1 on the 5-fold axes. Checks: overlaps, contacts, turning, shifting.
import itertools, numpy as np
from scipy.spatial import ConvexHull
g = (1 + 5 ** .5) / 2
V = []
for s in (1, -1):
    for i in range(3): v = [0, 0, 0]; v[i] = s * g; V.append(v)
for sx, sy, sz in itertools.product((1, -1), repeat=3):
    b = [sx * .5, sy * g / 2, sz * g * g / 2]
    for k in range(3): V.append(b[k:] + b[:k])
ID = np.array(V, float)
H = ConvexHull(ID); F = []
for e in H.equations:
    idx = tuple(sorted(i for i in range(30) if abs(ID[i] @ e[:3] + e[3]) < 1e-9))
    if idx not in [f for f, _ in F]: F.append((idx, e))
tri = [(ID[list(i)], e) for i, e in F if len(i) == 3]; pent = [(ID[list(i)], e) for i, e in F if len(i) == 5]
assert len(tri) == 20 and len(pent) == 12
r_in = g * g / (2 * 3 ** .5)            # inradius of the edge-1 icosahedron
R_ico = (10 + 2 * 5 ** .5) ** .5 / 4    # its circumradius
cleo = [np.vstack([T, T.mean(0) - e[:3] * r_in]) for T, e in tri]
for C in cleo: assert all(abs(np.linalg.norm(C[3] - C[k]) - R_ico) < 1e-12 for k in range(3))   # really a Cleo-Ico
core = np.array([-e[:3] * 0 + e[:3] * R_ico for _, e in pent])   # corners on the 12 five-fold axes
CE = ConvexHull(core); assert len(CE.simplices) == 20
assert abs(min(np.linalg.norm(a - b) for a, b in itertools.combinations(core, 2)) - 1) < 1e-12
def axes(P):
    h = ConvexHull(P); A = [e[:3] for e in h.equations]
    E = {tuple(np.round(P[j] - P[i], 12)) for s in h.simplices for i, j in itertools.combinations(s, 2)}
    return A, [np.array(x) for x in E]
def sep(P, Q):
    a1, e1 = axes(P); a2, e2 = axes(Q); best = -1e9
    for n in a1 + a2 + [np.cross(u, w) / np.linalg.norm(np.cross(u, w)) for u in e1 for w in e2 if np.linalg.norm(np.cross(u, w)) > 1e-12]:
        p, q = P @ n, Q @ n; best = max(best, q.min() - p.max(), p.min() - q.max())
    return best          # > 0 apart, = 0 touching, < 0 overlapping (penetration depth along the best axis)
out = []
# 1. the Cleo-Icos among themselves
s = [sep(a, b) for a, b in itertools.combinations(cleo, 2)]
out.append(f'1. Cleo-Icos pairwise: min separation {min(s):.3e} over {len(s)} pairs (>= 0: no overlap)')
# 2. each Cleo-Ico against the core, and the contact point
s = [sep(C, core) for C in cleo]
apex_r = [np.linalg.norm(C[3]) for C in cleo]
on_plane = max(abs(C[3] @ e[:3] + e[3]) for C in cleo for e in [min(CE.equations, key=lambda e: -(C[3] / np.linalg.norm(C[3])) @ e[:3])])
fc = [core[sm].mean(0) for sm in CE.simplices]; at_centre = max(min(np.linalg.norm(C[3] - c) for c in fc) for C in cleo)
out.append(f'2. Cleo-Ico vs core: separations {min(s):.2e}..{max(s):.2e}; apex radius {min(apex_r):.12f} = core inradius {r_in:.12f}; apex off its face plane {on_plane:.1e}, off the face centre {at_centre:.1e}')
# 3. the core inside the shell; room at the corners
pd = -pent[0][1][3]
out.append(f'3. core corner radius {R_ico:.6f}; pentagon faces at {pd:.6f}: each corner {pd - R_ico:.6f} short of its pentagonal window; triangle faces at {-tri[0][1][3]:.6f}')
# 4. can it turn? every rotation axis on a fine sphere grid, at 0.5, 1 and 2 degrees
def rot(a, t):
    a = a / np.linalg.norm(a); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
rng = np.random.default_rng(1); dirs = list(rng.normal(size=(300, 3))) + [core[0], fc[0], core[0] + core[1]]
for deg in (0.5, 1, 2):
    free = [d for d in dirs if min(sep(C, core @ rot(d, np.radians(deg)).T) for C in cleo) > -1e-12]
    pen = np.median([-min(sep(C, core @ rot(d, np.radians(deg)).T) for C in cleo) for d in dirs[:40]])
    out.append(f'4. turned {deg}°: {len(dirs) - len(free)} of {len(dirs)} axes collide (median depth {pen:.1e})')
# 5. can it shift? 300 directions, 0.001 and 0.01
for t in (0.001, 0.01):
    free = [d for d in dirs if min(sep(C, core + t * d / np.linalg.norm(d)) for C in cleo) > -1e-12]
    out.append(f'5. shifted {t}: {len(dirs) - len(free)} of {len(dirs)} directions collide')
vol = lambda P: ConvexHull(P).volume
out.append(f'6. volumes: shell {vol(ID):.6f}, core {vol(core):.6f}, 20 Cleo-Icos {sum(vol(C) for C in cleo):.6f}, empty {vol(ID) - vol(core) - sum(vol(C) for C in cleo):.6f}')
print('\n'.join(out)); open('cleo_hold.txt', 'w').write('\n'.join(out) + '\n')
