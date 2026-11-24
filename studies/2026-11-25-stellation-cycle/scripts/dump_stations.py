"""Exact corners of the Dharma stations O (DICTO Ogdoecontahedron) and rTI, and the Dharma icosahedron, rebuilt by the Progenitors
study's own code (as loose_step.py); written as exact strings and floats for gaps.py. Run from inside study 2026-10-16-progenitors.
-> ../2026-11-25-stellation-cycle/data/stations.json"""
import os, sys, json
_c = os.chdir
os.chdir = lambda p: _c(os.path.expanduser(p).replace("/kaleidohedra/", "/k-research/"))
import builtins
_o = builtins.open
builtins.open = lambda p, *a, **k: _o(os.path.expanduser(p).replace("/kaleidohedra/", "/k-research/") if isinstance(p, str) else p, *a, **k)
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
builtins.open = _o
os.chdir = _c
OUT = os.path.expanduser('~/k-research/studies/2026-11-25-stellation-cycle')
S = dict(C)
def ex(v): return [[str(x.a), str(x.b)] for x in v]
def fl(v): return [float(x.a) + float(x.b) * 5 ** .5 for x in v]
res = {k: dict(exact=[ex(v) for v in V], float=[fl(v) for v in V]) for k, V in (('O', S['O']), ('rTI', core), ('I', S['I']), ('ID', S['ID']) if 'ID' in S else ('I', S['I']))}
json.dump(res, open(os.path.join(OUT, 'data/stations.json'), 'w'))
print({k: len(v['float']) for k, v in res.items()}, 'keys in C:', list(S.keys()))
print('I corner 0:', res['I']['float'][0])
print('FINAL ok' if len(res['O']['float']) == 102 and len(res['rTI']['float']) == 90 else 'FINAL FAIL')
