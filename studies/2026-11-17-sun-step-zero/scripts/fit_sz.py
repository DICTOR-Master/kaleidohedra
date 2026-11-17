"""Step-0 extrapolation of the Sun swap rate with the moving-Voronoi detection efficiency (studies/2026-11-17-sun-step-zero).
Reads data/{sun,control,holdout,order}/*.json (census_sz.py output, with full swap lists) and the exact Delaunay pair sets of the
control sequences. Applies the persistence window P and the continuity threshold theta to the swap lists (census rule), computes
the detection efficiency f(step, P, theta) on the Sun-like controls, corrects the Sun rates, fits them to step 0 with four models,
and judges the criteria C1 to C5 written in README.md before the runs. Writes results/summary.json and results/summary.md.
Usage: fit_sz.py STUDYDIR"""
import sys, os, json, glob
import numpy as np

S = sys.argv[1]; D = f'{S}/data'; OLD = f'{S}/../2026-11-15-sun-granulation'
STEPS = ['1', '2', '3', '4', '6', '8']; DT = np.array([10.0 * int(s) for s in STEPS])
FAM = {'P0': lambda s: 0.0, 'k1': lambda s: s, 'k2': lambda s: 2 * s, 'k3': lambda s: 3 * s,
       'P30': lambda s: 30.0, 'P60': lambda s: 60.0, 'P120': lambda s: 120.0}
FAMJ = ['k1', 'k2', 'k3', 'P30', 'P60', 'P120']             # the six window families judged in C3 (P0 reported)
THETAS = [0.0, 0.3, 0.4, 0.5, 0.6, 0.7]
MAIN13 = ['en_T0.0_s1.5_hmax300', 'en_T0.0_s1.5_thr0.25', 'en_uz0.1_s1.5_hmax1200', 'en_uz0.1_s1.5_hmax300', 'en_uz0.1_s1.5_hmax600',
          'en_uz0.1_s1.5_thr0.0', 'en_uz0.1_s1.5_thr0.25', 'en_uz0.1_s1.5_thr0.5', 'en_uz0.1_s3.0_thr0.25', 'qs_uz0.1_s1.5_hmax600',
          'qs_uz0.1_s1.5_thr0.0', 'qs_uz0.1_s1.5_thr0.25', 'qs_uz0.1_s1.5_thr0.5']
PRIMARY = 'en_uz0.1_s1.5_thr0.25'
NULL2D = 3.04
checks, problems = {}, []


def chk(name, ok): checks[name] = bool(ok); return ok


def persistent(r, P, th):
    """Census rule on the swap list: elementary swaps with share >= th, minus twice the swaps undone by the same four cells within P."""
    op, fl, n = {}, 0, 0
    for t, lo, ga, two, sh in r['swap_list']:
        if sh < th: continue
        n += 1; lo, ga = tuple(lo), tuple(ga); k = (ga, lo)
        if k in op and t - op[k] <= P + 1e-6: fl += 1; del op[k]
        else: op[(lo, ga)] = t
    return n - 2 * fl


def exact(ex, s, P, dt=10.0):
    """Exact persistent swaps at step s (16 Nov rule): Delaunay pairs lost between sampled frames minus twice those regained at a
    sampled frame within P."""
    Pp = ex['_sets']; idx = list(range(0, len(Pp), s)); lost = []
    for a, b in zip(idx, idx[1:]): lost += [(b * dt, p) for p in Pp[a] - Pp[b]]
    reg = sum(1 for t, p in lost if any(t < c * dt <= t + P + 1e-6 and p in Pp[c] for c in idx))
    return len(lost) - 2 * reg


def cellmin(J, s): r = J['steps'][s]; return r['mean_cells'] * r['duration_s'] / 60.0


def fit(x, y, deg):
    c, cov = np.polyfit(x, y, deg, cov='unscaled')
    res = y - np.polyval(c, x); dof = len(x) - deg - 1
    se = np.sqrt(np.diag(cov) * (res ** 2).sum() / dof) if dof > 0 else np.full(deg + 1, np.nan)
    return dict(intercept=float(c[-1]), se=float(se[-1]), slope=float(c[-2]), slope_se=float(se[-2]), coef=c.tolist())


