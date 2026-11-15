"""Markdown tables from results/*.json (no hand-copied numbers). Usage: summarise.py RESULTS_DIR"""
import sys, json, glob, os
import numpy as np
R = sys.argv[1]
print('### Toy runs (exact events)\n')
print('| run | N | base step | contact gained | contact lost | births | deaths | clumps | simultaneous at 1e-9 | Euler / shift / margin / balance failures | mean contacts per cell | contact changes per cell per unit time |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for f in sorted(glob.glob(f'{R}/toy-*-N*-dt*.json')):
    s = json.load(open(f))['summary']; c = s['counts']
    print(f"| {s['mode']} | {s['N']} | {s['dt0']} | {c.get('contact gained', 0)} | {c.get('contact lost', 0)} | {c.get('birth', 0)} | {c.get('death', 0)} | "
          f"{c.get('clump', 0)} | {s['stats'].get('simultaneous', 0)} | {s['euler_fail']} / {s['robust_fail']} / {s['stats'].get('margin_fail', 0)} / {s['balance_fail']} | "
          f"{s['mean_contacts_per_cell']:.3f} | {s['contact_changes_per_cell_per_unit_time']:.2f} |")
print('\n### Fixed-step sampling of the toy (no halving): share of seen contact changes that come alone\n')
print('| run | step | seen contact changes per cell per step | share alone |')
print('|---|---|---|---|')
for f in sorted(glob.glob(f'{R}/toy-coarse-*.json')):
    d = json.load(open(f))
    for r in d['rows']: print(f"| {d['mode']} N={d['N']} | {r['dt']} | {r['seen_per_cell_per_step']:.3f} | {r['alone_share']:.3f} |")
print('\n### Void basins\n')
print('| run | R (Mpc/h) | a range | spacing Delta a | wall min (faces) | basins first / last | mean contacts first / last | contact changes seen | per basin per step | share alone | clumped with other contact changes | with a merge or split | basins merged | basins split | contact changes per merged basin | lost and regained next step | balance failures |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for f in sorted(glob.glob(f'{R}/basins-*.json')):
    d = json.load(open(f)); name = os.path.basename(f)[7:-5]
    da = d['nbody']['da']; amin_a = d.get('a_min', 0) or d['nbody']['snapshots'][0]['a']
    for v in d['variants']:
        st = v['snapshots_used'] - 1; nb = np.mean(v['basins_first_last']); D = v['derived']; cc = v['contact_changes_total']
        print(f"| {name} | {d['R_Mpc_h']:g} | {max(amin_a, d['nbody']['snapshots'][0]['a']):.3g}-1 | {v['k'] * da:.4g} | {v['amin']} | {v['basins_first_last'][0]} / {v['basins_first_last'][1]} | "
              f"{v['mean_contacts_first_last'][0]:.2f} / {v['mean_contacts_first_last'][1]:.2f} | {cc} | {cc / st / nb:.3f} | {v['fraction_alone']:.3f} | "
              f"{D.get('contact changes, clumped with other contact changes', 0) / cc:.3f} | {D.get('contact changes, with a merge/split/birth/death', 0) / cc:.3f} | "
              f"{D.get('cells died (merge or death)', 0)} | {D.get('cells born (split or birth)', 0)} | {v['contact_changes_per_merge']:.1f} | "
              f"{v['regained_next_step']} of {v['lost_total']} lost | {v['balance_failures']} |")
p = f'{R}/toy-static-degree.json'
if os.path.exists(p):
    d = json.load(open(p))
    print(f"\n### Mean contacts per cell, periodic Poisson-Voronoi (4 seeds each; target 48π²/35 + 2 = {d['target']:.4f})\n")
    print('| N | mean | error of mean |'); print('|---|---|---|')
    for r in d['rows']: print(f"| {r['N']} | {r['mean']:.4f} | {r['sd_of_mean']:.4f} |")
