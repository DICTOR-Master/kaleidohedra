"""Figures for the Golayantra study.
 classical-golayantra.png   Bhaskara I's gola-yantra (reconstruction after Lu 2015; latitude of Ujjayini 23.2 deg chosen here)
 dicto-golayantra.png       the DICTO Yantra (GF1) as 27 full rings, rho = 60 deg
 classical-vs-dicto.png     side by side
 antipol-golayantra.png     ring form | polar form (beads and threads) | the nine polar triangles round the core cap
Orthographic views; back halves of rings drawn faint.  Every figure carries the DICTO mark."""
import json, math, os, itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data'); FIG = os.path.join(HERE, '..', 'figures')
os.makedirs(FIG, exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
BG = '#0b0c12'; FG = '#e6e6ea'; MARK = '#e8c25a'
D = json.load(open(os.path.join(DATA, 'rings.json')))
G = json.load(open(os.path.join(DATA, 'golden_family.json')))['GF1']
f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(G['b']), f(G['w']), f(G['apex'])
UP = {i for i in range(1, 10) if a[i] < b[i]}
GOLD = '#e8c25a'; BLUE = '#3a70cd'

def view_matrix(az, el):
    """rows: screen right, screen up, direction to the viewer (depth >= 0 is the near side)"""
    az, el = math.radians(az), math.radians(min(el, 89.99))
    Vd = np.array([math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)])
    r = np.cross([0, 0, 1.0], Vd); r /= np.linalg.norm(r); up = np.cross(Vd, r)
    return np.array([r, up, Vd])

def draw_curve(ax, M, pts, color, lw, front_alpha=1.0, back_alpha=0.18, ls='-', z=2, back=True):
    q = pts @ M.T
    segs = np.stack([q[:-1, :2], q[1:, :2]], axis=1); dep = (q[:-1, 2] + q[1:, 2]) / 2
    fr = dep >= 0
    if fr.any(): ax.add_collection(LineCollection(segs[fr], colors=color, linewidths=lw, alpha=front_alpha, linestyles=ls, zorder=z + 1, capstyle='round'))
    if back and (~fr).any(): ax.add_collection(LineCollection(segs[~fr], colors=color, linewidths=lw * 0.7, alpha=back_alpha, linestyles=ls, zorder=z - 1))

def great_circle(n, r=1.0, k=361):
    n = np.asarray(n, float); n /= np.linalg.norm(n)
    e0 = np.cross(n, [0.3, 0.5, 0.81]); e0 /= np.linalg.norm(e0); e1 = np.cross(n, e0)
    t = np.linspace(0, 2 * math.pi, k)[:, None]
    return r * (np.cos(t) * e0 + np.sin(t) * e1)

def small_circle(c, ang, r=1.0, k=361):
    c = np.asarray(c, float); c /= np.linalg.norm(c)
    e0 = np.cross(c, [0.3, 0.5, 0.81]); e0 /= np.linalg.norm(e0); e1 = np.cross(c, e0)
    t = np.linspace(0, 2 * math.pi, k)[:, None]
    return r * (math.cos(ang) * c + math.sin(ang) * (np.cos(t) * e0 + np.sin(t) * e1))

def arc(p, q, r=1.0, k=80):
    p, q = np.asarray(p, float), np.asarray(q, float)
    om = math.acos(np.clip(np.dot(p, q), -1, 1)); t = np.linspace(0, 1, k)[:, None]
    return r * (np.sin((1 - t) * om) * p + np.sin(t * om) * q) / math.sin(om)

def frame(ax, title, lim=1.32, low=None):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim if low is None else low, lim); ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(BG)
    ax.text(0, lim * 0.97, title, color=FG, ha='center', va='top', fontsize=13)

def label(ax, M, p, text, dx, dy, color=FG, fs=8.5):
    q = np.asarray(p) @ M.T
    ax.annotate(text, xy=(q[0], q[1]), xytext=(q[0] + dx, q[1] + dy), color=color, fontsize=fs,
                arrowprops=dict(arrowstyle='-', color=color, lw=0.6, alpha=0.8), zorder=20,
                ha='left' if dx >= 0 else 'right', va='center')

def legend(ax, items, x=-1.42, y=-1.3, fs=8.6):
    for k, (t, c) in enumerate(items):
        ax.text(x, y - k * 0.068, t, color=c, fontsize=fs, va='top', ha='left', zorder=30)

def mark(fig):
    fig.text(0.985, 0.012, 'DICTO · dictospheres.com', color=MARK, ha='right', va='bottom', fontsize=11)

