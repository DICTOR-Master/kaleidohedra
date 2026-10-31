# Figures for Splash Rules II, approximants (dicto-big-brother): ~/geom/bin/python figs.py ../out ../fig
# Floats only for drawing; every plotted value is an exact rational (or Q(sqrt2), Q(sqrt5) number) from sturm.py / abfam.py.
import sys, os, json, math, itertools
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Polygon
from zono import int_kernel, zonogon

IN, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LOGO = plt.imread(os.path.expanduser('~/kres-tmp/dicto-logo.png'))
GOLD, INK, GREY, BLUE, RED, GREEN = '#b8962e', '#222222', '#9a9a9a', '#2f5d8a', '#a8402e', '#4f7d3a'
plt.rcParams.update({'font.size': 8, 'axes.linewidth': 1.0, 'font.family': 'DejaVu Sans', 'axes.edgecolor': '#555555'})
def mark(fig):
    fig.add_artist(AnnotationBbox(OffsetImage(LOGO, zoom=24 / LOGO.shape[0]), (0.995, 0.005), xycoords='figure fraction', box_alignment=(1, 0), frameon=False))
    fig.text(0.955, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=6.5, color='#8a6d1c')
def style(ax):
    ax.grid(True, color='#e6e6e6', linewidth=0.6, zorder=0); ax.tick_params(length=3, width=0.8)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
F = lambda s: float(Fr(s))
S = json.load(open(os.path.join(IN, 'sturm.json'))); A = json.load(open(os.path.join(IN, 'abfam.json')))
astar = (3 - math.sqrt(5)) / 2

fig, axs = plt.subplots(2, 2, figsize=(7.4, 6.4), dpi=220)
# (a) the window-2 plane: all primitive necklaces vs the approximants
a = axs[0, 0]; style(a)
pl = S['plane']
a.fill_between([0, 0.5, 1], [0, 0, 1], [0, 0.5, 1], color='#f4efe0', zorder=1)
a.scatter([F(h) for h, p, b in pl if not b], [F(p) for h, p, b in pl if not b], s=7, color=GREY, alpha=0.5, linewidths=0, label='all periodic words up to 12 letters (700)', zorder=2)
a.scatter([F(h) for h, p, b in pl if b], [F(p) for h, p, b in pl if b], s=16, marker='D', color=GOLD, edgecolors='white', linewidths=0.5, label='approximants (balanced words, 47)', zorder=3)
a.plot([0, 0.5, 1], [0, 0, 1], color=INK, lw=1.0, zorder=2)
a.scatter([astar], [0], s=70, marker='*', color=RED, zorder=5, label='Fibonacci chain, a = 1/φ²')
a.set_xlabel('share a of S tiles'); a.set_ylabel('share of SS pairs (the second number)')
a.set_title('(a) approximants on the edge SS = max(0, 2a − 1)', fontsize=8.5, loc='left'); a.legend(fontsize=6, frameon=False, loc='upper left')
# (b) window 3: every triple frequency, all approximants q <= 60, piecewise lines
a = axs[0, 1]; style(a)
ap = S['approximants']; xs = sorted(ap, key=F)
cols = {'LLL': BLUE, 'LLS': GOLD, 'LSL': INK, 'SLL': GOLD, 'LSS': GREEN, 'SLS': RED, 'SSL': GREEN, 'SSS': '#7a5aa6'}
mk = {'LLL': 'o', 'LLS': '^', 'LSL': 's', 'SLL': 'v', 'LSS': '^', 'SLS': 'D', 'SSL': 'v', 'SSS': 'o'}
for w in ['LLL', 'LLS', 'LSL', 'LSS', 'SLS', 'SSS']:
    a.scatter([F(x) for x in xs], [F(ap[x]['3'].get(w, '0')) for x in xs], s=5, marker=mk[w], color=cols[w], linewidths=0, label=w + (' (= SLL)' if w == 'LLS' else ' (= SSL)' if w == 'LSS' else ''), zorder=3)
