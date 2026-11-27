# #51 Version 2 figure: Samson and its first two cores under the Star Cores core rule (doubling rule t = 2), same view direction, each
# panel at its own scale. Panels: Samson (gold, as in #51), core 1, core 2 (the mirror image of core 1, at a third of its size).
# Control: Samson 16 corners / 10 faces; cores 12 corners / 8 faces (4 triangles, 4 hexagons); core 2 corners = -(1/3) x core 1 corners
# up to the common centre (point reflection, scale t/3 with t = 1 in the app's normalised chain is checked as a ratio). House renderer.
import json, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/k-research/studies/2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
src = open(os.path.expanduser('~/k-research/studies/2026-11-27-vacuus-solids-4d/scripts/plates4d.py')).read(); g = {'__file__': os.path.expanduser('~/k-research/studies/2026-11-27-vacuus-solids-4d/scripts/plates4d.py')}
exec(src[:src.index('out_scenes, meta = [], []')], g); hull_part = g['hull_part']
from collections import Counter
A = json.load(open('/tmp/all_stars.json')); sh = next(s for s in A if s['D'] == 'D71' and s['t'] == '2')
cols = ['#c9a24a', '#d8c08a', '#d8c08a']; scenes = []; Vs = []
for k in range(3):
    T = sh['turns'][k]; V = np.array(T['solid']['vertices'], float); V -= V.mean(0); F = T['solid']['faces']; Vs.append(V)
    print('panel', k, 'corners', len(V), 'faces', dict(Counter(len(f) for f in F)))
    p, _ = hull_part(V, cols[k], rad=0.006); R = np.linalg.norm(V, axis=1).max()
    scenes.append({'E': float(2.6 * R), 'dir': [0.55, 0.35, 1.0], 'parts': [p]})
# control: core 2 is the point reflection of core 1, scaled
V1, V2 = Vs[1], Vs[2]; k = np.linalg.norm(V2, axis=1).max() / np.linalg.norm(V1, axis=1).max()
err = max(np.min(np.linalg.norm(V1 * (-k) - v, axis=1)) for v in V2) / np.linalg.norm(V2, axis=1).max()
print('core 2 = -%.6f x core 1, max corner error %.1e' % (k, err))
os.makedirs('/tmp/samsoncores', exist_ok=True); R3.write('/tmp/samsoncores/samson.html', scenes)
ok = len(Vs[0]) == 16 and len(Vs[1]) == 12 and len(Vs[2]) == 12 and err < 1e-9
print('FINAL ok' if ok else 'FINAL FAIL')
