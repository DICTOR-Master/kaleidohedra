# exploration: the 4 Nov edge-to-edge DFS restricted to class O (pieces parallel to the 30 pyramids of one RT)
import sys, os, numpy as np, time
maxd = int(sys.argv[1]); cap = int(sys.argv[2]); kind = sys.argv[3]
sys.argv = [sys.argv[0], '1', '1', kind]
src = open(os.path.expanduser('~/k-research/studies/2026-11-04-rt-pyramids/scripts/rt_pyramids.py')).read().split('maxd = int(')[0]
exec(src)
def key(t):
    s = t - t[0]; return tuple(sorted(tuple(np.round(p, 6)) for p in s[1:]))
# class O: the I_h (resp. O_h) images = the pyramids of the solid round the same centre
import itertools
if kind == 'RT': faces = [np.array([v for v in RTV if abs(v @ n - 1) < 1e-8]) for n in ID]
O = {key(np.vstack([np.zeros(3), f])) for f in faces}
print('class O size', len(O))
_sc = sector_candidates
def sector_candidates(t, i, j, dih): return [[c for c in cs if key(c) in O] for cs in _sc(t, i, j, dih)]
st = {'nodes': 0, 'cap': cap, 'capped': False, 't0': time.time(), 'maxd': maxd}
todo = [(0, a, b, d, kk) for a, b, d in E0 for kk in range(int(round(2*math.pi/d)) - 1)]
KIND = kind + 'classO'
ok = search([P0], todo, maxd, st)
print({'best_patch': st.get('best_patch'), 'some_branch_reaches_max': ok, 'nodes': st['nodes'], 'capped': st['capped']})
