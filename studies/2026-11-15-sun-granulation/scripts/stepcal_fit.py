"""Step calibration fit (README section "Swap rate at step 0", 16 Nov 2026).
Reads results/stepcal/{sun,control,order,holdout}/*.json (census.py output) and the exact Delaunay pair sets of the control sequences
(data/control-s1, data/control-s2, data/stepcal *_exact.json). For every step s and persistence window P:
  detection fraction f(s, P) = pipeline persistent swaps / exact persistent swaps of a control sequence (same s, same P);
  Sun-like calibration = mean of f over speed 1, texture 0 and 1 (half-difference = calibration uncertainty);
  corrected Sun rate = rate / f, fitted against the step (seconds) by a line and by a parabola; intercept = rate at step 0.
Controls: held-out seed-2 sequences corrected with seed-1 fractions against their exact counts; time-reversed and shuffled frames.
Writes results/stepcal/summary.json, summary.md and results/figures/sun_stepcal.png.
Usage: stepcal_fit.py STUDYDIR"""
import sys, os, json, glob
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

S = sys.argv[1]; R = f'{S}/results/stepcal'
STEPS = ['1', '2', '3', '4', '6', '8']; DT = np.array([10.0 * int(s) for s in STEPS]); PS = ['20', '30', '60', '120', '240']
MAIN13 = ['en_T0.0_s1.5_hmax300', 'en_T0.0_s1.5_thr0.25', 'en_uz0.1_s1.5_hmax1200', 'en_uz0.1_s1.5_hmax300', 'en_uz0.1_s1.5_hmax600',
          'en_uz0.1_s1.5_thr0.0', 'en_uz0.1_s1.5_thr0.25', 'en_uz0.1_s1.5_thr0.5', 'en_uz0.1_s3.0_thr0.25', 'qs_uz0.1_s1.5_hmax600',
          'qs_uz0.1_s1.5_thr0.0', 'qs_uz0.1_s1.5_thr0.25', 'qs_uz0.1_s1.5_thr0.5']
problems = []


def load(path):
    try: return json.load(open(path))
    except Exception as e: problems.append(f'missing {path}: {e}'); return None


def exact(ex, s, P, dt=10.0):
    """Exact persistent swaps at step s: Delaunay pairs lost between sampled frames minus twice those regained at a sampled frame within P."""
    Pp = [set(map(tuple, f)) for f in ex['frame_pairs']]
    idx = list(range(0, len(Pp), s)); lost = []
    for a, b in zip(idx, idx[1:]):
        lost += [(b * dt, p) for p in Pp[a] - Pp[b]]
    reg = sum(1 for t, p in lost if any(t < c * dt <= t + P + 1e-6 and p in Pp[c] for c in idx))
    return len(lost) - 2 * reg


def pipe(J, s, P): return J['steps'][s]['swaps_persistent_by_W'][P]
def cellmin(J, s): r = J['steps'][s]; return r['mean_cells'] * r['duration_s'] / 60.0


def fit(y, deg):
    c, cov = np.polyfit(DT, y, deg, cov='unscaled')
    res = y - np.polyval(c, DT); dof = len(DT) - deg - 1
    s2 = (res ** 2).sum() / dof
    se = np.sqrt(np.diag(cov) * s2)
    ss = ((y - y.mean()) ** 2).sum()
    return dict(intercept=float(c[-1]), se=float(se[-1]), slope=float(c[-2]), slope_se=float(se[-2]),
                r2=float(1 - (res ** 2).sum() / ss) if ss > 0 else None, rms_rel=float(np.sqrt((res ** 2).mean()) / abs(y.mean())))


# --- calibration controls (seed 1) ---
ctl = {}
for v in (1, 2, 4):
    for z in (0, 1):
        n = f'voronoi_n500_v{v}.0_z{z}.0_s1'
        J = load(f'{R}/control/{n}.json'); E = load(f'{S}/data/control-s1/{n}_exact.json')
        if J and E:
            ctl[(v, z)] = {P: {s: dict(pipe=pipe(J, s, P), exact=exact(E, int(s), float(P)), cm=cellmin(J, s)) for s in STEPS} for P in PS}
            for P in PS:
                for s in STEPS:
                    d = ctl[(v, z)][P][s]; d['f'] = d['pipe'] / d['exact'] if d['exact'] > 0 else None
