"""Net neighbour change per surviving granule against the survivors' rms displacement D (plan in README.md, written before the run).
Reads the parent study's stored data only (../2026-11-18-sun-net-change: data/net/TAG.json, TAG-shuf.json, data/null/null_net.json,
scripts/settings.txt, results/summary.json for the equality check). Writes data/net_vs_d.json, results/summary.md, results/net_vs_d.png.
Usage: net_vs_d.py (from this study's folder)"""
import json, os
import numpy as np

P = '../2026-11-18-sun-net-change'
SET = [l.split() for l in open(f'{P}/scripts/settings.txt') if l.strip()]
TAGS = [s[0] for s in SET]
STEPS = ['1', '2', '4', '8']; TAUS = ['8', '16', '24', '32', '48', '64']
GRID = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
NULL = json.load(open(f'{P}/data/null/null_net.json'))
ND = np.array([0.0] + [float(d) for d in NULL['summary']]); NN = np.array([0.0] + [v['net_per_cell'] for v in NULL['summary'].values()])
NS = np.array([0.0] + [v['share_changed'] for v in NULL['summary'].values()])
null_net = lambda D: float(np.interp(D, ND, NN)); null_share = lambda D: float(np.interp(D, ND, NS))
PARENT = json.load(open(f'{P}/results/summary.json'))
checks = {}


def agg(J, s, tf):
    R = J['steps'][s][tf]; r = np.array(R['rows'], float); c = {k: i for i, k in enumerate(R['cols'])}
    col = lambda k: r[:, c[k]]
    sv = max(col('surv').sum(), 1.0)
    return dict(tau=R['tau_s'], net=float((col('lost') + col('made')).sum() / sv),
                D=float(np.sqrt(col('d2_px2').sum() / sv) / J['ell_px']),
                share=float(col('lost').sum() / max(1.0, col('E0s').sum())),
                surv_frac=float(col('surv').sum() / col('n0').sum()))


sun, shuf = {}, {}
nfiles = 0
for t in TAGS:
    J = json.load(open(f'{P}/data/net/{t}.json')); Js = json.load(open(f'{P}/data/net/{t}-shuf.json')); nfiles += 2
    sun[t] = {s: {tf: agg(J, s, tf) for tf in TAUS} for s in STEPS}
    shuf[t] = {s: {tf: agg(Js, s, tf) for tf in TAUS} for s in STEPS}
    for s in STEPS:
        for tf in TAUS:
            a = sun[t][s][tf]; a['null'] = null_net(a['D']); a['ratio'] = a['net'] / a['null']
            a['share_ratio'] = a['share'] / null_share(a['D'])
checks['all_32_files_read'] = nfiles == 32
checks['D_and_net_equal_parent'] = all(abs(sun[t][s][tf][k] - PARENT['sun'][t][s][tf][k]) <= 1e-9
                                       for t in TAGS for s in STEPS for tf in TAUS for k in ('D', 'net', 'share', 'surv_frac'))
checks['null_at_1.0_is_3.602'] = abs(null_net(1.0) - 3.602) <= 0.01
mono = {s: {t: bool(all(np.diff([sun[t][s][tf]['D'] for tf in TAUS]) > 0)) for t in TAGS} for s in ('1', '8')}
checks['D_increases_with_tau_10s'] = all(mono['1'].values())


def on_grid(s, key):
    """Per grid D: values of key interpolated along each setting's broken line (no extrapolation)."""
    out = {}
    for g in GRID:
        v = {}
        for t in TAGS:
            Ds = np.array([sun[t][s][tf]['D'] for tf in TAUS]); ys = np.array([sun[t][s][tf][key] for tf in TAUS])
            if Ds[0] <= g <= Ds[-1] and np.all(np.diff(Ds) > 0):
                v[t] = float(np.interp(g, Ds, ys))
        out[str(g)] = v
    return out


