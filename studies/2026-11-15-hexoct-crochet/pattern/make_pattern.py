#!/usr/bin/env python3
"""Figures, core templates (SVG in millimetres, true scale) and checks for the HexOct crochet pattern.
Usage: python3 make_pattern.py <hex scripts folder (tiles.py, stackings.py)> <dicto-mark.png>   (run in pattern/; reads ../data/pattern.json)
Writes fig/*.png, nets/*.svg, data/pattern-checks.json; prints FINAL OK when every check passes."""
import os, sys, math, json, itertools, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.optimize import linprog
from geom import *
HEX, MARK = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs('fig', exist_ok=True); os.makedirs('nets', exist_ok=True); os.makedirs('data', exist_ok=True)
pat = json.load(open('../data/pattern.json')); L = pat['L_cm']; GS = pat['gauge']['sts_per_10cm']/10; GR = pat['gauge']['rows_per_10cm']/10
INK, GOLD, PURPLE = '#222222', '#d4a020', '#7a5fb0'
C_SQ, C_HX, C_TR = '#c9b8e8', '#f0d27a', '#a9d8cf'; C_INC, C_D2, C_D3 = '#7cc47c', '#f2a65a', '#e0605a'
chk = {'ok': []}
def ok(name, cond, **kw): chk[name] = dict(ok=bool(cond), **kw); chk['ok'].append(bool(cond))
def mark(fig):
    a = fig.add_axes([0.9, 0.0, 0.09, 0.09]); a.imshow(plt.imread(MARK)); a.axis('off')
# ---------------- row-by-row counts (from data/pattern.json) and the side-length check ----------------
sq_rows = [pat['square']['sts']]*pat['square']['rows']
hx = pat['hexagon']; hx_rows = []; n = hx['bottom_sts']
for r in range(1, hx['total_rows'] + 1):
    if r in hx['increase_rows']: n += 2
    if r in hx['decrease_rows']: n -= 2
    hx_rows.append(n)
tr = pat['triangle']; tr_rows = [tr['first_row_sts']]
for d in tr['decrease_schedule']: tr_rows.append(tr_rows[-1] - d)
ok('row counts', hx_rows[0] == 14 and max(hx_rows) == 28 and hx_rows == hx_rows[::-1] and tr_rows[-1] == 1, square=sq_rows[0], hexagon=hx_rows, triangle=tr_rows)
t_true = L*H; p_true = L/s3
got = {'square: stitch edge': sq_rows[0]/GS, 'square: row edge': len(sq_rows)/GR,
       'hexagon: bottom and top': hx_rows[0]/GS, 'hexagon: slanted sides': math.hypot((max(hx_rows) - hx_rows[0])/2/GS, len(hx_rows)/2/GR),
       'triangle: long leg': tr_rows[0]/GS, 'triangle: short leg': len(tr_rows)/GR, 'triangle: hypotenuse': math.hypot(tr_rows[0]/GS, len(tr_rows)/GR)}
true = {'square: stitch edge': L, 'square: row edge': L, 'hexagon: bottom and top': t_true, 'hexagon: slanted sides': t_true,
        'triangle: long leg': t_true, 'triangle: short leg': p_true, 'triangle: hypotenuse': L}