out = dict(steps_s=DT.tolist(), P_s=[int(p) for p in PS], detection={}, sun={}, holdout={}, order={}, controls={})
for (v, z), D in ctl.items():
    out['detection'][f'v{v}_z{z}'] = {P: {s: D[P][s]['f'] for s in STEPS} for P in PS}
    out['detection'][f'v{v}_z{z}_exact'] = {P: {s: D[P][s]['exact'] for s in STEPS} for P in PS}


def fcal(P, s, which='mid'):
    a, b = ctl[(1, 0)][P][s]['f'], ctl[(1, 1)][P][s]['f']
    if which == 'mid': return 0.5 * (a + b)
    if which == 'lo': return min(a, b)
    if which == 'hi': return max(a, b)
    if which == 'v12': return np.mean([ctl[(v, z)][P][s]['f'] for v in (1, 2) for z in (0, 1)])


def corrected_fit(rates, P, which):
    y = np.array([rates[s] / fcal(P, s, which) for s in STEPS])
    return y, fit(y, 1), fit(y, 2)


# --- Sun ---
for f in sorted(glob.glob(f'{R}/sun/*.json')):
    tag = os.path.basename(f)[:-5]; J = load(f)
    if not J: continue
    ok = all(J['steps'][s]['balance_failures'] == 0 and J['steps'][s]['neg_control_caught'] in (True, None) for s in STEPS)
    if not ok: problems.append(f'{tag}: balance or negative control failed')
    T = dict(main=tag in MAIN13, byP={})
    for P in PS:
        rates = {s: pipe(J, s, P) / cellmin(J, s) for s in STEPS}
        raw = np.array([rates[s] for s in STEPS])
        y, lin, quad = corrected_fit(rates, P, 'mid')
        _, linlo, _ = corrected_fit(rates, P, 'lo'); _, linhi, _ = corrected_fit(rates, P, 'hi'); _, lin12, _ = corrected_fit(rates, P, 'v12')
        u = float(np.sqrt(lin['se'] ** 2 + (lin['intercept'] - quad['intercept']) ** 2 + (0.5 * (linlo['intercept'] - linhi['intercept'])) ** 2))
        T['byP'][P] = dict(raw=raw.tolist(), corrected=y.tolist(), raw_lin=fit(raw, 1), raw_quad=fit(raw, 2), lin=lin, quad=quad,
                           lin_cal_lo_hi=[linhi['intercept'], linlo['intercept']], lin_cal_speed12=lin12['intercept'], rate0=lin['intercept'], u=u,
                           change_0_80_rel=lin['slope'] * 80 / lin['intercept'], change_0_80_rel_se=lin['slope_se'] * 80 / lin['intercept'])
    a = {P: T['byP'][P]['rate0'] for P in ('30', '60', '120', '240')}; uu = {P: T['byP'][P]['u'] for P in a}
    T['stable_across_P'] = all(abs(a[p] - a[q]) <= np.hypot(uu[p], uu[q]) for p in a for q in a)
    T['rate0_spread_P'] = [min(a.values()), max(a.values())]
    out['sun'][tag] = T

# --- held-out control (seed 2) ---
for v in (1, 2):
    for z in (0, 1):
        n = f'voronoi_n500_v{v}.0_z{z}.0_s2'
        J = load(f'{R}/holdout/{n}.json'); E = load(f'{S}/data/control-s2/{n}_exact.json')
        if not (J and E): continue
        H = {}
        for P in PS:
            ex = np.array([exact(E, int(s), float(P)) / cellmin(J, s) for s in STEPS])
            raw = np.array([pipe(J, s, P) / cellmin(J, s) for s in STEPS])
            cm = raw / np.array([ctl[(v, z)][P][s]['f'] for s in STEPS])                  # matched seed-1 calibration
            cs = raw / np.array([fcal(P, s, 'mid') for s in STEPS])                         # Sun-like calibration (speed 1 mean)
            e0 = fit(ex, 1)['intercept']
            H[P] = dict(exact=ex.tolist(), raw=raw.tolist(), corr_matched=cm.tolist(), corr_sunlike=cs.tolist(), exact0=e0,
                        raw0_ratio=fit(raw, 1)['intercept'] / e0, matched0_ratio=fit(cm, 1)['intercept'] / e0,
                        sunlike0_ratio=fit(cs, 1)['intercept'] / e0, sunlike0_ratio_quad=fit(cs, 2)['intercept'] / fit(ex, 2)['intercept'],
                        matched_max_step_dev=float(np.max(np.abs(cm / ex - 1))))
        out['holdout'][f'v{v}_z{z}'] = H

