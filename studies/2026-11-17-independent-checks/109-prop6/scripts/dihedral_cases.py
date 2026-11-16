#!/usr/bin/env python3
"""Prop 6 of #109, dihedral part: for I2(n), n = 3..NMAX, enumerate Aut(D_n) by brute
force and classify each automorphism sigma of the reflection representation rho_1:
  (a) chi o sigma == chi
  (b) chi o sigma == chi * lambda for a nontrivial 1-dim character lambda
  (c) otherwise (and then test: is chi o sigma a Galois conjugate of chi, possibly * lambda).
Characters are exact elements of Z[zeta_n] (polynomials reduced mod the cyclotomic
polynomial Phi_n, python-flint).  Written from scratch, independent check.
"""
import sys, json
from math import gcd
import flint

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
OUT = sys.argv[2] if len(sys.argv) > 2 else None


def run(n):
    # element (k, e) = r^k s^e ; s r s = r^-1
    def mul(a, b):
        k1, e1 = a; k2, e2 = b
        return ((k1 + (k2 if e1 == 0 else -k2)) % n, (e1 + e2) % 2)
    els = [(k, e) for e in (0, 1) for k in range(n)]
    one = (0, 0)

    def order(g):
        x, m = g, 1
        while x != one:
            x = mul(x, g); m += 1
        return m

    def power(g, k):
        x = one
        for _ in range(k):
            x = mul(x, g)
        return x
    s0, s1 = (0, 1), (1, 1)           # Coxeter generators, s1*s0 = r
    assert mul(s1, s0) == (1, 0) and order(mul(s0, s1)) == n
    invols = [g for g in els if g != one and mul(g, g) == one]
    Phi = flint.fmpz_poly.cyclotomic(n)
    X = flint.fmpz_poly([0, 1])
    zpow = [(X ** k) % Phi for k in range(n)]

    def chi_of(g, j=1):               # Galois_j(chi_1) = chi_j  (zeta -> zeta^j)
        k, e = g
        if e == 1:
            return flint.fmpz_poly([])
        return (zpow[(j * k) % n] + zpow[(-j * k) % n]) % Phi
    chi = [chi_of(g) for g in els]
    # all 1-dim characters: values (a, b) on s0, s1 with (ab)^n = 1
    lams = []
    for a in (1, -1):
        for b in (1, -1):
            if (a * b) ** n != 1:
                continue
            # value on r^k s^e = r^k s0^e, r = s1 s0
            lams.append(((a, b), [((b * a) ** k) * (a ** e) for (k, e) in els]))
    nontriv = [l for l in lams if l[0] != (1, 1)]
    autos = []
    for x in invols:
        for y in invols:
            if order(mul(x, y)) != n:
                continue
            # sigma(s0)=x, sigma(s1)=y, sigma(r)=y x ; sigma(r^k s^e)=sigma(r)^k x^e
            R = mul(y, x)
            img = [mul(power(R, k), x if e else one) for (k, e) in els]
            if len(set(img)) != 2 * n:
                continue                  # not surjective -> not an automorphism
            # homomorphism check on all pairs (exact, brute force)
            idx = {g: i for i, g in enumerate(els)}
            ok = all(img[idx[mul(g, h)]] == mul(img[idx[g]], img[idx[h]]) for g in els for h in els)
            assert ok
            autos.append((x, y, img))
    assert len(autos) == n * sum(1 for a in range(1, n + 1) if gcd(a, n) == 1), (n, len(autos))
    res = {'a': 0, 'b': 0, 'c': 0}
    c_exps, b_exps = set(), set()
    galois_ok = True
    for x, y, img in autos:
        cs = [chi_of(g) for g in img]
        kR = mul(y, x)[0]
        a_exp = min(kR % n, (-kR) % n)    # sigma(r) = r^{+-a}
        if cs == chi:
            res['a'] += 1
        elif any(cs == [chi[i] * l[1][i] for i in range(2 * n)] for l in nontriv):
            res['b'] += 1; b_exps.add(a_exp)
        else:
            res['c'] += 1; c_exps.add(a_exp)
            gal = any(cs == [chi_of(els[i], j) * l[1][i] for i in range(2 * n)]
                      for j in range(1, n) if gcd(j, n) == 1 for l in lams)
            galois_ok &= gal
    return dict(n=n, n_aut=len(autos), counts=res, b_rotation_exponents=sorted(b_exps),
                c_rotation_exponents=sorted(c_exps), c_all_galois=galois_ok)


def predicted_c(n):
    units = {a for a in range(1, n) if gcd(a, n) == 1}
    good = {1 % n, (-1) % n}
    if n % 2 == 0:
        m = (1 + n // 2) % n
        good |= {m, (-m) % n}
    return len(units - good) > 0


allres, cset = [], []
fail = None
for n in range(3, NMAX + 1):
    r = run(n)
    allres.append(r)
    if r['counts']['c'] > 0:
        cset.append(n)
    if (r['counts']['c'] > 0) != predicted_c(n):
        fail = f'n={n} disagrees with the m = +-(1+n/2) rule'
    if not r['c_all_galois']:
        fail = f'n={n} case (c) not a Galois conjugate'
    print(f"n={n:2d} |Aut|={r['n_aut']:4d} a={r['counts']['a']:3d} b={r['counts']['b']:3d} "
          f"c={r['counts']['c']:4d} b-exps={r['b_rotation_exponents']} "
          f"c-exps={r['c_rotation_exponents'][:8]}{'...' if len(r['c_rotation_exponents'])>8 else ''}",
          flush=True)
print('n with a case-(c) automorphism:', cset)
noc = [n for n in range(3, NMAX + 1) if n not in cset]
print('n with no case-(c) automorphism:', noc)
claimed = [n for n in range(3, NMAX + 1) if n in (5, 7, 9, 10, 11) or n >= 13]
print('attack list (5,7,9,10,11, n>=13) ' + ('MATCH' if claimed == cset else 'MISMATCH'))
if OUT:
    json.dump(dict(results=allres, case_c_n=cset, no_case_c_n=noc), open(OUT, 'w'), indent=1)
if claimed != cset and fail is None:
    fail = 'list differs from attack list'
print('FINAL ok' if fail is None else 'FINAL FAIL ' + fail)
