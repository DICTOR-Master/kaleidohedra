"""The n-triangle yantras of the traditional apex-on-base pattern, n = 3, 5, 7, 9 (17 Nov 2026).

The pattern (from #103 (i)): the apex-on-base relation is one alternating chain
    t4 -> t8 -> t1 -> t6 -> t2 -> t9 -> t3 -> T     and     t5 -> t7 -> O
(down, up, down, ... each apex resting on the next triangle's base; t3 and t7 the two great triangles).
Taking off one up-and-down pair at a time while every remaining apex still rests on a remaining base
can be done in exactly one way: (t4, t8), then (t1, t6), then (t2, t9), leaving t3, t5, t7.
The n-triangle pattern (n = 3, 5, 7, 9) keeps the triangles that remain, their apex-on-base relations,
the order of their base levels, the two great triangles inscribed, and every marma and corner touch of
#103 (ii), (iii) among them (Chiodo's conditions restricted to them).  Free parameters (rational):
  n = 3: u, v, b5, w5                      t3, t5, t7
  n = 5: u, v, S, b2, b5, w5               + t2, t9          marmas (2,3,7), (2,7,9)
  n = 7: u, v, Q, S, b1, b2                + t1, t6          + (1,2,7), (1,5,9); corners (5,5,6), (2,6,6)
  n = 9: u, v, Q, S (Chiodo's family, model.py; closing quadratic, coordinates in Q(sqrt Delta))
Every sample is checked: all retained conditions vanish exactly; admissible as in #103 Theorem 1
(bases strictly in the pattern's order, half-widths > 0, apexes on the right side, corners in the
closed disc).  Counts by yarr.py (exact arithmetic).
usage: python3 family.py <study dir> <samples per n> [seed]"""
import sys, os, json, random, math, time
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yarr import Arr, QF
import model as M

ST = sys.argv[1]
NS = int(sys.argv[2])
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 20261117

ORDER = {3: [3, 5, 7], 5: [2, 3, 5, 7, 9], 7: [1, 2, 3, 5, 6, 7, 9], 9: list(range(1, 10))}
APEX_ON_BASE = {3: [(5, 7)], 5: [(5, 7), (9, 3), (2, 9)], 7: [(5, 7), (9, 3), (2, 9), (6, 2), (1, 6)],
                9: M.APEX_ON_BASE + [(5, 7)]}
MARMAS = {3: [], 5: [(2, 3, 7), (2, 7, 9)], 7: [(2, 3, 7), (2, 7, 9), (1, 2, 7), (1, 5, 9)], 9: M.MARMAS}
CORNERS = {3: [], 5: [], 7: [(5, 5, 6), (2, 6, 6)], 9: M.CORNERS}
DOWN = {1, 2, 3, 4, 5}


def great(u, v):
    P = v * v / (1 + v * v); w3 = v / (1 + v * v)
    R = 1 / (1 + u * u); w7 = u / (1 + u * u)
    return P, w3, R, w7


def build(n, p):
    if n == 9:
        u, v, Q, S, root = p
        P, w3, R, w7 = great(u, v)
        def sq(z):
            num, den = Fr(z).numerator, Fr(z).denominator
            if num >= 0 and math.isqrt(num) ** 2 == num and math.isqrt(den) ** 2 == den:
                return Fr(math.isqrt(num), math.isqrt(den))
            QF.D = Fr(z)
            return QF(0, 1)
        disc0 = M.solve(P, Q, R, S, w3, w7, lambda z: Fr(0), 0, b1=Fr(0))['disc']
        if disc0 < 0:
            return None
        y = M.solve(P, Q, R, S, w3, w7, sq, root)
        return {'b': y['b'], 'w': y['w'], 'a': y['a']}
    u, v = p[0], p[1]
    P, w3, R, w7 = great(u, v)
    b = {3: P, 7: R}; w = {3: w3, 7: w7}; a = {3: Fr(1), 7: Fr(0)}
    k7 = w7 / R
    if n == 3:
        b5, w5 = p[2], p[3]
    else:
        S = p[2] if n == 5 else p[3]
        xW = k7 * P
        xX = xW * (S - R) / (S - P); k9 = xX / (R - P)
        b[9], w[9], a[9] = S, k9 * (S - P), P
        if n == 5:
            b2, b5, w5 = p[3], p[4], p[5]
        else:
            Q, b1, b2 = p[2], p[4], p[5]
        b[2], w[2], a[2] = b2, xW * (S - b2) / (S - P), S
        if n == 7:
            w6 = xW * (S - Q) / (S - P)
            b[6], w[6], a[6] = Q, w6, b2
            m1 = k7 * b2 / (Q - b2)
            b[1], w[1], a[1] = b1, m1 * (Q - b1), Q
            b5 = (m1 * Q + k9 * P) / (m1 + k9)
            w5 = w6 * (b5 - b2) / (Q - b2)
    b[5], w[5], a[5] = b5, w5, R
    return {'b': b, 'w': w, 'a': a}


