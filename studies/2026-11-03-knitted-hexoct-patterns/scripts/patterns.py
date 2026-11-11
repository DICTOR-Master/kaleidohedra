# Knitted HexOct: Patterns (DICTO's Knitted HexOct, spec of 2026-11-02). Builds every number, chart, table and figure of the
# pattern booklet from the spec's formulas, with exact checks, and writes paper.html, figs/*.svg and data/check.out.
# Run on compute-host with python3:  python patterns.py <out dir> <dir holding tiles.py, engine.py, stackings.py>
# (the #75 scripts of studies/2026-10-29-endless-stack-cell, as for the spec's check.py).
import itertools, math, os, sys
from fractions import Fraction as Fr
import sympy as sp

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else '.'))
FIGS, DATA = os.path.join(OUT, 'figs'), os.path.join(OUT, 'data')
os.makedirs(FIGS, exist_ok=True); os.makedirs(DATA, exist_ok=True)
LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s); LOG.append(s)

# ---------------------------------------------------------------- spec §2(a): gauge rules and the sheet
N, M = 16, 14                      # node spacing a = N stitches; node rows M ridges apart (square garter gauge)
S_REF, R_REF, T_REF = 22, 22, 3.5  # reference gauge (sts and ridges per 10 cm) and sheet thickness (mm), spec §2-3
COLS, RIDGES = 4 * N, 3 * M
ROWS = 2 * RIDGES
def node_ridge(j): return (M + 1) // 2 + j * M
def node_row(j): return 2 * node_ridge(j) - 1          # the RS row of that ridge (row 1 = RS)
def node_st(i, j): return N // 2 + 1 + N * i + (N // 2) * j
assert all(node_st(i, j) == 9 + 16 * i + 8 * j for i in range(3) for j in range(3))      # spec: stitches 9 + 16i + 8j
assert [node_ridge(j) for j in range(3)] == [7, 21, 35] and [node_row(j) for j in range(3)] == [13, 41, 69]
assert M == round(0.866 * N * R_REF / S_REF) and N % 2 == 0
a_mm = 100 * N / S_REF                                   # 72.7 mm
d_mm = math.sqrt(2 / 3) * a_mm
ell_mm = lambda t: a_mm - 2 * t / (2 * math.sin(math.atan(math.sqrt(2))))   # spec: l = a - 1.22 t
assert abs(2 / (2 * math.sin(math.atan(math.sqrt(2)))) - 1.2247) < 1e-4
log(f"gauge: N={N}, M={M}, cast on {COLS}, {RIDGES} ridges = {ROWS} rows; node rows {[node_row(j) for j in range(3)]}, "
    f"node stitches {[[node_st(i, j) for i in range(3)] for j in range(3)]}")
log(f"reference sizes: a = {a_mm:.1f} mm, d = {d_mm:.1f} mm, l(t=3.5) = {ell_mm(3.5):.1f} mm")

# ---------------------------------------------------------------- spec §1: exact link geometry
POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
def norm2(u, v): return u * u + u * v + v * v
def up_links(lo, hi):
    out = []
    for di, dj in itertools.product(range(-2, 3), repeat=2):
        u, v = POS[hi][0] + di - POS[lo][0], POS[hi][1] + dj - POS[lo][1]
        if norm2(u, v) == Fr(1, 3): out.append((di, dj, u, v))
    assert len(out) == 3; return out
FWD, BWD = {(0, 0), (-1, 0), (0, -1)}, {(0, 0), (1, 0), (0, 1)}
for lo, hi in [('A', 'B'), ('B', 'C')]:   # the steps used here (C -> A wraps the origin by a lattice vector)
    assert {(x[0], x[1]) for x in up_links(lo, hi)} == FWD
    assert {(x[0], x[1]) for x in up_links(hi, lo)} == BWD
d = sp.sqrt(sp.Rational(2, 3))
for lo, hi in [('A', 'B'), ('B', 'A')]:
    for _, _, u, v in up_links(lo, hi):
        h2 = sp.Rational(norm2(u, v).numerator, norm2(u, v).denominator)
        assert sp.simplify(h2 + d ** 2 - 1) == 0 and sp.simplify(sp.atan(d / sp.sqrt(h2)) - sp.atan(sp.sqrt(2))) == 0
TILT = math.degrees(math.atan(math.sqrt(2)))
log(f"links: length a, tilt atan(sqrt 2) = {TILT:.4f} deg, sheet spacing sqrt(2/3) a (exact)")
def st_r(u, v): return N * (u + v / 2), M * v               # plan offset in stitches and ridges (ideal gauge)
assert {st_r(u, v) for _, _, u, v in up_links('A', 'B')} == {(Fr(8), Fr(14, 3)), (Fr(-8), Fr(14, 3)), (Fr(0), Fr(-28, 3))}
# c / h at sheet B: links up vs links down (plan vectors)
down = {(-u, -v) for _, _, u, v in up_links('A', 'B')}       # B -> A, plan part (falling)
upc = {(u, v) for _, _, u, v in up_links('B', 'C')}
uph = {(u, v) for _, _, u, v in up_links('B', 'A')}
assert all((-u, -v) in down for u, v in upc)                 # c: each link up is the straight continuation of a link down
assert uph == down                                           # h: each link up is the mirror image (in the sheet) of a link down
log("c: 3/3 links up collinear with a link down; h: 3/3 links up mirror a link down")

# any stacking word: each gap is a forward step (A->B, B->C, C->A: the upper sheet moves on by (1/3, 1/3)) or a backward step
NEXT = {'A': 'B', 'B': 'C', 'C': 'A'}
def steps_of(word):
    out = []
    for k in range(len(word) - 1):
        assert word[k] != word[k + 1] and word[k] in NEXT
        out.append(1 if word[k + 1] == NEXT[word[k]] else -1)
    return out
def offsets_of(word):
    o = [Fr(0)]
    for s in steps_of(word): o.append(o[-1] + Fr(s, 3))
    return o
def step_links(s): return [(di, dj, Fr(s, 3) + di, Fr(s, 3) + dj) for di, dj in sorted(FWD if s > 0 else BWD)]
assert set(step_links(1)) == set(up_links('A', 'B')) == set(up_links('B', 'C'))
assert set(step_links(-1)) == set(up_links('B', 'A')) == set(up_links('C', 'B'))
assert all(norm2(u, v) == Fr(1, 3) for s in (1, -1) for _, _, u, v in step_links(s))
def ch_of(word):   # c/h of the inner sheets: c when its two neighbours differ (equivalently: equal steps below and above)
    out = ''.join('c' if word[k - 1] != word[k + 1] else 'h' for k in range(1, len(word) - 1))
    st = steps_of(word); assert out == ''.join('c' if st[k - 1] == st[k] else 'h' for k in range(1, len(word) - 1))
    return out
def letters_from(inner):   # rule: sheets 1, 2 = A, B; next sheet = the third letter after c, the letter two below after h
    w = 'AB'
    for x in inner: w += ({'A', 'B', 'C'} - {w[-1], w[-2]}).pop() if x == 'c' else w[-2]
    return w
def rule_pairs(s):   # node numbers 1 + i + 3j: forward n -> n, n-1, n-3; backward n -> n, n+1, n+3 (inside the 3 x 3 patch)
    out = set()
    for n in range(1, 10):
        out.add((n, n))
        if s > 0:
            if n % 3 != 1: out.add((n, n - 1))
            if n > 3: out.add((n, n - 3))
        else:
            if n % 3 != 0: out.add((n, n + 1))
            if n <= 6: out.add((n, n + 3))
    return out
assert len(rule_pairs(1)) == len(rule_pairs(-1)) == 21

def frac(x):
    x = Fr(x); s = '−' if x < 0 else '+'; x = abs(x); w, r = divmod(x.numerator, x.denominator)
    f = {Fr(1, 3): '⅓', Fr(2, 3): '⅔'}.get(Fr(r, x.denominator), '' if r == 0 else f'{r}/{x.denominator}')
    return s + (str(w) if w or not f else '') + f
def fr0(x): return '0' if x == 0 else frac(x)

# ---------------------------------------------------------------- spec §3: the two test pieces
PIECES = {'T-c': dict(word='ABC', names=['A', 'B', 'C'], kind='c'),
          'T-h': dict(word='ABA', names=['A', 'B', 'A′'], kind='h')}
for P in PIECES.values(): P['off'] = offsets_of(P['word']); P['steps'] = steps_of(P['word'])
assert [(o, o) for o in PIECES['T-c']['off']] == [POS[w] for w in 'ABC'] and [(o, o) for o in PIECES['T-h']['off']] == [POS[w] for w in 'ABA']
EXPECT_DEG = {'ABC': [[[1, 2, 2], [2, 3, 3], [2, 3, 3]], [[4, 5, 4], [5, 6, 5], [4, 5, 4]], [[3, 3, 2], [3, 3, 2], [2, 2, 1]]],
              'ABA': [[[1, 2, 2], [2, 3, 3], [2, 3, 3]], [[6, 6, 4], [6, 6, 4], [4, 4, 2]], [[1, 2, 2], [2, 3, 3], [2, 3, 3]]]}
def lab(P, n): k, i, j = n; return f"{P['names'][k]}{1 + i + 3 * j}"
def lat(P, n): k, i, j = n; o = P['off'][k]; return (o + i, o + j, Fr(k))
def build(P):
    ns = len(P['word'])
    nodes = [(k, i, j) for k in range(ns) for j in range(3) for i in range(3)]
    links = []
    for k in range(ns - 1):
        for j in range(3):
            for i in range(3):
                row = []
                for di, dj, u, v in step_links(P['steps'][k]):
                    if 0 <= i + di < 3 and 0 <= j + dj < 3: row.append(((k, i, j), (k + 1, i + di, j + dj), u, v))
                links += sorted(row, key=lambda x: 1 + x[1][1] + 3 * x[1][2])
        gl = [x for x in links if x[0][0] == k]
        assert len(gl) == 21 and {(1 + x[0][1] + 3 * x[0][2], 1 + x[1][1] + 3 * x[1][2]) for x in gl} == rule_pairs(P['steps'][k])
    deg = {n: 0 for n in nodes}
    for x in links: deg[x[0]] += 1; deg[x[1]] += 1
    assert len(nodes) == 9 * ns and len(links) == 21 * (ns - 1) and sum(deg.values()) == 2 * len(links)
    if P['word'] in EXPECT_DEG and ns == 3:
        assert [[[deg[(k, i, j)] for i in range(3)] for j in range(3)] for k in range(3)] == EXPECT_DEG[P['word']]
    for x in links:                                           # every link: length a in the exact lattice
        p, q = lat(P, x[0]), lat(P, x[1])
        assert norm2(q[0] - p[0], q[1] - p[1]) == Fr(1, 3)
    return nodes, links, deg

def cells(P, links):
    L = {(x[0], x[1]) for x in links}
    def tris(k):
        out = []
        for i, j in itertools.product(range(2), repeat=2):
            out.append(((k, i, j), (k, i + 1, j), (k, i, j + 1)))
            out.append(((k, i + 1, j), (k, i, j + 1), (k, i + 1, j + 1)))
        return out
    C = []
    for g in range(len(P['word']) - 1):
        lo = [(g, i, j) for i in range(3) for j in range(3)]; hi = [(g + 1, i, j) for i in range(3) for j in range(3)]
        for T in tris(g):
            for n in hi:
                if all((t, n) in L for t in T): C.append(dict(kind='tet', gap=g, base=g, nodes=list(T) + [n]))
        for T in tris(g + 1):
            for n in lo:
                if all((n, t) in L for t in T): C.append(dict(kind='tet', gap=g, base=g + 1, nodes=list(T) + [n]))
        for T1 in tris(g):
            for T2 in tris(g + 1):
                ls = [(p, q) for p in T1 for q in T2 if (p, q) in L]
                if len(ls) == 6: C.append(dict(kind='oct', gap=g, lo=list(T1), hi=list(T2), links=ls))
    return C
def cell_counts(P, C):
    return {g: dict(tet_lo=sum(1 for c in C if c['kind'] == 'tet' and c['gap'] == g and c['base'] == g),
                    tet_hi=sum(1 for c in C if c['kind'] == 'tet' and c['gap'] == g and c['base'] == g + 1),
                    oct=sum(1 for c in C if c['kind'] == 'oct' and c['gap'] == g)) for g in range(len(P['word']) - 1)}
import tiles   # #75 tiles (exact rationals)
TILE_WORD = {'T-c': 'ABC', 'T-h': 'AB'}
def tile_check(name, P, C):
    pieces, _ = tiles.tile(TILE_WORD[name], 1, Fr(-1, 8))
    assert sorted(p[0] for p in pieces) == ['oct', 'oct', 'tet', 'tet']
    found = []
    for i0, j0 in itertools.product(range(3), repeat=2):
        o = lat(P, (1, i0, j0))
        def rel(n): p = lat(P, n); return (p[0] - o[0], p[1] - o[1], p[2] - o[2])
        hit = []
        for k, up, s, Pts, J in pieces:
            S = set(Pts); m = None
            for ci, c in enumerate(C):
                if k == 'tet' and c['kind'] == 'tet' and len(S) == 4 and S == {rel(n) for n in c['nodes']}: m = ci
                if k == 'oct' and c['kind'] == 'oct':
                    tri = c['hi'] if c['gap'] == 0 else c['lo']           # the B triangle of this octahedron
                    if (c['gap'] == 0) != bool(up): continue                # up=True: top half of the gap below B
                    mids = set()
                    for p, q in c['links']:
                        a_, b_ = rel(p), rel(q); mids.add(tuple((a_[r] + b_[r]) / 2 for r in range(3)))
                    if S == {rel(n) for n in tri} | mids and len(S) == 9: m = ci
            hit.append(m)
        if all(h is not None for h in hit): found.append(((i0, j0), hit))
    assert found, name
    return found

def owner(c):   # which sheet's tile a cell (or half) belongs to
    if c['kind'] == 'tet': return [c['base']]
    return [c['gap'], c['gap'] + 1]    # lower half -> lower sheet, upper half -> upper sheet

R = {}
for name, P in PIECES.items():
    nodes, links, deg = build(P); C = cells(P, links)
    cnt = cell_counts(P, C)
    found = tile_check(name, P, C)
    full = [lab(P, (1, i, j)) for (i, j), _ in found]
    R[name] = dict(P=P, nodes=nodes, links=links, deg=deg, C=C, cnt=cnt, full=full)
    log(f"{name} ({P['word']}): nodes 27, links 42 (21 + 21), degrees as spec check.out; cells gap 1 {cnt[0]}, gap 2 {cnt[1]}; "
        f"#75 tile of the middle sheet at lambda=-1/8 found complete as cells around {full}")


# ---------------------------------------------------------------- stacking sequences of #83 (papers/hexoct-knitting)
# #83 v3 (paper.src.html, "Five swatches"): name, A/B/C word, c/h labels as printed there (one per layer; the 6H label is its period)
SEQ83 = [('3C', 'ABCABCA', 'c'), ('2H', 'ABABA', 'h'), ('4H', 'ABCBA', 'hchch'), ('6H', 'ABCACBA', 'hcchcc'),
         ('Fibonacci', 'ABACBCACBABCA', 'chcchchcchcch')]
# #83 v4 part 2 (mechanics), 12-sheet blocks: word, c/h of the 10 inner sheets as stated there, mean Hagg symbol printed there
PART2 = {'3C': ('ABCABCABCABC', 'cccccccccc', 1.000), '2H': ('ABABABABABAB', 'hhhhhhhhhh', 0.091), '4H': ('ABACABACABAC', 'hchchchchc', -0.091),
         '6H': ('ABACBCABACBC', 'hcchcchcch', -0.091), 'Fibonacci': ('ABCBACABACBC', None, -0.091)}
