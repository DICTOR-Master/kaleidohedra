# Square approximants of Ammann-Beenker: t = a/b in [1/2, 1], b <= 40; chambers where every vertex-star count is a linear
# form in (R, Q) = (rhombs, squares) per period. ~/geom/bin/python abfam.py out/
import sys, os, json, random
from fractions import Fraction as Fr
from multiprocessing import Pool
from ab import plane_stats, rnd_gamma

OUT = sys.argv[1]
AB = ['00100101', '00101101', '01011011', '01101111', '01111111', '11111111']
NAME = dict(zip(AB, 'FEDCBA'))

def fitseg(seg, c):
    a = seg[0]
    for b in seg[1:]:
        s = solve2((a['R'], a['Q']), (b['R'], b['Q']), a['stars'].get(c, 0), b['stars'].get(c, 0))
        if s is not None:
            return s if all(x['stars'].get(c, 0) == s[0] * x['R'] + s[1] * x['Q'] for x in seg) else 'bad'
    return None

def solve2(r1, r2, y1, y2):
    d = r1[0] * r2[1] - r1[1] * r2[0]
    if d == 0: return None
    return (Fr(y1 * r2[1] - y2 * r1[1], d), Fr(r1[0] * y2 - r2[0] * y1, d))

if __name__ == '__main__':
    rng = random.Random(31)
    ts = sorted({Fr(a, b) for b in range(1, 41) for a in range(1, b + 1) if Fr(1, 2) <= Fr(a, b) <= 1})
    jobs = [(f't={t}', [t.denominator, t.numerator, 0, -t.numerator], [0, t.numerator, t.denominator, t.numerator], [rnd_gamma(rng) for _ in range(2)]) for t in ts]
    with Pool(22) as pool: res = pool.map(plane_stats, jobs, chunksize=1)
    rows = []
    for t, r in zip(ts, res):
        assert r['ok']
        a = {c: Fr(x) for c, x in r['avg'].items()}
        same = all(x['stars'] == r['runs'][0]['stars'] for x in r['runs']) and all(Fr(r['runs'][0]['stars'].get(c, 0)) == a.get(c, 0) for c in set(a) | set(r['runs'][0]['stars']))
        R = sum(r['pl'][k] for k in ('01', '03', '12', '23')); Q = r['pl']['02'] + r['pl']['13']
        rows.append({'t': t, 'R': R, 'Q': Q, 'N': r['N'], 'stars': a, 'exact_integer_counts': same})
    classes = sorted({c for x in rows for c in x['stars']}, key=lambda c: (c.count('1'), c))
    print('square approximants', len(rows), '; star counts offset-independent and = areas on all:', all(x['exact_integer_counts'] for x in rows))
    print('star classes seen:', classes)
    # greedy chambers: maximal runs of consecutive t on which every class is one linear form in (R, Q)
    ch = []; i = 0
    while i < len(rows):
        j = i + 1
        while j < len(rows):
            seg = rows[i:j + 1]; ok = True
            for c in classes:
                if fitseg(seg, c) == 'bad': ok = False; break
            if not ok: break
            j += 1
        seg = rows[i:j]
        law = {}
        for c in classes:
            law[c] = fitseg(seg, c)
        ch.append((seg[0]['t'], seg[-1]['t'], len(seg), law))
        i = j - 1 if j - 1 > i else j
        if j >= len(rows): break
    for lo, hi, n, law in ch:
        print(f'chamber t in [{lo}, {hi}] ({n} approximants):', '; '.join(f'{NAME.get(c, c)} {s[0]}R{"+" if s[1] >= 0 else ""}{s[1]}Q' for c, s in law.items() if s and (s[0] or s[1])))
    json.dump({'rows': [{'t': str(x['t']), 'R': x['R'], 'Q': x['Q'], 'N': x['N'], 'stars': {c: str(v) for c, v in x['stars'].items()}, 'exact': x['exact_integer_counts']} for x in rows],
               'chambers': [{'lo': str(lo), 'hi': str(hi), 'n': n, 'law': {c: [str(s[0]), str(s[1])] if s else None for c, s in law.items()}} for lo, hi, n, law in ch]},
              open(os.path.join(OUT, 'abfam.json'), 'w'), indent=0)
    # ---- window grows: edges by the stars at their two ends (offset-independent?) and the chamber around 1/sqrt2
    erows = []
    for t, r in zip(ts, res):
        R = sum(r['pl'][k] for k in ('01', '03', '12', '23')); Q = r['pl']['02'] + r['pl']['13']
        same = all(x['edges'] == r['runs'][0]['edges'] for x in r['runs'])
        erows.append({'t': t, 'R': R, 'Q': Q, 'stars': {k: Fr(v) for k, v in r['runs'][0]['edges'].items()}, 'same': same})
    print('edge counts by end stars offset-independent on all square approximants:', all(x['same'] for x in erows))
    ek = sorted({k for x in erows for k in x['stars']})
    import math
    s2 = Fr(70, 99)  # inside every chamber that contains 1/sqrt2 down to the resolution used here
    i0 = max(i for i, x in enumerate(erows) if x['t'] <= Fr(29, 41))
    best = None
    for lo in range(i0, -1, -1):
        for hi in range(i0 + 1, len(erows)):
            seg = erows[lo:hi + 1]
            if all(fitseg(seg, k) != 'bad' for k in ek):
                if best is None or (hi - lo) > best[1] - best[0]: best = (lo, hi)
    lo, hi = best
    seg = erows[lo:hi + 1]
    print(f'edges by end stars: largest chamber around 1/sqrt2 with every count a line in (R, Q): t in [{seg[0]["t"]}, {seg[-1]["t"]}] ({len(seg)} approximants)')
    for k in ek:
        s = fitseg(seg, k)
        if s and (s[0] or s[1]):
            print('   ', '|'.join(NAME.get(c, c) for c in k.split('|')), f'{s[0]}R{"+" if s[1] >= 0 else ""}{s[1]}Q')
    # ---- the defect transfer: outside the chamber every count = chamber line + kappa_c * X, X = number of defect stars
    from qf import QF
    mid = {'00100101': (0, 1), '00101101': (2, -2), '01011011': (-4, 6), '01101111': (10, -14), '01111111': (-12, 17), '11111111': (5, -7), '01011111': (0, 0)}
    kappa = {'00100101': 0, '00101101': 0, '01011011': -1, '01101111': 2, '01111111': -3, '11111111': 1, '01011111': 1}
    lim = {'00100101': QF(-1, 1, 2), '00101101': QF(6, -4, 2), '01011011': QF(-14, 10, 2), '01101111': QF(34, -24, 2), '01111111': QF(-41, 29, 2), '11111111': QF(17, -12, 2)}
    for c, v in lim.items():   # the AB value lies on every chamber line: per vertex R/N = 2 - sqrt2, Q/N = sqrt2 - 1
        assert mid[c][0] * QF(2, -1, 2) + mid[c][1] * QF(-1, 1, 2) == v
    print('the Ammann-Beenker frequencies lie on all six chamber lines (exact in Q(sqrt2))')
    nchk = 0
    for x in rows:
        a, b = x['t'].numerator, x['t'].denominator
        Nu = b * b + 4 * a * b + 2 * a * a
        X = 2 * (3 * a - 2 * b) ** 2 if x['t'] < Fr(2, 3) else ((4 * a - 3 * b) ** 2 if x['t'] > Fr(3, 4) else 0)
        Ru, Qu = 4 * a * b, b * b + 2 * a * a
        assert Fr(x['R'] * Nu, x['N']) == Ru and Fr(x['Q'] * Nu, x['N']) == Qu
        for c in classes:
            assert x['stars'].get(c, 0) * Fr(Nu, x['N']) == mid[c][0] * Ru + mid[c][1] * Qu + kappa[c] * X, (x['t'], c)
            nchk += 1
    print('defect transfer checked on all', len(rows), 'square approximants (', nchk, 'counts): count = line(R, Q) + kappa X, kappa (F,E,D,C,B,A,defect) = 0,0,-1,+2,-3,+1,+1;',
          'X = 2(3a-2b)^2 for t < 2/3, (4a-3b)^2 for t > 3/4, per cell of N_u = b^2+4ab+2a^2 vertices')