sides = {k: {'true_cm': round(true[k], 3), 'from_stitches_cm': round(got[k], 3), 'error_pct': round(100*(got[k]/true[k] - 1), 2)} for k in true}
ok('side lengths within 1 %', max(abs(v['error_pct']) for v in sides.values()) < 1, sides=sides)
# ---------------- stitch charts ----------------
def chart(rows, align, fname, title, edge_notes, color, inc_rows=(), d2=(), d3=(), dec_side=None):
    w, h = max(rows)/GS, len(rows)/GR
    fig, ax = plt.subplots(figsize=(6.4, 6.4*min(1.15, (h + 3)/(w + 6))), dpi=220)
    for i, n in enumerate(rows):
        r = i + 1; start_right = (r % 2 == 1)
        x0 = {'left': 0, 'right': max(rows) - n, 'centre': (max(rows) - n)/2}[align]
        for k in range(n):
            c = color; sym = ''
            if r in inc_rows and k in (0, n - 1): c, sym = C_INC, '+'
            if r in d2 and ((k == 0) if dec_side in ('left', 'both') else False or (dec_side == 'both' and k == n - 1)): c, sym = C_D2, '2'
            if r in d2 and dec_side == 'both' and k == n - 1: c, sym = C_D2, '2'
            if r in d3 and k == 0: c, sym = C_D3, '3'
            ax.add_patch(Rectangle(((x0 + k)/GS, i/GR), 1/GS, 1/GR, fc=c, ec='#666', lw=0.35))
            if sym: ax.text((x0 + k + 0.5)/GS, (i + 0.5)/GR, sym, ha='center', va='center', fontsize=5.2, weight='bold')
        xs = (x0 + n)/GS + 0.15 if start_right else x0/GS - 0.15
        ax.text(xs, (i + 0.5)/GR, f"{r}", ha='left' if start_right else 'right', va='center', fontsize=5.2, color='#333')
        xe = x0/GS - 0.15 if start_right else (x0 + n)/GS + 0.15
        ax.text(xe, (i + 0.5)/GR, f"({n})", ha='right' if start_right else 'left', va='center', fontsize=4.6, color='#777')
    for (xy, s, kw) in edge_notes: ax.text(*xy, s, fontsize=6.4, **kw)
    ax.set_aspect('equal'); ax.set_xlim(-2.8, w + 2.8); ax.set_ylim(-2.4, h + 0.6); ax.axis('off')
    ax.set_title(title, fontsize=8.5)
    lg = [(color, '', '1 sc'), (C_INC, '+', '2 sc in this st'), (C_D2, '2', 'sc2tog'), (C_D3, '3', 'sc3tog')]
    used = [lg[0]] + ([lg[1]] if inc_rows else []) + ([lg[2]] if d2 else []) + ([lg[3]] if d3 else [])
    for j, (c, s, t) in enumerate(used):
        X0 = 0.0 + j*3.1; ax.add_patch(Rectangle((X0, -1.45), 1/GS, 1/GR, fc=c, ec='#666', lw=0.35)); ax.text(X0 + 0.28, -1.2, s, ha='center', va='center', fontsize=5.2, weight='bold')
        ax.text(X0 + 0.75, -1.2, t, va='center', fontsize=5.6)
    ax.text(0, -2.05, 'Row numbers sit on the side where the row starts; (n) = stitches in the row. Every row from row 2 starts ch 1, turn (not counted).', ha='left', va='center', fontsize=5.2, color='#444')
    mark(fig); fig.savefig('fig/' + fname, bbox_inches='tight', pad_inches=0.08); plt.close(fig)
w = sq_rows[0]/GS; hgt = len(sq_rows)/GR
chart(sq_rows, 'left', 'chart-square.png', f"Square: ch {sq_rows[0] + 1}, then {len(sq_rows)} rows of {sq_rows[0]} sc  ({w:.2f} × {hgt:.2f} cm at gauge; true 9.50 × 9.50)",
      [((w/2, -0.45), f'foundation chain: ch {sq_rows[0] + 1}', dict(ha='center', va='center', color='#444'))], C_SQ)
w = max(hx_rows)/GS; hgt = len(hx_rows)/GR
chart(hx_rows, 'centre', 'chart-hexagon.png', f"Hexagon: ch {hx_rows[0] + 1}; 27 rows, {hx_rows[0]} → {max(hx_rows)} → {hx_rows[-1]} sc  (each side {got['hexagon: bottom and top']:.2f} / {got['hexagon: slanted sides']:.2f} cm; true {t_true:.2f})",
      [((w/2, -0.45), f'foundation chain: ch {hx_rows[0] + 1}', dict(ha='center', va='center', color='#444'))], C_HX, inc_rows=hx['increase_rows'], d2=hx['decrease_rows'], dec_side='both')
