"""Exact SKELETAL renders of three of DICTO's Vacuus builds (paper #87 DICTO Vacuus Solids), 24 Nov 2026.
DICTO, 24 Nov: "the way I build all my PET bottle and B1NR sculptures is as Vacuus ... and hulls ... they are skeletons and empty".
So every build is drawn as an open framework: struts (tubes) and joints (balls), no faces; the empty space shows.
Not fitted to photos: every strut joins exact corners of the solid the build realises.
 1. Cardboard octahedron (corners +-e_i): its 12 edges + the 6 corner-to-centre struts (the three half-axes pairs), so the three
    squares x = 0, y = 0, z = 0 stand as frames (each: 4 edges + its 2 diagonals = 4 half-axes). Pull-apart: each square frame
    moved along its own normal.
 2. B1NR cube [-1,1]^3: the hull skeleton (12 edges) + the Vacuus skeleton (8 corner-to-centre struts): the empty cube that is six
    square pyramids meeting at the centre O. Clear tubes. Pull-apart: the six pyramid skeletons along the face normals.
 3. White ring cube: the six diagonal rectangles as open frames. Each rectangle = its outline (two opposite cube edges + two face
    diagonals) + its two diagonals through O (four corner-to-centre struts). Union: 12 edges + 12 face diagonals + 8 corner-to-centre
    struts. Views: assembled; one rectangle in white with the rest faint; the three through one body diagonal pulled apart.
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
FD = [(CV[i], CV[j]) for i in range(8) for j in range(i + 1, 8) if np.abs(CV[i] - CV[j]).sum() == 4]            # 12 face diagonals
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

# 3. white ring cube
WHITE, WHITE_OUT, WHITE_BALL, FAINT = '#f3f0ea', '#2a2a2e', '#e6e1d6', '#5d636d'
PLANES = {}
for i, j in ((0, 1), (0, 2), (1, 2)):
    for s in (1, -1):
        nrm = np.zeros(3); nrm[i], nrm[j] = 1, -s
        inn = lambda p: abs(np.dot(p, nrm)) < 1e-12
        st = [(p, q) for p, q in CE + FD + CS if inn(p) and inn(q)]
        assert len(st) == 8                      # outline: 2 edges + 2 face diagonals; X: 4 corner-to-centre struts
        PLANES[(i, j, s)] = (nrm / np.linalg.norm(nrm), st)
def white_all():
    return [skel(CE + FD + CS, WHITE, WHITE_OUT, 0.0085, WHITE_BALL)]
def white_one(key=(0, 2, -1)):
    n, st = PLANES[key]
    key_set = {tuple(np.round(np.r_[p, q], 6)) for p, q in st}
    rest = [(p, q) for p, q in CE + FD + CS if tuple(np.round(np.r_[p, q], 6)) not in key_set]
    return [skel(rest, FAINT, None, 0.0040, None), skel(st, WHITE, WHITE_OUT, 0.0095, WHITE_BALL)]
TRIO = [((0, 1, 1), (1, -1, 0)), ((0, 2, 1), (-1, 0, 1)), ((1, 2, 1), (0, 1, -1))]
PULL3 = 2.4
def white_trio(pull):
    out = []
    for key, d in TRIO:
        n, st = PLANES[key]; d = np.array(d, float) / np.sqrt(2); assert abs(abs(np.dot(d, n)) - 1) < 1e-12
        out.append(skel(st, WHITE, WHITE_OUT, 0.0085, WHITE_BALL, d * pull))
    return out


VO = [0.85, 0.62, 1.25]; VC = [1.0, 0.62, 1.45]; VT = [0.9, 0.3, -0.3]
scenes = [
    {'E': 1.30, 'dir': VO, 'parts': octa_all()},             # p0 octahedron skeleton: 12 edges + 6 half-axes (three square frames)
    {'E': 2.95, 'dir': VO, 'parts': octa_pulled(1.8)},       # p1 the three square frames pulled apart along their normals
    {'E': 1.95, 'dir': VC, 'parts': b1nr_all()},             # p2 B1NR cube: 12 edges + 8 corner-to-centre struts
    {'E': 4.1, 'dir': VC, 'parts': b1nr_pulled(1.8)},       # p3 its six pyramid skeletons pulled apart
    {'E': 1.95, 'dir': VC, 'parts': white_all()},            # p4 white ring cube: six rectangle frames assembled
    {'E': 1.95, 'dir': VC, 'parts': white_one()},            # p5 one rectangle frame (x = -z) in white, the rest faint
    {'E': 3.6, 'dir': VT, 'parts': white_trio(PULL3)},       # p6 the three rectangle frames through one body diagonal, pulled apart
]
render3d.write(sys.argv[1], scenes)
ok = (len(OE), len(OS), len(CE), len(FD), len(CS), len(PLANES)) == (12, 6, 12, 12, 8, 6) \
    and all(s['parts'][0]['t'] == [] for s in scenes) and all(p['t'] == [] for s in scenes for p in s['parts'])
print('scenes', len(scenes), 'no faces in any scene' if ok else '', 'FINAL ok' if ok else 'FINAL FAIL')