# ---------------- classical gola-yantra (Bhaskara I) ----------------
def classical(ax, az=-62, el=14, labels=True):
    M = view_matrix(az, el)
    lat = math.radians(23.2)                     # Ujjayini (choice for the drawing; Bhaskara I sets any local latitude, para 18)
    # horizon frame: x east, y north, z zenith
    P = np.array([0, math.cos(lat), math.sin(lat)])          # north celestial pole
    E = np.array([1.0, 0, 0])
    Rk = 1.16                                               # khagola (outer shell) radius; bhagola radius 1
    col_k = '#9aa0ad'
    # outer shell khagola: kha-kakshya (meridian, N-S), sama-mandala (prime vertical), kshitija (horizon), unmandala (six o'clock)
    rings_k = [('kha-kakṣyā (meridian)', np.array([1.0, 0, 0])), ('sama-maṇḍala (prime vertical)', np.array([0, 1.0, 0])),
               ('kṣitija (horizon)', np.array([0, 0, 1.0])), ('unmaṇḍala (six o’clock circle)', np.cross(P, E))]
    for nm, n in rings_k: draw_curve(ax, M, great_circle(n, Rk), col_k, 1.6, back_alpha=0.22)
    # inner shell bhagola, turned by an hour angle H about the pole axis
    H = math.radians(35)
    eq_e = math.cos(H) * E + math.sin(H) * np.cross(P, E)       # vernal equinox direction (on the equator)
    s_dir = np.cross(P, eq_e)                                   # solstitial direction on the equator
    eps = math.radians(24)
    n_ecl = math.cos(eps) * P - math.sin(eps) * s_dir           # ecliptic normal: tilted 24 deg towards s
    col_eq, col_col, col_ec, col_moon, col_day = '#4f8fe8', '#b07a4a', '#e8c25a', '#d8d8e0', '#4fb3a0'
    draw_curve(ax, M, great_circle(P), col_eq, 2.2, back_alpha=0.25)                       # vishuvat (equator)
    draw_curve(ax, M, great_circle(s_dir), col_col, 1.7, back_alpha=0.25)                  # ring through poles and equinoxes
    draw_curve(ax, M, great_circle(eq_e), col_col, 1.7, back_alpha=0.25)                   # ring through poles and solstices
    draw_curve(ax, M, great_circle(n_ecl), col_ec, 2.4, back_alpha=0.28)                   # apamandala (ecliptic)
    # moon's orbit: 4.5 deg to the ecliptic, node at ecliptic longitude 60 deg (movable)
    lam = math.radians(60); ecl_e1 = np.cross(n_ecl, eq_e)
    node = math.cos(lam) * eq_e + math.sin(lam) * ecl_e1; node /= np.linalg.norm(node)
    i_m = math.radians(4.5); perp = np.cross(n_ecl, node)
    n_moon = math.cos(i_m) * n_ecl + math.sin(i_m) * perp
    draw_curve(ax, M, great_circle(n_moon), col_moon, 1.2, back_alpha=0.2, ls=(0, (4, 2)))
    # day circles at the declinations of the ends of Aries, Taurus, Gemini (and south)
    decs = [math.asin(math.sin(eps) * math.sin(math.radians(L))) for L in (30, 60, 90)]
    for dd in decs:
        for sg in (1, -1): draw_curve(ax, M, small_circle(P, math.pi / 2 - sg * dd), col_day, 0.9, back_alpha=0.15)
    # axis rod and earth
    rod = np.array([-1.32 * P, 1.32 * P]); draw_curve(ax, M, np.linspace(rod[0], rod[1], 50), '#c9c9cf', 2.6, back_alpha=0.9, z=6)
    q0 = np.zeros(3) @ M.T; ax.add_patch(plt.Circle((q0[0], q0[1]), 0.085, color='#6b8f3a', zorder=8))
    if labels:
        legend(ax, [('Outer shell, khagola (fixed):', FG), ('  kha-kakṣyā (meridian), sama-maṇḍala (prime vertical),', col_k),
                    ('  kṣitija (horizon), unmaṇḍala (six o’clock ring)', col_k),
                    ('Inner shell, bhagola (turns on the rod):', FG), ('  viṣuvat (equator, 60 ghaṭikās)', col_eq),
                    ('  two rings through the poles (S–N ring and girdle)', col_col), ('  apamaṇḍala (ecliptic, 24°, fixed at E and W)', col_ec),
                    ('  vimaṇḍala (moon’s orbit, 4½°, movable)', col_moon), ('  svāhorātra (6 day circles, movable)', col_day),
                    ('Iron rod; clay earth at the centre', '#c9c9cf')])
    return M

