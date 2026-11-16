"""Tables for the README section "Space-time slicing at a tilt": reads results/tilt-pilot (or another folder) blocks.jsonl and the
slice JSONs, prints one row per block and direction (core counts per 1000 Mm^2 min and raw)."""
import json, glob, sys
R = sys.argv[1] if len(sys.argv) > 1 else 'results/tilt-pilot'
for l in open(f'{R}/blocks.jsonl'):
    b = json.loads(l[6:]); c = b['checks']; e = b.get('exact')
    print(b['name'], {k: v for k, v in b.items() if k not in ('checks', 'exact', 'shape', 'kind', 'name')})
    print('   ', c)
    if e: print('    exact', e)
for f in sorted(glob.glob(f'{R}/*_t*_v*.json')):
    r = json.load(open(f)); ce = r['core_events']; g = ce.get
    print(f"{r['block']:22s} th{r['theta']:<4} v{r['v']:<4} planes {r['planes']:4d} | swap {g('swap',0)}+{r['core_swaps_twostep']} "
          f"pers {r['core_swaps_persistent']} birth {g('birth',0)} death {g('death',0)} split {g('split',0)} merge {g('merge',0)} "
          f"clump {g('clump',0)} relabel {g('relabel',0)} | truth {r['truth_core']} | euler-bad {r['planes_failing_euler']} "
          f"balance-bad {r['balance_failures']} multi {r['planes_cells_in_several_pieces']} frag {r['digital_fragments_reassigned']} "
          f"morse {r['morse_interior_cells']} vol {r['core_volume_Mm2min']:.0f} {r['seconds']}s")
