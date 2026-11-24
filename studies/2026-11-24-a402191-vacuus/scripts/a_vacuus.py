"""Vacuus of the permutohedron Pi_n = conv{permutations of (1..n)}, exact (Fractions).

Brute force, independent of the theorem: vertices -> facets (vertex sets maximising a
0/1 functional) -> ridges (facet pairs meeting in affine dimension n-3) -> the hyperplane
through the centre and the ridge (exact nullspace).  Checks, for every ridge:
  (1) the plate normal equals the predicted  c(a+b) 1_{B1} + a(b+c) 1_{B3}  (mod 1, up to scale);
  (2) distinct plates = A402191 formula;  (3) no plate is a type-A mirror x_i = x_j;
  (4) two-valued plates = resonance hyperplanes sum_S y = 0, which ones.
Usage: python3 a_vacuus.py NMAX
"""
import sys, json, itertools
from fractions import Fraction as Fr
from math import factorial as F, comb
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from exact import rank, nullspace, normalize


def oeis_formula(n):
    s = sum(F(n) // (F(a) * F(b) * F(n - a - b)) for a in range(1, n) for b in range(1, n)
            if n - a - b >= 1 and a < n - a - b)
    return s + (2 ** (n - 1) - 1 if n % 2 else 2 ** (n - 2) - 1)


def closed_form(n):
    cn = sum(F(n) // (F(k) ** 2 * F(n - 2 * k)) for k in range(n // 2 + 1))  # A002426
    An = cn - 1 - (comb(n, n // 2) if n % 2 == 0 else 0)
    ridges = 3 ** n - 3 * 2 ** n + 3
    return (ridges - An) // 2 + (2 ** (n - 1) - 1 if n % 2 else 2 ** (n - 2) - 1)


def centred_key(w, n):
    m = Fr(sum(w), n)
    return normalize([x - m for x in w])


def run(n):
    verts = list(itertools.permutations(range(1, n + 1)))
    c = Fr(n + 1, 2)
    facets = {}
    for k in range(1, n):
        for S in itertools.combinations(range(n), k):
            vals = [sum(v[i] for i in S) for v in verts]
            mn = min(vals)
            facets[S] = frozenset(i for i, x in enumerate(vals) if x == mn)
    keys = list(facets)
    plates = {}
    nridges = 0
    bad = 0
    for S, T in itertools.combinations(keys, 2):
        I = facets[S] & facets[T]
        if not I:
            continue
        vs = [verts[i] for i in I]
        base = vs[0]
        diffs = [[Fr(x - y) for x, y in zip(v, base)] for v in vs[1:]]
        if rank(diffs) != n - 3:
            continue
        nridges += 1
        rows = [[Fr(1)] * n] + [[Fr(x) - c for x in v] for v in vs]
        ns = nullspace(rows, n)
        assert len(ns) == 1, (S, T)
        key = normalize(ns[0])
        # blocks: smaller facet set is B1
        A, B = (set(S), set(T)) if len(S) < len(T) else (set(T), set(S))
        assert A < B, "facets meeting in a ridge are nested"
        B1, B2, B3 = A, B - A, set(range(n)) - B
        a, b, cc = len(B1), len(B2), len(B3)
        pred = [cc * (a + b) if i in B1 else (a * (b + cc) if i in B3 else 0) for i in range(n)]
        if centred_key(pred, n) != key:
            bad += 1
        plates.setdefault(key, []).append((tuple(sorted(B1)), tuple(sorted(B2)), tuple(sorted(B3))))
    mirrors = {centred_key([1 if k == i else (-1 if k == j else 0) for k in range(n)], n)
               for i, j in itertools.combinations(range(n), 2)}
    resonance = {centred_key([1 if k in S else 0 for k in range(n)], n): S
                 for r in range(1, n) for S in itertools.combinations(range(n), r)}
    two = [k for k in plates if len(set(k)) == 2]
    res_hit = sorted({min(len(resonance[k]), n - len(resonance[k])) for k in two if k in resonance})
    out = dict(n=n, ridges=nridges, ridges_formula=3 ** n - 3 * 2 ** n + 3, plates=len(plates),
               oeis=oeis_formula(n), closed=closed_form(n), normal_mismatches=bad,
               two_valued=len(two), two_valued_all_resonance=all(k in resonance for k in two),
               resonance_total=len(resonance) // 2 if n > 2 else 0,
               two_valued_subset_sizes=res_hit,
               three_valued=len(plates) - len(two),
               three_valued_in_resonance=sum(1 for k in plates if len(set(k)) == 3 and k in resonance),
               on_typeA_mirror=sum(1 for k in plates if k in mirrors),
               ridges_per_plate=sorted({len(v) for v in plates.values()}))
    # resonance count: S and complement give the same centred key, so the dict already merged them
    out["resonance_total"] = len(resonance)
    return out


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    res = []
    ok = True
    for n in range(3, nmax + 1):
        r = run(n)
        print(json.dumps(r), flush=True)
        print(f"PROGRESS {n-2}/{nmax-2} A n={n}", flush=True)
        ok &= (r["ridges"] == r["ridges_formula"] and r["plates"] == r["oeis"] == r["closed"]
               and r["normal_mismatches"] == 0 and r["on_typeA_mirror"] == 0
               and r["two_valued_all_resonance"] and r["three_valued_in_resonance"] == 0)
        res.append(r)
    json.dump(res, open(__file__.rsplit("/", 2)[0] + "/data/a_vacuus.json", "w"), indent=1)
    print("FINAL ok" if ok else "FINAL FAIL")
