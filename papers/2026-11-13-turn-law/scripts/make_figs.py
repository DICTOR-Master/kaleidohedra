"""Figures for the turn-law paper (float drawings of exact objects; each plotted value is checked against its exact form).
usage: python3 make_figs.py STUDIES_DIR OUT_DIR    (STUDIES_DIR holds 2026-11-09-ab-turn/scripts/zono.py)
Figure 1: the cube line (solids at mu = 1.2, sqrt3, 2.5; the antipol pair and the tangent solid), t_min on six regular lines and on a
          rhombic disphenoid line, against log(mu/hR).
Figure 2: the Ammann-Beenker line: T(2/3), T(1/sqrt2), T(3/4) (T(3/4) = T(2/3) turned by 45 degrees), squares per rhombus f(t).
Figure 3: three other turns: the beat line's shell ratios (#43), the yantra viewpoint orbits (#103), the dodecahedron-icosahedron line.
Ends with FINAL ok when every check passes."""
import sys, os, math, itertools, random
from fractions import Fraction as Fr
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import HalfspaceIntersection, ConvexHull
sys.path.insert(0, os.path.join(sys.argv[1], '2026-11-09-ab-turn', 'scripts'))
from zono import zonogon, halfplanes, cross, sub
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
OK = True
def check(name, cond):
    global OK
    OK &= bool(cond); print(('  ok   ' if cond else '  FAIL ') + name, flush=True)
GOLD = '#b8860b'; INK = '#222222'; RED = '#c0392b'; BLUE = '#2c5d9e'; GREY = '#888888'
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6})
def mark(fig):
    fig.text(0.995, 0.005, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=6.5, color='#9a7b2f')

# ---------------------------------------------------------------- Figure 1
def corners(N, d):
    hs = HalfspaceIntersection(np.hstack([N, -np.asarray(d, float)[:, None]]), np.zeros(N.shape[1]))
    out = []
    for p in hs.intersections:
        if not any(np.linalg.norm(p - q) < 1e-9 for q in out): out.append(p)
    return np.array(out)
Nc = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
Vc = np.array(list(itertools.product((1, -1), repeat=3)), float) / math.sqrt(3)
def cube_line(mu): return np.vstack([Nc, Vc]), np.array([1.0] * 6 + [mu / math.sqrt(3)] * 8)
def draw_solid(ax, N, d, title):
    C = corners(N, d); hull = ConvexHull(C)
    for i, n in enumerate(N):
        on = [p for p in C if abs(p @ n - d[i]) < 1e-9]
        if len(on) < 3: continue
        on = np.array(on); c0 = on.mean(0); u = on[0] - c0; u /= np.linalg.norm(u); w = np.cross(n, u)
        ang = np.arctan2((on - c0) @ w, (on - c0) @ u); poly = on[np.argsort(ang)]
        col = '#e9d9a6' if i < 6 else '#9fb7d9'
        ax.add_collection3d(Poly3DCollection([poly], facecolor=col, edgecolor=INK, linewidths=0.6, alpha=0.95))
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1); ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=35); ax.set_axis_off(); ax.set_title(title, fontsize=8.5)
    return C
def closed(nodes, m):
    h2, R2 = nodes[0], nodes[-1]; c = h2 * R2; m2 = c / m
    for r, A in zip(nodes, nodes[1:]):
        if r <= m <= A and r <= m2 <= A: return r + (m - r) * (m2 - r) / (A - r)
    return min(m, m2)
s5 = math.sqrt(5); phi = (1 + s5) / 2
LINES = {'cube / octahedron': [1, 2, 3], 'dodecahedron': [1 + 2 * s5 / 5, phi**2, 3], 'tetrahedron': [1 / 3, 1, 3],
         '24-cell': [1, 4 / 3, 1.5, 2], '600-cell': [7 / 16 + 3 * s5 / 16, .5 + s5 / 6, 5 / 8 + s5 / 8, 1], '5-cube': [1, 2, 3, 4, 5]}
PEAKS = {'cube / octahedron': 5 - 2 * math.sqrt(3), 'dodecahedron': 10 - s5 - math.sqrt(30 + 6 * s5), 'tetrahedron': 3,
         '24-cell': 24 - 16 * math.sqrt(2), '600-cell': 26 - 2 * s5 - 10 * math.sqrt(2) - 2 * math.sqrt(10), '5-cube': 11 - 4 * s5}
