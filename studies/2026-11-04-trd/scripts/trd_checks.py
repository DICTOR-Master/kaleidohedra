#!/usr/bin/env python3
"""The trapezo-rhombic dodecahedron (TRD) as the rhombic dodecahedron's h partner (Concordance gap, DICTO's node work), 4 Nov 2026.
Unit spheres (neighbour distance 1). Checks:
 1. In every close-packed stacking the Voronoi cell of a straight (c) site is the RD and of a twisted (h) site the TRD
    (words ABC, AB, ABCB, ABCACB), both of volume sqrt2/2.
 2. Voronoi cell = 1/2 x polar of the 12-neighbour shell: RD = 1/2 polar(CO), TRD = 1/2 polar(anticuboctahedron J27).
 3. TRD = RD with one half (cut by the hexagonal plane through its centre, perpendicular to a 3-fold axis) turned 60 deg.
 4. Faces: 6 rhombi congruent to the RD's, 6 isosceles trapezoids; each trapezoid = two half-rhombi (triangles) of the RD, mirror pair.
 5. Centre pyramids: TRD = 6 rhombic pyramids R12 (as #93) + 6 trapezoid pyramids, each = 2 half-R12 tetrahedra (mirror images).
 6. The 12 face-centre directions = the 12 neighbour directions: DICTO's TRD DICTOnode ports (elevation +-arctan(sqrt2)... checked vs node script).
Run with python3 on compute-host. Writes data/trd-checks.json."""
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
res = []
def check(name, ok, detail=''):
    res.append({'check': name, 'pass': bool(ok), 'detail': str(detail)}); print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail != '' else ''))

H = math.sqrt(2/3)
POS = {'A': (0.0, 0.0), 'B': (0.5, math.sqrt(3)/6), 'C': (1.0, math.sqrt(3)/3)}
def stack(word, reps=3, n=4):
    w = word * reps
    pts = []
    for z, L in enumerate(w):
        ox, oy = POS[L]
        for a in range(-n, n+1):
            for b in range(-n, n+1):
                pts.append((ox + a + b/2, oy + b*math.sqrt(3)/2, z*H))
    return np.array(pts), w

def faces_of(hull_pts, eqs):
    """group hull simplices into planar faces; return list of (normal, vertex list ordered)"""
    out = {}
    for eq in eqs:
        key = tuple(np.round(eq[:3], 6))
        out.setdefault(key, eq)
    fs = []
    for key, eq in out.items():
        n = eq[:3]; d = -eq[3]
        vs = [p for p in hull_pts if abs(p @ n - d) < 1e-7]
        c = np.mean(vs, axis=0); u = vs[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        vs.sort(key=lambda p: math.atan2((p - c) @ v, (p - c) @ u))
        fs.append((n, vs))
    return fs

def classify(vs):
    L = sorted(round(float(np.linalg.norm(vs[i] - vs[(i+1) % len(vs)])), 6) for i in range(len(vs)))
    if len(vs) == 4 and len(set(L)) == 1: return 'rhombus', L
    if len(vs) == 4: return 'trapezoid', L
    return f'{len(vs)}-gon', L

def voronoi(pts, i):
    p = pts[i]; d = np.linalg.norm(pts - p, axis=1)
    nb = pts[(d > 1e-9) & (d < 2.01)] - p
    hs = np.array([[*q, -(q @ q)/2] for q in nb])
    cell = HalfspaceIntersection(hs, np.zeros(3))
    V = np.unique(np.round(cell.intersections, 9), axis=0)
    hull = ConvexHull(V)
    return V, hull, nb[np.abs(np.linalg.norm(nb, axis=1) - 1) < 1e-9]

def site_type(w, z):
    return 'c' if w[z-1] != w[z+1] else 'h'

summary = {}
for word in ['ABC', 'AB', 'ABCB', 'ABCACB']:
    pts, w = stack(word)
    per = len(pts) // len(w)
    seen = set()
    for z in range(len(word), 2*len(word)):
        t = site_type(w, z)
        i = z*per + per//2   # a central site of layer z
        V, hull, shell = voronoi(pts, i)
        fs = faces_of(hull.points[hull.vertices], hull.equations)
        kinds = sorted(classify(f[1])[0] for f in fs)
        key = (t, len(fs), tuple(kinds), round(hull.volume, 9), len(V))
        seen.add(key)
    summary[word] = sorted(seen)
want = {'c': (12, ('rhombus',)*12), 'h': (12, ('rhombus',)*6 + ('trapezoid',)*6)}
ok = all(k[1] == want[k[0]][0] and k[2] == tuple(sorted(want[k[0]][1])) and abs(k[3] - math.sqrt(2)/2) < 1e-9 for s in summary.values() for k in s)
check('every site of ABC, AB, ABCB, ABCACB: c -> RD (12 rhombi), h -> TRD (6 rhombi + 6 trapezoids), volume sqrt2/2', ok,
      {w: [(k[0], k[4]) for k in s] for w, s in summary.items()})

# polar relation: Voronoi cell = 1/2 polar(shell) since all neighbours at distance 1
pts, w = stack('AB'); per = len(pts)//len(w); i = 3*per + per//2
V, hull, shell = voronoi(pts, i)
check('TRD: 12 nearest neighbours, 14 vertices (8 three-fold, 6 four-fold) like the RD', len(shell) == 12 and len(V) == 14, len(V))
facenorm = sorted(tuple(np.round(eq[:3], 6)) for eq in {tuple(np.round(e[:3], 6)): e for e in hull.equations}.values())
shellnorm = sorted(tuple(np.round(q, 6)) for q in shell)
check('face normals of the TRD = the 12 neighbour directions (each face on the bisector at distance 1/2): TRD = 1/2 polar(J27)', facenorm == shellnorm)

# geometry of the faces
fs = faces_of(hull.points[hull.vertices], hull.equations)
rh = [classify(f[1])[1] for f in fs if classify(f[1])[0] == 'rhombus']
tz = [classify(f[1])[1] for f in fs if classify(f[1])[0] == 'trapezoid']
check('the 6 rhombi are the RD rhombus, edge sqrt6/4', len({tuple(x) for x in rh}) == 1, rh[0])
check('6 trapezoids, all congruent', len({tuple(x) for x in tz}) == 1 and len(tz) == 6, tz[0])

# 3. TRD = RD with upper half turned 60 deg about the 3-fold (z) axis
ptsc, wc = stack('ABC'); per = len(ptsc)//len(wc); Vr, hr, _ = voronoi(ptsc, 4*per + per//2)
Vt = V
def turn(P, deg):
    a = math.radians(deg); R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]]); return P @ R.T
