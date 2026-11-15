"""Tables for the grid-or-physics follow-up, from results/grid-*.json, results/zones-*.json, results/pv-walls.json and the toy's fixed-step
curve (results/toy-coarse-voronoi.json). No hand-copied numbers. Usage: summarise_followup.py RESULTS_DIR
Yardstick: among contact changes NOT tied to a merge or split, the share clumped with other contact changes, against the exact Voronoi foam
sampled at the same number of such changes per cell per step (log-linear interpolation of the toy curve; the foam has no merges)."""
import sys, json, glob, os
import numpy as np
R = sys.argv[1]
toy = sorted(sum((json.load(open(f))['rows'] for f in glob.glob(f'{R}/toy-coarse-voronoi*.json')), []), key=lambda r: r['seen_per_cell_per_step'])
tx = np.log([r['seen_per_cell_per_step'] for r in toy]); ty = np.array([1 - r['alone_share'] for r in toy])


def yard(rate):
    return float(np.interp(np.log(rate), tx, ty)) if tx.min() <= np.log(rate) <= tx.max() else float('nan')


def rows(files, label):
    out = []
    for f in files:
        d = json.load(open(f)); da = d['nbody']['da']
        name = os.path.basename(f)[:-5]
        for v in d['variants']:
            D = v['derived']; al = D.get('contact changes, alone', 0); cl = D.get('contact changes, clumped with other contact changes', 0)
            cc = v['contact_changes_total']; st = v['snapshots_used'] - 1; nb = np.mean(v['basins_first_last'])
            rate = (al + cl) / st / nb; ex = cl / (al + cl) if al + cl else float('nan')
            out.append((name, label(d), v['k'] * da, f"{v['rule'][0]} {v['rule'][1]:g}", f"{v['basins_first_last'][0]} / {v['basins_first_last'][1]}",
                        f"{v['mean_contacts_mean']:.2f}", cc, f"{v['per_basin_per_step']:.3f}", f"{v['fraction_alone']:.3f}", f"{v['fraction_clumped']:.3f}",
                        f"{1 - v['fraction_alone'] - v['fraction_clumped']:.3f}", f"{rate:.3f}", f"{ex:.3f}", f"{yard(rate):.3f}",
                        f"{v['contact_changes_per_merge']:.1f}" if v['contact_changes_per_merge'] else '-', v['balance_failures']))
    return out


print('### Grid refinement and grid-free zones: share of contact changes alone and clumped\n')
print('| run | tiling | spacing Delta a | wall rule | basins first / last | mean contacts | contact changes | per basin per step | share alone | '
      'clumped with contact changes | with a merge or split | non-merge changes per basin per step | clumped share of non-merge changes | '
      'exact foam at the same rate | contact changes per merged basin | balance failures |')
print('|' + '---|' * 16)
G = sorted(glob.glob(f'{R}/grid-*.json'), key=lambda f: json.load(open(f))['grid'])
Z = sorted(glob.glob(f'{R}/zones-*.json'))
for r in rows(G, lambda d: f"voxels {d['grid']}^3 ({d['L_Mpc_h'] / d['grid']:g} Mpc/h)") + \
        rows(Z, lambda d: f"Voronoi tracers, {d['mode']}, {d['n_tracers']} tracers"):
    print('| ' + ' | '.join(map(str, r)) + ' |')
print('\n### Where the contact changes happen (finest spacing; wall area in units of Vbar^(2/3))\n')
print('| run | wall rule | group | contact changes | median wall area | share with wall area < 0.01 | share < 0.03 | mean smoothed field on the wall | '
      'share near a merge or split (same or adjacent step) | share that change again in an adjacent step | share lost (rest gained) |')
print('|' + '---|' * 11)
for f in G + Z:
    d = json.load(open(f)); name = os.path.basename(f)[:-5]
    for v in d['variants']:
        if v['k'] != 1 or v['rule'][0] not in ('faces', 'eps') or (v['rule'][0] == 'eps' and v['rule'][1] != 0.01): continue
        for g in ('alone', 'clumped', 'merge'):
            c = v['characterisation'].get(g)
            if not c: continue
            mf = f"{c['mean_wall_field']:.3f}" if c['mean_wall_field'] is not None else '-'
            print(f"| {name} | {v['rule'][0]} {v['rule'][1]:g} | {g} | {c['n']} | {c['median_area_eps']:.4f} | {c['frac_area_below_0p01']:.3f} | "
                  f"{c['frac_area_below_0p03']:.3f} | {mf} | {c['frac_near_merge']:.3f} | {c['frac_flicker']:.3f} | {c['frac_lost']:.3f} |")
print('\n### Top clump patterns (finest spacing, native wall rule)\n')
for f in G + Z:
    d = json.load(open(f)); v = d['variants'][0]
    print(f"- {os.path.basename(f)[:-5]} ({v['rule'][0]} {v['rule'][1]:g}): " + '; '.join(f'{k} x{n}' for k, n in list(v['top_clump_patterns'].items())[:5]))
print('\n### Neighbours per basin against the wall rule: a wall counts if its area >= eps * Vbar^(2/3) (mean over snapshots)\n')
pv = json.load(open(f'{R}/pv-walls.json')) if os.path.exists(f'{R}/pv-walls.json') else None
eps = json.load(open(G[0]))['eps_list'] if G else []
print('| tiling | ' + ' | '.join(f'eps {e:g}' for e in eps) + ' |')
print('|---|' + '---|' * len(eps))
if pv: print(f"| Poisson-Voronoi (N = {pv['N']}, {pv['seeds']} seeds) | " + ' | '.join(f'{m:.3f} +- {s:.3f}' for m, s in zip(pv['mean'], pv['sem'])) + ' |')
for f in G + Z:
    d = json.load(open(f)); print(f"| {os.path.basename(f)[:-5]} | " + ' | '.join(f'{x:.2f}' for x in d['neighbour_curve_mean']) + ' |')