fig = plt.figure(figsize=(7.2, 5.8))
for j, (mu, ttl) in enumerate([(1.2, 'S(1.2)'), (math.sqrt(3), 'S(√3): the tangent solid'), (2.5, r'S(2.5) = S(1.2)$^{\vee}$ (h = 1)')]):
    ax = fig.add_subplot(2, 3, j + 1, projection='3d'); N, d = cube_line(mu); C = draw_solid(ax, N, d, ttl)
    if j == 1:
        check('Figure 1: S(sqrt3) has every face at distance 1 (tangent to the unit sphere)', np.allclose(d / np.linalg.norm(N, axis=1), 1))
N1, d1 = cube_line(1.2); Cv = corners(N1, 1 / d1); C25 = corners(*cube_line(2.5))
check('Figure 1: corners of S(1.2)^v equal those of S(2.5) (antipol rule, h = 1, c = 3)', len(Cv) == len(C25) and all(min(np.linalg.norm(C25 - y, axis=1)) < 1e-9 for y in Cv))
ax = fig.add_subplot(2, 2, 3)
cols = [INK, GOLD, RED, BLUE, '#6a8f3a', '#8e5ea2']
for (name, nodes), col in zip(LINES.items(), cols):
    h2, R2 = nodes[0], nodes[-1]; c = h2 * R2
    xs = np.sort(np.append(np.exp(np.linspace(math.log(h2) + 1e-4, math.log(R2) - 1e-4, 1500)), math.sqrt(c))); ys = np.array([closed(nodes, x) for x in xs]) / h2
    ax.plot(np.log(xs / math.sqrt(c)), ys, color=col, lw=1.1, label=name)
    check(f'Figure 1: {name} peak plotted {ys.max():.6f} = exact {PEAKS[name]:.6f}', abs(ys.max() - PEAKS[name]) < 2e-5)
ax.axvline(0, color=GOLD, lw=0.8, ls='--'); ax.set_xlabel('log(μ / hR)   (the turn: x ↦ −x)'); ax.set_ylabel('t_min(S(μ))')
ax.legend(fontsize=6.5, frameon=False, loc='upper right'); ax.set_title('(d) six regular lines: symmetric, largest at the turn', fontsize=8.5)
# rhombic disphenoid line (numerical)
a, b, cz = 1, 1.3, 1.7
V = np.array([[a, b, cz], [a, -b, -cz], [-a, b, -cz], [-a, -b, cz]], float); R = np.linalg.norm(V[0]); Nf = []
for f in itertools.combinations(range(4), 3):
    p, q, r = V[list(f)]; n = np.cross(q - p, r - p); n /= np.linalg.norm(n); Nf.append(n if n @ p > 0 else -n)
Nf = np.array(Nf); h = float(Nf[0] @ V[0] if abs(Nf[0] @ V[0]) > 1e-9 else Nf[0] @ V[1]); h = max(Nf[0] @ V.T)
def dline(mu): return np.vstack([Nf, V / R]), np.array([h] * 4 + [mu / R] * 4)
xs = np.exp(np.linspace(math.log(h * h) + 1e-3, math.log(R * R) - 1e-3, 301)); ts = []
for mu in xs:
    N, d = dline(mu); ts.append(float(np.max(corners(N, d) @ corners(N, 1 / d).T)))
ts = np.array(ts); ax = fig.add_subplot(2, 2, 4)
ax.plot(np.log(xs / (h * R)), ts, color=BLUE, lw=1.2); ax.axvline(0, color=GOLD, lw=0.8, ls='--')
ax.set_xlabel('log(μ / hR)'); ax.set_ylabel('t_min (numerical)'); ax.set_title('(e) a rhombic disphenoid line (not regular)', fontsize=8.5)
k = int(np.argmax(ts)); print(f'     disphenoid: argmax mu/hR = {xs[k] / (h * R):.5f}, max {ts[k]:.6f}')
check('Figure 1: disphenoid curve symmetric under the turn (interpolated, < 1e-3)', max(abs(np.interp(-np.log(xs / (h * R)), np.log(xs / (h * R)), ts) - ts)) < 1e-3)
fig.text(0.01, 0.97, '(a)–(c) the cube line S(μ) = cube ∩ μ·octahedron: cube faces gold, octahedron faces blue', fontsize=8)
fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08, hspace=0.12, wspace=0.28); mark(fig); fig.savefig(os.path.join(OUT, 'fig1-turn-law.png'), dpi=220); plt.close(fig)

