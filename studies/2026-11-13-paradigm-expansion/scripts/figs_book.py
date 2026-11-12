# The new figures of The Permutohedron Paradigm, expanded version (PROPOSAL.html, figure plan; 13 Nov 2026).
# usage: figs_book.py pilot | all | NAME ...   -> ../figures/*.png, one PASS/FAIL line per check, last line FINAL ok / FINAL FAIL
# Every figure computes its geometry here from its definition (orders of values, half-spaces, Wythoff orbits) and checks the
# counts it draws against the book (1, 11, 11, 1; 1, 26, 66, 26, 1; 601 each way; 70 heights; ...). One red marks the swapping pair.
import sys, os, math, itertools, json
import numpy as np
from figlib import *
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, FancyArrowPatch, Circle, Rectangle
OK = [True]
def check(name, c):
    OK[0] &= bool(c); print(('PASS ' if c else 'FAIL ') + name, flush=True)
FIGS = {}
def fig(name):
    def deco(f): FIGS[name] = f; return f
    return deco

# ---------- geometry helpers
def perm3d(vals):
    """the permutohedron of four values, in 3D coordinates of the hyperplane sum = const (orthonormal basis)."""
    P = np.array(perms(vals), float); B = basis_sum0(4); return P, (P - P.mean(0)) @ B.T
def TO_faces_colours(P3, sq=GOLD, hx=BLUE):
    F = hull_faces(P3); return F, [sq if len(f) == 4 else hx for f, n in F]
def sweep_index(P, u, edges):
    """number of edges going down at each corner"""
    h = P @ u; idx = np.zeros(len(P), int)
    for a, b in edges:
        if h[b] < h[a]: idx[a] += 1
        else: idx[b] += 1
    return idx
def perm_edges(Pl):
    """edges of a permutohedron of distinct values: corners differing by a swap of two values adjacent in size."""
    vals = sorted(Pl[0]); pos = {v: i for i, v in enumerate(vals)}; E = []; key = {p: i for i, p in enumerate(Pl)}
    for i, p in enumerate(Pl):
        for k in range(len(vals) - 1):
            a, b = vals[k], vals[k + 1]; q = tuple(b if x == a else a if x == b else x for x in p)
            j = key[q]
            if i < j: E.append((i, j, k))
    return E

# ---------- Opening
ARC = [('Opening', 'one swap'), ('1', 'three values'), ('2', "Kelvin's cell"), ('3', 'the slider'), ('4', 'the bonds'), ('5', 'the RD taken apart'),
       ('6', 'scutoids'), ('7', 'web of swaps'), ('8', 'Centre I'), ('9', 'Centre II'), ('10', 'rosettes'), ('11', 'walls'),
       ('12', 'every n'), ('13', 'golden slice'), ('14', 'the Family'), ('15', 'the bells')]
RESULT = {'Opening': '1 move', '1': '6 orders', '2': '24 corners\n36 swaps', '3': 'silent at φ', '4': 'd = (g−m)/(g+m)', '5': 'volume 15', '6': '30 cells\nper shell',
          '7': '65 slices', '8': '26 · 66 · 26', '9': '601 each way', '10': 'balance\nby symmetry', '11': 'D = 0 from\nλ = −5s/8', '12': 'N(n), A(n, i)', '13': '35 kinds', '14': 'one cone', '15': '5396 tours'}
