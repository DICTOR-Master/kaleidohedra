"""Tables and control checks for the skeleton job (README section "The skeleton: persistence or reappearance").
Usage: skeleton_combine.py RESULTSDIR   (reads RESULTSDIR/anal/*.json, RESULTSDIR/voro/*.json; writes summary.json, summary.md)"""
import sys, os, json, glob
import numpy as np

R = sys.argv[1]
A = {}
for f in glob.glob(f'{R}/anal/*.json'):
    d = json.load(open(f)); A[(d['run'][:2], float(d['dz']), d['order'], d['step'])] = d
B = {}
for f in glob.glob(f'{R}/anal2/*.json'):
    d = json.load(open(f)); B[(d['run'][:2], float(d['dz']), d['order'], d['step'])] = d
V = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f'{R}/voro/*.json')}
PLANES = [('en', '0.1'), ('en', '0.0'), ('en', '0.2'), ('qs', '0.1')]
out = dict(planes={}, voro={}, checks={})
md = ['# Skeleton of the granulation: persistence or reappearance (job sun-skeleton)', '',
      'r = 144 km, gap window G = 60 s, apparently persistent = span >= 5 min unless stated. Times in s.', '']


def peak(freq, pw, lo=2.0, hi=8.0):
    """Largest excess over a log-log line fitted to 1-20 mHz, inside lo-hi mHz: (frequency, ratio)."""
    f = np.array(freq); p = np.array(pw); sel = (f >= 1.0) & (f <= 20.0)
    if sel.sum() < 5: return None, None
    c = np.polyfit(np.log(f[sel]), np.log(p[sel]), 1)
    ex = p / np.exp(np.polyval(c, np.log(np.maximum(f, 1e-9))))
    band = (f >= lo) & (f <= hi)
    if not band.any(): return None, None
    i = np.argmax(np.where(band, ex, -1))
    return float(f[i]), float(ex[i])


def plane_row(d, b):
    r3 = d['by_r']['3']; s = r3['sites']['60']; rc = r3['recurrence']; L = b['lanes'] if b else d['lanes']
    pf, pr = peak(L['freq_mHz'], L['power']); uf, ur = peak(d['uz']['freq_mHz'], d['uz']['power'])
    return dict(
        cell_overlap_km=d['cells_overlap']['km_median'], cell_overlap_half=d['cells_overlap']['survival']['half_s'],
        cell_centre_km=r3['cells_centre']['km_median'], cell_centre_half=r3['cells_centre']['survival']['half_s'],
        corner_km=r3['corners']['km_median'], corner_median=r3['corners']['median'], corner_half=r3['corners']['survival']['half_s'],
        corner_q90=r3['corners']['q90'], corner_n=r3['corners']['n'],
        sink_km=r3['sinks']['km_median'], sink_half=r3['sinks']['survival']['half_s'],
        site_half=s['survival_site']['half_s'], lane_efold=d['lanes']['efold_s'],
        fam_km=d['families_split']['km_median'], fam_median=d['families_split']['median'], fam_q90=d['families_split']['q90'],
        fam_children=d['families_split']['share_with_children'], famsm_km=d['families_splitmerge']['km_median'],
        single_median=d['cells_overlap']['median'], single_q90=d['cells_overlap']['q90'],
        sites_n=s['n_apparent'], share_a=s['share_a'], share_b=s['share_b'], share_c=s['share_c'], share_a_strict=s['share_a_strict'],
        gaps_per_site=s['gaps_per_site'], gap_median=s['gap_median_s'], absent_share=s['absent_share'],
        ncells_median=s['ncells_median'], ncells_per_min=s['ncells_per_min'], span_median=s['span_median_s'],
        sink_sites_c=s['sinks']['share_c'],
        reform=s['reform']['reform_share'], reform_uniform=s['reform']['chance_share'], reform_shifted=s['reform']['shifted_share'],
        reform_ratio_shifted=s['reform']['ratio_shifted'],
        born_near_death=rc['born_near_death'], bnd_uniform=rc['chance_uniform_death'], bnd_shifted=rc['shifted_death'],
        cover=rc['birth_cover_long_corner'], cover_chance=rc['chance_cover_long_corner'], cover_shifted=rc['shifted_cover_long_corner'],
        births=rc['births'], lane_share=L['lane_share'], lane_ac=L['ac_features'], lane_occ50_no_gap=L['occ50_no_gap'],
        lane_occ50_absent=L['occ50_absent_share'], lane_peak_mHz=pf, lane_peak_ratio=pr, uz_peak_mHz=uf, uz_peak_ratio=ur,
        ac_10min=L['autocorr'][min(len(L['autocorr']) - 1, int(600 / d['dt']))], ac_20min=L['autocorr'][-1],
        **(second(b) if b else {}))


