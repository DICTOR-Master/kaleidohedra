"""Step 1 analysis: tabulate nested / minimal against core size, die type and the neighbour changes needed (27 Nov 2026).
With Claude (Anthropic). Reads data/hs_*_sample.jsonl. Prints counts per core and size, and the cases that fail, with their features."""
import json, glob, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(HERE, '../data/hs_*_sample.jsonl'))):
    seen = set()
    for l in open(f):
        r = json.loads(l)
        if r['die'] in seen: continue
        seen.add(r['die']); rows.append(r)
print('pairs:', len(rows), Counter(r['core'] for r in rows))
for core in sorted({r['core'] for r in rows}):
    R = [r for r in rows if r['core'] == core]
    for i, rho in enumerate(R[0]['by_rho'] and [b['rho'] for b in R[0]['by_rho']]):
        nb = [r['by_rho'][i] for r in R]
        print(f'{core} rho {rho}: nested {sum(b["nested"] for b in nb)}/{len(nb)}, minimal {sum(b["minimal"] for b in nb)}/{len(nb)}, '
              f'nested and minimal {sum(b["nested"] and b["minimal"] for b in nb)}')
    for simple in (True, False):
        S = [r for r in R if r['die_simple'] == simple]
        if S: print(f'   die corners all three-way = {simple}: {len(S)} dice; minimal at smallest size {sum(r["by_rho"][0]["minimal"] for r in S)}; '
                    f'nested at largest size {sum(r["by_rho"][-1]["nested"] for r in S)}')
    zero = [r for r in R if r['to_gain'] == 0 and r['to_lose'] == 0]
    print(f'   same pattern (no change needed): {len(zero)}; all nested at every size: {all(all(b["nested"] for b in r["by_rho"]) for r in zero)}')
    fails = [r for r in R if not all(b['nested'] for b in r['by_rho'])]
    for r in fails[:8]:
        print(f'   not nested: die {r["die"]} simple {r["die_simple"]} to lose/gain {r["to_lose"]}/{r["to_gain"]} kept {r["kept"]}/{r["edges_core"]} '
              f'nested by size {[b["nested"] for b in r["by_rho"]]} minimal {[b["minimal"] for b in r["by_rho"]]}')
