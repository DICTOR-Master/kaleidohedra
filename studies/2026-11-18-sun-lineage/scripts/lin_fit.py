"""Lineage net change: tables, the criteria fixed in README.md before the run, checks, figure.
Reads data/lin/TAG.json, TAG-shuf.json, data/null/TAG_VARIANT.json, data/null/calib_calib.json, and the parent study's
results/summary.json (for the equality check and the null curve without births). Writes data/lin_summary.json,
results/summary.md, results/lin_vs_d.png. Usage: lin_fit.py (from this study's folder)"""
import json, os, glob
import numpy as np

P = '../2026-11-18-sun-net-change'
SET = [l.split() for l in open('scripts/settings.txt') if l.strip()]
TAGS = [s[0] for s in SET]
TAUS = ['8', '16', '24', '32', '48', '64']
GRID = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
PARENT = json.load(open(f'{P}/results/summary.json'))
ND = np.array([0.0] + [float(d) for d in PARENT['null']]); NN = np.array([0.0] + [v['net_per_cell'] for v in PARENT['null'].values()])
null0 = lambda D: float(np.interp(D, ND, NN))
checks = {}


def agg(J, s, tf):
    R = J['steps'][s][tf]; r = np.array(R['rows'], float); c = {k: i for i, k in enumerate(R['cols'])}
    col = lambda k: r[:, c[k]]
    sv = max(col('surv').sum(), 1.0); n0 = col('n0').sum()
    return dict(tau=R['tau_s'], starts=len(r), D=float(np.sqrt(col('d2_px2').sum() / sv) / J['ell_px']),
                net=float((col('lost') + col('made')).sum() / sv), surv_frac=float(col('surv').sum() / n0),
                lin=float((col('lin_lost') + col('lin_made')).sum() / n0),
                lin_lost=float(col('lin_lost').sum() / n0), lin_made=float(col('lin_made').sum() / n0),
                lin_share_lost=float(col('lin_lost').sum() / col('E0').sum()),
                lin_size=float(col('lin_size').sum() / n0), fused=float(col('fused').sum() / n0),
                multi_anc=float(col('multi_anc').sum() / col('n1').sum()),
                lin_se=float(np.std((col('lin_lost') + col('lin_made')) / col('n0'), ddof=1) / np.sqrt(len(r))) if len(r) > 1 else None)


sun, shuf, nul = {}, {}, {}
nfiles = 0
for t in TAGS:
    J = json.load(open(f'data/lin/{t}.json')); Js = json.load(open(f'data/lin/{t}-shuf.json')); nfiles += 2
    sun[t] = {s: {tf: agg(J, s, tf) for tf in TAUS} for s in ('1', '8')}
    shuf[t] = {'1': {tf: agg(Js, '1', tf) for tf in TAUS}}
    checks.setdefault('sun_files_ok', True)
    checks['sun_files_ok'] &= bool(J['identity_test'] and J['links_ok'] and J['parent_rows_equal'] and Js['links_ok']
                                   and Js['parent_rows_equal'])
    nul[t] = {}
    for v in ('main', 'V1', 'V2'):
        N = json.load(open(f'data/null/{t}_{v}.json')); nfiles += 1
        nul[t][v] = {tf: N['summary'][f'{sun[t]["1"][tf]["tau"]:g}'] for tf in TAUS}
        nul[t][v]['_rates'] = (N['beta_per_s'] * 60, N['delta_per_s'] * 60)
        checks.setdefault('null_files_ok', True); checks['null_files_ok'] &= bool(all(N['checks'].values()))
CAL = json.load(open('data/null/calib_calib.json')); nfiles += 1
checks['all_81_files_read'] = nfiles == 81   # 16 real + 16 shuffled + 48 null + calibration
checks['D_and_survivor_net_equal_parent'] = all(abs(sun[t][s][tf][k] - PARENT['sun'][t][s][tf][k]) <= 1e-9
                                               for t in TAGS for s in ('1', '8') for tf in TAUS for k in ('D', 'net', 'surv_frac'))
