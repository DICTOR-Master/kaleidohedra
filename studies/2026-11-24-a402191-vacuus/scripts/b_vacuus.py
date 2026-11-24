"""Vacuus of the type-B permutohedron P(l) = conv{signed permutations of (l1 > ... > ln > 0)}, exact.

Brute force (independent of the theorem): vertices -> facets (vertex sets maximising a signed
0/1 functional) -> ridges (facet pairs meeting in affine dimension n-2) -> plate through O
(exact nullspace).  Compared with the count of Theorem B:
  generic  : (5^n - 2*3^n + 1)/2  (every plate = one ridge and its opposite);
  in general: sum over (s,d) with  L(s) != N(s,d)  of  n!/(s!d!(n-s-d)!) 2^(s+d-1)
              + sum over t admitting some s with L(s) = N(s,t-s) of  C(n,t) 2^(t-1),
  L(s) = l1+...+ls, N(s,d) = l(s+1)+...+l(s+d).
Cases: uniform B3, B4 (l_k = 1+(k-1)sqrt2), integer values (1..n), a generic integer choice.
"""
import sys, json, itertools
from fractions import Fraction as Fr
from math import factorial as F, comb
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from exact import Q2, rank, nullspace, normalize, iszero


def formula(lam):
    n = len(lam)
    L = lambda s: sum(lam[:s], Q2(0))
    N = lambda s, d: sum(lam[s:s + d], Q2(0))
    tot = 0
    eq_t = set()
    for s in range(1, n):
        for d in range(1, n - s + 1):
            if L(s) == N(s, d):
                eq_t.add(s + d)
            else:
                tot += F(n) // (F(s) * F(d) * F(n - s - d)) * 2 ** (s + d - 1)
    tot += sum(comb(n, t) * 2 ** (t - 1) for t in eq_t)
    return tot, sorted(eq_t)


def run(lam, label):
    n = len(lam)
    lam = [x if isinstance(x, Q2) else Q2(x) for x in lam]
    verts = []
    for p in itertools.permutations(range(n)):
        for sg in itertools.product((1, -1), repeat=n):
            verts.append(tuple(lam[p[i]] * sg[i] for i in range(n)))
    facets = {}
    for k in range(1, n + 1):
        for S in itertools.combinations(range(n), k):
            for sg in itertools.product((1, -1), repeat=k):
                vals = [sum((v[i] * e for i, e in zip(S, sg)), Q2(0)) for v in verts]
                mx = max(vals)  # exact order in Q(sqrt2)
                facets[(S, sg)] = frozenset(i for i, x in enumerate(vals) if x == mx)
    plates = {}
    ridges = 0
    for f1, f2 in itertools.combinations(list(facets), 2):
        I = facets[f1] & facets[f2]
        if len(I) < 2:
            continue
        vs = [verts[i] for i in I]
        diffs = [[a - b for a, b in zip(v, vs[0])] for v in vs[1:]]
        if rank(diffs) != n - 2:
            continue
        ridges += 1
        ns = nullspace([list(v) for v in vs], n)
        assert len(ns) == 1
        plates.setdefault(normalize(ns[0]), []).append((f1, f2))
    mirrors = set()
    for i in range(n):
        mirrors.add(normalize([Q2(1) if k == i else Q2(0) for k in range(n)]))
        for j in range(i + 1, n):
            for e in (1, -1):
                mirrors.add(normalize([Q2(1) if k == i else (Q2(e) if k == j else Q2(0)) for k in range(n)]))
    fcount, eq_t = formula(lam)
    out = dict(case=label, n=n, ridges=ridges, ridges_formula=5 ** n - 2 * 3 ** n + 1,
               plates=len(plates), formula=fcount, generic=(5 ** n - 2 * 3 ** n + 1) // 2,
               equal_support_sizes=eq_t, on_mirror=sum(1 for k in plates if k in mirrors),
               ridges_per_plate=sorted({len(v) for v in plates.values()}))
    return out


if __name__ == "__main__":
    r2 = Q2(0, 1)
    cases = [([Q2(1) + 2 * r2, Q2(1) + r2, Q2(1)], "uniform B3 (truncated cuboctahedron)"),
             ([3, 2, 1], "B3 values (3,2,1)"),
             ([7, 3, 1], "B3 generic values (7,3,1)"),
             ([Q2(1) + 3 * r2, Q2(1) + 2 * r2, Q2(1) + r2, Q2(1)], "uniform B4 (omnitruncated tesseract)"),
             ([4, 3, 2, 1], "B4 values (4,3,2,1)")]
    ok = True
    res = []
    for lam, label in cases:
        r = run(lam, label)
        print(json.dumps(r), flush=True)
        print(f"PROGRESS {len(res)+1}/{len(cases)} {label}", flush=True)
        ok &= r["ridges"] == r["ridges_formula"] and r["plates"] == r["formula"]
        res.append(r)
    ok &= res[0]["plates"] == 36 and res[0]["on_mirror"] == 0 and res[3]["plates"] == 232
    json.dump(res, open(__file__.rsplit("/", 2)[0] + "/data/b_vacuus.json", "w"), indent=1)
    print("FINAL ok" if ok else "FINAL FAIL")
