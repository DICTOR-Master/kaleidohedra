"""Certificate 1: the certified sweep along the rhombus branch, u in [U0, U1] (c = u^2).

The interval [U0, U1] is cut into NB boxes with rational ends (bisected up to DMAX times where a test is not yet decided).
On each box U = m +- r, in ball arithmetic (Arb, 256 bits):
 (1) the branch: S in (R, 1) from G (the other root of G certified outside [R, 1]); t by parametric interval Newton: exactly one
     root of H1 in the t-box for every (u, S) of the box (ycert.branch);
 (2) every coordinate, side and triple determinant is enclosed by the centred form f(m) + f'(box) [-r, r], with f' carried by
     forward differentiation in u through the whole construction (t' and S' by implicit differentiation of H1 and G);
 (3) admissibility (#103 Theorem 1), strictly: bases ordered, b9 < 1, half-widths > 0, apexes on the right side, the corners of
     t2, t4, t5, t6, t8 strictly inside the disc (t1, t3, t7, t9 have their corners on the circle by construction);
 (4) every triple of the 27 lines other than the 115 identities (certificate 0) either has a determinant of fixed sign on the box,
     or its meeting point is certified off one of the three drawn sides (a parameter outside [0, 1]). The six threshold triples
     (t4's leg with two of t5's base, t5's leg and t6's leg, and the mirror images) are excused only on a box that contains one
     end of the window (u_lo or u*, as isolated in data/window-exact.json) in its interior, and only when the derivative of
     C = det(R4, B5, R6) along the branch has a fixed sign on the box (one zero at most), with B5, R5, R6 pairwise not parallel.
The arrangement of the 27 drawn sides changes only at such a concurrency on all three closed sides; so the counts are constant
on every stretch of [U0, U1] between the window ends. Certificate 2 places the zero of C on the end box at the end exactly.
usage: python -u cert1_sweep.py U0 U1 NB [DMAX]      (U0, U1 rationals such as 29/50; prints FINAL ok / FINAL FAIL)"""
import sys, os, json, time
from multiprocessing import Pool
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import flint
from flint import arb, fmpq
flint.ctx.prec = 256
import ycert as Y
from ycert import AD

IDENT = {tuple(s.split('-')) for s in json.load(open(os.path.join(ROOT, 'data', 'identities.json')))['identities']}
IDENT = {tuple(sorted(t)) for t in IDENT}
assert len(IDENT) == 115
PAR = [tuple(s.split('-')) for s in json.load(open(os.path.join(ROOT, 'data', 'identities.json')))['parallel_pairs']]
assert len(PAR) == 2
def has_par(tr): return any(p_ in tr and q_ in tr for p_, q_ in PAR)
TRIPLES = [tuple(sorted(t)) for t in Y.TRIPLES]
WIN = json.load(open(os.path.join(ROOT, 'data', 'window-exact.json')))
def q(s):
    n, d = s.split('/'); return fmpq(int(n), 10 ** int(d.split('^')[1]) if '^' in d else int(d))
ENDS = []                                   # u-intervals holding the two window ends: u = sqrt(c), c in the isolating interval
for lo, hi, n in WIN['c_intervals']:
    assert n == 1
    ENDS.append(arb(q(lo)).sqrt().union(arb(q(hi)).sqrt()))
# t near the branch (exploration values, only a starting guess for Newton; a wrong root fails admissibility)
TAB = [(0.55, 0.0610846), (0.58, 0.0820131), (0.588, 0.0885323), (0.6, 0.0991359), (0.62, 0.119191), (0.65, 0.155504), (0.68, 0.200148),
       (0.7, 0.234834), (0.72, 0.273467), (0.74, 0.315856), (0.746, 0.329255), (0.75, 0.338352), (0.7505, 0.339498), (0.76, 0.361636)]
def tguess(u):
    for (a, ta), (b, tb) in zip(TAB, TAB[1:]):
        if a <= u <= b: return ta + (tb - ta) * (u - a) / (b - a)
    raise ValueError('u outside the table')