def second(b):
    rf = b['reform']; q = b['lanes'].get('ac_quadrant_features', [])
    bumps = [x.get('bump', 0.0) for x in q]; pos = [x.get('next_max_s') for x in q]
    return dict(cell_half2=b['cells']['half_s'], fam_half=b['families_split']['half_s'], fam_n=b['families_split']['n_families_per_frame'],
                famsm_half=b['families_splitmerge']['half_s'], famsm_n=b['families_splitmerge']['n_families_per_frame'], cells_n=b['cells_per_frame'],
                fam_S=b['families_split']['S'], famsm_S=b['families_splitmerge']['S'],
                reform2={r: {g: dict(c=v['corners']['reformed'], c_null=v['corners']['null_reformed'], c_ratio=v['corners']['ratio'], c_n=v['corners']['vanishings'],
                                     s=v['sinks']['reformed'], s_null=v['sinks']['null_reformed'], s_ratio=v['sinks']['ratio'])
                             for g, v in rf[r].items()} for r in rf},
                quad_bumps=bumps, quad_next_max_s=pos)


fmt = lambda x: '-' if x is None else (f'{x:.3g}' if isinstance(x, float) else str(x))
for run, dz in PLANES:
    P = {}
    for o in ('real', 'rev', 'shuf:7'):
        for st in (1, 2, 4, 8):
            d = A.get((run, float(dz), o, st))
            if d: P[f'{o}/{st}'] = plane_row(d, B.get((run, float(dz), o, st)))
    # stability over r (real, step 1)
    d = A.get((run, float(dz), 'real', 1))
    if d:
        P['by_r'] = {r: dict(corner_half=d['by_r'][r]['corners']['survival']['half_s'], cell_centre_half=d['by_r'][r]['cells_centre']['survival']['half_s'],
                             sink_half=d['by_r'][r]['sinks']['survival']['half_s'], corner_km=d['by_r'][r]['corners']['km_median'],
                             share_c=d['by_r'][r]['sites']['60']['share_c'], share_a=d['by_r'][r]['sites']['60']['share_a'],
                             share_b=d['by_r'][r]['sites']['60']['share_b'],
                             reform_ratio_shifted=d['by_r'][r]['sites']['60']['reform']['ratio_shifted']) for r in d['by_r']}
        P['by_G'] = {g: dict(share_a=d['by_r']['3']['sites'][g]['share_a'], share_b=d['by_r']['3']['sites'][g]['share_b'],
                             share_c=d['by_r']['3']['sites'][g]['share_c'], n=d['by_r']['3']['sites'][g]['n_apparent'],
                             site_half=d['by_r']['3']['sites'][g]['survival_site']['half_s']) for g in d['by_r']['3']['sites']}
        b1 = B.get((run, float(dz), 'real', 1)) or d
        P['curves'] = dict(lags=d['lanes']['lags_s'], lane_ac=b1['lanes']['autocorr'], lane_ac_quadrants=b1['lanes'].get('autocorr_quadrants'),
                           fam_S=P['real/1'].get('fam_S'),
                           corner_S=d['by_r']['3']['corners']['survival']['S'], cell_S=d['cells_overlap']['survival']['S'],
                           centre_S=d['by_r']['3']['cells_centre']['survival']['S'], site_S=d['by_r']['3']['sites']['60']['survival_site']['S'],
                           freq=d['lanes']['freq_mHz'], lane_pw=d['lanes']['power'], uz_freq=d['uz']['freq_mHz'], uz_pw=d['uz']['power'])
        ds = A.get((run, float(dz), 'shuf:7', 1))
        if ds: P['curves']['lane_ac_shuf'] = (B.get((run, float(dz), 'shuf:7', 1)) or ds)['lanes']['autocorr']; P['curves']['corner_S_shuf'] = ds['by_r']['3']['corners']['survival']['S']
    out['planes'][f'{run}/{dz}'] = P
    md += [f'## {run} uz {dz} Mm', '',
           '| order/step | cell overlap KM / half | cell centre KM / half | corner KM / half | sink KM / half | site half | lane e-fold | sites (a/b/c, strict a) | re-form / uniform / shifted | born near death / uniform / shifted | cover / chance |',
           '|---|---|---|---|---|---|---|---|---|---|---|']
    for k, x in P.items():
        if '/' not in k: continue
        md.append(f"| {k} | {fmt(x['cell_overlap_km'])} / {fmt(x['cell_overlap_half'])} | {fmt(x['cell_centre_km'])} / {fmt(x['cell_centre_half'])} | "
                  f"{fmt(x['corner_km'])} / {fmt(x['corner_half'])} | {fmt(x['sink_km'])} / {fmt(x['sink_half'])} | {fmt(x['site_half'])} | {fmt(x['lane_efold'])} | "
                  f"{x['sites_n']}: {x['share_a']:.2f}/{x['share_b']:.2f}/{x['share_c']:.2f}, {x['share_a_strict']:.2f} | "
                  f"{fmt(x['reform'])} / {fmt(x['reform_uniform'])} / {fmt(x['reform_shifted'])} | {fmt(x['born_near_death'])} / {fmt(x['bnd_uniform'])} / {fmt(x['bnd_shifted'])} | "
                  f"{fmt(x['cover'])} / {fmt(x['cover_chance'])} |")
    if 'real/1' in P:
        x = P['real/1']
        if 'reform2' in x:
            md += ['', 'Re-formation after a true vanishing (corner / sink; share re-formed, null at the same place 10 min or more away, ratio), real 10 s: ' +
                   '; '.join(f"r {r} G {g}: {v['c']:.3f}/{v['c_null']:.3f} = {fmt(v['c_ratio'])}, sinks {v['s']:.3f}/{v['s_null']:.3f} = {fmt(v['s_ratio'])}" for r, gg in x['reform2'].items() for g, v in gg.items()),
                   f"Families as presence: cells half {fmt(x['cell_half2'])} s ({fmt(x['cells_n'])} per frame), split families half {fmt(x['fam_half'])} s ({fmt(x['fam_n'])} per frame), split+merge families half {fmt(x['famsm_half'])} s ({fmt(x['famsm_n'])} per frame).",
                   f"Lane autocorrelation secondary maximum per quadrant: bumps {[round(v, 3) for v in x['quad_bumps']]} at {x['quad_next_max_s']} s."]
            for o in ('shuf:7/1', 'rev/1', 'real/2', 'real/4', 'real/8'):
                y = P.get(o)
                if y and 'reform2' in y:
                    v = y['reform2']['3']['60']; md.append(f"  {o}: re-form r 3 G 60 corner {v['c']:.3f}/{v['c_null']:.3f} = {fmt(v['c_ratio'])}, sinks {v['s']:.3f}/{v['s_null']:.3f} = {fmt(v['s_ratio'])}; fam half {fmt(y['fam_half'])}, cell half {fmt(y['cell_half2'])}")
        md += ['', f"Families (split): KM median {fmt(x['fam_km'])}, median {fmt(x['fam_median'])}, q90 {fmt(x['fam_q90'])}, share with children {fmt(x['fam_children'])}; "
                   f"single cells median {fmt(x['single_median'])}, q90 {fmt(x['single_q90'])}; split+merge KM {fmt(x['famsm_km'])}.",
               f"Sites: gaps per site {fmt(x['gaps_per_site'])}, gap median {fmt(x['gap_median'])} s, absent share {fmt(x['absent_share'])}, distinct cells median {fmt(x['ncells_median'])} "
               f"({fmt(x['ncells_per_min'])} per min), span median {fmt(x['span_median'])} s; sink sites re-formed {fmt(x['sink_sites_c'])}.",
               f"Lanes: share {fmt(x['lane_share'])}, autocorrelation at 10 / 20 min {fmt(x['ac_10min'])} / {fmt(x['ac_20min'])}, secondary maximum {x['lane_ac']}; "
               f"pixels lane in >= half the frames with no gap {fmt(x['lane_occ50_no_gap'])}, absent share {fmt(x['lane_occ50_absent'])}; "
               f"spectral excess 2-8 mHz: lanes {fmt(x['lane_peak_ratio'])} at {fmt(x['lane_peak_mHz'])} mHz, uz {fmt(x['uz_peak_ratio'])} at {fmt(x['uz_peak_mHz'])} mHz.",
               'By r (px): ' + '; '.join(f"{r}: corner half {fmt(v['corner_half'])}, centre half {fmt(v['cell_centre_half'])}, a/b/c {v['share_a']:.2f}/{v['share_b']:.2f}/{v['share_c']:.2f}, re-form/shifted {fmt(v['reform_ratio_shifted'])}" for r, v in P['by_r'].items()),
               'By G (s): ' + '; '.join(f"{g}: n {v['n']}, a/b/c {v['share_a']:.2f}/{v['share_b']:.2f}/{v['share_c']:.2f}, site half {fmt(v['site_half'])}" for g, v in P['by_G'].items()), '']