w = tr_rows[0]/GS; hgt = len(tr_rows)/GR
d2r = [i + 2 for i, d in enumerate(tr['decrease_schedule']) if d == 1]; d3r = [i + 2 for i, d in enumerate(tr['decrease_schedule']) if d == 2]
chart(tr_rows, 'right', 'chart-triangle.png', f"Right triangle (make 6): ch {tr_rows[0] + 1}; 11 rows, {tr_rows[0]} → 1 sc",
      [((w/2, -0.45), f'long leg = foundation edge, ch {tr_rows[0] + 1}: {got["triangle: long leg"]:.2f} cm (true {t_true:.2f}); sews to the hexagon', dict(ha='center', va='center', color='#444')),
       ((w + 0.75, hgt/2), f'short leg\n(straight edge,\nmarked st)\n{got["triangle: short leg"]:.2f} cm\n(true {p_true:.2f})\nsews to the\nnext triangle', dict(ha='left', va='center', color='#444')),
       ((w*0.28, hgt*0.62), f'hypotenuse\n{got["triangle: hypotenuse"]:.2f} cm (true {L:.2f})\nsews to a square', dict(ha='center', va='center', color='#444', rotation=math.degrees(math.atan2(hgt, w))))],
      C_TR, d2=d2r, d3=d3r, dec_side='left')
# ---------------- the solids, edge letters ----------------
SC = L*math.sqrt(2)   # cm per ball spacing
FN, NN = solid(XN); labN, EN = label_edges(XN, FN, NN)
FC, NC = solid(XC); labC, EC = label_edges(XC, FC, NC)
kinds = sorted(kind(f) for f in FN); ok('Narcissus faces', kinds.count('square') == 3 and kinds.count('hexagon') == 1 and kinds.count('triangle') == 6 and len(EN) == 18 and len(XN) == 10)
dih = {l: round(dihedral(NN, *EN[e]), 2) for e, l in labN.items()}
lens = {l: round(float(np.linalg.norm(XN[list(e)[0]] - XN[list(e)[1]])*SC), 3) for e, l in labN.items()}
ok('Narcissus edges and folds', set(dih.values()) == {90.0, 120.0, 135.0}, dihedral_deg=dih, length_cm=lens)
# triangle hands: chart side out iff, seen from outside with the long leg at the bottom, the right angle is on the right
def hand(f):
    P = XN[f]; ln = [np.linalg.norm(P[k] - P[(k+1) % 3]) for k in range(3)]
    # right-angle corner: opposite the hypotenuse (longest side)
    k = int(np.argmax(ln)); Q_, R_ = f[k], f[(k+1) % 3]; Pr = f[(k+2) % 3]
    a, b = (Q_, R_) if np.linalg.norm(XN[Q_] - XN[Pr]) > np.linalg.norm(XN[R_] - XN[Pr]) else (R_, Q_)   # a: far end of the long leg, b: end of short leg
    n_ = NN[FN.index(f)]; return 'chart side out' if np.cross(XN[Pr] - XN[a], XN[b] - XN[a]) @ n_ > 0 else 'chart side in'
