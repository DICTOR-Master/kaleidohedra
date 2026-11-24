"""Exact 3D renders of three of DICTO's Vacuus builds (paper #87 DICTO Vacuus Solids), 24 Nov 2026.
Not fitted to photos: every piece is built from exact coordinates of the solid the build realises.
 1. Cardboard octahedron Vacuus: DICTO's four slotted pieces (A in z = 0, B in x = 0, C in y = 0 cut in two), the octahedron's
    three squares through one centre; corners at distance a = 1 on the axes. Board and slots to the scale of the cut sheet
    (studies/2026-11-02-vacuus-origami/scripts/cardboard_octahedron.py: edge 80 mm, board 3.5 mm, slot 3.8 mm).
 2. B1NR cube: the cube [-1,1]^3 as six square pyramids with apex at the centre O; their shared walls are the twelve fins O-A-B,
    the cube's Vacuus (two fins in each of the cube's six diagonal planes).
 3. White ring cube (DICTO, 24 Nov): the cube's six diagonal planes, each a WHOLE white rectangle through two opposite edges and
    the centre O (sides 2 and 2 sqrt 2). The six cut through each other, so three views: assembled; one rectangle alone; the three
    rectangles through one body diagonal pulled apart along their normals.
Usage: python builds.py <out.html>   (house renderer render3d.write; frames by shots.mjs)."""
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/renders/scripts"))
from render3d import write

# ---------------- 1. cardboard octahedron ----------------
EDGE_MM, T_MM, W_MM = 80.0, 3.5, 3.8
a = 1.0; mm = a / (EDGE_MM / 2 ** .5)          # half-diagonal a = 1
t, w = T_MM * mm, W_MM * mm                      # board thickness, slot width
h = w / 2
# piece outlines in their own (u, v) plane, counter-clockwise (exactly the cut sheet's pieces)
PA = [(a, 0), (h, a - h), (h, 0), (-h, 0), (-h, a - h), (-a, 0), (0, -a)]                       # one slot, +v corner to centre
PB = [(a, 0), (h, a - h), (h, a / 2), (-h, a / 2), (-h, a - h), (-a + h, h), (0, h), (0, -h),
      (-a + h, -h), (-h, -a + h), (-h, -a / 2), (h, -a / 2), (h, -a + h)]                          # three slots
PC1 = [(h, h), (a - h, h), (0, a), (-a + h, h), (-h, h), (-h, a / 2), (h, a / 2)]                  # upper half of C, slot to half-way
PC2 = [(u, -v) for (u, v) in PC1][::-1]                                                            # lower half
# (u, v, n) -> (x, y, z): A in z = 0 (u = x, v = y), B in x = 0 (u = y, v = z), C in y = 0 (u = x, v = z)
MAP = {'A': lambda u, v, n: (u, v, n), 'B': lambda u, v, n: (n, u, v), 'C': lambda u, v, n: (u, n, v)}


