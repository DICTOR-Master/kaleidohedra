# twin_ratios_exact.py, DICTO 11 Nov 2026 ("identify the three ratios exactly"): the side ratios of the twin hulls at k = 6 (rectangles),
# k = 8 (hexagons, alternating sides) and k = 10 (rectangles), exactly. Twin points = Galois conjugates (a, b) -> (a, -b) of the exact
# Q(sqrt5) corners of D_k; faces from the float hull; squared side lengths exact in Q(sqrt5); the ratio of squared sides r2 = a + b sqrt5
# and, when r2 is a square in Q(sqrt5), its exact square root p + q sqrt5 (denesting: sqrt(a + b sqrt5) = sqrt(x) + sqrt(y) with
# x + y = a, 4xy = 5 b^2). Also k = 1, 5 (golden rectangles) and k = 0, 4 as controls (phi^2, 3, 2 sqrt5 - 1).
# usage: python -u twin_ratios_exact.py <five-fold-octet dir> <out.json>
import sys, os, json
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
head = open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0]
_OUT = os.path.abspath(sys.argv[2]); sys.argv = [sys.argv[0], sys.argv[1], '0', '/dev/null']; exec(head)
import numpy as np, gmpy2
from scipy.spatial import ConvexHull
from fractions import Fraction
def conj(x): return R5(x.a, -x.b)
def tw(v): return tuple(conj(x) for x in v)
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
def sq(u, v): d = sub(u, v); return dot(d, d)
def rstr(x): return f'{x.a} + {x.b}·√5' if x.b != 0 else f'{x.a}'
def denest(r):
    """exact sqrt of a + b sqrt5 in Q(sqrt5) if it exists: (p + q sqrt5)^2 = p^2 + 5 q^2 + 2 p q sqrt5."""
    a, b = r.a, r.b; disc = a * a - 5 * b * b
    if disc < 0: return None
    s = gmpy2.isqrt_rem if False else None
    num, den = disc.numerator, disc.denominator
    if not (gmpy2.is_square(num) and gmpy2.is_square(den)): return None
    sd = gmpy2.mpq(gmpy2.isqrt(num), gmpy2.isqrt(den))
    for p2 in ((a + sd) / 2, (a - sd) / 2):                                    # p^2 candidates; then q = b / (2p)
        if p2 <= 0: continue
        n2, d2 = p2.numerator, p2.denominator
        if gmpy2.is_square(n2) and gmpy2.is_square(d2):
            p = gmpy2.mpq(gmpy2.isqrt(n2), gmpy2.isqrt(d2)); q = b / (2 * p); x = R5(p, q)
            if x.a * x.a + 5 * x.b * x.b == a and 2 * x.a * x.b == b:
                return x if float(x.a) + float(x.b) * 5 ** .5 > 0 else R5(-x.a, -x.b)   # 11-11: take the POSITIVE root
    return None
WANT = {0: None, 1: 4, 4: None, 5: 4, 6: 4, 8: 6, 10: 4}
rows = []; W = [tuple(cv(x) for x in v) for v in OG]
for k in range(11):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W])
    F, ne, _ = exact_faces(W, idx, Wfx)
    if k in WANT:
        cor = sorted(set(i for mem in F for i in mem)); T = [tw(W[i]) for i in cor]
        Tf = np.array([[twinf(x) for x in W[i]] for i in cor]); Tf_n = Tf / np.linalg.norm(Tf, axis=1).max()
        h = ConvexHull(Tf_n); E = h.equations; n = len(E); par = list(range(n))
        def find(i):
            while par[i] != i: par[i] = par[par[i]]; i = par[i]
            return i
        for f in range(n):
            for g in h.neighbors[f]:
                if np.abs(E[f] - E[g]).max() < 1e-9: par[find(f)] = find(g)
        grp = {}
        for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
        # simpler, robust: edges of the hull polygons in cyclic order
        Es = set()
        for pts in grp.values():
            idx2 = np.array(sorted(pts)); Q = Tf_n[idx2]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T
            cyc = list(idx2[np.argsort(np.arctan2(q[:, 1], q[:, 0]))])
            for a, b in zip(cyc, cyc[1:] + cyc[:1]): Es.add((min(a, b), max(a, b)))
        lens = {}
        for a, b in Es:
            s2 = sq(T[a], T[b]); lens[(s2.a, s2.b)] = s2
        L = sorted(lens.values(), key=lambda x: float(x.a) + float(x.b) * S5)
        out = dict(k=k, edge_lengths2=[rstr(x) for x in L])
        if len(L) >= 2:
            r2 = L[-1] / L[0]; rt = denest(r2)
            out.update(ratio2_max_min=rstr(r2), ratio2_float=float(r2.a) + float(r2.b) * S5, ratio_exact=(rstr(rt) if rt else f'sqrt({rstr(r2)})'),
                       ratio_float=(float(r2.a) + float(r2.b) * S5) ** .5)
        rows.append(out)
        print(f"k {k:2d}: {len(L)} edge lengths | longest/shortest: squared = {out.get('ratio2_max_min')} | ratio = {out.get('ratio_exact')} = {out.get('ratio_float', 0):.9f}", flush=True)
    feet = {}
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    W = list(feet)
json.dump(rows, open(_OUT, 'w'), indent=1, default=str)
chk = {r['k']: r.get('ratio_float') for r in rows}
ok = abs(chk[1] - 2.618034) < 1e-6 and abs(chk[4] - 3.0) < 1e-9 and abs(chk[0] - 3.472136) < 1e-6
print('FINAL ok' if ok else 'FINAL FAIL: controls (phi^2 at k = 1, 3 at k = 4, 2 sqrt5 - 1 at k = 0) not reproduced')
