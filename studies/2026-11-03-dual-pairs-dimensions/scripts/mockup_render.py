"""Mock-up renders for the proposed "Dual-Pair Cycles" world (Polyhedraverse, beside Golden Cut in the 3D+ wizard). PROPOSAL ONLY:
nothing here is in the app. DICTO approves by looking (house rule: picture first).
Geometry is exact, from this study's dp_lib (S(mu) = P cap mu P*, H(mu) = conv(P cup mu P*), OG = Q(mu_TI, phi^2) = H(mu_TI) cap
phi^2 D*, the polar Dharma cycle of s4, the rectified tesseractic slice of s7 A); every mu is computed exactly in K = Q(sqrt2, sqrt5)
and checked against the s1 / s4 data. Floats are used only to draw.
Look (house protocols): solid faces, crisp edges 2 px (>= 1.5), app dark background (#05050a), pair colours (P green = the
Polyhedraverse piece colour, P* violet), gold for golden stations, see-through crystal outer shells round a solid innermost station.
Outputs (transparent PNG, 2x device pixels) + mockup-data.json (stations, exact mu, gold flags) into <out dir>.
usage (compute-host): python3 mockup_render.py <out dir>
DICTO · dictospheres.com
"""
import os, sys, json, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from dp_lib import *          # noqa
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)

GREEN, VIOLET, GOLD, EDGE = '#5ee233', '#9a6cf0', '#d9a520', '#0b1220'
LIGHT = np.array([-0.40, 0.55, 0.73]); LIGHT /= np.linalg.norm(LIGHT)
EDGE_CSS = 2.0            # edge width in CSS px (render standard: >= 1.5)
SCALE = 2                 # device pixels per CSS px
DPI = 100


def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz


VIEW = rot(22, 33)


def fl3(V): return np.array([[float(x) for x in v] for v in V])


def shade(col, n, lo=0.42):
    c = np.array(matplotlib.colors.to_rgb(col)); k = lo + (1 - lo) * max(0.0, float(n @ LIGHT))
    return tuple(np.clip(c * k, 0, 1))


def faces(P, colour_of):
    """faces of conv(P) (floats, coplanar triangles merged), each (polygon, outward normal, colour)"""
    hl = ConvexHull(P); groups = {}
    for eq, sx in zip(np.round(hl.equations, 7), hl.simplices): groups.setdefault(tuple(eq), set()).update(sx)
    out = []
    for eq, g in groups.items():
        g = list(g); c = P[g].mean(0); n = np.array(eq[:3]); u = P[g[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        g.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u))
        out.append((P[g], n, colour_of(P[g], n)))
    return out


def by_family(Nf, Vf):
    """S(mu) faces: on a plane of P (normal along an n) -> green, on a plane of mu P* (along a v) -> violet"""
    Nu = Nf / np.linalg.norm(Nf, axis=1)[:, None]; Vu = Vf / np.linalg.norm(Vf, axis=1)[:, None]
    def f(Q, n):
        if np.max(Nu @ n) > 1 - 1e-6: return GREEN
        if np.max(Vu @ n) > 1 - 1e-6: return VIOLET
        return '#888888'
    return f


def front_back(F):
    fr, bk = [], []
    for P, n, col in F:
        (fr if (VIEW @ n)[2] > 1e-9 else bk).append((P, n, col))
    return fr, bk


def proj(P): return (P @ VIEW.T)


