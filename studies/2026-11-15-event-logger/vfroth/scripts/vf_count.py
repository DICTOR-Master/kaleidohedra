"""Count and law checks for the law-built froth (vfroth.py runs), pooled over the runs of one size. Rules fixed before any run.

WINDOW (fixed in advance, 16 Nov 2026, before any production run): from the first record with <A> >= 4 (four times the initial mean
area) to the last record with N >= 100 (Rutenberg & McCurdy see finite-size effects below about 100 bubbles), per run. SCALING TEST (the rule of the Potts scaling-state study, count_scaling.py, unchanged in its tolerances): the
window is cut into four quarters of equal log t; it is stationary if, for every quarter against the whole window (records pooled
over the runs): |p_q(n) - p(n)| <= 0.015 for n = 3..9; |mu2_q - mu2| <= 0.05; Kolmogorov-Smirnov distance of the A/<A>
distributions <= 0.03; and the slope of <A> against t within 10% of the window's (mean over runs). On failure the first quarter is
dropped and the test repeated (at most twice). Only the passing window is counted.
COUNT (Rutenberg & McCurdy's own rule, arXiv cond-mat/0502287 section III C): a T1 is macroscopic at cut-off c if all four bubbles
are larger than l^2 = c rc L(t), L = sqrt(<A>), at the event; T2 = every bubble that vanishes (T2_n and T2side). c = 0.5, 1 (main),
2. Error: Poisson on the macroscopic count, and the spread between runs. T2 shares: the sides of each bubble as its area falls past
l^2 (c = 1), for bubbles that vanish inside the window.
LAWS: per record, the largest deviation from 120 degrees, the largest |geometric gas flux - (pi/3)(n - 6)| and the regression of flux
on n (slope, zero); mu2; E / E_hex; growth of <A> over the von Neumann coefficient pi/3; Lewis and Aboav-Weaire fits on the window's
snapshots with tissue_stats() of the tissue-null-models study (nulllib.py, reused unchanged).
Usage: vf_count.py OUT.json RUNDIR [RUNDIR ...]    |    vf_count.py --selftest"""
import sys, os, json, math, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '2026-11-15-tissue-null-models', 'scripts'))
from nulllib import tissue_stats

CS = (0.5, 1.0, 2.0)
TOL_P, TOL_MU2, TOL_KS, TOL_SLOPE = 0.015, 0.05, 0.03, 0.10
AWIN0 = 4.0; NWIN_END = 100

def macro_count(t1, t2, rc, c):
    """t1: list of events [t, 'T1', P, Q, R, S, AP, AQ, AR, AS, Abar]; returns the number whose four areas exceed c rc sqrt(Abar)."""
    return sum(1 for e in t1 if min(e[6:10]) > c * rc * math.sqrt(e[10]))

def selftest():
    """Known answer: rc = 0.01, <A> = 100 (l^2 = c * 0.1). Event a: areas 5, 6, 7, 8 -> macroscopic at every c. Event b: one area
    0.09 -> microscopic at c = 1 (0.1) and 2, macroscopic at c = 0.5 (0.05). Event c: one area exactly 0.1 -> NOT macroscopic at
    c = 1 (strictly larger required). Negative: a rule that ignores the areas must count 3 at c = 2 and so fail."""
    t1 = [[0, 'T1', 1, 2, 3, 4, 5, 6, 7, 8, 100.0], [0, 'T1', 1, 2, 3, 4, 0.09, 6, 7, 8, 100.0], [0, 'T1', 1, 2, 3, 4, 5, 0.1, 7, 8, 100.0]]
    got = {c: macro_count(t1, [], 0.01, c) for c in CS}
    want = {0.5: 3, 1.0: 1, 2.0: 1}
    wrong = len(t1)                                     # deliberately wrong rule: every T1 macroscopic
    ok = got == want and wrong != want[2.0]
    print('SELFTEST count', got, 'expected', want, '| wrong rule gives', wrong, 'at c = 2 (must differ):', wrong != want[2.0])
    return ok

def load(run):
    st = [json.loads(l) for l in open(os.path.join(run, 'stats.jsonl'))]
    ev = [json.loads(l) for l in open(os.path.join(run, 'events.jsonl'))]
    cr = [json.loads(l) for l in open(os.path.join(run, 'cross.jsonl'))]
    fin = json.load(open(os.path.join(run, 'final.json')))
    snaps = sorted(glob.glob(os.path.join(run, 'snap_*.npz')))
    return dict(st=st, ev=ev, cr=cr, fin=fin, snaps=snaps, rc=fin['params']['rc'], N0=fin['params']['N0'])

