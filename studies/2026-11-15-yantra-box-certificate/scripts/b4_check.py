"""Step 4: exact checker of a branch-and-bound certificate (integer arithmetic only; this is the computation a Lean kernel would repeat).

Input: polys-<chart>.json, bnb-<chart>.json (leaves), and the holes file used by the generator (or '-').
1. Coverage: the leaves are rebuilt into the bisection tree from the root box (split rule: the coordinate of least depth, lowest index
   first, the rule of b2_bnb.py).  Every node is either a leaf or has both children; every leaf is reached exactly once.  So the leaves
   cover the box (closed cells; shared faces are harmless).
2. Each leaf's test is re-proved exactly.  Coordinates are rescaled to the unit cube (x_j = A_j + W_j y_j), so a leaf is the dyadic
   cell prod [i_j, i_j + 1] / 2^d_j.  Two enclosures (both sound for coordinates >= 0, both with a Lean-ready integer form):
     monotone split:  p+(lo) - p-(hi) <= p <= p+(hi) - p-(lo), scaled by 2^(sum D_j d_j)  (the evaluator of lean/BoxCheck.lean);
     slope form (Krawczyk and Neumaier 1985): p = p(m) + sum_j (y_j - m_j) A_j, with x^a - m^a = (x - m) sum_k x^k m^(a-1-k);
       the A_j are bounded by the monotone split; m is the cell centre, so |y_j - m_j| <= 2^-(d_j + 1).
   F leaf: the named polynomial has a fixed sign.  T leaf: the test's N and D have fixed opposite signs.  H leaf: the cell lies in the
   named hole (exact rational comparison).
Usage: b4_check.py polys.json bnb.json holes.json|- [workers]   (env PERTURB='F:G:<rational>' adds a constant to one polynomial:
the negative control).  FINAL ok iff coverage holds and every leaf passes."""
import json, sys, time, os
from fractions import Fraction as Fq
from multiprocessing import Pool
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
psrc, bsrc, hsrc = sys.argv[1], sys.argv[2], sys.argv[3]
NW = int(sys.argv[4]) if len(sys.argv) > 4 else 16
data = json.load(open(psrc)); cert = json.load(open(bsrc))
holes = json.load(open(hsrc))['holes'] if hsrc != '-' else []
box = [[Fq(a), Fq(b)] for a, b in data['box']]
A = [a for a, b in box]; W = [b - a for a, b in box]
def rescale(p):
    """p(A + W y) with integer coefficients (times a positive constant): sign tests are unchanged."""
    from math import comb
    out = {}
    for e, c in p:
        c = Fq(int(c)); terms = [((), c)]
        # expand prod_j (A_j + W_j y_j)^e_j
        parts = []
        for j in range(3):
            parts.append([(e[j], W[j]**e[j])] if A[j] == 0 else [(k, Fq(comb(e[j], k)) * A[j]**(e[j] - k) * W[j]**k) for k in range(e[j] + 1)])
        for k0, c0 in parts[0]:
            for k1, c1 in parts[1]:
                for k2, c2 in parts[2]:
                    key = (k0, k1, k2); out[key] = out.get(key, 0) + c * c0 * c1 * c2
    den = 1
    for v in out.values():
        den = den * v.denominator // __import__('math').gcd(den, v.denominator)
    return [(k, int(v * den)) for k, v in out.items() if v != 0]
pert = os.environ.get('PERTURB')
P = {}
for k, p in data['F'].items(): P[('F', k)] = rescale(p)
for k, nd in data['tests'].items(): P[('N', k)] = rescale(nd['N']); P[('D', k)] = rescale(nd['D'])
if pert:
    _, k, val = pert.split(':'); v = Fq(val)
    # add v (in the original coordinates) to F_k: rescaling a constant is the constant, times the same positive factor
    orig = data['F'][k] + [[[0, 0, 0], 0]]
    p2 = [(e, Fq(int(c))) for e, c in data['F'][k]] + [((0, 0, 0), v)]
    den = 1
    for e, c in p2: den = den * c.denominator // __import__('math').gcd(den, c.denominator)
    P[('F', k)] = rescale([(e, int(c * den)) for e, c in p2])
    say('NEGATIVE CONTROL: perturbed', k, 'by', v)