def canvas(w_css, h_css, lim, cx=0.0, cy=0.0):
    fig = plt.figure(figsize=(w_css * SCALE / DPI, h_css * SCALE / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis('off')
    asp = h_css / w_css
    ax.set_xlim(cx - lim, cx + lim); ax.set_ylim(cy - lim * asp, cy + lim * asp); ax.set_aspect('equal')
    return fig, ax


LW = EDGE_CSS * SCALE * 72 / DPI


def draw_solid(ax, F, z0=0, edge=EDGE):
    fr, _ = front_back(F)
    items = sorted(((proj(P)[:, 2].mean(), proj(P)[:, :2], shade(c, VIEW @ n)) for P, n, c in fr), key=lambda t: t[0])
    ax.add_collection(PolyCollection([t[1] for t in items], facecolors=[t[2] for t in items], edgecolors=edge, linewidths=LW,
                                     joinstyle='round', zorder=z0))


def draw_crystal(ax, F, part, alpha, ecol, z0, lw=None):
    """one half of a see-through shell: 'back' faces (drawn first, dimmer) or 'front' faces"""
    fr, bk = front_back(F)
    L = fr if part == 'front' else bk
    polys = [proj(P)[:, :2] for P, n, c in L]
    cols = [shade(c, VIEW @ n, 0.55) + (alpha if part == 'front' else alpha * 0.6,) for P, n, c in L]
    ec = matplotlib.colors.to_rgba(ecol, 0.85 if part == 'front' else 0.35)
    ax.add_collection(PolyCollection(polys, facecolors=cols, edgecolors=[ec], linewidths=(lw or LW) * (1 if part == 'front' else 0.75),
                                     zorder=z0))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), transparent=True); plt.close(fig); print('  wrote', name, flush=True)


def radius(P): return float(np.linalg.norm(P, axis=1).max())


def kfmt(x): return kstr(x).replace('1/2√5', '√5/2')


DATA_OUT = {'note': 'mock-up data for the Dual-Pair Cycles world proposal; exact mu from dp_lib; DICTO · dictospheres.com', 'pairs': {}}
pl = platonic()

# ------------------------------------------------------------------ the three sweeps (exact stations, checked against s1)
PAIRS = {'di': ('dodecahedron', 5, 3, 'icosahedron'), 'co': ('cube', 4, 3, 'octahedron'), 'tt': ('tetrahedron', 3, 3, 'tetrahedron')}
SHORT = {'di': ['Icosahedron', 'Lesser Golden Cut Icosahedron', 'Truncated icosahedron', 'Greater Golden Cut Icosahedron', 'Icosidodecahedron',
                'Greater Golden Cut Dodecahedron', 'Truncated dodecahedron', 'Lesser Golden Cut Dodecahedron', 'Dodecahedron'],
         'co': ['Octahedron', 'Unborn Axes', 'Truncated octahedron (TO)', 'Icosaxes', 'Cuboctahedron', 'Greater Golden Cut Cube',
                'Truncated cube', 'Lesser Golden Cut Cube', 'Cube'],
         'tt': ['Tetrahedron (polar)', 'Lesser Golden Cut Tetrahedron (polar)', 'Truncated tetrahedron (polar)',
                'Greater Golden Cut Tetrahedron (polar)', 'Octahedron', 'Greater Golden Cut Tetrahedron', 'Truncated tetrahedron',
                'Lesser Golden Cut Tetrahedron', 'Tetrahedron']}
TICK = {'di': ['I', 'LGCI', 'tI', 'GGCI', 'ID', 'GGCD', 'tD', 'LGCD', 'D'],
        'co': ['O', 'Unborn Axes', 'TO', 'Icosaxes', 'CO', 'GGC Cube', 'tC', 'LGC Cube', 'C'],
        'tt': ['T*', 'LGCT*', 'tT*', 'GGCT*', 'O', 'GGCT', 'tT', 'LGCT', 'T']}
