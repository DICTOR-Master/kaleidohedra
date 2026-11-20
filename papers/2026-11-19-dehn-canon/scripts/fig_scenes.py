# DICTO · dictospheres.com — scenes for the rendered figures of the Dehn Canon paper (renders/*.html, one scene per shot) and
# their labels (renders/*-labels.json, with label positions projected exactly as the camera draws). Every solid comes from
# canon_solids.py and passes its exact checks there first. Then: node shots.mjs renders/<f>.html renders/<f>; fig_compose.py.
import json, os
from fractions import Fraction as Fr
import numpy as np
import canon_solids as cs
from render3d import solid_part, write, project, basis, PX

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'renders'); os.makedirs(OUT, exist_ok=True)
APP = {'dodecahedron': '#8a5cc4', 'icosahedron': '#3a70cd', 'cube': '#488e48', 'tetrahedron': '#cd3e28', 'octahedron': '#e8c852',
       'CLEO': '#c792ea', 'AXE': '#4dd0e1', 'FUJI': '#c792ea'}          # app colours, only for the solid each stands for
NEUTRAL = '#aca290'                                                     # every other solid
ACOL = {'α': '#1f1f1f', 'β': '#9a6a2e', 'γ': '#5b6f8a', 'ε': '#a3a3a3', 'π − ε': '#a3a3a3'}   # Figure 3's angle colours
NOTQ, INQ = '#f2ead6', '#4a5f7e'                                        # Figure 4: angle not in ℚπ (cream) / in ℚπ (slate)
VIEW = (0.50, 0.40, 0.77)
log = []


def centred(S, scale=None):
    P = S.vf(); P = P - (P.max(0) + P.min(0)) / 2
    if scale: P = P / np.linalg.norm(P, axis=1).max() * scale
    return P


def pick_view(S, P, pref=VIEW, cone=28):
    """The view within `cone` degrees of `pref` that keeps the shortest edge on screen longest and no face edge-on."""
    pref = np.asarray(pref, float) / np.linalg.norm(pref); best, bv = -1, None
    N = [np.array([float(x) for x in f[0]]) for f in S.F]; N = [n / np.linalg.norm(n) for n in N]
    for th in np.linspace(0.15, np.pi - 0.15, 48):
        for ph in np.linspace(0, 2 * np.pi, 96, endpoint=False):
            v = np.array([np.sin(th) * np.cos(ph), np.cos(th), np.sin(th) * np.sin(ph)])
            if v @ pref < np.cos(np.radians(cone)): continue
            x, y, _ = basis(v); Q = np.c_[P @ x, P @ y]; R = np.abs(Q).max()
            s = min(np.linalg.norm(Q[a] - Q[b]) for a, b, *_ in S.E) / R
            s += 0.25 * min(abs(n @ v) for n in N)                              # no face edge-on
            if s > best: best, bv = s, v
    return bv


def fill(P, v, frac=0.93, E=1.08):
    """Scale centred corners so the drawing fills `frac` of the frame half-width E in view v."""
    x, y, _ = basis(v); Q = np.c_[P @ x, P @ y]; c = (Q.max(0) + Q.min(0)) / 2
    P = P - (c[0] * x + c[1] * y); Q = np.c_[P @ x, P @ y]
    return P / np.abs(Q).max() * frac * E


def segs2d(S, px):
    return [(px[a], px[b]) for a, b, *_ in S.E]


def clearance(p, segs, taken):
    m = 1e9
    for a, b in segs:
        d = b - a; t = np.clip((p - a) @ d / (d @ d + 1e-12), 0, 1); m = min(m, np.linalg.norm(a + t * d - p))
    for q in taken: m = min(m, np.linalg.norm(p - q) * 0.8)
    return m


def place(anchor, segs, taken, r, half_w=0, n=32):
    """Label position at distance r from anchor, in the direction farthest from every drawn edge and every placed label
    (a label of half-width half_w is tested at its two ends and its centre); kept inside the shot."""
    best, bp = -1, None
    for k in range(n):
        a = 2 * np.pi * k / n; p = anchor + r * np.array([np.cos(a), np.sin(a)])
        pts = [p + np.array([dx, 0]) for dx in (-half_w, 0, half_w)]
        if any(min(q) < 60 or max(q) > PX - 60 for q in pts): continue
        c = min(clearance(q, segs, taken) for q in pts)
        if c > best: best, bp = c, p
    taken.append(bp); return bp


# ---------- Figure A: the canon gallery ----------
ZERO = [('cube', cs.cube(), 'cube', '0'),
        ('rhombic dodecahedron', cs.rd(), None, '0'),
        ('cube ∩ rhombic dodecahedron', cs.cube_rd(1, Fr(3, 2)), None, '0 · drawn at s = 1, c = 3/2'),
        ('truncated octahedron', cs.cube_oct(Fr(3, 2)), None, '0 · cube ∩ octahedron, t = 3/2'),
        ('rhombic triacontahedron', cs.rt(), None, '0'),
        ('golden rhombohedron, prolate', cs.prolate(), None, '0'),
        ('golden rhombohedron, oblate', cs.oblate(), None, '0')]