def load(p):
    try: return json.load(open(p))
    except Exception as e: problems.append(f'missing {p}: {e}'); return None


def load_exact(p):
    E = load(p)
    if E: E['_sets'] = [set(map(tuple, f)) for f in E['frame_pairs']]
    return E


# ---------- 1. reproduction of 16 Nov ----------
old = {}
for tag in MAIN13:
    J = load(f'{D}/sun/{tag}.json'); O = load(f'{OLD}/results/stepcal/sun/{tag}.json')
    if not (J and O): continue
    old[tag] = J
    same = all(J['steps'][s]['swaps_persistent_by_W'] == O['steps'][s]['swaps_persistent_by_W'] for s in STEPS)
    lst = all(persistent(J['steps'][s], float(P), 0.0) == J['steps'][s]['swaps_persistent_by_W'][P] for s in STEPS for P in ('20', '30', '60', '120', '240'))
    chk(f'repro_16nov_{tag}', same); chk(f'list_rule_equals_census_{tag}', lst)
prim = old.get(PRIMARY)
chk('repro_primary_733_626_484_305', prim and [prim['steps'][s]['swaps_persistent'] for s in ('1', '2', '4', '8')] == [733, 626, 484, 305])
sh_prim = load(f'{D}/order/{PRIMARY}-shuf.json')
chk('repro_primary_shuffled_767', sh_prim and sh_prim['steps']['1']['swaps_persistent'] == 767)
sun = old

# ---------- 2. controls and efficiency ----------
ctl, ctlE = {}, {}
for v in (1, 2):
    for z in (0, 1):
        n = f'voronoi_n500_v{v}.0_z{z}.0_s1'
        J = load(f'{D}/control/{n}.json'); E = load_exact(f'{OLD}/data/control-s1/{n}_exact.json')
        O = load(f'{OLD}/results/stepcal/control/{n}.json')
        if J and O: chk(f'repro_16nov_control_{n}', all(J['steps'][s]['swaps_persistent_by_W'] == O['steps'][s]['swaps_persistent_by_W'] for s in STEPS))
        if J and E: ctl[(v, z)] = J; ctlE[(v, z)] = E
EX, F = {}, {}
for key, J in ctl.items():
    E = ctlE[key]
    for fam, Pf in FAM.items():
        for s in STEPS:
            ex = exact(E, int(s), Pf(10.0 * int(s)))
            EX[(key, fam, s)] = ex
            for th in THETAS:
                F[(key, fam, s, th)] = persistent(J['steps'][s], Pf(10.0 * int(s)), th) / ex if ex > 0 else np.nan


def fcal(fam, s, th, which='mid'):
    a, b = F[((1, 0), fam, s, th)], F[((1, 1), fam, s, th)]
    return {'mid': 0.5 * (a + b), 'lo': min(a, b), 'hi': max(a, b),
            'v12': np.mean([F[((v, z), fam, s, th)] for v in (1, 2) for z in (0, 1)])}[which]


# ---------- 3. continuity threshold theta* ----------
theta_star = None; th_table = {}
real_p, shuf_p = sun.get(PRIMARY), sh_prim
if real_p and shuf_p:
    for th in THETAS:
        a = persistent(real_p['steps']['1'], 20.0, th); b = persistent(shuf_p['steps']['1'], 20.0, th)
        th_table[th] = dict(real=a, shuffled=b, ratio=b / a if a else None)
    for th in THETAS[1:]:
        if th_table[th]['ratio'] is not None and th_table[th]['ratio'] <= 1 / 3: theta_star = th; break
cs_shuf = load(f'{D}/order/voronoi_n500_v1.0_z0.0_s1-shuf.json')
ctl_keep = None
if theta_star is not None and (1, 0) in ctl:
    a0 = persistent(ctl[(1, 0)]['steps']['1'], 20.0, 0.0); a1 = persistent(ctl[(1, 0)]['steps']['1'], 20.0, theta_star)
    ctl_keep = a1 / a0
TH_USED = [0.0] + ([theta_star] if theta_star is not None else [])

