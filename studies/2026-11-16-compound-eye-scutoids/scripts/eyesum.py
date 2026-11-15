#!/usr/bin/env python3
"""Pool the per-patch results of eyerun.py (summary.json) into the study's numbers: observed lost neighbour edges against the
image null (straight columns + calibrated jitter through the same segmentation) and the bootstrap null, per layer, per depth,
and against cornea curvature unevenness U and convergence anisotropy A (Spearman rank correlation, permutation p-value).
Writes data/eyetrace-summary.json (derived counts only). Usage: eyesum.py SUMMARY.json OUT.json"""
import sys, json, numpy as np

import os
S = json.load(open(sys.argv[1])); out = {}; RUN = os.path.dirname(os.path.abspath(sys.argv[1]))
P = [p for p in S['patches'] if 'skip' not in p]
rng = np.random.default_rng(11)
SEEDS = 10
HALF = 0.1      # tile half-width (rad): the patch grid is 0.2 rad apart, the patches themselves are wider and overlap

# ---- tile partition: every cell and every neighbour change is counted by one patch only, the one whose tile (|A-A0|, |B-B0| <= HALF
# in angles about the eye centre) contains it. Lost edges are counted exactly (their top midpoint); counted edges and null
# expectations are scaled by the share of the unit's cells that lie in the tile.
E_ = os.environ.get('EYE_DATA', os.path.expanduser('~/eye-data')) + '/'; fr = np.load(E_ + 'frame_iso.npy'); U0, G1, G2 = fr[:3], fr[3:6], fr[6:]
sph = np.load(E_ + 'sphere_iso.npy'); CEN = sph[:3] * 4 + 1.5


def gang(v):
    v = np.asarray(v, float); v = v / np.linalg.norm(v, axis=-1, keepdims=True)
    t = np.arccos(np.clip(v @ U0, -1, 1)); x, y = v @ G1, v @ G2; r = np.hypot(x, y) + 1e-15
    return np.stack([t * x / r, t * y / r], -1)


def tile(unit, A0, B0, lost_key='sm_lost', top_key='sm_top'):
    cells = np.asarray(unit.get('cells_A', []), float).reshape(-1, 2)
    inside = lambda a: (np.abs(a[:, 0] - A0) <= HALF) & (np.abs(a[:, 1] - B0) <= HALF)
    f = float(inside(cells).mean()) if len(cells) else 0.0
    sw = np.array([t for t, _ in unit.get('swap_xyz', [])], float).reshape(-1, 3)
    lost_in = int(inside(gang(sw - CEN)).sum()) if len(sw) else 0
    unit['untiled'] = {k: unit.get(k) for k in (lost_key, top_key)}
    unit['tile_cell_share'] = f; unit[lost_key] = lost_in; unit[top_key] = unit[top_key] * f
    for k in ('region_lost', 'region_top', 'model_expected_lost', 'boot_null_sm', 'null_smoothed_mean'):
        if k in unit and unit[k] is not None: unit[k] = unit[k] * f
    for k in ('boot_null_sm_sd', 'null_smoothed_sd'):
        if k in unit and unit[k] is not None: unit[k] = unit[k] * np.sqrt(f)
    unit['interior'] = unit.get('interior', unit.get('trusted', 0)) * f
    if 'trusted' in unit: unit['trusted'] = unit['trusted'] * f
    unit['swap_tile'] = [s for s, a in zip(unit.get('swap_xyz', []), gang(sw - CEN) if len(sw) else []) if inside(a[None])[0]]
    unit['cells_tile'] = cells[inside(cells)].tolist() if len(cells) else []


for p in P:
    if p.get('cone') and 'sm_lost' in p['cone']:
        cj = json.load(open(f'{RUN}/p{p["patch"]}_cone.json'))
        p['cone']['cells_A'] = cj.get('cells_A', []); p['cone']['swap_xyz'] = cj.get('swap_xyz', [])
        tile(p['cone'], p['A'], p['B'])
    for g in p.get('retina_segments', []):
        if 'skip' not in g: tile(g, p['A'], p['B'])
json.dump(dict(synthetic=S['synthetic'], patches=S['patches']), open(sys.argv[2].replace('.json', '_tiled_units.json'), 'w'), default=float)