def spread(vals):
    a = np.array(list(vals.values())); med = float(np.median(a))
    return dict(n=len(a), median=med, min=float(a.min()), max=float(a.max()), max_dev=float(np.max(np.abs(a / med - 1))))


res = {}
for s in ('1', '8'):
    R = {}
    for key in ('net', 'ratio', 'share_ratio'):
        G = on_grid(s, key)
        R[key] = {g: dict(spread(v), values=v) for g, v in G.items() if len(v) >= 1}
    judged = [g for g in R['net'] if R['net'][g]['n'] >= 12]
    tau_spread = {tf: spread({t: sun[t][s][tf]['net'] for t in TAGS}) for tf in TAUS}
    medD = {tf: float(np.median([sun[t][s][tf]['D'] for t in TAGS])) for tf in TAUS}
    lo, hi = (float(judged[0]), float(judged[-1])) if judged else (np.nan, np.nan)
    tau_in = [tf for tf in TAUS if lo <= medD[tf] <= hi]
    maxD = max(R['net'][g]['max_dev'] for g in judged) if judged else np.nan
    maxT = max(tau_spread[tf]['max_dev'] for tf in tau_in) if tau_in else np.nan
    within = all(R['net'][g]['max_dev'] <= 0.15 for g in judged)
    collapse = bool(judged) and within and maxD < maxT
    med_ratio = [R['ratio'][g]['median'] for g in judged]
    var_ratio = float(max(med_ratio) / min(med_ratio) - 1) if judged else np.nan
    ratio_within = all(R['ratio'][g]['max_dev'] <= 0.15 for g in judged)
    single = bool(judged) and var_ratio <= 0.10 and ratio_within
    res[s] = dict(grid=R, judged=judged, tau_spread=tau_spread, median_D_at_tau=medD, taus_in_range=tau_in,
                  max_spread_matched_D=maxD, max_spread_matched_tau_in_range=maxT, all_within_15=within, collapse=collapse,
                  median_ratio_variation=var_ratio, ratio_all_within_15=ratio_within, single_number=single,
                  candidate_rung=collapse and single, D_monotone=mono[s])

# C: survivor-share step test
step = {}
for t in TAGS:
    rows = {}
    for tf in TAUS:
        r1, r8 = sun[t]['1'][tf]['surv_frac'], sun[t]['8'][tf]['surv_frac']
        s1, s8 = shuf[t]['1'][tf]['surv_frac'], shuf[t]['8'][tf]['surv_frac']
        rd = r8 / r1 - 1
        sd = (s8 / s1 - 1) if s1 > 0 else (float('inf') if s8 > 0 else float('nan'))
        ok = abs(rd) < 0.05 and (sd > 0.50 if not np.isnan(sd) else False)
        rows[tf] = dict(real_dev=float(rd), shuf_dev=float(sd), shuf_share_10s=s1, shuf_share_80s=s8, ok=bool(ok))
    step[t] = dict(rows=rows, every_tau=all(v['ok'] for v in rows.values()), tau80=rows['8']['ok'])
nstep = sum(v['every_tau'] for v in step.values()); nstep80 = sum(v['tau80'] for v in step.values())
specific = nstep >= 13

def clean(x):
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)): return None if np.isnan(x) else ('inf' if x > 0 else '-inf')
    return x


out = dict(settings=TAGS, grid=GRID, sun=sun, collapse=res, step_test=step, step_pass_every_tau=nstep, step_pass_tau80=nstep80,
           specific=specific, checks=checks)
os.makedirs('data', exist_ok=True); os.makedirs('results', exist_ok=True)
json.dump(clean(out), open('data/net_vs_d.json', 'w'), indent=1, allow_nan=False)