def admissible(n, y):
    b, w, a = y['b'], y['w'], y['a']
    o = ORDER[n]
    if not all(b[o[k]] < b[o[k + 1]] for k in range(len(o) - 1)):
        return False
    if not all(w[i] > 0 for i in o):
        return False
    if not all((a[i] > b[i]) if i in DOWN else (a[i] < b[i]) for i in o):
        return False
    return all(w[i] * w[i] + b[i] * b[i] - b[i] <= 0 for i in o)


def conditions(n, y):
    out = []
    for i in (3, 7):
        out.append(y['w'][i] ** 2 + y['b'][i] ** 2 - y['b'][i])
    for p, q in APEX_ON_BASE[n]:
        out.append(y['a'][p] - y['b'][q])
    for p, q, r in MARMAS[n] + CORNERS[n]:
        out.append(M.det3(M.leg(y, p), M.base(y, q), M.leg(y, r)))
    return all(not z for z in out) if out else True


def rfrac(rng, lo, hi, den=97):
    q = rng.randint(7, den)
    return Fr(rng.randint(math.ceil(lo * q), math.floor(hi * q)), q)


def sample(n, rng):
    u, v = rfrac(rng, 0.45, 1.1), rfrac(rng, 0.45, 1.1)
    P, w3, R, w7 = great(u, v)
    if n == 9:
        return (u, v, rfrac(rng, 0.40, 0.75), rfrac(rng, 0.75, 0.999), rng.randint(0, 1))
    if n == 3:
        b5 = P + (R - P) * rfrac(rng, 0.02, 0.98)
        return (u, v, b5, rfrac(rng, 0.01, 0.5))
    S = rfrac(rng, max(float(R), 0.6) + 0.001, 0.999)
    if n == 5:
        b2 = P * rfrac(rng, 0.05, 0.98)
        b5 = P + (R - P) * rfrac(rng, 0.02, 0.98)
        return (u, v, S, b2, b5, rfrac(rng, 0.01, 0.5))
    Q = rfrac(rng, 0.40, 0.75)
    b2 = P * rfrac(rng, 0.2, 0.98)
    b1 = b2 * rfrac(rng, 0.02, 0.98)
    return (u, v, Q, S, b1, b2)


def job(arg):
    n, k = arg
    rng = random.Random(SEED * 1000 + n * 100003 + k)
    tries = 0
    while True:
        tries += 1
        p = sample(n, rng)
        try:
            y = build(n, p)
        except ZeroDivisionError:
            continue
        if y is None or not admissible(n, y):
            continue
        assert conditions(n, y), ('condition fails', n, p)
        o = ORDER[n]
        T = [(y['b'][i], y['w'][i], y['a'][i]) for i in o]
        r = Arr(T).analyse()
        r.pop('area2')
        r['params'] = [str(z) for z in p]
        r['tries'] = tries
        if n == 9:
            r['Delta_square'] = not isinstance(y['b'][1], QF)
        return n, r


if __name__ == '__main__':
    t0 = time.time()
    tasks = [(n, k) for n in (3, 5, 7, 9) for k in range(NS)]
    with Pool(4) as pool:
        out = pool.map(job, tasks, chunksize=4)
    res = {n: [r for m, r in out if m == n] for n in (3, 5, 7, 9)}
    summ = {}
    ok = True
    for n in (3, 5, 7, 9):
        rs = res[n]
        dist = {}
        for r in rs:
            key = (r['odd'], tuple(r['rings'].get(c, 0) for c in range(1, n + 1, 2)), r['odd_tri'], r['odd_quad'],
                   r['star'], tuple(r['star_by']), r['faces'], r['tri'], r['quad'], r['other'])
            dist.setdefault(key, []).append(r['params'])
        summ[n] = [dict(odd=k[0], odd_rings=k[1], odd_tri=k[2], odd_quad=k[3], star=k[4], star_by=k[5], faces=k[6],
                        tri=k[7], quad=k[8], other=k[9], samples=len(v), example=v[0]) for k, v in
                   sorted(dist.items(), key=lambda kv: -len(kv[1]))]
        print(f"n = {n}: {len(rs)} admissible samples, {len(dist)} distinct count patterns", flush=True)
        for s in summ[n][:12]:
            print(f"   {s['samples']:5d} x  odd {s['odd']} {s['odd_rings']} ({s['odd_tri']} tri, {s['odd_quad']} four-sided)"
                  f"  star {s['star']} {s['star_by']}  all regions {s['faces']} = {s['tri']} tri + {s['quad']} four + {s['other']} other",
                  flush=True)
        ok = ok and len(rs) == NS
    json.dump({'seed': SEED, 'samples_per_n': NS, 'summary': summ, 'raw': res},
              open(os.path.join(ST, 'data', f'family-n3-9-seed{SEED}.json'), 'w'), indent=0, default=str)
    print(f"time {time.time() - t0:.0f} s")
    # n = 9 must contain the traditional 43 (the DICTO Yantra's pattern) among its values
    ok = ok and any(s['odd'] == 43 and s['odd_rings'] == (14, 10, 10, 8, 1) for s in summ[9])
    print("FINAL ok" if ok else "FINAL FAIL (missing samples or no 43 at n = 9)")
