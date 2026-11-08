"""Figure of an exact yantra: the nine triangles in the circle, the faces of the line arrangement
(counted and checked: exactly 43 triangles), the 18 marmas (filled dots) and the 6 corner touches
(rings).  Drawing coordinates are floats taken from the exact values; the counting step merges
points closer than 1e-9 (the exact concurrencies make the triple points coincide).
usage: python3 figure.py <examples.json> <name> <out.svg> <title>
The 43 triangles are exactly the faces that lie inside an ODD number of the nine triangles (checked)."""
import json, math, sys
from fractions import Fraction as Fr
from model import MARMAS, CORNERS


def val(z):
    a = Fr(z['a']); b = Fr(z.get('b', '0'))
    return float(a) + (float(b) * math.sqrt(float(Fr(z['sqrt_of']))) if b != 0 else 0.0)


def load(path, name):
    e = json.load(open(path))[name]
    b = {int(k): val(x) for k, x in e['b'].items()}; w = {int(k): val(x) for k, x in e['w'].items()}
    a = {int(k): val(x) for k, x in e['apex'].items()}
    return e, b, w, a


def segments(b, w, a):
    segs = []
    for i in range(1, 10):
        L, Rr, A = (-w[i], b[i]), (w[i], b[i]), (0.0, a[i])
        segs += [(L, Rr, i), (L, A, i), (Rr, A, i)]
    return segs


def inter(s, t):
    (x1, y1), (x2, y2) = s[0], s[1]; (x3, y3), (x4, y4) = t[0], t[1]
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-15: return None
    p = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    q = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    e = 1e-12
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
        cuts.sort()
        ids = []
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
            used.add(cur); f.append(cur[0]); p, q = cur
            nb = out[q]; k = nb.index(p)
            cur = (q, nb[(k - 1) % len(nb)])
        fs.append(f)
    return pts, fs


def area(poly):
    return 0.5 * sum(poly[i][0] * poly[i - 1][1] - poly[i - 1][0] * poly[i][1] for i in range(len(poly)))


def corners_of(poly):
    """drop collinear vertices"""
    keep = []
    n = len(poly)
    for i in range(n):
        p, q, r = poly[i - 1], poly[i], poly[(i + 1) % n]
        if abs((q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])) > 1e-12: keep.append(q)
    return keep


def inside_tri(c, b, w, a, i):
    x, y = c
    if (y - b[i]) * (a[i] - b[i]) < 0: return False
    half = w[i] * (y - a[i]) / (b[i] - a[i])
    return abs(x) <= half