# ---- tables
f = lambda x, n=3: 'n/a' if x is None or (isinstance(x, float) and np.isnan(x)) else f'{x:.{n}f}'
pc = lambda x: f'{x * 100:.0f}%'
L = ['# Sun: net change against displacement: tables (generated by net_vs_d.py)', '',
     'net = (survivor pairs lost + made) / survivors; D = rms centroid displacement of survivors in spacings; step 10 s unless stated; '
     'grid values interpolated along each setting\'s six tau points, no extrapolation.', '',
     '## Per setting: D and net at each tau (10 s step)', '',
     '| setting | ' + ' | '.join(f'tau {int(float(tf) * 10)} s: D / net / Sun/null' for tf in TAUS) + ' |', '|---' * (len(TAUS) + 1) + '|']
for t in TAGS:
    L.append(f'| {t} | ' + ' | '.join(f'{f(sun[t]["1"][tf]["D"])} / {f(sun[t]["1"][tf]["net"])} / {f(sun[t]["1"][tf]["ratio"], 2)}' for tf in TAUS) + ' |')
for s, lab in (('1', '10 s'), ('8', '80 s (check, reported)')):
    r = res[s]
    L += ['', f'## Spread at matched D (step {lab})', '',
          '| D | settings | net median (min to max) | max dev | null(D) | Sun/null median (min to max) | max dev | share/null share median (min to max) |',
          '|---|---|---|---|---|---|---|---|']
    for g in r['grid']['net']:
        a, b, c = r['grid']['net'][g], r['grid']['ratio'][g], r['grid']['share_ratio'][g]
        mark = '' if g in r['judged'] else ' (not judged)'
        L.append(f'| {g}{mark} | {a["n"]} | {f(a["median"])} ({f(a["min"])} to {f(a["max"])}) | {pc(a["max_dev"])} | {f(null_net(float(g)))} | '
                 f'{f(b["median"], 2)} ({f(b["min"], 2)} to {f(b["max"], 2)}) | {pc(b["max_dev"])} | {f(c["median"], 2)} ({f(c["min"], 2)} to {f(c["max"], 2)}) |')
    L += ['', f'Spread at matched tau (step {lab}):', '', '| tau | median D | net median (min to max) | max dev |', '|---|---|---|---|']
    for tf in TAUS:
        a = r['tau_spread'][tf]
        L.append(f'| {int(float(tf) * 10)} s | {f(r["median_D_at_tau"][tf])} | {f(a["median"])} ({f(a["min"])} to {f(a["max"])}) | {pc(a["max_dev"])} |')
    L += ['', f'Judged D: {", ".join(r["judged"])}. Taus with median D in that range: {", ".join(str(int(float(x) * 10)) + " s" for x in r["taus_in_range"])}.',
          f'Largest spread at matched D: {pc(r["max_spread_matched_D"])}; at matched tau (those taus): {pc(r["max_spread_matched_tau_in_range"])}. '
          f'All within 15%: {r["all_within_15"]}. **Collapse: {"yes" if r["collapse"] else "no"}.**',
          f'Median Sun/null over judged D varies by {pc(r["median_ratio_variation"])}; every setting within 15% of the median ratio at each D: '
          f'{r["ratio_all_within_15"]}. **Single number: {"yes" if r["single_number"] else "no"}.** Candidate rung: {r["candidate_rung"]}.',
          f'D increases with tau in every setting: {all(r["D_monotone"].values())}.']
L += ['', '## Survivor-share step test (Lead 3; threshold fixed in README before the run)', '',
      'dev = survivor share at step 80 s / at step 10 s - 1; real / shuffled; passes at a tau if real |dev| < 5% and shuffled dev > +50%.', '',
      '| setting | ' + ' | '.join(f'tau {int(float(tf) * 10)} s' for tf in TAUS) + ' | every tau | tau 80 s |', '|---' * (len(TAUS) + 3) + '|']
def sdev(x):
    return 'inf' if x == float('inf') else ('n/a' if np.isnan(x) else f'{x * 100:+.0f}%')


