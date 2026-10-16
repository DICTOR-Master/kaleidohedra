# P4 figures (Fable's advice, 2026-10-16), all orthographic, from the interlock data (float corners, for drawing only):
#   renders/p4-ladder.png   both settings, one turn, original vs reversed stations on a log-radius scale, shared stations joined
#   renders/p4-section.png  the flat section z = 0 (a mirror plane holding 5-, 3- and 2-fold axes), ends and middle side by side
#   renders/p4-gallery-<setting>.png  one piece of each kind at one common scale, each with a locator in the section
import json, itertools, re, numpy as np
from scipy.spatial import ConvexHull
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
p = (1 + 5 ** .5) / 2
BG = '#f4f1ea'; INK = '#2a2218'; WARM = '#a0521d'; COOL = '#1f6aa5'
COL = ['#4dd0e1', '#c792ea', '#5fd38a', '#f08fc0', '#9fd8ff', '#ff9a52']          # by original layer, as in the earlier renders
OL = ['I→ID', 'ID→D', 'D→TI', 'TI→H', 'H→RT', 'RT→I·φ³']
AB = {'icosahedron': 'I', 'icosidodecahedron': 'ID', 'dodecahedron': 'D', 'truncated icosahedron': 'TI', 'Hecatodihedron': 'H', 'rhombic triacontahedron': 'RT',
      'icosahedron (phi^3)': 'I·φ³', 'dodecahedron (inner)': 'D', 'dual of the Hecatodihedron': 'O', 'pentakis dodecahedron': 'PD', 'dodecahedron (phi^3)': 'D·φ³'}
SET = {'ends': dict(rho2=p * p / 4, turns=(0, 1), scale=1.0, n='1'), 'middle': dict(rho2=3 * p * p / 4, turns=(-1, 0), scale=3.0, n='2')}
orig = [(AB[n], np.array(X)) for n, X in json.load(open('data/orig-chain.json'))]
flip0 = [(AB[n], np.array(X)) for n, X in json.load(open('data/flip-ends-chain.json'))]
def mark(fig): fig.text(0.995, 0.006, 'DICTO · dictospheres.com', ha='right', va='bottom', color='#5b5346', fontsize=9)
def radii(X):
    h = ConvexHull(X); return -h.equations[:, 3].max(), np.linalg.norm(X, axis=1).max()
SUF = {-2: '·φ⁻⁶', -1: '·φ⁻³', 0: '', 1: '·φ³', 2: '·φ⁶'}
def flipped(s):                                         # reversed stations at the setting's size, over enough turns to cover one original turn
    c = SET[s]; return [(n + SUF[t], X * c['scale'] * p ** (3 * t)) for t in range(-2, 3) for n, X in flip0[:-1]]
def same(X, Y): return len(X) == len(Y) and abs(radii(X)[1] - radii(Y)[1]) < 1e-6 and abs(radii(X)[0] - radii(Y)[0]) < 1e-6

# ---------- 1. the toggle ladder
from matplotlib.ticker import FixedLocator, NullLocator
fig, axs = plt.subplots(1, 2, figsize=(10.5, 7), facecolor=BG)
for ax, s in zip(axs, ('ends', 'middle')):
    ax.set_facecolor(BG); lo, hi = radii(orig[0][1])[0] / 1.06, radii(orig[-1][1])[1] * 1.06
    rho = SET[s]['rho2'] ** .5
    for k in range(-6, 7):
        r = rho * p ** (1.5 * k)
        if lo < r < hi:
            tg = k == 0; ax.axhline(r, color='#8a8170', lw=1.3 if tg else 0.8, ls='--' if tg else ':', zorder=0)
            ax.text(2.02, r, 'toggle sphere' if tg else 'mirror sphere', va='center', fontsize=8, color='#6d6556')
    fl = [(n, X) for n, X in flipped(s) if radii(X)[1] > lo and radii(X)[0] < hi]
    pos = {}
    for side, chain, colr, x0 in ((0, orig, WARM, 0.0), (1, fl, COOL, 1.2)):
        lanes = []
        for n, X in sorted(chain, key=lambda t: radii(t[1])[0]):
            a_, b_ = radii(X); j = next((i for i, e in enumerate(lanes) if e < a_ / 1.02), len(lanes))
            if j == len(lanes): lanes.append(0)
            lanes[j] = b_; x = x0 + (0.22 * j if side else -0.22 * j)
            ax.plot([x, x], [max(a_, lo), min(b_, hi)], color=colr, lw=6, solid_capstyle='butt', alpha=0.9)
            ax.text(x + (0.045 if side else -0.045), (max(a_, lo) * min(b_, hi)) ** .5, n, ha='left' if side else 'right', va='center', fontsize=9.5, color=colr, fontweight='bold')
            pos[(side, n)] = (x, X, (a_ * b_) ** .5)
    for (sd, n), (x, X, m) in pos.items():
        if sd != 1: continue
        for (sd2, n2), (x2, Y, m2) in pos.items():
            if sd2 == 0 and same(X, Y): ax.plot([x2 + 0.03, x - 0.03], [m, m], color=INK, lw=3, zorder=3); ax.text((x + x2) / 2, m * 1.02, 'shared', ha='center', va='bottom', fontsize=8.5, color=INK)
    ax.set_yscale('log'); ax.set_ylim(lo, hi); ax.set_xlim(-1.0, 2.45)
    ax.yaxis.set_major_locator(FixedLocator([0.5, 0.75, 1, 1.5, 2])); ax.yaxis.set_minor_locator(NullLocator()); ax.set_yticklabels(['0.5', '0.75', '1', '1.5', '2'])
    ax.set_xticks([-0.15, 1.35]); ax.set_xticklabels(['original cycle', 'reversed cycle']); ax.tick_params(axis='x', length=0)
    ax.set_ylabel('radius (log scale)')
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.set_title(f'{"Ends" if s == "ends" else "Middle"} setting, ρ² = {"φ²/4" if s == "ends" else "3φ²/4"}', fontsize=12)
fig.text(0.43, 0.012, "One turn of the original cycle, I to I·φ³. Bars run from face distance to corner radius; black bars join shared stations.", ha='center', fontsize=9, color='#5b5346')
fig.tight_layout(rect=(0, 0.035, 1, 1)); mark(fig); fig.savefig('renders/p4-ladder.png', dpi=200, facecolor=BG); plt.close(fig)