def main(path, name, out_svg, title):
    e, b, w, a = load(path, name)
    segs = segments(b, w, a)
    pts, fs = faces(segs)
    odd, even = [], []
    for f in fs:
        poly = [pts[k] for k in f]
        ar = area(poly)
        if ar >= -1e-14: continue           # outer boundary (positive orientation) or degenerate
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        cnt = sum(inside_tri((cx, cy), b, w, a, i) for i in range(1, 10))
        (odd if cnt % 2 else even).append((corners_of(poly), cnt))
    rings = {c: sum(1 for p, k in odd if k == c) for c in (1, 3, 5, 7, 9)}
    n_tri = sum(1 for p, k in odd if len(p) == 3)
    print(f'{name}: {len(odd) + len(even)} faces; {len(odd)} lie in an odd number of the nine triangles, '
          f'{n_tri} of these are triangles; by depth 1,3,5,7,9: {[rings[c] for c in (1, 3, 5, 7, 9)]}')
    S_ = 1000; M = 60
    X = lambda x: M + (x + 0.5) * S_; Y = lambda d: M + d * S_
    W = S_ + 2 * M
    ring_col = {1: '#e9b44c', 3: '#d1495b', 5: '#7d3c98', 7: '#1f6f8b', 9: '#0b132b'}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W + 70}" width="{W}" height="{W + 70}">',
         '<rect width="100%" height="100%" fill="#fffdf7"/>']
    for poly, cnt in odd:
        o.append('<polygon points="' + ' '.join(f'{X(x):.3f},{Y(y):.3f}' for x, y in poly) + f'" fill="{ring_col[cnt]}" fill-opacity="0.85" stroke="none"/>')
    # DICTO's rhombus: t7 legs from O and t3 legs from T, extended to meet at E (dashed)
    u = w[7] / b[7]; v = w[3] / (1 - b[3]); ex, ed = u * v / (u + v), v / (u + v)
    def dashed(p, q, on=0.022, off=0.012):
        L = math.hypot(q[0] - p[0], q[1] - p[1]); s0 = 0.0
        while s0 < L:
            s1 = min(s0 + on, L)
            x0, y0 = p[0] + (q[0] - p[0]) * s0 / L, p[1] + (q[1] - p[1]) * s0 / L
            x1, y1 = p[0] + (q[0] - p[0]) * s1 / L, p[1] + (q[1] - p[1]) * s1 / L
            o.append(f'<line x1="{X(x0):.2f}" y1="{Y(y0):.2f}" x2="{X(x1):.2f}" y2="{Y(y1):.2f}" stroke="#2a9d8f" stroke-width="6" stroke-opacity="0.8"/>')
            s0 = s1 + off
    for (p, q, i) in segs:
        o.append(f'<line x1="{X(p[0]):.3f}" y1="{Y(p[1]):.3f}" x2="{X(q[0]):.3f}" y2="{Y(q[1]):.3f}" stroke="#1a1a1a" stroke-width="1.6"/>')
    for p, q in (((0, 0), (ex, ed)), ((ex, ed), (0, 1)), ((0, 1), (-ex, ed)), ((-ex, ed), (0, 0))):
        dashed(p, q)
    n = 360   # circle as short line segments (some SVG renderers drop unfilled shapes)
    for k in range(n):
        t0, t1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        o.append(f'<line x1="{X(0.5 * math.cos(t0)):.2f}" y1="{Y(0.5 + 0.5 * math.sin(t0)):.2f}" '
                 f'x2="{X(0.5 * math.cos(t1)):.2f}" y2="{Y(0.5 + 0.5 * math.sin(t1)):.2f}" stroke="#333" stroke-width="2.4"/>')
    def lx(i, d): return w[i] * (d - a[i]) / (b[i] - a[i])
    for (p, q, r) in MARMAS:
        x = lx(p, b[q])
        for s in (1, -1): o.append(f'<circle cx="{X(s * x):.3f}" cy="{Y(b[q]):.3f}" r="6.5" fill="#c1121f" stroke="#fff" stroke-width="1.5"/>')
    for (p, q, r) in CORNERS:
        for s in (1, -1):
            cx, cy = X(s * w[q]), Y(b[q])
            o.append(f'<polygon points="{cx:.2f},{cy - 7:.2f} {cx + 7:.2f},{cy:.2f} {cx:.2f},{cy + 7:.2f} {cx - 7:.2f},{cy:.2f}" fill="#1d4ed8" stroke="#fff" stroke-width="1.2"/>')
    o.append(f'<text x="{M}" y="{W + 12}" font-family="Helvetica,Arial,sans-serif" font-size="18" fill="#222">{title}</text>')
    o.append(f'<text x="{M}" y="{W + 40}" font-family="Helvetica,Arial,sans-serif" font-size="17" fill="#333">'
             f'{len(odd)} odd faces ({", ".join(str(rings[c]) for c in (1, 3, 5, 7, 9))}) shaded by ring; red dots: the 18 marmas; blue diamonds: 6 corner touches; dashed: DICTO\'s rhombus (a kite unless u = v)</text>')
    o.append(f'<text x="{W - 14}" y="{W + 62}" text-anchor="end" font-family="Helvetica,Arial,sans-serif" font-size="16" fill="#555">DICTO · dictospheres.com</text>')
    o.append('</svg>')
    open(out_svg, 'w').write('\n'.join(o))
    return n_tri, len(odd), rings


if __name__ == '__main__':
    n_tri, n_odd, rings = main(*sys.argv[1:5])
    # optional 6th argument: the expected ring counts when a figure is KNOWN to differ (Kulaichev-type yantras
    # have two extra small faces in the third ring, as Pustynski 2014 remarked); default = the classical 43
    expect = [int(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 else [14, 10, 10, 8, 1]
    good = [rings[c] for c in (1, 3, 5, 7, 9)] == expect and (n_tri == n_odd == 43 if expect == [14, 10, 10, 8, 1] else True)
    print('FINAL ok' if good else f'FINAL FAIL odd faces {n_odd}, triangles {n_tri}, rings {rings} (expected 43 = 14+10+10+8+1)')