# ---------------------------------------------------------------- Figure 2
def epsr(t): return [(-t, t), (1, 0), (-t, -t), (0, 1)]
PH = [(math.cos(k * math.pi / 4), math.sin(k * math.pi / 4)) for k in range(4)]
def patch(t, gam, N=7, rad=4.6, exact=True):
    if exact:
        Ev = epsr(t); W = zonogon([(Fr(x), Fr(y)) for x, y in Ev]); H = halfplanes(W)
        def inside(y): return min(cross(sub(b_, a_), sub(y, a_)) for a_, b_ in H) > 0
    else:
        Ev = epsr(t); W = zonogon(Ev); H = halfplanes(W)
        def inside(y): return min(cross(sub(b_, a_), sub(y, a_)) for a_, b_ in H) > 1e-12
    pts = {}
    for n in itertools.product(range(-N, N + 1), repeat=4):
        x = (sum(n[k] * PH[k][0] for k in range(4)), sum(n[k] * PH[k][1] for k in range(4)))
        if x[0]**2 + x[1]**2 > (rad + 1.5)**2: continue
        y = (sum(n[k] * Ev[k][0] for k in range(4)) - gam[0], sum(n[k] * Ev[k][1] for k in range(4)) - gam[1])
        if inside(y): pts[n] = x
    edges = []
    for n, x in pts.items():
        for k in range(4):
            m = tuple(n[i] + (i == k) for i in range(4))
            if m in pts: edges.append((x, pts[m]))
    return pts, edges
random.seed(11)
g = (Fr(random.randint(1, 10**6), 10**6 + 3), Fr(random.randint(1, 10**6), 10**6 + 7))
M = [[Fr(3, 4), Fr(-3, 4)], [Fr(3, 4), Fr(3, 4)]]          # Rot45/(sqrt2 t) at t = 2/3
g2 = (-(M[0][0] * g[0] + M[0][1] * g[1]) - Fr(-3, 4), -(M[1][0] * g[0] + M[1][1] * g[1]) - Fr(3, 4))   # minus eps_0(3/4) = (-3/4, 3/4)
P1, E1 = patch(Fr(2, 3), g); P3, E3 = patch(Fr(3, 4), g2)
rot = lambda x: ((x[0] - x[1]) / math.sqrt(2), (x[0] + x[1]) / math.sqrt(2))
r1 = {tuple(np.round(rot(x), 9)) for x in P1.values() if x[0]**2 + x[1]**2 < 4.5**2}
r3 = {tuple(np.round(x, 9)) for x in P3.values() if x[0]**2 + x[1]**2 < 4.5**2}
check(f'Figure 2: the plotted T(3/4) is T(2/3) turned by 45 degrees ({len(r1)} vertices in the disc of radius 4.5)', r1 == r3 and len(r1) > 40)
ga = (0.1234567, 0.3456789); PA, EA = patch(1 / math.sqrt(2), ga, exact=False)
fig = plt.figure(figsize=(7.2, 5.3))
for j, (E_, ttl) in enumerate([(E1, '(a) T(2/3): a crystal'), (EA, '(b) T(1/√2): Ammann–Beenker'), (E3, '(c) T(3/4) = T(2/3) turned 45°')]):
    ax = fig.add_axes([0.01 + 0.33 * j, 0.42, 0.31, 0.53])
    for p, q in E_:
        if max(p[0]**2 + p[1]**2, q[0]**2 + q[1]**2) < 4.6**2: ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=0.55)
    ax.set_aspect('equal'); ax.set_xlim(-4.7, 4.7); ax.set_ylim(-4.7, 4.7); ax.axis('off'); ax.set_title(ttl, fontsize=8.5)
ax = fig.add_axes([0.09, 0.08, 0.86, 0.27])
tt = np.linspace(0.5, 1.0, 400); ax.plot(tt, 1 / (4 * tt) + tt / 2, color=BLUE, lw=1.2)
for p, q in [(2 / 3, 3 / 4), (5 / 7, 7 / 10), (12 / 17, 17 / 24)]:
    fp = 1 / (4 * p) + p / 2; fq = 1 / (4 * q) + q / 2
    check(f'Figure 2: f({p:.4f}) = f({q:.4f}) (turned pair)', abs(fp - fq) < 1e-12)
    ax.plot([p, q], [fp, fq], 'o', color=RED, ms=3); ax.plot([p, q], [fp, fq], color=RED, lw=0.5, ls=':')