def earclip(P):
    P = [np.array(p, float) for p in P]; idx = list(range(len(P))); tris = []
    cross = lambda o, p, q: (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    while len(idx) > 3:
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            if cross(P[i0], P[i1], P[i2]) <= 1e-12: continue
            if any(j not in (i0, i1, i2) and cross(P[i0], P[i1], P[j]) >= -1e-12 and cross(P[i1], P[i2], P[j]) >= -1e-12
                   and cross(P[i2], P[i0], P[j]) >= -1e-12 for j in idx): continue
            tris.append([i0, i1, i2]); idx.pop(k); break
        else: raise ValueError('ear clipping failed')
    tris.append(idx); return tris


def slab(P, plane, shift, face, edge, outline, rad):
    """a flat piece of board: outline P extruded to thickness t about its plane, moved by shift"""
    n = len(P); f = MAP[plane]; s = np.array(shift, float)
    V = [np.array(f(u, v, -t / 2)) + s for u, v in P] + [np.array(f(u, v, t / 2)) + s for u, v in P]
    tr = earclip(P); T = [list(x) for x in tr] + [[i + n for i in x] for x in tr]
    for i in range(n):
        j = (i + 1) % n; T += [[i, j, j + n], [i, j + n, i + n]]
    tubes = [[i, (i + 1) % n, edge, outline] for i in range(n)] + [[i + n, (i + 1) % n + n, edge, outline] for i in range(n)] \
        + [[i, i + n, edge, outline] for i in range(n)]
    return {'v': np.round(V, 6).tolist(), 't': T, 'c': [face] * len(T), 'a': 1, 'tubes': tubes, 'rad': rad, 'balls': []}


TAN, TAN_EDGE = '#c9a77c', '#6e5434'
def octa_parts(pull):
    sh = {'A': (0, pull * 1.15, 0), 'B': (0, -pull * 1.15, 0), 'C1': (0, 0, pull * 1.25), 'C2': (0, 0, -pull * 1.25)}
    return [slab(PA, 'A', sh['A'], TAN, TAN_EDGE, None, 0.0024), slab(PB, 'B', sh['B'], TAN, TAN_EDGE, None, 0.0024),
            slab(PC1, 'C', sh['C1'], TAN, TAN_EDGE, None, 0.0024), slab(PC2, 'C', sh['C2'], TAN, TAN_EDGE, None, 0.0024)]

# ---------------- cube: corners, faces, fins ----------------
CV = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)]
CE = [(i, j) for i in range(8) for j in range(i + 1, 8) if np.abs(CV[i] - CV[j]).sum() == 2]                     # 12 edges
CF = []                                                                                                         # 6 faces, corners in cyclic order
for ax_ in range(3):
    for s in (-1, 1):
        ids = [i for i in range(8) if CV[i][ax_] == s]; c = np.mean([CV[i] for i in ids], axis=0)
        e1, e2 = [k for k in range(3) if k != ax_]
        ids.sort(key=lambda i: np.arctan2(CV[i][e2] - c[e2], CV[i][e1] - c[e1])); CF.append((ids, s * np.eye(3)[ax_]))


def tri_part(tris_xyz, col, alpha, edges_xyz, ecol, eout, rad, shift=(0, 0, 0)):
    V, T, E = [], [], []
    def vid(p):
        p = tuple(np.round(np.array(p, float) + shift, 6))
        if p not in V: V.append(p)
        return V.index(p)
    for tr in tris_xyz: T.append([vid(p) for p in tr])
    for p, q in edges_xyz: E.append([vid(p), vid(q), ecol, eout])
    return {'v': [list(p) for p in V], 't': T, 'c': [col] * len(T), 'a': alpha, 'tubes': E, 'rad': rad, 'balls': []}


O = np.zeros(3)
FINS = [(O, CV[i], CV[j]) for i, j in CE]
GLASS, GLASS_FIN, GLASS_EDGE, DARK = '#d6ebf2', '#a8d2e2', '#eef8fb', '#1a2329'
def cube_pyramids(pull):
    parts = []
    for ids, nrm in CF:
        sh = nrm * pull; base = [CV[i] for i in ids]
        tris = [(base[0], base[1], base[2]), (base[0], base[2], base[3])] + [(O, base[k], base[(k + 1) % 4]) for k in range(4)]
        edges = [(base[k], base[(k + 1) % 4]) for k in range(4)] + [(O, b) for b in base]
        parts.append(tri_part(tris, GLASS, 0.30, edges, GLASS_EDGE, DARK, 0.0028, sh))
    return parts
def cube_assembled():
    faces = [t for ids, _ in CF for t in ((CV[ids[0]], CV[ids[1]], CV[ids[2]]), (CV[ids[0]], CV[ids[2]], CV[ids[3]]))]
    shell = tri_part(faces, GLASS, 0.22, [(CV[i], CV[j]) for i, j in CE], GLASS_EDGE, DARK, 0.0028)
    fins = tri_part(FINS, GLASS_FIN, 0.55, [(O, p) for p in CV], GLASS_EDGE, DARK, 0.0022)
    return [fins, shell]
def cube_vacuus():
    return [tri_part(FINS, GLASS_FIN, 0.80, [(O, p) for p in CV] + [(CV[i], CV[j]) for i, j in CE], GLASS_EDGE, DARK, 0.0028)]