# ---------- 4. held-out control (seed 2) ----------
hold, calerr = {}, {}
for th in TH_USED:
    for fam in FAM:
        errs = []
        for v in (1, 2):
            for z in (0, 1):
                n = f'voronoi_n500_v{v}.0_z{z}.0_s2'
                J = load(f'{D}/holdout/{n}.json'); E = load_exact(f'{S}/work/control-s2/{n}_exact.json') if os.path.exists(f'{S}/work/control-s2/{n}_exact.json') else load_exact(f'{OLD}/data/control-s2/{n}_exact.json')
                if not (J and E): continue
                Pf = FAM[fam]
                ex = np.array([exact(E, int(s), Pf(10.0 * int(s))) / cellmin(J, s) for s in STEPS])
                raw = np.array([persistent(J['steps'][s], Pf(10.0 * int(s)), th) / cellmin(J, s) for s in STEPS])
                cs = raw / np.array([fcal(fam, s, th) for s in STEPS])
                cm = raw / np.array([F[((v, z), fam, s, th)] for s in STEPS])
                e0 = fit(DT, ex, 1)['intercept']
                h = dict(exact0=e0, exact_change_0_80=fit(DT, ex, 1)['slope'] * 80 / e0, sunlike0_ratio=fit(DT, cs, 1)['intercept'] / e0,
                         matched0_ratio=fit(DT, cm, 1)['intercept'] / e0, raw0_ratio=fit(DT, raw, 1)['intercept'] / e0)
                hold[f'th{th}_{fam}_v{v}_z{z}'] = h
                if v == 1: errs.append(abs(h['sunlike0_ratio'] - 1))
        calerr[(th, fam)] = max(errs) if errs else 0.15
for th in TH_USED:
    chk(f'holdout_speed1_within_15pct_k2_theta{th}', all(abs(hold[f'th{th}_k2_v1_z{z}']['sunlike0_ratio'] - 1) <= 0.15 for z in (0, 1)))

