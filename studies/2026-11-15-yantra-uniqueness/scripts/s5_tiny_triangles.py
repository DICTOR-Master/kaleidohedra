"""Step 5 (DICTO, 15 Nov 2026: "yes measure them"): certified sizes of the two tiny extra triangles of Kulaichev's yantra, the white
sliver beside each, the four-sided regions A and B (and mirrors) they create, and the overshoot of t4's right leg past t5's corner.

Method. The Theorem 10 solution is rebuilt exactly as s3_backsolve.py does: the root of f348 in Theorem 10's dyadic interval
(data/roots-K.json) -> the real t-root of A(t, u) in (0, u) at which B vanishes -> S from G in (R, 1) -> the Krawczyk box of radius
1e-300 in (u, t, S) (one solution certified) -> the whole yantra in Arb balls (construct(), same lines as s3).
The combinatorics of the arrangement (which regions exist and which two of the 27 lines meet at each corner) is read from a
double-precision copy of the arrangement (the face walk of studies/2026-11-08-sri-yantra/scripts/figure.py, copied below); it is
the arrangement certified in #103 Proposition 11 (certified_counts.py: 45 odd regions, 41 triangles). Every corner is then recomputed
in Arb as the meeting point of its two lines, and every length and area below is a ball (certified bounds).
Checks: 45 odd regions (14, 10, 12, 8, 1), 41 triangles; the two smallest regions are the mirror pair in ring 3; the odd regions
and the even ones together fill the union of the nine triangles (sum of all bounded region areas = the union's area integrated slab by slab
from the triangles' cross-sections, in floats); the signed
distance of t5's corner from t4's right leg is certified negative (crossed over); every corner ball has radius < 1e-200.
Writes data/tiny-triangles.json.  FINAL ok iff every check holds."""
import json, os, sys, math, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = lambda *p: os.path.join(ROOT, *p)
import flint
from flint import arb, acb, fmpq, arb_mat
flint.ctx.prec = 2400
polys = json.load(open(D('data', 'polys-K.json'))); census = json.load(open(D('data', 'roots-K.json')))
P_ = {k: [(tuple(e), int(c)) for e, c in polys[k]] for k in ('G', 'H1', 'D', 'A', 'B')}
QUICK = '--pilot' in sys.argv
# ---------------- from s3_backsolve.py (unchanged) ----------------
def deriv(p, var): return [(tuple(e[i] - (i == var) for i in range(3)), c * e[var]) for e, c in p if e[var] > 0]
def ev(p, x):
    pw = [{}, {}, {}]
    def pk(i, k):
        if k not in pw[i]: pw[i][k] = x[i] ** k
        return pw[i][k]
    tot = 0
    for e, c in p: tot += c * pk(0, e[0]) * pk(1, e[1]) * pk(2, e[2])
    return tot
def coeffs_in(p, var, x):
    deg = max(e[var] for e, c in p); out = [0] * (deg + 1)
    for e, c in p:
        term = c
        for i in range(3):
            if i != var and e[i]: term = term * x[i] ** e[i]
        out[e[var]] += term
    return [arb(0) + c if not isinstance(c, arb) else c for c in out]
def ball(k, a, b):
    lo, hi = fmpq(int(a), 1 << k), fmpq(int(b), 1 << k); return arb((lo + hi) / 2, (hi - lo) / 2)
