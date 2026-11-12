"""Diagnostic (12 Nov 2026): where does the broken-marma control yantra (R1, t2's base moved 1/1000) have walls with a count jump of 2?"""
import sys, os
sys.argv = ['x']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yantra_regions import *
K = Ctx(); Y = load_r1(K, shift=(2, Fr(1, 1000)))
A = arrangement(K, Y); faces = A['faces']; S = A['S']; pts = A['pts']
by_edge = {e: fi for fi, f in enumerate(faces) for e in f['edges']}
seen = 0
for (p, q), fi in by_edge.items():
    if (q, p) in by_edge and abs(faces[fi]['c'] - faces[by_edge[(q, p)]]['c']) != 1:
        g = by_edge[(q, p)]
        print('wall', A['edges'][(p, q)], [float(v) for v in pts[p]], [float(v) for v in pts[q]])
        for h in (fi, g):
            print('  face', sorted(faces[h]['tris']), 'area2', float(faces[h]['A2']), 'corners', [(round(float(a), 6), round(float(b), 6)) for a, b in faces[h]['V']],
                  'walk length', len(faces[h]['edges']))
        seen += 1
        if seen == 2: break
print('FINAL ok' if seen else 'FINAL FAIL no exception found')
