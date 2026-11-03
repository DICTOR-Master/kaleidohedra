# Knitted HexOct Patch: Pattern. DICTO proposed the Knitted HexOct (#83); after the cushion plan DICTO chose to start with one patch.
# The patch is the plan's trial piece c (A-B-C, 4 x 4 nodes per sheet) on the plan's lattice: a = 8 stitches, node rows every 7 ridges,
# same offsets and the same rounding as scripts/plan.py. Builds every number, chart, table and figure, asserts the checks, and writes
#   <out>/paper.html, <out>/figs/*.svg, <out>/data/check.out, <out>/data/patch.json
# Usage: python pattern.py <out dir>        (run on dicto-big-brother with ~/geom/bin/python; stdlib only)
import sys, os, json, math, itertools

OUT = os.path.abspath(sys.argv[1]); FIGS, DATA = OUT + '/figs', OUT + '/data'
os.makedirs(FIGS, exist_ok=True); os.makedirs(DATA, exist_ok=True)
LOG = []; QUIET = [False]
def log(*a):
    s = ' '.join(str(x) for x in a)
    if not QUIET[0]: print(s); LOG.append(s)
def check(cond, msg):
    assert cond, 'FAILED: ' + msg
    log('ok  ' + msg)

# ---------------------------------------------------------------- the plan's gauge and lattice (scripts/plan.py)
S = R = 22.0                       # garter, DK mercerised cotton, stitches and ridges per 10 cm (plan)
st, rg = 100 / S, 100 / R          # mm per stitch, per ridge
N, M = 8, 7                        # node spacing in stitches, node-row spacing in ridges (plan)
a = N * st; d = math.sqrt(2 / 3) * a; pitch_true = math.sqrt(3) / 2 * a; t = 3.5
check(abs(a - 36.36) < 0.01 and round(a, 1) == 36.4, f'a = {a:.2f} mm (plan 36.4 mm, 8 stitches)')
check(round(d, 1) == 29.7, f'd = sqrt(2/3) a = {d:.2f} mm (plan 29.7 mm)')
TILT = math.degrees(math.atan(math.sqrt(2)))
OFF = {'A': (0.0, 0.0), 'B': (N / 2, 1 / 3), 'C': (0.0, 2 / 3)}   # plan offsets (stitches, node rows)

# ---------------------------------------------------------------- the patch: 35 stitches x 32 ridges, 4 x 4 nodes per sheet
W, H, BASE = 35, 33, 4             # sheet size; ridge of the first node row of sheet A (as in the plan)
SLO, SHI = 4, 32                   # node stitches lie in 4..32 (3 plain stitches at each edge)
def sheet_nodes(name, pos, k, rows):
    ox, oy = OFF[pos]; L = []
    for j in rows:
        base_s = 4 + ox + (N / 2) * (j % 2)
        ss = [s for s in range(SLO, SHI + 1) if (s - base_s) % N == 0]
        check(len(ss) == 4, f'sheet {name} row {j}: 4 node stitches {ss}')
        rt = BASE + M * (j + oy)                      # ridge before rounding (plan rule)
        for s in ss:
            L.append(dict(sheet=name, k=k, s=s, ridge=round(rt), rt=rt, X=s * st,
                          Y=(BASE + pitch_true / rg * (j + oy)) * rg, Z=k * d))
    return L
def links_of(lo, up):
    L = []
    for u in lo:
        for v in up:
            if abs(math.hypot(v['X'] - u['X'], v['Y'] - u['Y']) - a / math.sqrt(3)) < 0.05 * a: L.append((u, v))
    return L
def build(word, rows3):
    NS = [sheet_nodes(word[0], 'A', 0, range(4)), sheet_nodes(word[1], 'B', 1, range(4)),
          sheet_nodes(word[2] if word[2] != "A'" else "A'", 'C' if word[2] == 'C' else 'A', 2, rows3)]
    return NS, [links_of(NS[0], NS[1]), links_of(NS[1], NS[2])]
# choose sheet 3's four node rows: the window with most links (then the smaller ridge span)
def pick(word):
    best = None
    for rows3 in (range(-1, 3), range(0, 4)):
        QUIET[0] = True; NS, G = build(word, rows3); QUIET[0] = False
        log(f"{'-'.join(word)}: sheet 3 node rows {list(rows3)}: links {[len(g) for g in G]}")
        span = max(n['ridge'] for s_ in NS for n in s_) - min(n['ridge'] for s_ in NS for n in s_)
        key = (-sum(len(g) for g in G), span)
        if best is None or key < best[0]: best = (key, rows3)
    return best[1]
rows_c = pick(['A', 'B', 'C']); NS, G = build(['A', 'B', 'C'], rows_c)
ALL = [n for s_ in NS for n in s_]
for k, s_ in enumerate(NS):
    log(f"sheet {'ABC'[k]}: node ridges {sorted(set(n['ridge'] for n in s_))} (before rounding {sorted(set(round(n['rt'], 2) for n in s_))}), stitches {sorted(set(n['s'] for n in s_))}")
check(all(len(s_) == 16 for s_ in NS), 'each sheet has 4 x 4 = 16 nodes')
rmin, rmax = min(n['ridge'] for n in ALL), max(n['ridge'] for n in ALL)
check(rmin == 4 and H - rmax == 3, f'node ridges {rmin}..{rmax}: 3 plain ridges before and after in {H} ridges')
check(len({(n['k'], n['ridge']) for n in ALL}) == 12 and len({n['ridge'] for n in ALL}) == 12, 'twelve node ridges, no two sheets on the same ridge')
nl = [len(g) for g in G]; NL = sum(nl)
log(f'links: gap 1 (A-B) {nl[0]}, gap 2 (B-C) {nl[1]}, total {NL}')
for g in G:
    check(max(abs(math.dist((u['X'], u['Y'], u['Z']), (v['X'], v['Y'], v['Z'])) - a) for u, v in g) < 1e-9,
          'every link has length a in the ideal geometry')
    for u, v in g:
        ang = math.degrees(math.asin(d / a)); assert abs(ang - TILT) < 1e-9
check(True, f'every link rises at {TILT:.2f} deg to the sheets')
deg = {}
for g in G:
    for u, v in g:
        for n in (u, v): deg[id(n)] = deg.get(id(n), 0) + 1
check(max(deg.values()) <= 6, 'no node has more than 3 links per gap')
# straight on through sheet B (c)
straight = []
for (w, x) in G[0]:
    for (u, v) in G[1]:
        if u is x and abs((v['X'] - u['X']) - (x['X'] - w['X'])) < 1e-9 and abs((v['Y'] - u['Y']) - (x['Y'] - w['Y'])) < 1e-9:
            straight.append((w, x, v))
through = sum(1 for (w, x) in G[0] for (u, v) in G[1] if u is x and abs(math.atan2(v['Y'] - u['Y'], v['X'] - u['X']) - math.atan2(x['Y'] - w['Y'], x['X'] - w['X'])) % (2 * math.pi) < 1e-9)
check(len(straight) == through, f'sheet B is c: {len(straight)} link pairs run straight on through a B node (every pair that lines up in plan does)')
NSTRAIGHT = len(straight)

# ---------------------------------------------------------------- cord pieces, catch rows, order of work
# The node met first while knitting holds the first catch. A node that is first end of two links in a gap gets a V (fold caught there),
# otherwise a single. Cord to the sheet above is caught on row 1 of the ridge, cord to the sheet below on row 2 (the cord ends lie at the
# back of the work, and the back is the upper face on row 1, the lower face on row 2: see the in-step technique).
def row_for(node, other): return 1 if other['k'] > node['k'] else 2
def order_key(node, row):   # position in the work: ridge, row, sheet order in that row, stitch order along the row
    sh = node['k'] if row == 1 else 2 - node['k']
    return (node['ridge'], row, sh, node['s'] if row == 1 else W + 1 - node['s'])