checks['calibration_lineage_equals_plain'] = bool(CAL['checks']['lineage_equals_plain'])
cal1 = CAL['summary'][f'{640.0:g}']
checks['calibration_3600_at_D1'] = abs(cal1['lin_net'] - 3.600) <= 0.02
checks['null_contacts_within_1_of_3N'] = all(json.load(open(f))['checks']['contacts_3n_within_1'] for f in glob.glob('data/null/*.json'))
n_exact = sum(json.load(open(f))['n_exact_3n'] for f in glob.glob('data/null/*.json'))
n_conf = sum(len(json.load(open(f))['rows']) for f in glob.glob('data/null/*.json'))
mono = {t: bool(all(np.diff([sun[t]['1'][tf]['D'] for tf in TAUS]) > 0)) for t in TAGS}
checks['D_increases_with_tau_10s'] = all(mono.values())

for t in TAGS:
    for tf in TAUS:
        a = sun[t]['1'][tf]
        for v in ('main', 'V1', 'V2'):
            a[f'R_{v}'] = a['lin'] / nul[t][v][tf]['lin_net']
        a['R_nobirth'] = a['lin'] / null0(a['D'])
        a['surv_ratio_sun'] = a['net'] / null0(a['D'])                       # the parent's ratio
        a['surv_ratio_null'] = nul[t]['main'][tf]['surv_net'] / null0(nul[t]['main'][tf]['D'])   # same rule applied to the null


def on_grid(key):
    out = {}
    for g in GRID:
        v = {}
        for t in TAGS:
            Ds = np.array([sun[t]['1'][tf]['D'] for tf in TAUS])
            if Ds[0] <= g <= Ds[-1] and mono[t]:
                if key.startswith('R_'):
                    var = key[2:]
                    if var == 'nobirth':
                        v[t] = float(np.interp(g, Ds, [sun[t]['1'][tf]['lin'] for tf in TAUS])) / null0(g)
                    else:
                        v[t] = float(np.interp(g, Ds, [sun[t]['1'][tf]['lin'] for tf in TAUS])) / \
                               float(np.interp(g, Ds, [nul[t][var][tf]['lin_net'] for tf in TAUS]))
                elif key == 'null_lin':
                    v[t] = float(np.interp(g, Ds, [nul[t]['main'][tf]['lin_net'] for tf in TAUS]))
                else:
                    v[t] = float(np.interp(g, Ds, [sun[t]['1'][tf][key] for tf in TAUS]))
        out[str(g)] = v
    return out


def spread(vals):
    a = np.array(list(vals.values())); med = float(np.median(a))
    return dict(n=len(a), median=med, min=float(a.min()), max=float(a.max()), max_dev=float(np.max(np.abs(a / med - 1))))


G = {k: {g: dict(spread(v), values=v) for g, v in on_grid(k).items() if v}
     for k in ('lin', 'R_main', 'R_V1', 'R_V2', 'R_nobirth', 'null_lin', 'surv_ratio_sun', 'surv_ratio_null', 'lin_share_lost')}
judged = [g for g in G['lin'] if G['lin'][g]['n'] >= 12]
tau_spread = {tf: spread({t: sun[t]['1'][tf]['lin'] for t in TAGS}) for tf in TAUS}
medD = {tf: float(np.median([sun[t]['1'][tf]['D'] for t in TAGS])) for tf in TAUS}
lo, hi = float(judged[0]), float(judged[-1])
tau_in = [tf for tf in TAUS if lo <= medD[tf] <= hi]
maxD = max(G['lin'][g]['max_dev'] for g in judged); maxT = max(tau_spread[tf]['max_dev'] for tf in tau_in)
within = all(G['lin'][g]['max_dev'] <= 0.15 for g in judged)
collapse = within and maxD < maxT
medR = [G['R_main'][g]['median'] for g in judged]
varR = float(max(medR) / min(medR) - 1)
R_within = all(G['R_main'][g]['max_dev'] <= 0.15 for g in judged)
single = varR <= 0.10 and R_within
var_of = lambda k: float(max(G[k][g]['median'] for g in judged) / min(G[k][g]['median'] for g in judged) - 1)

