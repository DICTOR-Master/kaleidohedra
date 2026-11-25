# DICTO · dictospheres.com — the figures of "Which Platonic Solids Fill Space: Aristotle's Error, Machine-Checked" (blueprint
# draft, 25 Nov 2026), in the house look of #118 v2: scenes for render3d.py of study 2026-11-21-scutoid-stand-in (unchanged),
# shot by its shots.mjs, composed by its compose.py.  With Claude (Anthropic).
#   Figure 1: the five Platonic solids, D I C T O, in the exact coordinates of the Lean sets (dhSet, ihSet, cuSet, teSet, ocSet),
#             each with its dihedral angle; one edge of each marked with its wedge.
#   Figure 2: rings round one edge: five tetrahedra (gap 2π − 5 arccos(1/3)), three octahedra (gap 3 arccos(1/3) − π),
#             and tetrahedron, octahedron, tetrahedron, octahedron (closed exactly: 2 arccos(1/3) + 2(π − arccos(1/3)) = 2π).
# Usage: python fig_scenes.py scenes -> renders/fig*.html, renders/meta.json, scripts/fig_checks.log
#        python fig_scenes.py compose -> figures/fig*.jpg, renders/PREVIEW-aristotle-fig*.png
import json, os, sys, itertools, types
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); PAPER = os.path.normpath(os.path.join(HERE, '..'))
ST = os.environ.get('STUDIES', os.path.normpath(os.path.join(PAPER, '../../studies')))
REN = os.path.join(PAPER, 'renders'); FIG = os.path.join(PAPER, 'figures')
sys.path.insert(0, os.path.join(ST, '2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)

# element colours (app colours, used only for the solids they stand for)
COL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}
TEAL, INK = (64, 170, 160), (43, 38, 30)
EDGE = '#2b261e'
def hx(c): return '#%02x%02x%02x' % tuple(int(round(x)) for x in c)
def shade(c, k): return tuple(int(round(x * (1 + k) if k < 0 else x + (255 - x) * k)) for x in c)

# ---- exact corners: the Lean sets (teSet corners (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1); ocSet ±e_i; cuSet (±1,±1,±1)) ----
f5 = sp.sqrt(5); ph = (1 + f5) / 2
def cyc(p): return [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]
def signs(p): return {tuple(s * x for s, x in zip(sg, p)) for sg in itertools.product((1, -1), repeat=3)}
EXV = {
 'T': [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
 'O': sorted(signs((1, 0, 0)) | signs((0, 1, 0)) | signs((0, 0, 1))),
 'C': sorted(signs((1, 1, 1))),
 'D': sorted(signs((1, 1, 1)) | {q for c in cyc((0, 1 / ph, ph)) for q in signs(c)}, key=str),
 'I': sorted({q for c in cyc((0, 1, ph)) for q in signs(c)}, key=str)}
def faces_of(V):
    """faces of the convex hull of V (exact sympy points): lists of corner indices, ordered round the outward normal."""
    V = [sp.Matrix(v) for v in V]; n = len(V); F = {}
    for i, j, k in itertools.combinations(range(n), 3):
        N = (V[j] - V[i]).cross(V[k] - V[i])
        if N == sp.zeros(3, 1): continue
        s = [sp.simplify(N.dot(V[m] - V[i])) for m in range(n)]
        if all(x <= 0 for x in s) or all(x >= 0 for x in s):
            if all(x >= 0 for x in s): N = -N
            on = tuple(m for m in range(n) if s[m] == 0)
            F[on] = N
    out = []
    for on, N in F.items():
        c = sum((V[m] for m in on), sp.zeros(3, 1)) / len(on)
        Nf = np.array([float(x) for x in N]); Nf /= np.linalg.norm(Nf)
        u = np.array([float(x) for x in (V[on[0]] - c)]); u /= np.linalg.norm(u); w = np.cross(Nf, u)
        ang = lambda m: np.arctan2(np.array([float(x) for x in (V[m] - c)]) @ w, np.array([float(x) for x in (V[m] - c)]) @ u)
        out.append((sorted(on, key=ang), N))
    return out
def edges_of(F):
    E = set()
    for f, _ in F:
        for a, b in zip(f, f[1:] + f[:1]): E.add((min(a, b), max(a, b)))
    return sorted(E)

SOL = {}
for k in 'DICTO':
    V = EXV[k]; F = faces_of(V); E = edges_of(F)
    L = {sp.nsimplify(sp.simplify(sum((sp.Integer(a) - b) ** 2 if isinstance(a, int) else (a - b) ** 2 for a, b in zip(V[i], V[j])))) for i, j in E}
    # dihedral angle, exact: π − angle between outward normals of two faces at one edge
    (f0, N0), = [x for x in F if E[0][0] in x[0] and E[0][1] in x[0]][:1]
    (f1, N1), = [x for x in F if E[0][0] in x[0] and E[0][1] in x[0]][1:2]
    cosn = sp.nsimplify(sp.simplify(N0.dot(N1) / sp.sqrt(N0.dot(N0) * N1.dot(N1))))
    dih = sp.pi - sp.acos(cosn)
    assert len(L) == 1, (k, L)
    SOL[k] = dict(V=np.array([[float(x) for x in v] for v in V]), F=[f for f, _ in F], E=E, dih=dih, cos=-cosn, edge2=list(L)[0])
    log(k, 'corners', len(V), 'faces', len(F), 'edges', len(E), 'edge^2', list(L)[0], 'dihedral', sp.simplify(dih), '=', float(dih) * 180 / np.pi, 'deg')
assert [len(SOL[k]['F']) for k in 'DICTO'] == [12, 20, 6, 4, 8]
a = sp.acos(sp.Rational(1, 3))
C_ = {k: SOL[k]['cos'] for k in 'DICTO'}   # dihedral angles in (0, π): equal cosines = equal angles
assert C_['T'] == sp.Rational(1, 3) and C_['O'] == -sp.Rational(1, 3) and C_['C'] == 0, C_
SOL['T']['dih'] = a; SOL['O']['dih'] = sp.pi - a; SOL['C']['dih'] = sp.pi / 2
assert sp.simplify(C_['D'] + 1 / f5) == 0 and sp.simplify(C_['I'] + f5 / 3) == 0, C_
gapT = 2 * sp.pi - 5 * a; gapO = 3 * a - sp.pi; mix = 2 * a + 2 * (sp.pi - a)
assert sp.simplify(mix - 2 * sp.pi) == 0 and float(gapT) > 0 and float(gapO) > 0
log('five tetrahedra: gap 2pi - 5 acos(1/3) =', float(gapT) * 180 / np.pi, 'deg; three octahedra: gap 3 acos(1/3) - pi =', float(gapO) * 180 / np.pi, 'deg; T,O,T,O: 2pi exactly')

def part(V, F, col, alpha=1.0, rad=0.008, edges=None, ecol=EDGE):
    tris, cols = [], []
    for f in F:
        for b, c in zip(f[1:-1], f[2:]): tris.append([f[0], b, c]); cols.append(hx(col))
    E = edges if edges is not None else edges_of([(f, None) for f in F])
    return {'v': np.round(V, 6).tolist(), 't': tris, 'c': cols, 'a': alpha, 'tubes': [[int(i), int(j), ecol, None] for i, j in E], 'rad': rad, 'balls': []}
def extent(parts, dirv, m=1.10):
    x, y, _ = R3.basis(dirv); P = np.vstack([np.asarray(p['v']) for p in parts])
    return float(m * max(np.abs(P @ x).max(), np.abs(P @ y).max()))
def rotz(t): c, s = np.cos(t), np.sin(t); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def on_edge(k):
    """the solid moved so its first edge lies on the z axis (midpoint at 0), with its wedge starting at angle 0 (counter-clockwise)."""
    S = SOL[k]; V = S['V'] / np.sqrt(float(S['edge2'])); i, j = S['E'][0]      # unit edge length
    m = (V[i] + V[j]) / 2; V = V - m; z = V[j] - V[i]; z /= np.linalg.norm(z)
    c = V.mean(0); c -= (c @ z) * z; x = c / np.linalg.norm(c); y = np.cross(z, x); V = V @ np.array([x, y, z]).T
    th = np.arctan2(V[:, 1], V[:, 0]); dih = float(S['dih'])
    V = V @ rotz(dih / 2).T                                                     # wedge now spans [0, dih]
    th = np.arctan2(V[:, 1], V[:, 0]); r = np.hypot(V[:, 0], V[:, 1])
    assert th[r > 1e-9].min() > -1e-9 and th[r > 1e-9].max() < dih + 1e-9
    return V

def gap_wedge(t0, t1, R=0.9, h=0.5, k=24):
    ts = np.linspace(t0, t1, k + 1); P = [np.array([0, 0, -h]), np.array([0, 0, h])]
    for t in ts: P += [np.array([R * np.cos(t), R * np.sin(t), -h]), np.array([R * np.cos(t), R * np.sin(t), h])]
    F = []
    for q in range(k):
        a0, a1, b0, b1 = 2 + 2 * q, 3 + 2 * q, 4 + 2 * q, 5 + 2 * q
        F += [[0, b0, a0], [1, a1, b1], [a0, b0, b1, a1]]
    return {'v': np.round(np.array(P), 6).tolist(), 't': [[f[0], f[b], f[b + 1]] for f in F for b in range(1, len(f) - 1)],
            'c': [hx(TEAL)] * sum(len(f) - 2 for f in F), 'a': 0.55, 'tubes': [[0, 1, hx(TEAL), None]], 'rad': 0.004, 'balls': []}

def fig1():
    scenes, meta = [], []
    D1 = (0.42, 0.33, 1.0)
    for k in 'DICTO':
        S = SOL[k]; V = S['V'] / np.sqrt(float(S['edge2'])) * 1.0
        V = V / np.linalg.norm(V, axis=1).max()                                 # same circumradius for the picture
        i, j = S['E'][0]
        p = part(V, S['F'], COL[k], 1.0, 0.010)
        scenes.append({'E': 1.25, 'dir': D1, 'parts': [p]})
        meta.append(dict(k=k, dih=str(sp.simplify(S['dih'])), deg=float(S['dih']) * 180 / np.pi, F=len(S['F'])))
    R3.write(os.path.join(REN, 'fig1.html'), scenes); return meta

def fig2():
    scenes, meta = [], []
    DV = (0.30, -0.55, 1.0); TOP = (0.0001, -0.0001, 1.0)
    rings = [('five tetrahedra', 'TTTTT'), ('three octahedra', 'OOO'), ('tetrahedron, octahedron, tetrahedron, octahedron', 'TOTO')]
    for name, seq in rings:
        parts, t = [], 0.0
        for q, k in enumerate(seq):
            V = on_edge(k) @ rotz(t).T; t += float(SOL[k]['dih'])
            parts.append(part(V, SOL[k]['F'], shade(COL[k], -0.10 * (q % 2)), 1.0, 0.009))
        gap = 2 * np.pi - t
        if gap > 1e-9: parts.append(gap_wedge(t, 2 * np.pi))
        meta.append(dict(name=name, gap_deg=gap * 180 / np.pi))
        E = extent(parts, TOP, 1.12)
        scenes += [{'E': E, 'dir': TOP, 'parts': parts}, {'E': extent(parts, DV, 1.12), 'dir': DV, 'parts': parts}]
    assert abs(meta[0]['gap_deg'] - float(gapT) * 180 / np.pi) < 1e-9 and abs(meta[1]['gap_deg'] - float(gapO) * 180 / np.pi) < 1e-9 and abs(meta[2]['gap_deg']) < 1e-9
    R3.write(os.path.join(REN, 'fig2.html'), scenes); return meta

if __name__ == '__main__':
    os.makedirs(REN, exist_ok=True); os.makedirs(FIG, exist_ok=True)
    if sys.argv[1] == 'scenes':
        meta = {'fig1': fig1(), 'fig2': fig2()}
        json.dump(meta, open(os.path.join(REN, 'meta.json'), 'w'), indent=1)
        LOG.append('FINAL ok'); open(os.path.join(HERE, 'fig_checks.log'), 'w').write('\n'.join(LOG) + '\n'); print('FINAL ok')
    else:
        from PIL import Image
        src = open(os.path.join(ST, '2026-11-21-scutoid-stand-in/renders/scripts/compose.py')).read()
        Cp = types.ModuleType('compose_defs'); Cp.__dict__['__file__'] = os.path.join(REN, 'x')
        exec(src[:src.index('s = lambda')], Cp.__dict__)
        Cp.OUT = REN; Cp.MARK = 'DICTO · dictospheres.com'
        meta = json.load(open(os.path.join(REN, 'meta.json'))); sh_ = lambda f, i: os.path.join(REN, 'shots', f, f'p{i}.png')
        def done(png, jpg, prev):
            im = Image.open(os.path.join(REN, png)).convert('RGB'); im.save(os.path.join(FIG, jpg), quality=90, optimize=True)
            w = 2000; im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(os.path.join(REN, prev), optimize=True)
        NAME = {'D': 'dodecahedron', 'I': 'icosahedron', 'C': 'cube', 'T': 'tetrahedron', 'O': 'octahedron'}
        DIH = {'D': 'π − arccos(1/√5)', 'I': 'π − arccos(√5/3)', 'C': 'π/2', 'T': 'arccos(1/3)', 'O': 'π − arccos(1/3)'}
        Cp.figure('fig1.png', 'The five Platonic solids and their dihedral angles',
                  'The exact sets of the Lean entry (dhSet, ihSet, cuSet, teSet, ocSet) · only the cube\'s angle is a rational multiple of π',
                  [(sh_('fig1', q), NAME[d['k']], f"{DIH[d['k']]} ≈ {d['deg']:.2f}°") for q, d in enumerate(meta['fig1'])],
                  [(COL[d['k']], NAME[d['k']]) for d in meta['fig1']], cell=380)
        done('fig1.png', 'fig1-five.jpg', 'PREVIEW-aristotle-fig1-five.png')
        m = meta['fig2']
        Cp.figure('fig2.png', 'Round one edge the angles must add up to 2π',
                  'Seen along the common edge · gaps shaded',
                  [[(sh_('fig2', 0), 'five tetrahedra', f"gap 2π − 5 arccos(1/3) ≈ {m[0]['gap_deg']:.2f}°"),
                    (sh_('fig2', 2), 'three octahedra', f"gap 3 arccos(1/3) − π ≈ {m[1]['gap_deg']:.2f}°"),
                    (sh_('fig2', 4), 'tetrahedron, octahedron, ×2', 'closed exactly: 2π')]],
                  [(COL['T'], 'tetrahedron'), (COL['O'], 'octahedron'), (TEAL, 'the gap')], cell=520)
        done('fig2.png', 'fig2-edge-rings.jpg', 'PREVIEW-aristotle-fig2-edge-rings.png')
        print('FINAL ok')
