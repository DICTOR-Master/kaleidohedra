"""Summary of the full space-time run (job sun-tilt, 16 Nov 2026; README sections "Space-time slicing at a tilt" and "Granule tubes in
space-time: prisms and scutoids"). Applies the definitions and verdict rules written in the README BEFORE the run:
  Part A: counts per core volume (per 1000 Mm^2 min) of persistent swaps, logger births and logger deaths in each direction;
  spread of a block over a direction set = std / mean (population); TILT = the 14 tilted directions, TILT3 = the 13 tilted directions
  at v >= 3 km/s; s_PV = median spread of the 15 Poisson-Voronoi blocks (the yardstick); a Sun group (labelling, run, depth, order)
  is the sum of its four quadrants; a quadrant is compared with s_PV * sqrt(n_PV / n_quadrant) (counting noise); Morse rate = share
  of interior cells with (pieces born) - (joins) = Euler characteristic, mean over TILT; control-1 rate = median over the PV blocks.
  Part B: tube JSONs; share of scutoid tubes among tubes of 3 min or more; stability ranges; verdicts.
Usage: tilt_full_summary.py RESULTSDIR   -> RESULTSDIR/summary.json, summary.md; prints FINAL-SUMMARY ok"""
import json, glob, sys, os, re
import numpy as np
from collections import defaultdict
R = sys.argv[1]
TILT = [(th, 3.0, az) for th in (10, 20, 30, 45) for az in ('+x', '-x', '+y')] + [(30, 1.5, '+x'), (30, 6.0, '+x')]
TILT3 = [d for d in TILT if d[1] >= 3]
Q = ('swaps', 'births', 'deaths')
blocks = {}
for l in open(f'{R}/blocks.jsonl'):
    b = json.loads(l[6:]); blocks[b['name']] = b
sl = {}
for f in glob.glob(f'{R}/slices/*.json'):
    r = json.load(open(f))
    sl[(r['block'], float(r['theta']), float(r['v']), r['az'], bool(r.get('rev')), bool(r.get('half')))] = r


def counts(r):
    if r.get('gated'): return None
    k = 1000.0 / r['core_volume_Mm2min']; ce = r['core_events']
    return dict(swaps=r['core_swaps_persistent'] * k, births=ce.get('birth', 0) * k, deaths=ce.get('death', 0) * k,
                swaps_all=r['core_swaps_all'] * k, raw_swaps=r['core_swaps_persistent'], raw_births=ce.get('birth', 0),
                raw_deaths=ce.get('death', 0), pieces=r['truth_core'].get('new piece of a present cell', 0) * k,
                morse=r['morse_interior_cells'].get('holds', 0) / max(1, sum(r['morse_interior_cells'].values())),
                euler_bad=r['planes_failing_euler'] / max(1, r['planes']), balance_bad=r['balance_failures'])


def get(name, d, rev=False, half=False):
    r = sl.get((name, float(d[0]), float(d[1]), d[2], rev, half))
    return counts(r) if r else None


def spread(vals):
    v = np.array(vals, float)
    return float(v.std() / v.mean()) if len(v) and v.mean() > 0 else None


out = dict(partA={}, partB={})
A = out['partA']
# ---- control 1: Poisson-Voronoi
pv = sorted(n for n in blocks if n.startswith('pv_'))
pvres = {}
for n in pv:
    ex = blocks[n]['exact']
    sp = {k: (max(e[k] for e in ex.values()) - min(e[k] for e in ex.values())) / np.mean([e[k] for e in ex.values()]) for k in ('1', '2', '3')}
    rows = {d: get(n, d) for d in TILT}
    pvres[n] = dict(exact_range_births=sp['1'], exact_range_swaps=sp['2'], exact_range_deaths=sp['3'],
                    exact_index0_or_4=sum(e['0'] + e['4'] for e in ex.values()), theorem_bound=blocks[n]['theorem_bound'],
                    exact_swaps_per_birth=float(np.mean([e['2'] / e['1'] for e in ex.values()])),
                    spread_tilt={q: spread([rows[d][q] for d in TILT if rows[d]]) for q in Q},
                    spread_tilt3={q: spread([rows[d][q] for d in TILT3 if rows[d]]) for q in Q},
                    morse=float(np.mean([rows[d]['morse'] for d in TILT if rows[d]])),
                    detected_swaps_over_exact=float(np.mean([rows[d]['raw_swaps'] / max(1, ex[f'{d[0]}_{d[1]}_{d[2]}']['2']) for d in TILT if rows[d]])),
                    n_mean_swaps=float(np.mean([rows[d]['raw_swaps'] for d in TILT if rows[d]])),
                    n_mean_births=float(np.mean([rows[d]['raw_births'] for d in TILT if rows[d]])))
