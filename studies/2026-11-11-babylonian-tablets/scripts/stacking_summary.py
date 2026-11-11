"""Summary of tablet_stacking.py over the catalogue: medians by genre and period (whole groups of at least 5)."""
import json, re, sys, statistics as st
from collections import defaultdict
R = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2]))
idx = {}
for k, v in C.items(): idx.setdefault(re.sub(r'\D', '', k), v.get('from_cdli_search_view', {}) or {})
rows = []
for r in R.values():
    c = idx.get(re.sub(r'\D', '', r['hs']), {})
    r['gen'] = str(c.get('genre', '') or 'unknown').split(';')[0].strip() or 'unknown'
    r['per'] = re.sub(r'\s*\(.*', '', str(c.get('period', '') or 'unknown')) or 'unknown'; rows.append(r)
def s(rs, lab):
    if len(rs) < 5: return
    m = lambda k: st.median(x[k] for x in rs)
    e = st.mean(x['drop_long_edge'] + x['drop_short_edge'] for x in rs); n = sum(bool(x['can_stand_on_edge']) for x in rs)
    print(f"{lab:32s} n={len(rs):3d} sag flat {m('sag_flat'):.3f} round {m('sag_round'):.3f} stable {m('stable_positions'):.0f} edge drops {e:.3f} stands on edge {n}/{len(rs)}")
s(rows, 'ALL')
g = defaultdict(list)
for r in rows: g['genre ' + r['gen']].append(r); g['period ' + r['per']].append(r)
for k in sorted(g, key=lambda k: -len(g[k])): s(g[k], k[:32])
print('FINAL ok' if rows else 'FINAL FAIL')