DEG = {key: [max([e[j] for e, c in p] + [0]) for j in range(3)] for key, p in P.items()}
def mono_split(p, D, cell):
    lo = 0; hi = 0
    (d0, i0), (d1, i1), (d2, i2) = cell
    for e, c in p:
        a = (i0**e[0] << ((D[0] - e[0]) * d0)) * (i1**e[1] << ((D[1] - e[1]) * d1)) * (i2**e[2] << ((D[2] - e[2]) * d2))
        b = ((i0 + 1)**e[0] << ((D[0] - e[0]) * d0)) * ((i1 + 1)**e[1] << ((D[1] - e[1]) * d1)) * ((i2 + 1)**e[2] << ((D[2] - e[2]) * d2))
        if c > 0: lo += c * a; hi += c * b
        else: lo += c * b; hi += c * a
    return lo, hi                                     # bounds of p * 2^(sum D_j d_j)
def slope(p, D, cell):
    """bounds of p * T, T = prod 2^(e_j D_j), e_j = d_j + 1 (cell centre on the finer grid)."""
    E = [d + 1 for d, i in cell]
    Lo = [2 * i for d, i in cell]; Hi = [2 * i + 2 for d, i in cell]; Mi = [2 * i + 1 for d, i in cell]
    pw = lambda x, n: [x**k for k in range(n + 1)]
    PL = [pw(Lo[j], D[j]) for j in range(3)]; PH = [pw(Hi[j], D[j]) for j in range(3)]; PM = [pw(Mi[j], D[j]) for j in range(3)]
    def snum(x, m, n):                                 # S_k numerators, S_k = x S_{k-1} + m^(k-1)
        S = [0] * (n + 1)
        for k in range(1, n + 1): S[k] = x * S[k - 1] + m**(k - 1)
        return S
    SL = [snum(Lo[j], Mi[j], D[j]) for j in range(3)]; SH = [snum(Hi[j], Mi[j], D[j]) for j in range(3)]
    sh = lambda j, a: (D[j] - a) * E[j]
    val = 0; up = [0, 0, 0]; lw = [0, 0, 0]
    for e, c in p:
        a, b, g = e
        val += c * (PM[0][a] << sh(0, a)) * (PM[1][b] << sh(1, b)) * (PM[2][g] << sh(2, g))
        # A_x: S_a(x) y^b z^g ; A_y: m_x^a S_b(y) z^g ; A_z: m_x^a m_y^b S_g(z)   (scaled: the 2^-e_j of |y_j - m_j| absorbed)
        hiX = ((SH[0][a] << sh(0, a)) * (PH[1][b] << sh(1, b)) * (PH[2][g] << sh(2, g)),
               (PM[0][a] << sh(0, a)) * (SH[1][b] << sh(1, b)) * (PH[2][g] << sh(2, g)),
               (PM[0][a] << sh(0, a)) * (PM[1][b] << sh(1, b)) * (SH[2][g] << sh(2, g)))
        loX = ((SL[0][a] << sh(0, a)) * (PL[1][b] << sh(1, b)) * (PL[2][g] << sh(2, g)),
               (PM[0][a] << sh(0, a)) * (SL[1][b] << sh(1, b)) * (PL[2][g] << sh(2, g)),
               (PM[0][a] << sh(0, a)) * (PM[1][b] << sh(1, b)) * (SL[2][g] << sh(2, g)))
        for j in range(3):
            if c > 0: up[j] += c * hiX[j]; lw[j] += c * loX[j]
            else: up[j] += c * loX[j]; lw[j] += c * hiX[j]
    rad = sum(max(abs(up[j]), abs(lw[j])) for j in range(3))
    return val - rad, val + rad
def sign_of(key, cell):
    p = P[key]; D = DEG[key]
    l, h = mono_split(p, D, cell)
    if l > 0: return 1, 'mono'
    if h < 0: return -1, 'mono'
    l, h = slope(p, D, cell)
    if l > 0: return 1, 'slope'
    if h < 0: return -1, 'slope'
    return 0, None