def real_roots_in(coeffs, lo, hi):
    while abs(coeffs[-1]).upper() == 0 and len(coeffs) > 1: coeffs = coeffs[:-1]
    assert not coeffs[-1].contains(0)
    rts = flint.acb_poly([acb(c) for c in coeffs]).roots(tol=arb(2) ** (-(flint.ctx.prec // 3)), maxprec=4 * flint.ctx.prec)
    n = len(rts); out = []
    for i, r in enumerate(rts):
        if not r.imag.contains(0): continue
        cj = acb(r.real, -r.imag); assert not any(j != i and cj.overlaps(rts[j]) for j in range(n))
        x = r.real
        if (x < lo) or (x > hi): continue
        assert (x > lo) and (x < hi); out.append(x)
    return out
def construct(u, t, S):
    v = u; one = arb(1)
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: arb(0)}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return b, w, a
def krawczyk(x0, rad):
    F = [P_['G'], P_['H1'], P_['D']]; J = [[deriv(f, j) for j in range(3)] for f in F]
    X = [arb(c.mid(), rad) for c in x0]; y = [arb(c.mid()) for c in x0]
    Fy = [ev(f, y) for f in F]
    Jy = arb_mat([[ev(J[i][j], y) for j in range(3)] for i in range(3)]).mid(); Y = Jy.inv().mid()
    JX = arb_mat([[ev(J[i][j], X) for j in range(3)] for i in range(3)])
    M = arb_mat([[1 if i == j else 0 for j in range(3)] for i in range(3)]) - Y * JX
    d = arb_mat([[X[i] - y[i]] for i in range(3)]); fy = arb_mat([[Fy[i]] for i in range(3)])
    K = arb_mat([[y[i]] for i in range(3)]) - Y * fy + M * d
    return all(X[i].contains_interior(K[i, 0]) for i in range(3)), [K[i, 0] for i in range(3)]
# ---------------- the arrangement (face walk copied from studies/2026-11-08-sri-yantra/scripts/figure.py) ----------------
def segments(b, w, a):
    segs = []
    for i in range(1, 10):
        L, Rr, A = (-w[i], b[i]), (w[i], b[i]), (0.0, a[i]); segs += [(L, Rr, i), (L, A, i), (Rr, A, i)]
    return segs
def inter(s, t):
    (x1, y1), (x2, y2) = s[0], s[1]; (x3, y3), (x4, y4) = t[0], t[1]
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-15: return None
    p = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d; q = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d; e = 1e-12
    if -e <= p <= 1 + e and -e <= q <= 1 + e: return (x1 + p * (x2 - x1), y1 + p * (y2 - y1)), p
    return None
def faces(segs):
    pts = []
    def pid(p):
        for k, q in enumerate(pts):
            if abs(p[0] - q[0]) < 1e-9 and abs(p[1] - q[1]) < 1e-9: return k
        pts.append(p); return len(pts) - 1
    edges = set()
    for i, s in enumerate(segs):
        cuts = [(0.0, s[0]), (1.0, s[1])]
        for j, t in enumerate(segs):
            if i != j:
                r = inter(s, t)
                if r: cuts.append((r[1], r[0]))
        cuts.sort(); ids = []
        for _, p in cuts:
            k = pid(p)
            if not ids or ids[-1] != k: ids.append(k)
        for k in range(len(ids) - 1):
            if ids[k] != ids[k + 1]: edges.add((ids[k], ids[k + 1])); edges.add((ids[k + 1], ids[k]))
    out = {}
    for (p, q) in edges: out.setdefault(p, []).append(q)
    for p in out: out[p].sort(key=lambda q: math.atan2(pts[q][1] - pts[p][1], pts[q][0] - pts[p][0]))
    used, fs = set(), []
    for e in edges:
        if e in used: continue
        f = []; cur = e
        while cur not in used:
            used.add(cur); f.append(cur[0]); p, q = cur; nb = out[q]; k = nb.index(p); cur = (q, nb[(k - 1) % len(nb)])
        fs.append(f)
    return pts, fs
def farea(poly): return 0.5 * sum(poly[i][0] * poly[i - 1][1] - poly[i - 1][0] * poly[i][1] for i in range(len(poly)))
def corners_of(poly):
    keep = []; n = len(poly)
    for i in range(n):
        p, q, r = poly[i - 1], poly[i], poly[(i + 1) % n]
        if abs((q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])) > 1e-12: keep.append(q)
    return keep
def inside_tri(c, b, w, a, i):
    x, y = c
    if (y - b[i]) * (a[i] - b[i]) < 0: return False
    return abs(x) <= w[i] * (y - a[i]) / (b[i] - a[i])
# ---------------- 1. the certified yantra ----------------
c348 = [c for c in census if c['is_f348']][0]; k, a_, b_ = c348['roots01'][c348['theorem10_root_index']]; U = ball(k, a_, b_)
ts = real_roots_in(coeffs_in(P_['A'], 1, (U, None, None)), arb(0), U)
tau = [t for t in ts if ev(P_['B'], (U, t, arb(0))).contains(0)]; assert len(tau) == 1, tau; tau = tau[0]
Ss = real_roots_in(coeffs_in(P_['G'], 2, (U, None, None)), arb(1) / (1 + U**2), arb(1))
Sv = [s for s in Ss if ev(P_['H1'], (U, tau, s)).contains(0) and ev(P_['D'], (U, tau, s)).contains(0)]; assert len(Sv) == 1; Sv = Sv[0]
ins, K = krawczyk((U, tau, Sv), arb(10) ** -300); ok = bool(ins)
say('Krawczyk box (radius 1e-300) holds exactly one solution:', ins, ' u =', K[0].str(25, radius=False))
b, w, a = construct(*K)
print('PROGRESS 0.25 certified yantra rebuilt')
# the 27 lines, each as two points (Arb) and the same in floats
LINES = {}
for i in range(1, 10):
    LINES[f't{i} base'] = ((-w[i], b[i]), (w[i], b[i]))
    LINES[f't{i} left leg'] = ((-w[i], b[i]), (arb(0), a[i]))
    LINES[f't{i} right leg'] = ((w[i], b[i]), (arb(0), a[i]))
fl = lambda z: float(z.mid())
FL = {n: ((fl(p[0]), fl(p[1])), (fl(q[0]), fl(q[1]))) for n, (p, q) in LINES.items()}
def meet(L1, L2):                                        # Arb intersection of two lines given by two points each
    (x1, y1), (x2, y2) = L1; (x3, y3), (x4, y4) = L2
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3); assert not d.contains(0)
    s = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    return (x1 + s * (x2 - x1), y1 + s * (y2 - y1))
