"""Exact SKELETAL renders of DICTO's four Vacuus builds (paper #87 DICTO Vacuus Solids), 24 Nov 2026.
DICTO, 24 Nov: "the way I build all my PET bottle and B1NR sculptures is as Vacuus ... and hulls ... they are skeletons and empty".
So every build is drawn as an open framework: struts (tubes) and joints (balls), no faces; the empty space shows.
Not fitted to photos: every strut joins exact corners of the solid the build realises.
 1. Cardboard octahedron (corners +-e_i): its 12 edges + the 6 corner-to-centre struts (the three half-axes pairs), so the three
    squares x = 0, y = 0, z = 0 stand as frames (each: 4 edges + its 2 diagonals = 4 half-axes). Pull-apart: each square frame
    moved along its own normal.
 2. B1NR cube [-1,1]^3: the hull skeleton (12 edges) + the Vacuus skeleton (8 corner-to-centre struts): the empty cube that is six
    square pyramids meeting at the centre O. Clear tubes. Pull-apart: the six pyramid skeletons along the face normals, pull 27/5,
    chosen so that the six frames' projected bounding boxes (joint balls included) are pairwise disjoint in the drawn view.
 3. B1NR cuboctahedron Vacuus, NO hull, ring fins (DICTO's photos, 24 Nov): one white bottle security ring per fin, the fin's exact
    incircle in its plane: 24 rings in 4 hexagonal plates; cut cable ties (no tails) as small clasps where rings touch. Views: oblique;
    down a three-fold axis; the four plates pulled apart along their normals.
 4. B1NR dodecahedron Vacuus, NO hull, ring fins: 30 rings in 15 plates of 2. Views: oblique; down a five-fold axis (1, 0, phi).
 (The white ring cube is the B1NR cube itself, DICTO 24 Nov; its separate diagonal-rectangle render is withdrawn.)
Usage: python builds.py <out.html>   (house renderer render3d.write, with see-through tubes added below; frames by shots.mjs)."""
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/renders/scripts"))
import render3d

# The house renderer draws every tube opaque. For the clear bottle tubes a tube may carry an opacity as its 5th entry and a ball as
# its 3rd: the two lines below switch the tube and ball materials to see-through when one is given (nothing else changes).
render3d.HTML = render3d.HTML.replace(
    "function tube(a, b, rad, col, back) {", "function tube(a, b, rad, col, back, op) {").replace(
    "new THREE.MeshStandardMaterial({ color: col, roughness: 0.55, metalness: 0.0, side: back ? THREE.BackSide : THREE.FrontSide })",
    "new THREE.MeshStandardMaterial({ color: col, roughness: 0.25, metalness: 0.0, side: back ? THREE.BackSide : THREE.FrontSide, transparent: op < 1, opacity: op === undefined ? 1 : op, depthWrite: !(op < 1) })").replace(
    "grp.add(late(tube(d.v[e[0]], d.v[e[1]], d.rad * E, e[2], false)));",
    "grp.add(late(tube(d.v[e[0]], d.v[e[1]], d.rad * E, e[2], false, e[4]))); if (e[5]) grp.add(late(tube(d.v[e[0]], d.v[e[1]], d.rad * E * e[5][1], e[5][0], false)));").replace(
    "new THREE.MeshStandardMaterial({ color: b[1], roughness: 0.55 })",
    "new THREE.MeshStandardMaterial({ color: b[1], roughness: 0.35, transparent: b[2] < 1, opacity: b[2] === undefined ? 1 : b[2], depthWrite: !(b[2] < 1) })")