sPV = {s: {q: float(np.median([p[f'spread_{s}'][q] for p in pvres.values()])) for q in Q} for s in ('tilt', 'tilt3')}
morse_c1 = float(np.median([p['morse'] for p in pvres.values()]))
nPV = {q: float(np.median([p['n_mean_swaps' if q == 'swaps' else 'n_mean_births'] for p in pvres.values()])) for q in Q}
A['control1_pv'] = dict(blocks=pvres, s_PV=sPV, morse_rate=morse_c1,
                        exact_within_3pct=sum(all(p[f'exact_range_{k}'] <= 0.03 for k in ('births', 'swaps', 'deaths')) for p in pvres.values()),
                        exact_max_range=max(max(p[f'exact_range_{k}'] for k in ('births', 'swaps', 'deaths')) for p in pvres.values()),
                        theorem_bound_holds=sum(p['theorem_bound']['holds_all_directions'] for p in pvres.values()), n=len(pvres))
# ---- control 2: moving Voronoi
mvres = {}
for n in sorted(x for x in blocks if x.startswith('mv_')):
    b = blocks[n]; rows = []
    for d in [(0, 3.0, '+x')] + TILT:
        c = get(n, d)
        if not c: continue
        vmax = b['seed_y_speed_kms_max'] if d[2] == '+y' else b['seed_x_speed_kms_max']
        slow = d[0] == 0 or vmax < d[1] / np.tan(np.radians(d[0]))
        bd = c['raw_births'] + c['raw_deaths']; sw = c['raw_swaps']
        rows.append(dict(dir=list(d), slow=bool(slow), births_deaths=bd, swaps=sw, share=bd / max(1, sw)))
    mvres[n] = dict(rows=rows, pass_2pct=all(r['share'] <= 0.02 for r in rows if r['slow']),
                    max_share_slow=max(r['share'] for r in rows if r['slow']))
A['control2_mv'] = mvres
# ---- control 3: time reversal
rv = {}
for n in sorted({k[0] for k in sl if k[4]}):
    diffs = []
    for d in [(0, 3.0, '+x')] + TILT:
        a, b = sl.get((n, float(d[0]), float(d[1]), d[2], False, False)), sl.get((n, float(d[0]), float(d[1]), d[2], True, False))
        if not a or not b: continue
        diffs.append(dict(dir=list(d), swaps=(a['core_swaps_all'], b['core_swaps_all']),
                          births_vs_rev_deaths=(a['core_events'].get('birth', 0), b['core_events'].get('death', 0)),
                          deaths_vs_rev_births=(a['core_events'].get('death', 0), b['core_events'].get('birth', 0)),
                          planes=(a['planes'], b['planes'])))
    rv[n] = dict(rows=diffs, identical=all(x['swaps'][0] == x['swaps'][1] and x['births_vs_rev_deaths'][0] == x['births_vs_rev_deaths'][1]
                                            and x['deaths_vs_rev_births'][0] == x['deaths_vs_rev_births'][1] for x in diffs),
                 max_rel_diff=max(max(abs(p[0] - p[1]) / max(1, p[0]) for p in (x['swaps'], x['births_vs_rev_deaths'], x['deaths_vs_rev_births'])) for x in diffs) if diffs else None,
                 same_planes=all(x['planes'][0] == x['planes'][1] for x in diffs))
A['control3_reversal'] = rv
# ---- half step (sampling check)
hs = {}
for n in sorted({k[0] for k in sl if k[5]}):
    rows = []
    for d in [(0, 3.0, '+x')] + TILT:
        a, b = get(n, d), get(n, d, half=True)
        if a and b: rows.append(dict(dir=list(d), swaps=(a['swaps'], b['swaps']), births=(a['births'], b['births'])))
    hs[n] = dict(rows=rows, swaps_ratio_half_over_full=float(np.mean([r['swaps'][1] / max(1e-9, r['swaps'][0]) for r in rows])) if rows else None)
A['half_step'] = hs
# ---- Sun groups
groups = defaultdict(list)
for n, b in blocks.items():
    if b['kind'].startswith('sun'):
        lab = b['kind'] + (f"_thr{b['name'].split('_thr')[1]}" if b['kind'] == 'sunA' else '')
        groups[(lab, b['run'][:2], b['dz'], b['order'])].append(n)
