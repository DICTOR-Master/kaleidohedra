# Renders for the exact-vs-dissection study: each Kaleidohedra solid beside its classical construction.
# Face colours as the app's Targets world (square blue, rhombus pink, regular hexagon gold, other hexagon purple);
# classical pieces in the app's gold / purple / blue. Drawn from the data files (exact corners, as floats).
# DICTO · dictospheres.com, 2026-10-23
import json, math, os, sys, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact as X

HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, 'data'); OUT = os.path.join(HERE, 'renders')
os.makedirs(OUT, exist_ok=True)
GROUND = (20, 15, 11); INK = (233, 224, 208); EDGE = (11, 18, 32)
KIND = {'square': (0x5b, 0x8d, 0xef), 'rhombus': (0xf0, 0x62, 0x92), 'regular hexagon': (0xff, 0xc8, 0x57), 'hexagon': (0xa7, 0x7b, 0xf3)}
GOLD, PURPLE, BLUE, PINK = (232, 200, 82), (138, 92, 196), (110, 160, 225), (0xf0, 0x62, 0x92)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SS = 2  # supersampling


def kind_colour(k):
    if k.startswith('rhombus') or k == 'golden rhombus': return KIND['rhombus']
    if k == 'regular hexagon': return KIND['regular hexagon']
    if 'hexagon' in k: return KIND['hexagon']
    return KIND.get(k, (180, 180, 180))