def thumb(ax, key, x, y, r):
    """a small drawing for each station of the arc."""
    R = rot(30, 22)
    def solid(P, F=None, cols=None, col=GOLD, s=1.0):
        sc = Scene(R); P = np.asarray(P, float); P = P - P.mean(0); P = P / np.abs(P).max() * r * s
        sc.solid(P, F, color=col, facecolors=cols, lw=0.6); sc.draw(ax, shift=(x, y))
    if key == 'Opening' or key == '1' or key == '15':
        P = np.array(perms((1, 2, 3)), float); B = basis_sum0(3); Q = (P - 2) @ B.T; Q = Q / np.abs(Q).max() * r
        order = [0, 1, 3, 5, 4, 2]; order = sorted(range(6), key=lambda i: math.atan2(Q[i, 1], Q[i, 0]))
        ax.add_patch(MPoly(Q[order] + [x, y], closed=True, fc=IVORY if key != '1' else GOLD, ec=RED if key != '1' else INK, lw=1.2, zorder=3))
    elif key in ('2', '3', '4'):
        vals = {'2': (1, 2, 3, 4), '3': (-PHI ** 3, -1, 1, PHI ** 3), '4': (1, 2, 4, 5)}[key]
        _, P3 = perm3d(vals); F, cols = TO_faces_colours(P3); solid(P3, F, cols)
    elif key == '5':
        G = [np.eye(3)[i] for i in range(3)] + [0.5 * np.array(s) for s in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]]
        pts = [sum(c * g for c, g in zip(cs, G)) for cs in itertools.product([0, 1], repeat=7)]
        F = hull_faces(np.array(pts)); solid(np.array(pts), F, [GOLD if len(f) == 4 else TEAL for f, n in F])
    elif key in ('8', '9', '10'):
        P = np.array(perms((1, 2, 3, 4, 5)), float) - 3; u = np.array([0.03, 0.31, 0.47, 0.71, 1.0]); u -= u.mean()
        Bp = basis_perp(5, [u]); t = 0.15 * (P @ u).max()
        pts = []
        for i, j, k in perm_edges([tuple(p) for p in P]):
            a, b = P[i] @ u - t, P[j] @ u - t
            if a * b < 0: pts.append((P[i] + (P[j] - P[i]) * a / (a - b)) @ Bp.T)
        solid(np.array(pts), col=VIOLET if key == '10' else TEAL, s=1.1)
    elif key == '7':
        P = np.array(perms((1, 2, 3, 4, 5)), float); th = 2 * np.pi * np.arange(5) / 5
        Q = np.c_[P @ np.cos(th), P @ np.sin(th)]; Q = Q / np.abs(Q).max() * r
        for i, j, k in perm_edges([tuple(p) for p in P]): ax.plot([x + Q[i, 0], x + Q[j, 0]], [y + Q[i, 1], y + Q[j, 1]], color=RED if k == 0 else '#6d6d6d', lw=0.35, zorder=3)
    elif key == '6':
        for k, (a, b) in enumerate([(-1, 1), (1, 1), (-1, -1), (1, -1)]):
            pass
        H = np.array([[math.cos(math.pi / 3 * i + math.pi / 6), math.sin(math.pi / 3 * i + math.pi / 6)] for i in range(6)]) * r * 0.5
        for c, col in (((-0.45, 0), VIOLET), ((0.45, 0), VIOLET), ((0, 0.78), RED), ((0, -0.78), RED)):
            ax.add_patch(MPoly(H + [x + c[0] * r, y + c[1] * r * 0.62], closed=True, fc=col, ec=INK, lw=0.6, alpha=0.8, zorder=3))
    elif key == '11':
        for k, lab in enumerate('ABCA'):
            yy = y - r * 0.75 + k * r * 0.5
            ax.add_patch(MPoly([[x - r, yy], [x + r * 0.6, yy], [x + r, yy + r * 0.3], [x - r * 0.6, yy + r * 0.3]], closed=True, fc=[GOLD, BLUE, TEAL, GOLD][k], ec=INK, lw=0.5, alpha=0.85, zorder=3))
    elif key == '12':
        for k, v in enumerate([3, 15, 65, 225, 770]):
            hh = math.log10(v) / 3 * r * 1.8
            ax.add_patch(Rectangle((x - r + k * r * 0.42, y - r), r * 0.32, hh, fc=GOLD, ec=INK, lw=0.5, zorder=3))
    elif key == '13':
        xs = np.linspace(-r, r, 40)
        for k, xv in enumerate(xs): ax.plot([x + xv, x + xv], [y - r * 0.6, y + r * 0.6], color=GOLD if (k * PHI) % 1 < 0.618 else BLUE, lw=1.6, zorder=3)
    elif key == '14':
        A = np.array(perms((1, 2, 3, 4)), float)
        F = None
        # Loday's associahedron as a member of the family: {sum = 10, sum over every interval I >= C(|I|+1, 2)}
        Bq = basis_sum0(4); Aint = []; bint = []
        for S in itertools.chain.from_iterable(itertools.combinations(range(4), k) for k in (1, 2, 3)):
            if list(S) == list(range(S[0], S[-1] + 1)):
                n = np.zeros(4); n[list(S)] = 1; Aint.append(-(n @ Bq.T)); bint.append(-(len(S) * (len(S) + 1) / 2 - n.sum() * 2.5))
        V = halfspace_vertices(np.array(Aint), np.array(bint)); solid(V, col=GOLD)
    ax.add_patch(Circle((x, y), r * 1.32, fc='none', ec='#d8cfb4', lw=0.6, zorder=1))

def arc_map(name, results):
    fig_, ax = plt.subplots(figsize=(11.0, 5.2)); blank(ax)
    n = len(ARC); xs = np.linspace(0, 15, n)
    # beginning low, climbing to the centre (8, 9 large), the summit at 14, the return to the ground at 15
    ys = np.array([0, 0.2, 0.45, 0.7, 0.95, 1.15, 1.8, 2.3, 3.0, 3.0, 2.6, 2.45, 2.6, 2.9, 3.6, 0.15])
    xs[-1] = 14.6; ys[-1] = -0.25
    ax.plot(xs[:-1], ys[:-1], color='#c7b37b', lw=2.2, zorder=1)
    ax.annotate('', xy=(xs[-1] + 0.45, ys[-1] + 0.3), xytext=(xs[-2] + 0.45, ys[-2] - 0.2), arrowprops=dict(arrowstyle='->', color=RED, lw=1.6, connectionstyle='arc3,rad=-0.25'), zorder=1)
    ax.annotate('', xy=(xs[0], ys[0] - 0.75), xytext=(xs[-1] - 0.5, ys[-1] - 0.75), arrowprops=dict(arrowstyle='->', color=RED, lw=1.0, ls=(0, (3, 3)), connectionstyle='arc3,rad=0.12'), zorder=1)
    bands = [(0.5, 5.5, 'Part One · the swap builds solids', GOLD_D), (5.5, 11.5, 'Part Two · scutoid tissues, the centre', RED), (11.5, 13.5, 'Part Three', GOLD_D), (13.5, 14.5, 'Summit', VIOLET)]
    for a, b, lab, col in bands:
        x0, x1 = np.interp(a, range(n), xs), np.interp(b, range(n), xs)
        ax.plot([x0 + 0.1, x1 - 0.1], [-1.25, -1.25], color=col, lw=3, solid_capstyle='butt'); ax.text((x0 + x1) / 2, -1.48, lab, ha='center', va='top', fontsize=8, color=col)
    for i, (k, lab) in enumerate(ARC):
        big = k in ('8', '9'); r = 0.36 if big else 0.27
        thumb(ax, k, xs[i], ys[i], r)
        ax.text(xs[i], ys[i] + r * 1.32 + 0.12, ('Ch. ' + k if k[0].isdigit() else k), ha='center', va='bottom', fontsize=8.5 if big else 7.5, weight='bold' if big else 'normal', color=RED if big else INK)
        ax.text(xs[i], ys[i] - r * 1.32 - 0.08, (results.get(k) if results else lab), ha='center', va='top', fontsize=6.8 if results else 7, color='#444', linespacing=1.0)
    ax.text(xs[-1] + 0.3, ys[-1] - 1.0, 'the first hexagon, heard', fontsize=7, color=RED, ha='right', style='italic')
    ax.set_xlim(-0.7, 15.6); ax.set_ylim(-1.85, 4.35)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.99); save(fig_, name)