def window(r):
    st = [x for x in r['st'] if x['t'] > 0]
    i0 = next(i for i, x in enumerate(st) if x['Abar'] >= AWIN0)
    i1 = max(i for i, x in enumerate(st) if x['N'] >= NWIN_END)
    return st[i0]['t'], st[i1]['t']

def quarters(lo, hi):
    e = np.exp(np.linspace(math.log(lo), math.log(hi), 5)); return list(zip(e[:-1], e[1:]))

def pooled(runs, wins, sel):
    """Pool records (and snapshot areas) of every run inside its interval sel(run window) -> stats."""
    P = np.zeros(7); W = 0.0; mu = []; Avals = []; slopes = []
    for r, (lo, hi) in zip(runs, wins):
        recs = [x for x in r['st'] if lo <= x['t'] <= hi]
        for x in recs:
            P += np.array(x['p'][1:8]) * x['N']; W += x['N']; mu.append((x['mu2'], x['N']))
        if len(recs) >= 3:
            tt = np.array([x['t'] for x in recs]); aa = np.array([x['Abar'] for x in recs]); slopes.append(np.polyfit(tt, aa, 1)[0])
        for f in r['snaps']:
            z = np.load(f)
            if lo <= float(z['t']) <= hi: Avals.append(z['A'] / z['A'].mean())
    mu2 = sum(m * w for m, w in mu) / sum(w for _, w in mu)
    return dict(p=P / W, mu2=mu2, A=np.sort(np.concatenate(Avals)) if Avals else np.zeros(1), slope=float(np.mean(slopes)) if slopes else float('nan'))

def ks(a, b):
    x = np.concatenate([a, b]); ca = np.searchsorted(a, x, side='right') / len(a); cb = np.searchsorted(b, x, side='right') / len(b)
    return float(np.abs(ca - cb).max())

def scaling_test(runs, wins):
    out = []
    cur = list(wins)
    for drop in range(3):
        whole = pooled(runs, cur, None)
        qs_per_run = [quarters(lo, hi) for lo, hi in cur]
        res = dict(window=cur, q=[])
        allok = True
        for k in range(4):
            sub = [q[k] for q in qs_per_run]
            qq = pooled(runs, sub, None)
            dp = float(np.abs(qq['p'] - whole['p']).max()); dmu = abs(qq['mu2'] - whole['mu2']); kk = ks(qq['A'], whole['A'])
            ds = abs(qq['slope'] / whole['slope'] - 1)
            ok = dp <= TOL_P and dmu <= TOL_MU2 and kk <= TOL_KS and ds <= TOL_SLOPE
            allok &= ok
            res['q'].append(dict(max_dp=round(dp, 4), dmu2=round(dmu, 4), ks=round(kk, 4), slope_rel=round(ds, 4), ok=bool(ok)))
        res['passed'] = bool(allok); out.append(res)
        if allok: return cur, out
        cur = [(q[1][0], hi) for q, (lo, hi) in zip(qs_per_run, cur)]
    return None, out

def count(runs, wins):
    tot = dict(T1=0, T2=0, macro={c: 0 for c in CS}, sides={}, per_run=[])
    for r, (lo, hi) in zip(runs, wins):
        t1 = [e for e in r['ev'] if e[1] == 'T1' and lo <= e[0] <= hi]
        t2 = [e for e in r['ev'] if e[1] in ('T2', 'T2side') and lo <= e[0] <= hi]
        m = {c: macro_count(t1, t2, r['rc'], c) for c in CS}
        tot['T1'] += len(t1); tot['T2'] += len(t2)
        for c in CS: tot['macro'][c] += m[c]
        vanished = {e[2] for e in t2}
        for x in r['cr']:
            if x[1] == 1.0 and x[2] in vanished: tot['sides'][x[3]] = tot['sides'].get(x[3], 0) + 1
        tot['per_run'].append(dict(T1=len(t1), T2=len(t2), **{f'macro_c{c}': m[c] for c in CS},
                                   **{f'R_c{c}': round(m[c] / max(len(t2), 1), 4) for c in CS}))
    T2 = max(tot['T2'], 1)
    tot['R'] = {str(c): dict(value=round(tot['macro'][c] / T2, 4), poisson_err=round(math.sqrt(tot['macro'][c]) / T2, 4),
                             run_sd=round(float(np.std([pr[f'R_c{c}'] for pr in tot['per_run']], ddof=1)), 4) if len(runs) > 1 else None)
             for c in CS}
    tot['total_T1_per_T2'] = round(tot['T1'] / T2, 4)
    ns = sum(tot['sides'].values()) or 1
    tot['T2_shares_at_l2'] = {k: round(v / ns, 3) for k, v in sorted(tot['sides'].items())}
    tot['macro'] = {str(c): v for c, v in tot['macro'].items()}; tot['sides'] = {str(k): v for k, v in tot['sides'].items()}
    return tot