sun = {}
for key, names in sorted(groups.items()):
    gated = [n for n in names if blocks[n].get('gate_pass') is False]
    g = dict(blocks=len(names), gated=len(gated), largest_marker_share=[blocks[n].get('largest_marker_share') for n in sorted(names)])
    live = [n for n in names if n not in gated]
    if live:
        per_dir = {}
        for d in [(0, 3.0, '+x')] + TILT:
            cs = [get(n, d) for n in live]
            if any(c is None for c in cs): continue
            vol = len(cs)
            per_dir[d] = {q: sum(c[q] for c in cs) / vol for q in Q + ('pieces', 'swaps_all')}
            per_dir[d]['morse'] = float(np.mean([c['morse'] for c in cs]))
            per_dir[d]['raw'] = {q: sum(c['raw_' + q] for c in cs) for q in Q}
        g['quadrants_used'] = len(live)
        g['per_direction'] = {f'{d[0]}_{d[1]}_{d[2]}': v for d, v in per_dir.items()}
        g['spread_tilt'] = {q: spread([per_dir[d][q] for d in TILT if d in per_dir]) for q in Q}
        g['spread_tilt3'] = {q: spread([per_dir[d][q] for d in TILT3 if d in per_dir]) for q in Q}
        g['ratio_to_sPV_tilt'] = {q: g['spread_tilt'][q] / sPV['tilt'][q] for q in Q}
        g['ratio_to_sPV_tilt3'] = {q: g['spread_tilt3'][q] / sPV['tilt3'][q] for q in Q}
        g['theta0_over_tilt_mean'] = {q: per_dir[(0, 3.0, '+x')][q] / np.mean([per_dir[d][q] for d in TILT3]) for q in Q} if (0, 3.0, '+x') in per_dir else None
        g['morse_tilt'] = float(np.mean([per_dir[d]['morse'] for d in TILT if d in per_dir]))
        g['pieces_by_dir'] = {f'{d[0]}_{d[1]}_{d[2]}': per_dir[d]['pieces'] for d in per_dir}
        # quadrants against the counting-scaled yardstick
        qok = []
        for n in live:
            rows = {d: get(n, d) for d in TILT}
            ok = True
            for q in Q:
                nq = np.mean([rows[d]['raw_' + q] for d in TILT])
                yard = sPV['tilt'][q] * np.sqrt(nPV[q] / max(1.0, nq))
                ok &= spread([rows[d][q] for d in TILT]) <= yard
            qok.append(bool(ok))
        g['quadrants_within_scaled_yardstick'] = sum(qok)
    sun['/'.join(key)] = g
A['sun'] = sun
# shuffled control (5) and verdicts
def verdict(g, gs):
    if 'spread_tilt' not in g: return 'not tested (percolation gate)'
    est = all(g['ratio_to_sPV_tilt'][q] <= 1 for q in Q) and g['quadrants_within_scaled_yardstick'] == g['quadrants_used'] and g['morse_tilt'] >= morse_c1
    con = all(g['ratio_to_sPV_tilt3'][q] <= 1 for q in Q)
    shuf_breaks = gs is not None and 'spread_tilt' in gs and all(gs['ratio_to_sPV_tilt'][q] > 3 for q in ('swaps', 'births')) and gs['morse_tilt'] < 0.5 * g['morse_tilt']
    ctrl = A['control1_pv']['exact_within_3pct'] == A['control1_pv']['n']
    if any(g['ratio_to_sPV_tilt'][q] > 2 for q in Q) or (gs is not None and not shuf_breaks): v = 'NOT CONFIRMED'
    elif est and ctrl and shuf_breaks: v = 'ESTABLISHED'
    elif con and ctrl: v = 'CONSISTENT'
    else: v = 'NOT CONFIRMED'
    return v
for k, g in sun.items():
    lab, run, dz, order = k.split('/')
    if order != 'real': continue
    gs = sun.get(f'{lab}/{run}/{dz}/shuf:7')
    g['shuffled_breaks'] = None if gs is None or 'spread_tilt' not in gs else dict(
        ratio_swaps=gs['ratio_to_sPV_tilt']['swaps'], ratio_births=gs['ratio_to_sPV_tilt']['births'], morse=gs['morse_tilt'], morse_real=g.get('morse_tilt'))
    g['verdict'] = verdict(g, gs)
# ---- Part B
B = out['partB']
for f in sorted(glob.glob(f'{R}/tubes/*.json')):
    if f.endswith('_tubes.json'): continue
    B[os.path.basename(f)[:-5]] = json.load(open(f))
