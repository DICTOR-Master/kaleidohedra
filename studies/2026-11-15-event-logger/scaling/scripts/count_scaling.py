"""Scaling-state test and Rutenberg-McCurdy count on a froth_scaling.py run (One tissue, three scales; DICTO, 15 Nov 2026).
Rules fixed BEFORE any run (event-logger README, section "Scaling-state froth"):

SCALING TEST on stats.jsonl inside the saved window [win0, win1): split into 4 quarters of equal log t. Stationary if, for every
quarter q against the whole window: |p_q(n) - p(n)| <= 0.015 for n = 3..9; |mu2_q - mu2| <= 0.05; Kolmogorov-Smirnov distance of
the A/<A> distributions <= 0.03; and <A> linear in t: the slope of <A> against t in each quarter within 10% of the slope over the
window. If the window fails, its first quarter is dropped and the test repeated on the rest (at most twice). The count uses only
the part that passes (no count if none passes).
COUNT: scripts/rm_count.py (unchanged) on the saved frames of that part, in consecutive blocks of 500 MCS, at steps 1, 2, 4, 8 MCS
(frames[::s] inside each block), counted swaps W = P = 8 MCS (main) and W = P = 0; rule RM with rc = 1 pixel (main), 0.5, 2;
box = L^2. Block sums are reported; a second pass at step 1 with blocks shifted by 250 MCS measures the block-edge effect.
Usage: count_scaling.py RUNDIR OUT.json [block=500]"""
import sys, os, re, json, gzip, time, math
import numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
import eventlog as EL, pairing as PR, rm_count as RC

RUN, OUT = sys.argv[1], sys.argv[2]
P_ = dict(a.split('=', 1) for a in sys.argv[3:])
BLOCK = int(P_.get('block', 500))
RULES = [(8, 8), (0, 0)]; RCS = (1.0, 0.5, 2.0); STEPS = [1, 2, 4, 8]
TOL_P, TOL_MU2, TOL_KS, TOL_SLOPE = 0.015, 0.05, 0.03, 0.10
fin = json.load(open(os.path.join(RUN, 'final.json'))); prm = fin['params']
L, W0, W1 = prm['L'], prm['win0'], min(prm['win1'], fin['last_mcs'] + 1)
box = float(L * L)
t_start = time.time()
stats = [json.loads(l) for l in open(os.path.join(RUN, 'stats.jsonl'))]


def pdist(rows, ns=range(3, 10)):
    c = Counter(); tot = 0
    for r in rows:
        for k, v in r['p'].items(): c[int(k)] += v
        tot += r['N']
    return {n: c[n] / tot for n in ns}, {int(k): v / tot for k, v in sorted(c.items())}


def cdf(rows):
    h = np.sum([r['area_hist'] + [r['area_over']] for r in rows], 0).astype(float)
    return np.cumsum(h) / h.sum()


def slope(rows):
    t = np.array([r['t'] for r in rows], float); a = np.array([r['Abar'] for r in rows])
    k, c = np.polyfit(t, a, 1)
    return k, c