@fig('arc-map')
def f_arc(): arc_map('arc-map.png', None); check('arc map: 16 stations (Opening and 15 chapters)', len(ARC) == 16)
@fig('arc-map-results')
def f_arc2(): arc_map('arc-map-results.png', RESULT); check('arc map with results: 16 stations', len(RESULT) == 16)

def bells_hexagon(name, title_rows, heard=False):
    """three bells, six rows, each a corner of the hexagon; each side the pair of bells that swap (red)."""
    rows = [(1, 2, 3), (2, 1, 3), (2, 3, 1), (3, 2, 1), (3, 1, 2), (1, 3, 2)]
    # a row is the point whose coordinate b is the place of bell b
    def pt(r):
        place = {b: i + 1 for i, b in enumerate(r)}; v = np.array([place[1], place[2], place[3]], float) - 2
        B = basis_sum0(3); return v @ B.T
    Q = np.array([pt(r) for r in rows]); Q = Q @ np.array([[0, -1], [1, 0]])  # turn so rounds is at the top
    fig_, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 4.4), gridspec_kw=dict(width_ratios=[1, 1.5])); blank(a1); blank(a2)
    # left: the rows as ringers write them, the swapping pair red
    for k, r in enumerate(rows + [rows[0]]):
        y = -k * 0.62
        nxt = rows[(k + 1) % 6] if k < 6 else None
        sw = [i for i in range(3) if nxt and r[i] != nxt[i]]
        for i, b in enumerate(r):
            a1.text(i * 0.55, y, str(b), ha='center', va='center', fontsize=15, weight='bold', color=RED if i in sw else INK, family='DejaVu Sans Mono')
        if sw and k < 6:
            a1.annotate('', xy=(sw[1] * 0.55 - 0.05, y - 0.5), xytext=(sw[0] * 0.55 + 0.05, y - 0.12), arrowprops=dict(arrowstyle='-', color=RED, lw=1.0))
            a1.annotate('', xy=(sw[0] * 0.55 + 0.05, y - 0.5), xytext=(sw[1] * 0.55 - 0.05, y - 0.12), arrowprops=dict(arrowstyle='-', color=RED, lw=1.0))
        a1.text(-0.55, y, 'rounds' if k in (0, 6) else ('backrounds' if r == (3, 2, 1) else ''), ha='right', va='center', fontsize=8, color='#555')
    a1.set_xlim(-1.9, 1.5); a1.set_ylim(-4.2, 0.6)
    a1.text(0.55, 0.62, title_rows, ha='center', fontsize=9, color='#333')
    # right: the hexagon
    for k in range(6):
        a, b = Q[k], Q[(k + 1) % 6]; r, s = rows[k], rows[(k + 1) % 6]
        pair = sorted(set(x for x, y in zip(r, s) if x != y))
        a2.plot([a[0], b[0]], [a[1], b[1]], color=RED, lw=2.4, solid_capstyle='round', zorder=2)
        m = (a + b) / 2; o = m / np.linalg.norm(m) * 0.36
        a2.text(m[0] + o[0], m[1] + o[1], f'{pair[0]}↔{pair[1]}', ha='center', va='center', fontsize=9.5, color=RED)
        if heard:
            d = (b - a) * 0.18
            a2.annotate('', xy=(m[0] + d[0] - o[0] * 0.25, m[1] + d[1] - o[1] * 0.25), xytext=(m[0] - d[0] - o[0] * 0.25, m[1] - d[1] - o[1] * 0.25), arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
    a2.add_patch(MPoly(Q, closed=True, fc=IVORY, ec='none', zorder=1))
    for k, r in enumerate(rows):
        a2.scatter(*Q[k], s=34, color=INK, zorder=3)
        o = Q[k] / np.linalg.norm(Q[k]) * 0.34
        a2.text(Q[k, 0] + o[0], Q[k, 1] + o[1], ''.join(map(str, r)), ha='center', va='center', fontsize=11, family='DejaVu Sans Mono', weight='bold' if r in ((1, 2, 3), (3, 2, 1)) else 'normal')
    a2.set_xlim(-2.0, 2.0); a2.set_ylim(-1.75, 1.75)
    sides = [np.linalg.norm(Q[k] - Q[(k + 1) % 6]) for k in range(6)]
    check(f'{name}: six rows, each step one swap of neighbours, six equal sides √2 = {sides[0]:.4f}', all(abs(s - 2 ** .5) < 1e-9 for s in sides) and all(sum(x != y for x, y in zip(rows[k], rows[(k + 1) % 6])) == 2 for k in range(6)))
    mark(fig_); fig_.subplots_adjust(0.01, 0.07, 0.99, 0.97); save(fig_, name)
@fig('bells-hexagon')
def f_bells(): bells_hexagon('bells-hexagon.png', 'three bells, one swap of neighbours at a time')
@fig('bells-heard')
def f_bells2(): bells_hexagon('bells-heard.png', 'the extent on three bells, rung', heard=True)

# ---------- Chapter 1
@fig('three-hexagons')
def f_three():
    sets = [((1, 2, 3), '1, 2, 3: regular'), ((1, 1 + PHI, 2 + PHI), '1, 1 + φ, 2 + φ: golden'), ((1, 2, 4), '1, 2, 4: the 1:2')]
    fig_, axs = plt.subplots(1, 3, figsize=(11, 4.0))
    for ax, (vals, lab) in zip(axs, sets):
        blank(ax); P = np.array(perms(vals), float); B = basis_sum0(3); Q = (P - P.mean(0)) @ B.T
        order = sorted(range(6), key=lambda i: math.atan2(Q[i, 1], Q[i, 0])); Q = Q[order]; Pl = [perms(vals)[i] for i in order]
        ax.add_patch(MPoly(Q, closed=True, fc=IVORY, ec='none'))
        Ls = []
        for k in range(6):
            a, b = Q[k], Q[(k + 1) % 6]; r, s = Pl[k], Pl[(k + 1) % 6]
            pair = sorted(set(x for x, y in zip(r, s) if x != y)); L = np.linalg.norm(a - b); Ls.append((pair, L))
            ax.plot([a[0], b[0]], [a[1], b[1]], color=RED, lw=2.2, solid_capstyle='round')
            m = (a + b) / 2; o = m / np.linalg.norm(m)
            gap = pair[1] - pair[0]
            f = lambda v: {1: '1', 2: '2', 3: '3', 4: '4'}.get(v, f'{v:.3f}') if abs(v - round(v)) < 1e-9 else ('1 + φ' if abs(v - 1 - PHI) < 1e-9 else '2 + φ')
            sval = {1.0: '√2', 2.0: '2√2'}.get(round(gap, 6), 'φ√2' if abs(gap - PHI) < 1e-9 else f'√2·{gap:.3f}')
            ax.text(*(m + o * 0.42), f'{f(pair[0])}↔{f(pair[1])}', ha='center', va='center', fontsize=7.6, color=RED)
            ax.text(*(m - o * 0.30), sval, ha='center', va='center', fontsize=7.6, color='#555')
        for k in range(6):
            ax.scatter(*Q[k], s=14, color=INK, zorder=3)
        ax.set_xlim(-3.3, 3.3); ax.set_ylim(-3.1, 3.1); ax.set_title(lab, fontsize=10)
        g1, g2 = vals[1] - vals[0], vals[2] - vals[1]
        ok = all(abs(L - 2 ** .5 * (p[1] - p[0])) < 1e-9 for p, L in Ls) and abs(max(L for p, L in Ls) / min(L for p, L in Ls) - max(g1, g2) / min(g1, g2)) < 1e-9
        check(f'three-hexagons {lab}: every side √2 × the gap it swaps; side ratio = gap ratio {max(g1, g2) / min(g1, g2):.6f}', ok)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.93); save(fig_, 'three-hexagons.png')

