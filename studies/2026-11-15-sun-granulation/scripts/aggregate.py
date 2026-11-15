"""Tables for the README from results/census/*.json and results/control/*.json (+ the exact control counts in data/control).
Usage: aggregate.py STUDYDIR  -> STUDYDIR/results/summary.md, summary.json"""
import sys, os, json, glob
import numpy as np
S = sys.argv[1]
out, md = {}, []


def exact_steps(ex, steps=(1, 2, 4, 8), W=60, dt=10.0):
    """Exact swaps at each step: Delaunay pairs lost between sampled frames; persistent = lost - 2 x (lost pairs regained within W)."""
    P = [set(map(tuple, f)) for f in ex['frame_pairs']]
    r = {}
    for s in steps:
        idx = list(range(0, len(P), s))
        lost_ev = []
        for a, b in zip(idx, idx[1:]):
            for p in P[a] - P[b]: lost_ev.append((b * dt, p))
        regained = 0
        for t, p in lost_ev:
            # regained at a later sampled frame within W
            for c in idx:
                if t < c * dt <= t + W and p in P[c]: regained += 1; break
        r[str(s)] = dict(lost=len(lost_ev), regained_within_W=regained, persistent=len(lost_ev) - 2 * regained)
    return r


md.append('## Positive control: moving periodic Voronoi tilings drawn as images (500 cells, 120 frames)\n')
md.append('| speed | noise | step | exact swaps (frame to frame) | exact persistent | pipeline elementary | pipeline persistent | persistent ratio | clumps | splits+merges (should be 0) |')
md.append('|---|---|---|---|---|---|---|---|---|---|')
for f in sorted(glob.glob(f'{S}/results/control/voronoi_*.json')):
    R = json.load(open(f)); name = R['run']
    exf = f'{S}/data/control/{name}_exact.json'
    if not os.path.exists(exf): continue
    ex = json.load(open(exf)); E = exact_steps(ex)
    v, z = name.split('_v')[1].split('_z')[0], name.split('_z')[1].split('_s')[0]
    out[name] = dict(exact=E, exact_substep_total=ex['exact_swaps_total'], pipeline={})
    for s, r in R['steps'].items():
        e = E[s]; ratio = r['swaps_persistent'] / e['persistent'] if e['persistent'] else None
        out[name]['pipeline'][s] = dict(elementary=r['swaps_elementary'], persistent=r['swaps_persistent'], ratio=ratio,
                                        clumps=r['n_clumps'], splits=r['counts'].get('split', 0), merges=r['counts'].get('merge', 0))
        md.append(f"| {v} | {z} | {s} | {e['lost']} | {e['persistent']} | {r['swaps_elementary']} | {r['swaps_persistent']} | "
                  f"{ratio:.2f} | {r['n_clumps']} | {r['counts'].get('split', 0) + r['counts'].get('merge', 0)} |")
md.append('')

md.append('## Sun: Bifrost granulation, every setting and time step\n')
md.append('| setting | step (s) | cells | swaps: elementary / persistent (W 60 s; 120 s) | splits: all / persistent | merges: all / persistent | births / deaths | lifetime s (Little, persistent cells) | swaps per persistent split | swaps per cell lifetime | clumps | Euler bad frames |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|')
cellrows = []
for f in sorted(glob.glob(f'{S}/results/census/*.json')):
    R = json.load(open(f)); tag = os.path.basename(f)[:-5]; out[tag] = R
    for s, r in R['steps'].items():
        f2 = lambda x: 'n/a' if x is None else f'{x:.2f}'
        cn = r['counts']
        md.append(f"| {tag} | {r['dt_s']:.0f} | {r['mean_cells']:.0f} | {r['swaps_elementary']} / {r['swaps_persistent']}; {r['swaps_persistent_by_W']['120']} | "
                  f"{cn.get('split', 0)} / {r.get('splits_persistent', 'n/a')} | {cn.get('merge', 0)} / {r.get('merges_persistent', 'n/a')} | "
                  f"{cn.get('birth', 0)} / {cn.get('death', 0)} | {f2(r.get('lifetime_little_persistent_s'))} | {f2(r['swaps_per_split'])} | "
                  f"{f2(r['swaps_per_cell_lifetime'])} | {r['n_clumps']} | {r['frames_torus_euler_bad']} |")
    c, vv = R['cells'], R['centroid_voronoi']
    cellrows.append(f"| {tag} | {c['mean_cells']:.0f} | {c['mean_n']:.3f} | {c['mu2']:.2f} | {c['p_n'].get('6', 0):.3f} | {c['aboav_a']:.2f} | "
                    f"{c['aboav_intercept']:.2f} vs {c['aboav_pred_intercept']:.2f} | {c['lewis_slope'] if c['lewis_slope'] is None else round(c['lewis_slope'], 3)} "
                    f"(R2 {c['lewis_r2'] if c['lewis_r2'] is None else round(c['lewis_r2'], 3)}) | {vv['mu2']:.2f} | {vv['p_n'].get('6', 0):.3f} | {vv['aboav_a']:.2f} |")
md.append('')
md.append('## Sun: side numbers, Aboav-Weaire and Lewis, against the Voronoi tiling of the cell centroids\n')
md.append('| setting | cells | mean n | mu2 | p6 | Aboav a | n m(n) intercept: fit vs 6a + mu2 | Lewis slope of A(n)/mean A | Voronoi mu2 | Voronoi p6 | Voronoi a |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|')
md += cellrows
open(f'{S}/results/summary.md', 'w').write('\n'.join(md) + '\n')
json.dump(out, open(f'{S}/results/summary.json', 'w'), indent=1, default=float)
print('\n'.join(md))