T7 = Fr(17566, 10000)                                                   # the fair 14-face die, t = 1.7566… [10], drawn at 1.7566
NONZERO = [('dodecahedron', cs.dodeca(), 'dodecahedron', '−30(2√5 − 2) ⊗ α'),
           ('icosahedron', cs.icosa(), 'icosahedron', '−120 ⊗ γ'),
           ('tetrahedron', cs.tetra(), 'tetrahedron', '12√2 ⊗ arccos(1/3)'),
           ('octahedron', cs.octa(), 'octahedron', '−12√2 ⊗ arccos(1/3)'),
           ('fair 14-face die', cs.cube_oct(T7), None, '12√2(2t − 3) ⊗ arccos(1/3), t = 1.7566…'),
           ('CLEO', cs.word('CLEO'), 'CLEO', '3 ⊗ α + 3g ⊗ β'),
           ('AXE', cs.word('AXE'), 'AXE', '(1 + g) ⊗ α + 6 ⊗ β'),
           ('FUJI', cs.word('FUJI'), 'FUJI', '(9 − 3g) ⊗ α + (12 − 3g) ⊗ β')]
for nm, S, key, _ in ZERO[1:]:
    if nm != 'truncated octahedron': log.append(cs.check_zero(nm, S))
log.append(cs.check('cube', ZERO[0][1])); log.append(cs.check_co(Fr(3, 2), ZERO[3][1])); log.append(cs.check_co(T7, NONZERO[4][1]))
for nm, S, key, _ in NONZERO:
    if key: log.append(cs.check(key, S))
scenes, labels = [], []
for block in (ZERO, NONZERO):
    for nm, S, key, sub in block:
        P = centred(S, 1.0); v = pick_view(S, P); P = fill(P, v); col = APP[key] if key else NEUTRAL
        scenes.append({'E': 1.08, 'dir': v.tolist(), 'parts': [solid_part(S, col, P, rad=0.0055)]})
        labels.append({'title': nm, 'sub': sub, 'zero': block is ZERO})
write(os.path.join(OUT, 'canon.html'), scenes); json.dump(labels, open(os.path.join(OUT, 'canon-labels.json'), 'w'), indent=1)

