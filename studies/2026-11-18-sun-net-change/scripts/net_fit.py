"""Tables, criteria and verdict for the net-change study (plan in README.md, written before the runs).
Reads data/net/TAG.json and TAG-shuf.json (net_sz.py), data/null/null_net.json (null_net.py), the settings list, and the
centroid jitter j of the 17 Nov study (results/summary.md, table "Cell speed and units"; not available for the depth settings).
Writes results/summary.md and results/summary.json. Usage: net_fit.py (from the study folder)"""
import json, os, re
import numpy as np

SET = [l.split() for l in open('scripts/settings.txt') if l.strip()]
TAGS = [s[0] for s in SET]
STEPS = ['1', '2', '4', '8']; TAUS = ['8', '16', '24', '32', '48', '64']
NULL = json.load(open('data/null/null_net.json'))
ND = np.array([0.0] + [float(d) for d in NULL['summary']]); NN = np.array([0.0] + [v['net_per_cell'] for v in NULL['summary'].values()])
NS = np.array([0.0] + [v['share_changed'] for v in NULL['summary'].values()])
null_net = lambda D: float(np.interp(D, ND, NN)); null_share = lambda D: float(np.interp(D, ND, NS))

jit = {}
for l in open('../2026-11-17-sun-step-zero/results/summary.md'):
    m = re.match(r'\| (\S+) \| [\d.]+ / [\d.]+ / [\d.]+ / [\d.]+ \| [\d.]+ \| [\d.]+ \| ([\d.]+) \| ([\d.]+) \|', l)
    if m: jit[m.group(1)] = float(m.group(2))


def agg(J, s, tf):
    R = J['steps'][s][tf]; r = np.array(R['rows'], float); c = {k: i for i, k in enumerate(R['cols'])}
    col = lambda k: r[:, c[k]]
    surv = col('surv'); net_i = (col('lost') + col('made')) / np.maximum(surv, 1)
    tau = R['tau_s']; neff = max(1.0, len(r) * min(1.0, 80.0 / tau))
    ell = J['ell_px']
    sv = max(surv.sum(), 1.0)
    D = np.sqrt(col('d2_px2').sum() / sv) / ell
    Drel = np.sqrt(col('rel2_px2').sum() / max(1, col('E0s').sum())) / ell
    return dict(tau=tau, starts=len(r), net=float((col('lost') + col('made')).sum() / sv),
                se=float(net_i.std(ddof=1) / np.sqrt(neff)) if len(r) > 1 else float('nan'),
                share=float(col('lost').sum() / max(1.0, col('E0s').sum())),
                net_all=float((col('all_lost') + col('all_made')).sum() / ((col('n0') + col('n1')) / 2).sum()),
                surv_frac=float(surv.sum() / col('n0').sum()), pairs_per_surv=float(col('E0s').sum() / sv), E0s=int(col('E0s').sum()),
                made_minus_lost=int((col('made') - col('lost')).sum()), D=float(D), Drel=float(Drel), Deff=float(Drel / np.sqrt(2)))


out = dict(settings=TAGS, null=NULL['summary'], jitter_px=jit, sun={}, shuf={}, F={}, S={}, checks={})
for t in TAGS:
    J = json.load(open(f'data/net/{t}.json')); Jsh = json.load(open(f'data/net/{t}-shuf.json'))
    out['checks'][f'pairs_check_{t}'] = J['pairs_check'] and Jsh['pairs_check']
    out['sun'][t] = {s: {tf: agg(J, s, tf) for tf in TAUS} for s in STEPS}
    out['shuf'][t] = {s: {tf: agg(Jsh, s, tf) for tf in TAUS} for s in STEPS}
    for s in STEPS:
        for tf in TAUS:
            a = out['sun'][t][s][tf]; ell = J['ell_px']
            a['null_at_D'] = null_net(a['D']); a['null_at_Deff'] = null_net(a['Deff'])
            a['ratio_D'] = a['net'] / a['null_at_D']; a['ratio_Deff'] = a['net'] / a['null_at_Deff']
            a['share_ratio_D'] = a['share'] / null_share(a['D']); a['share_ratio_Deff'] = a['share'] / null_share(a['Deff'])
            if t in jit:
                Dj = np.sqrt(max(a['D'] ** 2 - (jit[t] / ell) ** 2, 1e-12)); a['D_jit'] = float(Dj); a['ratio_Djit'] = a['net'] / null_net(Dj)
    # F: frame-rate free (every tau: steps 20, 40, 80 s within 5% of 10 s, or within 2 standard errors)
    fpass = True; dev = {}
    for tf in TAUS:
        b = out['sun'][t]['1'][tf]
        for s in STEPS[1:]:
            x = out['sun'][t][s][tf]; d = x['net'] / b['net'] - 1
            ok = abs(d) <= 0.05 or abs(x['net'] - b['net']) <= 2 * np.hypot(x['se'], b['se'])
            dev[f'{s}_{tf}'] = (float(d), bool(ok)); fpass &= ok
    out['F'][t] = dict(passed=bool(fpass), dev=dev, max_abs_dev=float(max(abs(v[0]) for v in dev.values())))
    spass = all(out['sun'][t][s][tf]['net'] <= 0.5 * out['shuf'][t][s][tf]['net'] for s in STEPS for tf in TAUS)
    rr = lambda a, b: a / b if b > 0 else float('inf')
    out['S'][t] = dict(passed=bool(spass), worst=float(max(rr(out['sun'][t][s][tf]['net'], out['shuf'][t][s][tf]['net']) for s in STEPS for tf in TAUS)))
    # after the run (not in the plan): the same frame-rate test on shuffled frames, and survivor shares real / shuffled
    out['F_shuf'] = out.get('F_shuf', {})
    out['F_shuf'][t] = dict(surv_dev_8_vs_1=[float(rr(out['shuf'][t]['8'][tf]['surv_frac'], out['shuf'][t]['1'][tf]['surv_frac']) - 1) for tf in TAUS],
                            net_dev_8_vs_1=[float(rr(out['shuf'][t]['8'][tf]['net'], out['shuf'][t]['1'][tf]['net']) - 1) for tf in TAUS],
                            real_surv_dev_8_vs_1=[float(out['sun'][t]['8'][tf]['surv_frac'] / out['sun'][t]['1'][tf]['surv_frac'] - 1) for tf in TAUS])