def laws(runs, wins):
    recs = [x for r, (lo, hi) in zip(runs, wins) for x in r['st'] if lo <= x['t'] <= hi]
    out = dict(records=len(recs), max_angle_dev_deg=max(x['max_angle_dev_deg'] for x in recs),
               max_flux_vs_vN=max(x['flux_vs_vN_max'] for x in recs),
               flux_slope_range=[min(x['flux_slope'] for x in recs), max(x['flux_slope'] for x in recs)],
               flux_n0_range=[min(x['flux_n0'] for x in recs), max(x['flux_n0'] for x in recs)],
               mu2=float(np.average([x['mu2'] for x in recs], weights=[x['N'] for x in recs])),
               E_over_Ehex=float(np.average([x['E_over_Ehex'] for x in recs], weights=[x['N'] for x in recs])))
    g = []
    for r, (lo, hi) in zip(runs, wins):
        rr = [x for x in r['st'] if lo <= x['t'] <= hi]
        g.append(np.polyfit([x['t'] for x in rr], [x['Abar'] for x in rr], 1)[0])
    out['growth_over_vN_coefficient'] = float(np.mean(g) / (math.pi / 3)); out['growth_runs'] = [round(float(x) / (math.pi / 3), 4) for x in g]
    # Lewis and Aboav on pooled snapshots in the window
    nn, pairs_all, areas = [], [], []; off = 0
    for r, (lo, hi) in zip(runs, wins):
        for f in r['snaps']:
            z = np.load(f)
            if not (lo <= float(z['t']) <= hi): continue
            ids = z['ids']; idx = {int(b): i for i, b in enumerate(ids)}
            pr = np.array([[idx[int(a)], idx[int(b)]] for a, b in z['pairs']]) + off
            nn.append(z['n']); areas.append(z['A'] / z['A'].mean()); pairs_all.append(pr); off += len(ids)
    n = np.concatenate(nn); A = np.concatenate(areas); pairs = np.concatenate(pairs_all)
    ts = tissue_stats(n, pairs, A)
    out['lewis_slope'] = ts.get('lewis_slope'); out['lewis_n0'] = ts.get('lewis_n0'); out['area_n'] = ts.get('area_n')
    out['aboav_a'] = ts['aboav_a']; out['aboav_intercept'] = ts['aboav_intercept']; out['aboav_intercept_pred'] = ts['aboav_intercept_pred']
    out['m_n'] = ts['m_n']; out['bubble_samples'] = int(len(n))
    return out

if __name__ == '__main__':
    if sys.argv[1] == '--selftest':
        print('FINAL ok' if selftest() else 'FINAL FAIL'); sys.exit(0)
    outp = sys.argv[1]; runs = [load(d) for d in sys.argv[2:]]
    ok = selftest()
    statuses = [r['fin']['status'] for r in runs]
    wins = [window(r) for r in runs]
    win, tests = scaling_test(runs, wins)
    res = dict(runs=sys.argv[2:], statuses=statuses, N0=[r['N0'] for r in runs], rc=runs[0]['rc'], candidate_windows=wins,
               scaling_tests=tests, passed=win is not None)
    use = win if win is not None else wins
    res['count'] = count(runs, use); res['laws'] = laws(runs, use)
    res['counted_window'] = 'passing' if win is not None else 'candidate (scaling test FAILED; reported, not a test)'
    json.dump(res, open(outp, 'w'), indent=1)
    print(json.dumps(dict(passed=res['passed'], R=res['count']['R'], total=res['count']['total_T1_per_T2'], T2=res['count']['T2'],
                          shares=res['count']['T2_shares_at_l2'],
                          laws={k: res['laws'][k] for k in ('max_angle_dev_deg', 'max_flux_vs_vN', 'flux_slope_range', 'flux_n0_range',
                                                             'mu2', 'E_over_Ehex', 'growth_over_vN_coefficient', 'lewis_slope',
                                                             'lewis_n0', 'aboav_a')}), indent=None))
    good = ok and all(s == 'done' for s in statuses) and res['laws']['max_angle_dev_deg'] < 1e-4 and res['laws']['max_flux_vs_vN'] < 1e-6
    print('FINAL ok' if good else 'FINAL FAIL')