spec = {}
for t in TAGS:
    rows = {tf: dict(real=sun[t]['1'][tf]['lin'], shuf=shuf[t]['1'][tf]['lin'],
                     ratio=sun[t]['1'][tf]['lin'] / shuf[t]['1'][tf]['lin'] if shuf[t]['1'][tf]['lin'] > 0 else float('inf')) for tf in TAUS}
    spec[t] = dict(rows=rows, passed=all(r['ratio'] <= 0.5 for r in rows.values()), worst=max(r['ratio'] for r in rows.values()))
nspec = sum(v['passed'] for v in spec.values()); specific = nspec >= 13
rung = collapse and single and specific
step80 = {t: {tf: sun[t]['8'][tf]['lin'] / sun[t]['1'][tf]['lin'] - 1 for tf in TAUS} for t in TAGS}


def clean(x):
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)): return None if np.isnan(x) else 'inf'
    return x


out = dict(settings=TAGS, grid=GRID, sun=sun, shuf=shuf, null={t: {v: {k: x for k, x in d.items()} for v, d in nul[t].items()} for t in TAGS},
           calibration=CAL['summary'], on_grid=G, judged=judged, tau_spread=tau_spread, median_D_at_tau=medD, taus_in_range=tau_in,
           max_spread_matched_D=maxD, max_spread_matched_tau=maxT, all_within_15=within, collapse=collapse,
           median_R_variation=varR, R_all_within_15=R_within, single_number=single, specificity=spec, specific_n=nspec,
           specific=specific, candidate_rung=rung, step80_dev=step80, checks=checks, null_exact_3n=[n_exact, n_conf])
os.makedirs('results', exist_ok=True)
json.dump(clean(out), open('data/lin_summary.json', 'w'), indent=1, allow_nan=False)

# ---- tables
f = lambda x, n=3: 'n/a' if x is None else f'{x:.{n}f}'
pc = lambda x: f'{x * 100:.0f}%'
T = lambda tf: f'{int(float(tf) * 10)} s'
L = ['# Sun: lineage net change: tables (generated by lin_fit.py)', '',
     'lineage net = (start contacts lost + lineage contacts made) / cells at the start; D = rms centroid displacement of survivors '
     '(spacings, the parent\'s); step 10 s unless stated. Null = moving Poisson-Voronoi with births and deaths at the setting\'s census '
     'rates, matched D(tau) (main); V1 matched survival; V2 split births. "no births" = the parent\'s null curve.', '',
     '## Per setting at each tau (step 10 s): D / lineage net / null (main) / Sun / null', '',
     '| setting | ' + ' | '.join(f'tau {T(tf)}' for tf in TAUS) + ' |', '|---' * (len(TAUS) + 1) + '|']
for t in TAGS:
    L.append(f'| {t} | ' + ' | '.join(f'{f(sun[t]["1"][tf]["D"], 2)} / {f(sun[t]["1"][tf]["lin"], 2)} / {f(nul[t]["main"][tf]["lin_net"], 2)} / '
                                      f'{f(sun[t]["1"][tf]["R_main"], 2)}' for tf in TAUS) + ' |')
L += ['', '## A. Collapse at matched D, and B. Sun / null (main)', '',
      '| D | settings | lineage net median (min to max) | max dev | null with births median | Sun/null median (min to max) | max dev | '
      'Sun/null V1 | Sun/null V2 | Sun/no-births null | parent survivor ratio Sun | same rule on the null |', '|---' * 12 + '|']