GOLDEN = [False, True, False, True, False, True, False, True, False]
WRAP = {'co': {4: 'RD = H(2)', 2: 'tetrakis hexahedron'}, 'di': {4: 'RT = H(φ²)', 2: 'pentakis dodecahedron'}, 'tt': {4: 'cube = H(1)'}}
PR = {}
for key_, (pname, nP, nS, dname) in PAIRS.items():
    P = Pair(pname, pl[pname][0]); PR[key_] = P
    xg, xl = x_golden(nP); xgs, xls = x_golden(nS)
    mus = [P.mu_Ps(ZERO), P.mu_Ps(xls), P.mu_Ps(ONE / (C_N[nS] + 2)), P.mu_Ps(xgs), P.mu_P(K(Fr(1, 2))),
           P.mu_P(xg), P.mu_P(ONE / (C_N[nP] + 2)), P.mu_P(xl), P.mu_P(ZERO)]
    ref = json.load(open(os.path.join(DATA, f's1-sweep-{key_}.json')))['stages']
    assert all(abs(float(m) - r['mu']['float']) < 1e-12 and kstr(m) == r['mu']['exact'] for m, r in zip(mus, ref)), key_
    st = []
    for i, m in enumerate(mus):
        st.append({'name': SHORT[key_][i], 'tick': TICK[key_][i], 'mu': kstr(m), 'mu_float': float(m), 'golden': GOLDEN[i],
                   'nu_float': float(m / P.r2), 'wrap_name': WRAP.get(key_, {}).get(i)})
    DATA_OUT['pairs'][key_] = {'P': pname, 'Pstar': dname, 'r2': float(P.r2), 'R2': float(P.R2), 'stations': st}
    PR[key_ + '_mus'] = mus
print('stations exact and equal to s1 data (all three pairs)', flush=True)

# OG stations on the D·I line (exact, = s4 / s4c): Q(mu, phi^2) at mu_TI, sqrt5, (13 + 6 sqrt5)/11
Pdi = PR['di']; D = Pdi.V; rho2 = Pdi.rho2
assert rho2 == PHI * PHI


def Qog(mu):
    _, _, Pl = planes_of(Pdi.Hull(mu))
    return fast_vertices_H(Pl + [(v, rho2) for v in D])


muTI, muL, muG = PR['di_mus'][2], PR['di_mus'][1], PR['di_mus'][3]
OG, OGL = Qog(muTI), Qog(muL)
assert len(OG) == 102 and len(OGL) == 102
DATA_OUT['pairs']['di']['og_marks'] = [{'name': 'Lesser Golden OG', 'mu': kstr(muL), 'mu_float': float(muL)},
                                       {'name': 'OG', 'mu': kstr(muTI), 'mu_float': float(muTI)},
                                       {'name': 'Greater Golden OG', 'mu': kstr(muG), 'mu_float': float(muG)}]


def S_faces(key_, mu):
    P = PR[key_]; S = fl3(P.S(mu)); return faces(S, by_family(fl3(P.N), fl3(P.V))), S


# ------------------------------------------------------------------ fig 1, 2: C·O sweep at Icosaxes and at the Greater GCC
for name, mu in (('co-icosaxes', PR['co_mus'][3]), ('co-ggc-cube', PR['co_mus'][5])):
    F, S = S_faces('co', mu)
    fig, ax = canvas(760, 640, 1.95)          # frame on the cube end (R = sqrt3): the cut is seen inside a still frame
    draw_solid(ax, F); save(fig, f'r-{name}.png')
# fig 4: D·I sweep at the Lesser GCI (phone)
F, S = S_faces('di', muL)
fig, ax = canvas(380, 380, 1.95); draw_solid(ax, F); save(fig, 'r-di-lgci.png')

# ------------------------------------------------------------------ fig 3: polar Dharma cycle, nested (s4 stations, exact)
c = -6 + 3 * S5                                  # inner scale (s4: c = -6 + 3 sqrt5), closure phi^3: phi^3 c D = 3 D
assert PHI * PHI * PHI * c == K(3)
Nf, Vf = fl3(Pdi.N), fl3(Pdi.V)
fam = by_family(Nf, Vf)


def hull_col(Q, n):        # hull faces: neutral crystal tone
    return '#bcd7ff'


def og_col(Q, n):          # OG: the hexagons lie on phi^2 D* planes (icosahedron family, violet); kites gold (highlight)
    return VIOLET if len(Q) == 6 else GOLD