# ---------- Chapter 2
@fig('kelvin-swaps')
def f_kelvin():
    vals = (1, 2, 3, 4); Pl = perms(vals); P = np.array(Pl, float); B = basis_sum0(4); P3 = (P - 2.5) @ B.T
    E = perm_edges(Pl); F = hull_faces(P3)
    check(f'Kelvin: 24 corners, {len(E)} edges, {len(F)} faces, Euler {24 - len(E) + len(F)}', len(E) == 36 and len(F) == 14)
    check('Kelvin: 12 edges swap each pair 1↔2, 2↔3, 3↔4', [sum(1 for e in E if e[2] == k) for k in range(3)] == [12, 12, 12])
    R = rot(28, 18)
    fig_, axs = plt.subplots(1, 3, figsize=(12, 4.6))
    sq = next(i for i, (f, n) in enumerate(F) if len(f) == 4 and (R[2] @ n) > 0.5)
    hx = next(i for i, (f, n) in enumerate(F) if len(f) == 6 and (R[2] @ n) > 0.3 and len(set(F[sq][0]) & set(f)) == 2)
    for k, ax in enumerate(axs):
        blank(ax); sc = Scene(R)
        cols = [GOLD if i in (sq, hx) else '#f2efe6' for i in range(len(F))]
        sc.solid(P3, F, facecolors=cols, edge='#4a4a4a', lw=0.8, alpha=0.86)
        for i, j, kk in E:
            front = all(any(((R[2] @ n) > 1e-9) and (i in f and j in f) for f, n in F) for _ in [0])
            if kk == k:
                sc.line(P3[i], P3[j], color=RED, lw=2.6 if front else 1.2, ls='-' if front else (0, (2, 2)), z=1 if front else -1)
        if k == 0:
            for i, p in enumerate(Pl):
                if any((R[2] @ n) > 1e-9 and i in f for f, n in F):
                    sc.dot(P3[i], s=6, label=''.join(map(str, p)), fs=6.2, dy=0.0, z=2)
        sc.draw(ax); ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)
        ax.set_title(f'the 12 swaps {k + 1}↔{k + 2}', fontsize=10, color=RED)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.93); save(fig_, 'kelvin-swaps.png')

# ---------- Chapter 3
def P_mu(mu):
    a = mu - 1
    if mu <= 2:
        pts = set()
        for p in itertools.permutations((1.0, a, 0.0)):
            for s in itertools.product((1, -1), repeat=3): pts.add(tuple(round(x * y, 12) for x, y in zip(p, s)))
    else:
        b = mu - 2; pts = set()
        for p in itertools.permutations((1.0, 1.0, b)):
            for s in itertools.product((1, -1), repeat=3): pts.add(tuple(round(x * y, 12) for x, y in zip(p, s)))
    return np.array(sorted(pts))
def Q4(mu):
    P = P_mu(mu); r = np.linalg.norm(P, axis=1); K = ((P ** 4).sum(1) / r ** 4 - 3 / 5).mean()
    return 0.7637626 * abs(K) / 0.4