for k in (1 / 3, 1 / 2, 2 / 3): a.axvline(k, color='#cccccc', lw=0.7, zorder=1)
a.axvline(astar, color=RED, lw=0.9, ls='--', zorder=2)
a.text(astar + 0.01, 0.93, '1/φ²', color=RED, fontsize=7)
a.set_xlabel('share a of S tiles (approximant p/q, q ≤ 60)'); a.set_ylabel('frequency of the triple')
a.set_title('(b) triples: lines between 1/3, 1/2, 2/3', fontsize=8.5, loc='left'); a.legend(fontsize=5.6, frameon=False, loc='upper right', ncol=2)
# (c) AB square approximants in the chamber: deviation from the limit against the deviation of the square share
a = axs[1, 0]; style(a)
rows = A['rows']
NAME = {'00100101': 'F (3)', '00101101': 'E (4)', '01011011': 'D (5)', '01101111': 'C (6)', '01111111': 'B (7)', '11111111': 'A (8)', '01011111': 'defect (6)'}
CC = {'00100101': BLUE, '00101101': GOLD, '01011011': INK, '01101111': GREEN, '01111111': '#7a5aa6', '11111111': RED, '01011111': '#e07b39'}
MK = {'00100101': 'o', '00101101': '^', '01011011': 's', '01101111': 'D', '01111111': 'v', '11111111': 'P', '01011111': 'X'}
qs = lambda r: r['Q'] / (r['R'] + r['Q'])
inside = lambda r: Fr(2, 3) <= Fr(r['t']) <= Fr(3, 4)
law = {'00100101': (0, 1), '00101101': (2, -2), '01011011': (-4, 6), '01101111': (10, -14), '01111111': (-12, 17), '11111111': (5, -7)}
qst = math.sqrt(2) - 1
fst = {c: x * (1 - qst) + y * qst for c, (x, y) in law.items()}
ins = [r for r in rows if inside(r)]
for c, (x, y) in law.items():
    a.scatter([1e3 * (qs(r) - qst) for r in ins], [1e3 * (F(r['stars'].get(c, '0')) / r['N'] - fst[c]) for r in ins], s=14, marker=MK[c], color=CC[c], linewidths=0, label=f'{NAME[c]}: slope {y - x}', zorder=3)
    a.plot([0, 0.45], [0, 1e3 * (y - x) * 0.45e-3], color=CC[c], lw=0.8, zorder=2)
a.set_xlim(-0.02, 0.45)
a.set_xlabel('q − (√2 − 1), in thousandths (q = share of squares)'); a.set_ylabel('frequency − AB value, in thousandths')
a.set_title('(c) Ammann–Beenker, 42 approximants: lines in q', fontsize=8.5, loc='left'); a.legend(fontsize=5.8, frameon=False, loc='lower left', ncol=2)
# (d) the defect star: zero on the chamber, a square outside
a = axs[1, 1]; style(a)
ts = [F(r['t']) for r in rows]
a.scatter(ts, [F(r['stars'].get('01011111', '0')) / r['N'] for r in rows], s=9, marker='X', color='#e07b39', linewidths=0, zorder=3, label='defect stars per vertex (246 approximants)')
tt = [i / 400 for i in range(200, 401)]
def xf(t):
    if t < 2 / 3: return 2 * (3 * t - 2) ** 2 / (1 + 4 * t + 2 * t * t)
    if t > 3 / 4: return (4 * t - 3) ** 2 / (1 + 4 * t + 2 * t * t)
    return 0.0
a.plot(tt, [xf(t) for t in tt], color=INK, lw=0.9, zorder=2, label='2(3t − 2)² or (4t − 3)², over 1 + 4t + 2t²')
a.axvspan(2 / 3, 3 / 4, color='#f4efe0', zorder=1); a.axvline(1 / math.sqrt(2), color=RED, lw=0.9, ls='--')
a.text(0.672, 0.045, 'AB chamber\n2/3 ≤ t ≤ 3/4', fontsize=6.5, color='#8a6d1c')
a.set_xlabel('approximant parameter t (√2/2 replaced by t = a/b)'); a.set_ylabel('defect stars per vertex')
a.set_title('(d) the defect: zero inside, a square outside', fontsize=8.5, loc='left'); a.legend(fontsize=6, frameon=False, loc='upper center')
fig.tight_layout(rect=(0, 0.03, 1, 1)); mark(fig)
fig.savefig(os.path.join(OUT, 'splash2-approximants.png')); plt.close(fig)

# ---- Figure 2: an approximant patch beside the quasicrystal (Ammann-Beenker), vertices coloured by star
s2 = math.sqrt(2) / 2
PH = [(1, 0), (s2, s2), (0, 1), (-s2, s2)]
IN_ = [(1, 0), (-s2, s2), (0, -1), (s2, s2)]
def tiling(select, M=7, rad=6.2):
    pts = {}
    for x in itertools.product(range(-M, M + 1), repeat=4):
        if select(x):
            p = (sum(x[k] * PH[k][0] for k in range(4)), sum(x[k] * PH[k][1] for k in range(4)))
            if p[0] ** 2 + p[1] ** 2 < (rad + 1.5) ** 2: pts[x] = p
    return pts
def inside(z, W):
    n = len(W)
    for i in range(n):
        a, b = W[i], W[(i + 1) % n]
        if (b[0] - a[0]) * (z[1] - a[1]) - (b[1] - a[1]) * (z[0] - a[0]) <= 0: return False
    return True