json.dump(out, open(f'{R}/summary.json', 'w'), indent=1, default=str)
# ---- markdown tables
md = []
c1 = A['control1_pv']
md.append(f"Control 1 (PV, {c1['n']} blocks): exact range within 3%: {c1['exact_within_3pct']} of {c1['n']} (largest range {c1['exact_max_range']:.3f}); "
          f"theorem bound holds in {c1['theorem_bound_holds']} of {c1['n']}; s_PV tilt {sPV['tilt']}; tilt3 {sPV['tilt3']}; Morse rate {morse_c1:.3f}")
for n, p in pvres.items():
    md.append(f"  {n}: exact ranges b/s/d {p['exact_range_births']:.3f}/{p['exact_range_swaps']:.3f}/{p['exact_range_deaths']:.3f}, idx0/4 {p['exact_index0_or_4']}, "
              f"swaps/birth {p['exact_swaps_per_birth']:.2f}, bound {p['theorem_bound']}, pipeline spread {p['spread_tilt']}, Morse {p['morse']:.3f}, detected/exact swaps {p['detected_swaps_over_exact']:.2f}")
for n, m in mvres.items(): md.append(f"Control 2 {n}: pass {m['pass_2pct']}, max share (slow directions) {m['max_share_slow']:.3f}; " + '; '.join(f"{r['dir']}: {r['births_deaths']}/{r['swaps']}" for r in m['rows']))
for n, m in rv.items(): md.append(f"Control 3 reversal {n}: identical {m['identical']}, same planes {m['same_planes']}, max rel diff {m['max_rel_diff']}")
for n, m in hs.items(): md.append(f"Half step {n}: swaps half/full {m['swaps_ratio_half_over_full']}")
md.append('')
md.append('| group | quadrants (gated) | spread swaps / births / deaths over 14 tilts (x s_PV) | same over 13 tilts v>=3 (x s_PV) | theta 0 / tilt mean (swaps) | Morse | quadrants within | verdict |')
md.append('|---|---|---|---|---|---|---|---|')
for k, g in sun.items():
    if 'spread_tilt' not in g:
        md.append(f"| {k} | {g['blocks']} ({g['gated']}) | gated: largest marker share {', '.join(f'{x:.2f}' for x in g['largest_marker_share'])} | | | | | {g.get('verdict', '')} |"); continue
    r1 = ' / '.join(f"{g['spread_tilt'][q]:.3f} ({g['ratio_to_sPV_tilt'][q]:.1f})" for q in Q)
    r3 = ' / '.join(f"{g['spread_tilt3'][q]:.3f} ({g['ratio_to_sPV_tilt3'][q]:.1f})" for q in Q)
    t0 = f"{g['theta0_over_tilt_mean']['swaps']:.2f}" if g['theta0_over_tilt_mean'] else ''
    md.append(f"| {k} | {g['quadrants_used']} ({g['gated']}) | {r1} | {r3} | {t0} | {g['morse_tilt']:.2f} | {g['quadrants_within_scaled_yardstick']} | {g.get('verdict', '')} |")
md.append('')
md.append('| tube run | tubes (3 min+) | scutoid share 3 min+ | with a lateral corner | changes / corners per tube (mean) | per min | rho(changes, life) | rho(changes, area) | life mean (min) |')
md.append('|---|---|---|---|---|---|---|---|---|')
for k, r in B.items():
    if 'scutoid_share_3min' not in r:
        md.append(f"| {k} | " + ', '.join(f"{w}: exact {r[w]['exact_scutoid_share']:.3f}, exact filtered {r[w]['exact_filtered_scutoid_share']:.3f}, pipeline {r[w]['pipeline_scutoid_share']:.3f}" for w in r if w.startswith('window')) + ' |'); continue
    if r.get('scutoid_share_3min') is None:
        md.append(f"| {k} | {r['tubes']} ({r['tubes_3min']}) | none | | | | | | |"); continue
    sp = r['spearman_3min']
    md.append(f"| {k} | {r['tubes']} ({r['tubes_3min']}) | {r['scutoid_share_3min']:.3f} | {r['corner_share_3min']:.3f} | {r['changes_3min']['mean']:.1f} / {r['corners_3min']['mean']:.1f} | "
              f"{r['changes_3min']['per_min']:.2f} / {r['corners_3min']['per_min']:.2f} | {sp['changes_life']:.2f} | {sp['changes_area']:.2f} | {r['life_3min']['mean_min']:.1f} |")
open(f'{R}/summary.md', 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))
print('FINAL-SUMMARY ok')
