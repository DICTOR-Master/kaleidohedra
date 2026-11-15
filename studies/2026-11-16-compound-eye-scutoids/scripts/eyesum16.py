#!/usr/bin/env python3
"""Pool the per-patch, per-segment results of eyerun16.py (gw16) into the study's numbers. Every cell, counted pair and neighbour
change is counted once, in the patch whose top-plane centre is nearest in 3D (tile partition); null expectations are scaled by the
share of the unit's pairs that fall in its tile.

Each flagged change (a pair present at the top of a segment and absent at its bottom) is sorted by rules fixed before the run's
changes were looked at, then checked by eye on the overlay crops (INSPECTION_JSON, keyed "patch:segment_top:i-j", may override):
  artefact   a cell of the pair is detected in under 80% of the planes, or the pair is still a Delaunay edge among the tracked
             columns at the bottom (opposite-angle sum < 180 deg: it was lost only because an untracked detection came between),
             or the pair has no opposite cells (hull);
  near-tie   the four columns form a near-square rhombus at the top (opposite-angle sum > 160 deg) and stay near the tie at the
             bottom (<= 200 deg): a diagonal that flickers, not a clear exchange;
  true       otherwise: the rhombus passes clearly from one diagonal to the other.
Then: observed changes against the image null (straight columns + calibrated jitter through the same pipeline) and the bootstrap
null, by layer and depth; per patch, the excess and the true changes against cornea unevenness U and convergence anisotropy A
(Spearman, permutation p); change rates by the local anisotropy of the pair. Writes derived counts only.
Usage: eyesum16.py SUMMARY.json OUT.json [INSPECTION_JSON]"""
import sys, json, numpy as np

S = json.load(open(sys.argv[1])); OUT = sys.argv[2]
INS = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
P = [p for p in S['patches'] if 'skip' not in p and p.get('segments')]
rng = np.random.default_rng(11)
A_BINS = [1.0, 1.2, 1.4, 1.6, 3 ** 0.5, 2.0, 2.5, 3.0, 1e9]


def nvar(share, sd, top, seeds):
    """Variance of the null count of one unit: at least Poisson (few seeds can understate it) + uncertainty of the seed mean."""
    m, v = max(share, 0.5 / (seeds * max(top, 1))) * top, (sd * top) ** 2
    return max(v, m) + v / seeds


def spearman(x, y, nperm=20000):
    x, y = np.asarray(x, float), np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y); x, y = x[m], y[m]
    if len(x) < 5 or np.ptp(x) == 0 or np.ptp(y) == 0: return None          # a constant series has no rank order
    from scipy.stats import rankdata
    rx, ry = rankdata(x), rankdata(y); r = np.corrcoef(rx, ry)[0, 1]          # average ranks for ties
    perm = np.array([np.corrcoef(rx, rng.permutation(ry))[0, 1] for _ in range(nperm)])
    return dict(rho=float(r), p_two_sided=float((np.abs(perm) >= abs(r) - 1e-12).mean()), n=int(len(x)))


def rule(li):
    if min(li['support']) < 0.8 or li['top_sum'] is None: return 'artefact'
    if li['bottom_sum'] < 180: return 'artefact'
    if li['top_sum'] > 160 and li['bottom_sum'] <= 200: return 'near-tie'
    return 'true'


C = np.array([p['top_centre3'] for p in P]).reshape(-1, 3)
def owner(x): return int(np.argmin(np.linalg.norm(C - np.asarray(x), axis=1)))