ax.axvline(1 / math.sqrt(2), color=GOLD, lw=0.8, ls='--'); ax.plot([1 / math.sqrt(2)], [1 / math.sqrt(2)], 'o', color=GOLD, ms=4)
ax.set_xlabel('t   (the turn t ↦ 1/(2t); fixed point 1/√2)'); ax.set_ylabel('squares per rhombus')
ax.set_title('(d) squares per rhombus f(t) = (1 + 2t²)/(4t): least at the quasicrystal; Pell pairs at equal height', fontsize=8.5)
mark(fig); fig.savefig(os.path.join(OUT, 'fig2-ab-line.png'), dpi=220); plt.close(fig)

# ---------------------------------------------------------------- Figure 3
fig = plt.figure(figsize=(7.2, 2.9))
ax = fig.add_axes([0.07, 0.2, 0.25, 0.65])
tk = {1: (5 - s5) / 2, 2: 3 / phi**2, 3: 5 - 5 * s5 / 3, 4: 3 / phi**2, 5: (5 - s5) / 2}
ax.bar(list(tk), list(tk.values()), color=[GOLD if k in (1, 3, 5) else '#c9b98a' for k in tk], width=0.6)
ax.set_ylim(1, 1.42); ax.set_xticks(list(tk)); ax.set_xlabel('shell k'); ax.set_ylabel(r'$t_k$ (shell $S_{k-1} \to S_k$)'); ax.set_title(r'(a) #43 beat line: $t_k = t_{6-k}$', fontsize=8.5)
check('Figure 3: shell ratios symmetric about k = 3 (t_k = t_{6-k})', abs(tk[1] - tk[5]) < 1e-15 and abs(tk[2] - tk[4]) < 1e-15)
ax = fig.add_axes([0.40, 0.2, 0.25, 0.65])
uK = 0.7504385160222140244; uD, vD = 0.6793, 0.6950
for p_, col, lab in [(uK * uK, RED, 'Kulaichev'), (2 / phi**3, BLUE, 'DICTO Yantra')]:
    uu = np.linspace(0.45, 1.05, 300); ax.plot(uu, p_ / uu, color=col, lw=1, label=f'u·v = {p_:.4f} ({lab})')
ax.plot([0.45, 1.05], [0.45, 1.05], color=GOLD, lw=0.8, ls='--', label='the turn u = v')
ax.plot([uK], [uK], 'o', color=RED, ms=4); ax.plot([uD], [vD], 'o', color=BLUE, ms=4)
check('Figure 3: the DICTO Yantra point lies on its orbit u v = 2/phi^3 (to the 4 digits drawn)', abs(uD * vD - 2 / phi**3) < 2e-4)
ax.set_xlim(0.45, 1.05); ax.set_ylim(0.45, 1.05); ax.set_aspect('equal'); ax.set_xlabel('upper slope u'); ax.set_ylabel('lower slope v')
ax.legend(fontsize=5.6, frameon=False, loc='upper right'); ax.set_title('(b) #103 viewpoint orbits', fontsize=8.5)
ax = fig.add_axes([0.74, 0.2, 0.24, 0.65])
nodes = LINES['dodecahedron']; h2, R2 = nodes[0], nodes[-1]; c = h2 * R2
xs = np.exp(np.linspace(math.log(h2) + 1e-4, math.log(R2) - 1e-4, 800)); ys = np.array([closed(nodes, x) for x in xs]) / h2
ax.plot(xs, ys, color=INK, lw=1.1); ax.axvline(math.sqrt(c), color=GOLD, lw=0.8, ls='--')
for w in nodes[1:-1]: ax.axvline(w, color=GREY, lw=0.6, ls=':')
ax.set_xlabel('μ (dodecahedron line)'); ax.set_ylabel('t_min'); ax.set_title('(c) dodecahedron–icosahedron', fontsize=8.5)
mark(fig); fig.savefig(os.path.join(OUT, 'fig3-other-turns.png'), dpi=220); plt.close(fig)
print('FINAL ok' if OK else 'FINAL FAIL')