def nvar(share, sd, top):
    """Variance of the null count of one unit: at least Poisson (few seeds can understate it) + uncertainty of the seed mean."""
    m, v = max(share, 0.5 / (SEEDS * max(top, 1))) * top, (sd * top) ** 2   # half-count floor when no seed showed a change
    return max(v, m) + v / SEEDS


def spearman(x, y, nperm=20000):
    x, y = np.asarray(x, float), np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y); x, y = x[m], y[m]
    if len(x) < 5: return None
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y)); r = np.corrcoef(rx, ry)[0, 1]
    perm = np.array([np.corrcoef(rx, rng.permutation(ry))[0, 1] for _ in range(nperm)])
    return dict(rho=float(r), p_two_sided=float((np.abs(perm) >= abs(r) - 1e-12).mean()), n=int(len(x)))


# --- cone layer (one window per patch)
C = [p for p in P if p.get('cone') and 'sm_lost' in p['cone']]
O = sum(p['cone']['sm_lost'] for p in C); T = sum(p['cone']['sm_top'] for p in C)
E = sum(p['cone']['img_null_sm'] * p['cone']['sm_top'] for p in C); sd = np.sqrt(sum(nvar(p['cone']['img_null_sm'], p['cone']['img_null_sm_sd'], p['cone']['sm_top']) for p in C))
Eb = sum(p['cone']['null_smoothed_mean'] for p in C); sdb = np.sqrt(sum(p['cone']['null_smoothed_sd'] ** 2 for p in C))
out['cone'] = dict(patches=len(C), trusted_cells=sum(p['cone']['interior'] for p in C), edges=T, lost=O, share=O / max(1, T),
                   image_null=E, image_null_sd=float(sd), z_image=(O - E) / max(sd, 1e-9), bootstrap_null=Eb, bootstrap_null_sd=float(sdb),
                   region_lost=sum(p['cone']['region_lost'] for p in C), region_edges=sum(p['cone']['region_top'] for p in C),
                   depth_windows=[p['cone']['depth_um'] for p in C], model_expected=sum(p['cone']['model_expected_lost'] for p in C),
                   A_median=float(np.median([p['cone']['A_median'] for p in C])))
# --- retina (20 um segments)
segs = [(p, g) for p in P for g in p.get('retina_segments', []) if 'skip' not in g]
O = sum(g['sm_lost'] for _, g in segs); T = sum(g['sm_top'] for _, g in segs)
E = sum(g['img_null_sm'] * g['sm_top'] for _, g in segs); sd = float(np.sqrt(sum(nvar(g['img_null_sm'], g['img_null_sm_sd'], g['sm_top']) for _, g in segs)))
Eb = sum(g['boot_null_sm'] for _, g in segs); sdb = float(np.sqrt(sum(g['boot_null_sm_sd'] ** 2 for _, g in segs)))
Or = sum(g['region_lost'] for _, g in segs); Tr = sum(g['region_top'] for _, g in segs)
out['retina'] = dict(patches=len({p['patch'] for p, _ in segs}), segments=len(segs), edges=T, lost=O, share=O / max(1, T),
                     image_null=E, image_null_sd=sd, z_image=(O - E) / max(sd, 1e-9), excess=O - E, excess_share=(O - E) / max(1, T),
                     bootstrap_null=Eb, bootstrap_null_sd=sdb, region_lost=Or, region_edges=Tr,
                     model_expected=sum(g['model_expected_lost'] for _, g in segs),
                     trusted_cells_per_segment=float(np.mean([g['trusted'] for _, g in segs])) if segs else 0,
                     tracked_share=float(np.mean([g['tracked_share'] for _, g in segs])) if segs else 0,
                     segments_skipped=sum(1 for p in P for g in p.get('retina_segments', []) if 'skip' in g))