# ---------- 5. Sun: corrected rates, fits, criteria ----------
res = {}
for tag in MAIN13:
    J = sun.get(tag); Jsh = load(f'{D}/order/{tag}-shuf.json')
    if not J: continue
    T = {}
    for th in TH_USED:
        for fam, Pf in FAM.items():
            Ps = [Pf(10.0 * int(s)) for s in STEPS]
            n_real = np.array([persistent(J['steps'][s], P, th) for s, P in zip(STEPS, Ps)], float)
            n_shuf = np.array([persistent(Jsh['steps'][s], P, th) for s, P in zip(STEPS, Ps)], float) if Jsh else np.full(6, np.nan)
            cm = np.array([cellmin(J, s) for s in STEPS])
            f = np.array([fcal(fam, s, th) for s in STEPS])
            y = n_real / cm / f
            lin, quad = fit(DT, y, 1), fit(DT, y, 2)
            short = fit(DT[:4], y[:4], 1)
            lo = fit(DT, n_real / cm / np.array([fcal(fam, s, th, 'lo') for s in STEPS]), 1)['intercept']
            hi = fit(DT, n_real / cm / np.array([fcal(fam, s, th, 'hi') for s in STEPS]), 1)['intercept']
            v12 = fit(DT, n_real / cm / np.array([fcal(fam, s, th, 'v12') for s in STEPS]), 1)['intercept']
            yfs = (n_real - n_shuf) / cm / f
            fs = fit(DT, yfs, 1) if np.all(np.isfinite(yfs)) else None
            r0 = lin['intercept']
            u = float(np.sqrt(lin['se'] ** 2 + (r0 - quad['intercept']) ** 2 + (0.5 * (lo - hi)) ** 2 + (calerr[(th, fam)] * r0) ** 2))
            ho = fit(DT[1:], y[1:], 1); pred10 = np.polyval(ho['coef'], 10.0)
            # counting error at 10 s (Poisson on the persistent count), added to the hold-out comparison
            u10 = float(np.hypot(u, y[0] / np.sqrt(max(n_real[0], 1))))
            T[f'th{th}_{fam}'] = dict(P=Ps, n_real=n_real.tolist(), n_shuf=n_shuf.tolist(), f=f.tolist(), raw=(n_real / cm).tolist(), corrected=y.tolist(),
                                      line=lin, parabola=quad, short=short, floor_sub=fs, cal_lo_hi=[hi, lo], cal_speed12=v12, rate0=r0, u=u,
                                      change_0_80=lin['slope'] * 80 / r0, short_change_0_30=short['slope'] * 30 / short['intercept'],
                                      holdout_pred10=float(pred10), holdout_obs10=float(y[0]), shuf_over_real_10=float(n_shuf[0] / n_real[0]),
                                      C1=bool(abs(short['slope'] * 30 / short['intercept']) <= 0.10),
                                      C2=bool(abs(r0 - quad['intercept']) <= u and abs(r0 - short['intercept']) <= u),
                                      C4=bool(abs(pred10 - y[0]) <= u10),
                                      C5=bool(n_shuf[0] / n_real[0] <= 1 / 3 or (fs is not None and abs(fs['intercept'] - r0) <= u)))
        vals = {fam: (T[f'th{th}_{fam}']['rate0'], T[f'th{th}_{fam}']['u']) for fam in FAMJ}
        c3 = all(abs(vals[a][0] - vals[b][0]) <= np.hypot(vals[a][1], vals[b][1]) for a in FAMJ for b in FAMJ)
        for fam in FAM: T[f'th{th}_{fam}']['C3'] = bool(c3)
        T[f'th{th}_rate0_over_families'] = [min(v[0] for v in vals.values()), max(v[0] for v in vals.values())]
    # apparent cell speed: d2 = v^2 step^2 + j^2 over 10 to 40 s
    cen = [J['steps'][s]['centroid'] for s in STEPS]
    d2 = np.array([c['msd_px2_share05'] for c in cen]); x2 = DT ** 2
    cf = np.polyfit(x2[:4], d2[:4], 1); vpx = float(np.sqrt(max(cf[0], 0)))           # pixels per second
    Lpx = cen[0]['L_px']; ncell = J['steps']['1']['mean_cells']; ell = Lpx / np.sqrt(ncell)
    T['speed'] = dict(msd_px2=d2.tolist(), v_px_per_s=vpx, jitter_px=float(np.sqrt(max(cf[1], 0))), spacing_px=float(ell),
                      spacing_per_min=float(vpx * 60 / ell), d2_exponent=float(np.polyfit(np.log(DT[:4]), np.log(d2[:4]), 1)[0]))
    res[tag] = T

# per-setting pass under a theta
def passes(T, th):
    return all(all(T[f'th{th}_{fam}'][c] for c in ('C1', 'C2', 'C3', 'C4', 'C5')) for fam in FAMJ)
npass = {th: sum(passes(res[t], th) for t in res) for th in TH_USED}
crit = {th: {c: sum(all(res[t][f'th{th}_{fam}'][c] for fam in FAMJ) for t in res) for c in ('C1', 'C2', 'C3', 'C4', 'C5')} for th in TH_USED}
hold_ok = {th: checks.get(f'holdout_speed1_within_15pct_k2_theta{th}', False) for th in TH_USED}
converged = {th: npass[th] >= 10 and hold_ok[th] for th in TH_USED}

# ---------- 6. control: speed estimator and unit check ----------
def seed_speed(v, seed=1, N=500, L=504, NF=120):
    rng = np.random.default_rng(seed); rng.uniform(0, L, (N, 2))
    A = rng.normal(0, 1, (N, 2, 2)); w = rng.uniform(0.002, 0.01, (N, 2, 2)); ph = rng.uniform(0, 2 * np.pi, (N, 2, 2))
    t = np.arange(0, 10.0 * (NF - 1), 2.0)
    vel = np.stack([v * (A * w * np.cos(w * tt + ph)).sum(2) / np.maximum(w.mean(2), 1e-9) * 0.01 for tt in t])
    return float(np.sqrt((vel ** 2).sum(2).mean()))