def test(lo):
    rows = [r for r in stats if lo <= r['t'] < W1]
    ts = np.exp(np.linspace(math.log(lo), math.log(W1), 5))
    qs = [[r for r in rows if ts[i] <= r['t'] < ts[i + 1] or (i == 3 and r['t'] == ts[4])] for i in range(4)]
    p, pfull = pdist(rows); mu2 = float(np.mean([r['mu2'] for r in rows])); C = cdf(rows); k, c = slope(rows)
    out = dict(window=[lo, W1], quarters=[[q[0]['t'], q[-1]['t']] for q in qs], p=p, p_all_n=pfull, mu2=mu2,
               mean_n=float(np.mean([r['mean_n'] for r in rows])), growth_slope=k, t0=-c / k, N_first_last=[rows[0]['N'], rows[-1]['N']],
               Abar_first_last=[rows[0]['Abar'], rows[-1]['Abar']], q=[])
    if 'mu2_n2' in rows[0]:                    # reported beside the test, not part of it (added after the pilot)
        c2 = Counter(); tot = 0
        for r in rows:
            for k_, v in r['p_n2'].items(): c2[int(k_)] += v
            tot += r['N']
        out['n2'] = dict(mu2=float(np.mean([r['mu2_n2'] for r in rows])), mean_n=float(np.mean([r['mean_n2'] for r in rows])),
                         p={k_: round(v / tot, 4) for k_, v in sorted(c2.items())},
                         mu2_quarters=[float(np.mean([r['mu2_n2'] for r in q])) for q in qs])
    ok = True
    for q in qs:
        pq, _ = pdist(q); dp = max(abs(pq[n] - p[n]) for n in p); dmu = abs(float(np.mean([r['mu2'] for r in q])) - mu2)
        ks = float(np.abs(cdf(q) - C).max()); kq, _ = slope(q); ds = abs(kq / k - 1)
        qok = dp <= TOL_P and dmu <= TOL_MU2 and ks <= TOL_KS and ds <= TOL_SLOPE
        ok &= qok
        out['q'].append(dict(max_dp=round(dp, 4), dmu2=round(dmu, 4), ks=round(ks, 4), slope_rel=round(ds, 4), ok=bool(qok),
                             p=pq, mu2=float(np.mean([r['mu2'] for r in q]))))
    # von Neumann tally over the window
    vn = {}
    for r in rows:
        for kk, (cnt, s, s2) in r['vn'].items():
            v = vn.setdefault(int(kk), [0, 0.0, 0.0]); v[0] += cnt; v[1] += s; v[2] += s2
    ks_ = np.array([kk for kk in sorted(vn) if vn[kk][0] >= 50]); ys = np.array([vn[kk][1] / vn[kk][0] for kk in ks_])
    wts = np.array([vn[kk][0] for kk in ks_])
    kv, iv = np.polyfit(ks_, ys, 1, w=np.sqrt(wts))
    out['von_neumann'] = dict(per_n={int(kk): round(float(y), 4) for kk, y in zip(ks_, ys)}, slope=float(kv), n0=float(-iv / kv),
                              growth_over_vn=float(k / kv), RM_growth_over_vn=0.94 / (math.pi / 3))
    out['ok'] = bool(ok)
    return out


tests = []; lo = W0
for _ in range(3):
    r = test(lo); tests.append(r)
    if r['ok']: break
    lo = int(round(r['quarters'][1][0]))
passed = tests[-1] if tests[-1]['ok'] else None
FORCED = P_.get('force') == '1'          # pilot only: count even if the test fails (never in the real runs)
if FORCED and passed is None: passed = tests[0]
res = dict(run=prm, scaling_tests=tests, stationary=any(t_['ok'] for t_ in tests), forced=FORCED, count_window=passed['window'] if passed else None)
print('SCALING ' + json.dumps(dict(tests=[(t_['window'], t_['ok'], [q['ok'] for q in t_['q']], round(t_['mu2'], 4)) for t_ in tests])), flush=True)


def frames_in(lo, hi):
    fr, ar = [], []
    with gzip.open(os.path.join(RUN, 'frames.jsonl.gz'), 'rt') as f, gzip.open(os.path.join(RUN, 'areas.jsonl.gz'), 'rt') as g_:
        for lf, la in zip(f, g_):
            t = int(re.match(r'\{"t": (\d+)', lf).group(1))
            if t < lo: continue
            if t >= hi: break
            fr.append(EL.Tiling.from_json(lf)); ar.append(json.loads(la))
    return fr, ar


def add(acc, r):
    acc['swaps'] += r['swaps']; acc['vanished'] += r['vanished']; acc['ss'] += r['SS']['side_shedding']
    for rc in RCS:
        x = r['RM'][str(rc)]; acc['mac'][rc] += x['macroscopic']
        for k, v in x['sides_at_ell2'].items(): acc['sides'][rc][str(k)] += v


def new_acc():
    return dict(swaps=0, vanished=0, ss=0, mac={rc: 0 for rc in RCS}, sides={rc: Counter() for rc in RCS})