def check_box(a, b):
    """Returns (ok, why, info) for the u-box [a, b] (fmpq)."""
    U = arb(a).union(arb(b)); m = arb(U.mid()); r = arb(U.rad())
    tg = tguess(float(U.mid()))
    try:
        Sm, Tm, _ = Y.branch(m, tg)
        Sb, Tb, _ = Y.branch(U, tg)
    except (ValueError, ZeroDivisionError) as e:
        return False, 'branch: ' + str(e), None
    yP = Y.build(m, Tm, Sm)
    Sd, td = Y.branch_derivs(U, Tb, Sb, (m, Tm, Sm))
    yB = Y.build(AD(U, arb(1)), AD(Tb, td), AD(Sb, Sd))
    enc = lambda fm, fB: fm + fB.d * arb(0, r)
    info = {'adm_min': None, 'det_min': None, 'thr': False}
    # (3) admissibility
    for (nm, qp), (_, qb) in zip(Y.admissibility(yP), Y.admissibility(yB)):
        e = enc(qp, qb)
        if not e > 0: return False, 'admissibility ' + nm, None
        lw = e.lower(); info['adm_min'] = lw if info['adm_min'] is None or lw < info['adm_min'] else info['adm_min']
    # (4) triples
    SP, SB = Y.segments(yP), Y.segments(yB)
    LP = {n: Y.lc(s) for n, s in SP.items()}; LB = {n: Y.lc(s) for n, s in SB.items()}
    thr_zero = []
    for tr in TRIPLES:
        if tr in IDENT: continue
        dP = Y.det3(*(LP[n] for n in tr)); dB = Y.det3(*(LB[n] for n in tr))
        e = enc(dP, dB)
        if not e.contains(0):
            lw = abs(e).lower(); info['det_min'] = lw if info['det_min'] is None or lw < info['det_min'] else info['det_min']
            if tr == Y.C_TRIPLE: info['C_sign'] = 1 if e > 0 else -1
            continue
        if tr in Y.THRESH: thr_zero.append((tr, dB)); continue
        if has_par(tr):                                  # two distinct parallel lines never meet: no finite concurrency
            info['par_excused'] = info.get('par_excused', 0) + 1; continue
        off = False
        for rot in (tr, (tr[1], tr[2], tr[0]), (tr[2], tr[0], tr[1])):
            try:
                pP = Y.meet_params([SP[n] for n in rot]); pB = Y.meet_params([SB[n] for n in rot])
            except ZeroDivisionError:
                continue
            for x, xb in zip(pP, pB):
                ex = enc(x, xb)
                if ex.is_finite() and (ex < 0 or ex > 1): off = True; break
            if off: break
        if not off: return False, 'triple ' + '-'.join(tr), None
    if thr_zero:
        holds = [k for k, E in enumerate(ENDS) if U.lower() < E.lower() and E.upper() < U.upper()]
        if len(holds) != 1: return False, 'threshold triple may vanish on a box that holds no window end', None
        dC = [dB for tr, dB in thr_zero if tr == Y.C_TRIPLE]
        if not dC: return False, 'threshold: C itself certified nonzero on an end box (unexpected)', None
        if dC[0].d.contains(0): return False, 'threshold: dC/du contains 0', None
        mono = all(not dB.d.contains(0) for tr, dB in thr_zero)
        dirs = {n: (SB[n][1][0] - SB[n][0][0], SB[n][1][1] - SB[n][0][1]) for n in ('B5', 'R5', 'R6', 'L5', 'L6')}
        def cross(p, q_): return (dirs[p][0] * dirs[q_][1] - dirs[p][1] * dirs[q_][0]).v
        if any(cross(p, q_).contains(0) for p, q_ in [('B5', 'R5'), ('B5', 'R6'), ('R5', 'R6'), ('B5', 'L5'), ('B5', 'L6'), ('L5', 'L6')]):
            return False, 'threshold: two of B5, R5, R6 (or mirrors) may be parallel', None
        info.update(thr=True, end=holds[0], dC_sign=1 if dC[0].d > 0 else -1, all6_monotone=mono, n_thr=len(thr_zero))
    return True, '', info