hands = {i: hand(f) for i, f in enumerate(FN) if len(f) == 3}
ok('triangle hands alternate', list(hands.values()).count('chart side out') == 3)
def net_fig(X, F, N, lab, E, fname, title, names, scale, comps):
    """net drawn from outside, as separate pieces comps = [(root, tree edges)], every edge lettered; for the crochet assembly"""
    P = {}; xoff = 0.0; T = []
    for root, Tr in comps:
        faces = sorted({root} | {x for t in Tr for x in t}); Q = unfold(X*scale, F, N, faces, Tr, root)
        a, b = Q[root][0], Q[root][1]; t = -math.atan2(*(b - a)[::-1]); R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
        Q = {i: q @ R.T for i, q in Q.items()}; A = np.vstack(list(Q.values()))
        Q = {i: q - A.min(0) + np.array([xoff, 0]) for i, q in Q.items()}; xoff += np.ptp(A[:, 0]) + 0.12*scale
        P.update(Q); T += list(Tr)
    assert overlap(P) < 1e-9 and len(P) == len(F)
    fig, ax = plt.subplots(figsize=(6.4, 6.4), dpi=220)
    tree = {frozenset(t) for t in T}
    for i, Q in P.items():
        col = {3: C_TR, 4: C_SQ, 6: C_HX}[len(Q)]; ax.add_patch(MPoly(Q, closed=True, fc=col, ec=INK, lw=0.9))
        ax.text(*Q.mean(0), names[i], ha='center', va='center', fontsize=6.5 if len(Q) > 3 else 5.2)
        f = F[i]
        for k in range(len(f)):
            e = frozenset((f[k], f[(k+1) % len(f)])); a, b = Q[k], Q[(k+1) % len(f)]; m = (a + b)/2; c = Q.mean(0)
            inner = frozenset(E[e]) in tree
            pos = m + (c - m)/np.linalg.norm(c - m)*(0.0 if inner else (0.03 if len(f) == 3 else 0.045)*scale)
            ax.text(*pos, lab[e], ha='center', va='center', fontsize=7.5, weight='bold', color='#b00000' if not inner else '#003c8f',
                    bbox=dict(boxstyle='circle,pad=0.12', fc='white', ec='none', alpha=0.85) if inner else None)
            if inner: ax.plot(*zip(a, b), color='#003c8f', lw=1.6, ls=(0, (3, 2)))
        if len(f) == 3:   # right-angle mark
            ln = [np.linalg.norm(Q[k] - Q[(k+1) % 3]) for k in range(3)]; kk = int(np.argmax(ln)); r = Q[(kk + 2) % 3]
            u1 = (Q[kk] - r)/np.linalg.norm(Q[kk] - r); u2 = (Q[(kk+1) % 3] - r)/np.linalg.norm(Q[(kk+1) % 3] - r); s_ = 0.06*scale
            ax.plot(*zip(r + u1*s_, r + (u1 + u2)*s_, r + u2*s_), color=INK, lw=0.7)
    A = np.vstack(list(P.values())); ax.set_xlim(A[:, 0].min() - 0.5, A[:, 0].max() + 0.5); ax.set_ylim(A[:, 1].min() - 0.5, A[:, 1].max() + 0.5)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=8.5); mark(fig)
    fig.savefig('fig/' + fname, bbox_inches='tight', pad_inches=0.08); plt.close(fig)
namesN = {}; ct = {'square': 0, 'triangle': 0}
for i, f in enumerate(FN):
    k = kind(f)
    if k == 'hexagon': namesN[i] = 'hexagon'
    else: ct[k] += 1; namesN[i] = f"square {ct[k]}" if k == 'square' else f"T{ct[k]}\n{hands[i].split()[-1]}"
hxN = next(i for i, f in enumerate(FN) if len(f) == 6); sqN = sorted(i for i, f in enumerate(FN) if len(f) == 4)
cupT = [tuple(EN[e]) for e, l in labN.items() if l in 'ABCDEF']; lidT = [tuple(EN[e]) for e, l in labN.items() if l in 'JK']
ok('assembly groups', len(cupT) == 6 and len(lidT) == 2 and all(set(t) <= set(sqN) for t in lidT))
net_fig(XN, FN, NN, labN, EN, 'assembly-narcissus.png', 'Narcissus, seen from outside: the cup (hexagon and 6 triangles) and the lid (3 squares).\nBlue dashed letters = seams sewn flat; red letters = edges that meet the same red letter', namesN, SC,
        [(hxN, cupT), (sqN[0], lidT)])
namesC = {i: f"square {i + 1}" for i in range(6)}; bot = int(np.argmin(NC[:, 2])); top = int(np.argmax(NC[:, 2])); namesC[bot] = 'square 1\n(bottom)'; namesC[top] = 'square 6\n(top, last)'
k_ = 2
for i in range(6):
    if i not in (bot, top): namesC[i] = f"square {k_}"; k_ += 1
net_fig(XC, FC, NC, labC, EC, 'assembly-cube.png', 'Cube, seen from outside: blue dashed letters = seams sewn flat;\nred letters = edges that meet the same red letter', namesC, SC, [(bot, [(bot, i) for i in range(6) if i not in (bot, top)] + [(next(i for i in range(6) if i not in (bot, top) and any(set(fs) == {i, top} for fs in EC.values())), top)])])
# ---------------- cores ----------------
CORE = 0.91/0.95*0 + (L - 0.4)/L   # cube core side L - 4 mm: every face 2 mm inside the true face
def cheb(X, F, N):
    A = N; b = np.array([N[i] @ X[F[i][0]] for i in range(len(F))])
    res = linprog([0, 0, 0, -1], A_ub=np.hstack([A, np.ones((len(F), 1))]), b_ub=b, bounds=[(None, None)]*3 + [(0, None)])
    c = res.x[:3]; return c, b - A @ c