# --- frame-order controls ---
def order_cmp(fwd, other, exf_fwd=None, exf_other=None):
    r = {}
    for s in STEPS:
        a, b = fwd['steps'][s], other['steps'][s]
        d = dict(fwd=a['swaps_persistent'], other=b['swaps_persistent'], ratio=b['swaps_persistent'] / a['swaps_persistent'],
                 fwd_splits=a['counts'].get('split', 0), fwd_merges=a['counts'].get('merge', 0), other_splits=b['counts'].get('split', 0),
                 other_merges=b['counts'].get('merge', 0), fwd_clumps=a['n_clumps'], other_clumps=b['n_clumps'],
                 fwd_births=a['counts'].get('birth', 0), other_births=b['counts'].get('birth', 0), fwd_deaths=a['counts'].get('death', 0),
                 other_deaths=b['counts'].get('death', 0))
        if exf_fwd: d['exact_fwd'] = exact(exf_fwd, int(s), 60.0); d['exact_other'] = exact(exf_other, int(s), 60.0)
        r[s] = d
    return r
sf = load(f'{R}/sun/en_uz0.1_s1.5_thr0.25.json'); cf = load(f'{R}/control/voronoi_n500_v1.0_z0.0_s1.json')
cfe = load(f'{S}/data/control-s1/voronoi_n500_v1.0_z0.0_s1_exact.json')
for m in ('rev', 'shuf'):
    so = load(f'{R}/order/en_uz0.1_s1.5_thr0.25-{m}.json'); co = load(f'{R}/order/voronoi_n500_v1.0_z0.0_s1-{m}.json')
    coe = load(f'{S}/data/stepcal/voronoi_n500_v1.0_z0.0_s1-{m}_exact.json')
    if sf and so: out['order'][f'sun_{m}'] = order_cmp(sf, so)
    if cf and co and cfe and coe: out['order'][f'control_{m}'] = order_cmp(cf, co, cfe, coe)

# --- verdict on the controls (criteria fixed in the README before the runs) ---
C = out['controls']
if out['holdout']:
    C['holdout_speed1_matched_within_10pct'] = all(abs(out['holdout'][k]['60']['matched0_ratio'] - 1) <= 0.10 for k in ('v1_z0', 'v1_z1') if k in out['holdout'])
    C['holdout_speed1_sunlike_within_10pct'] = all(abs(out['holdout'][k]['60']['sunlike0_ratio'] - 1) <= 0.10 for k in ('v1_z0', 'v1_z1') if k in out['holdout'])
    C['holdout_speed2_sunlike_within_10pct'] = all(abs(out['holdout'][k]['60']['sunlike0_ratio'] - 1) <= 0.10 for k in ('v2_z0', 'v2_z1') if k in out['holdout'])
for who in ('sun', 'control'):
    if f'{who}_rev' in out['order']:
        C[f'{who}_reversed_within_10pct_all_steps'] = all(abs(d['ratio'] - 1) <= 0.10 for d in out['order'][f'{who}_rev'].values())
    if f'{who}_shuf' in out['order']:
        C[f'{who}_shuffled_changes_over_factor2_all_steps'] = all(d['ratio'] < 0.5 or d['ratio'] > 2 for d in out['order'][f'{who}_shuf'].values())