# by depth (segment start below the cornea)
bins = [300, 340, 380, 420, 460, 520]; byd = []
for a, b in zip(bins[:-1], bins[1:]):
    G = [g for _, g in segs if a <= g['depth_below_cornea_um'][0] < b]
    if not G: continue
    o = sum(g['sm_lost'] for g in G); t = sum(g['sm_top'] for g in G); e = sum(g['img_null_sm'] * g['sm_top'] for g in G)
    s = float(np.sqrt(sum(nvar(g['img_null_sm'], g['img_null_sm_sd'], g['sm_top']) for g in G)))
    byd.append(dict(depth_um=[a, b], segments=len(G), edges=t, lost=o, null=e, null_sd=s, z=(o - e) / max(s, 1e-9)))
out['retina_by_depth'] = byd
# per patch: excess share vs cornea unevenness, convergence anisotropy, bend
rows = []
for p in P:
    G = [g for g in p.get('retina_segments', []) if 'skip' not in g]
    if not G or not p.get('cornea'): continue
    t = sum(g['sm_top'] for g in G); o = sum(g['sm_lost'] for g in G); e = sum(g['img_null_sm'] * g['sm_top'] for g in G)
    rows.append(dict(patch=p['patch'], A=p['A'], B=p['B'], edges=t, lost=o, null=e, excess_share=(o - e) / max(1, t),
                     U=p['cornea']['unevenness'], k1=p['cornea']['k1_per_mm'], k2=p['cornea']['k2_per_mm'],
                     A_conv=float(np.median([g['A_median'] for g in G])), bend_deg=p.get('retina_bend_deg'),
                     angle_to_radial_deg=p.get('retina_angle_to_radial_deg')))
out['retina_patches'] = rows
if rows:
    out['spearman_excess_vs_U'] = spearman([r['U'] for r in rows], [r['excess_share'] for r in rows])
    out['spearman_excess_vs_Aconv'] = spearman([r['A_conv'] for r in rows], [r['excess_share'] for r in rows])
    out['spearman_excess_vs_bend'] = spearman([r['bend_deg'] for r in rows], [r['excess_share'] for r in rows])
    # swaps in the more vs less uneven half of the patches
    med = np.median([r['U'] for r in rows]); hi = [r for r in rows if r['U'] > med]; lo = [r for r in rows if r['U'] <= med]
    f = lambda R: dict(patches=len(R), edges=sum(r['edges'] for r in R), lost=sum(r['lost'] for r in R), null=sum(r['null'] for r in R),
                       U_range=[min(r['U'] for r in R), max(r['U'] for r in R)] if R else None)
    out['retina_by_U_half'] = dict(median_U=float(med), uneven=f(hi), even=f(lo))
out['cornea'] = dict(U=[p['cornea']['unevenness'] for p in P if p.get('cornea')], radius1_um=[p['cornea']['radius1_um'] for p in P if p.get('cornea')],
                     radius2_um=[p['cornea']['radius2_um'] for p in P if p.get('cornea')])
out['synthetic'] = {k: v for k, v in S['synthetic'].items()}
out['patches_total'] = len(S['patches']); out['patches_used'] = len(P); out['skips'] = [(p['patch'], p.get('skip')) for p in S['patches'] if 'skip' in p]
json.dump(out, open(sys.argv[2], 'w'), indent=1, default=float)
c, r = out['cone'], out['retina']
print(f"cone: {c['patches']} patches, {c['trusted_cells']} trusted cells, lost {c['lost']}/{c['edges']} ({100 * c['share']:.2f}%), image null {c['image_null']:.1f} +- {c['image_null_sd']:.1f} (z {c['z_image']:.1f}), bootstrap {c['bootstrap_null']:.1f}")
print(f"retina: {r['patches']} patches, {r['segments']} segments, lost {r['lost']}/{r['edges']} ({100 * r['share']:.2f}%), image null {r['image_null']:.1f} +- {r['image_null_sd']:.1f} (z {r['z_image']:.1f}), excess {r['excess']:.1f}, bootstrap {r['bootstrap_null']:.1f}, model {r['model_expected']:.1f}, region {r['region_lost']}/{r['region_edges']}")
for d in byd: print('  depth', d)
for k in ['spearman_excess_vs_U', 'spearman_excess_vs_Aconv', 'spearman_excess_vs_bend', 'retina_by_U_half']: print(k, out.get(k))
print('synthetic', {k: (v.get('raw_lost'), v.get('raw_top')) if isinstance(v, dict) and 'raw_lost' in v else v for k, v in out['synthetic'].items()})