def job(args):
    flint.ctx.prec = 256
    a, b, depth, dmax = args
    out = []; stack = [(a, b, depth)]
    while stack:
        a, b, d = stack.pop()
        ok, why, info = check_box(a, b)
        if not ok and d < dmax:
            mid = (a + b) / 2; stack += [(mid, b, d + 1), (a, mid, d + 1)]; continue
        out.append(dict(a=str(a), b=str(b), depth=d, ok=ok, why=why,
                        **({} if info is None else {k: (arb(v).str(4, radius=False) if isinstance(v, arb) else v) for k, v in info.items()})))
    return out


if __name__ == '__main__':
    def rq(s): n, dd = s.split('/'); return fmpq(int(n), int(dd))
    U0, U1, NB = rq(sys.argv[1]), rq(sys.argv[2]), int(sys.argv[3]); DMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    h = (U1 - U0) / NB
    tasks = [(U0 + k * h, U0 + (k + 1) * h, 0, DMAX) for k in range(NB)]
    say(f'sweep u in [{U0}, {U1}] = c in [{float(U0) ** 2:.6f}, {float(U1) ** 2:.6f}], {NB} boxes of width {h}, up to {DMAX} bisections; '
        f'window ends u_lo in {ENDS[0].str(12)}, u* in {ENDS[1].str(12)}')
    res = []; t1 = time.time()
    with Pool(int(os.environ.get('NPROC', '22'))) as pool:
        for k, r in enumerate(pool.imap(job, tasks, chunksize=1)):
            res += r
            if time.time() - t1 > 30: say(f'PROGRESS {(k + 1) / NB:.3f} boxes done {len(res)}'); t1 = time.time()
    res.sort(key=lambda z: rq(z['a']))
    cover = all(rq(x['b']) == rq(y_['a']) for x, y_ in zip(res, res[1:])) and rq(res[0]['a']) == U0 and rq(res[-1]['b']) == U1
    fails = [x for x in res if not x['ok']]
    thr = [x for x in res if x.get('thr')]
    say(f'{len(res)} boxes (deepest bisection {max(x["depth"] for x in res)}), contiguous cover of [U0, U1]: {cover}; failures {len(fails)}')
    for x in thr: say(f'  end box [{x["a"]}, {x["b"]}] holds window end {x["end"]}: dC/du sign {x["dC_sign"]}, all six threshold triples monotone {x["all6_monotone"]}')
    signs = {}
    for x in res:
        if 'C_sign' in x: signs.setdefault(x['C_sign'], []).append(float(rq(x['a'])))
    for s_, v in signs.items(): say(f'  C sign {s_:+d} on boxes from u = {min(v):.6f} to {max(v):.6f} ({len(v)} boxes)')
    pe = [x for x in res if x.get('par_excused')]
    if pe: say(f'  {len(pe)} boxes where a triple holding two opposite rhombus sides (parallel, distinct) may vanish: excused, no finite meeting; u from {min(float(rq(x["a"])) for x in pe):.6f} to {max(float(rq(x["b"])) for x in pe):.6f}')
    mins = [float(x['det_min']) for x in res if x.get('det_min')]; amins = [float(x['adm_min']) for x in res if x.get('adm_min')]
    if res and mins: say(f'  smallest certified |det| over all boxes {min(mins):.3e}; smallest admissibility slack {min(amins):.3e}')
    for x in fails[:10]: say('  FAIL', x)
    tag = f'{sys.argv[1]}-{sys.argv[2]}'.replace('/', '_')
    json.dump(dict(U0=str(U0), U1=str(U1), NB=NB, boxes=res), open(os.path.join(ROOT, 'data', f'sweep-{tag}.json'), 'w'))
    print('FINAL ok' if cover and not fails else f'FINAL FAIL: cover {cover}, failures {len(fails)}')