# --- summary over the 13 main settings ---
summ = {}
for P in PS:
    r0 = np.array([out['sun'][t]['byP'][P]['rate0'] for t in MAIN13 if t in out['sun']])
    uu = np.array([out['sun'][t]['byP'][P]['u'] for t in MAIN13 if t in out['sun']])
    ch = np.array([out['sun'][t]['byP'][P]['change_0_80_rel'] for t in MAIN13 if t in out['sun']])
    raw10 = np.array([out['sun'][t]['byP'][P]['raw'][0] for t in MAIN13 if t in out['sun']])
    if len(r0): summ[P] = dict(n=len(r0), rate0_min=float(r0.min()), rate0_median=float(np.median(r0)), rate0_max=float(r0.max()),
                               u_median=float(np.median(uu)), u_rel_median=float(np.median(uu / r0)), raw10_min=float(raw10.min()), raw10_max=float(raw10.max()),
                               change_0_80_median=float(np.median(ch)), change_0_80_min=float(ch.min()), change_0_80_max=float(ch.max()))
out['summary_main13'] = summ
out['stable_across_P_count'] = sum(1 for t in MAIN13 if t in out['sun'] and out['sun'][t]['stable_across_P'])
out['problems'] = problems
json.dump(out, open(f'{R}/summary.json', 'w'), indent=1, default=float)

# --- tables ---
md = ['# Step calibration of the Sun swap rate (generated by stepcal_fit.py)', '']
md.append('## Detection fraction f = pipeline / exact persistent swaps, moving-Voronoi control (seed 1)\n')
md.append('| speed, texture | P (s) | ' + ' | '.join(f'{int(d)} s' for d in DT) + ' |'); md.append('|---|---|' + '---|' * len(DT))
for (v, z) in sorted(ctl):
    for P in PS:
        md.append(f'| {v}, {z} | {P} | ' + ' | '.join(f"{ctl[(v, z)][P][s]['f']:.2f}" for s in STEPS) + ' |')
md.append('\n## Sun: rate at step 0 (persistent swaps per cell per minute), linear fit of the corrected rate\n')
md.append('| setting | P (s) | raw rate at 10 / 80 s | corrected at 10 / 80 s | step 0: line (SE) | parabola | calibration band | speed 1+2 cal. | uncertainty | change 0 to 80 s (line) | R2 line | stable over P |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
for t, T in out['sun'].items():
    for P in PS:
        b = T['byP'][P]
        md.append(f"| {t}{'' if T['main'] else ' (depth)'} | {P} | {b['raw'][0]:.3f} / {b['raw'][-1]:.3f} | {b['corrected'][0]:.3f} / {b['corrected'][-1]:.3f} | "
                  f"{b['lin']['intercept']:.3f} ({b['lin']['se']:.3f}) | {b['quad']['intercept']:.3f} | {b['lin_cal_lo_hi'][0]:.3f} to {b['lin_cal_lo_hi'][1]:.3f} | "
                  f"{b['lin_cal_speed12']:.3f} | {b['u']:.3f} | {100 * b['change_0_80_rel']:+.0f}% ({100 * b['change_0_80_rel_se']:.0f}) | {b['lin']['r2'] if b['lin']['r2'] is None else round(b['lin']['r2'], 2)} | "
                  f"{'yes' if T['stable_across_P'] else 'no'} |")
md.append('\n## Summary over the 13 main settings\n')
md.append('| P (s) | raw rate at 10 s | rate at step 0: min / median / max | median uncertainty (relative) | corrected change 0 to 80 s: median (min to max) |')
md.append('|---|---|---|---|---|')
for P, d in summ.items():
    md.append(f"| {P} | {d['raw10_min']:.3f} to {d['raw10_max']:.3f} | {d['rate0_min']:.3f} / {d['rate0_median']:.3f} / {d['rate0_max']:.3f} | {d['u_median']:.3f} ({100 * d['u_rel_median']:.0f}%) | "
              f"{100 * d['change_0_80_median']:+.0f}% ({100 * d['change_0_80_min']:+.0f}% to {100 * d['change_0_80_max']:+.0f}%) |")
md.append(f"\nStable across P (30, 60, 120, 240 s) within uncertainty: {out['stable_across_P_count']} of {len([t for t in MAIN13 if t in out['sun']])} main settings.\n")
md.append('## Held-out control (seed 2): step-0 rate / exact step-0 rate\n')
md.append('| speed, texture | P (s) | uncorrected | matched seed-1 calibration | Sun-like calibration (line) | Sun-like (parabola) | matched: largest step deviation |')
md.append('|---|---|---|---|---|---|---|')
for k, H in out['holdout'].items():
    for P in PS:
        h = H[P]
        md.append(f"| {k} | {P} | {h['raw0_ratio']:.3f} | {h['matched0_ratio']:.3f} | {h['sunlike0_ratio']:.3f} | {h['sunlike0_ratio_quad']:.3f} | {100 * h['matched_max_step_dev']:.0f}% |")
md.append('\n## Frame-order controls (P = 60 s)\n')
md.append('| sequence | step (s) | persistent swaps forward / changed order (ratio) | exact forward / changed | splits, merges forward | splits, merges changed | births, deaths changed | clumps forward / changed |')
md.append('|---|---|---|---|---|---|---|---|')
for k, O in out['order'].items():
    for s, d in O.items():
        exs = f"{d['exact_fwd']} / {d['exact_other']}" if 'exact_fwd' in d else '-'
        md.append(f"| {k} | {10 * int(s)} | {d['fwd']} / {d['other']} ({d['ratio']:.2f}) | {exs} | {d['fwd_splits']}, {d['fwd_merges']} | {d['other_splits']}, {d['other_merges']} | "
                  f"{d['other_births']}, {d['other_deaths']} | {d['fwd_clumps']} / {d['other_clumps']} |")
md.append('\n## Controls against the criteria fixed before the runs\n')
for k, v in C.items(): md.append(f"- {k}: {'PASS' if v else 'FAIL'}")
if problems: md.append('\nProblems: ' + '; '.join(problems))
open(f'{R}/summary.md', 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))