# Rings and clasps (24 Nov, ring-fin builds): a part may carry 'rings' [centre, normal, R, width, thickness, outer col, inner col, opacity],
# drawn as a flat band whose OUTER face has radius R in the plane through centre with that normal (two open cylinders + two rims), and
# 'clasps' [point, axis, R, tube, col, opacity]: a small torus around the axis at the point (a cut cable tie, no tail) with a flush head.
BALLS = render3d.HTML[render3d.HTML.index("    for (const b of (d.balls"):].split("\n")[0]
render3d.HTML = render3d.HTML.replace(BALLS, BALLS + """
    for (const q of (d.rings || [])) { const [c, n, R, w, th, co, ci, op] = q; const g = new THREE.Group();
      const mat = (col, side) => new THREE.MeshStandardMaterial({ color: col, roughness: 0.3, metalness: 0.0, side, transparent: op < 1, opacity: op });
      g.add(new THREE.Mesh(new THREE.CylinderGeometry(R, R, w, 160, 1, true), mat(co, THREE.FrontSide)));
      g.add(new THREE.Mesh(new THREE.CylinderGeometry(R - th, R - th, w, 160, 1, true), mat(ci, THREE.BackSide)));
      for (const s of [1, -1]) { const m = new THREE.Mesh(new THREE.RingGeometry(R - th, R, 160), mat('#ffffff', THREE.DoubleSide)); m.rotation.x = -s * Math.PI / 2; m.position.y = s * w / 2; g.add(m); }
      g.position.set(...c); g.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), new THREE.Vector3(...n).normalize()); grp.add(g); }
    for (const q of (d.clasps || [])) { const [p, u, R, tb, col, op] = q; const g = new THREE.Group();
      const mat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.2, transparent: op < 1, opacity: op });
      g.add(new THREE.Mesh(new THREE.TorusGeometry(R, tb, 12, 48), mat));
      const h = new THREE.Mesh(new THREE.BoxGeometry(3.2 * tb, 2.4 * tb, 3.2 * tb), mat); h.position.set(R + tb, 0, 0); g.add(h);
      g.position.set(...p); g.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), new THREE.Vector3(...u).normalize()); grp.add(g); }""")
assert render3d.HTML.count("d.rings") == 1 and render3d.HTML.count("d.clasps") == 1
assert render3d.HTML.count('e[4]') == 1 and render3d.HTML.count('b[2]') == 4 and 'back, op)' in render3d.HTML and 'e[5][0]' in render3d.HTML and 'op === undefined' in render3d.HTML


def skel(struts, col, out, rad, ball, shift=(0, 0, 0), op=None, core=None, bop=None):
    """a framework: struts [(p, q)] as tubes (outline tube behind for the dark ground), a ball at every joint"""
    V = []
    def vid(p):
        p = tuple(np.round(np.array(p, float) + shift, 6))
        if p not in V: V.append(p)
        return V.index(p)
    T = []
    for p, q in struts:
        e = [vid(p), vid(q), col, out]
        if op is not None: e += [op, core]
        T.append(e)
    balls = [[i, ball] + ([bop] if bop is not None else []) for i in range(len(V))] if ball else []
    return {'v': [list(p) for p in V], 't': [], 'c': [], 'a': 1, 'tubes': T, 'rad': rad, 'balls': balls}


O = np.zeros(3)
# ---------------- 1. cardboard octahedron ----------------
OV = [s * np.eye(3)[k] for k in range(3) for s in (1, -1)]
OE = [(p, q) for p, q in itertools.combinations(OV, 2) if abs(np.dot(p, q)) < 1e-12]          # 12 edges
OS = [(O, p) for p in OV]                                                                     # 6 corner-to-centre struts
TAN, TAN_OUT, TAN_BALL = '#c9a77c', '#5a4229', '#a8855a'
def octa_square(k):                       # the square in the plane x_k = 0: its 4 edges and its 4 half-axes
    return [(p, q) for p, q in OE if p[k] == 0 and q[k] == 0] + [(O, p) for p in OV if p[k] == 0]
def octa_all():
    return [skel(OE + OS, TAN, TAN_OUT, 0.0105, TAN_BALL)]
def octa_pulled(pull):
    return [skel(octa_square(k), TAN, TAN_OUT, 0.0105, TAN_BALL, np.eye(3)[k] * pull * (1 if k != 1 else -1)) for k in range(3)]

# ---------------- cube ----------------
CV = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)]
CE = [(CV[i], CV[j]) for i in range(8) for j in range(i + 1, 8) if np.abs(CV[i] - CV[j]).sum() == 2]            # 12 edges
CS = [(O, p) for p in CV]                                                                                       # 8 corner-to-centre struts
CF = [(k, s) for k in range(3) for s in (1, -1)]                                                                # faces x_k = s