for g in G['lin']:
    a, b = G['lin'][g], G['R_main'][g]
    mark = '' if g in judged else ' (not judged)'
    L.append(f'| {g}{mark} | {a["n"]} | {f(a["median"])} ({f(a["min"])} to {f(a["max"])}) | {pc(a["max_dev"])} | {f(G["null_lin"][g]["median"])} | '
             f'{f(b["median"], 2)} ({f(b["min"], 2)} to {f(b["max"], 2)}) | {pc(b["max_dev"])} | {f(G["R_V1"][g]["median"], 2)} | '
             f'{f(G["R_V2"][g]["median"], 2)} | {f(G["R_nobirth"][g]["median"], 2)} | {f(G["surv_ratio_sun"][g]["median"], 2)} | '
             f'{f(G["surv_ratio_null"][g]["median"], 2)} |')
L += ['', 'Spread at matched tau:', '', '| tau | median D | lineage net median (min to max) | max dev |', '|---|---|---|---|']
for tf in TAUS:
    a = tau_spread[tf]
    L.append(f'| {T(tf)} | {f(medD[tf])} | {f(a["median"])} ({f(a["min"])} to {f(a["max"])}) | {pc(a["max_dev"])} |')
L += ['', f'Judged D: {", ".join(judged)}. Taus with median D in that range: {", ".join(T(x) for x in tau_in)}.',
      f'Largest spread at matched D: {pc(maxD)}; at matched tau: {pc(maxT)}. All within 15%: {within}. **Collapse: {"yes" if collapse else "no"}.**',
      f'Median Sun/null (main) over judged D varies by {pc(varR)}; every setting within 15% of each D\'s median: {R_within}. '
      f'**Single number: {"yes" if single else "no"}.** (Reported: V1 varies by {pc(var_of("R_V1"))}, V2 by {pc(var_of("R_V2"))}, '
      f'no-births null by {pc(var_of("R_nobirth"))}; parent survivor ratio by {pc(var_of("surv_ratio_sun"))}.)']
L += ['', '## C. Specificity (fixed before the run): real lineage net <= 1/2 shuffled at every tau, step 10 s', '',
      '| setting | ' + ' | '.join(f'tau {T(tf)} real / shuf' for tf in TAUS) + ' | worst ratio | pass |', '|---' * (len(TAUS) + 3) + '|']
for t in TAGS:
    L.append(f'| {t} | ' + ' | '.join(f'{f(spec[t]["rows"][tf]["real"], 2)} / {f(spec[t]["rows"][tf]["shuf"], 2)}' for tf in TAUS)
             + f' | {f(spec[t]["worst"], 2)} | {"y" if spec[t]["passed"] else "n"} |')
L += ['', f'Passes in {nspec} of 16 (needed 13). **Specific: {specific}.**', '',
      '## Reported: lineage composition (step 10 s), survivor share Sun against null, step 80 s', '',
      '| setting | tau | lost / cell | made / cell | lineage size | fused pairs / cell | Sun survivor share | null survivor share (main) | '
      'share of start contacts lost: Sun / null | step 80 s vs 10 s |', '|---' * 10 + '|']
for t in TAGS:
    for tf in ('8', '32', '64'):
        a, n = sun[t]['1'][tf], nul[t]['main'][tf]
        L.append(f'| {t} | {T(tf)} | {f(a["lin_lost"], 2)} | {f(a["lin_made"], 2)} | {f(a["lin_size"], 2)} | {f(a["fused"], 2)} | '
                 f'{f(a["surv_frac"], 2)} | {f(n["surv_frac"], 2)} | {f(a["lin_share_lost"], 3)} / {f(n["lin_share_lost"], 3)} | {step80[t][tf] * 100:+.1f}% |')
L += ['', f'Calibration (zero rates): lineage net at D = 1.0 = {cal1["lin_net"]:.4f} +- {cal1["lin_err"]:.4f} (parent 3.602 +- 0.008); '
      f'lineage = plain in every run: {CAL["checks"]["lineage_equals_plain"]}.',
      f'Null configurations with exactly 3N contacts: {n_exact} of {n_conf} (the rest 3N + 1).', '', '## Checks', '']