ctl_speed = {}
for (v, z), J in ctl.items():
    cen = [J['steps'][s]['centroid'] for s in STEPS]
    d2 = np.array([c['msd_px2_share05'] for c in cen]); cf = np.polyfit(DT[:4] ** 2, d2[:4], 1)
    vt = seed_speed(v); ell = 504 / np.sqrt(500)
    E = ctlE[(v, z)]; dur = 10.0 * (len(E['frame_pairs']) - 1)
    ex_rate = E['exact_swaps_total'] / (500 * dur)              # exact T1 per cell per second (20 substeps per frame)
    ctl_speed[f'v{v}_z{z}'] = dict(v_true_px_s=vt, v_est_px_s=float(np.sqrt(max(cf[0], 0))), est_over_true=float(np.sqrt(max(cf[0], 0)) / vt),
                                   exact_T1_per_cell_per_spacing=float(ex_rate * ell / vt))

# dimensionless Sun rate (reported whatever the verdict; meaningful only if converged)
th0 = theta_star if (theta_star is not None and converged.get(theta_star)) else 0.0
dimless = {}
for tag, T in res.items():
    r0 = T[f'th{th0}_k2']['rate0'] / 60.0; sp = T['speed']
    est = np.median([c['est_over_true'] for c in ctl_speed.values()]) if ctl_speed else 1.0
    dimless[tag] = dict(rate0_per_min=r0 * 60, per_spacing=r0 * sp['spacing_px'] / sp['v_px_per_s'] if sp['v_px_per_s'] > 0 else None)
    if dimless[tag]['per_spacing']: dimless[tag]['over_null'] = dimless[tag]['per_spacing'] / NULL2D

out = dict(families={k: k for k in FAM}, thetas=THETAS, theta_star=theta_star, theta_table=th_table, control_keep_at_theta_star=ctl_keep,
           efficiency={f'{k[0]}_{k[1]}_{k[2]}_{k[3]}': v for k, v in F.items()}, exact={f'{k[0]}_{k[1]}_{k[2]}': v for k, v in EX.items()},
           holdout=hold, calerr={f'{k[0]}_{k[1]}': v for k, v in calerr.items()}, sun=res, npass=npass, criteria_counts=crit,
           holdout_ok=hold_ok, converged=converged, control_speed=ctl_speed, dimensionless=dimless, checks=checks, problems=problems)
os.makedirs(f'{S}/results', exist_ok=True)
json.dump(out, open(f'{S}/results/summary.json', 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))

# ---------- 7. tables ----------
M = ['# Sun swap rate at step 0: tables (generated by fit_sz.py)', '']
M += ['## Continuity threshold (primary setting, 10 s, P = 20 s)', '', '| theta | real | shuffled | shuffled / real |', '|---|---|---|---|']
M += [f'| {th} | {d["real"]} | {d["shuffled"]} | {d["ratio"]:.2f} |' for th, d in th_table.items()]
M += ['', f'theta* = {theta_star}; control (speed 1, texture 0) keeps {ctl_keep if ctl_keep is None else round(ctl_keep, 3)} of its swaps at theta*.', '']
M += ['## Efficiency f (Sun-like mean of speed 1, texture 0 and 1), steps 10 / 20 / 30 / 40 / 60 / 80 s', '', '| theta | window | f | exact (texture 0) |', '|---|---|---|---|']
for th in TH_USED:
    for fam in FAM:
        M.append(f'| {th} | {fam} | ' + ' / '.join(f'{fcal(fam, s, th):.2f}' for s in STEPS) + ' | ' + ' / '.join(str(EX[((1, 0), fam, s)]) for s in STEPS) + ' |')
M += ['', '## Held-out control (seed 2): step-0 line / exact step-0 line (Sun-like calibration)', '', '| theta | window | v1 z0 | v1 z1 | v2 z0 | v2 z1 | exact change 0 to 80 s (v1 z0) |', '|---|---|---|---|---|---|---|']
for th in TH_USED:
    for fam in FAM:
        g = lambda v, z: hold.get(f'th{th}_{fam}_v{v}_z{z}', {}).get('sunlike0_ratio', np.nan)
        M.append(f'| {th} | {fam} | {g(1,0):.2f} | {g(1,1):.2f} | {g(2,0):.2f} | {g(2,1):.2f} | {hold.get(f"th{th}_{fam}_v1_z0", {}).get("exact_change_0_80", np.nan):+.0%} |')