units, calls = [], {}
for i, p in enumerate(P):
    for g in p['segments']:
        if 'skip' in g: continue
        seeds = len(g.get('img_null_sm_lost', [])) or 8
        f = float(np.mean([owner(e) == i for e in g['edges3']])) if g['edges3'] else 0.0
        info = {tuple(li['pair']): li for li in g.get('lost_info', [])}
        c = {'true': 0, 'near-tie': 0, 'artefact': 0}
        for s in g['swap3']:
            if owner(s[0]) != i: continue
            key = f"{p['patch']}:{g['depth_um'][0]}:{s[2][0]}-{s[2][1]}"; li = info.get(tuple(s[2]))
            call = INS.get(key, {}).get('call') or (rule(li) if li else 'artefact'); c[call] += 1
            calls[key] = dict(rule=rule(li) if li else 'artefact', call=call, top_sum=li and li['top_sum'], bottom_sum=li and li['bottom_sum'],
                              support=li and li['support'], A=None)
        top = g['sm_top'] * f
        units.append(dict(patch=p['patch'], layer=g['layer'], depth_um=g['depth_um'], cells=sum(owner(x) == i for x in g['cells3']), pairs=top,
                          lost=sum(c.values()), true=c['true'], near_tie=c['near-tie'], artefact=c['artefact'],
                          null=g['img_null_sm'] * top, null_var=nvar(g['img_null_sm'], g['img_null_sm_sd'], top, seeds),
                          boot=g['boot_null_sm'] * f, boot_var=g['boot_null_sm_sd'] ** 2 * f, model=g['model_expected_lost'] * f,
                          tracked=g['tracked_share_zone'], trusted_share=g['trusted_share_zone'], A_median=g['A_median'], A_global=g['A_global'],
                          noise_px=g['noise_px'], A_of_lost=g['A_of_lost'], A_of_pairs=g['A_of_pairs']))


def pool(U_):
    o = sum(u['lost'] for u in U_); t = sum(u['pairs'] for u in U_); e = sum(u['null'] for u in U_); sd = float(np.sqrt(sum(u['null_var'] for u in U_)))
    tr = sum(u['true'] for u in U_)
    return dict(units=len(U_), cells=sum(u['cells'] for u in U_), pairs=t, lost=o, share=o / max(t, 1), image_null=e, image_null_sd=sd,
                z=(o - e) / max(sd, 1e-9), true=tr, near_tie=sum(u['near_tie'] for u in U_), artefact=sum(u['artefact'] for u in U_),
                true_share=tr / max(t, 1), null_share=e / max(t, 1), bootstrap=sum(u['boot'] for u in U_), bootstrap_sd=float(np.sqrt(sum(u['boot_var'] for u in U_))),
                model=sum(u['model'] for u in U_), tracked_median=float(np.median([u['tracked'] for u in U_])) if U_ else None,
                tracked_range=[float(min(u['tracked'] for u in U_)), float(max(u['tracked'] for u in U_))] if U_ else None,
                trusted_median=float(np.median([u['trusted_share'] for u in U_])) if U_ else None,
                A_median=float(np.median([u['A_median'] for u in U_])) if U_ else None)


out = {'by_layer': {L: pool([u for u in units if u['layer'] == L]) for L in ('cone', 'tips', 'retina')}}
out['by_segment'] = {f'{a}-{b}': pool([u for u in units if u['depth_um'] == [a, b]]) for a, b, _ in S['segments']}
out['all'] = pool(units)
fr = [p['full_range'] for p in P if p.get('full_range')]
out['full_range'] = dict(depth_um=S.get('full_range'), patches=len(fr), tracked_median=float(np.median([f['tracked_share_zone'] for f in fr])) if fr else None,
                         trusted_median=float(np.median([f['trusted_share_zone'] for f in fr])) if fr else None,
                         trusted_columns=sum(f['trusted'] for f in fr), lost=sum(f['lost'] for f in fr), pairs=sum(f['top'] for f in fr))
# change rate by local anisotropy of the pair (untiled; rates only)
for L in ('cone', 'retina'):
    al = np.concatenate([u['A_of_lost'] for u in units if u['layer'] == L] or [[]]); ap = np.concatenate([u['A_of_pairs'] for u in units if u['layer'] == L] or [[]])
    out[f'by_pair_A_{L}'] = [dict(A=[a, b if b < 1e8 else None], pairs=int(((ap >= a) & (ap < b)).sum()), lost=int(((al >= a) & (al < b)).sum()))
                             for a, b in zip(A_BINS[:-1], A_BINS[1:]) if ((ap >= a) & (ap < b)).sum()]