stations = [('D', fl3([vscale(c, v) for v in D]), lambda Q, n: GREEN),
            ('ID', fl3(Pdi.S(rho2)), fam),
            ('OG', fl3(OG), og_col),
            ('pentakis', fl3(Pdi.Hull(muTI)), hull_col),
            ('ico', fl3(Pdi.Hull(K(3))), hull_col),
            ('RT', fl3([vscale(K(3) / rho2, p) for p in Pdi.Hull(rho2)]), hull_col),
            ('3D', fl3([vscale(K(3), v) for v in D]), hull_col)]
Fs = [faces(P, col) for _, P, col in stations]
DATA_OUT['dharma'] = [{'station': s, 'R': radius(P)} for s, P, _ in stations]
# The film paused at OG (zoomed), (Dual Vision's standard: the current station solid, the stations outside it see-through crystal; the
# inner dodecahedron and the icosidodecahedron lie inside OG and are shown on the station strip).
fig, ax = canvas(720, 640, 2.45 * 720 / 640)      # zoomed on this turn (Dual Vision zooms into each turn); the closing 3D lies beyond the frame
z = 0
CUR = 2
shells = list(range(len(stations) - 2, CUR, -1))      # outermost first (RT .. pentakis); 3D = phi^3 c D is off frame
STYLE = {6: (0.06, '#9fb6d8'), 5: (0.08, '#b0c8ee'), 4: (0.09, '#c3d9fa'), 3: (0.10, '#d6e6ff')}
for i in shells:
    a, e = STYLE[i]; draw_crystal(ax, Fs[i], 'back', a, e, z, lw=LW * 0.75); z += 1
draw_solid(ax, Fs[CUR], z); z += 1
for i in reversed(shells):
    a, e = STYLE[i]; draw_crystal(ax, Fs[i], 'front', a, e, z, lw=LW * 0.75); z += 1
save(fig, 'r-di-dharma-nested.png')
# inset: Lesser Golden OG (solid), and OG (solid) for the same-size comparison
for nm, X in (('r-lesser-golden-og.png', OGL), ('r-og.png', OG)):
    fig, ax = canvas(260, 260, 2.6 * radius(fl3(X)) / 2.6 * 1.08)
    draw_solid(ax, faces(fl3(X), og_col)); save(fig, nm)

# ------------------------------------------------------------------ fig 5: rectified tesseractic honeycomb, slice x4 = h (s7 A)
# cell at 0: |x_i| <= 1, sum |x_i| <= 3 - |x4| -> slice tile S(3 - h) of the cube pair (C cap (3-h) O) at 2Z^3; 16-cells at
# (2Z+1)^4 -> octahedra of radius h at (2Z+1)^3 (h in [0, 1]).
Pco = PR['co']; muGcc = PR['co_mus'][5]; h = 3 - muGcc
DATA_OUT['slice'] = {'h': kstr(h), 'h_float': float(h), 'stations': [
    {'name': 'Cube (simple cubic)', 'h': 0.0, 'golden': False}, {'name': 'Lesser Golden Cut Cube + octahedra', 'h': float(3 - PR['co_mus'][7]), 'golden': True},
    {'name': 'Truncated cube + octahedra', 'h': float(3 - PR['co_mus'][6]), 'golden': False},
    {'name': 'Greater Golden Cut Cube + octahedra', 'h': float(h), 'golden': True},
    {'name': 'Cuboctahedron + octahedra', 'h': 1.0, 'golden': False}]}