# ---------------- DICTO golayantra ----------------
RHO = math.pi / 3; sc = 2 * math.tan(RHO)
def sph(x, d): q = np.array([x * sc, (0.5 - d) * sc, 1.0]); return q / np.linalg.norm(q)
R60 = D['by_rho']['60']
N = {k: np.array([float(c) for c in v]) for k, v in R60['normals'].items()}
SIDES = {}
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0, a[i])
    SIDES[f'B{i}'] = (L, R); SIDES[f'R{i}'] = (R, A); SIDES[f'L{i}'] = (L, A)
JT = {'marma': '#ff5a5a', 'corner touch': '#ff9d3a', 'apex': '#c084ff', 'base pole': '#ffffff'}
def jcolor(t):
    for k, c in JT.items():
        if t.startswith(k): return c
    return '#00ff00'

def dicto(ax, az=0, el=62, labels=True, faint=0.45):
    M = view_matrix(az, el)
    for k, n in N.items():
        i = int(k[1]); c = GOLD if i in UP else BLUE
        draw_curve(ax, M, great_circle(n), c, 0.8, front_alpha=faint, back_alpha=0.12)
    for k, (p, q) in SIDES.items():
        i = int(k[1]); c = GOLD if i in UP else BLUE
        draw_curve(ax, M, np.array([sph(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t) for t in np.linspace(0, 1, 60)]), c, 2.2, back=False, z=5)
    draw_curve(ax, M, small_circle([0, 0, 1], RHO), '#f2f2f5', 1.4, back_alpha=0.15, z=4)
    draw_curve(ax, M, great_circle([1, 0, 0]), '#8ad0c8', 1.1, front_alpha=0.9, back_alpha=0.2, ls=(0, (5, 3)))   # equator = symmetry ring
    draw_curve(ax, M, great_circle([0, 0, 1]), '#9aa0ad', 1.1, front_alpha=0.9, back_alpha=0.2, ls=(0, (2, 2)))   # horizon = line at infinity
    for s_ in (1, -1): draw_curve(ax, M, np.linspace([s_ * 1.0, 0, 0], [s_ * 1.3, 0, 0], 10), '#c9c9cf', 2.6, back_alpha=0.9, z=6)
    draw_curve(ax, M, np.linspace([-1.0, 0, 0], [1.0, 0, 0], 40), '#c9c9cf', 1.0, front_alpha=0.25, back_alpha=0.25, z=0)
    for J in R60['joints']:
        v = np.array([float(c) for c in J['xyz']])
        for s in (1, -1):
            q = (s * v) @ M.T
            ax.scatter([q[0]], [q[1]], s=(26 if J['type'].startswith('base') else 9) if q[2] >= 0 else 4, color=jcolor(J['type']),
                       alpha=1 if q[2] >= 0 else 0.3, zorder=9 if q[2] >= 0 else 1, edgecolors='none')
    if labels:
        legend(ax, [('27 rings (great circles, radius = sphere radius)', FG), ('  gold: rings of t6–t9 (pointing up), blue: t1–t5', GOLD),
                    ('  bold arcs: the yantra on its cap (ρ = 60°)', GOLD), ('Rod: polar axis ±X, where all nine base rings meet', '#c9c9cf'),
                    ('Dashed teal: equator ring x = 0 (symmetry line); apexes on it', '#8ad0c8'),
                    ('Dotted grey: horizon ring (line at infinity), a tenth meridian', '#9aa0ad'), ('White: yantra circle (small circle)', '#f2f2f5'),
                    ('● marma joints (18)', JT['marma']), ('● corner-touch joints (6)', JT['corner touch']),
                    ('● apex-on-base joints (7, on the equator ring)', JT['apex']), ('● base pole (9 rings)', JT['base pole']),
                    ('faint dots: antipodal joints behind', FG)])
    return M

def save(fig, name):
    mark(fig); fig.savefig(os.path.join(FIG, name), dpi=160, facecolor=BG); plt.close(fig)

fig = plt.figure(figsize=(9, 10.9), facecolor=BG); ax = fig.add_axes([0, 0, 1, 1]); frame(ax, 'Gola-yantra of Bhāskara I (629 CE), reconstructed', lim=1.45, low=-2.25)
classical(ax)
ax.text(-1.42, -2.2, 'Inner shell (bhagola) turns on the iron rod: equator, two rings through the poles, ecliptic, moon’s orbit, day circles.\n'
        'Outer shell (khagola) fixed: meridian, prime vertical, horizon, six o’clock ring. Drawn for latitude 23.2° (Ujjayinī).\n'
        'Ring pattern after Bhāskara I’s text (Shukla 1976 ed., tr. Lu 2015); this drawing is a reconstruction.', color=FG, fontsize=7.6, va='bottom')
