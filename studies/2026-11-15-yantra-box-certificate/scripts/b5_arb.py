"""Step 5: independent re-verification of every leaf with FLINT/Arb ball arithmetic (python-flint), a different library and a different
enclosure from b4_check.py.  For each leaf (in the chart's own parameters, not rescaled) the polynomial p is enclosed by the mean-value
form p(X) in p(m) + sum_j dp/dx_j(X) (X_j - m_j), where p(m) and the gradient over X are evaluated term by term in ball arithmetic (Moore's
centred form; Arb by F. Johansson).  A leaf whose enclosure is inconclusive is split into 8 and each part is retried (two rounds); a part
that is still inconclusive counts as a failure.  Holes are checked by exact rational comparison.
Usage: b5_arb.py polys.json bnb.json holes.json|- [workers].  FINAL ok iff every leaf is confirmed."""
import json, sys, time, os
from fractions import Fraction as Fq
from multiprocessing import Pool
import flint
from flint import arb, fmpq
flint.ctx.prec = 320
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
psrc, bsrc, hsrc = sys.argv[1], sys.argv[2], sys.argv[3]
NW = int(sys.argv[4]) if len(sys.argv) > 4 else 4
data = json.load(open(psrc)); cert = json.load(open(bsrc))
holes = json.load(open(hsrc))['holes'] if hsrc != '-' else []
box = [[Fq(a), Fq(b)] for a, b in data['box']]
A = [a for a, b in box]; W = [b - a for a, b in box]
P = {}
for k, p in data['F'].items(): P[('F', k)] = [(tuple(e), int(c)) for e, c in p]
for k, nd in data['tests'].items():
    P[('N', k)] = [(tuple(e), int(c)) for e, c in nd['N']]; P[('D', k)] = [(tuple(e), int(c)) for e, c in nd['D']]
G = {key: [[(tuple(e[i] - (i == j) for i in range(3)), c * e[j]) for e, c in p if e[j] > 0] for j in range(3)] for key, p in P.items()}
def ev(p, x):
    pw = [{}, {}, {}]
    def pk(i, k):
        if k not in pw[i]: pw[i][k] = x[i] ** k
        return pw[i][k]
    s = arb(0)
    for e, c in p: s += c * pk(0, e[0]) * pk(1, e[1]) * pk(2, e[2])
    return s
def sign_on(key, lo, hi):
    """lo, hi: Fractions per coordinate.  returns +1 / -1 if certified, else 0."""
    m = [arb(fmpq((lo[j] + hi[j]).numerator, (lo[j] + hi[j]).denominator) / 2) for j in range(3)]
    X = [arb(fmpq(((lo[j] + hi[j]) / 2).numerator, ((lo[j] + hi[j]) / 2).denominator), fmpq(((hi[j] - lo[j]) / 2).numerator, ((hi[j] - lo[j]) / 2).denominator)) for j in range(3)]
    v = ev(P[key], m)
    for j in range(3):
        v += ev(G[key][j], X) * (X[j] - m[j])
    if v > 0: return 1
    if v < 0: return -1
    return 0
def leaf_box(cell):
    lo = []; hi = []
    for j, (d, i) in enumerate(cell):
        lo.append(A[j] + W[j] * Fq(i, 2**d)); hi.append(A[j] + W[j] * Fq(i + 1, 2**d))
    return lo, hi
def test_box(kind, name, lo, hi):
    if kind == 'F': return sign_on(('F', name), lo, hi) != 0
    sN = sign_on(('N', name), lo, hi)
    if sN == 0: return False
    return sN * sign_on(('D', name), lo, hi) == -1
def split8(lo, hi):
    mid = [(lo[j] + hi[j]) / 2 for j in range(3)]
    for b in range(8):
        l = [lo[j] if not (b >> j) & 1 else mid[j] for j in range(3)]; h = [mid[j] if not (b >> j) & 1 else hi[j] for j in range(3)]
        yield l, h
def check(lf):
    d0, i0, d1, i1, d2, i2, kind, name = lf
    lo, hi = leaf_box(((d0, i0), (d1, i1), (d2, i2)))
    if kind == 'H':
        Hb = [h for h in holes if h['name'] == name][0]['box']
        return (all(Fq(Hb[j][0]) <= lo[j] and hi[j] <= Fq(Hb[j][1]) for j in range(3)), 0)
    if test_box(kind, name, lo, hi): return (True, 0)
    for l1, h1 in split8(lo, hi):
        if test_box(kind, name, l1, h1): continue
        if not all(test_box(kind, name, l2, h2) for l2, h2 in split8(l1, h1)): return (False, 2)
    return (True, 1)
if __name__ == '__main__':
    leaves = cert['leaves']; say(f'{psrc}: {len(leaves)} leaves, Arb at {flint.ctx.prec} bits')
    res = []; fails = []
    with Pool(NW) as pool:
        for k, r in enumerate(pool.imap(check, leaves, chunksize=32)):
            res.append(r)
            if not r[0]: fails.append(leaves[k])
            if (k + 1) % max(1, len(leaves) // 10) == 0: print(f'PROGRESS {(k + 1) / len(leaves):.3f} leaves {k + 1}/{len(leaves)}', flush=True)
    nsplit = sum(1 for r in res if r[1] == 1)
    say('Arb: confirmed', len(res) - len(fails), 'of', len(res), '; needed a split:', nsplit, '; failed:', len(fails))
    if fails: say('failed (first 10):', fails[:10])
    json.dump({'polys': psrc, 'leaves': len(res), 'confirmed': len(res) - len(fails), 'split': nsplit, 'failed': fails[:50]},
              open(bsrc.replace('.json', '.arb.json'), 'w'), indent=1)
    print('FINAL ok' if not fails else f'FINAL FAIL: {len(fails)} leaves not confirmed')
