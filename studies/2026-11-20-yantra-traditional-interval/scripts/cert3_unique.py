"""Certificate 3: for every u in [U0, U1] the rhombus member of certificate 1 is the ONLY admissible (b), (c) yantra with u = v.

Every admissible (b), (c) yantra with u = v solves G = 0 and H1 = 0 in the census unknowns (t, S) (the divisor lemma of #103
Theorem 15's census, generic u, v: study 2026-11-20-cleo-antonius-selection, s0_generic.py), with
  S in (R, 1)   (b7 < b9 < 1),   t in (0, u)   (t = b1/w1 > 0 since w1 > 0; b1 < b3 gives t^2/(1+t^2) < u^2/(1+u^2)).
On each u-box U (ball arithmetic, Arb, 256 bits):
 (1) G, quadratic in S, has exactly one root in (R, 1); the other is certified outside [R, 1] (ycert.S_branch);
 (2) the branch box T_b: exactly one root of H1 in T_b for every (u, S) of the box (parametric interval Newton, ycert.branch);
 (3) [0, u_max] minus T_b is cut into t-boxes (bisection) and each is closed by one test: H1 has no zero on (U, T, S-box)
     (centred form), or the yantra built from (U, T, S-box) breaks one admissibility condition on the whole box (a strict
     condition <= 0, or a corner of t2, t4, t5, t6, t8 strictly outside the disc), or t > u on the whole box.
So for every u in [U0, U1] the admissible solutions are exactly the branch.
usage: python -u cert3_unique.py U0 U1 NB [TDEPTH]"""
import sys, os, json, time
from multiprocessing import Pool
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import flint
from flint import arb, fmpq
flint.ctx.prec = 256
import ycert as Y
from cert1_sweep import tguess


def violated(y, U, T):
    """True if the yantra of the box certainly breaks an admissibility condition (or t > u) everywhere on the box."""
    if T.lower() > U.upper(): return 't > u'
    b, w, a = y['b'], y['w'], y['a']
    qs = [(f'b{i}<b{i+1}', b[i + 1] - b[i]) for i in range(1, 9)] + [('b9<1', 1 - b[9])] + [(f'w{i}>0', w[i]) for i in range(1, 10)]
    qs += [(f'apex t{i}', (a[i] - b[i]) if i in Y.DOWN else (b[i] - a[i])) for i in range(1, 10) if i not in (3, 7)]
    for nm, q in qs:
        if q.is_finite() and q <= 0: return nm
    for i in (2, 4, 5, 6, 8):
        q = w[i] * w[i] + b[i] * b[i] - b[i]
        if q.is_finite() and q > 0: return f't{i} corner outside'
    return None


def check_u(a, b, tdepth):
    U = arb(a).union(arb(b)); um = arb(U.mid())
    try:
        Sb, Tb, tm = Y.branch(U, tguess(float(U.mid())))
        Sm = Y.S_branch(um)
    except (ValueError, ZeroDivisionError) as e:
        return False, 'branch: ' + str(e), {}
    ranges = [(arb(0), arb(Tb.lower())), (arb(Tb.upper()), arb(U.upper()))]
    stats = {'H1 nonzero': 0}; stack = [(lo, hi, 0) for lo, hi in ranges]
    while stack:
        lo, hi, d = stack.pop()
        T = lo.union(hi); tmid = arb(T.mid())
        h = Y.cp(Y.H1, (um, tmid, Sm), (U, T, Sb))
        if not h.contains(0): stats['H1 nonzero'] += 1; continue
        try:
            why = violated(Y.build(U, T, Sb), U, T)
        except ZeroDivisionError:
            why = None
        if why: stats[why] = stats.get(why, 0) + 1; continue
        if d >= tdepth: return False, f't-box [{lo.str(8)}, {hi.str(8)}] not closed', stats
        stack += [(lo, tmid, d + 1), (tmid, hi, d + 1)]
    return True, '', stats


def job(args):
    flint.ctx.prec = 256
    a, b, depth, dmax, tdepth = args
    out = []; stack = [(a, b, depth)]
    while stack:
        a, b, d = stack.pop()
        ok, why, st = check_u(a, b, tdepth)
        if not ok and d < dmax:
            mid = (a + b) / 2; stack += [(mid, b, d + 1), (a, mid, d + 1)]; continue
        out.append(dict(a=str(a), b=str(b), depth=d, ok=ok, why=why, closed=st))
    return out


if __name__ == '__main__':
    def rq(s): n, dd = s.split('/'); return fmpq(int(n), int(dd))
    U0, U1, NB = rq(sys.argv[1]), rq(sys.argv[2]), int(sys.argv[3]); TD = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    h = (U1 - U0) / NB
    tasks = [(U0 + k * h, U0 + (k + 1) * h, 0, 6, TD) for k in range(NB)]
    say(f'uniqueness: u in [{U0}, {U1}], {NB} u-boxes, t-bisection depth up to {TD}')
    res = []; t1 = time.time()
    with Pool(int(os.environ.get('NPROC', '22'))) as pool:
        for k, r in enumerate(pool.imap(job, tasks, chunksize=1)):
            res += r
            if time.time() - t1 > 30: say(f'PROGRESS {(k + 1) / NB:.3f}'); t1 = time.time()
    res.sort(key=lambda z: rq(z['a']))
    cover = all(rq(x['b']) == rq(y_['a']) for x, y_ in zip(res, res[1:])) and rq(res[0]['a']) == U0 and rq(res[-1]['b']) == U1
    fails = [x for x in res if not x['ok']]
    tot = {}
    for x in res:
        for k_, v in x['closed'].items(): tot[k_] = tot.get(k_, 0) + v
    say(f'{len(res)} u-boxes, contiguous cover: {cover}; failures {len(fails)}; t-boxes closed by each test: {dict(sorted(tot.items(), key=lambda z: -z[1]))}')
    for x in fails[:10]: say('  FAIL', x)
    tag = f'{sys.argv[1]}-{sys.argv[2]}'.replace('/', '_')
    json.dump(dict(U0=str(U0), U1=str(U1), boxes=res, closed_by=tot), open(os.path.join(ROOT, 'data', f'unique-{tag}.json'), 'w'))
    print('FINAL ok' if cover and not fails else f'FINAL FAIL: cover {cover}, failures {len(fails)}')