pieces = []
for gi, g in enumerate(G):
    first = {}
    for u, v in g:
        check_tie = u['ridge'] != v['ridge']; assert check_tie
        f, s_ = (u, v) if u['ridge'] < v['ridge'] else (v, u)
        first.setdefault(id(f), (f, []))[1].append(s_)
    for f, far in first.values():
        assert len(far) in (1, 2)
        if len(far) == 2: assert far[0]['ridge'] == far[1]['ridge'] and far[0]['k'] == far[1]['k']
        pieces.append(dict(gap=gi + 1, kind='V' if len(far) == 2 else 'S', first=f, far=sorted(far, key=lambda n: order_key(n, row_for(n, f))),
                           row1=row_for(f, far[0]), rowf=row_for(far[0], f)))
pieces.sort(key=lambda p: order_key(p['first'], p['row1']) + (p['gap'],))
cnt = {'V': 0, 'S': 0}
for p in pieces:
    cnt[p['kind']] += 1; p['id'] = f"{p['kind']}{cnt[p['kind']]}"
NV, NSI = cnt['V'], cnt['S']; NP = NV + NSI; NCATCH = 3 * NV + 2 * NSI
check(2 * NV + NSI == NL, f'{NV} V pieces and {NSI} single pieces make {NL} links')
log(f'cord pieces {NP}, catches {NCATCH}')
for gi in (1, 2):
    pv = [p for p in pieces if p['gap'] == gi]
    log(f"gap {gi}: V {sum(p['kind'] == 'V' for p in pv)}, single {sum(p['kind'] == 'S' for p in pv)}, links {nl[gi - 1]}")
span = max(p['far'][0]['ridge'] - p['first']['ridge'] for p in pieces)
check(span == 5, f'longest open cord: {span} ridges between first and far catch (plan: at most 5)')
# the cord reaches easily while knitting: distance first catch -> far stitch with the sheets lying together (thickness t apart)
reach = max(math.sqrt(((f['s'] - n['s']) * st) ** 2 + ((n['ridge'] - p['first']['ridge']) * rg) ** 2 + (t * abs(n['k'] - p['first']['k'])) ** 2)
            for p in pieces for f in [p['first']] for n in p['far'])
check(reach < a, f'every far node lies within {reach:.1f} mm of its first catch while knitting (< a = {a:.1f} mm): the measured cord always reaches, slack')
# catch-row rule and order: every far catch comes after its first catch
for p in pieces:
    for n in p['far']: assert order_key(n, p['rowf']) > order_key(p['first'], p['row1'])
check(True, 'every far catch is made after its first catch (order of work)')
# per stitch catches
CAT = {}
for p in pieces:
    CAT.setdefault((p['first']['ridge'], p['row1'], p['first']['k'], p['first']['s']), []).append((p, 'first'))
    for n in p['far']: CAT.setdefault((n['ridge'], p['rowf'], n['k'], n['s']), []).append((p, 'far'))
check(sum(len(v) for v in CAT.values()) == NCATCH, f'{NCATCH} catches at {len(CAT)} node stitches')
check(all(k[2] != 0 or k[1] == 1 for k in CAT) and all(k[2] != 2 or k[1] == 2 for k in CAT), 'sheet A catches only on row 1, sheet C only on row 2')
maxstr = max(sum(2 if (p['kind'] == 'V' and w == 'first') else 1 for p, w in v) for v in CAT.values())
maxc = max(len(v) for v in CAT.values())
check(maxc <= 3, f'at most {maxc} cords meet in one node stitch on one row ({maxstr} cord strands at most, a V fold counting as 2)')
# cut lengths: link length(s) + 25 mm per end for catch and knot (plan) + 10 mm for the V knot; rounded up to whole cm
TAIL, VKNOT = 25.0, 10.0
cutV = math.ceil((2 * a + 2 * TAIL + VKNOT) / 10); cutS = math.ceil((a + 2 * TAIL) / 10)
check((cutV, cutS) == (14, 9), f'cut lengths: V {cutV} cm (2a + 2 x 25 mm + 10 mm = {2 * a + 2 * TAIL + VKNOT:.1f} mm), single {cutS} cm (a + 2 x 25 mm = {a + 2 * TAIL:.1f} mm)')
cord_m = (NV * cutV + NSI * cutS) / 100

# ---------------------------------------------------------------- the h patch (A-B-A): only sheet 3 changes
rows_h = pick(['A', 'B', "A'"]); NSh, Gh = build(['A', 'B', "A'"], rows_h)
nlh = [len(g) for g in Gh]
check(sorted((n['s'], n['ridge']) for n in NSh[0]) == sorted((n['s'], n['ridge']) for n in NSh[2]), "h patch: sheet 3 (A') has exactly sheet A's node stitches and ridges")
straight_h = sum(1 for (w, x) in Gh[0] for (u, v) in Gh[1] if u is x and abs((v['X'] - u['X']) - (x['X'] - w['X'])) < 1e-9 and abs((v['Y'] - u['Y']) - (x['Y'] - w['Y'])) < 1e-9)
check(straight_h == 0, 'h patch: no link pair runs straight on through B (B is h)')
H3 = sorted({(n['ridge'], tuple(sorted(m['s'] for m in NSh[2] if m['ridge'] == n['ridge']))) for n in NSh[2]})
C3 = sorted({(n['ridge'], tuple(sorted(m['s'] for m in NS[2] if m['ridge'] == n['ridge']))) for n in NS[2]})
log(f'h patch: links {nlh} total {sum(nlh)}; sheet 3 rows {H3}')
pieces_h = 0; vh = 0
for g in Gh:
    first = {}
    for u, v in g:
        f = u if u['ridge'] < v['ridge'] else v; first[id(f)] = first.get(id(f), 0) + 1
    vh += sum(1 for x in first.values() if x == 2); pieces_h += len(first)
log(f'h patch: cord pieces {pieces_h} ({vh} V, {pieces_h - vh} single)')
rmax_h = max(n['ridge'] for s_ in NSh for n in s_); check(H - rmax_h >= 3 and min(n['ridge'] for s_ in NSh for n in s_) >= 4, 'h patch fits the same 35 x 33 sheet')

# ---------------------------------------------------------------- materials, time, test numbers
sts = 3 * W * 2 * H; yarn_m = sts * 0.01
W_mm, H_mm = W * st, H * rg
gapvol = W_mm * H_mm * d / 1e6
fill_lo, fill_hi = gapvol * 2 * 400 / 9.5, gapvol * 2 * 500 / 9.5
mins = sts / 25 * 1.25 + (NCATCH + NP) * 0.5
BOARD = 140.0; press_kpa = 5 * 9.81 / (BOARD / 1000) ** 2 / 1000
check(abs(W_mm - 159.1) < 0.1 and abs(H_mm - 150.0) < 0.1, f'patch {W_mm:.1f} x {H_mm:.1f} mm, depth 2d + t = {2 * d + t:.1f} mm')
log(f'yarn {yarn_m:.0f} m ({sts} stitches at 1 cm), cord {cord_m:.2f} m, test fill {fill_lo:.0f}-{fill_hi:.0f} g, time {mins / 60:.1f} h, press {press_kpa:.2f} kPa')
row_err = {r: (M * 100 / r / pitch_true - 1) * 100 for r in (21, 22, 23)}
log('row spacing error at ridge gauge 21/22/23: ' + ', '.join(f'{r}: {e:+.1f} %' for r, e in row_err.items()))

# ---------------------------------------------------------------- cells (for the drawing)
def tris(nodes):
    return [c for c in itertools.combinations(nodes, 3) if all(abs(math.hypot(p['X'] - q['X'], p['Y'] - q['Y']) - a) < 1e-6 for p, q in itertools.combinations(c, 2))]