for t in TAGS:
    L.append(f'| {t} | ' + ' | '.join(
        f'{step[t]["rows"][tf]["real_dev"] * 100:+.1f}% / {sdev(step[t]["rows"][tf]["shuf_dev"])} {"y" if step[t]["rows"][tf]["ok"] else "n"}'
        for tf in TAUS) + f' | {"y" if step[t]["every_tau"] else "n"} | {"y" if step[t]["tau80"] else "n"} |')
L += ['', f'Passes at every tau in {nstep} of 16 settings (needed: 13); at tau = 80 s alone in {nstep80} of 16. **Specific: {specific}.**', '',
      '## Checks', ''] + [f'- {k}: {"PASS" if v else "FAIL"}' for k, v in checks.items()]
open('results/summary.md', 'w').write('\n'.join(L) + '\n')

# ---- figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(12, 5.2))
col = {'thr': '#3b6fb6', 'hmax': '#d08a2e'}
for t, *_rest in SET:
    method = _rest[-1].split(':')[0]; field = 'T' if '_T' in t else ('qs' if t.startswith('qs') else 'en')
    ls = {'en': '-', 'qs': '--', 'T': ':'}[field]
    Ds = [sun[t]['1'][tf]['D'] for tf in TAUS]
    ax[0].plot(Ds, [sun[t]['1'][tf]['net'] for tf in TAUS], ls, marker='o', ms=3, lw=1.2, color=col[method], alpha=0.85)
    ax[1].plot(Ds, [sun[t]['1'][tf]['ratio'] for tf in TAUS], ls, marker='o', ms=3, lw=1.2, color=col[method], alpha=0.85)
xd = np.linspace(0, 0.75, 200)
ax[0].plot(xd, [null_net(x) for x in xd], '-', color='black', lw=2.2, label='null: independent seeds (Poisson-Voronoi)')
for a in ax:
    for g in res['1']['judged']:
        a.axvline(float(g), color='0.85', lw=0.6, zorder=0)
    a.set_xlabel('D: rms displacement of survivors (spacings)'); a.set_xlim(0, 0.75); a.grid(False)
ax[0].set_ylabel('net neighbour change per survivor'); ax[0].set_ylim(0, 3.0)
ax[1].set_ylabel('Sun / null at the same D'); ax[1].set_ylim(0.3, 1.0); ax[1].axhline(1.0, color='black', lw=0.8)
from matplotlib.lines import Line2D
h = [Line2D([], [], color='black', lw=2.2, label='null curve'),
     Line2D([], [], color=col['thr'], label='threshold markers'), Line2D([], [], color=col['hmax'], label='h-maxima markers'),
     Line2D([], [], color='0.3', ls='-', label='run en, vertical velocity'), Line2D([], [], color='0.3', ls='--', label='run qs, vertical velocity'),
     Line2D([], [], color='0.3', ls=':', label='run en, temperature')]
ax[0].legend(handles=h, fontsize=8, loc='upper left', frameon=False)
ax[0].set_title('16 settings, step 10 s, tau 80 to 640 s', fontsize=10); ax[1].set_title('ratio to the null curve', fontsize=10)
fig.text(0.995, 0.01, 'DICTO', ha='right', va='bottom', fontsize=8, color='0.45')
fig.tight_layout(); fig.savefig('results/net_vs_d.png', dpi=150)
checks['figure_written'] = os.path.getsize('results/net_vs_d.png') > 10000
json.dump(clean(out), open('data/net_vs_d.json', 'w'), indent=1, allow_nan=False)

nf = sum(not v for v in checks.values())
r = res['1']
print(f'collapse {r["collapse"]} (max spread matched D {pc(r["max_spread_matched_D"])} vs matched tau {pc(r["max_spread_matched_tau_in_range"])}); '
      f'single number {r["single_number"]} (median ratio varies {pc(r["median_ratio_variation"])}); step test {nstep}/16 every tau, {nstep80}/16 at 80 s; '
      f'checks failed {nf}')
print('FINAL ok' if nf == 0 else f'FINAL FAIL ({nf} checks: ' + ', '.join(k for k, v in checks.items() if not v) + ')')