# 2. B1NR cube: clear bottle tubes (pale see-through with a bright core line), clear joints
BOT, BOT_CORE, BOT_BALL = '#9fd3e3', '#f2fbff', '#cfeaf2'
def b1nr(struts, shift=(0, 0, 0)):
    return skel(struts, BOT, None, 0.0175, BOT_BALL, shift, op=0.42, core=[BOT_CORE, 0.32], bop=0.6)
def b1nr_all():
    return [b1nr(CE + CS)]
def b1nr_pulled(pull):
    out = []
    for k, s in CF:
        base = [p for p in CV if p[k] == s]
        out.append(b1nr([(p, q) for p, q in CE if p[k] == s and q[k] == s] + [(O, p) for p in base], np.eye(3)[k] * s * pull))
    return out

VO = [0.85, 0.62, 1.25]; VC = [1.0, 0.62, 1.45]

# 3. and 4. B1NR ring-fin Vacuus, no hull (DICTO's photos of the cuboctahedron build, 24 Nov): one white PET-bottle security ring per fin
# (the triangle O, a, b of an edge ab), inscribed in the fin and lying in its plane: centre the incentre, radius the inradius, normal a x b.
# Drawn as a flat band (as the real rings): its OUTER face is the incircle, so a ring touches the fin's three sides exactly. Rings that touch
# meet on the centre-to-corner lines (spokes); there the build has a cut cable tie (DICTO 24 Nov, "cut them": no tails), drawn as a small
# flush clasp around the spoke. Exact geometry (sympy, Q(sqrt 3, sqrt 5)) in check.py; the same formulas in floats here.
PHI = (1 + 5 ** 0.5) / 2
QV = [np.array(p, float) for p in {tuple(np.roll(q, r)) for q in itertools.product((1, -1), (1, -1), (0,)) for r in range(3)}]
DV = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)] + \
     [np.roll(np.array([0, a / PHI, b * PHI]), r) for a in (1, -1) for b in (1, -1) for r in range(3)]
assert len(QV) == 12 and len(DV) == 20
def edges(V):
    L = min(np.linalg.norm(p - q) for p, q in itertools.combinations(V, 2))
    return [(p, q) for p, q in itertools.combinations(V, 2) if abs(np.linalg.norm(p - q) - L) < 1e-9]
def fin_ring(a, b):
    """incircle of the fin O, a, b: (centre, unit normal, radius) by the incentre formula (|ab| O + |Ob| a + |Oa| b) / perimeter"""
    la, lb, lab = np.linalg.norm(a), np.linalg.norm(b), np.linalg.norm(a - b)
    n = np.cross(a, b); P = la + lb + lab
    return (lb * a + la * b) / P, n / np.linalg.norm(n), np.linalg.norm(n) / P
def rings_of(V):
    return [fin_ring(a, b) for a, b in edges(V)]
def dist_line(c, p, q):
    d = q - p; return np.linalg.norm(np.cross(c - p, d)) / np.linalg.norm(d)
for V in (QV, DV):
    for (a, b), (c, n, r) in zip(edges(V), rings_of(V)):
        assert abs(np.dot(c, n)) < 1e-12 and all(abs(dist_line(c, p, q) - r) < 1e-12 for p, q in ((O, a), (O, b), (a, b)))
def touch_points(V):
    """where rings touch: on each spoke O-v the fins at v touch it at one common point (incircle tangent length from O)"""
    out = []
    for v in V:
        fins = [(a, b) for a, b in edges(V) if np.allclose(a, v) or np.allclose(b, v)]
        a, b = fins[0]; la, lb, lab = np.linalg.norm(a), np.linalg.norm(b), np.linalg.norm(a - b)
        t = (la + lb - lab) / 2                                  # tangent length from O (equal for all fins: congruent)
        out.append((t * v / np.linalg.norm(v), v / np.linalg.norm(v), len(fins)))
    return out