# ---------- helpers for sections and solids
def section(X, z=0.0):
    pts = [x[:2] for x in X if abs(x[2] - z) < 1e-9]
    for a, b in itertools.combinations(X, 2):
        if (a[2] - z) * (b[2] - z) < -1e-12: t = (z - a[2]) / (b[2] - a[2]); pts.append((a + t * (b - a))[:2])
    if len(pts) < 3: return None
    P = np.array(pts)
    try: h = ConvexHull(P)
    except Exception: return None
    return P[h.vertices] if h.volume > 1e-9 else None
def faces(X):
    h = ConvexHull(X); out = []; seen = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in seen): continue
        seen.append(e); idx = [i for i in range(len(X)) if abs(X[i] @ e[:3] + e[3]) < 1e-7]
        F = X[idx]; c = F.mean(0); u = F[0] - c; u /= np.linalg.norm(u); w = np.cross(e[:3], u)
        out.append((F[np.argsort([np.arctan2((f - c) @ w, (f - c) @ u) for f in F])], e[:3]))
    return out
def kinds(s):
    d = json.load(open(f'data/interlock-{s}.json')); vols = sorted({round(q['vol'], 7) for q in d['pieces']}, reverse=True)
    for q in d['pieces']: q['k'] = vols.index(round(q['vol'], 7)) + 1; q['X'] = np.array(q['v'])
    return d['pieces'], len(vols)
I0 = orig[0][1]; ax5 = [v / np.linalg.norm(v) for v in I0]
def axes_in_plane():
    fc = [];  ed = []
    h = ConvexHull(I0)
    for s_ in h.simplices: fc.append(I0[s_].mean(0))
    for a, b in itertools.combinations(I0, 2):
        if abs(np.linalg.norm(a - b) - 1 / p) < 1e-6: ed.append((a + b) / 2)
    pick = lambda L: [v / np.linalg.norm(v) for v in L if abs(v[2]) < 1e-9]
    return {'5': pick(I0), '3': pick(fc), '2': pick(ed)}
AX = axes_in_plane()

# ---------- 2. the section
fig, axs = plt.subplots(1, 2, figsize=(11, 5.9), facecolor=BG)
for ax, s in zip(axs, ('ends', 'middle')):
    ax.set_facecolor(BG); P, nk = kinds(s); R = radii(orig[-1][1])[1] * 1.08
    for q in P:
        S = section(q['X'])
        if S is not None: ax.add_patch(Polygon(S, closed=True, fc=COL[q['o'][0]], ec='#6d6556', lw=0.35, alpha=0.75))
    fl = flipped(s); outer = Polygon(section(orig[-1][1]), closed=True, transform=ax.transData)
    ax.add_patch(Polygon(section(orig[0][1]), closed=True, fc=BG, ec='none', zorder=3.5))
    for n, X in orig:
        S = section(X); sh = any(same(X, Y) for _, Y in fl)
        ax.add_patch(Polygon(S, closed=True, fill=False, ec=INK if sh else WARM, lw=2.6 if sh else 1.5, zorder=4))
    for n, X in fl:
        if radii(X)[0] > R or radii(X)[1] < radii(orig[0][1])[0] or any(same(X, Y) for _, Y in orig): continue
        S = section(X)
        if S is not None:
            pg = Polygon(S, closed=True, fill=False, ec=COOL, lw=1.3, zorder=3); ax.add_patch(pg); pg.set_clip_path(outer)
    for sym, L in AX.items():
        for v in L:
            if v[0] < -1e-9 or v[1] < -1e-9: continue
            ax.plot([v[0] * R * 0.985, v[0] * R * 1.04], [v[1] * R * 0.985, v[1] * R * 1.04], color=INK, lw=1)
            ax.text(v[0] * R * 1.08, v[1] * R * 1.08, sym, ha='center', va='center', fontsize=10, fontweight='bold')
    ax.set_xlim(0, R * 1.14); ax.set_ylim(0, R * 1.14); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f'{"Ends" if s == "ends" else "Middle"} setting', fontsize=12, pad=4)