# ---------------- 3. white ring cube (DICTO, 24 Nov: six whole diagonal rectangles) ----------------
WHITE, WHITE_EDGE, WHITE_OUT = '#f3f0ea', '#dcd7cc', '#2a2a2e'
PLANES = {}                                     # six diagonal planes x_i = s x_j; each a whole rectangle through two opposite edges and O
for i, j in ((0, 1), (0, 2), (1, 2)):
    for s in (1, -1):
        nrm = np.zeros(3); nrm[i], nrm[j] = 1, -s; nrm /= np.linalg.norm(nrm)
        k = 3 - i - j                           # the axis along which the two cube edges of the rectangle run
        cs = [p for p in CV if p[i] == s * p[j]]
        lo = sorted([p for p in cs if p[k] == -1], key=lambda p: p[i]); hi = sorted([p for p in cs if p[k] == 1], key=lambda p: p[i])
        R = [lo[0], lo[1], hi[1], hi[0]]        # cyclic: edge lo[0]-hi[0] and edge lo[1]-hi[1] are the two opposite cube edges
        assert len(cs) == 4 and abs(np.dot(R[0] - R[1], R[1] - R[2])) < 1e-12
        PLANES[(i, j, s)] = (nrm, R)
def rect_part(nrm, R, shift):
    return tri_part([(R[0], R[1], R[2]), (R[0], R[2], R[3])], WHITE, 1, [(R[m], R[(m + 1) % 4]) for m in range(4)],
                    WHITE_EDGE, WHITE_OUT, 0.0030, np.asarray(shift, float))
def white_all():
    return [rect_part(n, R, (0, 0, 0)) for n, R in PLANES.values()]
def white_one(key=(0, 2, -1)):
    n, R = PLANES[key]                          # the rectangle with the cube's twelve edges as thin lines, to show where it sits
    return [rect_part(n, R, (0, 0, 0)), tri_part([], WHITE, 1, [(CV[i], CV[j]) for i, j in CE], '#8a8f99', None, 0.0016)]
# the three rectangles through the body diagonal from (-1,-1,-1) to (1,1,1): planes x = y, x = z, y = z; their unit normals
# (1,-1,0), (-1,0,1), (0,1,-1) (/sqrt 2) sum to zero, so pulling each along its own normal spreads them at 120 deg about the diagonal
TRIO = [((0, 1, 1), (1, -1, 0)), ((0, 2, 1), (-1, 0, 1)), ((1, 2, 1), (0, 1, -1))]
PULL3 = 2.4
def white_trio(pull):
    out = []
    for key, d in TRIO:
        n, R = PLANES[key]; d = np.array(d, float) / np.sqrt(2); assert abs(abs(np.dot(d, n)) - 1) < 1e-12
        out.append(rect_part(n, R, d * pull))
    return out


VO = [0.85, 0.62, 1.25]; VC = [1.0, 0.62, 1.45]; VT = [0.9, 0.3, -0.3]
scenes = [
    {'E': 1.22, 'dir': VO, 'parts': octa_parts(0)},          # p0 cardboard octahedron, assembled
    {'E': 2.75, 'dir': VO, 'parts': octa_parts(1)},          # p1 its four pieces pulled apart along their slide lines
    {'E': 1.95, 'dir': VC, 'parts': cube_assembled()},       # p2 B1NR cube: six pyramids, fins inside
    {'E': 3.6, 'dir': VC, 'parts': cube_pyramids(1.25)},     # p3 the six pyramids pulled apart
    {'E': 1.95, 'dir': VC, 'parts': cube_vacuus()},          # p4 the cube's Vacuus: twelve fins
    {'E': 1.95, 'dir': VC, 'parts': white_all()},            # p5 white ring cube: six whole diagonal rectangles, assembled
    {'E': 1.95, 'dir': VC, 'parts': white_one()},            # p6 one rectangle alone (plane x = -z, nearly face-on in this view)
    {'E': 3.6, 'dir': VT, 'parts': white_trio(PULL3)},       # p7 the three rectangles through one body diagonal, pulled apart
]
write(sys.argv[1], scenes)
ok = len(FINS) == 12 and len(CE) == 12 and len(PLANES) == 6 and t < w
print('scenes', len(scenes), 'board t', round(t, 5), 'slot w', round(w, 5), 'FINAL ok' if ok else 'FINAL FAIL')
