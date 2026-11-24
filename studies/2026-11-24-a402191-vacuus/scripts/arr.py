"""The Vacuus as a hyperplane arrangement: intersection lattice, characteristic polynomial,
number of regions (Zaslavsky 1975: r = sum |mu|), and the simplicial test
  sum over chambers of #walls = 2 * sum_H r(A^H)  ==  rank * r   (simplicial iff equal).
Cases: A, n = 4 and 5 (in the sum-zero space of R^n); uniform B3 in Q(sqrt2).
Usage: python3 arr.py [nmaxA]
"""
import sys, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from exact import Q2, nullspace, normalize, iszero, rank


def dot(u, v):
    s = 0
    for a, b in zip(u, v):
        s = s + a * b
    return s


def lattice(normals, extra, m):
    """normals: list of vectors in R^N; extra: constraint rows defining the ambient space (dim m).
    Flats are frozensets of hyperplane indices. Returns list of levels (rank 0..m)."""
    N = len(normals[0])
    levels = [{frozenset(): None}]
    levels.append({frozenset([i]): None for i in range(len(normals))})
    for k in range(2, m + 1):
        new = {}
        for X in levels[k - 1]:
            for h in range(len(normals)):
                if h in X:
                    continue
                gens = [normals[i] for i in X] + [normals[h]]
                if rank(gens) != k:
                    continue
                if k == m:
                    new[frozenset(range(len(normals)))] = None
                    continue
                basis = nullspace([list(r) for r in gens] + [list(r) for r in extra], N)  # the flat
                Y = frozenset(i for i, nv in enumerate(normals) if all(iszero(dot(nv, b)) for b in basis))
                new[Y] = None
            # small speed-up not needed for these sizes
        levels.append(new)
    return [list(l) for l in levels]


def mobius_counts(levels, m):
    """mu(0, X) on the whole intersection lattice (X ordered by inclusion of hyperplane sets)."""
    mu, rk = {}, {}
    for k, lev in enumerate(levels):
        for X in lev:
            rk[X] = k
            mu[X] = 1 if k == 0 else -sum(v for Y, v in mu.items() if rk[Y] < k and Y < X)
    return mu, rk


def analyse(normals, extra, m, label):
    levels = lattice(normals, extra, m)
    mu, rk = mobius_counts(levels, m)
    chi = [0] * (m + 1)  # coefficient of t^(m-k)
    for X, v in mu.items():
        chi[rk[X]] += v
    r = sum(abs(v) for v in mu.values())
    walls = 0
    for h in range(len(normals)):
        H = frozenset([h])
        sub = {}
        for k, lev in enumerate(levels):
            for X in lev:
                if H <= X:
                    sub[X] = k
        muH = {}
        for X in sorted(sub, key=lambda X: sub[X]):
            if X == H:
                muH[X] = 1
            else:
                muH[X] = -sum(muH[Y] for Y in muH if Y < X)
        walls += 2 * sum(abs(v) for v in muH.values())
    out = dict(case=label, hyperplanes=len(normals), rank=m,
               flats_per_rank=[len(l) for l in levels], chi_coeffs=chi, regions=r,
               wall_incidences=walls, simplicial=(walls == m * r),
               mean_walls_per_chamber=str(Fr(walls, r)))
    return out


def a_plates(n):
    import a_vacuus
    import itertools as it
    keys = set()
    for a in range(1, n):
        for b in range(1, n - a):
            c = n - a - b
            for B1 in it.combinations(range(n), a):
                rest = [i for i in range(n) if i not in B1]
                for B2 in it.combinations(rest, b):
                    B3 = [i for i in rest if i not in B2]
                    w = [c * (a + b) if i in B1 else (a * (b + c) if i in B3 else 0) for i in range(n)]
                    keys.add(a_vacuus.centred_key(w, n))
    return [list(k) for k in keys]


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    res = []
    for n in range(4, nmax + 1):
        P = a_plates(n)
        r = analyse(P, [[Fr(1)] * n], n - 1, f"A Vacuus, n={n} (permutohedron of dimension {n-1})")
        print(json.dumps(r), flush=True)
        print(f"PROGRESS {n-3}/{nmax-2} arrangement n={n}", flush=True)
        res.append(r)
    # uniform B3: plates from the brute force of b_vacuus (recomputed here)
    import b_vacuus
    r2 = Q2(0, 1)
    lam = [Q2(1) + 2 * r2, Q2(1) + r2, Q2(1)]
    # rebuild plate normals by the pencil formula h(S2) chi_{S1} - h(S1) chi_{S2} (checked against brute force in b_vacuus)
    n = 3
    keys = set()
    for s in range(1, n):
        for d in range(1, n - s + 1):
            for S2 in itertools.permutations(range(n), s + d):
                for sg in itertools.product((1, -1), repeat=s + d):
                    S1 = S2[:s]
                    hs = sum(lam[:s], Q2(0)); ht = sum(lam[:s + d], Q2(0))
                    w = [Q2(0)] * n
                    for idx, i in enumerate(S2):
                        w[i] = (ht - hs) * sg[idx] if idx < s else (-hs) * sg[idx]
                    keys.add(normalize(w))
    B = [list(k) for k in keys]
    r = analyse(B, [], 3, "uniform B3 Vacuus (truncated cuboctahedron)")
    print(json.dumps(r), flush=True)
    res.append(r)
    ok = res[0]["hyperplanes"] == 15 and B and len(B) == 36
    json.dump(res, open(__file__.rsplit("/", 2)[0] + f"/data/arrangement.json", "w"), indent=1)
    print("FINAL ok" if ok else "FINAL FAIL")
