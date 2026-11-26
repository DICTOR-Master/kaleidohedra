"""The best alignment (27 Nov 2026, c116_orbitpairs.py): one 12-hexagon orbit -> squares, pentagons -> hexagons, the other 12-hexagon
orbit -> heptagons keeps 144 of 174 neighbour pairs; the 30 gained pairs are all 2 apart. With Claude (Anthropic).
Test: is each gained pair one swap (dual edge flip) away, are the 30 swaps pairwise non-touching (no common corner), and does doing
all 30 at once give Minana #377's corners EXACTLY? If so C116 -> Minana is ONE floor, i.e. one layer of Scutoid-Frusta.
Output data/c116/onefloor.json (pairing, swaps)."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json'))); faces, mf = d['faces'], d['minana_faces']
rows = json.load(open(os.path.join(HERE, '../data/c116/orbitpairs.json')))
best = max((r for r in rows if r['best']), key=lambda r: (r['best']['kept'], -r['best']['max_dist']))
sig = {int(k): v for k, v in best['best_pairing'].items()}
SUF = os.environ.get('FLOAT', '')
if SUF:   # 27 Nov: the floating-resin best-synchronized state (c116_float.py), no symmetry imposed
    fl = json.load(open(os.path.join(HERE, '../data/c116/float.json')))[0]; sig = {k: int(v) for k, v in enumerate(fl['pairing'])}
    best = dict(assignment='floating resin, best synchronized (no symmetry imposed)', best=fl)
iv = {v: k for k, v in sig.items()}
print('alignment:', best['assignment'], best['best'], flush=True)
def corners(fl):   # corners = triples of faces meeting at a vertex
    at = {}
    for k, f in enumerate(fl):
        for v in f: at.setdefault(v, set()).add(k)
    assert all(len(s) == 3 for s in at.values()); return {frozenset(s) for s in at.values()}
T0 = corners(faces); T1 = {frozenset(iv[x] for x in t) for t in corners(mf)}
E = lambda T: {frozenset(p) for t in T for p in [(a, b) for a in t for b in t if a < b]}
gain = E(T1) - E(T0); lose = E(T0) - E(T1)
print('corners', len(T0), len(T1), '; pairs to gain', len(gain), 'to lose', len(lose), flush=True)
swaps = []
for e in sorted(gain, key=sorted):
    c, dd = tuple(e)
    cand = [f for f in lose if all(frozenset((x,) + tuple(f)) in T0 for x in (c, dd))]
    swaps.append((e, cand))
one = all(len(c) == 1 for e, c in swaps)
print('every gained pair is exactly one swap of a lost pair:', one, flush=True)
used = []
for e, c in swaps:
    if c:
        a, b = tuple(c[0]); cc, dd = tuple(e); used.append([frozenset((a, b, cc)), frozenset((a, b, dd))])
flat = [t for u in used for t in u]
indep = len(flat) == len(set(flat))
print('the swaps touch no common corner:', indep, flush=True)
T = set(T0)
for u, (e, c) in zip(used, swaps):
    a, b = tuple(c[0]); cc, dd = tuple(e); T -= set(u); T |= {frozenset((a, cc, dd)), frozenset((b, cc, dd))}
exact = T == T1
print('all swaps at once give Minana #377 corners exactly:', exact, flush=True)
json.dump(dict(assignment=best['assignment'], pairing={str(k): v for k, v in sig.items()},
               swaps=[[sorted(e), sorted(c[0]) if c else None] for e, c in swaps]), open(os.path.join(HERE, f'../data/c116/onefloor{"_float" if SUF else ""}.json'), 'w'))
print('ONE FLOOR' if one and indep and exact else 'NOT ONE FLOOR')
print('gained pairs at distance 2 (one swap each):', sum(1 for e, c in swaps if c), 'of', len(swaps), flush=True)
print('FINAL ok' if len(T0) == len(T1) == 116 else 'FINAL FAIL (corner counts)')
