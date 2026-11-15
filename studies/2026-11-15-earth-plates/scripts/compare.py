"""Tables for the README from results/*.json (earth_mesh.py series outputs). Light: reads JSON only.
Usage: python compare.py results/*.json"""
import sys, json, os
from collections import Counter, defaultdict
CL = ('swap', 'birth', 'death', 'split', 'merge', 'relabel', 'clump')

def window_counts(res, step, L, lo, hi):
    """Counts per class for events with t0 in (lo, hi] Ma, from the per-100 bins is too coarse; use swap_times + per100 only
    when the window is whole 100s. Here: events file is needed; so use per100 bins that lie inside [lo, hi]."""
    c = next(r for r in res['census'] if r['step'] == step and r['Lmin'] == L)
    out = Counter()
    for k, v in c['per100'].items():
        a, b = [int(x) for x in k.split(' ')[0].split('-')]
        if a >= lo and b <= hi: out.update(v)
    return out

for path in sys.argv[1:]:
    R = json.load(open(path)); print(f"\n## {R['model']} rule {R['rule']}  tmax {R['tmax']}  level {R['level']} ({R['spacing_km']:.1f} km)")
    pb = R['plates_by_time']; ks = sorted(pb, key=lambda x: -int(x)); print('plates:', {k: pb[k] for k in ks[::max(1, len(ks) // 8)]}, 'now', pb['0'])
    inf = R['infos']
    print('max gap (rigid) %.4f  max overlap %.4f  sliver pieces merged %d  labels below resolution in %d frames' % (
        max(i['gap_rigid_frac'] for i in inf), max(i['overlap_rigid_frac'] for i in inf), sum(i['sliver_pieces_merged'] for i in inf),
        sum(bool(i['labels_below_resolution']) for i in inf)))
    print('| step | Lmin | frames fail | ' + ' | '.join(CL) + ' | swaps direct+4fold | persistent k=1,2,5 (censored k=5) | bal | neg |')
    for r in R['census']:
        c = r['counts']
        print(f"| {r['step']} | {r['Lmin']} | {r['frames_failing']} | " + ' | '.join(str(c.get(x, 0)) for x in CL) +
              f" | {r['swaps_direct']}+{r['swaps_fourfold']} | {r['swaps_persistent']['1']},{r['swaps_persistent']['2']},{r['swaps_persistent']['5']} ({r['swaps_persistent_censored']['5']}) | {r['balance_failures']} | {r['neg_control_caught']} |")
    p = R['pair_rule_step1_L0']; print('pair rule (old), step 1, Lmin 0:', p['counts'], 'one-contact clumps:',
          {k: v for k, v in p['clump_patterns'].items() if k.endswith('lost 1 gained 0') or k.endswith('lost 0 gained 1')})
    c1 = next(r for r in R['census'] if r['step'] == 1 and r['Lmin'] == 0)
    print('by-boundary, step 1, Lmin 0, one-contact clumps:', {k: v for k, v in c1['clump_patterns'].items() if k.endswith('lost 1 gained 0') or k.endswith('lost 0 gained 1')})