fib = 'a'
while len(fib) < 13: fib = ''.join('ab' if x == 'a' else 'a' for x in fib)
FIB13 = fib[:13].replace('a', 'c').replace('b', 'h')
assert fib[:10] == 'abaababaab' and FIB13 == 'chcchchcchcch'
PART2['Fibonacci'] = (PART2['Fibonacci'][0], fib[:10].replace('a', 'c').replace('b', 'h'), PART2['Fibonacci'][2])
for nm_, (w, chw, hagg) in PART2.items():
    assert ch_of(w) == chw, nm_
    assert round(sum(steps_of(w)) / len(steps_of(w)), 3) == hagg, nm_
SEQ = {}
for nm_, letters, lab83 in SEQ83:
    inner = ch_of(letters); n = len(letters)
    assert inner == ''.join(lab83[p % len(lab83)] for p in range(1, n - 1)), nm_     # agrees with #83's labels
    assert letters_from(inner) == letters, nm_                                        # the rule rebuilds #83's letters
    P = dict(word=letters, names=[f'{k + 1}{w}' for k, w in enumerate(letters)], kind=None, off=offsets_of(letters), steps=steps_of(letters))
    nodes, links, deg = build(P); C = cells(P, links); cnt = cell_counts(P, C)
    SEQ[nm_] = dict(P=P, n=n, lab83=lab83, inner=inner, nodes=nodes, links=links, deg=deg, C=C, cnt=cnt)
assert SEQ['Fibonacci']['inner'] == FIB13[1:-1]
FWD_CNT, BWD_CNT = R['T-c']['cnt'][0], R['T-h']['cnt'][1]
assert R['T-c']['cnt'][1] == FWD_CNT and R['T-h']['cnt'][0] == FWD_CNT
for nm_, S in SEQ.items():
    for g, s_ in enumerate(S['P']['steps']): assert S['cnt'][g] == (FWD_CNT if s_ > 0 else BWD_CNT), (nm_, g)
    log(f"{nm_} {S['P']['word']}: inner c/h {S['inner']} (agrees with #83 '{S['lab83']}'), {S['n']} sheets, {9 * S['n']} nodes, "
        f"{len(S['links'])} links (21 per gap), steps {''.join('+' if x > 0 else '-' for x in S['P']['steps'])}, cells per gap as T-c (forward) / T-h gap 2 (backward)")
log(f"Fibonacci: a -> ab, b -> a gives {fib[:13]}; a -> c, b -> h: {FIB13} (#83); part 2 words checked (c/h and mean Hagg symbol)")
log(f"cells per forward gap {FWD_CNT}, per backward gap {BWD_CNT}")

# ---------------------------------------------------------------- figures (SVG, line drawings)
a_cm, d_cm = a_mm / 10, d_mm / 10
GOLD, VIOL_UP, VIOL_DN, TEAL = '#d9a521', '#8a5cc2', '#b48ae0', '#2bb3a3'
YARN, YARN_LINE, THREAD, FRAME, INK = '#efe9da', '#6f6a5e', '#8a5cc2', '#6b5310', '#222'
def svg(w, h, body, wmm=None):
    size = f'width="{wmm}mm" height="{wmm * h / w:.2f}mm"' if wmm else f'width="{w}" height="{h}"'
    return f'<svg xmlns="http://www.w3.org/2000/svg" {size} viewBox="0 0 {w} {h}" font-family="DejaVu Sans, sans-serif">{body}</svg>'
def line(x1, y1, x2, y2, w=1.0, c='#000', dash=None, op=1):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"'
            + (f' stroke-dasharray="{dash}"' if dash else '') + (f' stroke-opacity="{op}"' if op < 1 else '') + '/>')
def text(x, y, s, size=10, anchor='middle', weight='normal', c='#000', italic=False):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{c}"'
            + (' font-style="italic"' if italic else '') + f'>{s}</text>')