@fig('slider-silent')
def f_slider():
    fig_ = plt.figure(figsize=(11, 5.6)); ax = fig_.add_axes([0.03, 0.42, 0.94, 0.55]); blank(ax)
    stops = [(1.0, 'octahedron'), (4 / 3, 'DICTO 1:2\nx = 1/2'), (1.5, "Kelvin's cell\nx = 1"), (PHI, 'Icosaxes\nx = φ, silent'), (5 / 3, 'DICTO 2:1\nx = 2'), (2.0, 'cuboctahedron')]
    R = rot(30, 20)
    for k, (mu, lab) in enumerate(stops):
        P = P_mu(mu); F = hull_faces(P); sc = Scene(R); xk = k * 2.05
        sc.solid(P, F, facecolors=[GOLD if len(f) == 4 else BLUE for f, n in F], lw=0.8)
        sc.draw(ax, scale=0.62, shift=(xk, 0)); silent = abs(mu - PHI) < 1e-9
        ax.text(xk, -1.25, lab + f'\nμ = {mu:.4g}', ha='center', va='top', fontsize=8, color=RED if silent else INK, weight='bold' if silent else 'normal')
        if silent: ax.add_patch(Circle((xk, 0), 1.12, fc='none', ec=RED, lw=1.4))
    ax.set_xlim(-1.3, 11.6); ax.set_ylim(-2.25, 1.2)
    a2 = fig_.add_axes([0.075, 0.10, 0.86, 0.27])
    mus = np.linspace(1.0, 2.0, 801); q = np.array([Q4(m) for m in mus])
    a2.plot(mus, q, color=GOLD_D, lw=2.0); a2.axhline(0, color='#888', lw=0.6)
    a2.scatter([PHI], [0], color=RED, s=40, zorder=3); a2.annotate('Q₄ = 0 only at μ = φ', (PHI, 0), (PHI + 0.06, 0.32), color=RED, fontsize=9, arrowprops=dict(arrowstyle='->', color=RED, lw=0.9))
    for mu, lab in stops:
        a2.axvline(mu, color='#d9d0b8', lw=0.6, zorder=0); a2.text(mu, 0.86, lab.split(chr(10))[0], rotation=90, fontsize=6.5, color='#777', ha='right', va='top')
    a2.set_xlim(0.97, 2.03); a2.set_xlabel('μ  (the slider: μ = 1 + x/(1 + x); a = μ − 1)', fontsize=9); a2.set_ylabel('Q₄', fontsize=9)
    a2.spines['top'].set_visible(False); a2.spines['right'].set_visible(False)
    a = 1 / PHI
    check(f'slider: Q4 vanishes on the slider only at μ = φ (a⁴ − 3a² + 1 = {a ** 4 - 3 * a * a + 1:.2e}); grid minimum at μ = {mus[q.argmin()]:.4f}', abs(mus[q.argmin()] - PHI) < 2e-3 and (q > 1e-3)[np.abs(mus - PHI) > 0.01].all())
    check(f'slider: Q4 of the octahedron {Q4(1.0):.4f} (0.764) and cuboctahedron {Q4(2.0):.4f} (0.191), as #94', abs(Q4(1.0) - 0.7638) < 1e-3 and abs(Q4(2.0) - 0.1909) < 1e-3)
    mark(fig_); save(fig_, 'slider-silent.png')

def cell_A(mu, c=(0, 0, 0)):
    """the power cell of an A site: {|y_i| <= 1, |e.y| <= mu}, e = (±1, ±1, ±1) (#90, Proposition 6), centred at c."""
    A = []; b = []
    for i in range(3):
        for s in (1, -1): n = np.zeros(3); n[i] = s; A.append(n); b.append(1.0)
    for e in itertools.product((1, -1), repeat=3): A.append(np.array(e, float)); b.append(mu)
    return halfspace_vertices(np.array(A), np.array(b)) + np.asarray(c, float)
@fig('partner-fill')
def f_partner():
    mu = PHI; muB = 3 - PHI
    A0 = cell_A(mu); FA = hull_faces(A0)
    fig_, ax = plt.subplots(figsize=(7.2, 6.4)); blank(ax); R = rot(32, 20); sc = Scene(R)
    sc.solid(A0, FA, facecolors=[GOLD if len(f) == 4 else '#e9cf7a' for f, n in FA], lw=1.0)
    volA = ConvexHull(A0).volume; volB = ConvexHull(cell_A(muB)).volume
    for e in itertools.product((1, -1), repeat=3):
        c = np.array(e, float); Bc = cell_A(muB, c * 1.0)
        sc.solid(Bc, offset=c * 0.55, color=VIOLET, glass=True, alpha=0.30, lw=0.8, edge='#4b2f78')
    sc.draw(ax); ax.set_xlim(-3.1, 3.1); ax.set_ylim(-3.0, 3.0)
    check(f'partner fill at x = φ: A cell (Icosaxes, μ = φ) + B cell (Unborn Axes, μ = 3 − φ) volumes {volA:.6f} + {volB:.6f} = 8 = the cell of 2Z³ per A site', abs(volA + volB - 8) < 1e-9)
    check('partner fill: 24 corners each, squares and hexagons', len(A0) == 24 and sorted(len(f) for f, n in FA) == [4] * 6 + [6] * 8)
    mark(fig_); fig_.subplots_adjust(0, 0.05, 1, 1); save(fig_, 'partner-fill.png')

# ---------- Chapter 4
@fig('two-sites')
def f_two():
    fig_, axs = plt.subplots(1, 3, figsize=(12, 4.6)); R = rot(32, 18)
    for ax, d in zip(axs, (-1 / 3, 0.0, 1 / 3)):
        blank(ax); mu = (3 + d) / 2; sc = Scene(R)
        A0 = cell_A(mu); B0 = cell_A(3 - mu, (1, 1, 1))
        sc.solid(A0, color=GOLD, lw=0.9)
        sc.solid(B0, offset=(0.35, 0.35, 0.35), color=VIOLET, glass=True, alpha=0.32, lw=0.8, edge='#4b2f78')
        sc.dot((0, 0, 0), color=GOLD_D, s=18); sc.dot(np.array([1.35, 1.35, 1.35]), color=VIOLET, s=18)
        sc.draw(ax); ax.set_xlim(-2.4, 3.2); ax.set_ylim(-2.6, 3.0)
        g, m = (1 + d) / 2, (1 - d) / 2
        ax.set_title(f'd = {"−1/3" if d < 0 else ("0" if d == 0 else "1/3")}:  gaps g : m : g = {g / m:.3g} : 1 : {g / m:.3g}', fontsize=9.5)
        check(f'two sites at d = {d:+.4f}: A + B volume = 8, A cell corners {len(A0)}', abs(ConvexHull(A0).volume + ConvexHull(B0).volume - 8) < 1e-9 and len(A0) == 24)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.93); save(fig_, 'two-sites.png')
