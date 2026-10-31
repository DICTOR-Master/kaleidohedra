# Star Cores names (2026-10-31): three two- and three-family solids from study 3 that have a property of their own, built from their
# planes and checked exactly (sympy): the edge-cut cube with all corners on one sphere, its dodecahedral analogue, and the truncated
# cuboctahedron proportions (1, 1/phi, 3/4) whose chain of T closes. Usage: ~/geom/bin/python pearls.py <out json>
import sys, json, itertools
import numpy as np, sympy as sp
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import brentq
OUT = sys.argv[1]
r5 = sp.sqrt(5); phi = (1 + r5) / 2

def orbit(vs):
    """all sign changes and cyclic permutations (enough for the octahedral and icosahedral axis sets used here), duplicates removed"""
    out = []
    for v in vs:
        for p in [v, v[1:] + v[:1], v[2:] + v[:2]]:
            for sg in itertools.product([1, -1], repeat=3):
                w = tuple(sp.nsimplify(a * b) for a, b in zip(sg, p))
                if all(x == 0 for x in w): continue
                if not any(all(sp.simplify(a - b) == 0 for a, b in zip(w, u)) for u in out): out.append(w)
    return out

FL = {}
def fl(v):
    if v not in FL: FL[v] = [float(a) for a in v]
    return FL[v]

def build(families):
    """families: list of (axis vectors, s); planes v.x <= s v.v. Returns exact planes, float corners, faces, corner->3 planes"""
    P = []
    for vs, s in families:
        for v in vs: P.append((v, s * sum(a * a for a in v)))
    A = np.array([fl(v) + [-float(c)] for v, c in P])
    V = HalfspaceIntersection(A, np.zeros(3)).intersections
    V = np.unique(np.round(V, 9), axis=0)
    on = [list(np.nonzero(np.abs(A[:, :3] @ x + A[:, 3]) < 1e-7)[0]) for x in V]
    faces = [i for i in range(len(P)) if sum(i in o for o in on) >= 3]
    return P, V, on, faces

def exact_corner(P, idx):
    for t in itertools.combinations(idx, 3):
        M = sp.Matrix([list(P[i][0]) for i in t])
        if sp.simplify(M.det()) != 0:
            return [sp.radsimp(sp.simplify(x)) for x in M.solve(sp.Matrix([P[i][1] for i in t]))]

def report(name, families):
    P, V, on, faces = build(families)
    E = [exact_corner(P, o) for o in on]
    r2 = sorted({sp.nsimplify(sp.simplify(sum(x * x for x in e))) for e in E}, key=float)
    # every corner satisfies every plane exactly
    ok = all(sp.simplify(c - sum(a * b for a, b in zip(v, e))) >= 0 for e in E for v, c in P)
    ch = ConvexHull(V); kinds = {}
    for i in faces:
        k = sum(i in o for o in on); kinds[k] = kinds.get(k, 0) + 1
    print(name, len(V), 'corners;', dict(sorted(kinds.items())), 'faces; all planes faces:', len(faces) == len(P), '; inside all planes:', ok,
          '; corner radii^2:', [str(x) for x in r2], flush=True)
    return dict(name=name, V=V.tolist(), faces=[[j for j, o in enumerate(on) if i in o] for i in faces],
                normals=[[float(a) for a in P[i][0]] for i in faces], kinds={str(k): n for k, n in kinds.items()},
                radii2=[str(x) for x in r2], all_planes_faces=len(faces) == len(P), inside=bool(ok))

ax4 = orbit([(1, 0, 0)]); ax3 = orbit([(1, 1, 1)]); ax2 = orbit([(1, 1, 0)])
i5 = orbit([(0, 1, phi)]); i2 = orbit([(1, 0, 0), (phi, 1 / phi, 1)])          # 6 axes x 2 = 12 five-fold; 30 two-fold
assert len(ax4) == 6 and len(ax3) == 8 and len(ax2) == 12 and len(i5) == 12 and len(i2) == 30, (len(i5), len(i2))
out = []
out.append(report('edge-cut cube s = 3/5', [(ax4, 1), (ax2, sp.Rational(3, 5))]))

# dodecahedral analogue: dodecahedron planes on the 5-fold axes at foot distance 1 along unit axes, edge planes on the 2-fold axes;
# find the depth where all corners lie on one sphere (float root, then the exact value, then the exact check)
u5 = [tuple(a / sp.sqrt(sum(b * b for b in v)) for a in v) for v in i5]; u2 = [tuple(a / sp.sqrt(sum(b * b for b in v)) for a in v) for v in i2]
def spread(d):
    _, V, _, _ = build([(u5, 1), (u2, d)]); r = np.linalg.norm(V, axis=1); return r.max() - r.min()
ds = np.linspace(1.17, 1.18, 41); vals = [spread(d) for d in ds]
k = int(np.argmin(vals)); print('dodeca spread min', vals[k], 'at d =', ds[k], flush=True)
# the spread is |r_axis - r_edge|: solve r_axis = r_edge as a smooth function by the corner kinds
def gap(d):
    _, V, on, _ = build([(u5, 1), (u2, d)]); r = np.linalg.norm(V, axis=1)
    a = [r[i] for i, o in enumerate(on) if all(j >= 12 for j in o)]; b = [r[i] for i, o in enumerate(on) if any(j < 12 for j in o)]
    return np.mean(a) - np.mean(b)
lo, hi = ds[max(k - 3, 0)], ds[min(k + 3, len(ds) - 1)]
from scipy.optimize import minimize_scalar
d0 = minimize_scalar(spread, bounds=(ds[max(k - 1, 0)], ds[min(k + 1, len(ds) - 1)]), method='bounded', options=dict(xatol=1e-13)).x
dex = sp.nsimplify(d0, [r5], tolerance=1e-8)
print('dodeca one-sphere depth float', d0, 'exact guess', dex, flush=True)
out.append(report('edge-cut dodecahedron d = %s' % dex, [(u5, 1), (u2, dex)]))
out[-1]['depth'] = str(dex)

out.append(report('truncated cuboctahedron proportions (1, 1/phi, 3/4)', [(ax4, 1), (ax3, 1 / phi), (ax2, sp.Rational(3, 4))]))
json.dump(out, open(OUT, 'w'))
print('done', flush=True)
