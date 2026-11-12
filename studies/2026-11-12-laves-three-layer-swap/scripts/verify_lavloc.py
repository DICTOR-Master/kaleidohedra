# Independent check of the Laves locality certificates (lavloc.py). Shares NO geometry code with lavloc.py / lavgeom.py:
#  (1) site sets are rebuilt from #64's own net builder (splash-rules/run2/laves_net.py, laves(word)) on concrete periodic stackings:
#      for every neighbourhood (layers -2..3 round gap 0) and every continuation (layers -4, -3 and 4, 5: 16 per neighbourhood), the
#      sites of gaps -4..4 are read off the built net (lateral translates within Q <= 4/3 of the role's site, own Gram-matrix code);
#  (2) the sites fixed by layers -2..3 must be exactly the rows of the certified cell, and every other site of gaps -4..4 of every
#      continuation must carry a certificate (gaps >= 5 and <= -5 are covered by the zeta certificates and vertical dominance);
#  (3) every certificate is re-checked in exact rationals from its own site references: rows rebuilt as Gram-matrix power differences,
#      y >= 0, sum y_k a_k = c, sum y_k b_k <= beta.
# Usage: python3 verify_lavloc.py pilot|full
import os, sys, json, gzip, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '2026-10-27-splash-rules', 'run2')))
from laves_net import laves
MODE = sys.argv[1] if len(sys.argv) > 1 else 'pilot'
OUT = os.path.normpath(os.path.join(HERE, '..', 'out'))
G = [[Fr(1), Fr(1, 2), Fr(0)], [Fr(1, 2), Fr(1), Fr(0)], [Fr(0), Fr(0), Fr(2, 3)]]      # (x, y, zeta in layer spacings)
def dot(u, v): return sum(G[a][b] * u[a] * v[b] for a in range(3) for b in range(3))
ROLES = ['M0', 'M1', 'K1', 'K2', 'K3', 'T']
LET = 'ABC'

def concrete_word(P):
    """P: m -> letter for m = -4..5 (adjacent distinct); close it into a periodic word starting at layer -4"""
    w = [P[m] for m in range(-4, 6)]
    while True:   # append layers until the last differs from the first and the word is long enough to keep images away
        if len(w) >= 14 and w[-1] != w[0]: break
        w.append(next(x for x in LET if x != w[-1] and (len(w) < 13 or x != w[0])))
    return ''.join(w)

_NETCACHE = {}
def gap_sites_from_net(P):
    key = tuple(sorted(P.items()))
    if key not in _NETCACHE: _NETCACHE[key] = _gap_sites_from_net(P)
    return _NETCACHE[key]

_SPLIT = {}
def split_sites(Q, role):
    """(site i, sites fixed by layers -2..3, all other sites of gaps -4..4) for the concrete continuation Q (cached)"""
    key = (tuple(sorted(Q.items())), role)
    if key not in _SPLIT:
        S = gap_sites_from_net(Q); ci, zi, bi = S[(0, role)]; i = (ci, zi, bi); inside, outside = set(), set()
        for (m, r), (b0, z, b) in S.items():
            T = translates(b0, z, b, ci) - {i}
            (inside if (-2 <= m <= 2 or (m == 3 and r != 'T')) else outside).update(T)
        _SPLIT[key] = (i, inside, outside)
    return _SPLIT[key]

def _gap_sites_from_net(P):
    """{(gap m, role): (lateral base mod 1, height in layer units, big)} for gaps -4..4, from laves_net.laves"""
    word = concrete_word(P); n = len(word); _, big, small = laves(word); out = {}
    for k in range(n):
        m = k - 4
        if m > 4: break
        pts = [(big[2 * k], 1), (big[2 * k + 1], 1)] + [(p, 0) for p in small[4 * k: 4 * k + 4]]
        for r, (p, b) in zip(ROLES, pts):
            out[(m, r)] = ((p[0], p[1]), p[2] * n - 4, b)
    return out

def translates(base, z, b, centre):
    out = set()
    for a1, a2 in itertools.product(range(-4, 5), repeat=2):
        c = (base[0] + a1, base[1] + a2); d = (c[0] - centre[0], c[1] - centre[1], 0)
        if dot(d, d) <= Fr(4, 3): out.add((c, z, b))
    return out

def rebuild(ref):
    return ((Fr(ref[0]), Fr(ref[1])), Fr(ref[2]), int(ref[3]))

def row_gram(i, j):
    """pow_i <= pow_j as (coefficients on (lam, x, y, zeta), right side), via the Gram matrix"""
    (ci, zi, bi), (cj, zj, bj) = i, j
    vi = (ci[0], ci[1], zi); vj = (cj[0], cj[1], zj); d = tuple(vj[a] - vi[a] for a in range(3))
    grad = [2 * sum(G[a][b] * d[b] for b in range(3)) for a in range(3)]
    return [Fr(bj - bi)] + grad, dot(vj, vj) - dot(vi, vi)