hd = [Polygon([[0, 0]], fc=c, ec='#6d6556', lw=0.4, alpha=0.75, label=l) for c, l in zip(COL, OL)]
from matplotlib.lines import Line2D
hd += [Line2D([], [], color=WARM, lw=1.5, label='original station'), Line2D([], [], color=COOL, lw=1.3, label='reversed station'), Line2D([], [], color=INK, lw=2.6, label='shared station')]
fig.legend(handles=hd, loc='lower center', ncol=5, frameon=False, fontsize=8.5, title='fill: original layer of each piece', title_fontsize=8.5)
fig.subplots_adjust(0.02, 0.15, 0.98, 0.93, wspace=0.08); mark(fig); fig.savefig('renders/p4-section.png', dpi=200, facecolor=BG); plt.close(fig)

# ---------- 3D drawing
L = np.array([0.35, -0.5, 0.8]); L /= np.linalg.norm(L)
def shade(c, n):
    rgb = np.array(matplotlib.colors.to_rgb(c)); k = 0.62 + 0.38 * max(0, n @ L); return tuple(np.clip(rgb * k, 0, 1))
def draw(ax, X, c, lw=0.5):
    for F, n in faces(X): ax.add_collection3d(Poly3DCollection([F], facecolor=shade(c, n), edgecolor='#2a2218', linewidths=lw))
def rot_to_z(v):
    v = v / np.linalg.norm(v); z = np.array([0, 0, 1.]); c = v @ z; k = np.cross(v, z); s_ = np.linalg.norm(k)
    if s_ < 1e-12: return np.eye(3) if c > 0 else np.diag([1, -1, -1.])
    k /= s_; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]]); return np.eye(3) + s_ * K + (1 - c) * K @ K

# ---------- 3. gallery at one common scale (cleaned corners from interlock-kinds-render), with locators
TXT = open('data/interlock-kinds.txt').read()
for s in ('ends', 'middle'):
    P, nk = kinds(s); R_ = json.load(open(f'data/interlock-kinds-render-{s}.json'))['layers']
    stats = re.findall(r'(\d+) corners, (\d+) faces', TXT.split(f'== {s} setting')[1].split('== ')[0])
    reps = []
    for k in range(1, nk + 1):
        Q = [q for q in P if q['k'] == k]; X = np.array(R_[k - 1]['pieces'][0]['v']); c = X.mean(0); reps.append((Q, (X - c) @ rot_to_z(c).T))
    span = max((Xr.max(0) - Xr.min(0)).max() for _, Xr in reps) / 2
    cols = 4; rows = (nk + cols - 1) // cols; W, Hh = 3.3, 3.3
    fig = plt.figure(figsize=(cols * W, rows * Hh + 0.4), facecolor=BG); FH = rows * Hh + 0.4
    for i, (Q, Xr) in enumerate(reps):
        x0 = (i % cols) / cols; y0 = (0.4 + (rows - 1 - i // cols) * Hh) / FH; th = Hh / FH
        ax = fig.add_axes([x0 + 0.1 / cols, y0 + 0.17 * th, 0.9 / cols, 0.75 * th], projection='3d', proj_type='ortho', facecolor=BG)
        draw(ax, Xr, COL[Q[0]['o'][0]], 0.6)
        ax.set_xlim(-span, span); ax.set_ylim(-span, span); ax.set_zlim(-span, span); ax.set_box_aspect((1, 1, 1), zoom=1.45); ax.view_init(elev=12, azim=-60); ax.axis('off')
        nc, nf = stats[i]
        fig.text(x0 + 0.5 / cols, y0 + 0.13 * th, f'I{SET[s]["n"]}·{i + 1}  ×{len(Q)}', ha='center', fontsize=11.5, fontweight='bold')
        fig.text(x0 + 0.5 / cols, y0 + 0.05 * th, f'{OL[Q[0]["o"][0]]} · {nc} corners, {nf} faces', ha='center', fontsize=8.5, color='#3a3328')
        ins = fig.add_axes([x0 + 0.01 / cols, y0 + 0.62 * th, 0.34 / cols, 0.36 * th], facecolor=BG); R = radii(orig[-1][1])[1] * 1.02
        for n, X in orig: ins.add_patch(Polygon(section(X), closed=True, fill=False, ec='#b9ae98', lw=0.5))
        for q in Q:
            S = section(q['X'])
            if S is not None: ins.add_patch(Polygon(S, closed=True, fc=INK, ec=INK, lw=0.3))
        ins.set_xlim(-0.02, R); ins.set_ylim(-0.02, R); ins.set_aspect('equal'); ins.axis('off')
    fig.text(0.01, 0.008, 'All pieces at one scale, outward direction up. Inset: where the pieces of this kind cut the section of Figure 2 (black).', fontsize=8.5, color='#5b5346')
    mark(fig); fig.savefig(f'renders/p4-gallery-{s}.png', dpi=170, facecolor=BG); plt.close(fig)
print('done')
