"""Second surgery (B): twist the ROOT side by a toggle involution that fixes the root's in-plane point o, preserves P and the
root-side pairing.  Counts, among the rigid-at-kf polygons of a dump, those that are B-symmetric, per length, in G and G2."""
import sys
from collections import Counter
fn, kf = sys.argv[1], int(sys.argv[2])
def upper(v): return v[0] > kf or (v[0] == kf and v[3] == 1)
# the 12 point-group matrices (60-degree basis)
def mul(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
Rm = ((0, -1), (1, 1)); Sw = ((0, 1), (1, 0)); I = ((1, 0), (0, 1))
G12 = []; cur = I
for r in range(6): G12 += [cur, mul(Sw, cur)]; cur = mul(Rm, cur)
INV = [A for A in G12 if mul(A, A) == I and A != I]
def app(A, c, X): return (c[0] + A[0][0] * (X[0] - c[0]) + A[0][1] * (X[1] - c[1]), c[1] + A[1][0] * (X[0] - c[0]) + A[1][1] * (X[1] - c[1]))
res = Counter()
for line in open(fn):
    if not line.startswith('D '): continue
    f = line.split(); tag, l = f[1], int(f[2]); v = [tuple(map(int, f[3 + 4 * i:7 + 4 * i])) for i in range(l)]
    o = (v[0][1], v[0][2]); s = v[0][1] % 3; rootup = upper(v[0])
    cr = [i for i in range(l) if v[i][0] == kf and v[(i + 1) % l][0] == kf]
    P = set((v[i][1], v[i][2]) for i in cr); sk = next(iter(P))[0] % 3
    Mroot = set()
    for a in range(len(cr)):
        i, j = cr[a], cr[(a + 1) % len(cr)]
        if upper(v[(i + 1) % l]) == rootup: Mroot.add(frozenset(((v[i][1], v[i][2]), (v[j][1], v[j][2]))))
    okB = False
    for A in INV:
        if {app(A, o, p) for p in P} != P: continue
        t = app(A, o, (o[0] + 1, o[1] + 1))   # toggle test relative to the letter of kf
        tp = app(A, o, (next(iter(P))[0] + 1, next(iter(P))[1] + 1))
        if not ((tp[0] - sk) % 3 == 2 and (tp[1] - sk) % 3 == 2): continue
        if {frozenset(app(A, o, p) for p in e) for e in Mroot} != Mroot: continue
        okB = True; break
    res[(tag, l, okB)] += 1
for l in sorted({k[1] for k in res}):
    print(l, 'G: B-sym', res[('G', l, True)], 'residual', res[('G', l, False)], '| G2: B-sym', res[('H', l, True)], 'residual', res[('H', l, False)])