Wq = zonogon([(Fr(1), Fr(0)), (Fr(-1), Fr(1)), (Fr(0), Fr(-1)), (Fr(1), Fr(1))])  # placeholder (replaced below)
Wirr = [(float(p[0]), float(p[1])) for p in zonogon([(1.0, 0.0), (-s2, s2), (0.0, -1.0), (s2, s2)])]
gq = (0.1234567, 0.0456789)
sel_qc = lambda x: inside((sum(x[k] * IN_[k][0] for k in range(4)) - gq[0], sum(x[k] * IN_[k][1] for k in range(4)) - gq[1]), Wirr)
a_, b_ = 5, 7     # t = 5/7: the 239-vertex square approximant
N = int_kernel([[b_, a_, 0, -a_], [0, a_, b_, a_]])
gens = [(Fr(N[0][k]), Fr(N[1][k])) for k in range(4)]
Wr = zonogon(gens); gr = (Fr(1234567, 10 ** 7 + 19), Fr(456789, 10 ** 7 + 79))
sel_ap = lambda x: inside((sum(x[k] * N[0][k] for k in range(4)) - gr[0], sum(x[k] * N[1][k] for k in range(4)) - gr[1]), Wr)
STARC = CC
def star(x, pts):
    b = [tuple(x[i] + (1 if i == k else 0) for i in range(4)) in pts for k in range(4)] + [tuple(x[i] - (1 if i == k else 0) for i in range(4)) in pts for k in range(4)]
    best = None
    for r in range(8):
        for sg in (1, -1):
            t = tuple(b[(sg * d + r) % 8] for d in range(8))
            if best is None or t < best: best = t
    return ''.join('1' if v else '0' for v in best)
def draw(ax, pts, title, cell=None):
    rad = 6.2
    for x, p in pts.items():
        for i, j in itertools.combinations(range(4), 2):
            xs = [x, tuple(x[k] + (k == i) for k in range(4)), tuple(x[k] + (k == i) + (k == j) for k in range(4)), tuple(x[k] + (k == j) for k in range(4))]
            if all(y in pts for y in xs):
                P = [pts[y] for y in xs]
                cx, cy = sum(q[0] for q in P) / 4, sum(q[1] for q in P) / 4
                if cx * cx + cy * cy > rad * rad: continue
                ax.add_patch(Polygon(P, closed=True, facecolor=('#efe3bf' if j - i == 2 else '#dfe7ef'), edgecolor='#555555', linewidth=0.5, zorder=1))
    for x, p in pts.items():
        if p[0] ** 2 + p[1] ** 2 > rad * rad: continue
        c = star(x, pts)
        if c in STARC: ax.scatter([p[0]], [p[1]], s=9 if c != '01011111' else 22, marker=MK[c], color=STARC[c], linewidths=0, zorder=3)
    if cell:
        ax.add_patch(Polygon(cell, closed=True, fill=False, edgecolor=RED, linewidth=1.3, zorder=4))
    ax.set_aspect('equal'); ax.set_xlim(-rad, rad); ax.set_ylim(-rad, rad); ax.axis('off'); ax.set_title(title, fontsize=8.5, loc='left')
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.9), dpi=240)
P1 = tiling(sel_ap); P2 = tiling(sel_qc)
L = int_kernel(N)
ph = lambda v: (sum(v[k] * PH[k][0] for k in range(4)), sum(v[k] * PH[k][1] for k in range(4)))
u, v = ph(L[0]), ph(L[1])
while True:
    if u[0] ** 2 + u[1] ** 2 > v[0] ** 2 + v[1] ** 2: u, v = v, u
    m = round((u[0] * v[0] + u[1] * v[1]) / (u[0] ** 2 + u[1] ** 2))
    if m == 0: break
    v = (v[0] - m * u[0], v[1] - m * u[1])
o = (-u[0] / 2 - v[0] / 2, -u[1] / 2 - v[1] / 2)
cell = [o, (o[0] + u[0], o[1] + u[1]), (o[0] + u[0] + v[0], o[1] + u[1] + v[1]), (o[0] + v[0], o[1] + v[1])]
draw(axs[0], P1, f'(a) approximant t = 5/7, square period {math.hypot(*u):.2f}')
draw(axs[1], P2, '(b) Ammann–Beenker quasicrystal')
from matplotlib.lines import Line2D
h = [Line2D([], [], marker=MK[c], color=CC[c], ls='', markersize=4, label=NAME[c]) for c in law]
fig.legend(handles=h, loc='lower center', ncol=6, fontsize=6.5, frameon=False, bbox_to_anchor=(0.45, 0.0))
fig.tight_layout(rect=(0, 0.06, 1, 0.95)); mark(fig)
fig.savefig(os.path.join(OUT, 'patches.png')); plt.close(fig)
print('figures written')