cN, dN = cheb(XN, FN, NN); insetN = dN*SC*10*(1 - CORE)
ok('cores', True, scale=round(CORE, 4), cube_core_side_mm=round(L*10*CORE, 1), narcissus_inset_mm=[round(float(insetN.min()), 2), round(float(insetN.max()), 2)],
   narcissus_core_edges_mm={'square': round(L*10*CORE, 1), 'hexagon': round(t_true*10*CORE, 1), 'triangle short leg': round(p_true*10*CORE, 1), 'triangle long leg': round(t_true*10*CORE, 1), 'triangle hypotenuse': round(L*10*CORE, 1)})
SW, SH = 178.0, 236.0   # svg box (mm) inside the 180 mm text column
sol, fits = split_net(XN, FN, NN, SW - 6, SH - 6, SC*10*CORE)
ok('Narcissus core net pieces', sum(len(p) for p in sol) == 10, pieces=[sorted(namesN[i].split('\n')[0] for i in p) for p in sol])
def svg_piece(X, F, N, lab, E, faces, T, polys, angle, fname, title_txt, names, folds_extra=None):
    t = math.radians(angle); R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
    Pp = {i: Q @ R.T for i, Q in polys.items()}; A = np.vstack(list(Pp.values())); lo, hi = A.min(0), A.max(0)
    W, Hh = hi - lo + 6
    def tr_(p): return (p[0] - lo[0] + 3, hi[1] - p[1] + 3)   # flip y: SVG y runs down; keeps the outside view unmirrored
    tree = {frozenset(x) for x in T}; out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{Hh:.2f}mm" viewBox="0 0 {W:.3f} {Hh:.3f}" font-family="Helvetica, Arial, sans-serif">']
    for i, Q in Pp.items():
        col = {3: C_TR, 4: C_SQ, 6: C_HX}[len(Q)]
        out.append('<polygon points="' + ' '.join('%.3f,%.3f' % tr_(p) for p in Q) + f'" fill="{col}" fill-opacity="0.35" stroke="none"/>')
    done = set()
    for i, Q in Pp.items():
        f = F[i]; c = Q.mean(0)
        x, y = tr_(c); out.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="3.6" text-anchor="middle" fill="#555">{names[i].split(chr(10))[0]}</text>')
        for k in range(len(f)):
            e = frozenset((f[k], f[(k+1) % len(f)])); a, b = Q[k], Q[(k+1) % len(f)]
            fold = frozenset(E[e]) in tree
            if e not in done:
                done.add(e); (x1, y1), (x2, y2) = tr_(a), tr_(b)
                out.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{"#1d4fa0" if fold else "#000"}" stroke-width="0.3"' + (' stroke-dasharray="2.5,1.5"' if fold else '') + '/>')
            m = (a + b)/2; pos = m + (c - m)*(0.13 if not fold else 0.0) * (60/np.linalg.norm(c - m)) * 0.12
            pos = m + (c - m)/np.linalg.norm(c - m)*(5.0 if not fold else 4.0)
            x, y = tr_(pos); ang = -math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            if ang > 90: ang -= 180
            if ang < -90: ang += 180
            txt = lab[e] + (f' fold {dihedral(N, *E[e]):.0f}°' if fold else '')
            if fold and i != min(E[e]): continue
            out.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{3.0 if fold else 4.2}" font-weight="bold" text-anchor="middle" dominant-baseline="middle" fill="{"#1d4fa0" if fold else "#b00000"}" transform="rotate({ang:.1f} {x:.2f} {y:.2f})">{txt}</text>')
    out.append('</svg>'); open('nets/' + fname, 'w').write('\n'.join(out))
    return float(W), float(Hh)