WHITE, WHITE_IN, TIE = '#f6f5f0', '#e4e2da', '#dfe8ea'
def ring_part(V, shift=lambda n: np.zeros(3), clasps=True, only=None):
    R = rings_of(V); rr = R[0][2]; w, th = 0.40 * rr, 0.07 * rr
    rings = []
    for c, n, r in R:
        if only is not None and not only(n): continue
        rings.append([list(np.round(c + shift(n), 6)), list(np.round(n, 6)), round(r, 6), w, th, WHITE, WHITE_IN, 0.9])
    cl = [[list(np.round(p, 6)), list(np.round(u, 6)), 0.62 * w, 0.075 * w, TIE, 0.78] for p, u, k in touch_points(V)] if clasps else []
    return {'v': [], 't': [], 'c': [], 'a': 1, 'tubes': [], 'rad': 0.01, 'balls': [], 'rings': rings, 'clasps': cl}
# plates: the fins grouped by plane (normal up to sign); cuboctahedron 4 hexagons of 6, dodecahedron 15 planes of 2
def plates(V):
    P = []
    for c, n, r in rings_of(V):
        for g in P:
            if abs(abs(np.dot(g[0], n)) - 1) < 1e-9: g[1].append(c); break
        else: P.append([n, [c]])
    return P
QP = plates(QV); DP = plates(DV)
assert sorted(len(g[1]) for g in QP) == [6] * 4 and sorted(len(g[1]) for g in DP) == [2] * 15
def cubo_pulled(pull):    # each hexagon plate moved along its own normal, sign chosen tetrahedrally (normals sum to 0)
    parts = []
    for n0, _ in QP:
        m = n0 * np.sign(n0[0] * n0[1] * n0[2])                    # (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)
        parts.append(ring_part(QV, shift=lambda n, m=m: m * pull, clasps=False, only=lambda n, m=m: abs(abs(np.dot(n, m)) - 1) < 1e-9))
    return parts
V3 = [1, 1, 1]; V5 = [1, 0, PHI]
# B1NR pull-apart: the six pyramid frames must be clearly separate IN THE PICTURE. Check by projected bounding boxes in the drawn
# view (render3d.project, joint ball radius as margin): every pair of boxes disjoint with a gap of at least 1.5 % of the frame.
PULLB, EP = 5.4, 6.9
def b1nr_boxes(pull, E):
    pad = 1.25 * 0.0175 / 2 * render3d.PX                          # joint ball radius (1.25 rad E) in pixels
    B = []
    for part in b1nr_pulled(pull):
        P = render3d.project(np.array(part['v']), VC, E)
        B.append((P[:, 0].min() - pad, P[:, 0].max() + pad, P[:, 1].min() - pad, P[:, 1].max() + pad))
    return B
BX = b1nr_boxes(PULLB, EP)
GAP = min(max(b[0] - a[1], a[0] - b[1], b[2] - a[3], a[2] - b[3]) for a, b in itertools.combinations(BX, 2))
INFRAME = all(0 < b[0] and b[1] < render3d.PX and 0 < b[2] and b[3] < render3d.PX for b in BX)
print('B1NR pull %.2f, E %.2f: smallest gap between projected boxes %.1f px of %d; all boxes in frame: %s'
      % (PULLB, EP, GAP, render3d.PX, INFRAME))
for k, b in zip(['+x', '-x', '+y', '-y', '+z', '-z'], BX): print('  pyramid %s box x %.0f-%.0f y %.0f-%.0f' % ((k,) + b))
# Cuboctahedron pull-apart: the four hexagon plates must be clearly separate IN THE PICTURE. Check: the convex hulls of the projected
# rings (outer circles sampled, half band width as margin) are pairwise disjoint, by separating axes, with a gap >= 1.5 % of the frame.
PULLQ, EQ, VQP = 2.0, 3.0, [0, 0, 1]      # seen down a four-fold axis: the four tetrahedral pull directions spread to the four corners
def hull(P):                                   # convex hull, monotone chain
    P = sorted(map(tuple, P)); cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    def half(seq):
        H = []
        for p in seq:
            while len(H) >= 2 and cr(H[-2], H[-1], p) <= 0: H.pop()
            H.append(p)
        return H[:-1]
    return np.array(half(P) + half(P[::-1]))