up = Vr[Vr[:, 2] > 1e-9]; low = Vr[Vr[:, 2] <= 1e-9]
built = np.vstack([low, turn(up, 60)])
s1 = set(map(tuple, np.round(built, 6))); s2 = set(map(tuple, np.round(Vt, 6)))
alt = set(map(tuple, np.round(np.vstack([low, turn(up, -60)]), 6)))
check('RD with its upper half turned 60 deg about the 3-fold axis has exactly the TRD corners', s1 == s2 or alt == s2)
check('the turning plane through the centre holds no RD corner: it cuts six edges, so the turn needs no new corners', int(np.sum(np.abs(Vr[:, 2]) < 1e-9)) == 0)

# 5. pyramids: volumes
def cone_vol(f):
    vs = f[1]; c = vs[0]; v = 0
    for k in range(1, len(vs)-1): v += abs(np.linalg.det(np.array([vs[0], vs[k], vs[k+1]]))) / 6
    return v
pr = sorted(round(cone_vol(f), 9) for f in fs)
rdpr = sorted(round(cone_vol(f), 9) for f in faces_of(hr.points[hr.vertices], hr.equations))
check('RD: 12 equal centre pyramids R12 of volume sqrt2/24', len(set(rdpr)) == 1 and abs(rdpr[0] - math.sqrt(2)/24) < 1e-9, rdpr[0])
check('TRD: 12 centre pyramids, all of the same volume sqrt2/24 (6 rhombic = R12, 6 trapezoidal)', len(set(pr)) == 1 and abs(pr[0] - math.sqrt(2)/24) < 1e-9, pr[0])
# each trapezoid pyramid = 2 tetrahedra (cone over the two triangles cut by the waist plane) = 2 half-R12
rdn = [tuple(np.round(e[:3], 6)) for e in hr.equations]
tn = [f[0] for f in fs if classify(f[1])[0] == 'trapezoid']
okp = all(tuple(np.round(n, 6)) in rdn and tuple(np.round(turn(n[None, :], -60)[0], 6)) in rdn for n in tn)
check('each trapezoid has 2 corners above and 2 below the waist; its plane is that of one RD rhombus below and of the next RD rhombus (turned 60 deg) above, so a trapezoid is the lower part of one cut rhombus and the upper part of another, and its pyramid the matching parts of two R12',
      okp and all(sum(1 for p in f[1] if p[2] > 1e-9) == 2 for f in fs if classify(f[1])[0] == 'trapezoid'))
check('trapezoid: parallel sides 1/sqrt6 and 2/sqrt6 (ratio 1 : 2), legs sqrt6/4 = the rhombus edge', abs(tz[0][0] - 1/math.sqrt(6)) < 1e-6 and abs(tz[0][3] - 2/math.sqrt(6)) < 1e-6 and abs(tz[0][1] - math.sqrt(6)/4) < 1e-6)
os.makedirs(OUT, exist_ok=True)
json.dump(res, open(os.path.join(OUT, 'trd-checks.json'), 'w'), indent=1)
print(sum(r['pass'] for r in res), 'PASS', sum(not r['pass'] for r in res), 'FAIL')