def fdist(pt, L):
    (x1, y1), (x2, y2) = L; return abs((x2 - x1) * (pt[1] - y1) - (y2 - y1) * (pt[0] - x1)) / math.hypot(x2 - x1, y2 - y1)
def lines_through(pt):
    return [n for n, L in FL.items() if fdist(pt, L) < 1e-10]
def acorner(pt):
    ns = lines_through(pt); assert len(ns) >= 2, (pt, ns)
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            (x1, y1), (x2, y2) = FL[ns[i]]; (x3, y3), (x4, y4) = FL[ns[j]]
            if abs((x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)) > 1e-9:
                P = meet(LINES[ns[i]], LINES[ns[j]]); return P, ns
    raise AssertionError('no non-parallel pair')
def aarea(poly):
    s = arb(0)
    for i in range(len(poly)): s += poly[i][0] * poly[i - 1][1] - poly[i - 1][0] * poly[i][1]
    return abs(s) / 2
def alen(p, q): return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2).sqrt()
# ---------------- 2. the arrangement and its regions ----------------
bf = {i: fl(b[i]) for i in b}; wf = {i: fl(w[i]) for i in w}; af = {i: fl(a[i]) for i in a}
pts, fs = faces(segments(bf, wf, af)); regions = []; total = 0.0
for f in fs:
    poly = [pts[i] for i in f]; ar = farea(poly)
    if ar >= -1e-14: continue                          # the outer face has the other orientation
    total += -ar
    cx = sum(x for x, _ in poly) / len(poly); cy = sum(y for _, y in poly) / len(poly)
    cnt = sum(inside_tri((cx, cy), bf, wf, af, i) for i in range(1, 10)); c = corners_of(poly)
    regions.append(dict(corners=c, cnt=cnt, odd=cnt % 2 == 1, area_f=-ar, centre=(cx, cy)))
odd = [r for r in regions if r['odd']]; rings = [sum(1 for r in odd if r['cnt'] == c) for c in (1, 3, 5, 7, 9)]
ntri = sum(1 for r in odd if len(r['corners']) == 3)
say('odd regions:', len(odd), 'rings', rings, 'triangles', ntri, '; bounded regions', len(regions))
ok &= len(odd) == 45 and rings == [14, 10, 12, 8, 1] and ntri == 41
# union of the nine triangles, slab by slab in floats (independent of the face walk): must equal the sum of all region areas
def width_at(y):                                       # union of the nine triangles' cross-sections at depth y
    ivs = []
    for i in range(1, 10):
        if (y - bf[i]) * (af[i] - bf[i]) < 0 or (y - af[i]) * (bf[i] - af[i]) < 0: continue
        h = wf[i] * (y - af[i]) / (bf[i] - af[i]); ivs.append((-h, h))
    ivs.sort(); cur = None; s = 0.0
    for lo, hi in ivs:
        if cur is None or lo > cur[1]:
            if cur: s += cur[1] - cur[0]
            cur = [lo, hi]
        else: cur[1] = max(cur[1], hi)
    return s + (cur[1] - cur[0] if cur else 0.0)
def union_area():                                      # the width is linear between consecutive vertex depths: midpoint rule is exact
    ys = sorted(set([round(p[1], 13) for p in pts] + [bf[i] for i in bf] + [af[i] for i in af]))
    return sum((y1 - y0) * width_at((y0 + y1) / 2) for y0, y1 in zip(ys, ys[1:]) if y1 - y0 > 1e-13)
