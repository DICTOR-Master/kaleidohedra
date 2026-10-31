#!/usr/bin/env python3
"""HexOct as a knitted pattern: exact slice of the 4H stacking + knitting chart (31 Oct 2026).

Close packing, ball spacing a = 1, layers stacked along z, layer spacing h = sqrt(2/3).
Exact integer coordinates: x = X/2, y = Y*sqrt(3)/6, z = Z*h.  A sites (X,Y) = (2m+n, 3n), B = A + (1,1), C = A + (2,2).
Slice plane x = 0 (a {11-20} plane: normal along a close-packed row, contains the stacking axis and [1-100]).
Lateral slice coordinate s = -y, i.e. S = -Y in units sqrt(3)/6; repeat = sqrt(3) (S = 6); A at 0, B at 1/3, C at 2/3.
Pieces: classical Delaunay cells of the close packing (= HexOct pieces at lambda = -1/8): up-tetrahedra, down-tetrahedra,
octahedra in every gap; each cut at the gap mid-plane (Rule of Halves) into a lower half (layer below) and an upper half.
All slice polygons are computed exactly with Fractions in (S, Z); drawing converts to true lengths.

Usage (dicto-big-brother): LOGO=~/kres-tmp/dicto-logo.png ~/geom/bin/python knit.py  -> ../out/slice-4H.png, chart-4H.png, slice-4H.json
"""
import os, json, math, itertools
from fractions import Fraction as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '../out')
LOGO = os.environ.get('LOGO', os.path.join(HERE, '../../../papers/dicto-logo.png'))

SEQ = 'ABCBABCBA'                 # 4H, two periods, layers 0..8
OFF = {'A': (0, 0), 'B': (1, 1), 'C': (2, 2)}
SOFF = {'A': 0, 'B': 2, 'C': 4}   # lateral offset on the slice, in S units (repeat 6)
REP = 6
NREP = 2
SQ3_6 = math.sqrt(3) / 6
H = math.sqrt(2 / 3)
GOLD_D, GOLD_L, BLUE_D, BLUE_L = '#d9a521', '#f1d98a', '#3f7fc4', '#a9c9ec'   # book colours
EDGE = '#1d1d24'


def ltype(k):
    """c/h of layer k in the periodic 4H stacking."""
    per = 'ABCB'
    p = per[(k - 1) % 4]; n = per[(k + 1) % 4]
    return 'h' if p == n else 'c'


def sites(letter, R=14):
    ox, oy = OFF[letter]
    return [(2 * m + n + ox, 3 * n + oy) for m in range(-R, R + 1) for n in range(-R, R + 1)]


