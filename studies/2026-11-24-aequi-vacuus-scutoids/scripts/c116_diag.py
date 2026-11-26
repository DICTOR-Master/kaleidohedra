"""Diagnostic (26 Nov): at the best state of the floor search (132/174), why is each missing Minana pair not one swap away?"""
import os, json
os.environ.setdefault('PAIRFILE', 'pairing_local.json'); os.environ['DEPTH'] = '1'
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c116_stages.py')).read().split("sc, T, path = best")[0]
exec(src)
sc, T, path = best; cur = E(T); missing = target - cur; extra = cur - target
print('state', sc, '/174; missing', len(missing), 'extra', len(extra))
from collections import Counter
why = Counter()
for p in missing:
    c, d = tuple(p); common = [x for x in range(60) if frozenset((c, x)) in cur and frozenset((d, x)) in cur]
    es = [frozenset((a, b)) for i, a in enumerate(common) for b in common[i + 1:] if frozenset((a, b)) in cur
          and frozenset((a, b, c)) in T and frozenset((a, b, d)) in T]
    if not es: why['not opposite across any edge (long, needs more than one swap)'] += 1
    elif all(e in target for e in es): why['the edge to swap is itself a Minana pair (swap would lose one)'] += 1
    else: why['one swap would do it, but its symmetry orbit fails'] += 1
print(dict(why)); print('FINAL ok' if sum(why.values()) == len(missing) == 42 else 'FINAL FAIL (unexpected count)')