nF = sum(v['passed'] for v in out['F'].values()); nS = sum(v['passed'] for v in out['S'].values())
stab = {}
for tf in TAUS:
    v = np.array([out['sun'][t]['1'][tf]['net'] for t in TAGS]); med = float(np.median(v))
    stab[tf] = dict(median=med, min=float(v.min()), max=float(v.max()), within15=bool(np.all(np.abs(v / med - 1) <= 0.15)),
                    max_dev=float(np.max(np.abs(v / med - 1))))
    for key in ('ratio_D', 'ratio_Deff', 'share_ratio_D'):
        w = np.array([out['sun'][t]['1'][tf][key] for t in TAGS])
        stab[tf][key] = dict(median=float(np.median(w)), min=float(w.min()), max=float(w.max()))
stable = all(v['within15'] for v in stab.values())
out['stability'] = stab
out['frame_rate_free'] = nF >= 13; out['specific'] = nS >= 13; out['stable'] = stable
out['positive'] = out['frame_rate_free'] and out['specific'] and stable
out['checks']['null_reproduces_3600'] = bool(NULL['check_reproduces_3600'])
out['checks']['all_files'] = len(out['sun']) == 16 and len(out['shuf']) == 16
json.dump(out, open('results/summary.json', 'w'), indent=1)

# ---- tables
f = lambda x, n=3: f'{x:.{n}f}'
L = ['# Sun: net change of neighbours after a fixed time: tables (generated by net_fit.py)', '',
     'net = (survivor pairs lost + made) / survivors (the null study\'s definition, survivors in place of its fixed cells); '
     'D, D_eff in spacings; step 10 s unless stated.', '',
     '## Null curve (2D Poisson-Voronoi, N = 20 000, 4 repetitions, independent Gaussian displacement of rms D)', '',
     '| D | net per cell | +- | share of contacts changed |', '|---|---|---|---|']
for d, v in NULL['summary'].items():
    L.append(f'| {d} | {f(v["net_per_cell"])} | {f(v["err"])} | {f(v["share_changed"])} |')
L += ['', '## Frame-rate test: net per survivor at steps 10 / 20 / 40 / 80 s, for each tau', '',
      '| setting | ' + ' | '.join(f'tau {int(float(tf) * 10)} s' for tf in TAUS) + ' | max dev | F |', '|---' * (len(TAUS) + 3) + '|']
for t in TAGS:
    row = [' / '.join(f(out['sun'][t][s][tf]['net']) for s in STEPS) for tf in TAUS]
    L.append(f'| {t} | ' + ' | '.join(row) + f' | {out["F"][t]["max_abs_dev"] * 100:.1f}% | {"y" if out["F"][t]["passed"] else "n"} |')
L += ['', f'F (frame-rate free) holds in {nF} of 16 settings (needed: 13).', '',
      '## Survivor share and standard error (10 s step)', '',
      '| setting | ' + ' | '.join(f'tau {int(float(tf) * 10)} s: surv / se / starts' for tf in TAUS) + ' |', '|---' * (len(TAUS) + 1) + '|']