@fig('gap-bars')
def f_gaps():
    fig_, ax = plt.subplots(figsize=(10.5, 4.2))
    stops = [(-1 + 1e-9, 'octahedron'), (-1 / 3, 'DICTO 1:2'), (0, 'Kelvin'), (1 / PHI ** 3, 'golden bond'), (1 / 3, 'DICTO 2:1'), (1 - 1e-9, 'cuboctahedron')]
    ax.plot([-1, 1], [0, 0], color=INK, lw=1.2)
    for d, lab in stops:
        g, m = (1 + d) / 2, (1 - d) / 2; w = 0.28; s = w / (2 * g + m)
        x0 = d - w / 2; y = 0.18
        vals = [0, g, g + m, 2 * g + m]
        for k in range(3):
            ax.add_patch(Rectangle((x0 + vals[k] * s, y), (vals[k + 1] - vals[k]) * s, 0.22, fc=[GOLD, BLUE, GOLD][k], ec=INK, lw=0.6))
        for v in vals: ax.scatter([x0 + v * s], [y + 0.11], s=10, color=INK, zorder=3)
        ax.plot([d, d], [-0.04, 0.04], color=INK, lw=1)
        ax.text(d, -0.1, lab, ha='center', va='top', fontsize=8.5)
        dl = {-1 / 3: '−1/3', 0: '0', 1 / 3: '1/3'}.get(round(d, 12), '1/φ³' if abs(d - PHI ** -3) < 1e-9 else ('−1' if d < 0 else '1'))
        ax.text(d, -0.24, f'd = {dl}', ha='center', va='top', fontsize=8, color='#555')
        check(f'gap bars at {lab}: (g − m)/(g + m) = d', abs((g - m) / (g + m) - d) < 1e-9)
    ax.text(0, 0.62, 'gold: the outer gaps g    blue: the middle gap m    d = (g − m)/(g + m)', ha='center', fontsize=9)
    ax.set_xlim(-1.18, 1.18); ax.set_ylim(-0.42, 0.75); ax.axis('off')
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.98); save(fig_, 'gap-bars.png')

# ---------- Chapter 5
@fig('rd-apart')
def f_rd():
    Bj = json.load(open(os.path.join(HERE, '..', 'data', 'dicto-build-worldpoly.json')))
    LV = np.array([[-0.5,-0.3,0.7],[-1,0.2,0.2],[-0.5,0.7,-0.3],[0.5,0.7,-0.3],[1,0.2,0.2],[0.5,-0.3,0.7],[-0.5,-0.3,-0.3],[0.5,-0.3,-0.3],[0,-0.8,0.2],[0,0.2,-0.8]])
    def q2m(q):
        x, y, z, w = q; n = (x*x+y*y+z*z+w*w) ** .5; x, y, z, w = x/n, y/n, z/n, w/n
        return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
    pieces = [LV @ q2m(n['transform']['quaternion']).T + np.array(n['transform']['position']) for n in Bj['nodes']]
    allp = np.vstack(pieces); c = allp.mean(0); Hf = hull_faces(allp)
    sq = [(f, n) for f, n in Hf if len(f) == 4]
    check(f'RD build: {len(pieces)} Hemi RDs; hull faces {len(Hf)} = 6 squares + 12 hexagons', len(pieces) == 14 and len(sq) == 6 and len(Hf) == 18)
    pyr = []
    for f, n in sq:
        n = np.asarray(n) / np.linalg.norm(n); base = allp[f]; apex = base.mean(0) - 0.5 * n; pyr.append(np.vstack([base, apex]))
    vols = sum(ConvexHull(p).volume for p in pieces) + sum(ConvexHull(p).volume for p in pyr)
    check(f'RD build: 14 pieces + 6 pyramids volume {vols:.6f} = hull volume {ConvexHull(allp).volume:.6f} = 15', abs(vols - 15) < 1e-6 and abs(ConvexHull(allp).volume - 15) < 1e-6)
    fig_, axs = plt.subplots(1, 2, figsize=(11.5, 5.6)); R = rot(35, 24)
    for ax, ex in zip(axs, (0.0, 0.55)):
        blank(ax); sc = Scene(R)
        if ex == 0: sc.solid(allp - c, Hf, color='#e6eef6', glass=True, alpha=0.18, lw=0.9, edge='#5d6f83', shell=True)
        for k, p in enumerate(pieces):
            d = p.mean(0) - c; sc.solid(p - c, color=[GOLD, '#c99a2e', '#e8c45a'][k % 3], lw=0.8, offset=d * ex)
        for p in pyr:
            d = p.mean(0) - c; sc.solid(p - c, color=TEAL, glass=True, alpha=0.55, lw=0.8, edge='#1f5f5b', offset=d * (ex + 0.7 if ex else 0.0))
        sc.draw(ax); ax.set_xlim(-3.4, 3.4); ax.set_ylim(-3.2, 3.2)
    axs[0].set_title('closed: the chamfered cube (crystal shell)', fontsize=10); axs[1].set_title('pulled apart: 14 Hemi RDs (gold), 6 cube pyramids (teal glass)', fontsize=10)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.93); save(fig_, 'rd-apart.png')