def linked(g, p, q): return any((u is p and v is q) or (u is q and v is p) for u, v in g)
CELLS = []
for gi, g in enumerate(G):
    lo, up = NS[gi], NS[gi + 1]
    for T in tris(lo):
        for v in up:
            if all(linked(g, x, v) for x in T): CELLS.append(('tet', gi, list(T) + [v]))
    for T in tris(up):
        for u in lo:
            if all(linked(g, u, x) for x in T): CELLS.append(('tet', gi, list(T) + [u]))
    for T in tris(lo):
        for U in tris(up):
            if all(sum(linked(g, x, y) for y in U) == 2 for x in T) and all(sum(linked(g, x, y) for x in T) == 2 for y in U):
                CELLS.append(('oct', gi, list(T) + list(U)))
nt = sum(c[0] == 'tet' for c in CELLS); no = sum(c[0] == 'oct' for c in CELLS)
log(f'whole cells inside the patch: {nt} tetrahedra, {no} octahedra')
check(no > 0 and nt > 0 and nt >= 2 * no - 4, 'tetrahedra and octahedra present (ratio near 2 : 1 in the interior)')

# ---------------------------------------------------------------- SVG helpers (line drawings, house colours)
GOLD, VIOL, TEAL = '#d9a521', '#8a5cc2', '#1f9e90'
YARN, YLINE, INK, GREY = '#efe9da', '#6f6a5e', '#222', '#8d877a'
SHEET_FILL = {'A': '#e4e0d6', 'B': '#ece6d6', 'C': '#f1ede4', "A'": '#f1ede4'}
def svg(w, h, body, wmm):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{wmm}mm" height="{wmm * h / w:.3f}mm" viewBox="0 0 {w} {h}" '
            f'font-family="DejaVu Sans, sans-serif">{body}</svg>')
def line(x1, y1, x2, y2, w=1.0, c='#000', dash=None, op=1):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"'
            + (f' stroke-dasharray="{dash}"' if dash else '') + (f' stroke-opacity="{op}"' if op < 1 else '') + '/>')
