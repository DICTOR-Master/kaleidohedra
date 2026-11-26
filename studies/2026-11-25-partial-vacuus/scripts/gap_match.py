# DICTO · partial Vacuus: do excavated solids fill the gaps of the nested shells? (26 Nov 2026). With Claude (Anthropic).
# DICTO: "are there any here that would fill the gaps precisely in our nested shell work; vajrayana, double vision et al?"
# Golden cycle (Progenitors #34 / Vajrayana #35): twelve stations with exact corners (study 2026-10-25-gnomon-shapes,
# stations-exact.json, triangles in Q(sqrt5)). For every station X and every step X -> Y:
#  (a) is X an excavated solid of its own hull P: X = P minus one pyramid on every face of P, apex on the face axis at one common
#      fraction s?  (corners of X = corners of P + one apex per face; volume X = vol P - sum of the pits; all apexes at one s)
#  (b) is the gap Y \ X exactly the pits of an excavated solid (Y convex = P and X = excavated P), or does X fill the pits of Y?
# Volumes exact in floating point from the triangles (signed tetrahedra about O); 1e-9.
import json, os, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../2026-10-25-gnomon-shapes/stations-exact.json')
r5 = 5 ** .5
def val(p): a, b = p; return eval(a.replace('/', '/1.0/') if False else a) if False else float(eval(a + '+0')) + float(eval(b + '+0')) * r5
def fl(q): return float(eval(q[0] + '*1.0')) + float(eval(q[1] + '*1.0')) * r5
st = json.load(open(G))
def solid(tris):
    T = np.array([[[fl(c) for c in v] for v in t] for t in tris]); vol = sum(np.dot(t[0], np.cross(t[1], t[2])) for t in T) / 6
    P = np.unique(np.round(T.reshape(-1, 3), 9), axis=0); return T, abs(vol), P
def excavated_of_hull(P, vol):
    H = ConvexHull(P); hv = H.volume
    planes = {}
    for eq, sm in zip(H.equations, H.simplices):
        k = tuple(np.round(eq, 7)); planes.setdefault(k, set()).update(sm)
    hullc = set(H.vertices); inner = [i for i in range(len(P)) if i not in hullc]
    res = dict(hull_faces=len(planes), hull_corners=len(hullc), inner_corners=len(inner), volume=vol, hull_volume=hv)
    if not inner or abs(vol - hv) < 1e-9: res['excavated'] = False; return res
    S = []; pits = 0.0; ok = True
    for k, idx in planes.items():
        n = np.array(k[:3]); d = -k[3]; F = P[list(idx)]; c = F.mean(0)
        on_axis = [i for i in inner if np.linalg.norm(np.cross(P[i], n)) < 1e-7 and 0 < P[i] @ n < d]
        if len(on_axis) != 1: ok = False; break
        a = P[on_axis[0]]; S.append(round((a @ n) / d, 7))
        # pit volume: pyramid over the face polygon with apex a
        Fs = F[np.argsort(np.arctan2((F - c) @ np.cross(n, F[0] - c), (F - c) @ (F[0] - c)))]
        area = sum(np.linalg.norm(np.cross(Fs[i] - c, Fs[(i + 1) % len(Fs)] - c)) / 2 for i in range(len(Fs)))
        pits += area * (d - a @ n) / 3
    res['excavated'] = bool(ok and len(set(S)) == 1 and abs(hv - pits - vol) < 1e-7)
    if ok: res['s'] = sorted(set(S)); res['vol_check'] = hv - pits - vol
    return res
names = list(st); out = {}
for nm in names:
    T, vol, P = solid(st[nm]); r = excavated_of_hull(P, vol); out[nm] = r
    print(f"{nm:16s} V {len(P):3d} hull faces {r['hull_faces']:3d} inner corners {r['inner_corners']:3d} vol {vol:.6f} hull {r['hull_volume']:.6f}  excavated of its hull: {r['excavated']}  s {r.get('s')}", flush=True)
steps = []
for x, y in zip(names, names[1:]):
    hy = out[y]; hx = out[x]
    steps.append(dict(step=f'{x} -> {y}', Y_is_hull_of_X=abs(hx['hull_volume'] - hy['volume']) < 1e-7 and hy['inner_corners'] == 0, X_excavated=hx['excavated']))
    print('step', steps[-1], flush=True)
json.dump(dict(stations=out, steps=steps), open(os.path.join(HERE, '../data-gap-match.json'), 'w'), indent=1)
ctrl = out['I']['inner_corners'] == 0 and not out['I']['excavated']   # the icosahedron is convex: not excavated (negative control)
print('FINAL ok' if ctrl else 'FINAL FAIL (control: the icosahedron must read as convex)')