tile = fl3(Pco.S(muGcc)); Ft = faces(tile, by_family(fl3(Pco.N), fl3(Pco.V)))
octf = fl3(Pco.N) * float(h); Fo = faces(octf, lambda Q, n: VIOLET)
gap = 1.10                                             # pull-apart (house standard for nested / packed builds)
items = []
cells = [np.array(p, float) for p in itertools.product((0, 2), repeat=3)]
octs = [np.array(p, float) for p in itertools.product((-1, 1, 3), repeat=3)]
octs = [o for o in octs if sum(1 for k in o if k == 1) >= 2]   # the shared corners inside the 2x2x2 block and on its faces
for cc in cells: items.append((cc * gap, Ft))
for o in octs: items.append((o * gap, Fo))
cen = np.array([1, 1, 1]) * gap
polys = []
for off, F in items:
    for P, n, col in F:
        if (VIEW @ n)[2] <= 1e-9: continue
        Q = proj(P + off - cen); polys.append((Q[:, 2].mean() + 0.0 * 0, Q[:, :2], shade(col, VIEW @ n)))
polys.sort(key=lambda t: t[0])
fig, ax = canvas(640, 560, 4.0)
ax.add_collection(PolyCollection([p[1] for p in polys], facecolors=[p[2] for p in polys], edgecolors=EDGE, linewidths=LW))
save(fig, 'r-co-slice.png')

# small 2D diagram: the plane (t (1,1,1)/sqrt3, x4) through the 4D honeycomb; rectified tesseracts -> octagons, 16-cells -> diamonds
s3 = 3 ** .5
fig = plt.figure(figsize=(340 * SCALE / DPI, 250 * SCALE / DPI), dpi=DPI); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96]); ax.axis('off')
oct8 = np.array([[s3, 0], [2 / s3, 1], [-2 / s3, 1], [-s3, 0], [-2 / s3, -1], [2 / s3, -1]])
oct8 = np.array([[s3, 0], [2 / s3, 1], [-2 / s3, 1], [-s3, 0], [-2 / s3, -1], [2 / s3, -1]])
dia = np.array([[1 / s3, 0], [0, 1], [-1 / s3, 0], [0, -1]])
A, B = [], []
for i in range(-2, 3):
    for j in range(-2, 3):
        A.append(oct8 + [2 * s3 * i, 2 * j]); B.append(dia + [2 * s3 * i + s3, 2 * j + 1])
ax.add_collection(PolyCollection(A, facecolors=matplotlib.colors.to_rgba(GREEN, 0.22), edgecolors=GREEN, linewidths=LW * 0.6))
ax.add_collection(PolyCollection(B, facecolors=matplotlib.colors.to_rgba(VIOLET, 0.45), edgecolors=VIOLET, linewidths=LW * 0.6))
hf = float(h)
ax.plot([-2.2 * s3, 2.2 * s3], [hf, hf], color=GOLD, lw=LW * 2.0)
ax.text(-2.15 * s3, hf + 0.08, 'h', color=GOLD, fontsize=26, weight='bold', va='bottom')
ax.text(2.1 * s3, 2.45, 'x₄', color='#d8ffcc', fontsize=24, ha='right', va='top')
ax.text(2.1 * s3, -1.5, 't', color='#d8ffcc', fontsize=24, ha='right', va='bottom')
ax.set_xlim(-2.2 * s3, 2.2 * s3); ax.set_ylim(-1.6, 2.6); ax.set_aspect('equal')
save(fig, 'r-slice-diagram.png')

# ------------------------------------------------------------------ fig 6: overview filmstrips (white, for paper #91 too)
LOGO = os.path.expanduser('~/work/dicto-logo.png')
fig = plt.figure(figsize=(10.0, 6.9), dpi=200)
plt.rcParams['font.family'] = 'DejaVu Sans'
fig.text(0.012, 0.965, 'Dual-pair sweeps  S(μ) = P ∩ μP*  (station films)', fontsize=11, weight='bold', color='#1d1d24')
fig.text(0.012, 0.938, 'faces on P planes green, on μP* planes violet; golden stations framed gold; exact μ under each '
         '(dual end left, P end right)', fontsize=7.6, color='#444')