def d12(p, q):  # 12 * squared xy distance
    return 3 * (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def tri_around(letter, s):
    t = [p for p in sites(letter) if d12(p, s) == 4]
    assert len(t) == 3, (letter, s, t)
    return t


def hull2(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def area2(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def slice_x0(verts):
    """Exact polygon (S, Z) = conv(verts) cut by X = 0."""
    pts = []
    for (p, q) in itertools.combinations(verts, 2):
        if p[0] == 0:
            pts.append((F(-p[1]), F(p[2])))
        if (p[0] < 0 < q[0]) or (q[0] < 0 < p[0]):
            t = F(-p[0], q[0] - p[0])
            pts.append((-(p[1] + t * (q[1] - p[1])), p[2] + t * (q[2] - p[2])))
    if verts[-1][0] == 0:
        pts.append((F(-verts[-1][1]), F(verts[-1][2])))
    h = hull2(pts)
    return h if len(h) >= 3 and area2(h) != 0 else None


def clip(poly, axis, val, keep_le):
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        pin = p[axis] <= val if keep_le else p[axis] >= val
        qin = q[axis] <= val if keep_le else q[axis] >= val
        if pin: out.append(p)
        if pin != qin:
            t = (val - p[axis]) / (q[axis] - p[axis])
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    out = hull2(out) if len(out) >= 3 else out
    return out if len(out) >= 3 and area2(out) != 0 else None


def build(S0=0, S1=REP * NREP, ngap=None):
    halves = []   # dict(kind, gap, layer, poly)
    for g in range(ngap if ngap is not None else len(SEQ) - 1):
        P, Q = SEQ[g], SEQ[g + 1]
        Rl = ({'A', 'B', 'C'} - {P, Q}).pop()
        pieces = []
        for s in sites(Q, 6):
            if -S1 - 4 <= s[1] <= -S0 + 4 and abs(s[0]) <= 4:
                pieces.append(('tet-up', [(x, y, g) for x, y in tri_around(P, s)] + [(s[0], s[1], g + 1)]))
        for s in sites(P, 6):
            if -S1 - 4 <= s[1] <= -S0 + 4 and abs(s[0]) <= 4:
                pieces.append(('tet-down', [(x, y, g + 1) for x, y in tri_around(Q, s)] + [(s[0], s[1], g)]))
        for s in sites(Rl, 6):
            if -S1 - 4 <= s[1] <= -S0 + 4 and abs(s[0]) <= 4:
                pieces.append(('oct', [(x, y, g) for x, y in tri_around(P, s)] + [(x, y, g + 1) for x, y in tri_around(Q, s)]))
        mid = F(2 * g + 1, 2)
        for kind, V in pieces:
            V = [(F(x), F(y), F(z)) for x, y, z in V]
            pol = slice_x0(V)
            if pol is None:
                continue
            for keep_le, layer in ((True, g), (False, g + 1)):
                hp = clip(pol, 1, mid, keep_le)
                if hp is None: continue
                hp = clip(hp, 0, F(S0), False)
                if hp is None: continue
                hp = clip(hp, 0, F(S1), True)
                if hp is None: continue
                halves.append(dict(kind=kind, gap=g, layer=layer, half='lower' if keep_le else 'upper', poly=hp))
    return halves


def colour(h):
    t = ltype(h['layer'])
    dark = h['kind'].startswith('tet')
    return (GOLD_D if dark else GOLD_L) if t == 'c' else (BLUE_D if dark else BLUE_L)


def true(p):
    return (float(p[0]) * SQ3_6, float(p[1]) * H)


def fmt(v):
    return str(v) if v.denominator != 1 else str(v.numerator)


def check_balls():
    """Ball centres on the plane x = 0, and distance of the others."""
    rep = {}
    for L in 'ABC':
        on = sorted({(-y) % REP for x, y in sites(L, 6) if x == 0})
        dmin = min(abs(x) for x, y in sites(L, 6) if x != 0) / 2
        rep[L] = dict(S_on_plane_mod6=on, nearest_offplane_distance=dmin)
    return rep


def shape_catalogue(halves):
    """Distinct polygon shapes (up to lateral translation by the repeat and vertical translation), per kind/half."""
    cat = {}
    for h in halves:
        p = h['poly']
        # skip polygons cut by the window edge
        if any(v[0] in (0, REP * NREP) for v in p) and not all(0 < v[0] < REP * NREP for v in p):
            pass
        mx = min(v[0] for v in p); mz = F(h['gap'])
        key_poly = tuple(sorted(((v[0] - mx), v[1] - mz) for v in p))
        key = (h['kind'], h['half'], ltype(h['layer']), key_poly)
        cat.setdefault(key, 0); cat[key] += 1
    return cat


def describe(poly):
    P = [true(v) for v in poly]
    n = len(P)
    sides = [math.dist(P[i], P[(i + 1) % n]) for i in range(n)]
    angs = []
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        u = (a[0] - b[0], a[1] - b[1]); w = (c[0] - b[0], c[1] - b[1])
        angs.append(math.degrees(math.acos((u[0] * w[0] + u[1] * w[1]) / math.hypot(*u) / math.hypot(*w))))
    return sides, angs


def logo(fig, rect):
    try:
        lg = plt.imread(os.path.expanduser(LOGO))
        la = fig.add_axes(rect); la.imshow(lg); la.axis('off')
    except Exception as e:
        print('logo missing', e)


def draw_slice(halves):
    W, Ht = REP * NREP * SQ3_6, (len(SEQ) - 1) * H
    fig = plt.figure(figsize=(9.2, 9.2 * (Ht + 1.3) / (W + 1.6)), dpi=200)
    ax = fig.add_axes([0.08, 0.05, 0.84, 0.88])
    for h in halves:
        ax.add_patch(MPoly([true(v) for v in h['poly']], closed=True, fc=colour(h), ec=EDGE, lw=1.5, joinstyle='miter'))
    for k in range(len(SEQ) - 1):
        ax.plot([0, W], [(k + 0.5) * H] * 2, ls=(0, (3, 3)), lw=0.7, color='#555')
    for k, L in enumerate(SEQ):
        z = k * H
        for r in range(NREP + 1):
            s = (SOFF[L] + r * REP) * SQ3_6
            if s <= W + 1e-9:
                ax.add_patch(Circle((s, z), 0.5, fill=False, ec='#222', lw=0.6, ls=(0, (1, 2)), clip_on=True))
                ax.plot(s, z, 'o', ms=5.5, mfc='#1d1d24', mec='white', mew=0.8, zorder=5)
        ax.text(-0.12, z, L, ha='right', va='center', fontsize=13, weight='bold')
        ax.text(W + 0.12, z, ltype(k), ha='left', va='center', fontsize=13, weight='bold',
                color=GOLD_D if ltype(k) == 'c' else BLUE_D)
    ax.set_xlim(-0.45, W + 0.45); ax.set_ylim(-0.25, Ht + 0.25); ax.set_aspect('equal'); ax.axis('off')
    ax.set_clip_box(None)
    for t in ax.patches: t.set_clip_path(Rectangle((0, 0), W, Ht, transform=ax.transData))
    fig.text(0.08, 0.965, '4H (ABCB) — exact slice on the {11-20} plane x = 0, two periods, two repeats', fontsize=11, weight='bold')
    fig.text(0.08, 0.945, 'pieces cut at each gap mid-plane (dashed); each half in its own layer\'s colour: c gold, h blue; '
             'tetrahedra dark, octahedra light; dots = ball centres', fontsize=8)
    logo(fig, [0.90, 0.005, 0.08, 0.06])
    fig.savefig(os.path.join(OUT, 'slice-4H.png')); plt.close(fig)


def inside(poly, x, y):
    c = False; n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


# Gauge: repeat = 3k stitches, layer = r rows
K, RW = 4, 7
NCOL = 3 * K * NREP
NROW = RW * (len(SEQ) - 1) + 1


def shift_rows():
    """Cumulative bias shift S(j) in stitches for chart row j (0-based, row 0 = layer 0's ball row).
    Over each gap the shift changes by k = 4 stitches, one per bias row, at the row boundaries 1|2, 2|3, 4|5, 5|6
    (symmetric about the mid-plane, which lies on boundary 3|4)."""
    S = [0] * NROW; bias = [0] * NROW
    cur = 0
    steps_at = (2, 3, 5, 6)
    for g in range(len(SEQ) - 1):
        d = 1 if (SOFF[SEQ[g + 1]] - SOFF[SEQ[g]]) % REP == 2 else -1
        for i in range(1, RW + 1):
            j = g * RW + i
            if i in steps_at:
                cur += d; bias[j] = d
            S[j] = cur
        assert (cur // K) % 3 == (SOFF[SEQ[g + 1]] // 2) % 3 and cur % K == 0
    return S, bias


def chart(halves):
    polys = [([(float(v[0]), float(v[1])) for v in h['poly']], h) for h in halves]
    # periodic copy so sampling never falls off the window
    per = []
    for P, h in polys:
        for dx in (-REP * NREP, 0, REP * NREP):
            per.append(([(x + dx, y) for x, y in P], h))
    cw = REP / (3 * K)              # S units per stitch
    rh = 1 / RW                     # Z units per row
    S, bias = shift_rows()
    grid = [[None] * NCOL for _ in range(NROW)]
    sub = [(-3 / 8), (-1 / 8), (1 / 8), (3 / 8)]
    ties = 0
    for j in range(NROW):
        for c in range(NCOL):
            sc = (c + S[j]) * cw            # true lateral position of fabric stitch (j, c)
            z = j * rh
            votes = {}
            for du in sub:
                for dv in sub:
                    xs = ((sc + du * cw) % (REP * NREP)); zs = z + dv * rh
                    if zs < 0 or zs > len(SEQ) - 1: continue
                    for P, h in per:
                        if inside(P, xs, zs):
                            col = colour(h); votes[col] = votes.get(col, 0) + 1; break
            best = max(votes.values())
            win = [k for k, v in votes.items() if v == best]
            if len(win) > 1:
                ties += 1
                win = [w for w in win if w in (GOLD_D, BLUE_D)] or win
            grid[j][c] = win[0]
    balls = []
    for k, L in enumerate(SEQ):
        j = k * RW
        for c in range(NCOL):
            if ((c + S[j]) * cw - SOFF[L]) % REP == 0:
                balls.append((j, c))
    return grid, balls, S, bias, ties


def draw_chart(grid, balls, S, bias):
    stw, sth = 1.25, 1.0          # stitch aspect 5:4
    fig = plt.figure(figsize=(9.5, 13.2), dpi=200)
    ax = fig.add_axes([0.10, 0.04, 0.78, 0.89])
    for j in range(NROW):
        for c in range(NCOL):
            ax.add_patch(Rectangle((c * stw, j * sth), stw, sth, fc=grid[j][c], ec='#3a3a3a', lw=0.35))
    for j, c in balls:
        ax.plot((c + 0.5) * stw, (j + 0.5) * sth, 'o', ms=6, mfc='#1d1d24', mec='white', mew=0.8)
    for k in range(NREP * 3 + 1):
        x = k * K * stw
        ax.plot([x, x], [0, NROW * sth], color='#1d1d24', lw=0.9 if k % 3 else 1.6)
    for k, L in enumerate(SEQ):
        j = k * RW
        ax.text(-2.2, (j + 0.5) * sth, f'{L} ({ltype(k)})', ha='right', va='center', fontsize=10, weight='bold',
                color=GOLD_D if ltype(k) == 'c' else BLUE_D)
    for j in range(NROW):
        ax.text(-0.3, (j + 0.5) * sth, str(j + 1), ha='right', va='center', fontsize=5.5)
        if bias[j]:
            ax.text(NCOL * stw + 0.4, (j + 0.5) * sth, 'bias R' if bias[j] > 0 else 'bias L', ha='left', va='center',
                    fontsize=6, color='#b00020')
        ax.text(NCOL * stw + 4.2, (j + 0.5) * sth, f'{S[j]:+d}', ha='left', va='center', fontsize=5.5, color='#555')
    ax.text(NCOL * stw + 4.2, NROW * sth + 0.5, 'shift', fontsize=6, color='#555')
    for c in range(NCOL):
        ax.text((c + 0.5) * stw, -0.6, str(c + 1), ha='center', va='top', fontsize=5)
    ax.set_xlim(-6, NCOL * stw + 7); ax.set_ylim(-1.5, NROW * sth + 1.2); ax.set_aspect('equal'); ax.axis('off')
    fig.text(0.10, 0.968, '4H (ABCB) knitting chart — fabric grid, read from row 1 at the bottom', fontsize=11, weight='bold')
    fig.text(0.10, 0.952, f'gauge: repeat 12 stitches (3 × k, k = {K}), layer {RW} rows, stitch 5:4 (wider than tall); '
             'one bias row moves the row one stitch; 4 bias rows per layer = 1/3 repeat', fontsize=7.5)
    fig.text(0.10, 0.940, 'bias R / bias L: decrease at one end, increase at the other, row moves one stitch right / left '
             '(true position = chart column + shift). 4 colours; dots = ball stitches', fontsize=7.5)
    logo(fig, [0.88, 0.005, 0.09, 0.05])
    fig.savefig(os.path.join(OUT, 'chart-4H.png')); plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    halves = build()
    balls = check_balls()
    print('balls on plane x=0 (S mod 6) and nearest off-plane distance:', balls)
    # exact checks: area of slice window covered exactly once
    tot = sum(area2(h['poly']) for h in halves)
    print('covered area (S*Z units) =', tot, ' window =', REP * NREP * (len(SEQ) - 1))
    assert tot == REP * NREP * (len(SEQ) - 1)
    cat = shape_catalogue(halves)
    lines = []
    for key, cnt in sorted(cat.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], len(kv[0][3]))):
        kind, half, t, poly = key
        hp = hull2(list(poly))
        sides, angs = describe(hp)
        lines.append(dict(kind=kind, half=half, layer_type=t, count=cnt, n=len(hp),
                          corners_S_Z=[(fmt(v[0]), fmt(v[1])) for v in hp],
                          sides=[round(s, 4) for s in sides], angles=[round(a, 2) for a in angs]))
        print(f'{kind:8s} {half:5s} {t} x{cnt:2d}  {len(hp)}-gon  corners (S,Z)=' +
              ' '.join(f'({fmt(v[0])},{fmt(v[1])})' for v in hp) +
              '  sides ' + ' '.join(f'{s:.4f}' for s in sides) + '  angles ' + ' '.join(f'{a:.2f}' for a in angs))
    draw_slice(halves)
    grid, bl, S, bias, ties = chart(halves)
    draw_chart(grid, bl, S, bias)
    counts = {}
    for row in grid:
        for c in row: counts[c] = counts.get(c, 0) + 1
    print('chart', NROW, 'rows x', NCOL, 'stitches; colour counts', counts, 'ties (to dark)', ties, 'ball stitches', len(bl))
    print('ball stitch columns (1-based):', sorted({c + 1 for j, c in bl}))
    json.dump(dict(balls=balls, shapes=lines, gauge=dict(k=K, rows_per_layer=RW, stitches_per_repeat=3 * K),
                   colours=counts, ties=ties, shift=S), open(os.path.join(OUT, 'slice-4H.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()


def whole_catalogue():
    """Uncut-by-window slices of whole pieces and of their halves, per gap kind (up = shift +1/3, down = -1/3)."""
    res = {}
    for P, Q in (('A', 'B'), ('B', 'A')):
        Rl = ({'A', 'B', 'C'} - {P, Q}).pop()
        cand = []
        for s in sites(Q, 6):
            cand.append(('tet-up', [(x, y, 0) for x, y in tri_around(P, s)] + [(s[0], s[1], 1)]))
        for s in sites(P, 6):
            cand.append(('tet-down', [(x, y, 1) for x, y in tri_around(Q, s)] + [(s[0], s[1], 0)]))
        for s in sites(Rl, 6):
            cand.append(('oct', [(x, y, 0) for x, y in tri_around(P, s)] + [(x, y, 1) for x, y in tri_around(Q, s)]))
        for kind, V in cand:
            if not all(abs(v[0]) <= 3 and -14 <= v[1] <= 14 for v in V): continue
            pol = slice_x0([(F(x), F(y), F(z)) for x, y, z in V])
            if pol is None: continue
            mx = min(v[0] for v in pol)
            parts = [pol, clip(pol, 1, F(1, 2), True), clip(pol, 1, F(1, 2), False)]
            key = (P + Q, kind) + tuple(tuple(sorted((v[0] - mx, v[1]) for v in p)) if p else None for p in parts)
            res[key] = res.get(key, 0) + 1
    out = []
    for key in sorted(res):
        gap, kind, whole, lo, up = key
        row = dict(gap=gap, kind=kind)
        for name, p in (('whole', whole), ('lower', lo), ('upper', up)):
            if p is None: row[name] = None; continue
            hp = hull2(list(p)); sides, angs = describe(hp)
            row[name] = dict(n=len(hp), corners_S_Z=[(fmt(v[0]), fmt(v[1])) for v in hp],
                             sides=[round(x, 4) for x in sides], angles=[round(x, 2) for x in angs])
        out.append(row)
        print(gap, kind, {k: (row[k]['n'], row[k]['corners_S_Z'], row[k]['sides'], row[k]['angles']) if row[k] else None
                          for k in ('whole', 'lower', 'upper')})
    return out


if __name__ == '__main__' and os.environ.get('CATALOGUE'):
    json.dump(whole_catalogue(), open(os.path.join(OUT, 'pieces-in-slice.json'), 'w'), indent=1)