def sep_gap(A, B):
    g = -1e9
    for H in (A, B):
        for i in range(len(H)):
            e = H[(i + 1) % len(H)] - H[i]; nrm = np.array([-e[1], e[0]]) / np.linalg.norm(e)
            pa, pb = A @ nrm, B @ nrm; g = max(g, pb.min() - pa.max(), pa.min() - pb.max())
    return g
def plate_hulls(pull, E):
    out = []
    for part in cubo_pulled(pull):
        pts = []
        for c, n, r, w, *_ in part['rings']:
            c, n = np.array(c), np.array(n); u = np.cross(n, [0.3, 0.5, 0.8]); u /= np.linalg.norm(u); v = np.cross(n, u)
            for t in np.linspace(0, 2 * np.pi, 180, endpoint=False):
                for h in (-w / 2, w / 2): pts.append(c + r * (np.cos(t) * u + np.sin(t) * v) + h * n)
        out.append(hull(render3d.project(np.array(pts), VQP, E)))
    return out
QH = plate_hulls(PULLQ, EQ)
GAPQ = min(sep_gap(a, b) for a, b in itertools.combinations(QH, 2))
INQ = all(h.min() > 0 and h.max() < render3d.PX for h in QH)
print('cuboctahedron plates pull %.2f, E %.2f, view down (0, 0, 1): smallest hull gap %.1f px of %d; all in frame: %s' % (PULLQ, EQ, GAPQ, render3d.PX, INQ))
print('cuboctahedron: %d rings, %d plates of %s; dodecahedron: %d rings, %d plates of %s' % (len(rings_of(QV)), len(QP), {len(g[1]) for g in QP},
      len(rings_of(DV)), len(DP), {len(g[1]) for g in DP}))
for nm, V in (('cuboctahedron', QV), ('dodecahedron', DV)):
    c, n, r = rings_of(V)[0]; tp = touch_points(V)
    print('  %s ring radius %.6f, centre at %.6f from O; %d clasps, %d rings at each, at %.6f from O' % (nm, r, np.linalg.norm(c), len(tp), tp[0][2], np.linalg.norm(tp[0][0])))
scenes = [
    {'E': 1.30, 'dir': VO, 'parts': octa_all()},             # p0 octahedron skeleton: 12 edges + 6 half-axes (three square frames)
    {'E': 2.95, 'dir': VO, 'parts': octa_pulled(1.8)},       # p1 the three square frames pulled apart along their normals
    {'E': 1.95, 'dir': VC, 'parts': b1nr_all()},             # p2 B1NR cube: 12 edges + 8 corner-to-centre struts
    {'E': EP, 'dir': VC, 'parts': b1nr_pulled(PULLB)},       # p3 its six pyramid skeletons pulled apart
    {'E': 1.50, 'dir': VC, 'parts': [ring_part(QV)]},       # p4 cuboctahedron ring-fin Vacuus: 24 rings, 12 clasps
    {'E': 1.50, 'dir': V3, 'parts': [ring_part(QV)]},       # p5 the same down a three-fold axis (one hexagon plate face-on)
    {'E': EQ, 'dir': VQP, 'parts': cubo_pulled(PULLQ)},     # p6 its four hexagon plates pulled apart along their normals
    {'E': 1.85, 'dir': VC, 'parts': [ring_part(DV)]},       # p7 dodecahedron ring-fin Vacuus: 30 rings, 20 clasps
    {'E': 1.85, 'dir': V5, 'parts': [ring_part(DV)]},       # p8 the same down a five-fold axis
]
render3d.write(sys.argv[1], scenes)
ok = (len(OE), len(OS), len(CE), len(CS), len(QV), len(DV)) == (12, 6, 12, 8, 12, 20) and GAP >= 0.015 * render3d.PX and INFRAME \
    and GAPQ >= 0.015 * render3d.PX and INQ and len(rings_of(QV)) == 24 and len(rings_of(DV)) == 30 \
    and all(s['parts'][0]['t'] == [] for s in scenes) and all(p['t'] == [] for s in scenes for p in s['parts'])
print('scenes', len(scenes), 'no faces in any scene' if ok else '', 'FINAL ok' if ok else 'FINAL FAIL')