@fig('hexagons-two')
def f_hex2():
    fig_, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    # truncated triangle: a face of Kelvin's cell of 1, 2, 4, 5 (gaps 1, 2): values 1, 2, 4 on three places
    vals = (1, 2, 4); P = np.array(perms(vals), float); B = basis_sum0(3); Q = (P - P.mean(0)) @ B.T; Q = Q[sorted(range(6), key=lambda i: math.atan2(Q[i, 1], Q[i, 0]))]
    # elongated hexagon of the chamfered cube: sides 1, √3/2, √3/2 in turn (long sides opposite)
    d1 = np.array([1.0, 0]); a = math.radians(180 - 125.26); s = 3 ** .5 / 2
    # build from edge directions: e (length 1), then two diagonals of length √3/2 turning; close by central symmetry
    ang = math.acos(-1 / 3 ** .5)  # not used for the picture's angles; take the face of Z directly
    G = [np.eye(3)[i] for i in range(3)] + [0.5 * np.array(t) for t in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]]
    pts = np.unique(np.round(np.array([sum(cc * g for cc, g in zip(cs, G)) for cs in itertools.product([0, 1], repeat=7)]), 9), axis=0); pts = pts[sorted(set(ConvexHull(pts).vertices))]
    F = hull_faces(pts); f, n = next((f, n) for f, n in F if len(f) == 6)
    H = pts[f]; n = np.asarray(n) / np.linalg.norm(n); u = H[1] - H[0]; u /= np.linalg.norm(u); v = np.cross(n, u); H2 = np.c_[(H - H.mean(0)) @ u, (H - H.mean(0)) @ v]
    roots = [np.array(r, float) / 2 ** .5 for r in [(1, -1, 0), (1, 0, -1), (0, 1, -1)]]
    for ax, poly, title, red, labs in ((axs[0], Q, 'truncated triangle: every side a swap', True, None), (axs[1], H2, 'elongated hexagon: no side a swap', False, H)):
        blank(ax); ax.add_patch(MPoly(poly, closed=True, fc=IVORY, ec='none'))
        for k in range(6):
            a_, b_ = poly[k], poly[(k + 1) % 6]
            ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=RED if red else GREY, lw=2.6, solid_capstyle='round')
            m = (a_ + b_) / 2; o = m / np.linalg.norm(m)
            ax.text(*(m + o * 0.28 * np.abs(poly).max() / 2), f'{np.linalg.norm(a_ - b_) / (2 ** .5 if red else 1):.3g}' + ('·√2' if red else ''), ha='center', va='center', fontsize=8.5, color=RED if red else '#555')
        lim = np.abs(poly).max() * 1.45; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_title(title, fontsize=10)
    # check: no edge of Z is along a root direction of the 3D permutohedron (the face diagonals (1, −1, 0)/√2 and images)
    E = set()
    for f_, n_ in F:
        for k in range(len(f_)): E.add(tuple(np.round(np.abs(pts[f_[k]] - pts[f_[(k + 1) % len(f_)]]), 6)))
    diag = [np.array(p) for p in itertools.permutations((1, 1, 0))]
    check(f'chamfered cube: edge directions {len(E)} classes up to sign, none parallel to a swap direction (1, ±1, 0)', all(abs(abs(np.dot(np.array(e) / np.linalg.norm(e), d / np.linalg.norm(d))) - 1) > 1e-6 for e in E for d in diag))
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.92); save(fig_, 'hexagons-two.png')

# ---------- Chapter 6
@fig('one-swap')
def f_t1():
    from scipy.spatial import Voronoi
    base = [(x + 0.5 * (y % 2), y * 0.866) for y in range(-3, 4) for x in range(-3, 4)]
    fig_, axs = plt.subplots(1, 3, figsize=(11.5, 4.2))
    names = ['before: A and B touch', 'the moment of the swap', 'after: C and D touch']
    for ax, t, nm in zip(axs, (-1, 0, 1), names):
        blank(ax)
        pts = [p for p in base if not (abs(p[1]) < 1e-9 and p[0] in (0, 1))]
        s = 0.5 + 0.2 * t   # A, B move apart and C, D together as t grows
        A, Bp = (0.5 - s, 0.0), (0.5 + s, 0.0)
        C, Dp = (0.5, 0.866 - 0.366 * (t + 1)), (0.5, -0.866 + 0.366 * (t + 1))
        pts = [p for p in pts if not (abs(p[0] - 0.5) < 1e-9 and abs(abs(p[1]) - 0.866) < 1e-9)] + [A, Bp, C, Dp]
        V = Voronoi(np.array(pts))
        for i, p in enumerate(pts):
            reg = V.regions[V.point_region[i]]
            if -1 in reg or not reg: continue
            poly = V.vertices[reg]
            if np.abs(poly).max() > 2.2: continue
            col = '#f1ece0'; lab = None
            if p == A or p == Bp: col = '#d9c9ef'; lab = 'A' if p == A else 'B'
            if p == C or p == Dp: col = '#f2b3a6'; lab = 'C' if p == C else 'D'
            ax.add_patch(MPoly(poly, closed=True, fc=col, ec=INK, lw=1.0))
            if lab: ax.text(*poly.mean(0), lab, ha='center', va='center', fontsize=12, weight='bold', color=RED if lab in 'CD' else '#4b2f78')
        ax.set_xlim(-1.5, 2.5); ax.set_ylim(-1.7, 1.7); ax.set_title(nm, fontsize=10)
    check('one swap: three frames drawn', True)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.92); save(fig_, 'one-swap.png')

