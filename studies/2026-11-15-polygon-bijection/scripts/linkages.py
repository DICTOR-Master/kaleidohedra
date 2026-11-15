"""Factor the rigid-at-kf polygons into root-side and far-side linkages (study 2026-11-15-polygon-bijection).
A polygon crossing bilayer kf at the points P is its root-side arcs (pairing M of P) + its far-side arcs (pairing M').  Every
root-side linkage of (P, M, R bonds) combines with every far-side linkage of (P, M', F bonds) when M != M' (disjoint vertex sets),
so  #polygons(P, M, M', R, F) = r(P, M, R) * f(P, M', F).  The root side is the same in G and G2, so
    Delta(l) = rigid(G2) - rigid(G) = sum_{P, M, M', R + F = l - 4n/..} r(P, M, R) * (f2(P, M', F) - f(P, M', F)).
Usage: linkages.py DUMPFILE KF LMAX   (DUMPFILE from bij.py dump with DMIN low enough that all lengths <= LMAX are present)."""
import sys
from collections import defaultdict, Counter
fn, kf, LMAX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def upper(v): return v[0] > kf or (v[0] == kf and v[3] == 1)
def split(v):
    l = len(v); rootup = upper(v[0])
    cr = [i for i in range(l) if v[i][0] == kf and v[(i + 1) % l][0] == kf]
    P = frozenset((v[i][1], v[i][2]) for i in cr)
    root, far = [], []
    for a in range(len(cr)):
        i, j = cr[a], cr[(a + 1) % len(cr)]
        seg = tuple(v[t % l] for t in range(i + 1, (j if j > i else j + l) + 1))
        if seg[0][1:3] > seg[-1][1:3]: seg = seg[::-1]
        (far if upper(seg[0]) != rootup else root).append(seg)
    pair = lambda arcs: frozenset(frozenset((s[0][1:3], s[-1][1:3])) for s in arcs)
    return P, pair(root), pair(far), tuple(sorted(root)), tuple(sorted(far)), sum(len(s) - 1 for s in root), sum(len(s) - 1 for s in far), len(cr)
data = {}
for tag in ('G', 'H'):
    rl, fl, cyc = defaultdict(set), defaultdict(set), Counter()
    for line in open(fn):
        if not line.startswith('D ' + tag): continue
        f = line.split(); l = int(f[2])
        if l > LMAX: continue
        v = [tuple(map(int, f[3 + 4 * i:7 + 4 * i])) for i in range(l)]
        P, M, Mp, ra, fa, R, F, n = split(v)
        rl[(P, M, R)].add(ra); fl[(P, Mp, F)].add(fa); cyc[(P, M, Mp, R, F)] += 1
    prod_ok = all(c == len(rl[(P, M, R)]) * len(fl[(P, Mp, F)]) for (P, M, Mp, R, F), c in cyc.items())
    data[tag] = (rl, fl, cyc, prod_ok)
    print(f'{tag}: polygons {sum(cyc.values())}, keys {len(cyc)}, product structure holds: {prod_ok}')
rG, fG, cG, _ = data['G']; rH, fH, cH, _ = data['H']
root_same = all(len(rG[k]) == len(rH[k]) for k in set(rG) & set(rH))
print('root-side linkage counts equal in G and G2 where both occur:', root_same)
# Delta per length from the factorisation
keys = set(cG) | set(cH)
byl = Counter(); byl_direct = Counter()
for (P, M, Mp, R, F) in keys:
    r = max(len(rG.get((P, M, R), ())), len(rH.get((P, M, R), ())))
    d = len(fH.get((P, Mp, F), ())) - len(fG.get((P, Mp, F), ()))
    byl[R + F + len(P)] += r * d
for (k, c) in cG.items(): byl_direct[k[3] + k[4] + len(k[0])] -= c
for (k, c) in cH.items(): byl_direct[k[3] + k[4] + len(k[0])] += c
for l in sorted(byl_direct): print(f'l={l}: rigid(G2)-rigid(G) = {byl_direct[l]}, sum r*(f2-f) = {byl[l]}')
# far configurations whose linkage count differs between the two far sides
fk = set(fG) | set(fH)
diff = [(F, P, Mp, len(fG.get((P, Mp, F), ())), len(fH.get((P, Mp, F), ()))) for (P, Mp, F) in fk if len(fG.get((P, Mp, F), ())) != len(fH.get((P, Mp, F), ()))]
print('far configurations (P, M\', F) occurring:', len(fk), ' with f2 != f:', len(diff))
hist = Counter((F, len(P)) for F, P, *_ in diff); print('  by (F, n):', dict(sorted(hist.items())))
def shape(P):
    x0, y0 = min(P); return tuple(sorted((x - x0, y - y0) for x, y in P))
for F, P, Mp, a, b in sorted(diff, key=lambda t: (t[0], shape(t[1])))[:int(sys.argv[4]) if len(sys.argv) > 4 else 12]:
    x0, y0 = min(P)
    print(f'  F={F} P={shape(P)} M\'={sorted(tuple(sorted((x - x0, y - y0) for x, y in e)) for e in Mp)} f={a} f2={b}')