core_pages = []
for n_, p in enumerate(sol):
    area, ang, T, P = fits[p]
    Wd, Hd = svg_piece(XN, FN, NN, labN, EN, p, T, P, ang, f'core-narcissus-{n_ + 1}.svg', '', namesN)
    lens_ok = all(abs(np.linalg.norm(P[i][k] - P[i][(k+1) % len(FN[i])]) - np.linalg.norm(XN[FN[i][k]] - XN[FN[i][(k+1) % len(FN[i])]])*SC*10*CORE) < 1e-3 for i in P for k in range(len(FN[i])))
    core_pages.append({'file': f'core-narcissus-{n_ + 1}.svg', 'faces': [namesN[i].split('\n')[0] for i in p], 'w_mm': round(Wd, 1), 'h_mm': round(Hd, 1), 'true_lengths': lens_ok,
                       'cut_edges': sorted({labN[e] for e in EN if set(EN[e]) & set(p) and frozenset(EN[e]) not in {frozenset(x) for x in T}}),
                       'fold_edges': sorted(labN[e] for e in EN if frozenset(EN[e]) in {frozenset(x) for x in T})})
ok('core pieces at true size, in the column', all(c['true_lengths'] and c['w_mm'] <= 180 and c['h_mm'] <= 240 for c in core_pages), pieces=core_pages)
# cube core: one strip of two squares (cut 3); strips = (bottom, side), (side, side), (top, side)
sides = [i for i in range(6) if i not in (bot, top)]
def adj(a, b): return any(set(fs) == {a, b} for fs in EC.values())
strips = None
for s0 in sides:
    rest = [s for s in sides if s != s0]
    for s3_ in rest:
        mid = [s for s in rest if s != s3_]
        if adj(bot, s0) and adj(top, s3_) and adj(*mid): strips = [(bot, s0), tuple(mid), (top, s3_)]; break
    if strips: break
T1 = [strips[0]]; P1 = unfold(XC*SC*10*CORE, FC, NC, strips[0], T1, strips[0][0])
Wc, Hc = svg_piece(XC, FC, NC, {e: '' for e in labC}, EC, strips[0], T1, P1, best_rotation(P1, 100, 236)[1], 'core-cube-strip.svg', '', {i: '' for i in range(6)})
ok('cube core strip', Wc <= 180 and Hc <= 240, w_mm=round(Wc, 1), h_mm=round(Hc, 1), strips=[[namesC[i].split('\n')[0] for i in s] for s in strips])
# small cube diagram: which strip is which, edge letters
fig, ax = plt.subplots(figsize=(3.0, 3.6), dpi=220)
Tc = [(bot, s) for s in sides] + [(strips[2][1], top)]
Pc = unfold(XC, FC, NC, range(6), Tc, bot)
scol = {}
for k, s in enumerate(strips):
    for i in s: scol[i] = (['#f4c96b', '#a8d8cf', '#c9b8e8'][k], k + 1)
for i, Q in Pc.items():
    ax.add_patch(MPoly(Q, closed=True, fc=scol[i][0], ec=INK, lw=0.8)); ax.text(*Q.mean(0), f"{namesC[i].split(chr(10))[0]}\nstrip {scol[i][1]}", ha='center', va='center', fontsize=5.5)
    f = FC[i]
    for k in range(4):
        e = frozenset((f[k], f[(k+1) % 4])); m = (Q[k] + Q[(k+1) % 4])/2; c = Q.mean(0)
        ax.text(*(m + (c - m)*0.2), labC[e], ha='center', va='center', fontsize=6.5, weight='bold', color='#b00000')
A = np.vstack(list(Pc.values())); ax.set_xlim(A[:, 0].min() - .05, A[:, 0].max() + .05); ax.set_ylim(A[:, 1].min() - .05, A[:, 1].max() + .05); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Cube core: three strips,\nedge letters as on the crochet cube', fontsize=7); mark(fig); fig.savefig('fig/cube-strips.png', bbox_inches='tight', pad_inches=0.06); plt.close(fig)
# ---------------- 3D: twisted cube, test piece ----------------
sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as Tt
from stackings import POS
os.chdir(here)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*s3/2, float(p[2])*H])
w4 = 'ABCB'; types = Tt.types(w4); pieces = []
for Lr in range(2):
    os.chdir(HEX); pcs, _ = Tt.tile(w4, Lr, Fr(3, 8)); os.chdir(here)
    ball = cart((*POS[w4[Lr]], Lr))
    for k, up, s_, P, J in pcs:
        X0 = np.unique(np.round(np.array([cart(p) for p in P]), 12), axis=0) + ball
        for i, j in itertools.product(range(-1, 3), repeat=2): pieces.append((Lr, X0 + cart((i, j, 0))))
