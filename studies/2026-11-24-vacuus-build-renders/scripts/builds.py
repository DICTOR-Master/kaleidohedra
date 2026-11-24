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
 3. B1NR cuboctahedron Vacuus, NO hull (DICTO 24 Nov, "both B1NR no hulls"): the STRUTS form of #87 without its optional edges,
    one clear rod from O to each of the 12 corners (permutations of (+-1, +-1, 0)). Views: oblique; down a three-fold axis.
 4. B1NR dodecahedron Vacuus, NO hull: one clear rod from O to each of the 20 corners ((+-1, +-1, +-1) and the cyclic permutations
    of (0, +-1/phi, +-phi)). Views: oblique; down a five-fold axis (1, 0, phi).
 No pull-apart for 3 and 4: without edges a centre pyramid is a bare tuft of rods, so pulling them apart shows nothing new.
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

# 3. and 4. B1NR, no hull: the centre struts only (same clear tubes as the B1NR cube)
PHI = (1 + 5 ** 0.5) / 2
QV = [np.array(p, float) for p in {tuple(np.roll(q, r)) for q in itertools.product((1, -1), (1, -1), (0,)) for r in range(3)}]
DV = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)] + \
     [np.roll(np.array([0, a / PHI, b * PHI]), r) for a in (1, -1) for b in (1, -1) for r in range(3)]
assert len(QV) == 12 and len(DV) == 20
def centre_struts(V):
    return [b1nr([(O, p) for p in V])]
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
scenes = [
    {'E': 1.30, 'dir': VO, 'parts': octa_all()},             # p0 octahedron skeleton: 12 edges + 6 half-axes (three square frames)
    {'E': 2.95, 'dir': VO, 'parts': octa_pulled(1.8)},       # p1 the three square frames pulled apart along their normals
    {'E': 1.95, 'dir': VC, 'parts': b1nr_all()},             # p2 B1NR cube: 12 edges + 8 corner-to-centre struts
    {'E': EP, 'dir': VC, 'parts': b1nr_pulled(PULLB)},       # p3 its six pyramid skeletons pulled apart
    {'E': 1.62, 'dir': VC, 'parts': centre_struts(QV)},       # p4 cuboctahedron Vacuus, 12 centre struts, no hull
    {'E': 1.62, 'dir': V3, 'parts': centre_struts(QV)},       # p5 the same down a three-fold axis
    {'E': 1.95, 'dir': VC, 'parts': centre_struts(DV)},       # p6 dodecahedron Vacuus, 20 centre struts, no hull
    {'E': 1.95, 'dir': V5, 'parts': centre_struts(DV)},       # p7 the same down a five-fold axis
]
render3d.write(sys.argv[1], scenes)
ok = (len(OE), len(OS), len(CE), len(CS), len(QV), len(DV)) == (12, 6, 12, 8, 12, 20) and GAP >= 0.015 * render3d.PX and INFRAME \
    and all(s['parts'][0]['t'] == [] for s in scenes) and all(p['t'] == [] for s in scenes for p in s['parts'])
print('scenes', len(scenes), 'no faces in any scene' if ok else '', 'FINAL ok' if ok else 'FINAL FAIL')