ROWS = [('di', 'D·I  dodecahedron – icosahedron'), ('co', 'C·O  cube – octahedron'), ('tt', 'T  tetrahedron – its polar')]
for r, (k, title) in enumerate(ROWS):
    y0 = 0.637 - r * 0.293
    fig.text(0.012, y0 + 0.262, title, fontsize=9, weight='bold', color='#1d1d24')
    P = PR[k]
    for i, m in enumerate(PR[k + '_mus']):
        ax = fig.add_axes([0.008 + i * 0.1096, y0 + 0.085, 0.104, 0.17]); ax.axis('off')
        if i == 0: S = fl3(P.N) * float(m)
        elif i == 8: S = fl3(P.V)
        else: S = fl3(P.S(m))
        S = S / radius(S)
        F = faces(S, by_family(fl3(P.N), fl3(P.V)))
        Vw = rot(30, 14) if k == 'tt' else VIEW
        fr = [(Q, n, col) for Q, n, col in F if (Vw @ n)[2] > 1e-9]
        its = sorted((((Q @ Vw.T)[:, 2].mean(), (Q @ Vw.T)[:, :2], shade(col, Vw @ n)) for Q, n, col in fr), key=lambda t: t[0])
        ax.add_collection(PolyCollection([t[1] for t in its], facecolors=[t[2] for t in its], edgecolors=EDGE, linewidths=0.6))
        ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.12, 1.12); ax.set_aspect('equal')
        st = DATA_OUT['pairs'][k]['stations'][i]
        if st['golden']:
            ax.add_patch(matplotlib.patches.FancyBboxPatch((-1.08, -1.08), 2.16, 2.16, boxstyle='round,pad=0,rounding_size=0.18',
                                                           fill=False, ec=GOLD, lw=1.6, transform=ax.transData))
        nm = st['name'].replace('Golden Cut', 'GC').replace(' (polar)', '*').replace('Truncated', 'trunc.')
        nm = nm.replace('Icosidodecahedron', 'Icosidodeca-\nhedron').replace(' (TO)', '\n(TO)')
        if len(nm) > 15 and '\n' not in nm: nm = nm.replace(' ', '\n', 1)
        fig.text(0.008 + i * 0.1096 + 0.052, y0 + 0.082, nm, ha='center', va='top', fontsize=6.3,
                 color='#8a6a00' if st['golden'] else '#1d1d24', weight='bold' if st['golden'] else 'normal')
        ms = st['mu'].replace('1/2√5', '√5/2').replace('1/2√2', '√2/2').replace('1/2√10', '√10/2')
        fig.text(0.008 + i * 0.1096 + 0.052, y0 + 0.036, f'μ = {ms}\n≈ {st["mu_float"]:.4f}', ha='center', va='top', fontsize=5.4,
                 color='#8a6a00' if st['golden'] else '#555')
fig.text(0.012, 0.006, 'C·O: TO = S(3/2); RD = H(2) (wrap side at the cuboctahedron).  D·I: OG = Q(μ_TI, φ²) at the truncated icosahedron μ; '
         'Lesser / Greater Golden OG at the Lesser / Greater GCI μ.\nT: * = the polar tetrahedron.  GC = Golden Cut.  '
         'Icosaxes is the one golden station whose ν = μ/r² is a power of φ (ν = φ).', fontsize=6.6, color='#333', linespacing=1.4)
if os.path.exists(LOGO):
    a = fig.add_axes([0.925, 0.925, 0.06, 0.06 * 10 / 6.9]); a.imshow(plt.imread(LOGO)); a.axis('off')
fig.text(0.988, 0.905, 'DICTO · dictospheres.com', ha='right', fontsize=6.4, color='#8a6a00')
fig.savefig(os.path.join(OUT, 'fig6-filmstrips.png'), facecolor='white'); plt.close(fig); print('  wrote fig6-filmstrips.png')

json.dump(DATA_OUT, open(os.path.join(OUT, 'mockup-data.json'), 'w'), indent=1)
print('done', flush=True)
