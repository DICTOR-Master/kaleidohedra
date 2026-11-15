"""Classify dumped rigid polygons: crossing set P (up to translation), the root-side and far-side pairings, arc lengths and depth."""
import sys
from collections import Counter
fn, kf = sys.argv[1], int(sys.argv[2])
def parse(line):
    f = line.split(); tag, l = f[1], int(f[2]); v = [tuple(map(int, f[3 + 4 * i:7 + 4 * i])) for i in range(l)]; return tag, l, v
def upper(v): k, x, y, u = v; return k > kf or (k == kf and u == 1)
def analyse(v):
    l = len(v); rootup = upper(v[0])
    cr = [i for i in range(l) if v[i][0] == kf and v[(i + 1) % l][0] == kf]
    P = [(v[i][1], v[i][2]) for i in cr]
    # arcs between consecutive crossings
    arcs = []
    for a in range(len(cr)):
        i, j = cr[a], cr[(a + 1) % len(cr)]
        seg = [v[(t) % l] for t in range(i + 1, (j if j > i else j + l) + 1)]
        side = 'F' if upper(seg[0]) != rootup else 'R'
        depth = max(abs(s[0] - kf) for s in seg)
        arcs.append((side, a, (a + 1) % len(cr), len(seg) - 1, depth))
    x0, y0 = min(P)
    Pn = tuple(sorted((x - x0, y - y0) for x, y in P))
    return len(cr), Pn, arcs
for want in ('G', 'H'):
    c = Counter()
    for line in open(fn):
        if not line.startswith('D ' + want): continue
        tag, l, v = parse(line)
        if l > int(sys.argv[3]): continue
        n, Pn, arcs = analyse(v)
        key = (l, n, Pn, tuple(sorted((s, ln, d) for s, a, b, ln, d in arcs)))
        c[key] += 1
    print(want, len(c), sum(c.values()))
    for k, val in sorted(c.items()): print(' ', want, k, val)