save(fig, 'classical-golayantra.png')

fig = plt.figure(figsize=(9, 10.9), facecolor=BG); ax = fig.add_axes([0, 0, 1, 1]); frame(ax, 'DICTO Golayantra: the DICTO Yantra as 27 rings', lim=1.45, low=-2.25)
dicto(ax)
save(fig, 'dicto-golayantra.png')

fig = plt.figure(figsize=(16, 9.7), facecolor=BG)
a1 = fig.add_axes([0, 0, 0.5, 1]); frame(a1, 'Classical gola-yantra (Bhāskara I)', lim=1.45, low=-2.25); classical(a1, labels=True)
a2 = fig.add_axes([0.5, 0, 0.5, 1]); frame(a2, 'DICTO Golayantra', lim=1.45, low=-2.25); dicto(a2, labels=True)
save(fig, 'classical-vs-dicto.png')

# ---------------- antipol: ring form | polar form ----------------
P3 = D['polar']['60']
fig = plt.figure(figsize=(21, 7.6), facecolor=BG)
a1 = fig.add_axes([0, 0, 1 / 3, 1]); frame(a1, 'Ring form: 27 rings, 32 joints'); dicto(a1, labels=False)
a2 = fig.add_axes([1 / 3, 0, 1 / 3, 1]); frame(a2, 'Polar form: 54 beads on 32 threads')
M = view_matrix(0, 62)
for J in R60['joints']:   # thread = polar great circle of each joint
    v = np.array([float(c) for c in J['xyz']])
    draw_curve(a2, M, great_circle(v), jcolor(J['type']), 1.0 if not J['type'].startswith('base') else 1.8, front_alpha=0.75, back_alpha=0.12)
for k, n in N.items():
    i = int(k[1]); c = GOLD if i in UP else BLUE
    for s in (1, -1):
        q = (s * n) @ M.T
        a2.scatter([q[0]], [q[1]], s=30 if q[2] >= 0 else 10, color=c, alpha=1 if q[2] >= 0 else 0.35, zorder=9, edgecolors='white' if q[2] >= 0 else 'none', linewidths=0.4)
draw_curve(a2, M, small_circle([0, 0, 1], math.pi / 2 - RHO), '#f2f2f5', 1.2, back_alpha=0.15)
a2.text(-1.3, -1.25, 'bead = pole of a ring (two per ring); thread = polar of a joint.\nWhite thread: the equator x = 0 carries all 18 base beads (polar of the base pole).\n'
        'Each marma thread carries 3 bead pairs: all 18 alignments exact. White circle: core cap 90° − ρ = 30°.', color=FG, fontsize=7.8, va='bottom')
a3 = fig.add_axes([2 / 3, 0, 1 / 3, 1]); frame(a3, 'Nine polar triangles round the core cap')
M3 = view_matrix(0, 90)   # looking down the pole Z of the cap
for t in P3['polar_triangles']:
    V = {k: np.array([float(c) for c in v]) for k, v in t['polar_vertices'].items()}
    c = GOLD if t['up'] else BLUE
    for p_, q_ in (('A', 'L'), ('L', 'R'), ('R', 'A')): draw_curve(a3, M3, arc(V[p_], V[q_]), c, 1.6 if t['t'] in (3, 7) else 1.0, back_alpha=0.15)
draw_curve(a3, M3, small_circle([0, 0, 1], math.pi / 2 - RHO), '#f2f2f5', 1.6, back_alpha=0.15)
draw_curve(a3, M3, great_circle([0, 0, 1]), '#9aa0ad', 0.8, back_alpha=0.1, ls=(0, (2, 2)))
a3.text(-1.3, -1.25, 'Polar triangle of t_i: sides 180° − angles of t_i. All nine contain the core cap\n(dual of: all nine lie in the yantra cap). t3, t7 (bold) circumscribe it, t1, t9 touch it twice\n'
        '(dual of: corners on the circle). View from above the cap; dashed: horizon ring.', color=FG, fontsize=7.8, va='bottom')
save(fig, 'antipol-golayantra.png')

ok = all(os.path.getsize(os.path.join(FIG, n)) > 50000 for n in ('classical-golayantra.png', 'dicto-golayantra.png', 'classical-vs-dicto.png', 'antipol-golayantra.png'))
print('FINAL ok' if ok else 'FINAL FAIL: a figure is missing or empty')
