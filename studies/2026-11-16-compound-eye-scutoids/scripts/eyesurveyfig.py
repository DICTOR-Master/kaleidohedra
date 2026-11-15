#!/usr/bin/env python3
"""Survey figure and summary for the seven Paukner 2024 butterfly eyes (study 2026-11-16-compound-eye-scutoids).
Per eye: a radial cross-section through the cap axis (2.4 um grid, derived and low resolution; the volumes stay off git) and the
depth profiles of texture, column alignment and tissue from eyesurvey.py. Writes FIG/eye-survey.png and SUMMARY.json.
Usage: eyesurveyfig.py SURVEYDIR FIGDIR SUMMARY.json NAME..."""
import sys, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import os
SD, FIG, SUM, names = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
summ = {}
ok_names = []
for n in names:                                    # an eye counts only if its cornea sheet was found (1000 points or more, 5 discs)
    f = f'{SD}/{n}-survey.json'
    d = json.load(open(f)) if os.path.exists(f) else None
    if d is None or d['sheet']['points'] < 1000 or d['local']['tiles'] < 5:
        summ[n] = dict(measured=False, reason='cornea sheet not found at 2.4 um' if d is None or d['sheet']['points'] < 1000 else 'fewer than 5 counted discs',
                       sheet_points=None if d is None else d['sheet']['points']); print('NOT MEASURED', n)
    else: ok_names.append(n)
names = ok_names
MARK = 'DICTO · dictospheres.com'
fig, axs = plt.subplots(len(names), 2, figsize=(9, 2.6 * len(names)), gridspec_kw=dict(width_ratios=[1, 1.4]))
for r, n in enumerate(names):
    d = json.load(open(f'{SD}/{n}-survey.json')); sl = np.load(f'{SD}/{n}-xsec.npy')
    lo, hi = np.percentile(sl[sl > 0], [1, 99.5]) if (sl > 0).any() else (0, 1)
    e = d['xsec']['ext_um']; R = d['sphere']['radius_um']
    ax = axs[r, 0]; ax.imshow(np.clip((sl - lo) / (hi - lo), 0, 1), cmap='gray', extent=(-e, e, -650, 48), aspect='equal')
    ax.set_title(f'{n}: section along the mean surface normal', fontsize=8); ax.set_xlabel('um along the surface', fontsize=7)
    ax.set_ylabel('um above the cornea centre', fontsize=7); ax.tick_params(labelsize=6)
    for b in d['clear_zone_bands_um']: ax.axhspan(-b[1], -b[0], color='orange', alpha=0.15)
    P = d['profile']; dd = np.array([p['depth_um'] for p in P])
    g = lambda k: np.array([np.nan if p.get(k) is None else p[k] for p in P])
    tx = g('texture'); ax2 = axs[r, 1]
    ax2.plot(dd, tx / np.nanmax(tx), label='texture (band-pass rms, scaled)', lw=1)
    ax2.plot(dd, g('aligned30'), label='share of column axes within 30 deg of the normal', lw=1)
    ax2.plot(dd, g('tissue'), label='tissue share', lw=0.8, color='0.5', ls=':')
    for b in d['clear_zone_bands_um']: ax2.axvspan(*b, color='orange', alpha=0.15)
    ax2.set_xlim(0, 600); ax2.set_ylim(0, 1.05); ax2.tick_params(labelsize=6); ax2.set_xlabel('depth below the cornea (um)', fontsize=7)
    loc = d['local']; q = d['quadric']
    ax2.set_title(f"U median {loc['U_median']:.2f} ({loc['tiles']} tiles); quadric max/min {q.get('ratio_max_min', float('nan')):.2f}", fontsize=8)
    if r == 0: ax2.legend(fontsize=6, loc='upper right')
    summ[n] = dict(measured=True, seed_iso=d['seed_iso'], sheet_points=d['sheet']['points'], sheet_extent_um=[round(v) for v in d['sheet']['extent_um']],
                   sphere_radius_um=round(R), sphere_rms_um=round(d['sphere']['rms_um'], 1),
                   quadric=q.get('kind'), semi_axes_um=[round(a) for a in q.get('semi_axes_um', [])], ratio_max_min=q.get('ratio_max_min'),
                   ratio_mid_min=q.get('ratio_mid_min'), ratio_bootstrap=q.get('bootstrap_ratio_max_min'),
                   U_tiles=loc['tiles'], U_median=loc['U_median'], U_iqr=[loc['U_q25'], loc['U_q75']], U_max=loc['U_max'], discs_placed=loc['discs_placed'], r1_median_um=loc['r1_median_um'], r2_median_um=loc['r2_median_um'],
                   clear_zone_bands_um=d['clear_zone_bands_um'], texture_dip=d['texture_dip'], column_runs_um=d['column_runs_um'],
                   aligned_depth_um=d['aligned_depth_um'], tissue_end_um=d['tissue_end_um'], shape_zyx=d['shape_zyx'])
plt.tight_layout(rect=(0, 0.015, 1, 1)); fig.text(0.995, 0.003, MARK, ha='right', va='bottom', fontsize=8, color='0.35')
fig.savefig(f'{FIG}/eye-survey.png', dpi=60); json.dump(summ, open(SUM, 'w'), indent=1); print('FIG ok')
