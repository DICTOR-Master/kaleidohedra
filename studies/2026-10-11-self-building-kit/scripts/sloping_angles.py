# DICTO 2026-10-11 "try thirty and forty five": planes through each edge of the tip's base (the band's top), tilted 30 or 45
# degrees from the base plane, sloping down outward or inward. Cells of the side ring (band minus the turned-over P(1/phi)).
import sys, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
exec(open('sloping_cuts.py').read().split("for role in ('j2', 'fuji'):")[0])   # reuse helpers
DEGS = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [30, 45]
def cell(A):
    norms = np.linalg.norm(A[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], norms], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if not r.success or r.x[3] < 1e-6: return None
    V = HalfspaceIntersection(A, r.x[:3]).intersections
    keep = []
    for v in V:
        if all(np.linalg.norm(v - k) > 1e-7 for k in keep): keep.append(v)
    return np.array(keep)
for role in ('j2', 'fuji'):
    apex, base = pyramid(role); vP = ConvexHull(np.vstack([apex, base])).volume
    big = apex + PHI * (np.vstack([apex, base]) - apex)
    B = np.unique(np.round(ConvexHull(np.vstack([base, big[1:]])).equations, 9), axis=0)
    c1 = base.mean(0); up = (apex - c1) / np.linalg.norm(apex - c1)
    small = c1 - (np.vstack([apex, base]) - c1) / PHI; Hh = np.unique(np.round(ConvexHull(small).equations, 9), axis=0)
    # base corners in cyclic order
    ang = np.arctan2(*(np.c_[(base - c1) @ np.cross(up, base[0] - c1), (base - c1) @ (base[0] - c1)].T))
    cyc = base[np.argsort(ang)]
    for deg in DEGS:
        for way in ('outward', 'inward'):
            a = np.radians(deg); planes = []
            for i in range(len(cyc)):
                p, q = cyc[i], cyc[(i + 1) % len(cyc)]; u = (q - p) / np.linalg.norm(q - p)
                m = np.cross(u, up); m = m if m @ (p - c1) > 0 else -m
                if way == 'inward': m = -m
                n = np.sin(a) * m + np.cos(a) * up; planes.append(np.r_[n, -n @ p])
            pieces = []
            for signs in itertools.product((1, -1), repeat=len(planes)):
                A = np.vstack([B] + [s * pl for s, pl in zip(signs, planes)])
                C = cell(A)
                if C is None: continue
                # subtract the hole: split by its faces
                for k in range(len(Hh)):
                    A2 = np.vstack([A, -Hh[k]] + [Hh[j] for j in range(k)])
                    D = cell(A2)
                    if D is not None: pieces.append(D)
            vols = [ConvexHull(V).volume / vP for V in pieces]
            kinds = {}
            for V, v in zip(pieces, vols): kinds.setdefault((len(V), round(v, 5)), []).append(V)
            named = [k for V in pieces if (k := known(V))]
            print(f'{role.upper()} {deg}° {way}: {len(pieces)} pieces, total {sum(vols):.6f} P, {len(kinds)} kinds; '
                  f'kit pieces found: {sorted(set(named)) or "none"}; smallest {min(vols):.4f} P')