ua = union_area()
cov = sum(r['area_f'] for r in regions if r['cnt'] > 0); gaps = [r['area_f'] for r in regions if r['cnt'] == 0]
say(f'sum of bounded region areas {total:.9f} (inside some triangle {cov:.9f}; enclosed gaps in no triangle: {len(gaps)}, area {sum(gaps):.3g}); union of the nine triangles by slabs {ua:.9f}')
ok &= abs(ua - cov) < 1e-9
print('PROGRESS 0.5 arrangement read')
# ---------------- 3. certified measurements ----------------
def cert(region):
    cs = [acorner(p) for p in region['corners']]; poly = [c[0] for c in cs]
    sides = [alen(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    A = aarea(poly); per = sum(sides, arb(0))
    return dict(poly=poly, lines=[c[1] for c in cs], area=A, sides=sides, inradius=2 * A / per if len(poly) == 3 else None)
for r in odd: r['cert'] = cert(r)
odd.sort(key=lambda r: float(r['cert']['area'].mid()))
tiny = odd[:2]; ok &= all(r['cnt'] == 5 and len(r['corners']) == 3 for r in tiny) and tiny[0]['centre'][0] * tiny[1]['centre'][0] < 0
ok &= tiny[1]['cert']['area'] < odd[2]['cert']['area']      # certified: the two tiny ones are strictly the smallest
proper = [r for r in odd[2:] if len(r['corners']) == 3]; smallest = proper[0]
four = [r for r in odd if len(r['corners']) == 4]; ok &= len(four) == 4
# the white sliver: the even region with corners p, q, c (right half)
C5 = (w[5], b[5]); C5f = (fl(w[5]), fl(b[5]))
ev_small = sorted([r for r in regions if not r['odd'] and len(r['corners']) == 3 and r['centre'][0] > 0
                   and min(math.dist(v, C5f) for v in r['corners']) < 1e-9], key=lambda r: r['area_f'])
sliver = cert(ev_small[0]); ok &= float(sliver['area'].mid()) < 1e-6
# the overshoot: signed distance of t5's corner c from t4's right leg (negative = crossed over), and the points p, q, r
(x1, y1), (x2, y2) = LINES['t4 right leg']
sd = ((x2 - x1) * (C5[1] - y1) - (y2 - y1) * (C5[0] - x1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2).sqrt()
ok &= bool(sd < 0); say('signed distance of t5\'s corner from t4\'s right leg (diameter 1):', sd.str(8))
p = meet(LINES['t4 right leg'], LINES['t5 base']); q = meet(LINES['t4 right leg'], LINES['t5 right leg']); rr = meet(LINES['t4 right leg'], LINES['t6 right leg'])
cp = alen(C5, p)
# reference areas
GT = w[3] * (1 - b[3]); GT7 = w[7] * b[7]; ok &= bool(abs(GT - GT7) < arb(10) ** -200)     # condition (a): equal great triangles
CIRC = arb.pi() / 4
radius = arb(1) / 2
def fmt(x, sig=4):
    if x.contains(0): return f'|x| <= {float(abs(x).upper().mid()):.2g}'
    lo, hi = float(x.lower().mid()), float(x.upper().mid())
    e = math.floor(math.log10(abs((lo + hi) / 2))); s = 10 ** (e - sig + 1)
    return f'[{math.floor(lo / s) * s:.{sig}g}, {math.ceil(hi / s) * s:.{sig}g}]'
maxrad = max((z.rad() for r in odd for P in r['cert']['poly'] for z in P), key=lambda q: float(q.log().mid()) if q > 0 else -1e9); ok &= bool(maxrad < arb(10) ** -200); maxrad = maxrad.str(3)
say('largest corner ball radius:', maxrad)
print('PROGRESS 0.75 measured')
out = {}
def rec(name, x, unit):
    out[name] = dict(value=fmt(x), mid=float(x.mid()), rad=float(x.rad()), unit=unit); say(f'{name:62s} {fmt(x):>26s}  {unit}')
T = tiny[0] if tiny[0]['centre'][0] > 0 else tiny[1]
rec('tiny triangle area / great triangle area', T['cert']['area'] / GT, 'ratio')
rec('tiny triangle area / circle area', T['cert']['area'] / CIRC, 'ratio')
rec('tiny triangle area / smallest proper triangle area', T['cert']['area'] / smallest['cert']['area'], 'ratio')
rec('tiny triangle area (diameter 1)', T['cert']['area'], 'D^2')
rec('tiny triangle area / radius^2', T['cert']['area'] / radius ** 2, 'r^2')
for i, s in enumerate(sorted(T['cert']['sides'], key=lambda z: float(z.mid()))): rec(f'tiny triangle side {i + 1} / radius', s / radius, 'r')
rec('tiny triangle inradius / radius', T['cert']['inradius'] / radius, 'r')
rec('mirror tiny triangle area minus this one (|diff|)', abs((tiny[0]['cert']['area'] - tiny[1]['cert']['area'])), 'D^2')
rec('white sliver (p, q, c) area / radius^2', sliver['area'] / radius ** 2, 'r^2')
for i, s in enumerate(sorted(sliver['sides'], key=lambda z: float(z.mid()))): rec(f'white sliver side {i + 1} / radius', s / radius, 'r')
rec('white sliver inradius / radius', sliver['inradius'] / radius, 'r')
for r in sorted([r for r in four if r['centre'][0] > 0], key=lambda r: -r['cnt']):
    nm = 'A' if r['cnt'] == 5 else 'B'
    rec(f'four-sided {nm} (ring {(r["cnt"] + 1) // 2}) area / great triangle area', r['cert']['area'] / GT, 'ratio')
    rec(f'four-sided {nm} area / smallest proper triangle area', r['cert']['area'] / smallest['cert']['area'], 'ratio')
    sd_ = sorted(r['cert']['sides'], key=lambda z: float(z.mid()))
    rec(f'four-sided {nm} shortest side / radius', sd_[0] / radius, 'r')
    rec(f'four-sided {nm} longest side / radius', sd_[-1] / radius, 'r')
rec('smallest proper triangle area / great triangle area', smallest['cert']['area'] / GT, 'ratio')
rec('smallest proper triangle area / radius^2', smallest['cert']['area'] / radius ** 2, 'r^2')
rec('great triangle area / radius^2', GT / radius ** 2, 'r^2')
rec('overshoot: signed distance of t5 corner from t4 right leg / radius', sd / radius, 'r')
rec('overshoot along t5 base, |c - p| / radius', cp / radius, 'r')
rec('|c - q| / radius (A short side)', alen(C5, q) / radius, 'r')
rec('|p - q| / radius (B short side)', alen(p, q) / radius, 'r')
rec('|c - r| / radius', alen(C5, rr) / radius, 'r')
say('smallest proper triangle: ring', (smallest['cnt'] + 1) // 2, 'centre', tuple(round(z, 5) for z in smallest['centre']), 'lines', smallest['cert']['lines'])
say('tiny triangle lines at its corners:', T['cert']['lines'])
# drawing scale: radius 10 cm and 1 m; pen line 0.1 mm
scale = {}
for Rm, lab in ((arb('0.1'), '10 cm'), (arb(1), '1 m')):
    um = Rm * 10 ** 6   # micrometres per radius
    d = dict(
        tiny_sides_um=[fmt(s / radius * um, 3) for s in sorted(T['cert']['sides'], key=lambda z: float(z.mid()))],
        tiny_inradius_um=fmt(T['cert']['inradius'] / radius * um, 3),
        tiny_area_um2=fmt(T['cert']['area'] / radius ** 2 * um ** 2, 3),
        overshoot_um=fmt(abs(sd) / radius * um, 3), along_base_um=fmt(cp / radius * um, 3),
        sliver_inradius_um=fmt(sliver['inradius'] / radius * um, 3),
        A_short_um=fmt(alen(C5, q) / radius * um, 3), B_short_um=fmt(alen(p, q) / radius * um, 3),
        smallest_proper_inradius_um=fmt(smallest['cert']['inradius'] / radius * um, 3))
    scale[lab] = d; say('radius', lab, ':', d)
out['drawing_scale'] = scale; out['checks'] = dict(odd=len(odd), rings=rings, triangles=ntri, four_sided=len(four), krawczyk=bool(ins), maxrad=maxrad)
out['smallest_proper'] = dict(ring=(smallest['cnt'] + 1) // 2, centre=smallest['centre'], lines=smallest['cert']['lines'])
out['tiny_lines'] = T['cert']['lines']
json.dump(out, open(D('data', 'tiny-triangles-pilot.json' if QUICK else 'tiny-triangles.json'), 'w'), indent=1, default=str)
print('PROGRESS 1.000 done')
print('FINAL ok' if ok else 'FINAL FAIL: see above')