# ---------- Chapter 7
@fig('square-hexagon')
def f_rules():
    fig_, axs = plt.subplots(1, 2, figsize=(10.5, 4.6))
    def ap(r, v1, v2): return tuple(v2 if x == v1 else v1 if x == v2 else x for x in r)
    # square: two far-apart swaps 1↔2 and 4↔5 commute
    r0 = (1, 2, 3, 4, 5); sqr = [r0, ap(r0, 1, 2), ap(ap(r0, 1, 2), 4, 5), ap(r0, 4, 5)]
    Q = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]]) * 1.3
    ax = axs[0]; blank(ax); ax.add_patch(MPoly(Q, closed=True, fc=IVORY, ec='none'))
    for k in range(4):
        a, b = Q[k], Q[(k + 1) % 4]; pair = sorted(set(x for x, y in zip(sqr[k], sqr[(k + 1) % 4]) if x != y))
        ax.plot([a[0], b[0]], [a[1], b[1]], color=RED if pair == [1, 2] else INK, lw=2.4); m = (a + b) / 2
        ax.text(m[0] * 1.32, m[1] * 1.32, f'{pair[0]}↔{pair[1]}', ha='center', va='center', fontsize=10, color=RED if pair == [1, 2] else INK)
    for k in range(4): ax.text(Q[k, 0] * 1.18, Q[k, 1] * 1.18 + (0.18 if Q[k, 1] > 0 else -0.18), ''.join(map(str, sqr[k])), ha='center', fontsize=10, family='DejaVu Sans Mono')
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.4, 2.4); ax.set_title('a square: swaps of far-apart values commute', fontsize=10)
    check('square: 1↔2 then 4↔5 equals 4↔5 then 1↔2', ap(ap(r0, 1, 2), 4, 5) == ap(ap(r0, 4, 5), 1, 2))
    # hexagon: 1↔2, 2↔3 alternate; three values cycle
    hexr = [r0]
    for k in range(5): hexr.append(ap(hexr[-1], *((1, 2) if k % 2 == 0 else (2, 3))))
    Qh = np.array([[math.cos(math.pi / 2 + k * math.pi / 3), math.sin(math.pi / 2 + k * math.pi / 3)] for k in range(6)]) * 1.6
    ax = axs[1]; blank(ax); ax.add_patch(MPoly(Qh, closed=True, fc=IVORY, ec='none'))
    for k in range(6):
        a, b = Qh[k], Qh[(k + 1) % 6]; pair = sorted(set(x for x, y in zip(hexr[k], hexr[(k + 1) % 6]) if x != y))
        ax.plot([a[0], b[0]], [a[1], b[1]], color=RED if pair == [1, 2] else INK, lw=2.4); m = (a + b) / 2
        ax.text(m[0] * 1.25, m[1] * 1.25, f'{pair[0]}↔{pair[1]}', ha='center', va='center', fontsize=10, color=RED if pair == [1, 2] else INK)
    for k in range(6): ax.text(Qh[k, 0] * 1.2, Qh[k, 1] * 1.2, ''.join(map(str, hexr[k])), ha='center', va='center', fontsize=10, family='DejaVu Sans Mono')
    ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.4, 2.4); ax.set_title('a hexagon: three values cycle (braid relation)', fontsize=10)
    check('hexagon: six alternate swaps 1↔2, 2↔3 return to the start', ap(hexr[-1], 2, 3) == r0)
    mark(fig_); fig_.subplots_adjust(0.01, 0.06, 0.99, 0.92); save(fig_, 'square-hexagon.png')

def perm4d():
    Pl = perms((1, 2, 3, 4, 5)); P = np.array(Pl, float) - 3.0; return Pl, P, perm_edges(Pl)
def slice_center(normal):
    """the central slice of the 4D permutohedron with the given normal (in R^5, sum 0): corners in 3D, and which of its faces are 2-faces of the solid."""
    Pl, P, E = perm4d(); c = np.asarray(normal, float); Bp = basis_perp(5, [c])
    pts = []
    for i in range(len(P)):
        if abs(P[i] @ c) < 1e-9: pts.append(P[i])
    for i, j, k in E:
        a, b = P[i] @ c, P[j] @ c
        if a * b < -1e-12: pts.append(P[i] + (P[j] - P[i]) * a / (a - b))
    pts = np.array(pts); X = pts @ Bp.T; F = hull_faces(X)
    FAC = facets5()   # a face of the slice is a 2-face of the solid when it lies on two cells of the solid
    solidface = [sum(1 for S, nn, rhs in FAC if np.all(np.abs(pts[f] @ nn - rhs) < 1e-7)) >= 2 for f, n in F]
    return X, F, solidface
@fig('four-slices')
def f_cards():
    kinds = [((8, -7, -7, 3, 3), '30 slices, split (1, 2, 2)'), ((6, -9, 1, 1, 1), '20 slices, split (1, 1, 3)'), ((3, -2, -2, -2, 3), '10 slices, split (1, 3, 1)'), ((1, 1, -4, 1, 1), '5 slices: the DICTO 1:2, the heart')]
    want = [(32, 52, 22), (24, 36, 14), (24, 42, 20), (24, 36, 14)]
    fig_, axs = plt.subplots(1, 4, figsize=(13, 4.0)); R = rot(30, 20)
    for ax, (c, lab), w in zip(axs, kinds, want):
        blank(ax); X, F, sf = slice_center(c)
        nE = sum(len(f) for f, n in F) // 2
        check(f'slice {lab}: {len(X)} corners, {nE} edges, {len(F)} faces; faces of the solid on it {sum(sf)}', (len(X), nE, len(F)) == w and sum(sf) == (6 if '1:2' in lab else 2))
        sc = Scene(R); sc.solid(X, F, facecolors=[GOLD if s else '#cfe0f3' for s in sf], lw=0.8)
        sc.draw(ax); m = np.abs(X).max() * 1.15; ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_title(lab, fontsize=9)
    fig_.text(0.5, 0.075, 'gold: 2-faces of the 4D permutohedron that lie in the slice (2, 2, 2 and 6 of them)', ha='center', fontsize=8.5, color='#555')
    mark(fig_); fig_.subplots_adjust(0.01, 0.1, 0.99, 0.92); save(fig_, 'four-slices.png')

exec(open(os.path.join(HERE, 'figs_book2.py'), encoding='utf8').read())

PILOT = ['bells-hexagon', 'kelvin-swaps', 'four-slices']
if __name__ == '__main__':
    args = sys.argv[1:] or ['pilot']
    names = PILOT if args == ['pilot'] else (list(FIGS) if args == ['all'] else args)
    for k, nm in enumerate(names):
        print(f'PROGRESS {k}/{len(names)} {nm}', flush=True)
        try: FIGS[nm]()
        except Exception as ex:
            import traceback; traceback.print_exc(); check(f'{nm} raised {ex!r}', False)
    print(f'PROGRESS {len(names)}/{len(names)} done')
    print('FINAL ok' if OK[0] else 'FINAL FAIL')