def check_leaf(lf):
    d0, i0, d1, i1, d2, i2, kind, name = lf
    cell = ((d0, i0), (d1, i1), (d2, i2))
    if kind == 'F':
        s, how = sign_of(('F', name), cell); return (s != 0, how, 1, len(P[('F', name)]))
    if kind == 'T':
        sN, h1 = sign_of(('N', name), cell)
        if sN == 0: return (False, None, 1, len(P[('N', name)]))
        sD, h2 = sign_of(('D', name), cell)
        return (sN * sD == -1, (h1 if h1 == 'slope' or h2 == 'slope' else 'mono') if sN * sD == -1 else None, 2, len(P[('N', name)]) + len(P[('D', name)]))
    if kind == 'H':
        H = [h for h in holes if h['name'] == name][0]['box']
        ok = all(Fq(H[j][0]) <= A[j] + W[j] * Fq(i, 2**d) and A[j] + W[j] * Fq(i + 1, 2**d) <= Fq(H[j][1])
                 for j, (d, i) in enumerate(cell))
        return (ok, 'hole', 0, 0)
    return (False, None, 0, 0)
if __name__ == '__main__':
    leaves = cert['leaves']
    say(f'{psrc}: {len(leaves)} leaves')
    print('PROGRESS 0.05 coverage', flush=True)
    L = {(l[0], l[1], l[2], l[3], l[4], l[5]): l for l in leaves}
    assert len(L) == len(leaves), 'duplicate leaves'
    seen = 0; stack = [(0, 0, 0, 0, 0, 0)]; cover_ok = True; maxd = 0
    while stack:
        nd = stack.pop()
        if nd in L: seen += 1; continue
        d = [nd[0], nd[2], nd[4]]; maxd = max(maxd, max(d))
        if max(d) > 80: cover_ok = False; break
        j = min(range(3), key=lambda k: (d[k], k))
        for b in (0, 1):
            c = list(nd); c[2 * j] += 1; c[2 * j + 1] = 2 * nd[2 * j + 1] + b; stack.append(tuple(c))
    cover_ok = cover_ok and seen == len(leaves) and not cert.get('open')
    say('coverage: tree rebuilt, leaves reached', seen, 'of', len(leaves), '; open boxes in certificate:', len(cert.get('open', [])), '->', cover_ok)
    print('PROGRESS 0.1 leaves', flush=True)
    res = []; fails = []
    with Pool(NW) as pool:
        for k, r in enumerate(pool.imap(check_leaf, leaves, chunksize=64)):
            res.append(r)
            if not r[0]: fails.append(leaves[k])
            if (k + 1) % max(1, len(leaves) // 20) == 0: print(f'PROGRESS {0.1 + 0.9 * (k + 1) / len(leaves):.3f} leaves {k + 1}/{len(leaves)}', flush=True)
    from collections import Counter
    how = Counter(r[1] for r in res if r[0]); evals = sum(r[2] for r in res); terms = sum(r[3] for r in res)
    dig = 0
    for l in leaves:
        for d, i in ((l[0], l[1]), (l[2], l[3]), (l[4], l[5])): dig = max(dig, len(str(i + 1)), len(str(2**d)))
    say('leaves passed:', len(res) - len(fails), 'of', len(res), '; by enclosure:', dict(how), '; polynomial evaluations:', evals, '; term evaluations:', terms,
        '; max digits of a box endpoint (numerator/denominator):', dig)
    if fails: say('FAILED leaves (first 10):', fails[:10])
    json.dump({'polys': psrc, 'leaves': len(leaves), 'passed': len(res) - len(fails), 'failed': len(fails), 'by_enclosure': dict(how),
               'evaluations': evals, 'term_evaluations': terms, 'max_endpoint_digits': dig, 'coverage': cover_ok, 'max_depth': maxd,
               'perturb': pert, 'failed_sample': fails[:50]}, open(bsrc.replace('.json', '.check.json') if not pert else bsrc.replace('.json', '.perturbed-check.json'), 'w'), indent=1)
    print('PROGRESS 1.0 done', flush=True)
    ok = cover_ok and not fails
    print('FINAL ok' if ok else f'FINAL FAIL: coverage {cover_ok}, failed leaves {len(fails)}')