def vs(X): return {tuple(np.round(p, 6)) for p in X}
nar = [X for Lr, X in pieces if Lr == 0 and len(X) == 10]; cub = [X for Lr, X in pieces if Lr == 1 and len(X) == 8]
pair = next((A_, B_) for A_, B_ in itertools.combinations(nar, 2) if len(vs(A_) & vs(B_)) == 6)
U = np.vstack(pair); hU = ConvexHull(U); FU, _ = solid(np.unique(np.round(U, 9), axis=0))
ok('twisted cube', abs(hU.volume - ConvexHull(pair[0]).volume - ConvexHull(pair[1]).volume) < 1e-9 and len(FU) == 12, faces=len(FU))
best = None
for A_, B_ in itertools.combinations(cub, 2):
    if len(vs(A_) & vs(B_)) != 4: continue
    cont = sum(len(vs(C_) & vs(Nn)) == 4 for C_ in (A_, B_) for Nn in pair)
    if best is None or cont > best[0]: best = (cont, (A_, B_))
ok('test piece contacts', best[0] >= 1, square_contacts_between_units=best[0])
light = np.array([.4, -.5, .8]); light /= np.linalg.norm(light)
def draw(ax, X, col, off):
    F_, N_ = solid(X); Y = X + off
    for f, n_ in zip(F_, N_):
        ax.add_collection3d(Poly3DCollection([Y[f]], facecolors=[np.clip(np.array(matplotlib.colors.to_rgb(col))*(0.55 + 0.45*max(0, n_ @ light)), 0, 1)], edgecolors=INK, linewidths=0.5))
def save3d(fig, name):
    fig.savefig('fig/_raw.png', dpi=220); img = plt.imread('fig/_raw.png'); plt.close(fig)
    ink = np.where(img[..., :3].min(2) < 0.97); y0, y1, x0, x1 = ink[0].min(), ink[0].max(), ink[1].min(), ink[1].max()
    img = img[max(0, y0 - 14):y1 + 14, max(0, x0 - 14):x1 + 14]; hh, ww = img.shape[:2]
    f2 = plt.figure(figsize=(ww/220, hh/220 + 0.3), dpi=220); a = f2.add_axes([0, 0.3/(hh/220 + 0.3), 1, (hh/220)/(hh/220 + 0.3)]); a.imshow(img); a.axis('off'); mark(f2)
    f2.savefig('fig/' + name, dpi=220); plt.close(f2); os.remove('fig/_raw.png')
cen = U.mean(0); nh = None
F0, N0 = solid(pair[0]); hxi = next(i for i, f in enumerate(F0) if len(f) == 6); nh = N0[hxi]
fig = plt.figure(figsize=(7.2, 3.6)); 
for k, gap in enumerate((0.6, 0.0)):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d')
    draw(ax, pair[0] - cen, GOLD, nh*gap); draw(ax, pair[1] - cen, '#e8c25a', -nh*gap)
    r = 0.95; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.view_init(18, -55); ax.set_axis_off()
    ax.set_title(['two Narcissus, hexagon to hexagon', 'sewn together: the twisted cube'][k], fontsize=8)
save3d(fig, 'twisted-cube.png')
fig = plt.figure(figsize=(4.4, 4.8)); ax = fig.add_subplot(projection='3d'); c2 = np.vstack(list(pair) + list(best[1])).mean(0)
for X in pair: draw(ax, X - c2, GOLD, np.array([0, 0, -0.25]))
for X in best[1]: draw(ax, X - c2, PURPLE, np.array([0, 0, 0.25]))
r = 1.1; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.view_init(14, -60); ax.set_axis_off()
ax.set_title('Test piece 1, drawn apart: two cubes (c layer, purple)\nover two Narcissus (h layer, gold)', fontsize=8)
save3d(fig, 'test-piece.png')
json.dump(chk, open('data/pattern-checks.json', 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in chk.items() if k != 'ok'}, indent=1, default=float)[:6000])
print('FINAL', 'OK' if all(chk['ok']) else 'CHECK')