# per patch (retina segments, and cone window), against U and A
rows = []
for p in P:
    cor = p.get('cornea') or {}
    for L in ('retina', 'cone'):
        G = [u for u in units if u['patch'] == p['patch'] and u['layer'] == L]
        if not G or cor.get('U') is None: continue
        t = sum(u['pairs'] for u in G)
        rows.append(dict(patch=p['patch'], layer=L, pairs=t, lost=sum(u['lost'] for u in G), true=sum(u['true'] for u in G), null=sum(u['null'] for u in G),
                         excess_share=(sum(u['lost'] for u in G) - sum(u['null'] for u in G)) / max(t, 1), true_share=sum(u['true'] for u in G) / max(t, 1),
                         U=cor['U'], U_min=cor['U_min'], U_max=cor['U_max'], U_sd=cor['U_sd'], radius1_um=cor['radius1_um'], radius2_um=cor['radius2_um'],
                         A_global=float(np.median([u['A_global'] for u in G])), A_median=float(np.median([u['A_median'] for u in G])),
                         tracked=float(np.median([u['tracked'] for u in G]))))
out['patch_rows'] = rows
for L in ('retina', 'cone'):
    R = [r for r in rows if r['layer'] == L]
    if len(R) < 5: continue
    out[f'spearman_{L}'] = {f'{y}_vs_{x}': spearman([r[x] for r in R], [r[y] for r in R]) for x in ('U', 'A_global') for y in ('excess_share', 'true_share')}
    out[f'spearman_{L}']['U_vs_A_global'] = spearman([r['U'] for r in R], [r['A_global'] for r in R])
    med = float(np.median([r['U'] for r in R])); hi = [r for r in R if r['U'] > med]; lo = [r for r in R if r['U'] <= med]
    f_ = lambda G: dict(patches=len(G), pairs=sum(r['pairs'] for r in G), lost=sum(r['lost'] for r in G), true=sum(r['true'] for r in G),
                        null=sum(r['null'] for r in G), U_range=[min(r['U'] for r in G), max(r['U'] for r in G)] if G else None)
    out[f'by_U_half_{L}'] = dict(median_U=med, uneven=f_(hi), even=f_(lo))
Ru = [r for r in rows if r['layer'] == 'retina'] or rows
out['U'] = dict(patches=len(Ru), median=float(np.median([r['U'] for r in Ru])), iqr=[float(np.percentile([r['U'] for r in Ru], q)) for q in (25, 75)],
                range=[float(min(r['U'] for r in Ru)), float(max(r['U'] for r in Ru))],
                variant_spread_median=float(np.median([r['U_max'] - r['U_min'] for r in Ru])), variant_sd_median=float(np.median([r['U_sd'] for r in Ru])),
                radius1_median_um=float(np.median([r['radius1_um'] for r in Ru])), radius2_median_um=float(np.median([r['radius2_um'] for r in Ru])))
out['units'] = [{k: v for k, v in u.items() if k not in ('A_of_lost', 'A_of_pairs')} for u in units]
out['calls'] = calls
out['synthetic'] = S['synthetic']; out['patches_total'] = len(S['patches']); out['skips'] = [(p['patch'], p.get('skip')) for p in S['patches'] if 'skip' in p]
json.dump(out, open(OUT, 'w'), indent=1, default=float)
for k in ('cone', 'tips', 'retina'):
    b = out['by_layer'][k]
    if b['units']: print(k, {x: (round(v, 3) if isinstance(v, float) else v) for x, v in b.items()})
for k, b in out['by_segment'].items():
    if b['units']: print(' seg', k, 'lost', b['lost'], 'pairs', round(b['pairs']), 'null', round(b['image_null'], 1), '+-', round(b['image_null_sd'], 1), 'true', b['true'], 'near-tie', b['near_tie'], 'artefact', b['artefact'], 'tracked', round(b['tracked_median'], 2))
print('full range', out['full_range'])
for k in ('spearman_retina', 'spearman_cone', 'by_U_half_retina', 'U', 'by_pair_A_retina', 'by_pair_A_cone'): print(k, out.get(k))
print('synthetic', {k: (v.get('raw_lost'), v.get('raw_top')) if isinstance(v, dict) and 'raw_lost' in v else v for k, v in out['synthetic'].items()})