def summ(acc):
    v = acc['vanished']
    out = dict(swaps=acc['swaps'], vanished=v, total_per_T2=round(acc['swaps'] / v, 4) if v else None,
               SS_side_shedding_per_T2=round(acc['ss'] / v, 4) if v else None, RM={})
    for rc in RCS:
        s = acc['sides'][rc]; n345 = sum(s.get(k, 0) for k in s if k != 'never below')
        out['RM'][str(rc)] = dict(macroscopic=acc['mac'][rc], per_T2=round(acc['mac'][rc] / v, 4) if v else None,
                                  microscopic_per_T2=round((acc['swaps'] - acc['mac'][rc]) / v, 4) if v else None,
                                  sides_at_ell2=dict(s),
                                  shares_3_4_5=[round(s.get(str(k), 0) / n345, 4) if n345 else None for k in (3, 4, 5)])
    return out


if passed:
    lo, hi = passed['window']
    edges = list(range(lo, hi, BLOCK))
    blocks = [(a, min(a + BLOCK, hi)) for a in edges if min(a + BLOCK, hi) - a >= BLOCK // 2]
    shifted = [(a + BLOCK // 2, min(a + BLOCK // 2 + BLOCK, hi)) for a in edges if min(a + BLOCK // 2 + BLOCK, hi) - a - BLOCK // 2 >= BLOCK // 2]
    acc = {(s, W): new_acc() for s in STEPS for W, _ in RULES}; per_block = []
    njobs = len(blocks) + len(shifted); done = 0
    for a, b in blocks:
        fr, ar = frames_in(a, b); row = dict(block=[a, b], cells_first_last=[len(fr[0].cells), len(fr[-1].cells)])
        for s in STEPS:
            f_, a_ = fr[::s], ar[::s]; data = PR.collect(f_)
            for W, P in RULES:
                r = RC.rm_count(f_, data, W, P, areas=a_, box=box, rcs=RCS, units='MCS (rc: pixels)')
                assert r['SS']['identity_ok']
                add(acc[(s, W)], r)
                if W == 8: row[f'step{s}'] = dict(vanished=r['vanished'], swaps=r['swaps'],
                                                   RM1_per_T2=r['RM']['1.0']['macroscopic_per_vanished'],
                                                   total_per_T2=r['per_vanished']['total'], ell2=r['RM']['1.0']['ell2_first_last'])
        per_block.append(row); done += 1
        print(f'PROGRESS {done / njobs:.3f} block {a}-{b} step1 RM1/T2 {row["step1"]["RM1_per_T2"]} total/T2 {row["step1"]["total_per_T2"]}', flush=True)
        del fr, ar
    accS = new_acc()
    for a, b in shifted:
        fr, ar = frames_in(a, b); data = PR.collect(fr)
        add(accS, RC.rm_count(fr, data, 8, 8, areas=ar, box=box, rcs=RCS, units='MCS (rc: pixels)'))
        done += 1; print(f'PROGRESS {done / njobs:.3f} shifted block {a}-{b}', flush=True)
        del fr, ar
    res['blocks'] = blocks; res['per_block'] = per_block
    res['sums'] = {f'step{s} W=P={W}': summ(acc[(s, W)]) for s in STEPS for W, _ in RULES}
    res['shifted_step1_W=P=8'] = summ(accS)
res['seconds'] = round(time.time() - t_start, 1)
json.dump(res, open(OUT, 'w'), indent=1, default=str)
if passed:
    for s in STEPS:
        x = res['sums'][f'step{s} W=P=8']
        print(f'step {s}: T2 {x["vanished"]} swaps {x["swaps"]} total/T2 {x["total_per_T2"]} RM macroscopic/T2 rc 1 / 0.5 / 2: '
              + ' / '.join(str(x['RM'][str(rc)]['per_T2']) for rc in (1.0, 0.5, 2.0)) + f'; shares 3/4/5 at l^2 (rc 1) {x["RM"]["1.0"]["shares_3_4_5"]}')
    x = res['shifted_step1_W=P=8']; print(f'shifted blocks step 1: total/T2 {x["total_per_T2"]} RM1/T2 {x["RM"]["1.0"]["per_T2"]}')
print('COUNT_OK' if passed and not FORCED else ('COUNT_FORCED_PILOT' if passed else 'COUNT_NOT_STATIONARY'))