# --- figure ---
os.makedirs(f'{S}/results/figures', exist_ok=True)
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
for t in MAIN13:
    if t not in out['sun']: continue
    b = out['sun'][t]['byP']['60']; ls = '-' if t.startswith('en') else '--'
    ax[0].plot(DT, b['raw'], ls, marker='o', ms=3, label=t); ax[1].plot(DT, b['corrected'], ls, marker='o', ms=3)
    ax[1].plot([0], [b['rate0']], 'k_', ms=8)
ax[0].set_title('Sun, raw persistent swaps per cell-minute (P = 60 s)', fontsize=9); ax[0].legend(fontsize=5.5, ncol=2)
ax[1].set_title('Sun, corrected by the control detection fraction; ticks: line to step 0', fontsize=9)
for (v, z) in sorted(ctl):
    ax[2].plot(DT, [ctl[(v, z)]['60'][s]['f'] for s in STEPS], marker='o', ms=3, label=f'control speed {v}, texture {z}')
for k, H in out['holdout'].items():
    ax[2].plot(DT, np.array(H['60']['raw']) / np.array(H['60']['exact']), 'x:', ms=5, label=f'held out {k}')
ax[2].set_title('Detection fraction, moving-Voronoi control (P = 60 s)', fontsize=9); ax[2].legend(fontsize=6)
for a in ax: a.set_xlabel('time step (s)'); a.grid(alpha=0.3); a.set_xlim(left=0)
ax[0].set_ylabel('per cell per minute'); ax[1].set_ylabel('per cell per minute'); ax[2].set_ylabel('pipeline / exact')
fig.text(0.99, 0.01, 'DICTO', ha='right', va='bottom', fontsize=8, color='0.4')
plt.tight_layout(); plt.savefig(f'{S}/results/figures/sun_stepcal.png', dpi=110)
complete = len(ctl) == 6 and len(out['holdout']) == 4 and len(out['sun']) == 17 and len(out['order']) == 4
finite = all(np.isfinite(out['sun'][t]['byP'][P]['rate0']) for t in out['sun'] for P in PS)
print('FINAL ok' if complete and finite and not problems else f'FINAL FAIL (controls {len(ctl)}/6, holdout {len(out["holdout"])}/4, sun {len(out["sun"])}/17, order {len(out["order"])}/4, problems {len(problems)})', flush=True)