for th in TH_USED:
    M += ['', f'## Sun, theta = {th}: step-0 rate (persistent swaps per cell per minute), line through 10 to 80 s', '',
          '| setting | window | raw 10 / 80 s | corrected 10 / 80 s | step 0 line +- u | parabola | short line | floor-subtracted | change 0 to 80 s | shuffled/real 10 s | hold-out pred / obs 10 s | C1 C2 C3 C4 C5 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for tag, T in res.items():
        for fam in FAM:
            d = T[f'th{th}_{fam}']; fl = d['floor_sub']['intercept'] if d['floor_sub'] else np.nan
            cc = ' '.join('y' if d[c] else 'n' for c in ('C1', 'C2', 'C3', 'C4', 'C5'))
            M.append(f'| {tag} | {fam} | {d["raw"][0]:.3f} / {d["raw"][-1]:.3f} | {d["corrected"][0]:.3f} / {d["corrected"][-1]:.3f} | {d["rate0"]:.3f} +- {d["u"]:.3f} | '
                     f'{d["parabola"]["intercept"]:.3f} | {d["short"]["intercept"]:.3f} | {fl:.3f} | {d["change_0_80"]:+.0%} | {d["shuf_over_real_10"]:.2f} | '
                     f'{d["holdout_pred10"]:.3f} / {d["holdout_obs10"]:.3f} | {cc} |')
    M += ['', f'Criteria passed (all six judged windows) out of {len(res)} settings: ' + ', '.join(f'{c} {n}' for c, n in crit[th].items()) +
          f'; all five: {npass[th]}. Held-out control within 15% (k2): {hold_ok[th]}. Converged: {converged[th]}.']
    meds = {fam: float(np.median([res[t][f'th{th}_{fam}']['rate0'] for t in res])) for fam in FAM}
    M += ['', 'Median step-0 rate over the 13 settings by window: ' + ', '.join(f'{k} {v:.3f}' for k, v in meds.items())]
    out.setdefault('medians', {})[str(th)] = meds
M += ['', '## Cell speed and units', '', '| setting | msd (px^2) at 10 / 20 / 30 / 40 s | exponent of msd vs step | v (px/s) | jitter (px) | spacing (px) | step-0 rate per spacing of rms displacement (k2) | / 3.04 |', '|---|---|---|---|---|---|---|---|']
for tag, T in res.items():
    sp = T['speed']; dl = dimless[tag]
    M.append(f'| {tag} | ' + ' / '.join(f'{x:.1f}' for x in sp['msd_px2'][:4]) + f' | {sp["d2_exponent"]:.2f} | {sp["v_px_per_s"]:.4f} | {sp["jitter_px"]:.2f} | {sp["spacing_px"]:.1f} | '
             f'{dl["per_spacing"]:.2f} | {dl.get("over_null", np.nan):.2f} |')
M += ['', '| control | true rms seed speed (px/s) | estimated | estimated / true | exact T1 per cell per spacing of rms displacement |', '|---|---|---|---|---|']
M += [f'| {k} | {d["v_true_px_s"]:.4f} | {d["v_est_px_s"]:.4f} | {d["est_over_true"]:.2f} | {d["exact_T1_per_cell_per_spacing"]:.2f} |' for k, d in ctl_speed.items()]
M += ['', '## Checks', ''] + [f'- {k}: {"PASS" if v else "FAIL"}' for k, v in checks.items()] + [f'- problem: {p}' for p in problems]
open(f'{S}/results/summary.md', 'w').write('\n'.join(M) + '\n')
json.dump(out, open(f'{S}/results/summary.json', 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
repro = [k for k in checks if k.startswith('repro') or k.startswith('list_rule')]
ok = not problems and all(checks[k] for k in repro) and len(res) == 13
print('VERDICT', 'converged' if any(converged.values()) else 'not converged', json.dumps(npass), json.dumps({str(k): v for k, v in converged.items()}))
print('FINAL ok' if ok else 'FINAL FAIL ' + '; '.join([k for k in repro if not checks[k]] + problems + ([] if len(res) == 13 else ['settings missing'])))