def circ(x, y, r, fill='#000', stroke='none', w=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def poly(pts, fill='none', stroke='#000', w=0.8, fop=1, dash=None):
    return (f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="{fill}" fill-opacity="{fop}" stroke="{stroke}" '
            f'stroke-width="{w}" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def path(d, c='#000', w=1.2, fill='none', dash=None):
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
def ell(x, y, rx, ry, c='#444', w=1.3, fill='none', dash=None):
    return f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
def arrow(x1, y1, x2, y2, w=1.2, c='#000', hs=6, dash=None):
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - hs * math.cos(a - 0.42), y2 - hs * math.sin(a - 0.42)); p2 = (x2 - hs * math.cos(a + 0.42), y2 - hs * math.sin(a + 0.42))
    return line(x1, y1, x2, y2, w, c, dash) + poly([(x2, y2), p1, p2], c, c, 0.6)
def grp(x, y, body): return f'<g transform="translate({x:.2f},{y:.2f})">{body}</g>'
def needle(x1, y1, x2, y2): return line(x1, y1, x2, y2, 7, '#7a7466') + line(x1, y1, x2, y2, 4.6, '#dcd6c6')
def save(name, s): open(os.path.join(FIGS, name), 'w').write(s)
def ptitle(n, t, sub=None, x=8):
    out = text(x, 16, f'{n}  {t}', 11.5, 'start', 'bold')
    for n_, t in enumerate([sub] if isinstance(sub, str) else (sub or [])): out += text(x, 31 + 12 * n_, t, 9.5, 'start', c='#333')
    return out
def garter(x0, y0, cols, ridges, s, marks=None):
    """Garter close-up, RS: per ridge a row of knit Vs over a row of purl bumps. marks: {(col, ridge): colour} (col 0 = left)."""
    marks = marks or {}; b = [f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{cols * s:.2f}" height="{ridges * s:.2f}" fill="{YARN}"/>']
    for r in range(ridges):
        yc = y0 + r * s
        for c in range(cols):
            xc = x0 + c * s + s / 2; col = marks.get((c, r), YARN_LINE); w = 3.0 if (c, r) in marks else 0.9
            b.append(path(f'M {xc - 0.33 * s:.2f} {yc + 0.06 * s:.2f} L {xc:.2f} {yc + 0.52 * s:.2f} L {xc + 0.33 * s:.2f} {yc + 0.06 * s:.2f}', col, w))
            b.append(path(f'M {xc - 0.44 * s:.2f} {yc + 0.64 * s:.2f} Q {xc:.2f} {yc + 0.98 * s:.2f} {xc + 0.44 * s:.2f} {yc + 0.64 * s:.2f}', YARN_LINE, 0.9))
    return ''.join(b)

# --- the sheet chart: one square = 1 stitch x 1 ridge (2 rows); stitch 1 at the right (RS view, cast-on edge at the bottom)
def chart():
    s = 10; X0, Y0 = 46, 34; W = X0 + COLS * s + 70; H = Y0 + RIDGES * s + 46
    X = lambda st: X0 + (COLS - st) * s + s / 2
    Y = lambda rg: Y0 + (RIDGES - rg) * s + s / 2
    b = [f'<rect x="{X0}" y="{Y0}" width="{COLS * s}" height="{RIDGES * s}" fill="#fff" stroke="#000" stroke-width="1.2"/>']
    for c in range(1, COLS):
        b.append(line(X0 + c * s, Y0, X0 + c * s, Y0 + RIDGES * s, 1.0 if c % 8 == 0 else 0.35, '#000' if c % 8 == 0 else '#999'))
    for r in range(1, RIDGES):
        b.append(line(X0, Y0 + r * s, X0 + COLS * s, Y0 + r * s, 1.0 if r % 7 == 0 else 0.35, '#000' if r % 7 == 0 else '#999'))
    for st in [1] + list(range(8, COLS + 1, 8)):
        b.append(text(X(st), Y0 + RIDGES * s + 13, str(st), 8.5)); b.append(text(X(st), Y0 - 5, str(st), 8.5))
    for rg in [1] + list(range(7, RIDGES + 1, 7)):
        b.append(text(X0 - 5, Y(rg) + 3, str(rg), 8.5, 'end'))
    b.append(text(X0 - 26, Y0 + RIDGES * s / 2, 'ridge', 9, 'middle'))
    b.append(text(X0 + COLS * s / 2, Y0 + RIDGES * s + 27, 'stitch (counted from the start of the RS row, stitch 1 at the right) · cast-on edge at the bottom', 9))
    for j in range(3):
        b.append(line(X0 + COLS * s + 2, Y(node_ridge(j)), X0 + COLS * s + 8, Y(node_ridge(j)), 1))
        b.append(text(X0 + COLS * s + 10, Y(node_ridge(j)) + 3.5, f'row {node_row(j)} (RS)', 8.5, 'start', 'bold'))
    for i, j in itertools.product(range(3), repeat=2):
        st, rg = node_st(i, j), node_ridge(j)
        b.append(f'<rect x="{X(st) - s / 2:.1f}" y="{Y(rg) - s / 2:.1f}" width="{s}" height="{s}" fill="#000"/>')
        b.append(text(X(st), Y(rg) - 7.5, str(1 + i + 3 * j), 9.5, 'middle', 'bold'))
    save('chart.svg', svg(W, H, ''.join(b)))

# --- the node stitch, step by step (2 x 2 panels)
def nk_fig():
    PW, PH = 250, 215; out = []
    def base(rn, ln, node=True):   # right-needle loops, left-needle loops (x positions); fabric below
        b = [garter(14, 160, 12, 2, 18.5)]
        for x in rn: b.append(line(x, 118, x, 160, 0.9, YARN_LINE))
        for x in ln: b.append(line(x, 118, x, 160, 0.9, YARN_LINE))
        return b
    # 1
    b = [ptitle(1, 'Knit to the node stitch', 'Lay the contrast thread beside the yarn.')]
    rn = [24, 42, 60, 78, 96]; ln = [140, 158, 176, 194, 212, 230]; b += base(rn, ln)
    b.append(needle(4, 108, 114, 108)); b.append(needle(246, 108, 128, 108))
    for x in rn + ln: b.append(ell(x, 108, 5, 10))
    b.append(ell(140, 108, 5, 10, '#000', 2.0))
    b.append(text(146, 74, 'node stitch', 9.5, 'start', 'bold')); b.append(line(150, 78, 142, 96, 0.8))
    b.append(path('M 96 118 C 104 122, 104 80, 92 46', YARN_LINE, 2.4)); b.append(text(80, 50, 'yarn', 9.5, 'end'))
    b.append(path('M 116 92 C 106 80, 104 64, 100 44', THREAD, 2.2)); b.append(text(106, 54, 'contrast thread', 9.5, 'start', c=THREAD))
    out.append(grp(0, 0, ''.join(b)))
    # 2
    b = [ptitle(2, 'Insert the right needle knitwise', ['into the node stitch; take yarn', 'and thread together.'])]
    b += base(rn, ln); b.append(needle(246, 108, 128, 108))
    yN = lambda x: 122 - (x - 4) * (24 / 146)
    b.append(needle(4, 122, 150, 98))
    for x in rn: b.append(ell(x, yN(x), 5, 10))
    for x in ln: b.append(ell(x, 108, 5, 10, '#000' if x == 140 else '#444', 2.0 if x == 140 else 1.3))
    b.append(path('M 92 44 C 110 60, 130 80, 146 96', YARN_LINE, 2.4)); b.append(path('M 98 42 C 116 58, 134 78, 149 94', THREAD, 2.2))
    b.append(text(150, 66, 'yarn + thread', 9.5, 'start')); b.append(text(150, 78, 'held together', 9.5, 'start'))
    out.append(grp(PW, 0, ''.join(b)))
    # 3
    b = [ptitle(3, 'Wrap both and pull them through', ['One new stitch of yarn and thread;', 'slip the old stitch off.'])]
    ln3 = [158, 176, 194, 212, 230]; b += base(rn, ln3)
    b.append(needle(4, 108, 132, 108)); b.append(needle(246, 108, 146, 108))
    for x in rn + ln3: b.append(ell(x, 108, 5, 10))
    b.append(ell(116, 108, 5.5, 10.5, YARN_LINE, 2.2)); b.append(ell(119, 108, 5.5, 10.5, THREAD, 2.0))
    b.append(arrow(140, 96, 140, 70, 1.1)); b.append(text(144, 66, 'old stitch slips off', 9.5, 'start'))
    b.append(text(104, 66, 'new stitch', 9.5, 'end', 'bold')); b.append(line(100, 70, 114, 96, 0.8))
    b.append(path('M 118 118 C 126 132, 116 146, 124 178', THREAD, 2.0)); b.append(text(130, 150, 'thread end, about 7 cm', 9, 'start', c=THREAD))
    b.append(path('M 118 98 C 120 80, 112 60, 108 44', YARN_LINE, 2.4))
    out.append(grp(0, PH, ''.join(b)))
    # 4
    b = [ptitle(4, 'The finished node stitch (RS)', ['Next row: knit yarn and thread', 'together as one stitch.'])]
    s = 21; cols, rid = 10, 6; x0, y0 = 20, 54
    b.append(garter(x0, y0, cols, rid, s, {(5, 2): THREAD}))
    cx, cy = x0 + 5 * s + s / 2, y0 + 2 * s + s / 2
    b.append(path(f'M {cx - 2} {cy + 6} C {cx - 14} {cy + 30}, {cx - 4} {cy + 50}, {cx - 22} {cy + 82}', THREAD, 2.0))
    b.append(path(f'M {cx + 2} {cy + 6} C {cx + 16} {cy + 30}, {cx + 8} {cy + 54}, {cx + 24} {cy + 84}', THREAD, 2.0))
    b.append(f'<rect x="{cx + 34}" y="{cy - 48}" width="70" height="15" fill="#fff"/>'); b.append(text(cx + 38, cy - 37, 'node stitch', 9.5, 'start', 'bold')); b.append(line(cx + 36, cy - 36, cx + 6, cy - 4, 0.9))
    b.append(text(cx + 30, cy + 66, 'both ends', 9.5, 'start', c=THREAD)); b.append(text(cx + 30, cy + 78, 'hang free', 9.5, 'start', c=THREAD))
    out.append(grp(PW, PH, ''.join(b)))
    save('nk.svg', svg(2 * PW, 2 * PH, ''.join(out)))

# --- a marked node: the node stitch and its two neighbours in the same ridge
def mark_fig():
    s = 24; cols, rid = 13, 7; x0, y0 = 20, 70; b = []
    nc, nr = 6, 3
    b.append(garter(x0, y0, cols, rid, s, {(nc, nr): THREAD, (nc - 1, nr): GOLD, (nc + 1, nr): GOLD}))
    cx, cy = x0 + nc * s + s / 2, y0 + nr * s + s / 2
    b.append(path(f'M {cx - 2} {cy + 6} C {cx - 12} {cy + 40}, {cx - 2} {cy + 70}, {cx - 20} {cy + 112}', THREAD, 2.0))
    b.append(path(f'M {cx + 2} {cy + 6} C {cx + 14} {cy + 40}, {cx + 6} {cy + 72}, {cx + 22} {cy + 112}', THREAD, 2.0))
    bx0, bx1 = x0 + (nc - 1) * s + 2, x0 + (nc + 2) * s - 2
    b.append(path(f'M {bx0} {y0 + nr * s - 4} L {bx0} {y0 + nr * s - 10} L {bx1} {y0 + nr * s - 10} L {bx1} {y0 + nr * s - 4}', '#000', 1.0))
    b.append(line((bx0 + bx1) / 2, y0 + nr * s - 10, (bx0 + bx1) / 2, y0 - 6, 0.8)); b.append(text((bx0 + bx1) / 2, y0 - 10, 'the 3 stitches a cord is picked up from (and sewn to)', 10, 'middle', 'bold'))
    W = x0 + cols * s + 230
    lx = x0 + cols * s + 16
    b.append(circ(lx + 6, 110, 5, THREAD)); b.append(text(lx + 18, 114, 'node stitch (worked NK)', 10, 'start'))
    b.append(circ(lx + 6, 134, 5, GOLD)); b.append(text(lx + 18, 138, 'its two neighbours in the ridge', 10, 'start'))
    b.append(line(lx, 158, lx + 12, 158, 2, THREAD)); b.append(text(lx + 18, 162, 'contrast thread ends', 10, 'start'))
    b.append(text(lx, 196, 'V = knit stitch; arc = ridge bump', 9.5, 'start', c='#444'))
    b.append(text(lx, 212, 'RS facing, cast-on edge at the bottom', 9.5, 'start', c='#444'))
    b.append(text(x0, 24, 'Close-up of a node on the RS', 11.5, 'start', 'bold'))
    save('mark.svg', svg(W, y0 + rid * s + 82, ''.join(b)))

# --- the 3-stitch i-cord (3 x 2 panels)
def icord_fig():
    PW, PH = 215, 270; out = []; s = 19; gx, gy = 13, 205
    cxs = [gx + c * s + s / 2 for c in (3, 4, 5)]
    def patch(): return garter(gx, gy, 10, 3, s, {(4, 0): THREAD, (3, 0): GOLD, (5, 0): GOLD})
    # 1 pick up
    b = [ptitle(1, 'Pick up and knit 3 sts', 'the node stitch and its two neighbours'), patch()]
    b.append(needle(20, 130, 196, 130))
    for x in cxs: b.append(ell(x, 130, 5, 10)); b.append(line(x, 140, x, gy + 4, 1.0, YARN_LINE))
    b.append(path(f'M {cxs[0]} 140 C {cxs[0] - 30} 150, {cxs[0] - 40} 100, {cxs[0] - 50} 66', YARN_LINE, 2.4)); b.append(text(cxs[0] - 54, 62, 'yarn', 9.5, 'end'))
    b.append(text(196, 118, 'DPN', 9.5, 'end')); b.append(text(107, 196, 'RS', 9.5, 'middle', c='#444'))
    out.append(grp(0, 0, ''.join(b)))
    # 2 slide
    b = [ptitle(2, 'Slide the sts to the other end', 'The yarn now hangs from the left stitch.'), patch()]
    b.append(needle(20, 130, 196, 130)); xs2 = [146, 164, 182]
    for x in xs2: b.append(ell(x, 130, 5, 10))
    for x0_, x1_ in zip(cxs, xs2): b.append(path(f'M {x1_} 140 C {x1_} 170, {x0_} 180, {x0_} {gy + 4}', YARN_LINE, 0.9))
    b.append(arrow(70, 104, 140, 104, 1.2)); b.append(path(f'M {xs2[0]} 140 C {xs2[0] - 20} 150, {xs2[0] - 40} 150, {xs2[0] - 60} 160', YARN_LINE, 2.4))
    b.append(text(xs2[0] - 64, 170, 'yarn', 9.5, 'end'))
    out.append(grp(PW, 0, ''.join(b)))
    # 3 pull and K3
    b = [ptitle(3, 'Yarn across the back, K3', 'Pull firmly: the sts close into a tube.'), patch()]
    b.append(needle(20, 130, 192, 130)); b.append(needle(210, 70, 186, 124))
    for x in xs2: b.append(ell(x, 130, 5, 10))
    for x0_, x1_ in zip(cxs, xs2): b.append(path(f'M {x1_} 140 C {x1_} 170, {x0_} 180, {x0_} {gy + 4}', YARN_LINE, 0.9))
    b.append(path(f'M {xs2[0]} 140 C {xs2[0] + 10} 150, {xs2[2] + 6} 150, {xs2[2] + 8} 132 C {xs2[2] + 10} 112, 200 96, 206 80', YARN_LINE, 2.4, dash='4 3'))
    b.append(text(100, 176, 'yarn behind the work', 9.5, 'middle'))
    out.append(grp(2 * PW, 0, ''.join(b)))
    # 4 repeat
    b = [ptitle(4, 'Repeat to the row count', 'Every cord: the same number of rows.'), patch()]
    tx = cxs[1]; ty0, ty1 = gy + 2, 78
    b.append(f'<rect x="{tx - 11}" y="{ty1}" width="22" height="{ty0 - ty1}" rx="6" fill="{YARN}" stroke="{YARN_LINE}" stroke-width="1.2"/>')
    for yy in range(int(ty1) + 6, int(ty0) - 2, 7):
        for dx in (-5.5, 0, 5.5): b.append(path(f'M {tx + dx - 2.6} {yy - 2.6} L {tx + dx} {yy + 1.6} L {tx + dx + 2.6} {yy - 2.6}', YARN_LINE, 0.8))
    b.append(needle(tx - 34, ty1 - 4, tx + 34, ty1 - 4))
    sx = tx + 40
    b.append(f'<rect x="{sx}" y="{ty1}" width="13" height="{ty0 - ty1}" fill="#faf6ea" stroke="#000" stroke-width="0.9"/>')
    b.append(f'<text font-size="9.5" text-anchor="middle" transform="translate({sx + 8.5:.1f},{(ty0 + ty1) / 2:.1f}) rotate(-90)">card strip, length ℓ</text>')
    b.append(text(tx - 18, 112, 'count', 9.5, 'end')); b.append(text(tx - 18, 124, 'the rows', 9.5, 'end'))
    out.append(grp(0, PH, ''.join(b)))
    # 5 pin and tag
    b = [ptitle(5, 'Pin the 3 live sts and tag', 'Tag: cord number and target node.'), patch()]
    b.append(f'<rect x="{tx - 11}" y="{ty1}" width="22" height="{ty0 - ty1}" rx="6" fill="{YARN}" stroke="{YARN_LINE}" stroke-width="1.2"/>')
    for yy in range(int(ty1) + 6, int(ty0) - 2, 7):
        for dx in (-5.5, 0, 5.5): b.append(path(f'M {tx + dx - 2.6} {yy - 2.6} L {tx + dx} {yy + 1.6} L {tx + dx + 2.6} {yy - 2.6}', YARN_LINE, 0.8))
    for dx in (-6, 0, 6): b.append(ell(tx + dx, ty1 - 4, 3.2, 6))
    b.append(path(f'M {tx - 22} {ty1 - 6} L {tx + 22} {ty1 - 6} M {tx - 22} {ty1 - 6} C {tx - 30} {ty1 - 6}, {tx - 30} {ty1 - 18}, {tx - 22} {ty1 - 18} L {tx + 18} {ty1 - 18}', '#555', 1.6))
    b.append(circ(tx + 22, ty1 - 6, 2.4, '#555'))
    b.append(line(tx + 22, ty1 - 6, tx + 52, ty1 + 10, 0.8))
    b.append(f'<rect x="{tx + 46}" y="{ty1 + 10}" width="62" height="26" fill="#fff" stroke="#000" stroke-width="0.9"/>')
    b.append(text(tx + 77, ty1 + 27, '7 → B5', 10.5, 'middle', 'bold'))
    out.append(grp(PW, PH, ''.join(b)))
    # 6 when tensioned
    b = [ptitle(6, 'Tensioned, the cord slants', f'at {TILT:.1f}° between two sheets.')]
    U = 150; x0, y0 = 26, 230; hgt = math.sqrt(2 / 3) * U; base = U / math.sqrt(3)
    b.append(f'<rect x="8" y="{y0}" width="200" height="8" fill="{YARN}" stroke="{YARN_LINE}"/>')
    b.append(f'<rect x="8" y="{y0 - hgt - 8}" width="200" height="8" fill="{YARN}" stroke="{YARN_LINE}"/>')
    b.append(line(x0 + 20, y0, x0 + 20 + base, y0 - hgt, 6, TEAL))
    b.append(circ(x0 + 20, y0 + 4, 4)); b.append(circ(x0 + 20 + base, y0 - hgt - 4, 4))
    r = 26; a = math.radians(TILT)
    b.append(path(f'M {x0 + 20 + r} {y0} A {r} {r} 0 0 0 {x0 + 20 + r * math.cos(a):.2f} {y0 - r * math.sin(a):.2f}', '#000', 1))
    b.append(text(x0 + 52, y0 - 8, f'{TILT:.1f}°', 10, 'start', 'bold'))
    b.append(line(x0 + 20 + base + 20, y0, x0 + 20 + base + 20, y0 - hgt, 0.8)); b.append(text(x0 + 20 + base + 25, y0 - hgt / 2, 'd', 11, 'start', italic=True))
    b.append(text(x0 + 6, y0 - hgt / 2 - 8, 'a node to node', 9.5, 'start'))
    b.append(text(x0 + 6, y0 - hgt / 2 + 6, 'ℓ face to face', 9.5, 'start'))
    out.append(grp(2 * PW, PH, ''.join(b)))
    save('icord.svg', svg(3 * PW, 2 * PH, ''.join(out)))

# --- attaching a cord end to a node (section + view from above)
def attach_fig():
    out = []
    b = [ptitle(1, 'Sew the live sts to the node', 'Section through the upper sheet (RS up).')]
    yb = 120
    b.append(f'<rect x="10" y="{yb}" width="270" height="12" fill="{YARN}" stroke="{YARN_LINE}"/>')
    nx = 160
    b.append(f'<rect x="{nx - 6}" y="{yb}" width="12" height="12" fill="{THREAD}" fill-opacity="0.75"/>')
    b.append(f'<rect x="{nx - 18}" y="{yb}" width="12" height="12" fill="{GOLD}" fill-opacity="0.6"/>')
    b.append(f'<rect x="{nx + 6}" y="{yb}" width="12" height="12" fill="{GOLD}" fill-opacity="0.6"/>')
    a = math.radians(TILT); L = 110
    fx, fy = nx - L * math.cos(a), yb + 12 + L * math.sin(a)
    b.append(line(fx, fy, nx, yb + 18, 12, YARN_LINE)); b.append(line(fx, fy, nx, yb + 18, 9.5, YARN))
    for dx in (-8, 0, 8): b.append(ell(nx + dx, yb + 18, 3.5, 5, '#444', 1.2))
    b.append(path(f'M {nx + 8} {yb + 18} C {nx + 14} {yb + 8}, {nx + 14} {yb - 4}, {nx + 12} {yb - 18}', TEAL, 2))
    b.append(line(nx + 12, yb - 18, nx + 40, yb - 88, 3.4, '#555')); b.append(ell(nx + 38, yb - 82, 1.6, 4, '#fff', 1))
    b.append(text(nx + 46, yb - 64, 'tapestry needle', 9.5, 'start'))
    b.append(text(14, yb - 6, 'upper sheet, RS up', 9.5, 'start'))
    b.append(text(fx + 4, fy + 2, 'cord from below', 9.5, 'start'))
    b.append(text(nx + 24, yb + 36, '3 live sts', 9.5, 'start'))
    b.append(text(10, 232, 'Down through the fabric, through one live st, back up', 9.5, 'start', c='#333'))
    b.append(text(10, 245, 'through the same fabric stitch.', 9.5, 'start', c='#333'))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Seen from above (RS)', 'One live st into each of the 3 stitches.')]
    s = 26; x0, y0 = 20, 60; nc, nr = 4, 2
    b.append(garter(x0, y0, 10, 5, s, {(nc, nr): THREAD, (nc - 1, nr): GOLD, (nc + 1, nr): GOLD}))
    for dc in (-1, 0, 1):
        xc = x0 + (nc + dc) * s + s / 2; yc = y0 + nr * s + s / 2
        b.append(path(f'M {xc - 6} {yc - 10} C {xc - 2} {yc - 18}, {xc + 2} {yc - 18}, {xc + 6} {yc - 10}', TEAL, 2.4))
    xe = x0 + (nc + 1) * s + s / 2
    b.append(path(f'M {xe + 6} {y0 + nr * s - 2} C {xe + 26} {y0 + nr * s - 20}, {xe + 50} {y0 + nr * s - 10}, {xe + 60} {y0 + nr * s - 30}', TEAL, 2))
    b.append(text(xe + 62, y0 + nr * s - 34, 'fasten off on the RS', 9.5, 'start'))
    out.append(grp(300, 0, ''.join(b)))
    save('attach.svg', svg(600, 255, ''.join(out)))

# --- lacing a sheet into its frame (plan)
def lace_fig():
    sc = 4.2; X0, Y0 = 40, 50; fw = 18
    X = lambda st: X0 + fw + (COLS + 0.5 - st) * sc; Y = lambda rg: Y0 + fw + (RIDGES + 0.5 - rg) * sc
    sw, sh = COLS * sc, RIDGES * sc; b = []
    b.append(f'<rect x="{X0}" y="{Y0}" width="{sw + 2 * fw}" height="{sh + 2 * fw}" fill="none" stroke="{FRAME}" stroke-width="7"/>')
    b.append(f'<rect x="{X0 + fw}" y="{Y0 + fw}" width="{sw}" height="{sh}" fill="{YARN}" stroke="{YARN_LINE}"/>')
    pts = []
    n = 14
    for t in range(n + 1):
        pts.append((X0 + fw + sw * t / n, Y0 + fw, X0 + fw + sw * (t + 0.5) / n, Y0 + 3))
        pts.append((X0 + fw + sw * t / n, Y0 + fw + sh, X0 + fw + sw * (t + 0.5) / n, Y0 + sh + 2 * fw - 3))
    for t in range(9 + 1):
        pts.append((X0 + fw, Y0 + fw + sh * t / 9, X0 + 3, Y0 + fw + sh * (t + 0.5) / 9))
        pts.append((X0 + fw + sw, Y0 + fw + sh * t / 9, X0 + sw + 2 * fw - 3, Y0 + fw + sh * (t + 0.5) / 9))
    for x1, y1, x2, y2 in pts: b.append(line(x1, y1, x2, y2, 0.8, '#777'))
    P_ = {}
    for i, j in itertools.product(range(3), repeat=2):
        P_[1 + i + 3 * j] = (X(node_st(i, j)), Y(node_ridge(j))); b.append(circ(*P_[1 + i + 3 * j], 3.6, THREAD))
        b.append(text(P_[1 + i + 3 * j][0] + 6, P_[1 + i + 3 * j][1] - 5, str(1 + i + 3 * j), 9.5, 'start', 'bold'))
    tri = [P_[1], P_[2], P_[4]]
    b.append(poly(tri, 'none', '#000', 1.4, dash='5 3'))
    for (x1, y1), (x2, y2) in [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]:
        b.append(text((x1 + x2) / 2 + 8, (y1 + y2) / 2 + 12, 'a', 11, 'start', italic=True))
    b.append(text(X0 + fw + sw / 2, Y0 + sh + 2 * fw + 18, 'cast-on edge (towards you)', 10, 'middle', 'bold'))
    b.append(text(X0 + fw + sw / 2, Y0 - 10, 'frame', 10, 'middle', c=FRAME))
    lx = X0 + sw + 2 * fw + 18
    for k, t in enumerate(['Sheet RS up, cast-on edge towards you.', 'Lace all round, firm but not stretched.',
                           f'Check: every node triangle (1-2-4, 2-4-5, …)', f'measures a = {a_cm:.1f} cm on all three sides,',
                           'node centre to node centre.']):
        b.append(text(lx, Y0 + 30 + 15 * k, t, 10, 'start'))
    save('lace.svg', svg(lx + 250, Y0 + sh + 2 * fw + 28, ''.join(b)))

# --- side section of a stack (any word): sheets as lines, cords seen along a row of nodes (horizontal = ridges)
def section(word, x0, ybot, U, tmin, tmax, patch=range(3), follow=1, hi=True, names=None, chlab=True):
    p = math.sqrt(3) / 2; dd = math.sqrt(2 / 3); off = [float(o) for o in offsets_of(word)]; st = steps_of(word)
    X = lambda t: x0 + (t - tmin) * p * U; Z = lambda k: ybot - k * dd * U; b = []
    for k in range(len(word)):
        b.append(line(X(tmin), Z(k), X(tmax), Z(k), 1.6, '#000'))
        b.append(text(X(tmin) - 7, Z(k) + 4, names[k] if names else word[k], 11, 'end', 'bold'))
    for k in range(len(word) - 1):
        s = st[k]
        for j in patch:
            t = j + off[k]
            for dj, w in ((0, 2.6), (-s, 1.0)):
                if j + dj in patch: b.append(line(X(t), Z(k), X(t + s / 3 + dj), Z(k + 1), w, TEAL if hi else '#9ab'))
    if follow is not None:
        for k in range(len(word) - 1):
            b.append(line(X(follow + off[k]), Z(k), X(follow + off[k + 1]), Z(k + 1), 3.6, '#000'))
    for k in range(len(word)):
        for j in patch: b.append(circ(X(j + off[k]), Z(k), 3.2))
    if chlab:
        ch = ch_of(word)
        for k in range(1, len(word) - 1): b.append(text(X(tmax) + 10, Z(k) + 4, ch[k - 1], 11, 'start', 'bold', TEAL if ch[k - 1] == 'c' else VIOL_UP))
    return ''.join(b), X, Z

# --- hanging and tensioning, then standing on posts
def hang_fig():
    out = []; U = 74; p = math.sqrt(3) / 2; dd = math.sqrt(2 / 3)
    for panel in range(2):
        tmin, tmax = -0.9, 3.3
        body, X, Z = section('ABC', 20, 300 if panel == 0 else 280, U, tmin, tmax, follow=None, names=['A', 'B', 'C'], chlab=False)
        b = [body]
        for k in range(3):
            b.append(line(X(tmin) - 4, Z(k), X(tmin) + 16, Z(k), 7, FRAME)); b.append(line(X(tmax) - 16, Z(k), X(tmax) + 4, Z(k), 7, FRAME))
        if panel == 0:
            b.insert(0, ptitle(1, 'Hang it and let it settle', 'Hang by the top frame; the lower frames sink'))
            b.append(text(8, 46, 'until every cord is taut.', 9.5, 'start', c='#333'))
            b.append(line(X(tmin) - 20, 66, X(tmax) + 20, 66, 6, '#555'))
            b.append(line(X(tmin) + 6, 66, X(tmin) + 6, Z(2), 1.2)); b.append(line(X(tmax) - 6, 66, X(tmax) - 6, Z(2), 1.2))
            for k in (0, 1): b.append(arrow(X(tmax) + 22, Z(k) - 20, X(tmax) + 22, Z(k) + 8, 1.4))
            b.append(text(X(tmax) + 30, Z(0) - 4, 'weight', 9.5, 'start'))
            b.append(line(X(tmin) + 34, Z(0), X(tmin) + 34, Z(1), 0.8)); b.append(text(X(tmin) + 38, (Z(0) + Z(1)) / 2 + 4, 'd', 11, 'start', italic=True))
        else:
            b.insert(0, ptitle(2, 'Stand it on posts', 'Four posts per gap at the frame corners,'))
            b.append(text(8, 46, 'cut to the measured spacing.', 9.5, 'start', c='#333'))
            for k in range(2):
                for x in (X(tmin) + 8, X(tmax) - 8): b.append(line(x, Z(k) - 4, x, Z(k + 1) + 4, 5, '#8a7a5a'))
            b.append(line(0, Z(0) + 6, X(tmax) + 30, Z(0) + 6, 2.5, '#555')); b.append(text(X(tmax) + 28, Z(0) + 20, 'table', 9.5, 'end'))
        out.append(grp(panel * 330, 0, ''.join(b)))
    save('hang.svg', svg(660, 320, ''.join(out)))

# --- measuring: card template against a cord; plumb line from the top sheet
def measure_fig():
    out = []; U = 190; hgt = math.sqrt(2 / 3) * U; base = U / math.sqrt(3); y0 = 250; x0 = 60
    b = [ptitle(1, 'Check angle and spacing with the card', ['Stand the card upright on the lower sheet;', 'the long leg must just reach the upper sheet.'])]
    b.append(f'<rect x="10" y="{y0}" width="290" height="8" fill="{YARN}" stroke="{YARN_LINE}"/>')
    b.append(f'<rect x="10" y="{y0 - hgt - 8:.2f}" width="290" height="8" fill="{YARN}" stroke="{YARN_LINE}"/>')
    b.append(poly([(x0, y0), (x0 + base, y0), (x0 + base, y0 - hgt)], '#faf6ea', '#000', 1.0, 0.92))
    b.append(line(x0, y0, x0 + base, y0 - hgt, 5, TEAL))
    b.append(text(x0 + base / 2, y0 + 22, 'short leg on the sheet', 9.5))
    b.append(f'<text font-size="9.5" text-anchor="middle" transform="translate({x0 + base + 14:.1f},{y0 - hgt / 2:.1f}) rotate(-90)">long leg upright = d</text>')
    b.append(f'<text font-size="9.5" text-anchor="middle" transform="translate({x0 + base / 2 - 14:.1f},{y0 - hgt / 2 - 8:.1f}) rotate({-TILT:.1f})">cord along the slanted edge</text>')
    r = 22; a = math.radians(TILT)
    b.append(path(f'M {x0 + r} {y0} A {r} {r} 0 0 0 {x0 + r * math.cos(a):.2f} {y0 - r * math.sin(a):.2f}', '#000', 1))
    b.append(text(x0 + 26, y0 - 6, f'{TILT:.1f}°', 9.5, 'start'))
    out.append(grp(0, 0, ''.join(b)))
    b = [ptitle(2, 'Plumb line from the top sheet', 'Thread and a small weight from node 1.')]
    yA, yT = 250, 70
    b.append(f'<rect x="10" y="{yA}" width="280" height="8" fill="{YARN}" stroke="{YARN_LINE}"/>')
    b.append(f'<rect x="10" y="{yT}" width="280" height="8" fill="{YARN}" stroke="{YARN_LINE}"/>')
    b.append(circ(190, yT + 4, 4.5, VIOL_UP)); b.append(text(198, yT - 6, 'node 1 of the top sheet', 9.5, 'start'))
    b.append(line(190, yT + 8, 190, yA - 14, 1.0, '#000', '3 2')); b.append(poly([(184, yA - 14), (196, yA - 14), (190, yA - 3)], '#555', '#555'))
    b.append(circ(110, yA + 4, 4.5, '#666')); b.append(text(110, yA + 26, 'A1', 10, 'middle', 'bold'))
    b.append(arrow(116, yA + 18, 186, yA + 18, 1.0)); b.append(text(150, yA + 34, 'count st and ridges', 9.5))
    b.append(text(14, yA - 40, 'Compare with the stacking table of the pattern.', 9.5, 'start', c='#333'))
    out.append(grp(320, 0, ''.join(b)))
    save('measure.svg', svg(640, 300, ''.join(out)))

# --- 3D view of a piece or stack (knitter's frame: stitch numbers increase to the left, ridges away from you)
def xyz(P, n):
    u, v, k = lat(P, n); return (-(float(u) + float(v) / 2), float(v) * math.sqrt(3) / 2, float(k) * math.sqrt(2 / 3))
def rect_pts(P, k, s0, s1, r0, r1):
    u0, v0, _ = lat(P, (k, 0, 0)); pts = []
    for st, rg in [(s0, r0), (s1, r0), (s1, r1), (s0, r1)]:
        dv = (rg - node_ridge(0)) / M; du = (st - node_st(0, 0)) / N - dv / 2
        u, v = float(u0) + du, float(v0) + dv
        pts.append((-(u + v / 2), v * math.sqrt(3) / 2, k * math.sqrt(2 / 3)))
    return pts
def sheet_rect(P, k): return rect_pts(P, k, 0.5, COLS + 0.5, 0.5, RIDGES + 0.5)
def frame_rect(P, k, e=4): return rect_pts(P, k, 0.5 - e, COLS + 0.5 + e, 0.5 - e, RIDGES + 0.5 + e)
def hull_faces(pts):
    faces = []; n = len(pts)
    for a_, b_, c_ in itertools.combinations(range(n), 3):
        A, B, Cc = (pts[t] for t in (a_, b_, c_))
        nx = (B[1] - A[1]) * (Cc[2] - A[2]) - (B[2] - A[2]) * (Cc[1] - A[1]); ny = (B[2] - A[2]) * (Cc[0] - A[0]) - (B[0] - A[0]) * (Cc[2] - A[2])
        nz = (B[0] - A[0]) * (Cc[1] - A[1]) - (B[1] - A[1]) * (Cc[0] - A[0]); ln = math.sqrt(nx * nx + ny * ny + nz * nz)
        if ln < 1e-9: continue
        sd = [(p[0] - A[0]) * nx + (p[1] - A[1]) * ny + (p[2] - A[2]) * nz for p in pts]
        if all(x <= 1e-7 * ln for x in sd) or all(x >= -1e-7 * ln for x in sd):
            on = frozenset(t for t in range(n) if abs(sd[t]) <= 1e-7 * ln)
            if on not in faces: faces.append(on)
    out = []
    for f in faces:
        f = list(f); cx = [sum(pts[t][r] for t in f) / len(f) for r in range(3)]
        A = pts[f[0]]; e = [A[r] - cx[r] for r in range(3)]; nrm = None
        for t in f[1:]:
            q = [pts[t][r] - cx[r] for r in range(3)]
            cr = (e[1] * q[2] - e[2] * q[1], e[2] * q[0] - e[0] * q[2], e[0] * q[1] - e[1] * q[0])
            if math.sqrt(sum(x * x for x in cr)) > 1e-9: nrm = cr; break
        f2 = (nrm[1] * e[2] - nrm[2] * e[1], nrm[2] * e[0] - nrm[0] * e[2], nrm[0] * e[1] - nrm[1] * e[0])
        ang = lambda t: math.atan2(sum((pts[t][r] - cx[r]) * f2[r] for r in range(3)), sum((pts[t][r] - cx[r]) * e[r] for r in range(3)))
        out.append([pts[t] for t in sorted(f, key=ang)])
    return out

def view3d(P, links, C, fname, upto=None, free_gap=None, mode='structure', frames=False, W=820, H=560, phi=-28, theta=27,
           node_labels=True, sheet_lab=None, lab_size=11):
    ns = len(P['word']); upto = ns if upto is None else upto
    sheet_lab = sheet_lab or (lambda k: f"sheet {P['names'][k]}")
    cp, sp_, ct, st_ = math.cos(math.radians(phi)), math.sin(math.radians(phi)), math.cos(math.radians(theta)), math.sin(math.radians(theta))
    allp = [p for k in range(ns) for p in (frame_rect(P, k) if frames else sheet_rect(P, k))]
    def proj0(p):
        x1 = p[0] * cp + p[1] * sp_; y1 = -p[0] * sp_ + p[1] * cp
        return x1, -(p[2] * ct + y1 * st_), y1 * ct - p[2] * st_
    xs = [proj0(p)[0] for p in allp]; ys = [proj0(p)[1] for p in allp]
    sc = min((W - 150) / (max(xs) - min(xs)), (H - 40) / (max(ys) - min(ys)))
    ox, oy = (W + 120 - sc * (max(xs) + min(xs))) / 2, (H - sc * (max(ys) + min(ys))) / 2
    def pr(p): x, y, z = proj0(p); return (ox + sc * x, oy + sc * y)
    depth = lambda p: proj0(p)[2]
    b = []
    for k in range(upto):
        if frames: b.append(poly([pr(p) for p in frame_rect(P, k)], 'none', FRAME, 2.6))
        rect = sheet_rect(P, k)
        b.append(poly([pr(p) for p in rect], '#e9e6df', '#777', 0.9, 0.55))
        lp = min((pr(p) for p in (frame_rect(P, k) if frames else rect)), key=lambda q: q[0])
        b.append(text(lp[0] - 6, lp[1] + 4, sheet_lab(k), lab_size, 'end', 'bold', '#444'))
        for i, j in itertools.product(range(3), repeat=2):
            for di, dj in [(1, 0), (0, 1), (-1, 1)]:
                if 0 <= i + di < 3 and 0 <= j + dj < 3:
                    b.append(line(*pr(xyz(P, (k, i, j))), *pr(xyz(P, (k, i + di, j + dj))), 0.7, '#999', '3 2'))
        for i, j in itertools.product(range(3), repeat=2):
            b.append(circ(*pr(xyz(P, (k, i, j))), 3.0, '#000'))
            if node_labels and ((i, j) in [(0, 0), (2, 0), (0, 2), (2, 2)] or (mode == 'cells' and (i, j) == (1, 1))):
                x, y = pr(xyz(P, (k, i, j))); b.append(text(x + 5, y + 12, lab(P, (k, i, j)), 9, 'start', 'bold', '#222'))
        if k == ns - 1: break
        joined = k < upto - 1; free = (k == upto - 1 and free_gap == k)
        if not (joined or free): continue
        items = []
        for x in links:
            if x[0][0] != k: continue
            p, q = xyz(P, x[0]), xyz(P, x[1])
            items.append(((depth(p) + depth(q)) / 2 - 1e-3, line(*pr(p), *pr(q), 2.2, TEAL)))
            if free: items.append((depth(q) - 2e-3, circ(*pr(q), 3.4, '#fff', TEAL, 1.6)))
        if mode == 'cells' and joined:
            for c in C:
                if c['gap'] != k: continue
                if c['kind'] == 'tet' and c['base'] == 1:
                    for f in hull_faces([xyz(P, n) for n in c['nodes']]):
                        items.append((sum(depth(p) for p in f) / len(f), poly([pr(p) for p in f], GOLD, '#6b5310', 0.7, 0.42)))
                if c['kind'] == 'oct':
                    tri = c['hi'] if k == 0 else c['lo']
                    pts = [xyz(P, n) for n in tri]
                    for p_, q_ in c['links']:
                        a_, b2 = xyz(P, p_), xyz(P, q_); pts.append(tuple((a_[r] + b2[r]) / 2 for r in range(3)))
                    col = VIOL_DN if k == 0 else VIOL_UP
                    for f in hull_faces(pts):
                        items.append((sum(depth(p) for p in f) / len(f), poly([pr(p) for p in f], col, '#3c2366', 0.7, 0.42)))
        for _, it in sorted(items, key=lambda t: -t[0]): b.append(it)
    save(fname, svg(W, H, ''.join(b)))

# --- the stacking plan of a test piece, seen from above
def layout_fig(name):
    P = R[name]['P']; nm = P['names']; sc = 4.4
    offs = [tuple(float(x) for x in st_r(P['off'][k], P['off'][k])) for k in range(3)]
    smin = 0.5 + min(o[0] for o in offs); smax = COLS + 0.5 + max(o[0] for o in offs)
    rmin = 0.5 + min(o[1] for o in offs); rmax = RIDGES + 0.5 + max(o[1] for o in offs)
    X0, Y0 = 20, 30
    X = lambda st: X0 + (smax - st) * sc; Y = lambda rg: Y0 + (rmax - rg) * sc
    cols = ['#555', GOLD, VIOL_UP]; b = []
    for k in range(3):
        ds, dr = offs[k]
        pts = [(X(0.5 + ds), Y(0.5 + dr)), (X(COLS + 0.5 + ds), Y(0.5 + dr)), (X(COLS + 0.5 + ds), Y(RIDGES + 0.5 + dr)), (X(0.5 + ds), Y(RIDGES + 0.5 + dr))]
        b.append(poly(pts, cols[k], cols[k], 1.2, 0.06, '6 3' if k else None))
    def marker(k, x, y):
        if k == 0: return circ(x, y, 4.6, 'none', cols[0], 1.8)
        if k == 1: return poly([(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)], 'none', cols[1], 2)
        r_ = 7.5 if P['off'][2] == P['off'][0] else 5
        return poly([(x - r_, y - r_), (x + r_, y - r_), (x + r_, y + r_), (x - r_, y + r_)], 'none', cols[2], 2)
    for k in range(3):
        ds, dr = offs[k]
        for i, j in itertools.product(range(3), repeat=2):
            x, y = X(node_st(i, j) + ds), Y(node_ridge(j) + dr); b.append(marker(k, x, y))
            if (i, j) in [(0, 0), (2, 2)]:
                dy = {0: 16, 1: -9, 2: -12}[k]; b.append(text(x + (9 if k != 1 else -9), y + dy, lab(P, (k, i, j)), 9.5, 'start' if k != 1 else 'end', 'bold', cols[k]))
    A1 = (X(node_st(0, 0)), Y(node_ridge(0)))
    for k in (1, 2):
        ds, dr = offs[k]
        if ds == 0 and dr == 0: continue
        P1 = (X(node_st(0, 0) + ds), Y(node_ridge(0) + dr)); b.append(arrow(A1[0] - 2, A1[1] - 2, P1[0] + 5, P1[1] + 5, 1.2, cols[k]))
    W = X0 + (smax - smin) * sc + 20; Hh = Y0 + (rmax - rmin) * sc
    lx = W + 10; ly = Y0 + 10
    leg = [(0, f'sheet A (bottom)'), (1, f'sheet B (middle)'), (2, f'sheet {nm[2]} (top)')]
    for n_, (k, t) in enumerate(leg):
        b.append(marker(k, lx + 8, ly + 22 * n_)); b.append(text(lx + 22, ly + 22 * n_ + 4, t, 10, 'start', c=cols[k] if k else '#222'))
    rows = []
    for k in (1, 2):
        ds, dr = st_r(P['off'][k], P['off'][k]); cm = math.sqrt(float(norm2(P['off'][k], P['off'][k]))) * a_cm
        rows.append(f'{nm[k]}1: {fr0(ds)} st, {fr0(dr)} r from A1 ({cm:.1f} cm)' if ds or dr else f'{nm[k]}1: straight over A1')
    for n_, t in enumerate(rows): b.append(text(lx, ly + 90 + 18 * n_, t, 10, 'start'))
    b.append(text(lx, ly + 150, 'Seen from above, RS up,', 9.5, 'start', c='#444'))
    b.append(text(lx, ly + 164, 'cast-on edges at the bottom;', 9.5, 'start', c='#444'))
    b.append(text(lx, ly + 178, '+ st = towards higher stitch numbers (left),', 9.5, 'start', c='#444'))
    b.append(text(lx, ly + 192, '+ r = towards the bind-off edge (up).', 9.5, 'start', c='#444'))
    save(f'layout-{name}.svg', svg(lx + 250, Hh + 20, ''.join(b)))

# --- c against h: section along a row (horizontal = ridges) and plan at one node of B, in the knitter's frame
def ch_fig():
    U = 78; p = math.sqrt(3) / 2; dd = math.sqrt(2 / 3); b = []
    OFF = {'A': 0, 'B': 1 / 3, 'C': 2 / 3}
    def panel(x0, word, kind, names):
        ymin, ymax = -0.15, 2.65
        X = lambda t: x0 + 34 + (t - ymin) * p * U; Z = lambda k: 214 - k * dd * U
        for k, L in enumerate(word):
            b.append(line(X(ymin), Z(k), X(ymax), Z(k), 1.6, '#000')); b.append(text(X(ymin) - 7, Z(k) + 4, names[k], 12, 'end', 'bold'))
        for k in range(2):
            lo, h_ = word[k], word[k + 1]; sgn = 1 if abs((OFF[h_] - OFF[lo]) % 1 - 1 / 3) < 1e-9 else -1
            for r in range(-2, 5):
                t = r + OFF[lo]
                for dt, w in ((sgn / 3, 2.4), (-2 * sgn / 3, 1.0)):
                    if ymin <= t <= ymax and ymin <= t + dt <= ymax: b.append(line(X(t), Z(k), X(t + dt), Z(k + 1), w, TEAL))
        t0 = 1 + OFF[word[0]]; s2 = 1 / 3 if kind == 'c' else -1 / 3
        b.append(line(X(t0), Z(0), X(t0 + 1 / 3), Z(1), 3.6, '#000')); b.append(line(X(t0 + 1 / 3), Z(1), X(t0 + 1 / 3 + s2), Z(2), 3.6, '#000'))
        for k, L in enumerate(word):
            for r in range(-2, 5):
                t = r + OFF[L]
                if ymin <= t <= ymax: b.append(circ(X(t), Z(k), 3.0))
        title = f"{'T-c' if kind == 'c' else 'T-h'}: B is {kind}, links {'run straight on' if kind == 'c' else 'turn back'}"
        b.append(text(X((ymin + ymax) / 2), 40, title, 11, 'middle', 'bold'))
        b.append(text(X((ymin + ymax) / 2), 247, 'ridges → (towards the bind-off edge)', 9.5))
        return X, Z
    Wp = 2.8 * p * U + 70
    X, Z = panel(0, 'ABC', 'c', ['A', 'B', 'C']); panel(Wp + 14, 'ABA', 'h', ['A', 'B', 'A′'])
    b.append(line(X(2.45) + 14, Z(0), X(2.45) + 14, Z(1), 0.8)); b.append(text(X(2.45) + 17, (Z(0) + Z(1)) / 2 + 4, 'd', 10, 'start', italic=True))
    def plan(cx, cy, kind):
        Rr = 64; out = []
        up = [(u, v) for _, _, u, v in up_links('B', 'C' if kind == 'c' else 'A')]
        dn = [(-u, -v) for _, _, u, v in up_links('A', 'B')]
        V = lambda u, v: (cx - Rr * (float(u) + float(v) / 2), cy - Rr * float(v) * p)
        for i, j in itertools.product(range(-2, 3), repeat=2):
            x, y = V(i, j)
            if math.hypot(x - cx, y - cy) < 1.15 * Rr: out.append(circ(x, y, 2.2, '#aaa'))
        for u, v in dn: out.append(line(cx, cy, *V(u, v), 1.5, '#000', '4 3'))
        for u, v in up:
            ex, ey = V(u, v); out.append(line(cx, cy, ex, ey, 2.6, TEAL)); out.append(circ(ex, ey, 4.2, 'none', '#000', 1.2))
            ds, dr = st_r(u, v); out.append(text(ex + (ex - cx) * 0.55, ey + (ey - cy) * 0.55 + 3, f'{fr0(ds)} st, {fr0(dr)} r', 8.5, 'middle', c='#333'))
        out.append(circ(cx, cy, 4.4))
        out.append(text(cx, cy - 98, f"plan at a node of B ({kind}):", 10.5, 'middle', 'bold'))
        out.append(text(cx, cy - 85, f"links up {'opposite' if kind == 'c' else 'over'} the links down", 10.5, 'middle', 'bold'))
        return ''.join(out)
    b.append(plan(Wp / 2, 386, 'c')); b.append(plan(Wp + 14 + Wp / 2, 386, 'h'))
    b.append(text(Wp + 7, 484, 'black: one pair of links followed through sheet B · thick line: two links (in front of and behind the section) · thin line: one link', 8.4))
    b.append(text(Wp + 7, 497, 'dashed: links down to A · ring: top end of a link up', 8.4))
    b.append(text(Wp + 7, 510, 'st = stitches (+ towards higher stitch numbers) · r = ridges (+ towards the bind-off edge)', 8.4))
    save('ch.svg', svg(2 * Wp + 14, 516, ''.join(b)))

# --- a stacking sequence seen from the side edge (cord zigzag)
def seq_side(name):
    S = SEQ[name]; P = S['P']; off = [float(o) for o in P['off']]; U = 62 if S['n'] <= 7 else 44
    tmin, tmax = min(off) - 0.3, max(off) + 2.3
    ns = S['n']; dd = math.sqrt(2 / 3); top = 40; ybot = top + 20 + (ns - 1) * dd * U
    body, X, Z = section(P['word'], 52, ybot, U, tmin, tmax, follow=1, names=[f"{k + 1} {w}" for k, w in enumerate(P['word'])])
    W = max(X(tmax) + 40, 340)
    b = [body, text(8, 18, f'{name}: side view along a row of nodes', 11, 'start', 'bold'),
         text(W / 2, ybot + 22, 'ridges → (towards the bind-off edge)', 9.5)]
    save(f'seq-{name}-side.svg', svg(W, ybot + 30, ''.join(b)))

# --- card template, true scale at the reference gauge (print at 100 %)
def card():
    a = a_mm; base, hgt = a / math.sqrt(3), math.sqrt(2 / 3) * a; b = []; top = max(hgt, ell_mm(T_REF)); x0, y0 = 8, 6 + top
    b.append(poly([(x0, y0), (x0 + base, y0), (x0 + base, y0 - hgt)], '#faf6ea', '#000', 0.35))
    r = 11; ang = math.radians(TILT)
    b.append(f'<path d="M {x0 + r:.2f} {y0:.2f} A {r} {r} 0 0 0 {x0 + r * math.cos(ang):.2f} {y0 - r * math.sin(ang):.2f}" fill="none" stroke="#000" stroke-width="0.3"/>')
    b.append(text(x0 + 13.5, y0 - 4.2, f'{TILT:.1f}°', 3.3, 'start'))
    b.append(text(x0 + base / 2, y0 + 4.2, f'a/√3 = {base:.1f} mm (lies on the sheet)', 3.1))
    b.append(text(x0 + base + 1.5, y0 - hgt / 2, f'd = {hgt:.1f} mm', 3.1, 'start'))
    b.append(f'<text font-size="3.1" text-anchor="middle" transform="translate({x0 + base / 2 - 3.5:.2f},{y0 - hgt / 2 - 1:.2f}) rotate({-TILT:.2f})">a = {a:.1f} mm (link)</text>')
    xs = x0 + base + 28; ell_ = ell_mm(T_REF)
    b.append(poly([(xs, y0), (xs + 8, y0), (xs + 8, y0 - ell_), (xs, y0 - ell_)], '#faf6ea', '#000', 0.35))
    b.append(f'<text font-size="3.1" text-anchor="middle" transform="translate({xs + 5:.2f},{y0 - ell_ / 2:.2f}) rotate(-90)">cord strip ℓ = {ell_:.1f} mm (t = {T_REF} mm)</text>')
    xb = xs + 22
    b.append(line(xb, y0, xb, y0 - 50, 0.6)); b.append(line(xb - 1.5, y0, xb + 1.5, y0, 0.4)); b.append(line(xb - 1.5, y0 - 50, xb + 1.5, y0 - 50, 0.4))
    b.append(f'<text font-size="3.1" text-anchor="middle" transform="translate({xb + 4:.2f},{y0 - 25:.2f}) rotate(-90)">50 mm: check the print</text>')
    W = xb + 10
    save('card.svg', svg(W, top + 13, ''.join(b), wmm=round(W, 2)))
    return round(W, 2)

chart(); nk_fig(); mark_fig(); icord_fig(); attach_fig(); lace_fig(); hang_fig(); measure_fig(); ch_fig()
for name in PIECES:
    r_ = R[name]; P_ = r_['P']
    view3d(P_, r_['links'], r_['C'], f'piece-{name}.svg', theta=22, phi=-22)
    view3d(P_, r_['links'], r_['C'], f'side-{name}.svg', phi=90, theta=4, H=300, node_labels=False)
    view3d(P_, r_['links'], r_['C'], f'cells-{name}.svg', mode='cells')
    view3d(P_, r_['links'], r_['C'], f'stage1-{name}.svg', upto=1, free_gap=0, frames=True, W=760, H=500)
    view3d(P_, r_['links'], r_['C'], f'stage2-{name}.svg', upto=2, frames=True, W=760, H=500)
    view3d(P_, r_['links'], r_['C'], f'stage3-{name}.svg', upto=2, free_gap=1, frames=True, W=760, H=500)
    layout_fig(name)
for name, S in SEQ.items():
    seq_side(name)
    view3d(S['P'], S['links'], S['C'], f'seq-{name}-3d.svg', theta=16, phi=-24, W=640, H=560 if S['n'] > 7 else 470, node_labels=False,
           sheet_lab=lambda k, P=S['P']: f"{k + 1} {P['word'][k]}", lab_size=10)
CARD_W = card()
open(os.path.join(DATA, 'check.out'), 'w').write('\n'.join(LOG) + '\n')

# ---------------------------------------------------------------- the booklet
SHEET_W, SHEET_H = COLS * 10 / S_REF, RIDGES * 10 / R_REF
THICK = 2 * d_cm + T_REF / 10
ELL = ell_mm(T_REF)
CORE_M = 42 * (ELL + 40) / 1000
def fig(src, cap, w=None, cls=''):
    st = f' style="width:{w}"' if w else ''
    return f'<figure class="{cls}"><img src="figs/{src}"{st} alt=""><figcaption>{cap}</figcaption></figure>'
def nnum(n): return 1 + n[1] + 3 * n[2]

def sheet_rows():
    out = [f'<li>With 3.5 mm needles, cast on {COLS} sts (long-tail). Mark the side facing you as the RS (Row 1 is a RS row).</li>']
    prev = 0
    for j in range(3):
        r = node_row(j)
        out.append(f'<li><b>Rows {prev + 1}–{r - 1}:</b> knit.</li>')
        parts, pos = [], 0
        for i in range(3):
            st = node_st(i, j); parts.append(f'K{st - pos - 1}' if st - pos - 1 else ''); parts.append(f'NK [{1 + i + 3 * j}]'); pos = st
        parts.append(f'K{COLS - pos}')
        out.append(f'<li><b>Row {r} (RS, node row {j + 1}, ridge {node_ridge(j)}):</b> {", ".join(x for x in parts if x)}. ({COLS} sts)</li>')
        prev = r
    out.append(f'<li><b>Rows {prev + 1}–{ROWS}:</b> knit. ({RIDGES} ridges)</li>')
    out.append('<li>Bind off knitwise on the next RS row. Do not block. Tie a tag with the sheet\'s letter to the cast-on edge.</li>')
    return '<ol class="rows">' + ''.join(out) + '</ol>'

def node_table():
    rows = ''.join(f'<tr><td><b>{1 + i + 3 * j}</b></td><td class="n">{node_row(j)}</td><td class="n">{node_ridge(j)}</td><td class="n">{node_st(i, j)}</td></tr>'
                   for j in range(3) for i in range(3))
    return ('<table class="nt"><tr><th>node</th><th class="n">row</th><th class="n">ridge</th><th class="n">stitch</th></tr>' + rows + '</table>')

def gap_table(name, g):
    P = R[name]['P']; L = R[name]['links']
    rows = []
    for n, x in enumerate(L):
        if x[0][0] != g: continue
        ds, dr = st_r(x[2], x[3])
        rows.append(f'<tr><td class="n">{n + 1}</td><td><b>{lab(P, x[0])}</b></td><td><b>{lab(P, x[1])}</b></td><td>{fr0(ds)} st, {fr0(dr)} r</td><td class="box">☐</td></tr>')
    lo, hi = P['names'][g], P['names'][g + 1]
    st = 'forward' if P['steps'][g] > 0 else 'backward'
    head = (f'<table class="lt"><tr><th colspan="5">Gap {g + 1}: sheet {lo} → sheet {hi} ({st} step), cords {21 * g + 1}–{21 * g + 21}</th></tr>'
            '<tr><th class="n">cord</th><th>from</th><th>to</th><th>top end lies</th><th>done</th></tr>')
    return f'<div class="two">{head + "".join(rows[:11]) + "</table>"}{head + "".join(rows[11:]) + "</table>"}</div>'

def by_target(name, g):
    P = R[name]['P']; L = R[name]['links']; out = []
    for j in range(3):
        for i in range(3):
            t = (g + 1, i, j); src = [f'{n + 1} (from {lab(P, x[0])})' for n, x in enumerate(L) if x[1] == t]
            out.append(f'<li><b>{lab(P, t)}</b>: cords {", ".join(src) if src else "none"}</li>')
    return '<ul class="recv">' + ''.join(out) + '</ul>'

def stack_table(name):
    P = R[name]['P']; nm = P['names']; rows = []
    pos = ['bottom', 'middle', 'top']
    for k in range(3):
        ds, dr = st_r(P['off'][k], P['off'][k]); cm = math.sqrt(float(norm2(P['off'][k], P['off'][k]))) * a_cm
        step = '' if k == 0 else ('forward' if P['steps'][k - 1] > 0 else 'backward')
        where = 'reference' if k == 0 else (f'{fr0(ds)} st, {fr0(dr)} r ({cm:.1f} cm)' if ds or dr else 'straight over A1')
        rows.append(f'<tr><td><b>{nm[k]}</b></td><td>{pos[k]}</td><td>{step}</td><td>{where}</td></tr>')
    return ('<table class="sz"><tr><th>sheet</th><th>place</th><th>step from the sheet below</th><th>node 1 seen from above, from A1</th></tr>'
            + ''.join(rows) + '</table>')

def pattern(name):
    P = R[name]['P']; r = R[name]; kind = P['kind']; nm = P['names']; cnt = r['cnt']; top = nm[2]
    word = '-'.join(nm); g2 = 'forward' if kind == 'c' else 'backward'
    ds2, dr2 = st_r(P['off'][2], P['off'][2]); ds21, dr21 = st_r(P['off'][2] - P['off'][1], P['off'][2] - P['off'][1])
    ntet = sum(1 for c in r['C'] if c['kind'] == 'tet'); noct = sum(1 for c in r['C'] if c['kind'] == 'oct')
    nb = sum(1 for c in r['C'] if c['kind'] == 'tet' and c['base'] == 1)
    h = [f'<h1 class="brk pat">Pattern {name}: {word} (middle sheet {kind})</h1>']
    if kind == 'c':
        what = (f'Three sheets, each moved on from the one below by the same step: A, then B, then C. The middle sheet B is <b>c</b>: '
                'each cord up from a B node runs on in a straight line from a cord coming down into it. This is the start of the cubic stacking 3C.')
    else:
        what = ('Three sheets A, B, A′: the top sheet A′ lies straight over A. The middle sheet B is <b>h</b>: each cord up from a B node is the mirror '
                'image of a cord coming down into it, so the cords turn back in a chevron. This is the start of the hexagonal stacking 2H.')
    h.append(f'''<h2>What you are making</h2>
<p>{what} The cells around B are the pieces of the HexOct {kind}-tile (#75, at λ = −1/8). Sizes of every piece are in the table
“Sizes of a finished piece” (Techniques); for {name}:</p>
<table class="sz"><tr><th>{name}</th><th class="n"></th></tr>
<tr><td>sheets · node stitches · cords</td><td class="n">3 · 27 · 42</td></tr>
<tr><td>height (2<i>d</i> + one sheet thickness)</td><td class="n">{THICK:.1f} cm</td></tr>
<tr><td>top sheet {top} over sheet A</td><td class="n">{f"{fr0(ds2)} st, {fr0(dr2)} ridges ({math.sqrt(float(norm2(P['off'][2], P['off'][2]))) * a_cm:.1f} cm sideways)" if ds2 or dr2 else "straight over, 0 cm sideways"}</td></tr>
<tr><td>cells closed by sheets and cords</td><td class="n">{ntet} tetrahedra, {noct} octahedra</td></tr></table>''')
    h.append(f'<div>{fig(f"piece-{name}.svg", f"Figure {name}.1. The finished piece {name}, tensioned, seen from the front (cast-on edges towards you) and above. Grey: the three sheets; dots: node stitches; dashed: the sheet between neighbouring nodes; teal: the 42 cords, each of length <i>a</i> at {TILT:.1f}°.", "62%")}'
             f'{fig(f"side-{name}.svg", f"Figure {name}.2. The same piece seen from its side edge (the bind-off edges to the right): the cords {chr(10)}" + ("run on the same way through B." if kind == "c" else "turn back at B, and A′ is straight over A."), "62%")}</div>')
    h.append(f'''<h2>You need</h2>
<p>Three sheets knitted as in “The sheet”, tagged <b>A</b>, <b>B</b> and <b>{top}</b>; yarn for 42 cords; the materials listed at the front for one piece.</p>
<h2>How the sheets are stacked</h2>
<p>The stacking is not knitted in: the cords set it when the piece is tensioned. The table and the plan show where each sheet ends up, so that you can hold
each sheet near its place while you sew, and check the piece at the end.</p>
{stack_table(name)}''')
    h.append(fig(f'layout-{name}.svg', f'Figure {name}.3. Stacking plan of {name}, seen from above. Each sheet is drawn with its outline and its 9 nodes; '
                 + ('B sits one step on from A, and C one more step on in the same direction.' if kind == 'c' else 'B sits one step on from A; A′ steps back and lies exactly over A (squares around the circles).'), '82%'))
    # assembly
    h.append(f'<h2 class="brk">Assembly of {name}, step by step</h2>')
    h.append(f'''<p class="step"><b>Step 1.</b> Check the three sheets: each has 9 node stitches with a contrast thread, and a tag (A, B, {top}).</p>
<p class="step"><b>Step 2.</b> Lace sheet A into its frame, RS up, cast-on edge towards you (see “Lacing a sheet into its frame”). Check the node triangles: <i>a</i> = {a_cm:.1f} cm.</p>
<p class="step"><b>Step 3.</b> Work cords 1–21 from the nodes of sheet A, in the order of the table (see “Making a cord”). Knit each to the same row count;
pin its 3 live sts and tag it with its number and target node. Tick each cord off in the “done” column.</p>''')
    h.append(gap_table(name, 0))
    h.append(fig(f'stage1-{name}.svg', f'Figure {name}.4. After step 3: sheet A in its frame with its 21 cords standing; the rings are the free ends on their pins, '
                 'drawn where they will be sewn.', '66%'))
    h.append(f'''<p class="step"><b>Step 4.</b> Lace sheet B into its frame the same way and hold it over sheet A, about <i>d</i> = {d_cm:.1f} cm above,
with B1 over the point +8 st and +4⅔ ridges from A1 (Figure {name}.3).</p>
<p class="step"><b>Step 5.</b> Sew cords 1–21 to sheet B, node by node (see “Sewing a cord to a node”). Each node of B receives these cords:</p>
{by_target(name, 0)}''')
    h.append(fig(f'stage2-{name}.svg', f'Figure {name}.5. After step 5: sheets A and B joined by the 21 cords of gap 1.', '66%'))
    turn = ('Their top ends lean on in the same direction as the cords of gap 1: B is c.' if kind == 'c' else
            'Their top ends lean back, over the nodes of A: this is the h turn at B.')
    h.append(f'''<p class="step"><b>Step 6.</b> Work cords 22–42 from the nodes of sheet B, on its RS (gap 2: {g2} step), pin and tag them. {turn}</p>''')
    h.append(gap_table(name, 1))
    h.append(fig(f'stage3-{name}.svg', f'Figure {name}.6. After step 6: the 21 cords of gap 2 stand on sheet B with free ends.', '66%'))
    place = (f'{top}1 over the point {fr0(ds21)} st and {fr0(dr21)} ridges from B1, that is {fr0(ds2)} st and {fr0(dr2)} ridges from A1' if kind == 'c'
             else f'{top}1 over the point {fr0(ds21)} st and {fr0(dr21)} ridges from B1, straight over A1')
    h.append(f'''<p class="step"><b>Step 7.</b> Lace sheet {top} into its frame, hold it over B at about <i>d</i> with {place}, and sew cords 22–42 node by node:</p>
{by_target(name, 1)}
<p class="step"><b>Step 8.</b> Weave in all ends. Remove the contrast threads, or leave them as node marks. The piece now looks like Figure {name}.1.</p>
<p class="step"><b>Step 9.</b> Tension the piece and stand it on posts (see “Finishing”), then check it (below).</p>''')
    # check
    deg = r['deg']
    degtab = ''.join(f'<tr><td>sheet {nm[k]}</td>' + ''.join(f'<td class="n">{deg[(k, i, j)]}</td>' for j in range(3) for i in range(3)) + f'<td class="n">{sum(deg[(k, i, j)] for i in range(3) for j in range(3))}</td></tr>' for k in range(3))
    h.append(f'<h2 class="brk">{name}: check your work</h2>')
    h.append(f'''<table class="sz"><tr><th>count</th><th class="n">expected</th></tr>
<tr><td>node stitches (9 per sheet)</td><td class="n">27</td></tr>
<tr><td>cords (gap 1 + gap 2)</td><td class="n">42 (21 + 21)</td></tr>
<tr><td>gap 1 (A–B): tetrahedra on A · tetrahedra hanging from B · octahedra</td><td class="n">{cnt[0]["tet_lo"]} · {cnt[0]["tet_hi"]} · {cnt[0]["oct"]}</td></tr>
<tr><td>gap 2 (B–{top}): tetrahedra on B · tetrahedra hanging from {top} · octahedra</td><td class="n">{cnt[1]["tet_lo"]} · {cnt[1]["tet_hi"]} · {cnt[1]["oct"]}</td></tr>
<tr><td>plumb line from {top}1 meets sheet A</td><td class="n">{f"{fr0(ds2)} st, {fr0(dr2)} ridges from A1" if ds2 or dr2 else "on A1"}</td></tr></table>
<table class="dg"><tr><th>cords per node</th>{"".join(f"<th class='n'>{t}</th>" for t in range(1, 10))}<th class="n">sum</th></tr>{degtab}</table>
<p>This piece holds {nb} tetrahedral pieces and {nb * 2} octahedral halves of sheet B; around node {", ".join(r["full"])} the four pieces of one whole
{kind}-tile are all closed (checked against tiles.py of #75). {"The octahedra of gap 2 are set aside from those of gap 1 (c)." if kind == "c" else "The octahedra of gap 2 sit straight over those of gap 1 (h)."}</p>''')
    h.append(fig(f'cells-{name}.svg', f'Figure {name}.7. The tensioned piece with the cells of sheet B coloured as its HexOct {kind}-tile pieces (#75, λ = −1/8): '
                 'gold, tetrahedral pieces; violet, octahedral halves (lighter: below B, darker: above B); teal, the cords. '
                 f'Cells of sheets A and {top} are left open.', '78%'))
    return '\n'.join(h)

def gauge_table():
    rows = []
    for q in [Fr(85, 100), Fr(90, 100), Fr(95, 100), Fr(1), Fr(105, 100), Fr(110, 100), Fr(115, 100)]:
        m = round(0.866 * N * float(q)); err = m / (math.sqrt(3) / 2 * N * float(q)) - 1
        rows.append(f'<tr><td class="n">{float(q):.2f}</td><td class="n">{m}</td><td class="n">{err * 100:+.1f} %</td></tr>')
    return ('<table class="gt"><tr><th class="n">R / S</th><th class="n">M (N = 16)</th><th class="n">row spacing error</th></tr>' + ''.join(rows) + '</table>')

# --- stacking sequences
SEQ_TEXT = {
    '3C': 'All inner sheets c: every gap is a forward step. A followed cord path runs straight through the whole stack in one slant, and every sheet moves on by the same step, so the stack leans.',
    '2H': 'All inner sheets h: forward and backward steps alternate. Every followed cord path turns back at every inner sheet, a column of chevrons; sheets 1, 3 and 5 lie straight over one another.',
    '4H': 'c and h alternate: two forward steps, then two backward steps. Cord paths slant two gaps one way, then two gaps back; sheet 5 lies straight over sheet 1.',
    '6H': 'h, c, c repeating: three forward steps, then three backward steps. Cord paths slant three gaps one way, then three back; sheet 7 lies straight over sheet 1.',
    'Fibonacci': 'The Fibonacci order of c and h: runs of equal steps of lengths 1, 3, 2, 3, 3 that never settle into a period. Cord paths wander but stay near the middle.'}
def runs(st):
    out, cur = [], 1
    for a_, b_ in zip(st, st[1:]):
        if a_ == b_: cur += 1
        else: out.append(cur); cur = 1
    return out + [cur]
assert runs(SEQ['Fibonacci']['P']['steps']) == [1, 3, 2, 3, 3]
def rule_text(s):
    pr_ = sorted(rule_pairs(s)); out = []
    for n in range(1, 10): out.append(f'{n} → {", ".join(str(m) for a_, m in pr_ if a_ == n)}')
    return '; '.join(out)
YARN_SHEET, YARN_CORD = 55, 1.0     # estimate: 3 x 55 m + 42 x 1 m = 207 m, the 210 m of a three-sheet piece
def seq_section(name):
    S = SEQ[name]; P = S['P']; n = S['n']; st = P['steps']; ch = S['inner']
    hgt = (n - 1) * d_cm + T_REF / 10; ncord = 21 * (n - 1)
    rows = []
    for k in range(n):
        ds, dr = st_r(P['off'][k], P['off'][k]); cm = math.sqrt(float(norm2(P['off'][k], P['off'][k]))) * a_cm
        rows.append(f'<tr><td class="n">{k + 1}</td><td><b>{P["word"][k]}</b></td><td>{ch[k - 1] if 0 < k < n - 1 else "end"}</td>'
                    f'<td>{"" if k == 0 else ("forward" if st[k - 1] > 0 else "backward")}</td>'
                    f'<td>{"reference" if k == 0 else (f"{fr0(ds)} st, {fr0(dr)} r ({cm:.1f} cm)" if ds or dr else "straight over sheet 1")}</td></tr>')
    gaps = []
    for g in range(n - 1):
        gl = [x for x in S['links'] if x[0][0] == g]
        gaps.append(f'<tr><td class="n">{g + 1}</td><td>{g + 1} {P["word"][g]} → {g + 2} {P["word"][g + 1]}</td><td>{"forward" if st[g] > 0 else "backward"}</td>'
                    f'<td>{"n → n, n−1, n−3" if st[g] > 0 else "n → n, n+1, n+3"}</td><td class="n">{21 * g + 1}–{21 * g + 21}</td><td class="n">{len(gl)}</td>'
                    f'<td class="n">{S["cnt"][g]["tet_lo"]} · {S["cnt"][g]["tet_hi"]} · {S["cnt"][g]["oct"]}</td></tr>')
    nf = sum(1 for x in st if x > 0); nbk = len(st) - nf
    h = [f'<h2 class="brk">{name}: {P["word"]} ({ch}, {n} sheets)</h2>',
         f'<p>{SEQ_TEXT[name]} #83 writes it {P["word"]} ({S["lab83"] if len(S["lab83"]) > 1 else "all " + S["lab83"]}).</p>',
         f'''<table class="sz"><tr><th>{name}</th><th class="n"></th></tr>
<tr><td>sheets (each knitted as in “The sheet”) · node stitches</td><td class="n">{n} · {9 * n}</td></tr>
<tr><td>cords (21 per gap × {n - 1} gaps)</td><td class="n">{ncord}</td></tr>
<tr><td>gaps: forward · backward</td><td class="n">{nf} · {nbk}</td></tr>
<tr><td>height ({n - 1}<i>d</i> + one sheet thickness)</td><td class="n">{hgt:.1f} cm</td></tr>
<tr><td>yarn, estimate (about {YARN_SHEET} m per sheet and {YARN_CORD:.0f} m per cord)</td><td class="n">about {YARN_SHEET * n + YARN_CORD * ncord:.0f} m ({math.ceil((YARN_SHEET * n + YARN_CORD * ncord) / 100)} balls of 50 g)</td></tr>
<tr><td>contrast threads · frames · posts (4 per gap) · safety pins (reused each gap)</td><td class="n">{9 * n} · {n} · {4 * (n - 1)} · 21</td></tr></table>''',
         '<div class="two">' + fig(f'seq-{name}-side.svg', f'Figure {name}.1. {name} seen from the side edge, sheets as lines, cords seen along a row of nodes (thick: two cords, one in front of and one behind the section; thin: one cord). Black: one cord path followed up the stack. Right: c (teal) or h (violet) of each inner sheet.')
         + fig(f'seq-{name}-3d.svg', f'Figure {name}.2. The tensioned {name} stack ({n} sheets, {ncord} cords), from the front and above; labels give sheet number and letter.') + '</div>',
         '<table class="sq"><tr><th class="n">sheet</th><th>letter</th><th>c / h</th><th>step from below</th><th>node 1 from sheet 1 node 1 (from above)</th></tr>' + ''.join(rows) + '</table>',
         '<table class="sq"><tr><th class="n">gap</th><th>sheets</th><th>step</th><th>cord rule (node n below → nodes above)</th><th class="n">cords</th><th class="n">count</th><th class="n">tet up · tet down · oct</th></tr>' + ''.join(gaps) + '</table>',
         f'<p class="small"><b>Check.</b> {9 * n} node stitches; {ncord} cords, 21 in every gap; every gap closes 4 tetrahedra standing on its lower sheet, 4 hanging from its upper sheet and 4 octahedra; '
         f'the cords per node add up to {2 * ncord}. All of this is generated and asserted by patterns.py, and the c/h word is checked against #83.</p>']
    return '\n'.join(h)

def seq_part():
    rows = []
    for nm_, S in SEQ.items():
        P = S['P']; mean = sum(P['steps']) / len(P['steps'])
        rows.append(f'<tr><td><b>{nm_}</b></td><td>{S["lab83"] if len(S["lab83"]) > 1 else "all " + S["lab83"]}</td><td>{P["word"]}</td><td>{S["inner"]}</td>'
                    f'<td class="n">{S["n"]}</td><td class="n">{21 * (S["n"] - 1)}</td><td>{"".join("+" if x > 0 else "−" for x in P["steps"])}</td><td class="n">{mean:+.2f}</td></tr>')
    h = ['<h1 class="brk">Stacking sequences</h1>']
    h.append(f'''<p>T-c and T-h are the smallest pieces of two stackings. Any close-packed stacking can be knitted the same way, because
<b>every sheet is the same knit</b> (“The sheet”). Only the cords decide where a sheet goes. In each gap the cords make either a
<b>forward step</b> (the upper sheet moves on by +8 st and +4⅔ ridges: A → B, B → C, C → A) or a <b>backward step</b> (−8 st and −4⅔ ridges:
B → A, C → B, A → C). An inner sheet is <b>c</b> when the steps below and above it are the same: its cords run straight on. It is <b>h</b> when they differ:
its cords turn back in a chevron. So the c/h word of the inner sheets decides the whole stack. The stacking sequences below are the five of #83
(DICTO's HexOct: Knitting Crystals); there they were flat swatches, here each is a three-dimensional HexOct structure of sheets and cords.</p>
<h2>The rule for any sequence</h2>
<ol>
<li>Write the c/h word of the inner sheets: a stack of <i>n</i> sheets has <i>n</i> − 2 inner sheets.</li>
<li>Sheet 1 is A, sheet 2 is B.</li>
<li>Each further sheet: if the sheet below it is <b>c</b>, it takes the letter that is not one of the two sheets below it; if <b>h</b>, it repeats the letter two below.</li>
<li>Each gap is forward (A → B, B → C, C → A) or backward (the other three).</li>
<li>Each gap has 21 cords, from the 9 nodes of the lower sheet (node numbers 1–9 as in the chart):<br>
forward: {rule_text(1)};<br>backward: {rule_text(-1)}.<br>
A node at the edge of the patch has fewer cords: a target outside 1–9 is left out.</li>
<li>Number the cords gap by gap: gap <i>g</i> has cords 21(<i>g</i> − 1) + 1 to 21<i>g</i>, in order of the lower node and then the upper node.</li></ol>
<p><b>Growing the Fibonacci word.</b> Start with <b>a</b>. Replace every a by ab and every b by a, and repeat: a, ab, aba, abaab, abaababa, abaababaabaab.
Then write c for a and h for b: <b>{FIB13}</b>. #83 uses these 13 letters as the labels of 13 layers, the end layers included as if the stack went on.
In a knitted stack of 13 sheets the 11 inner sheets carry letters 2–12, {SEQ["Fibonacci"]["inner"]}, and the rule gives the sheet letters
{SEQ["Fibonacci"]["P"]["word"]}, the word printed in #83. (The end labels have no effect on the knitting: no cords go beyond the end sheets.)</p>
<table class="sq"><tr><th>sequence</th><th>c/h in #83</th><th>sheet letters</th><th>inner sheets</th><th class="n">sheets</th><th class="n">cords</th><th>steps, gap 1 up</th><th class="n">mean step</th></tr>
{"".join(rows)}</table>
<p class="small">Mean step: (forward − backward) / gaps, the net c-twist (mean Hägg symbol) of #83 part 2, for these stacks. Every word here was checked by script against
#83: the c/h of each sheet, the rule rebuilding the letters, and the Fibonacci growth; the 12-sheet words of #83 part 2 were checked too (c/h and mean Hägg symbol).</p>
<h2>Building a stack of n sheets</h2>
<p>The steps are those of T-c and T-h, gap by gap from the bottom up. Techniques as in the shared section.</p>
<ol>
<li>Knit <i>n</i> sheets as in “The sheet”. Tag each with its number and letter (1 A, 2 B, 3 A, …).</li>
<li>Lace sheet 1 into its frame, RS up, cast-on edge towards you.</li>
<li>For each gap <i>g</i> = 1, 2, …, <i>n</i> − 1: work the 21 cords of the gap from sheet <i>g</i> by the gap's rule (cord table of the sequence), pin and tag each with its
number and target node; lace sheet <i>g</i> + 1 into its frame; hold it about <i>d</i> above sheet <i>g</i>, placed as the offset table shows; sew the cords node by node.</li>
<li>Weave in all ends. Hang the stack by the top frame and tension it; set four posts per gap where the two frames overlap (in 3C each frame sits 4.2 cm on from the one below).</li>
<li>Check it: the sequence's check line; the card and plumb-line checks of the shared section, sheet by sheet.</li></ol>''')
    for nm_ in SEQ: h.append(seq_section(nm_))
    h.append('''<h2 class="brk">What you will see and feel</h2>
<p>#83 part 2 (“Knitted HexOct: c/h as a design dial”) tested the stackings in an idealised model: straight rods for the cords meeting at the nodes, blocks of
12 sheets, periodic sideways. All cord lengths, angles and node counts are the same in every stacking, so every stacking has the same density.</p>
<p><b>The same in every sequence.</b> Pressing down through the thickness: the compression stiffness, the strain at which the first cords buckle, and the
work done in compression are the same in 3C, 2H, 4H, 6H and the Fibonacci stack (to 4 digits). Through-thickness stiffness does not tell the stackings apart.</p>
<p><b>What changes.</b></p>
<ul>
<li><b>Looking straight down through the stack.</b> The open area along the stacking direction depends only on which of the three cord directions in plan
(AB, BC, CA) occur: 2H has one, 4H two, and 3C, 6H and Fibonacci all three. At cord radius 0.05&nbsp;<i>a</i>: 2H 34.7 %, 4H 9.9 %, 3C, 6H and Fibonacci 3.25 %;
at 0.1&nbsp;<i>a</i>: 2H 14.3 %, all others 0. In the model the sheets are open (rods between the nodes). A garter sheet is closed fabric, so this difference
shows only between the sheets, or in a stack whose sheets are worked open.</li>
<li><b>Pushing the top sideways against the bottom</b> (transverse shear), when the sheets are soft and free to stretch in their own plane, as knitted sheets are.
With cords only and rigid joints the free shear stiffness is (in 10<sup>−3</sup>&nbsp;<i>E</i><sub>s</sub>) 0.193 for 3C, 3.378 for 2H, 3.283 for 4H, 3.276 for 6H
and 3.275 for Fibonacci: 3C is about 17 times softer in shear than 2H. The controlling number is the net c-twist (mean step), not the share of c sheets: an h sheet
reverses the twist, so c runs split by h sheets cancel. With sheets as stiff as the cords the 3C/2H ratio rises to 0.90.</li></ul>
<p class="small">These are model results, not measurements: no yarn mechanics (loops, friction, cords that cannot carry compression), and small 3 × 3-node pieces have
edges that the periodic model does not. The pieces in this booklet are the physical tests that #83 part 2 asks for; none has been knitted yet.</p>''')
    return '\n'.join(h)

CSS = '''table{border-collapse:collapse;font-size:7.8pt;margin:1.5mm 0;width:100%} td,th{border-bottom:1px solid #ddd;padding:0.5mm 1.1mm;text-align:left;vertical-align:top} td.n,th.n{text-align:right}
body,p,li{font-size:8.9pt;line-height:1.38} h1{font-size:17pt} h1.pat{font-size:15pt;margin-top:0} h1.brk{font-size:13pt;margin-top:0} .logo{width:22mm}
h2{font-size:11pt;margin:3mm 0 1mm} h3{font:600 9.6pt "DejaVu Sans",sans-serif;margin:2mm 0 0.5mm} h2,h1,h3{break-after:avoid} ol,ul{margin:1mm 0 1mm 5mm;padding-left:3mm} li{margin:0.4mm 0}
figure{margin:2mm 0;break-inside:avoid;text-align:center} figure img{width:100%;display:block;margin:0 auto} figcaption{font-size:7.8pt;line-height:1.33;color:#333;margin-top:1mm;text-align:left}
.brk{break-before:page} .status{border:1px solid #b8962e;background:#faf6ea;padding:2mm 3mm;font:8pt "DejaVu Sans",sans-serif;margin:0 0 3mm}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:start} .two table{font-size:7.6pt} .small{font-size:7.9pt}
.sheet{display:grid;grid-template-columns:1.7fr 1fr;gap:4mm;break-inside:avoid} ol.rows li{font-size:8.6pt} table.nt{font-size:7.6pt}
table.sz{width:auto;min-width:60%} table.gt{width:auto} table.dg td,table.dg th{padding:0.4mm 1.2mm} .abbr td:first-child{font-weight:bold;white-space:nowrap}
p.step{margin:2mm 0 1mm} ul.recv{columns:3;font-size:7.9pt;margin-left:4mm} ul.recv li{break-inside:avoid} td.box{text-align:center;font-size:9pt}
table.sq{font-size:7.6pt} table.lt th[colspan]{color:#6b5310}'''

contents = ''.join(f'<li>{t}</li>' for t in [
    'Materials, gauge, abbreviations',
    'The sheet: the node stitch, row by row, chart, marking (one instruction for every sheet)',
    'Techniques used in every piece: sizes, lacing a sheet into its frame, making a cord, sewing a cord to a node, finishing, measuring, the card template, the cells',
    'Pattern T-c (A-B-C, middle sheet c): what you are making, stacking, assembly step by step with all 42 cords, check your work',
    'Pattern T-h (A-B-A′, middle sheet h): the same parts',
    'c against h: the two patterns compared',
    'Stacking sequences: the rule for any sequence; 3C, 2H, 4H, 6H and Fibonacci as knitted stacks; what you will see and feel'])

shared = f'''<h1 class="brk">Techniques used in every piece</h1>
<p>These steps are the same in T-c, T-h and every stack. Each pattern says when to use them.</p>
<h2>Sizes of a finished piece</h2>
<p>When the sheets are pulled apart until every cord is taut, the cords stand at {TILT:.1f}° to the sheets, the sheets lie <i>d</i> = √(2/3)&nbsp;<i>a</i> apart,
and sheets and cords close off tetrahedra and octahedra in space. At the reference gauge:</p>
<table class="sz"><tr><th>at {S_REF} sts and {R_REF} ridges per 10 cm (N = {N}, M = {M})</th><th class="n"></th></tr>
<tr><td>node spacing <i>a</i> (= cord length, node to node)</td><td class="n">{a_cm:.2f} cm</td></tr>
<tr><td>sheet spacing <i>d</i> = √(2/3)&nbsp;<i>a</i> (mid-plane to mid-plane)</td><td class="n">{d_cm:.2f} cm</td></tr>
<tr><td>each sheet ({COLS} sts × {RIDGES} ridges)</td><td class="n">{SHEET_W:.1f} × {SHEET_H:.1f} cm</td></tr>
<tr><td>node patch in each sheet (node 1 to node 9)</td><td class="n">{3 * a_cm:.1f} × {math.sqrt(3) * a_cm:.1f} cm</td></tr>
<tr><td>one step between sheets (seen from above)</td><td class="n">8 st, 4⅔ ridges = <i>a</i>/√3 = {a_cm / math.sqrt(3):.1f} cm</td></tr>
<tr><td>height of a piece of <i>n</i> sheets</td><td class="n">(<i>n</i> − 1)&nbsp;<i>d</i> + {T_REF / 10:.2f} cm</td></tr></table>
<h2>Lacing a sheet into its frame</h2>
<p>Lay the sheet RS up in its frame, cast-on edge towards you. Lace it to the frame all round with strong thread, firm but not stretched. Then measure
the node triangles (1-2-4, 2-4-5, 2-3-5, …) from node centre to node centre: each side should be <i>a</i> = {a_cm:.1f} cm. Ease the lacing until they are.</p>
{fig('lace.svg', 'Lacing a sheet into its frame, seen from above. Purple: the 9 nodes; dashed: one node triangle, all sides <i>a</i>.', '86%')}
<h2>Making a cord (link)</h2>
<p><b>Cord length.</b> Every cord is a 3-stitch i-cord of the same free length ℓ = <i>a</i> − 1.22&nbsp;<i>t</i>, measured between the
two sheet faces (<i>t</i> = sheet thickness; measure it on a sheet with a ruler under light pressure). At the reference gauge
<i>a</i> = {a_mm:.1f} mm: ℓ = {ell_mm(3.0):.1f} mm for <i>t</i> = 3.0 mm, {ell_mm(3.5):.1f} mm for 3.5 mm, {ell_mm(4.0):.1f} mm for 4.0 mm.
Cut a card strip of length ℓ (or use the one on the card template). Knit the first cord to the strip under a light, even pull and count its rows; knit every other cord to the
same row count. Equal counts make equal cords.</p>
<p><b>To work one cord, from node X of the lower sheet:</b></p>
<ol>
<li>Lay the lower sheet RS up, cast-on edge towards you. With a 3.0 mm DPN, on the RS, pick up and knit 3 sts: the node stitch X and the stitch on each side of it in the same ridge (panel 1).</li>
<li>Slide the 3 sts to the other end of the DPN (panel 2).</li>
<li>Pull the yarn across the back and K3 (panel 3).</li>
<li>Repeat steps 2 and 3 to the row count (panel 4).</li>
<li>Do not bind off: put the 3 live sts on a safety pin and tag it with the cord number and its target node Y (panel 5).</li></ol>
{fig('icord.svg', f'Making a cord. 1–5: the 3-stitch i-cord from a node; 6: once the piece is tensioned, each cord runs node to node with length <i>a</i> at {TILT:.1f}° to the sheets.', '92%')}
<p class="small">In each pattern's cord table, “top end lies” is where the top of the cord ends up, seen from above, counted from its foot X:
st = stitches (+ towards higher stitch numbers), r = ridges (+ towards the bind-off edge). It is a check, not an instruction: the cords
find these places themselves when tensioned. Cords whose target would lie outside the 3 × 3 node patch are left out; that is why
nodes at the edge of the patch have fewer cords.</p>
<h2>Sewing a cord to a node</h2>
<ol>
<li>Hold the upper sheet, RS up, over the lower sheet. Find the target node Y and its two neighbours in the same ridge.</li>
<li>Thread the tapestry needle with a length of yarn. From above, pass down through the first of the 3 stitches, through one live stitch of the cord, and back up through the same stitch.</li>
<li>Do the same for the other two live stitches, one into the node stitch and one into the other neighbour. Remove the pin.</li>
<li>Fasten off on the RS. Work node by node, in the order of the pattern's list.</li></ol>
{fig('attach.svg', 'Sewing a cord to its node: 1, section through the upper sheet; 2, from above. Purple: the node stitch; gold: its neighbours; teal: the sewing yarn.', '92%')}
<h2>Finishing: tension the piece</h2>
<p>Hang the piece by the frame of the top sheet (two strings from a hook or a rod), sheets horizontal, and let the lower frames hang on the
cords. Each frame sinks until all of its cords are taut. Taut cords of equal length allow the greatest spacing only when the sheet sits
exactly in its place over the one below (spec §1: any sideways shift <i>t</i> lowers the spacing to at most √(2/3&nbsp;<i>a</i>² − <i>t</i>²));
so a hanging sheet centres itself. Tap the frames lightly so that they settle. Measure the spacing at the four corners of each frame
(expect <i>d</i> = {d_cm:.1f} cm between the sheets' mid-planes) and cut four posts to the measured length for each gap. Set the posts
between the frame corners, outside the node patch, and stand the piece on a table. If a cord is slack while the others are taut, it is
too long: unpick its sewn end and work it again to the row count.</p>
{fig('hang.svg', 'Finishing, seen from a side edge (drawn for T-c). 1: hanging from the top frame, each lower frame sinks until its cords are taut. 2: standing on four posts per gap.', '92%')}
<h2>Measure it</h2>
<ul>
<li><b>Cord length.</b> Node centre to node centre along each cord: <i>a</i> = {a_cm:.1f} cm (the same as the node spacing in a sheet). Free cord between the sheet faces: ℓ.</li>
<li><b>Sheet spacing.</b> Mid-plane to mid-plane at each frame corner: <i>d</i> = √(2/3)&nbsp;<i>a</i> = 0.8165&nbsp;<i>a</i> = {d_cm:.1f} cm (face to face {d_cm - T_REF / 10:.1f} cm).</li>
<li><b>Cord angle.</b> Stand the card template on the lower sheet, upright, its long leg vertical, its slanted edge along a cord: the cord lies on the edge, at {TILT:.2f}° to the sheet (arctan √2), and the long leg just reaches the upper sheet.</li>
<li><b>Position of the top sheet.</b> Hang a plumb line (thread and a small weight) from node 1 of the top sheet and count stitches and ridges from A1 to where it meets the bottom sheet. Compare with the pattern's stacking table. From B1 it meets sheet A at +8 st and +4⅔ ridges from A1 ({a_cm / math.sqrt(3):.1f} cm).</li></ul>
{fig('measure.svg', 'Measuring: 1, the card template against a cord; 2, the plumb line from node 1 of the top sheet.', '88%')}
<figure><img src="figs/card.svg" style="width:{CARD_W}mm" alt=""><figcaption>Card template (cord angle and sheet spacing) and cord strip, true size for
<i>a</i> = {a_mm:.1f} mm (print at 100 %; the bar must measure 50 mm). For another <i>a</i>: a right triangle with legs
0.577&nbsp;<i>a</i> (on the sheet) and 0.816&nbsp;<i>a</i> (upright); its slanted edge is <i>a</i> and its foot angle {TILT:.1f}°.
Cut it from card and use the long leg to check the sheet spacing at the same time.</figcaption></figure>
<h2>The cells: what to look for</h2>
<p>Every closed cell has all its edges of length <i>a</i>: a sheet edge between neighbouring nodes or a cord. A tetrahedron is 3 nodes of one sheet and the
one node of the next sheet linked to all three (3 cords). An octahedron is a triangle of 3 nodes below and the opposite triangle above, joined by 6 cords.
Each gap of a 3 × 3 patch closes 4 tetrahedra standing on its lower sheet, 4 hanging from its upper sheet and 4 octahedra, whatever the step. In the HexOct
tiles of #75 at λ = −1/8, the tile of a middle sheet is: the tetrahedra standing on it and hanging from it (gold in the figures), the upper halves of the
octahedra of the gap below and the lower halves of the octahedra of the gap above, cut at the gaps' mid-planes (violet; each half has 3 nodes and the
midpoints of its 6 cords). It is the c-tile when the sheet is c and the h-tile when it is h.</p>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Knitted HexOct: Patterns</title><link rel="stylesheet" href="../paper.css">
<style>{CSS}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Knitted HexOct: Patterns</h1>
<p class="sub">Two test pieces, T-c and T-h, and five stacking sequences: knitted sheets and knitted cords that stand in space as the HexOct structure</p>
<div class="meta"><b>DICTO</b> · dictospheres.com · 3 November 2026 · study 2026-11-03-knitted-hexoct-patterns · pattern, not published</div>
<div class="status"><b>Status.</b> Pattern, not published; no DOI. Not yet test-knitted. Built from the Knitted HexOct specification (study
2026-11-02-knitted-hexoct) and the stacking sequences of #83; every number, chart, table and figure is generated by scripts/patterns.py and checked
there (nodes, cords, node positions, cord geometry, cells against the #75 tiles, sequence words against #83). The yarn amounts for the stacks are estimates.
The mechanics of the stackings are model results of #83 part 2, not measurements.</div>
<p>DICTO proposed the Knitted HexOct: a multi-layer knitted fabric whose sheets are close-packed layers and whose links join each node
to the 3 nodes of the next sheet that its ball touches, so that c and h are carried by the links. These patterns make the two smallest
pieces that show c against h, and then any stacking sequence. Each piece is the structure itself in three dimensions: the sheets are layers A, B, C (or A, B, A′),
the knitted cords (links) are the bonds between them, and the cells closed off by sheets and cords are tetrahedra and octahedra, the pieces of
the HexOct c-tile or h-tile. There is no colourwork: the chart only tells you where the node stitches are.</p>
<h2>Contents</h2><ol>{contents}</ol>
<h2>Materials (both pieces)</h2><ul>
<li>Yarn: DK-weight mercerised cotton, firm and low-stretch, about 210 m per piece: 3 balls of 50 g (about 100 m) per piece, 5 balls for both.</li>
<li>Needles: 3.5 mm pair (sheets); 3.0 mm double-pointed needles (DPNs), two (cords).</li>
<li>Contrast thread for the node marks: 27 lengths of 15 cm per piece.</li>
<li>42 safety pins with paper tags per piece; tapestry needle; ruler; card for the cord strip and the angle template.</li>
<li>To hold the shape: three flat rigid frames per piece (opening about 32 × 22 cm) and four posts per gap (length <i>d</i>, about {d_cm:.1f} cm, cut to the measured spacing); or, as alternatives (spec §4), spacer blocks between the sheets, stuffing in the cells, or stiffened cords (starch, glue, or a non-stretch core cord inside each i-cord, about {CORE_M:.1f} m per piece).</li></ul>
<h2>Gauge</h2>
<p>Knit a garter-stitch swatch of 30 sts × 40 ridges on 3.5 mm needles (one ridge = 2 rows). Lay it flat without stretching and measure
<b>S</b> = stitches per 10 cm and <b>R</b> = ridges per 10 cm.</p>
<ul><li><b>N</b>, the node spacing in stitches: {N} (must be even, so that every second node row can shift by half a spacing). Then
<i>a</i> = 10&nbsp;N/S cm.</li>
<li><b>M</b>, the node-row spacing in ridges: the whole number nearest 0.866 × N × R/S. With a square garter gauge (R = S), M = {M}: the
node rows come out 14/16 = 0.875&nbsp;<i>a</i> apart instead of 0.866&nbsp;<i>a</i>, +1.0 %.</li>
<li>Sheet: cast on 4N sts, work 3M ridges. Node rows: the RS row of ridges ⌈M/2⌉, ⌈M/2⌉ + M, ⌈M/2⌉ + 2M. Node stitch (i, j), i = 0, 1, 2 along the
row, j = 0, 1, 2 the node row: stitch N/2 + 1 + N&nbsp;i + (N/2)&nbsp;j.</li></ul>
<div class="two"><div>{gauge_table()}<p class="small">For a more exact triangle, larger N: N = 30, M = 26 gives the row spacing to 0.07 %, but <i>a</i> ≈ 14 cm (spec §4).</p></div>
<div><p class="small">The patterns below are written for <b>N = {N}, M = {M}</b> (cast on {COLS}, {RIDGES} ridges, node rows {node_row(0)}, {node_row(1)},
{node_row(2)}). Sizes are given at the reference gauge {S_REF} sts and {R_REF} ridges per 10 cm: <i>a</i> = {a_cm:.2f} cm,
<i>d</i> = {d_cm:.2f} cm. With your own S, scale every size by {S_REF}/S. If your M differs, recompute the node rows from the formula;
the node stitches depend on N only.</p></div></div>
<h2>Abbreviations</h2>
<table class="abbr" style="width:auto">
<tr><td>K, Kn</td><td>knit; knit n stitches</td></tr>
<tr><td>NK [X]</td><td>node knit: knit the next stitch with the yarn and a 15 cm contrast thread held together; leave both thread ends hanging. This stitch is node X.</td></tr>
<tr><td>RS, WS</td><td>right side, wrong side (mark the RS: garter looks the same on both)</td></tr>
<tr><td>st(s); r</td><td>stitch(es); ridge (2 rows of garter)</td></tr>
<tr><td>DPN</td><td>double-pointed needle</td></tr>
<tr><td>i-cord</td><td>3 sts on a DPN: knit 3, slide the sts to the other end, pull the yarn across the back, repeat</td></tr>
<tr><td><i>a</i>, <i>d</i>, ℓ, <i>t</i></td><td>node spacing; sheet spacing √(2/3)&nbsp;<i>a</i>; free cord length <i>a</i> − 1.22&nbsp;<i>t</i>; sheet thickness</td></tr>
<tr><td>A1…A9, B1…B9, C1…C9, A′1…A′9</td><td>nodes: sheet letter, then 1 + i + 3j (node row 1: 1–3, row 2: 4–6, row 3: 7–9)</td></tr>
<tr><td>gap 1, gap 2</td><td>the space between sheets 1 and 2, and between sheets 2 and 3</td></tr></table>

<h1 class="brk">The sheet</h1>
<p>Every sheet in this booklet is knitted the same way: garter stitch, {COLS} sts and {ROWS} rows ({RIDGES} ridges), with 9 node stitches on rows
{node_row(0)}, {node_row(1)} and {node_row(2)}. Do not stretch or block the sheets. Where a sheet lies in a finished piece is not knitted in: the cords set it.</p>
<h2>The node stitch (NK)</h2>
<ol>
<li>Knit to the node stitch. Lay the 15 cm contrast thread beside the yarn.</li>
<li>Insert the right needle knitwise into the node stitch and take the yarn and the thread together.</li>
<li>Wrap both round the needle and pull them through as one new stitch; slip the old stitch off. Leave the thread ends hanging, about 7 cm each.</li>
<li>On the next row, knit the yarn and the thread of that stitch together as one stitch.</li></ol>
{fig('nk.svg', 'The node stitch NK, step by step: 1–3 on the needles, 4 the finished node in the garter fabric (RS). Violet: the contrast thread.', '78%')}
<h2>Row by row</h2>
<div class="sheet"><div>{sheet_rows()}</div><div>{node_table()}<p class="small">NK [5] makes node 5 of the sheet; on sheet B it is node B5.</p></div></div>
{fig('chart.svg', f'Chart of the sheet: {COLS} sts × {RIDGES} ridges ({ROWS} rows), RS view, cast-on edge at the bottom, one square = 1 stitch × 1 ridge. '
     f'Black squares: the node stitches 1–9 (worked NK) on rows {node_row(0)}, {node_row(1)} and {node_row(2)}.', '100%')}
<h2>The marked node</h2>
<p>Each node stitch carries its contrast thread. Leave the ends hanging until the cords are on: they show you the node and its two neighbours in the ridge,
the 3 stitches that a cord is picked up from (on a lower sheet) or sewn to (on an upper sheet). After binding off, check: 9 node stitches, each with its thread.</p>
{fig('mark.svg', 'A marked node on the RS. Purple: the node stitch; gold: its two neighbours in the same ridge.', '86%')}
<p><b>Knit three sheets for T-c (label A, B, C) and three for T-h (label A, B, A′); all six are the same.</b> For a stacking sequence, knit as many sheets as it
has and label them with their numbers and letters.</p>
{shared}
{pattern("T-c")}
{pattern("T-h")}
<h1 class="brk">c against h</h1>
<p>T-c and T-h differ only in the second gap: in T-c it is a forward step, as the first; in T-h it is a backward step. Seen from the side, the cords of T-c run on
through B in one straight line; those of T-h fold back at B like a chevron, and A′ comes to lie over A. Seen from above at a node of B, the three cords up
from B in T-c point opposite to the three cords coming down; in T-h they lie over them.</p>
{fig('ch.svg', 'c against h at sheet B. Top: section seen along a row of nodes (from the side edge), sheets as horizontal lines. Bottom: plan at one node of sheet B, as seen from above on the RS. '
     'Left, T-c (c): the cords up from B go on in the same direction as the cords coming in from A (forward step A→B→C): a pair of cords followed through B is one straight line. '
     'Right, T-h (h): the cords up from B go back the way the cords from A came (forward step A→B, then backward step B→A′): a pair of cords followed through B folds back like a chevron, and A′ lies over A.', '94%')}
{seq_part()}
</body></html>'''
open(os.path.join(OUT, 'paper.html'), 'w').write(html)
print('written', OUT)
