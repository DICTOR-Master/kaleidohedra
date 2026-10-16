# Fable, GBPC pass 4: compact summary of the search results (the full body lists stay on dicto-node in ~/gbpc4/data/search-*.json).
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
S = {'mark': 'DICTO · dictospheres.com', 'note': 'volumes "a|b" = a + b*sqrt5 per bcc cell, |v| units cubed; full body lists on dicto-node ~/gbpc4/data', 'runs': {}}
for f in sorted(glob.glob(os.path.join(STUDY, 'data', 'search-*.json'))):
    d = json.load(open(f))
    S['runs'][os.path.basename(f)] = {k: d[k] for k in ('mode', 'seed', 'restarts', 'best_fill_float', 'best_volume_exact', 'gap_volume_exact', 'counts', 'n_axes')}
json.dump(S, open(os.path.join(STUDY, 'data', 'gbpc-search-summary.json'), 'w'), indent=1)
for k, v in S['runs'].items(): print(k, v['mode'], round(v['best_fill_float'], 4), v['counts'])