md += ['## Moving-Voronoi control (exact circumcentre corners and the pipeline)', '',
       '| control | step | exact triangle KM / half | exact corner KM / half | pipeline corner KM / half | exact sites a/b/c | pipeline sites a/b/c |', '|---|---|---|---|---|---|---|']
for name, v in sorted(V.items()):
    out['voro'][name] = {}
    for st, B in v['by_step'].items():
        e = B['3']
        row = dict(tri_km=B['exact_triangle']['km_median'], tri_half=e['triangle_survival']['half_s'],
                   ex_km=e['corners_exact']['km_median'], ex_half=e['corners_exact']['survival']['half_s'],
                   pp_km=e['corners_pipeline']['km_median'], pp_half=e['corners_pipeline']['survival']['half_s'],
                   ex_sites=[e['sites_exact'][k] for k in ('share_a', 'share_b', 'share_c')], pp_sites=[e['sites_pipeline'][k] for k in ('share_a', 'share_b', 'share_c')],
                   ex_ncells_per_min=e['sites_exact']['ncells_per_min'], pp_ncells_per_min=e['sites_pipeline']['ncells_per_min'])
        out['voro'][name][st] = row
        md.append(f"| {name} | {int(st) * 10} s | {fmt(row['tri_km'])} / {fmt(row['tri_half'])} | {fmt(row['ex_km'])} / {fmt(row['ex_half'])} | {fmt(row['pp_km'])} / {fmt(row['pp_half'])} | "
                  + '/'.join(f'{x:.2f}' for x in row['ex_sites']) + ' | ' + '/'.join(f'{x:.2f}' for x in row['pp_sites']) + ' |')