def main():
    certs = {}
    with gzip.open(os.path.join(OUT, f'lavloc_{MODE}_certs.jsonl.gz'), 'rt') as f:
        for line in f:
            c = json.loads(line); certs.setdefault(tuple(c['case']), []).append(c)
    rep = json.load(open(os.path.join(OUT, f'lavloc_{MODE}.json')))
    print(f'verify {MODE}: {sum(len(v) for v in certs.values())} certificates in {len(certs)} cases', flush=True)
    ok = badn = 0; cover_ok = cover_bad = 0; problems = []
    for idx, (case, L) in enumerate(sorted(certs.items())):
        lo, hi, role, name = Fr(case[0]), Fr(case[1]), case[2], case[3]
        P = {m - 2: name[m] for m in range(6)}
        # site i and the inside set from the net builder
        rowsites = set()
        for c in L:
            for ref, v in c['y']:
                if ref[0] == 'site': rowsites.add(rebuild(ref[1:]))
        certified = {rebuild(c['j']) for c in L if c['j'] is not None}
        kinds = {c['kind'] for c in L}
        if not {'zeta_hi', 'zeta_lo'} <= kinds: problems.append((case, 'zeta certificate missing')); cover_bad += 1; continue
        insite_all = None
        for ext in itertools.product(LET, repeat=4):
            Q = dict(P); Q[-3], Q[-4], Q[4], Q[5] = ext
            if Q[-3] == Q[-2] or Q[-4] == Q[-3] or Q[4] == Q[3] or Q[5] == Q[4]: continue
            i, inside, outside = split_sites(Q, role)
            if insite_all is None: insite_all = inside
            elif inside != insite_all: problems.append((case, 'inside set depends on the continuation')); cover_bad += 1
            if not rowsites <= inside: problems.append((case, 'certificate uses a row that is not an inside site')); cover_bad += 1
            miss = outside - certified
            if miss: problems.append((case, f'{len(miss)} outside sites without certificate, e.g. {sorted(miss)[0]}')); cover_bad += 1
            else: cover_ok += 1
        # exact re-check of every certificate
        for c in L:
            if c['kind'] == 'zeta_hi': cvec, beta = [Fr(0), Fr(0), Fr(0), Fr(1)], Fr(c['beta'])
            elif c['kind'] == 'zeta_lo': cvec, beta = [Fr(0), Fr(0), Fr(0), Fr(-1)], Fr(c['beta'])
            else: cvec, beta = row_gram(i, rebuild(c['j']))
            if c['kind'] not in ('zeta_hi', 'zeta_lo') and Fr(c['beta']) != beta: problems.append((case, 'beta differs')); badn += 1; continue
            if c['kind'] == 'zeta_hi' and beta != 4 or c['kind'] == 'zeta_lo' and beta != 3: problems.append((case, 'zeta bound weaker than needed')); badn += 1; continue
            s = [Fr(0)] * 4; rhs = Fr(0); good = True
            for ref, v in c['y']:
                v = Fr(v)
                if v < 0: good = False
                if ref[0] == 'site': a, b = row_gram(i, rebuild(ref[1:]))
                elif ref == ['dom', 'lo']: a, b = [Fr(-1), Fr(0), Fr(0), Fr(0)], -lo
                elif ref == ['dom', 'hi']: a, b = [Fr(1), Fr(0), Fr(0), Fr(0)], hi
                else: good = False; continue
                s = [s[r] + v * a[r] for r in range(4)]; rhs += v * b
            good = good and s == cvec and rhs <= beta
            ok += good; badn += not good
            if not good: problems.append((case, 'certificate fails', c['kind'], c['j']))
        if (idx + 1) % 10 == 0 or idx + 1 == len(certs):
            print(f'PROGRESS {(idx + 1) / len(certs):.3f} cases {idx + 1}/{len(certs)}: certificates {ok} ok {badn} bad; coverage {cover_ok} ok {cover_bad} bad', flush=True)
    expect = rep['total_pass']
    print(f'TOTAL certificates re-checked {ok} ok, {badn} bad (lavloc reported {expect} PASS); coverage of every continuation {cover_ok} ok, {cover_bad} bad', flush=True)
    for p in problems[:20]: print('  PROBLEM', p, flush=True)
    # negative check of the checker itself: a tampered certificate must be rejected
    case, L = next(iter(sorted(certs.items()))); c = next(c for c in L if c['j'] is not None)
    lo, hi, role, name = Fr(case[0]), Fr(case[1]), case[2], case[3]
    S = gap_sites_from_net(_fill({m - 2: name[m] for m in range(6)}))
    b0, zi, bi = S[(0, role)]; i = (b0, zi, bi); cvec, beta = row_gram(i, rebuild(c['j']))
    ref, v = c['y'][0]; tam = [[ref, str(Fr(v) * 2)]] + c['y'][1:]
    s = [Fr(0)] * 4; rhs = Fr(0)
    for ref, v in tam:
        v = Fr(v)
        a, b = row_gram(i, rebuild(ref[1:])) if ref[0] == 'site' else (([Fr(-1), 0, 0, 0], -lo) if ref[1] == 'lo' else ([Fr(1), 0, 0, 0], hi))
        s = [s[r] + v * a[r] for r in range(4)]; rhs += v * b
    rejected = not (s == cvec and rhs <= beta)
    print(f'  checker control: tampered certificate (first multiplier doubled) rejected: {rejected}', flush=True)
    good = badn == 0 and cover_bad == 0 and ok == expect and rejected
    print('FINAL ok' if good else 'FINAL FAIL', flush=True)
    sys.exit(0 if good else 1)

def _fill(P):
    P = dict(P)
    P[-3] = next(x for x in LET if x != P[-2]); P[-4] = next(x for x in LET if x != P[-3])
    P[4] = next(x for x in LET if x != P[3]); P[5] = next(x for x in LET if x != P[4])
    return P

if __name__ == '__main__': main()
