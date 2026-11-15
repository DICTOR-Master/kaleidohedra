"""Markdown table from census JSON files. Usage: summarize.py FILE.json ... > table.md"""
import sys, json
print('| setting | step (min) | interior cells | mean n, mu2 | births / deaths | splits / merges | clumps | swaps: elementary / flicker-free W20 / two-sided P20 | P20 swaps per cell-hour | P20 swaps per new cell | Euler-bad frames |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for f in sys.argv[1:]:
    d = json.load(open(f))
    for s, r in d['steps'].items():
        c = r['counts_interior']; w = r['by_W'].get('20.0', {}); p = r.get('two_sided', {}).get('20.0', {})
        newc = c.get('birth', 0) + c.get('split', 0) - w.get('split_flicker', 0)
        spn = p.get('persistent', 0) / newc if newc > 0 and p else None
        f2 = lambda x: '-' if x is None else f'{x:.2f}'
        print(f"| sigma {d['sigma']}, h {d['h']} | {r['dt_min']:.1f} | {r['mean_interior_cells']:.0f} | {f2(r['mean_n_interior'])}, {f2(r['mu2'])} | "
              f"{c.get('birth', 0)} / {c.get('death', 0)} | {c.get('split', 0)} / {c.get('merge', 0)} | {c.get('clump', 0)} | "
              f"{r['swaps_elementary']} / {w.get('swaps_persistent', '-')} / {p.get('persistent', '-')} of {p.get('judged', '-')} | "
              f"{f2(p.get('per_cell_hour'))} | {f2(spn)} | {r['frames_euler_bad']} / {r['frames']} |")