# control checks (criteria written before the run)
C = out['checks']
for key, P in out['planes'].items():
    if 'real/1' not in P or 'shuf:7/1' not in P: continue
    x, s, rv = P['real/1'], P['shuf:7/1'], P.get('rev/1')
    c = {}
    c['shuffled_corner_half_s'] = s['corner_half']
    c['shuffled_pass_corner'] = s['corner_half'] is not None and s['corner_half'] <= 20
    c['shuffled_reform_ratio_shifted'] = s['reform_ratio_shifted']
    c['shuffled_pass_reform'] = s['reform_ratio_shifted'] is not None and 0.8 <= s['reform_ratio_shifted'] <= 1.25
    if 'reform2' in s:
        c['shuffled_reform2_ratio'] = s['reform2']['3']['60']['c_ratio']; c['real_reform2_ratio'] = x['reform2']['3']['60']['c_ratio']
        c['shuffled_pass_reform2'] = c['shuffled_reform2_ratio'] is not None and 0.8 <= c['shuffled_reform2_ratio'] <= 1.25
        c['step_reform2_ratio'] = [P[f'real/{st}']['reform2']['3']['60']['c_ratio'] if f'real/{st}' in P and 'reform2' in P[f'real/{st}'] else None for st in (1, 2, 4, 8)]
        c['r_reform2_ratio'] = [x['reform2'][r]['60']['c_ratio'] for r in sorted(x['reform2'])]
        c['step_fam_half'] = [P[f'real/{st}'].get('fam_half') if f'real/{st}' in P else None for st in (1, 2, 4, 8)]
        c['step_cell_half2'] = [P[f'real/{st}'].get('cell_half2') if f'real/{st}' in P else None for st in (1, 2, 4, 8)]
    c['shuffled_bnd_ratio_shifted'] = (s['born_near_death'] / s['bnd_shifted']) if s['bnd_shifted'] else None
    c['real_reform_ratio_shifted'] = x['reform_ratio_shifted']
    c['real_bnd_ratio_shifted'] = (x['born_near_death'] / x['bnd_shifted']) if x['bnd_shifted'] else None
    c['real_cover_ratio'] = (x['cover'] / x['cover_chance']) if x['cover_chance'] else None
    c['shuffled_cover_ratio'] = (s['cover'] / s['cover_chance']) if s['cover_chance'] else None
    if rv:
        rel = lambda a, b: abs(a - b) / max(abs(b), 1e-9) if a is not None and b is not None else None
        c['reversed_rel_diff'] = {k: rel(rv[k], x[k]) for k in ('corner_half', 'sink_half', 'cell_centre_half', 'corner_km', 'share_c', 'site_half', 'cell_overlap_half')}
        c['reversed_pass'] = all(v is not None and v <= 0.05 for k, v in c['reversed_rel_diff'].items() if k in ('corner_half', 'sink_half', 'cell_centre_half', 'corner_km'))
    def spread(vals):
        v = [a for a in vals if a is not None]
        return (max(v) - min(v)) / max(min(v), 1e-9) if len(v) == len(vals) and v else None
    steps = [P.get(f'real/{st}') for st in (1, 2, 4, 8)]
    for q in ('corner_half', 'cell_overlap_half', 'cell_centre_half', 'sink_half', 'site_half', 'lane_efold', 'share_c', 'share_a', 'share_b'):
        c[f'step_{q}'] = [st[q] if st else None for st in steps]
        c[f'step_spread_{q}'] = spread(c[f'step_{q}'])
        if q in P['real/1'] and 'by_r' in P and q in next(iter(P['by_r'].values())):
            c[f'r_{q}'] = [P['by_r'][r][q] for r in sorted(P['by_r'])]
            c[f'r_spread_{q}'] = spread(c[f'r_{q}'])
    C[key] = c
md += ['', '## Control checks', '', '```', json.dumps(C, indent=1), '```']
json.dump(out, open(f'{R}/summary.json', 'w'))
open(f'{R}/summary.md', 'w').write('\n'.join(md) + '\n')
ok = len(out['planes']) == 4 and all('real/1' in P for P in out['planes'].values()) and len(V) == 4 and len(B) == 48
print('COMBINE', len(A), 'analyses', len(V), 'controls')
print('FINAL ok' if ok else 'FINAL FAIL')