# ---------- Figure B: Dehn's pair and Hilbert's pair ----------
up = lambda P: np.c_[P[:, 0], P[:, 2], -P[:, 1]]                       # z of the paper drawn upward
Tt, Cu = cs.tetra(), cs.cube()
s3 = 3 ** (1 / 3)                                                       # tetrahedron (±1) has volume 8/3; × ∛3 gives 8 = the cube's
assert cs.vol_tet([(-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]) == Fr(8, 3) and Fr(8, 3) * 3 == 8
log.append('Dehn pair: tetrahedron × ∛3 and the cube [−1, 1]³ both have volume 8')
ecol = lambda S: [NOTQ if not e[4] else INQ for e in S.E]
eout = lambda S: ['#2b261e' if not e[4] else '#efe6d2' for e in S.E]
assert all(not e[4] for e in Tt.E) and all(e[4] for e in Cu.E)
B_E = 2.65; B_DIR = (0.55, 0.38, 0.74)
sc_b, lab_b = [], []
for S, col, P in [(Tt, APP['tetrahedron'], Tt.vf() * s3), (Cu, APP['cube'], Cu.vf())]:
    vb = np.array((-0.45, 0.75, 0.48)) if S is Tt else np.array(B_DIR)      # the tetrahedron seen near a corner: three faces
    sc_b.append({'E': B_E, 'dir': vb.tolist(), 'parts': [solid_part(S, col, P, rad=0.011, edge_cols=ecol(S), outline=eout(S), ball='#2b261e')]})
H_DIR = (0.95, 0.80, 1.55); H_E = 0.98; ctr = np.array([0.5, 0.5, 0.5])
for nm, S, apex in [('T', cs.hilbert_T(), 'D'), ("T'", cs.hilbert_T2(), 'D′')]:
    P = up(S.vf() - ctr)
    base = [k for k, f in enumerate(S.F) if f[1] == 0 and f[0][0] == 0 and f[0][1] == 0 and f[0][2].sign() < 0]
    assert len(base) == 1 and sorted(S.F[base[0]][2]) == [0, 1, 2]       # the face ABC on z = 0, outward normal down
    side = [k for k in range(len(S.F)) if k != base[0]]
    parts = [solid_part(S, NEUTRAL, P, alpha=0.5, rad=0.016, edge_cols=ecol(S), outline=eout(S), ball='#2b261e', faces=side),
             solid_part(S, '#f3e2b0', P, alpha=0.55, rad=0.016, faces=base)]
    parts[1]['tubes'] = []
    sc_b.append({'E': H_E, 'dir': H_DIR, 'parts': parts})
    names = ['A', 'B', 'C', apex]
    V = S.vf(); px = project(P, H_DIR, H_E); c2 = px.mean(0)
    pts = []; sg = segs2d(S, px); taken = []
    foot = (0, 0, 0) if apex == 'D' else (0, 1, 0)
    ia = [i for i, v in enumerate(V) if v[2] == 1][0]; iff = [i for i, v in enumerate(V) if tuple(v) == foot][0]
    # the height: the edge from the apex straight down to the base (AD for T, CD′ for T′), length 1 = the altitude
    assert np.allclose(V[ia] - V[iff], [0, 0, 1])
    for i, v in enumerate(V):
        nmv = {(0, 0, 0): 'A', (1, 0, 0): 'B', (0, 1, 0): 'C'}.get(tuple(v), apex)
        pts.append([nmv, place(px[i], sg, taken, 78).tolist()])
    hp = place((px[ia] + px[iff]) / 2, sg, taken, 175, half_w=130)
    lab_b.append({'name': nm, 'pts': pts, 'height': hp.tolist()})
    log.append(cs.check(nm, S) + f'; volume {cs.vol_tet([cs.A0, cs.B0, cs.C0, cs.D0 if apex == "D" else cs.D1])}, height 1')
write(os.path.join(OUT, 'pairs.html'), sc_b); json.dump(lab_b, open(os.path.join(OUT, 'pairs-labels.json'), 'w'), indent=1)

# ---------- Figure C: the cube ∩ octahedron line ----------
TS = [Fr(1), Fr(9, 8), Fr(5, 4), Fr(11, 8), Fr(3, 2), Fr(13, 8), T7, Fr(15, 8)]
sc_c, lab_c = [], []
C_DIR = (0.62, 0.47, 0.63); C_E = 1.44
for t in TS:
    S = cs.cube_oct(t); log.append(cs.check_co(t, S))
    col = APP['octahedron'] if t == 1 else NEUTRAL
    sc_c.append({'E': C_E, 'dir': C_DIR, 'parts': [solid_part(S, col, S.vf(), rad=0.0065)]})
    lab_c.append({'t': str(t), 'coef': float(12 * (2 * t - 3))})
write(os.path.join(OUT, 'line.html'), sc_c); json.dump(lab_c, open(os.path.join(OUT, 'line-labels.json'), 'w'), indent=1)

# ---------- Figure D: CLEO, AXE, FUJI rendered, edges by angle ----------
def good_view(S, P):
    """A view direction (grid search, both it and its opposite are drawn) that keeps every edge long on screen and corners apart."""
    best, bv = -1, None
    for th in np.linspace(0.2, np.pi - 0.2, 40):
        for ph in np.linspace(0, 2 * np.pi, 80, endpoint=False):
            v = np.array([np.sin(th) * np.cos(ph), np.cos(th), np.sin(th) * np.sin(ph)])
            x, y, _ = basis(v); Q = np.c_[P @ x, P @ y]
            s = min(np.linalg.norm(Q[a] - Q[b]) for a, b, *_ in S.E) / np.linalg.norm(P, axis=1).max()
            if s > best: best, bv = s, v
    return bv
sc_d, lab_d = [], []
for nm in ['CLEO', 'AXE', 'FUJI']:
    S = cs.word(nm); log.append(cs.check(nm, S)); P = centred(S, 1.0); v = good_view(S, P); P = fill(P, v, 0.86, 1.12)
    N = [np.array([float(x) for x in f[0]]) for f in S.F]
    for side, dv in (('front', v), ('back', -v)):
        cols = [ACOL[e[3]] for e in S.E]
        sc_d.append({'E': 1.12, 'dir': dv.tolist(), 'parts': [solid_part(S, APP[nm], P, rad=0.024, edge_cols=cols, outline='#efe6d2', ball='#3a332b')]})
        px = project(P, dv, 1.12); el = []; sg = segs2d(S, px); taken = []
        for a, b, l2, cl, rat in S.E:
            fa = [k for k, f in enumerate(S.F) if a in f[2] and b in f[2]]
            if not any(N[k] @ dv > 1e-9 for k in fa): continue           # hidden in this view (seen in the other)
            el.append([cl, place((px[a] + px[b]) / 2, sg, taken, 70, half_w=40 if len(cl) > 1 else 0).tolist()])
        lab_d.append({'name': nm, 'side': side, 'edges': el})
    vis = lambda dv: {(a, b) for a, b, *_ in S.E if any(N[k] @ dv > 1e-9 for k, f in enumerate(S.F) if a in f[2] and b in f[2])}
    assert vis(v) | vis(-v) == {(a, b) for a, b, *_ in S.E}, nm          # every edge is seen in one of the two views
write(os.path.join(OUT, 'words.html'), sc_d); json.dump(lab_d, open(os.path.join(OUT, 'words-labels.json'), 'w'), indent=1)
open(os.path.join(OUT, 'fig-scenes.log'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log)); print('scenes', len(scenes), len(sc_b), len(sc_c), len(sc_d)); print('FINAL ok')