def rot(axis, a):
    a_ = np.asarray(axis, float); a_ /= np.linalg.norm(a_)
    K = np.array([[0, -a_[2], a_[1]], [a_[2], 0, -a_[0]], [-a_[1], a_[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K


GID = None
VIEW = rot((1, 0, 0), -1.05) @ rot((0, 0, 1), 0.42)
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)


def draw(polys, px, R=VIEW, scale=None):
    """polys: list of (3D float polygon, colour[, piece id]). Pieces drawn back to front; back faces dropped."""
    global GID
    GID = [t[2] if len(t) > 2 else 0 for t in polys]
    P = [(np.asarray(t[0], float) @ R.T, t[1]) for t in polys]
    allp = np.vstack([p for p, _ in P]); ctr = (allp.max(0) + allp.min(0)) / 2
    ext = max(allp[:, 0].max() - allp[:, 0].min(), allp[:, 1].max() - allp[:, 1].min())
    s = scale or 0.82 * px * SS / ext
    img = Image.new('RGB', (px * SS, px * SS), GROUND); d = ImageDraw.Draw(img)
    vis = []
    groups = {}
    for gi, (p, c) in enumerate(P): groups.setdefault(GID[gi] if GID else 0, []).append((p, c))
    depth = {g: np.vstack([p for p, _ in fs]).mean(0)[2] for g, fs in groups.items()}
    for g in sorted(groups, key=lambda g: depth[g]):            # whole pieces back to front (convex pieces, set apart)
        for p, c in groups[g]:
            n = np.cross(p[1] - p[0], p[2] - p[1]); n /= np.linalg.norm(n)
            if n[2] > 1e-9: vis.append((p, c, n))
    for p, c, n in vis:
        sh = 0.42 + 0.58 * max(0.0, float(n @ LIGHT))
        col = tuple(int(min(255, x * sh)) for x in c)
        pts = [((x - ctr[0]) * s + px * SS / 2, -(y - ctr[1]) * s + px * SS / 2) for x, y, _ in p]
        d.polygon(pts, fill=col); d.line(pts + [pts[0]], fill=EDGE, width=2 * SS, joint='curve')
    return img.resize((px, px), Image.LANCZOS)


def solid_polys(rec, colour=None):
    Vf = np.array(rec['vertices_float']); Vx = [X.vparse(v) for v in rec['vertices_exact']]
    return [(Vf[f], colour or kind_colour(X.face_kind(Vx, f))) for f in rec['faces']]


def piece_polys(points_exact, colour, shift=(0, 0, 0), gid=0):
    Vx, F = X.hull([X.vparse(p) for p in points_exact])
    Vf = np.array([[float(x) for x in v] for v in Vx]) + np.asarray(shift, float)
    return [(Vf[f], colour, gid) for f in F]


def exploded(pieces, colours, k=0.35):
    allc = np.vstack([np.array([[float(x) for x in X.vparse(p)] for p in P]) for P in pieces]).mean(0)
    out = []
    for gi, (P, c) in enumerate(zip(pieces, colours)):
        cen = np.array([[float(x) for x in X.vparse(p)] for p in P]).mean(0)
        out += piece_polys(P, c, k * (cen - allc), gi)
    return out


def zone_polys(gens_exact, highlight, base=GOLD, hi=PURPLE):
    """A zonotope with the faces of the zones parallel to the generators in `highlight` coloured hi."""
    g = [X.vparse(v) for v in gens_exact]
    Vx, F, info = X.zonotope(g)
    Vf = np.array([[float(x) for x in v] for v in Vx])
    return [(Vf[f], hi if any(h in z for h in highlight) else base) for f, z in zip(F, info['zones'])]


def sheet(panels, title, fname, px=520):
    fb = ImageFont.truetype(FONT, 22); fs = ImageFont.truetype(FONT, 17); fm = ImageFont.truetype(FONT, 14)
    W = px * len(panels); H = px + 150
    S = Image.new('RGB', (W, H), GROUND); d = ImageDraw.Draw(S)
    d.text((W / 2, 18), title, font=fb, fill=INK, anchor='mt')
    for i, panel in enumerate(panels):
        polys, cap1, cap2 = panel[:3]; R = panel[3] if len(panel) > 3 else VIEW
        S.paste(draw(polys, px, R), (i * px, 50))
        d.text((i * px + px / 2, 50 + px + 8), cap1, font=fs, fill=INK, anchor='mt')
        d.text((i * px + px / 2, 50 + px + 34), cap2, font=fm, fill=(190, 180, 160), anchor='mt')
    try:
        logo = Image.open('/home/dicto/dictospheres/dicto-logo.png').convert('RGBA').resize((40, 40), Image.LANCZOS)
        S.paste(logo, (W - 250, H - 48), logo)
    except OSError:
        pass
    d.text((W - 12, H - 28), 'DICTO · dictospheres.com', font=fm, fill=GOLD, anchor='rm')
    d.text((12, H - 28), 'exact study 2026-10-23 · exact computation with Claude (Anthropic)', font=fm, fill=(150, 140, 120), anchor='lm')
    S.save(os.path.join(OUT, fname)); print('wrote', fname)


J = lambda f: json.load(open(os.path.join(DATA, f)))

# 1. regular-hexagon ED beside the truncated octahedron with one zone to shrink
f5 = J('regular-hexagon-ed.json')
to_gens = f5['classical_exact'][1]['identity_zonotope']
sheet([(solid_polys(f5), 'Kaleidohedra: Bain stretch, Cell = 1, + fifth direction', 'squares blue, 60° rhombi pink, regular hexagons gold'),
       (zone_polys(to_gens, [0]), 'Classical: truncated octahedron, purple zone shrunk to 0', 'Fedorov § 83; Wikipedia "contraction"')],
      'Regular-hexagon elongated dodecahedron (F5): volume 4√2 at edge 1', 'regular-hexagon-ed.png')

# 2. Bain RD beside cuboctahedron + two square pyramids, and the TO with two zones to shrink
b = J('bain-rd.json'); pcs = b['classical_exact'][0]['pieces']
perp = [i for i, g in enumerate(to_gens) if X.vparse(g) not in [X.vparse(x) for x in b['classical_exact'][1]['zonotope']]]
sheet([(solid_polys(b), 'Kaleidohedra: Towards Bain stop 2, Cell = 1', 'squares blue, 60° rhombi pink'),
       (exploded(pcs, [GOLD, PURPLE, PURPLE], 0.5), 'Classical: cuboctahedron + 2 square pyramids', 'Wikipedia (D4h form), shown apart'),
       (zone_polys(to_gens, perp), 'Classical: truncated octahedron, 2 zones shrunk', 'Fedorov § 83 (purple zones)')],
      'Bain rhombic dodecahedron (#4): volume 2√2 at edge 1', 'bain-rd.png')

# 3. the ED type: classical equilateral ED beside RD halves + square prism; and F7's two EDs with DICTO's RD
ed = J('elongated-dodecahedron-type.json'); ce = ed['members']['classical_equilateral_ED']
sheet([(solid_polys(ce), 'Kaleidohedra: FCC, Cell = 1, + fifth direction s = edge', '70.53° rhombi pink, hexagons purple'),
       (exploded(ce['classical_exact'][1]['pieces'], [GOLD, PURPLE, GOLD], 0.45), 'Classical: RD halves capping a square prism', 'Polytope Wiki / MathWorld, shown apart'),
       (solid_polys(ed['members']['bain_ED_along_z_TARGETS_23']), 'Same move on the Bain lattice, other free line', 'TARGETS #23: 8 rhombi 60°, 4 hexagons 135/135/90')],
      'The elongated dodecahedron as a type: RD + one free direction (stretch)', 'ed-type.png')
fl = ed['members']['dicto_free_lines']; k16 = ed['F7_partitions']['ED16'][0]; k18 = ed['F7_partitions']['ED18'][0]
sheet([(solid_polys(ed['members']['dicto_skewed_RD_F1']), "DICTO's skewed RD (F1): DICTO FCC, Cell = 1", '60° and 72° rhombi, volume φ²'),
       (solid_polys(fl[k16]['solid']), f'F7 ED #16: + free line {k16}', 'volume φ² + 2'),
       (solid_polys(fl[k18]['solid']), f'F7 ED #18: + free line {k18}', 'volume φ³ + 1/2')],
      "DICTO's skewed elongated dodecahedra (F7): the same stretch on DICTO FCC", 'f7-skewed-eds.png')

# 4. Bilinski: Kaleidohedra cell, the triacontahedron with two zones to delete, the four golden rhombohedra
bil = J('bilinski-dodecahedron.json')
F6 = bil['classical_exact'][0]['zone_deletion_generators']
hz = bil['classical_exact'][1]['pieces']
kinds = []
for P in hz:
    Vp = [X.vparse(p) for p in P]; o = Vp[0]
    nb = sorted(Vp[1:], key=lambda v: float(X.dot(X.sub(v, o), X.sub(v, o))))[:3]
    e = [X.sub(v, o) for v in nb]; s = (X.dot(e[0], e[1]) * X.dot(e[0], e[2]) * X.dot(e[1], e[2])).sign()
    kinds.append(GOLD if s > 0 else PURPLE)
VB = rot((0, 1, 0), 0.9) @ rot((1, 0, 0), -0.7)
sheet([(solid_polys(bil), 'Kaleidohedra: FCC with γ = 36°, Cell = 1', '12 golden rhombi, edges equal', VB),
       (zone_polys(F6, [4, 5]), 'Classical: triacontahedron, 2 zones deleted', 'Grünbaum Fig. 4 (purple zones)', VB),
       (exploded(hz, kinds, 0.9), 'Classical: 2 acute + 2 obtuse golden rhombohedra', 'Hafner–Zitko gluing; acute gold, obtuse purple', VB)],
      'Bilinski dodecahedron: one FCC angle from 60° to 36°, then Cell = 1', 'bilinski.png')

# 5. 60-degree rhombohedron beside tetrahedron + octahedron + tetrahedron
rh = J('rhombohedron-60.json'); pcs = rh['classical_exact'][0]['pieces']
VR = rot((0, 1, 0), 0.9) @ rot((1, 0, 0), -0.7) @ rot((1, -1, 0), 0.6)
sheet([(solid_polys(rh), 'Kaleidohedra: cube lattice sheared to 60°', 'six 60° rhombi, volume 1/√2', VR),
       (exploded(pcs, [GOLD, PURPLE, PURPLE], 0.5), 'Classical: tetrahedron + octahedron + tetrahedron', 'Maurolico (Lagarias–Zong 2012), shown apart', VR)],
      'The 60° rhombohedron: a worked example', 'rhombohedron-60.png')