def text(x, y, s, size=10, anchor='middle', weight='normal', c='#000', rot=None):
    tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ''
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{c}"{tr}>{s}</text>'
def circ(x, y, r, fill='#000', stroke='none', w=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def poly(pts, fill='none', stroke='#000', w=0.8, fop=1, dash=None):
    return (f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="{fill}" fill-opacity="{fop}" stroke="{stroke}" '
            f'stroke-width="{w}" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def rect(x, y, w, h, fill='none', stroke='#000', sw=0.8, rx=0):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(dd, c='#000', w=1.2, fill='none', dash=None):
    return f'<path d="{dd}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
def ell(x, y, rx, ry, c='#444', w=1.3, fill='none'):
    return f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'
def arrow(x1, y1, x2, y2, w=1.2, c='#000', hs=6):
    an = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - hs * math.cos(an - 0.42), y2 - hs * math.sin(an - 0.42)); p2 = (x2 - hs * math.cos(an + 0.42), y2 - hs * math.sin(an + 0.42))
    return line(x1, y1, x2, y2, w, c) + poly([(x2, y2), p1, p2], c, c, 0.6)
def grp(x, y, body): return f'<g transform="translate({x:.2f},{y:.2f})">{body}</g>'
def needle(x1, y1, x2, y2): return line(x1, y1, x2, y2, 7, '#7a7466') + line(x1, y1, x2, y2, 4.6, '#dcd6c6')
def save(name, s): open(os.path.join(FIGS, name), 'w').write(s)
def ptitle(n, tt, sub=(), x=6):
    out = text(x, 14, f'{n}  {tt}', 10.5, 'start', 'bold')
    for i, s in enumerate(sub): out += text(x, 27 + 11 * i, s, 9, 'start', c='#333')
    return out
def garter(x0, y0, cols, ridges, s, marks=None):
    marks = marks or {}; b = [rect(x0, y0, cols * s, ridges * s, YARN, 'none', 0)]
    for r in range(ridges):
        yc = y0 + r * s
        for c in range(cols):
            xc = x0 + c * s + s / 2; col = marks.get((c, r), YLINE); w = 2.6 if (c, r) in marks else 0.9
            b.append(path(f'M {xc - 0.33 * s:.2f} {yc + 0.06 * s:.2f} L {xc:.2f} {yc + 0.52 * s:.2f} L {xc + 0.33 * s:.2f} {yc + 0.06 * s:.2f}', col, w))
            b.append(path(f'M {xc - 0.44 * s:.2f} {yc + 0.64 * s:.2f} Q {xc:.2f} {yc + 0.98 * s:.2f} {xc + 0.44 * s:.2f} {yc + 0.64 * s:.2f}', YLINE, 0.9))
    return ''.join(b)
def mark(x, y, sc=1.0):   # small DICTO mark text for figures
    return text(x, y, 'DICTO', 7 * sc, 'end', 'bold', '#b8962e')

# ---------------------------------------------------------------- Fig 1: what you are making (3D, true geometry)
def hull_faces(pts):
    faces = []; n = len(pts)
    for a_, b_, c_ in itertools.combinations(range(n), 3):
        A, B, Cc = (pts[q] for q in (a_, b_, c_))
        nx = (B[1] - A[1]) * (Cc[2] - A[2]) - (B[2] - A[2]) * (Cc[1] - A[1]); ny = (B[2] - A[2]) * (Cc[0] - A[0]) - (B[0] - A[0]) * (Cc[2] - A[2])
        nz = (B[0] - A[0]) * (Cc[1] - A[1]) - (B[1] - A[1]) * (Cc[0] - A[0]); ln = math.sqrt(nx * nx + ny * ny + nz * nz)
        if ln < 1e-9: continue
        sd = [(p[0] - A[0]) * nx + (p[1] - A[1]) * ny + (p[2] - A[2]) * nz for p in pts]
        if all(x <= 1e-7 * ln for x in sd) or all(x >= -1e-7 * ln for x in sd):
            f = [q for q in range(n) if abs(sd[q]) <= 1e-7 * ln]
            if len(f) == 3 and set(f) not in [set(x) for x in faces]: faces.append(f)
    return [[pts[q] for q in f] for f in faces]
def proj_factory(az=-32, el=28):
    ca, sa, ce, se = math.cos(math.radians(az)), math.sin(math.radians(az)), math.cos(math.radians(el)), math.sin(math.radians(el))
    def P(p):
        x, y, z = p[0], p[1], p[2]           # seen from above (sheet C side): stitch 1 at the left
        x1 = x * ca - y * sa; y1 = x * sa + y * ca
        return (x1, -(z * ce + y1 * se), y1 * ce - z * se)
    return P
def fig_make():
    P = proj_factory(); sc = 1.9; Wd, Hd = 660, 380
    corners = lambda k, zz: [(0.5 * st, 0.5 * rg, zz), (W_mm + 0.5 * st, 0.5 * rg, zz), (W_mm + 0.5 * st, H_mm + 0.5 * rg, zz), (0.5 * st, H_mm + 0.5 * rg, zz)]
    pts = [P(c) for k in range(3) for c in corners(k, k * d)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = 330 - sc * (max(xs) + min(xs)) / 2, Hd / 2 - sc * (max(ys) + min(ys)) / 2
    pr = lambda p: (ox + sc * P(p)[0], oy + sc * P(p)[1]); dep = lambda p: P(p)[2]
    xyz = lambda n: (n['X'], n['Y'], n['Z'])
    b = []
    # choose one tetrahedron and one octahedron near the middle in each gap
    cx, cy = W_mm / 2, H_mm / 2
    show = []
    for gi in range(2):
        for kind in ('tet', 'oct'):
            cs = [c for c in CELLS if c[0] == kind and c[1] == gi]
            show.append(min(cs, key=lambda c: (sum(n['X'] for n in c[2]) / len(c[2]) - cx - (25 if kind == 'oct' else -25)) ** 2 + (sum(n['Y'] for n in c[2]) / len(c[2]) - cy) ** 2))
    for k in range(3):
        nm = 'ABC'[k]; zz = k * d
        items = []
        b.append(poly([pr(c) for c in corners(k, zz)], SHEET_FILL[nm], '#6f6a5e', 0.9, 0.62))
        for n in NS[k]: b.append(circ(*pr(xyz(n)), 2.4, '#333'))
        if k < 2:
            for u, v in G[k]:
                items.append(((dep(xyz(u)) + dep(xyz(v))) / 2, line(*pr(xyz(u)), *pr(xyz(v)), 1.5, TEAL)))
            for c in show:
                if c[1] != k: continue
                col, ec = (GOLD, '#6b5310') if c[0] == 'tet' else (VIOL, '#3c2366')
                for f in hull_faces([xyz(n) for n in c[2]]):
                    items.append((sum(dep(p) for p in f) / 3, poly([pr(p) for p in f], col, ec, 0.6, 0.5)))
            for _, it in sorted(items, key=lambda q: -q[0]): b.append(it)
        lp = min((pr(c) for c in corners(k, zz)), key=lambda q: q[0])
        b.append(text(lp[0] - 6, lp[1] + 4, f'sheet {nm}' + (' (middle, c)' if k == 1 else ' (bottom)' if k == 0 else ' (top)'), 10, 'end', 'bold', '#444'))
    # dimensions
    p0, p1 = pr((0.5 * st, 0.5 * rg, 2 * d)), pr((W_mm + 0.5 * st, 0.5 * rg, 2 * d))
    q0, q1 = pr((0.5 * st, 0.5 * rg, 0)), pr((W_mm + 0.5 * st, 0.5 * rg, 0))
    b.append(text((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2 + 24, f'{W} stitches = {W_mm / 10:.1f} cm', 9.5, 'middle', c='#333'))
    r0, r1 = pr((W_mm + 0.5 * st, 0.5 * rg, 0)), pr((W_mm + 0.5 * st, H_mm + 0.5 * rg, 0))
    b.append(text((r0[0] + r1[0]) / 2 + 12, (r0[1] + r1[1]) / 2 + 16, f'{H} ridges = {H_mm / 10:.1f} cm', 9.5, 'start', c='#333'))
    e0, e1 = pr((0.5 * st, 0.5 * rg, 0)), pr((0.5 * st, 0.5 * rg, 2 * d))

    # legend
    lx = 530; ly = 30
    b.append(line(lx, ly, lx + 22, ly, 2, TEAL)); b.append(text(lx + 28, ly + 3.5, 'link cord, length a', 9, 'start'))
    b.append(poly([(lx, ly + 22), (lx + 22, ly + 22), (lx + 11, ly + 8)], GOLD, '#6b5310', 0.6, 0.6)); b.append(text(lx + 28, ly + 19, 'a tetrahedron', 9, 'start'))
    b.append(poly([(lx + 11, ly + 26), (lx + 22, ly + 36), (lx + 11, ly + 46), (lx, ly + 36)], VIOL, '#3c2366', 0.6, 0.6)); b.append(text(lx + 28, ly + 40, 'an octahedron', 9, 'start'))
    b.append(circ(lx + 11, ly + 58, 2.4, '#333')); b.append(text(lx + 28, ly + 61, 'node stitch', 9, 'start'))
    b.append(text(lx, ly + 80, 'seen from above:', 8.5, 'start', c='#555')); b.append(text(lx, ly + 92, 'stitch 1 at the left,', 8.5, 'start', c='#555'))
    b.append(text(lx, ly + 104, 'cast-on edge in front', 8.5, 'start', c='#555'))
    b.append(mark(Wd - 6, Hd - 6))
    save('make.svg', svg(Wd, Hd, ''.join(b), 150))

# ---------------------------------------------------------------- Fig 2: three needles in step (end view along the needles)
def fig_instep():
    PW, PH = 190, 262; out = []
    def stack(order, x0, y0, tipped=(), hl=None, cords=True):
        # order: sheets front (left) to back (right); end view: needle = circle, fabric hangs down
        b = []; gapx = 26
        pos = {}
        for i, nm in enumerate(order):
            x = x0 + i * gapx
            if nm in tipped:   # tipped forward: fabric lies toward the knitter
                b.append(path(f'M {x} {y0} Q {x - 30} {y0 + 10} {x - 62} {y0 + 50 + 6 * i}', '#6f6a5e', 4 if nm == hl else 2.6))
                b.append(circ(x, y0, 5.2, '#7a7466')); b.append(circ(x, y0, 3.4, '#dcd6c6'))
                b.append(text(x - 64, y0 + 66 + 6 * i, nm, 10, 'middle', 'bold'))
            else:
                b.append(line(x, y0, x, y0 + 120, 4 if nm == hl else 2.6, '#6f6a5e'))
                b.append(circ(x, y0, 5.2, '#7a7466')); b.append(circ(x, y0, 3.4, '#dcd6c6'))
                b.append(text(x, y0 + 136, nm, 10, 'middle', 'bold'))
            pos[nm] = x
        if cords:
            names = list(order)
            for i in range(len(names) - 1):
                p, q = pos[names[i]], pos[names[i + 1]]
                if names[i] in tipped or names[i + 1] in tipped: continue
                for yy in (y0 + 30, y0 + 70, y0 + 100):
                    b.append(path(f'M {p + 1.5} {yy} Q {(p + q) / 2} {yy + 14} {q - 1.5} {yy + 4}', TEAL, 1.3))
        return b
    eye = lambda x, y: ell(x, y, 7, 4.2, '#333', 1.0) + circ(x + 2, y, 2.0, '#333') + text(x, y + 16, 'you', 8.5)
    b = [ptitle(1, 'Row 1: sheet A in front', ['Knit across A, then tip', 'it forward out of the way.'])]
    b += stack(['A', 'B', 'C'], 82, 52, hl='A'); b.append(eye(26, 52)); b.append(arrow(60, 40, 60, 40.1, 1, '#000', 0.1))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Then B, then C', ['Knit across B, tip it forward;', 'knit across C, tip it forward.'])]
    b += stack(['A', 'B', 'C'], 112, 52, tipped=('A', 'B'), hl='C'); b.append(eye(26, 52))
    out.append(grp(PW, 0, ''.join(b)))
    b = [ptitle(3, 'Turn the stack', ['Lift the three needles together', 'and turn them round as one.'])]
    b += stack(['A', 'B', 'C'], 70, 70, cords=True)
    b.append(path('M 58 60 C 78 40, 140 40, 160 60', '#000', 1.3)); b.append(poly([(160, 60), (151, 56), (157, 50)], '#000', '#000', 0.5))
    b.append(path('M 160 212 C 140 232, 80 232, 60 212', '#000', 1.3)); b.append(poly([(60, 212), (69, 216), (63, 222)], '#000', '#000', 0.5))
    out.append(grp(2 * PW, 0, ''.join(b)))
    b = [ptitle(4, 'Row 2: sheet C in front', ['Knit across C, then B, then A,', 'tipping each forward in turn.'])]
    b += stack(['C', 'B', 'A'], 82, 52, hl='C'); b.append(eye(26, 52))
    out.append(grp(3 * PW, 0, ''.join(b)))
    foot = [text(4, PH - 12, 'Seen along the needles. Teal: link cords hanging slack between the sheets.', 9, 'start', c='#333'),
            mark(4 * PW - 4, PH - 12)]
    save('instep.svg', svg(4 * PW, PH, ''.join(out + foot), 178))

# ---------------------------------------------------------------- Fig 3: the node stitch with the cord (CK)
def fig_ck():
    PW, PH = 200, 200; out = []
    rn = [20, 36, 52, 68, 84]; ln = [118, 134, 150, 166, 182]
    def base(b):
        b.append(garter(10, 146, 11, 2, 16.4))
        for x in rn + ln: b.append(line(x, 110, x, 146, 0.9, YLINE))
    b = [ptitle(1, 'Knit to the node stitch', ['Lay the cord beside the yarn,', 'at the back of the work.'])]
    base(b); b.append(needle(2, 100, 96, 100)); b.append(needle(198, 100, 110, 100))
    for x in rn + ln: b.append(ell(x, 100, 4.5, 9))
    b.append(ell(118, 100, 4.5, 9, '#000', 2.0)); b.append(text(126, 66, 'node stitch', 9, 'start', 'bold')); b.append(line(128, 70, 120, 88, 0.8))
    b.append(path('M 84 110 C 92 114, 92 76, 80 44', YLINE, 2.4)); b.append(text(74, 50, 'yarn', 9, 'end'))
    b.append(path('M 100 86 C 94 74, 94 60, 92 42', TEAL, 2.2)); b.append(text(98, 50, 'cord', 9, 'start', c=TEAL))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Insert the needle knitwise', ['into the node stitch; wrap the', 'yarn and the cord together.'])]
    base(b); b.append(needle(198, 100, 110, 100))
    yN = lambda x: 112 - (x - 2) * (22 / 126)
    b.append(needle(2, 112, 128, 90))
    for x in rn: b.append(ell(x, yN(x), 4.5, 9))
    for x in ln: b.append(ell(x, 100, 4.5, 9, '#000' if x == 118 else '#444', 2.0 if x == 118 else 1.3))
    b.append(path('M 82 42 C 98 58, 114 74, 126 88', YLINE, 2.4)); b.append(path('M 88 40 C 104 56, 118 72, 129 86', TEAL, 2.2))
    b.append(text(76, 66, 'yarn + cord', 9, 'end')); b.append(text(76, 77, 'held together', 9, 'end'))
    out.append(grp(PW, 0, ''.join(b)))
    b = [ptitle(3, 'Pull both through', ['One new stitch of yarn and cord;', 'slip the old stitch off.'])]
    ln3 = ln[1:]; base(b); b.append(needle(2, 100, 116, 100)); b.append(needle(198, 100, 128, 100))
    for x in rn + ln3: b.append(ell(x, 100, 4.5, 9))
    b.append(ell(101, 100, 5, 9.5, YLINE, 2.2)); b.append(ell(104, 100, 5, 9.5, TEAL, 2.0))
    b.append(arrow(118, 88, 118, 66, 1.0)); b.append(text(122, 62, 'old stitch off', 9, 'start'))
    b.append(text(92, 58, 'new stitch', 9, 'end', 'bold')); b.append(line(88, 62, 100, 88, 0.8))
    b.append(path('M 104 112 C 112 126, 102 140, 110 176', TEAL, 2.0)); b.append(path('M 100 112 C 92 128, 98 150, 88 178', TEAL, 2.0))
    b.append(text(84, 140, 'cord at', 8.5, 'end', c=TEAL)); b.append(text(84, 150, 'the back', 8.5, 'end', c=TEAL))
    out.append(grp(2 * PW, 0, ''.join(b)))
    b = [ptitle(4, 'Next row: lock it', ['Knit the stitch and its cord', 'loop together as one stitch.'])]
    base(b); b.append(needle(2, 100, 96, 100)); b.append(needle(198, 100, 110, 100))
    for x in rn: b.append(ell(x, 100, 4.5, 9))
    for x in ln[1:]: b.append(ell(x, 100, 4.5, 9))
    b.append(ell(118, 100, 5, 9.5, YLINE, 2.2)); b.append(ell(121, 100, 5, 9.5, TEAL, 2.0)); b.append(line(108, 92, 132, 108, 0.6, '#000'))
    b.append(text(100, 62, 'yarn loop + cord loop', 9, 'middle')); b.append(text(100, 73, 'knitted as one stitch', 9, 'middle')); b.append(line(112, 76, 120, 89, 0.8))
    out.append(grp(3 * PW, 0, ''.join(b)))
    foot = [text(4, PH - 4, 'Several cords at one stitch: hold them all with the yarn and work steps 2 to 4 once. A V is caught by its fold, held as one strand.', 9, 'start', c='#333'),
            mark(4 * PW - 4, PH - 4)]
    save('ck.svg', svg(4 * PW, PH + 4, ''.join(out + foot), 178))

# ---------------------------------------------------------------- Fig 4: the card gauge at true size, and the catch at card length
CARD_W, CARD_H = 90.0, 22.0; CARD_SVG_W = 160.0
def fig_card():
    # units = mm (viewBox in mm, printed width in mm = true size)
    Wm, Hm = CARD_SVG_W, 30.0; b = []
    x0, y0 = 4.0, 4.0
    b.append(rect(x0, y0, CARD_W, CARD_H, '#fbf7ec', '#000', 0.3))
    # notch at 0 (the end of the card) and at a; tail mark at a + 25
    b.append(poly([(x0 + a - 1.2, y0), (x0 + a + 1.2, y0), (x0 + a, y0 + 2.4)], '#fff', '#000', 0.25))
    b.append(line(x0 + a, y0, x0 + a, y0 + CARD_H, 0.25, '#000'))
    b.append(line(x0 + a + TAIL, y0, x0 + a + TAIL, y0 + CARD_H, 0.2, '#000', '0.8 0.8'))
    b.append(line(x0 + d, y0 + CARD_H, x0 + d, y0 + CARD_H - 5, 0.25, VIOL))
    b.append(line(x0, y0 + 0.2, x0, y0 + CARD_H - 0.2, 0.6, TEAL))
    b.append(line(x0 + 0.3, y0 + 7.0, x0 + a, y0 + 7.0, 0.5, TEAL))
    b.append(text(x0 + 1.2, y0 + 5.0, 'start: at the stitch or knot', 2.0, 'start'))
    b.append(text(x0 + a / 2, y0 + 10.6, f'a = {a:.1f} mm', 2.6, 'middle', 'bold', TEAL))
    b.append(text(x0 + a + 1.0, y0 + 5.0, 'catch here', 2.0, 'start', 'bold'))
    b.append(text(x0 + a + 1.0, y0 + 8.0, '(pinch the cord', 2.0, 'start'))
    b.append(text(x0 + a + 1.0, y0 + 10.6, 'at the notch)', 2.0, 'start'))
    b.append(text(x0 + a + TAIL + 1.0, y0 + 5.0, 'tail at least', 2.0, 'start'))
    b.append(text(x0 + a + TAIL + 1.0, y0 + 7.6, 'to here (25 mm)', 2.0, 'start'))
    b.append(text(x0 + d - 0.6, y0 + CARD_H - 2.0, f'd = {d:.1f} mm (check only)', 2.0, 'end', c=VIOL))
    b.append(text(x0 + CARD_W - 1.5, y0 + CARD_H - 2.0, 'DICTO · card gauge · cut on the outline', 1.9, 'end', 'bold', '#b8962e'))
    # print check bar
    bx = x0 + CARD_W + 8; b.append(line(bx, y0 + 4, bx + 50, y0 + 4, 0.4)); b.append(line(bx, y0 + 2.5, bx, y0 + 5.5, 0.4)); b.append(line(bx + 50, y0 + 2.5, bx + 50, y0 + 5.5, 0.4))
    for q in range(1, 5): b.append(line(bx + 10 * q, y0 + 3.2, bx + 10 * q, y0 + 4.8, 0.25))
    check(bx + 50 + 1 < Wm and x0 + CARD_W < bx, f'card figure: card {CARD_W:.0f} mm and 50 mm check bar lie inside the {Wm:.0f} mm wide drawing (printed at true size)')
    b.append(text(bx + 25, y0 + 9.0, 'print check: this bar is 50 mm', 2.1))
    b.append(text(bx + 25, y0 + 12.0, '(print at 100 %, not "fit to page")', 2.0, c='#444'))
    save('card.svg', svg(Wm, Hm, ''.join(b), Wm))

def fig_catch():
    PW, PH = 200, 196; out = []
    def sheets(b, ypin=150):
        b.append(line(30, 46, 30, 186, 3, '#6f6a5e')); b.append(text(26, 196 - 2, 'earlier', 8, 'middle', c='#555'))
        b.append(needle(130, 70, 196, 70)); b.append(line(150, 76, 150, 186, 3, '#6f6a5e')); b.append(text(150, 196 - 2, 'on the needle', 8, 'middle', c='#555'))
        for x in (140, 156, 172, 188): b.append(ell(x, 70, 4, 8))
        b.append(circ(30, ypin, 3.2, '#000'))
    b = [ptitle(1, 'Lay the card on the cord', ['Card end at the stitch (or knot)', 'where the cord leaves the sheet.'])]
    sheets(b)
    b.append(path('M 31 150 C 70 140, 80 120, 96 100 C 104 90, 110 84, 112 76', TEAL, 2.0))
    b.append(poly([(34, 150), (34 + 90 * math.cos(-0.72), 150 + 90 * math.sin(-0.72)), (34 + 90 * math.cos(-0.72) + 12 * math.sin(0.72), 150 + 90 * math.sin(-0.72) + 12 * math.cos(0.72)), (34 + 12 * math.sin(0.72), 150 + 12 * math.cos(0.72))], '#fbf7ec', '#000', 0.9))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Pinch at the notch', ['Cord straight along the card', 'edge under a light pull.'])]
    sheets(b)
    ang = -0.62; L = 120; ex, ey = 34 + L * math.cos(ang), 150 + L * math.sin(ang)
    b.append(poly([(32, 150), (32 + 100 * math.cos(ang), 150 + 100 * math.sin(ang)), (32 + 100 * math.cos(ang) + 14 * math.sin(-ang), 150 + 100 * math.sin(ang) + 14 * math.cos(ang)), (32 + 14 * math.sin(-ang), 150 + 14 * math.cos(ang))], '#fbf7ec', '#000', 0.9))
    b.append(line(31, 150, ex, ey, 2.0, TEAL))
    nx, ny = 32 + 0.404 * 100 * math.cos(ang), 150 + 0.404 * 100 * math.sin(ang)
    b.append(circ(nx, ny, 5, 'none', '#000', 1.2)); b.append(text(nx + 8, ny + 18, 'notch a', 9, 'start', 'bold'))
    b.append(text(nx - 6, ny - 10, 'pinch', 9, 'end'))
    out.append(grp(PW, 0, ''.join(b)))
    b = [ptitle(3, 'Knit the pinch point in', ['Keep the pinch; work the node', 'stitch with yarn and cord (CK).'])]
    sheets(b)
    b.append(path('M 31 150 C 80 140, 120 110, 140 80', TEAL, 2.0)); b.append(circ(140, 80, 3.5, 'none', '#000', 1.1))
    b.append(path('M 140 80 C 150 96, 146 112, 154 128', TEAL, 2.0)); b.append(text(158, 126, 'tail', 9, 'start', c=TEAL))
    b.append(ell(140, 70, 4.6, 8.6, '#000', 2.0))
    out.append(grp(2 * PW, 0, ''.join(b)))
    b = [ptitle(4, 'Knot the tail', ['Stopper knot in the tail, snug', 'against the back of the stitch.'])]
    sheets(b)
    b.append(path('M 31 150 C 80 140, 120 110, 140 80', TEAL, 2.0)); b.append(ell(140, 70, 4.6, 8.6, '#000', 2.0))
    b.append(circ(146, 88, 4.2, TEAL)); b.append(path('M 147 92 C 150 102, 148 108, 152 114', TEAL, 2.0))
    b.append(text(158, 96, 'knot', 9, 'start', 'bold', TEAL))
    out.append(grp(3 * PW, 0, ''.join(b)))
    foot = [text(4, PH + 10, 'Side view, the sheets drawn apart for clarity; on the needles they lie close and the measured cord hangs in a slack loop.', 9, 'start', c='#333'),
            mark(4 * PW - 4, PH + 10)]
    save('catch.svg', svg(4 * PW, PH + 16, ''.join(out + foot), 178))

# ---------------------------------------------------------------- Fig 5: stopper knot and V knot; the two cord pieces
def fig_knot():
    PW, PH = 160, 150; out = []
    def stitch(b, x=40, y=100):
        b.append(garter(4, y - 8, 5, 2, 15)); b.append(ell(x, y, 5, 9, '#000', 2.0))
    b = [ptitle(1, 'Loop the tail', ['Make a loop in the tail', 'close to the stitch.'])]
    stitch(b); b.append(path('M 40 108 C 48 70, 92 64, 98 84 C 104 104, 70 112, 64 92 C 60 78, 82 60, 120 46', TEAL, 2.0))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Tuck the end through', ['Pass the end through the', 'loop (an overhand knot).'])]
    stitch(b); b.append(path('M 40 108 C 46 84, 70 70, 86 78 C 100 86, 92 102, 76 96 C 66 92, 74 74, 96 70 C 112 68, 124 80, 136 96', TEAL, 2.0))
    out.append(grp(PW, 0, ''.join(b)))
    b = [ptitle(3, 'Slide it home', ['Guide the knot to the stitch', 'with a needle tip; pull tight.'])]
    stitch(b); b.append(path('M 40 108 C 44 98, 46 92, 50 88', TEAL, 2.0)); b.append(circ(53, 85, 4.4, TEAL))
    b.append(path('M 56 82 C 70 70, 86 70, 100 74', TEAL, 2.0)); b.append(line(110, 40, 60, 80, 3.5, '#7a7466'))
    b.append(text(154, 140, 'trim tails to 5 mm', 8.5, 'end', c='#333')); b.append(text(154, 150, 'at finishing', 8.5, 'end', c='#333'))
    out.append(grp(2 * PW, 0, ''.join(b)))
    b = [ptitle(4, 'V knot', ['After catching a V fold: tie both', 'arms together in one overhand.'])]
    stitch(b); b.append(circ(48, 84, 5, TEAL))
    b.append(path('M 40 100 C 42 94, 44 90, 46 88', TEAL, 2.0)); b.append(path('M 51 80 C 70 60, 100 54, 140 50', TEAL, 2.0)); b.append(path('M 52 84 C 76 80, 110 86, 146 92', TEAL, 2.0))
    b.append(text(150, 64, 'arm 1', 8.5, 'end', c=TEAL)); b.append(text(146, 106, 'arm 2', 8.5, 'end', c=TEAL))
    out.append(grp(3 * PW, 0, ''.join(b)))
    foot = [text(4, PH + 8, 'If a knot pulls through the stitch, tie a second overhand on top of the first.', 9, 'start', c='#333'), mark(4 * PW - 4, PH + 8)]
    save('knot.svg', svg(4 * PW, PH + 12, ''.join(out + foot), 178))

def fig_pieces():
    Wd, Hd = 330, 70; b = []; s = 1.6   # px per mm
    x0 = 10
    b.append(text(x0, 14, f'V piece: cut {cutV} cm', 10, 'start', 'bold'))
    L = cutV * 10 * s / 2
    b.append(line(x0, 30, x0 + L * 0.95, 30, 2.2, TEAL)); b.append(line(x0, 34, x0 + L * 0.95, 34, 2.2, TEAL))
    b.append(path(f'M {x0 + L * 0.95} 30 A 2 2 0 0 1 {x0 + L * 0.95} 34', TEAL, 2.2))
    b.append(text(x0 + L * 0.95 + 6, 35, 'fold', 9, 'start')); b.append(text(x0, 50, 'fold caught first, then each arm', 8.5, 'start', c='#333'))
    x1 = 196
    b.append(text(x1, 14, f'single: cut {cutS} cm', 10, 'start', 'bold'))
    b.append(line(x1, 32, x1 + cutS * 10 * s * 0.75, 32, 2.2, TEAL)); b.append(text(x1, 50, 'first end (2.5 cm tail), far end', 8.5, 'start', c='#333'))
    b.append(text(Wd - 4, Hd - 6, 'not to scale', 8, 'end', c='#666')); b.append(mark(Wd - 4, 12))
    save('pieces.svg', svg(Wd, Hd, ''.join(b), 84))

# ---------------------------------------------------------------- Fig 6: the node chart (all three sheets on one chart, plan view)
SYM = {0: 'circle', 1: 'square', 2: 'triangle'}
def sym(k, x, y, r=4.2, fill='#fff'):
    if k == 0: return circ(x, y, r, fill, '#000', 1.3)
    if k == 1: return rect(x - r * 0.85, y - r * 0.85, 1.7 * r, 1.7 * r, fill, '#000', 1.3)
    return poly([(x, y - r * 1.05), (x + r, y + r * 0.75), (x - r, y + r * 0.75)], fill, '#000', 1.3)
def fig_chart():
    s = 11.0; X0, Y0 = 40, 22; Wd = X0 + W * s + 76; Hd = Y0 + H * s + 74
    X = lambda sn: X0 + (W - sn) * s + s / 2
    Y = lambda r: Y0 + (H - r) * s + s / 2
    b = [rect(X0, Y0, W * s, H * s, '#fff', '#000', 1.0)]
    for c in range(1, W): b.append(line(X0 + c * s, Y0, X0 + c * s, Y0 + H * s, 0.3, '#bbb'))
    for r in range(1, H): b.append(line(X0, Y0 + r * s, X0 + W * s, Y0 + r * s, 0.3, '#bbb'))
    node_r = sorted({n['ridge'] for n in ALL})
    for r in node_r:
        k = [n['k'] for n in ALL if n['ridge'] == r][0]
        b.append(rect(X0, Y(r) - s / 2, W * s, s, ['#f2efe8', '#f6efd9', '#eeeaf4'][k], 'none', 0))
    for c in range(1, W): b.append(line(X0 + c * s, Y0, X0 + c * s, Y0 + H * s, 0.3, '#bbb'))
    for sn in [1, 4, 8, 12, 16, 20, 24, 28, 32, 35]:
        b.append(text(X(sn), Y0 + H * s + 11, str(sn), 7.5)); b.append(text(X(sn), Y0 - 4, str(sn), 7.5))
    for r in [1] + node_r + [H]:
        k = [n['k'] for n in ALL if n['ridge'] == r]
        b.append(text(X0 - 4, Y(r) + 3, str(r), 7.5, 'end', 'bold' if k else 'normal'))
        if k: b.append(text(X0 + W * s + 4, Y(r) + 3, f"{'ABC'[k[0]]}  " + ('row 1' if k[0] == 0 else 'row 2' if k[0] == 2 else 'rows 1 + 2'), 7.5, 'start', 'bold'))
    b.append(text(X0 - 26, Y0 + H * s / 2, 'ridge', 8.5, 'middle', rot=-90))
    b.append(text(X0 + W * s / 2, Y0 + H * s + 24, 'stitch number (stitch 1 at the right, where row 1 starts) · cast-on edge at the bottom', 8.5))
    for gi, g in enumerate(G):
        for u, v in g:
            b.append(line(X(u['s']), Y(u['ridge']), X(v['s']), Y(v['ridge']), 1.4 if gi == 0 else 1.4, TEAL, None if gi == 0 else '4 2.5'))
    for n in ALL: b.append(sym(n['k'], X(n['s']), Y(n['ridge'])))
    for p in pieces:
        f = p['first']; dy = 8.5 if p['row1'] == 1 else -5.5
        b.append(text(X(f['s']) + (6 if p['gap'] == 1 else -6), Y(f['ridge']) + (8.8 if p['gap'] == 1 else -5.0), p['id'], 6.2, 'start' if p['gap'] == 1 else 'end', 'bold', '#0d5f56'))
    lx = X0; ly = Y0 + H * s + 40
    for k in range(3):
        b.append(sym(k, lx + 5 + 70 * k, ly)); b.append(text(lx + 13 + 70 * k, ly + 3, f"sheet {'ABC'[k]} node", 8, 'start'))
    b.append(line(lx + 214, ly, lx + 228, ly, 1.4, TEAL)); b.append(text(lx + 232, ly + 3, 'link A-B', 8, 'start'))
    b.append(line(lx + 280, ly, lx + 294, ly, 1.4, TEAL, '4 2.5')); b.append(text(lx + 298, ly + 3, 'link B-C', 8, 'start'))
    b.append(text(lx, ly + 18, 'V3, S5: cord piece, written beside the stitch of its first catch', 8, 'start', c='#0d5f56'))
    b.append(mark(Wd - 4, Hd - 4))
    save('chart.svg', svg(Wd, Hd, ''.join(b), 172))

# ---------------------------------------------------------------- Fig 7: the checks
def fig_check():
    PW, PH = 240, 150; out = []
    def patch(b, x, y, wdt=150, sink=0, shift=0):
        ys = [y, y - 26 + sink / 2, y - 52 + sink]
        for i, yy in enumerate(ys):
            off = shift * i / 2
            b.append(rect(x + off, yy - 3, wdt, 6, SHEET_FILL['ABC'[i]], '#6f6a5e', 0.8))
        for j in range(5):
            xx = x + 14 + j * 30
            b.append(line(xx, ys[0] - 3, xx + 12 + shift / 2, ys[1] + 3, 1.2, TEAL)); b.append(line(xx + 12 + shift / 2, ys[1] - 3, xx + 24 + shift, ys[2] + 3, 1.2, TEAL))
        return ys
    b = [ptitle(1, 'Measure', ['Wool test fill in both gaps; every', 'cord just taut. Ruler upright.'])]
    b.append(rect(10, 128, 200, 6, '#ddd', '#666', 0.6))
    ys = patch(b, 30, 120); b.append(line(196, 126, 196, 50, 1.0)); [b.append(line(193, yy, 199, yy, 0.6)) for yy in range(54, 126, 6)]
    b.append(text(204, (ys[0] + ys[1]) / 2 + 3, f'd {d:.1f}', 8.5, 'start')); b.append(text(204, (ys[1] + ys[2]) / 2 + 3, f'd {d:.1f}', 8.5, 'start'))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Press', ['Board, then 5 kg bag of rice;', 'read the sink on the ruler.'])]
    b.append(rect(10, 128, 200, 6, '#ddd', '#666', 0.6))
    ys = patch(b, 30, 120, sink=14); b.append(rect(40, ys[2] - 9, 130, 6, '#b9a77d', '#555', 0.7)); b.append(rect(70, ys[2] - 40, 70, 31, '#eee', '#555', 0.7, 6))
    b.append(text(105, ys[2] - 21, '5 kg', 9, 'middle', 'bold')); b.append(line(196, 126, 196, 46, 1.0))
    out.append(grp(PW, 0, ''.join(b)))
    b = [ptitle(3, 'Shear', ['Same load; pull the board sideways', 'with a luggage scale; read the shift.'])]
    b.append(rect(10, 128, 200, 6, '#ddd', '#666', 0.6)); b.append(rect(22, 112, 6, 16, '#999', '#555', 0.6))
    ys = patch(b, 30, 120, sink=14, shift=16); b.append(rect(56, ys[2] - 9, 130, 6, '#b9a77d', '#555', 0.7)); b.append(rect(86, ys[2] - 40, 70, 31, '#eee', '#555', 0.7, 6))
    b.append(text(121, ys[2] - 21, '5 kg', 9, 'middle', 'bold')); b.append(arrow(188, ys[2] - 6, 228, ys[2] - 6, 1.2))
    b.append(text(226, ys[2] + 8, 'scale', 8.5, 'end')); b.append(text(16, 108, 'stop', 8, 'start', c='#555'))
    out.append(grp(2 * PW, 0, ''.join(b)))
    foot = [mark(3 * PW - 4, PH - 4)]
    save('check.svg', svg(3 * PW, PH, ''.join(out + foot), 172))

for f in (fig_make, fig_instep, fig_ck, fig_card, fig_catch, fig_knot, fig_pieces, fig_chart, fig_check): f()
log('figures written')

# ---------------------------------------------------------------- the ridge table and the link table (HTML)
SN = ['A', 'B', 'C']
def where(n, row): return f"{SN[n['k']]} st {n['s']}" + (f" ({W + 1 - n['s']}th)" if row == 2 else '') + f", ridge {n['ridge']} row {row}"
def catch_text(key):
    items = sorted(CAT[key], key=lambda q: (q[1] != 'first', q[0]['id']))
    parts = []
    for p, w in items:
        if w == 'first': parts.append(f"<b>{p['id']}</b> fold (new {cutV} cm cord)" if p['kind'] == 'V' else f"<b>{p['id']}</b> first end (new {cutS} cm cord)")
        else: parts.append(f"{p['id']} {'arm' if p['kind'] == 'V' else 'end'} at card")
    return ' + '.join(parts)
def ordinal(i): return f"{i}{'th' if 10 <= i % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(i % 10, 'th')}"
rows_html = []; plain = []
def flush_plain():
    if plain:
        rng = f"{plain[0]}" if len(plain) == 1 else f"{plain[0]}–{plain[-1]}"
        rows_html.append(f'<tr class="plain"><td class="r">{rng}</td><td colspan="2">knit, all three sheets in step</td></tr>'); plain.clear()
n_entries = 0
for r in range(1, H + 1):
    cells = {1: [], 2: []}
    for row in (1, 2):
        order = (0, 1, 2) if row == 1 else (2, 1, 0)
        for k in order:
            ks = sorted([key for key in CAT if key[0] == r and key[1] == row and key[2] == k], key=lambda q: q[3] if row == 1 else -q[3])
            if ks:
                n_entries += 1
                parts = [(f"st {q[3]}" if row == 1 else f"st {q[3]} ({ordinal(W + 1 - q[3])} of the row)") + f": {catch_text(q)}" for q in ks]
                cells[row].append(f'<div><span class="sh">{SN[k]}</span> ' + '; '.join(parts) + '</div>')
    if not cells[1] and not cells[2]: plain.append(r); continue
    flush_plain()
    rows_html.append(f'<tr><td class="r">{r}</td><td>{"".join(cells[1]) or "knit"}</td><td>{"".join(cells[2]) or "knit"}</td></tr>')
flush_plain()
check(n_entries == 16, 'ridge table: 16 sheet-rows with catches (A and C 4 each, B 8)')
RIDGE_TABLE = '\n'.join(rows_html)
def tick(): return '<span class="box"></span>'
lt = []
for p in pieces:
    far = ''.join(f"<div>{tick()} {SN[n['k']]} st {n['s']}, r {n['ridge']}/{p['rowf']}</div>" for n in p['far'])
    lt.append(f"<tr><td><b>{p['id']}</b></td><td>{p['gap']}</td><td>{cutV if p['kind'] == 'V' else cutS}</td><td>{tick()} {SN[p['first']['k']]} st {p['first']['s']}, r {p['first']['ridge']}/{p['row1']}</td><td>{far}</td></tr>")
half = (len(lt) + 1) // 2
def lt_table(rows): return ('<table class="lt"><tr><th>piece</th><th>gap</th><th>cm</th><th>first catch</th><th>far catch at card</th></tr>' + ''.join(rows) + '</table>')
LINK_TABLES = f'<div class="cols2">{lt_table(lt[:half])}{lt_table(lt[half:])}</div>'
check(sum(1 + len(p['far']) for p in pieces) == NCATCH, f'link table: {NP} pieces, {NCATCH} tick boxes for catches')
h_rows = ''.join(f"<tr><td>{r}</td><td>{', '.join(map(str, s_))}</td><td>{rc}</td><td>{', '.join(map(str, sc))}</td></tr>" for (r, s_), (rc, sc) in zip(H3, C3))

# ---------------------------------------------------------------- numbers file and log
json.dump(dict(a=a, d=d, W=W, H=H, size_mm=[W_mm, H_mm], nodes=[16, 16, 16], links=nl, pieces=NP, V=NV, single=NSI, catches=NCATCH,
               straight=NSTRAIGHT, cut_cm=dict(V=cutV, single=cutS), cord_m=cord_m, yarn_m=yarn_m, fill_g=[fill_lo, fill_hi], hours=mins / 60,
               press_kpa=press_kpa, h=dict(links=nlh, pieces=pieces_h, sheet3=H3),
               table=[dict(id=p['id'], gap=p['gap'], first=[SN[p['first']['k']], p['first']['s'], p['first']['ridge'], p['row1']],
                           far=[[SN[n['k']], n['s'], n['ridge'], p['rowf']] for n in p['far']]) for p in pieces]),
          open(DATA + '/patch.json', 'w'), indent=1)

# ---------------------------------------------------------------- the pattern (HTML)
V = dict(a=f'{a:.1f}', d=f'{d:.1f}', W=W, H=H, Wc=f'{W_mm / 10:.1f}', Hc=f'{H_mm / 10:.1f}', depth=f'{(2 * d + t) / 10:.1f}', NL=NL, nl0=nl[0], nl1=nl[1],
         NV=NV, NSI=NSI, NP=NP, NC=NCATCH, cutV=cutV, cutS=cutS, cord=f'{cord_m:.1f}', yarn=f'{yarn_m:.0f}', ysheet=f'{yarn_m / 3:.0f}',
         fill=f'{5 * round(fill_lo / 5):.0f}–{5 * round(fill_hi / 5):.0f}', fillgap=f'{5 * round(fill_lo / 10):.0f}–{5 * round(fill_hi / 10):.0f}', hours=f'{mins / 60:.0f}',
         kpa=f'{press_kpa:.1f}', straight=NSTRAIGHT, tilt=f'{TILT:.2f}', e23=f'{row_err[23]:+.1f} %', e22=f'{row_err[22]:+.1f} %', e21=f'{row_err[21]:+.1f} %',
         row3=f'{3 * M * rg:.1f}', row3t=f'{3 * pitch_true:.1f}', sp3=f'{3 * a:.1f}', board=f'{BOARD / 10:.0f}', nlh=sum(nlh), ph=pieces_h, span=span,
         nt=nt, no=no, maxc=maxc, cordbuy=math.ceil(cord_m * 1.2), cardw=f'{CARD_W:.0f}', cardsvgw=f'{CARD_SVG_W:.0f}', cardh=f'{CARD_H:.0f}')
html = open(os.path.join(os.path.dirname(__file__), 'pattern.src.html')).read()
for k_, v_ in V.items(): html = html.replace('{{' + k_ + '}}', str(v_))
html = html.replace('{{RIDGE_TABLE}}', RIDGE_TABLE).replace('{{LINK_TABLES}}', LINK_TABLES).replace('{{H_ROWS}}', h_rows)
assert '{{' not in html, 'unfilled placeholder: ' + html[html.index('{{'):html.index('{{') + 30]
open(OUT + '/paper.html', 'w').write(html)
check(True, 'paper.html written, every placeholder filled')
open(DATA + '/check.out', 'w').write('\n'.join(LOG) + '\n')