for t in TAGS:
    L.append(f'| {t} | ' + ' | '.join(f'{f(out["sun"][t]["1"][tf]["surv_frac"], 2)} / {f(out["sun"][t]["1"][tf]["se"])} / {out["sun"][t]["1"][tf]["starts"]}' for tf in TAUS) + ' |')
L += ['', '## Shuffled frames: net per survivor (10 / 80 s step) and real / shuffled', '',
      '| setting | ' + ' | '.join(f'tau {int(float(tf) * 10)} s' for tf in TAUS) + ' | worst real/shuf | S |', '|---' * (len(TAUS) + 3) + '|']
for t in TAGS:
    row = [f'{f(out["shuf"][t]["1"][tf]["net"], 2)} / {f(out["shuf"][t]["8"][tf]["net"], 2)} ({f(out["sun"][t]["1"][tf]["net"] / max(out["shuf"][t]["1"][tf]["net"], 1e-9), 2)})' for tf in TAUS]
    L.append(f'| {t} | ' + ' | '.join(row) + f' | {f(out["S"][t]["worst"], 2)} | {"y" if out["S"][t]["passed"] else "n"} |')
L += ['', f'S (real at most 1/2 of shuffled at every step and tau) holds in {nS} of 16 settings.', '',
      '## After the run (not in the plan): survivor share and share of contacts changed, real against shuffled', '',
      'Per cell: survivor share at step 10 s, real / shuffled; at step 80 s, real / shuffled; share of survivor contacts changed at '
      'step 10 s, real / shuffled (survivor pairs at the start, shuffled).', '',
      '| setting | ' + ' | '.join(f'tau {int(float(tf) * 10)} s' for tf in TAUS) + ' |', '|---' * (len(TAUS) + 1) + '|']
for t in TAGS:
    L.append(f'| {t} | ' + ' | '.join(
        f'{f(out["sun"][t]["1"][tf]["surv_frac"], 2)}/{f(out["shuf"][t]["1"][tf]["surv_frac"], 2)}; '
        f'{f(out["sun"][t]["8"][tf]["surv_frac"], 2)}/{f(out["shuf"][t]["8"][tf]["surv_frac"], 2)}; '
        f'{f(out["sun"][t]["1"][tf]["share"], 2)}/{f(out["shuf"][t]["1"][tf]["share"], 2)} ({out["shuf"][t]["1"][tf]["E0s"]})' for tf in TAUS) + ' |')
L += ['',
      '## Against the null at matched displacement (10 s step)', '',
      '| setting | tau | net | D | null(D) | net/null(D) | D_eff | net/null(D_eff) | D jitter-corrected: net/null | share / null share (D) | net all labels | survivor pairs per survivor |',
      '|---|---|---|---|---|---|---|---|---|---|---|---|']
for t in TAGS:
    for tf in TAUS:
        a = out['sun'][t]['1'][tf]
        L.append(f'| {t} | {int(a["tau"])} | {f(a["net"])} | {f(a["D"])} | {f(a["null_at_D"])} | {f(a["ratio_D"], 2)} | {f(a["Deff"])} | '
                 f'{f(a["ratio_Deff"], 2)} | {f(a["ratio_Djit"], 2) if "ratio_Djit" in a else "n/a"} | {f(a["share_ratio_D"], 2)} | {f(a["net_all"])} | {f(a["pairs_per_surv"], 2)} |')
L += ['', '## Stability over the 16 settings (10 s step)', '',
      '| tau | net median (min to max) | max dev from median | within 15% | net/null(D) median (min to max) | net/null(D_eff) median (min to max) |',
      '|---|---|---|---|---|---|']
for tf in TAUS:
    v = stab[tf]
    L.append(f'| {int(float(tf) * 10)} s | {f(v["median"])} ({f(v["min"])} to {f(v["max"])}) | {v["max_dev"] * 100:.0f}% | {"y" if v["within15"] else "n"} | '
             f'{f(v["ratio_D"]["median"], 2)} ({f(v["ratio_D"]["min"], 2)} to {f(v["ratio_D"]["max"], 2)}) | '
             f'{f(v["ratio_Deff"]["median"], 2)} ({f(v["ratio_Deff"]["min"], 2)} to {f(v["ratio_Deff"]["max"], 2)}) |')
L += ['', f'Frame-rate free: {out["frame_rate_free"]}. Specific: {out["specific"]}. Stable: {stable}. Positive: {out["positive"]}.', '',
      '## Checks', ''] + [f'- {k}: {"PASS" if v else "FAIL"}' for k, v in out['checks'].items()]
open('results/summary.md', 'w').write('\n'.join(L) + '\n')
nf = sum(not v for v in out['checks'].values())
print(f'F {nF}/16  S {nS}/16  stable {stable}  positive {out["positive"]}  checks failed {nf}')
print('FINAL ok' if nf == 0 else 'FINAL FAIL (checks)')