L += [f'- {k}: {"PASS" if v else "FAIL"}' for k, v in checks.items()]
open('results/summary.md', 'w').write('\n'.join(L) + '\n')

# ---- figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.2))
col = {'thr': '#3b6fb6', 'hmax': '#c9852b'}
for t, *_r in SET:
    method = _r[-1].split(':')[0]; field = 'T' if '_T' in t else ('qs' if t.startswith('qs') else 'en')
    ls = {'en': '-', 'qs': '--', 'T': ':'}[field]
    Ds = [sun[t]['1'][tf]['D'] for tf in TAUS]
    ax[0].plot(Ds, [nul[t]['main'][tf]['lin_net'] for tf in TAUS], '-', color='0.72', lw=0.9, zorder=1)
    ax[0].plot(Ds, [sun[t]['1'][tf]['lin'] for tf in TAUS], ls, marker='o', ms=3, lw=1.2, color=col[method], alpha=0.9, zorder=3)
    ax[1].plot(Ds, [sun[t]['1'][tf]['R_main'] for tf in TAUS], ls, marker='o', ms=3, lw=1.2, color=col[method], alpha=0.9)
xd = np.linspace(0, 0.75, 200)
ax[0].plot(xd, [null0(x) for x in xd], '-', color='black', lw=2.0)
gx = [float(g) for g in judged]
ax[1].plot(gx, [G['R_main'][g]['median'] for g in judged], '-', color='black', lw=2.4, label='median, lineage count')
ax[1].plot(gx, [G['surv_ratio_sun'][g]['median'] for g in judged], '--', color='black', lw=1.4, label='median, survivor count against the null without births (parent)')
for a in ax:
    for g in judged: a.axvline(float(g), color='0.88', lw=0.6, zorder=0)
    a.set_xlabel('D: rms displacement of survivors (spacings)'); a.set_xlim(0, 0.75)
ax[0].set_ylabel('net neighbour change per cell, between lineages'); ax[0].set_ylim(0, 6)
ax[1].set_ylabel('Sun / null'); ax[1].set_ylim(0.4, 2.6); ax[1].axhline(1.0, color='black', lw=0.7)
h = [Line2D([], [], color='black', lw=2.0, label='null, no births or deaths'), Line2D([], [], color='0.72', label='null with births and deaths (per setting)'),
     Line2D([], [], color=col['thr'], label='threshold markers'), Line2D([], [], color=col['hmax'], label='h-maxima markers'),
     Line2D([], [], color='0.3', ls='-', label='run en, vertical velocity'), Line2D([], [], color='0.3', ls='--', label='run qs, vertical velocity'),
     Line2D([], [], color='0.3', ls=':', label='run en, temperature')]
ax[0].legend(handles=h, fontsize=8, loc='upper left', frameon=False)
ax[1].legend(fontsize=8, loc='lower left', frameon=False)
ax[0].set_title('16 settings, step 10 s, tau 80 to 640 s (axis cut at 6; values to 14.3)', fontsize=10); ax[1].set_title('ratio to each setting\'s null with births and deaths', fontsize=10)
fig.text(0.995, 0.01, 'DICTO', ha='right', va='bottom', fontsize=8, color='0.45')
fig.tight_layout(); fig.savefig('results/lin_vs_d.png', dpi=150)
checks['figure_written'] = os.path.getsize('results/lin_vs_d.png') > 10000
json.dump(clean(out), open('data/lin_summary.json', 'w'), indent=1, allow_nan=False)

nf = sum(not v for v in checks.values())
print(f'collapse {collapse} (matched D {pc(maxD)} vs matched tau {pc(maxT)}); single number {single} (median R varies {pc(varR)}, '
      f'within15 {R_within}); specific {nspec}/16; candidate rung {rung}; checks failed {nf}')
print('FINAL ok' if nf == 0 else f'FINAL FAIL ({nf} checks: ' + ', '.join(k for k, v in checks.items() if not v) + ')')
