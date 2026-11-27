# Samson (D71), turn 1, doubling rule: the star beside its hull with pits dug under each face down to the star (axis pits, the test's
# picture). Panels: (0) the star: solid core S (grey) and its spikes (sand); (1) the hull see-through with the pits solid (rose);
# (2) both together: star solid, pits see-through. House renderer. With Claude (Anthropic).
import json, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/k-research/studies/2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
src = open(os.path.expanduser('~/k-research/studies/2026-11-27-vacuus-solids-4d/scripts/plates4d.py')).read(); g = {'__file__': os.path.expanduser('~/k-research/studies/2026-11-27-vacuus-solids-4d/scripts/plates4d.py')}
exec(src[:src.index('out_scenes, meta = [], []')], g); hull_part = g['hull_part']
from scipy.spatial import ConvexHull
A = json.load(open('/tmp/all_stars.json')); sh = next(s for s in A if s['D'] == 'D71' and s['t'] == '2'); T = sh['turns'][int(os.environ.get('TURN', '1')) - 1]
V = np.array(T['solid']['vertices']); F = T['solid']['faces']; tips = np.array(T['tips']); c0 = V.mean(0); V -= c0; tips -= c0
core, _ = hull_part(V, '#8f8a80', rad=0.006)
spikes = [hull_part(np.vstack([V[f], [tp]]), '#d9cdb4', rad=0.006)[0] for f, tp in zip(F, tips)]
P = np.vstack([V, tips]); h = ConvexHull(P); fs = {}
for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(sm)
Sp = []
for f in F:
    X = V[f]; n = np.cross(X[1] - X[0], X[2] - X[0]); n /= np.linalg.norm(n); n = n if n @ X[0] > 0 else -n; Sp.append((n, n @ X[0]))
pits = []
for k, idx in fs.items():
    n = np.array(k[:3]); n /= np.linalg.norm(n); d = -k[3]; s = min(dd / (m @ n) for m, dd in Sp if m @ n > 1e-12)
    if d - s < 1e-9: continue
    pits.append(hull_part(np.vstack([P[list(idx)], [s * n]]), '#c99e95', rad=0.006)[0])
hullp, _ = hull_part(P, '#e9e4da', alpha=0.22, rad=0.007)
R = np.linalg.norm(P, axis=1).max(); E = float(2.3 * R); dv = [0.55, 0.35, 1.0]
scenes = [{'E': E, 'dir': dv, 'parts': [core] + spikes}, {'E': E, 'dir': dv, 'parts': [hullp] + pits},
          {'E': E, 'dir': dv, 'parts': [core] + spikes + [dict(p, a=0.35) for p in pits]}]
os.makedirs('/tmp/samson' + os.environ.get('TURN', '1'), exist_ok=True); R3.write('/tmp/samson' + os.environ.get('TURN', '1') + '/samson.html', scenes); print('scenes', len(scenes), 'pits', len(pits), 'spikes', len(spikes))
print('FINAL ok' if pits and spikes else 'FINAL FAIL')
