"""Task 2, screen (double precision): does any Aequus with its Resonus inside the 31 planes fit exactly in a gap of the cycle?
For a gap X_in ⊂ X_out and a die P (unit normals u_i, depths d_i):
  s1 = the least scale with X_in inside s1.P   (s1 = max over corners v of X_in and faces i of u_i.v / d_i; X_in touches s1.P)
  t1 = how far s1.P reaches toward X_out        (max over corners x of P and facets (n, h) of X_out of n.(s1 x) / h)
  the die fits in the gap iff t1 <= 1, and closes it (touches both) iff t1 = 1.  Also: the largest scale inside X_out, s2 = s1 / t1.
Gaps (all in the dice frame: five-fold axes along (0, phi, 1)):
  (a) O ⊂ rTI of the Spheres of Dharma with O in D's place (data/stations.json, rebuilt by the Progenitors code);
  (c) the DICTO-Star: its icosidodecahedron ⊂ the hull of the star (#14 data, edge 1; turned x <-> y into this frame);
  (d) the Sunstar: its dodecahedron D0 ⊂ the hull of D0 with six Dogstars (cycle.py, Theorem 5). The Sunstar has only the
      symmetry Th, so each die is tried in the 5 placements that differ by a turn of 72 degrees about a five-fold axis.
Dice: the 4 039 of data/aequi.json (frames '31' and 'primed31'; primed dice are turned x <-> y into placement A).
-> data/gaps.json"""
import json, os, sys, glob, gzip, itertools
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-exact-dice', 'scripts'))
from groups import DIRS, DFAM
phi = (1 + 5 ** .5) / 2
SW = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1.]])
def fams(label): return [p for p in label.split('/')[0].split('+')]
def frame(orbits):
    F = [f for o in orbits for f in fams(o)]
    if any(f.startswith('RD12') for f in F): return 'cube'
    pr = any(f.endswith('p') for f in F); un = any(f in ('D12', 'I12', 'RT24') for f in F)
    return 'both' if (pr and un) else 'primed31' if pr else '31'
def dice():
    for f in sorted(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '*.json'))):
        d = json.load(open(f)); fr = frame(d['orbits'])
        if fr in ('31', 'primed31'):
            yield dict(src='4553', sid=d['sid'], label=d['label'], idx=d['face_directions'], sizes=d['orbit_sizes'], depths=[float(x) for x in d['depths_60_digits']], fr=fr)
    for p in ['2a', '2caps', '2caps2', '2caps3']:
        for d in json.load(open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'dice%s-new.json' % p))):
            ev = lambda x: eval(x) if isinstance(x, str) else x
            lab = d['label'].split(': ', 1)[1]; orbits = [o.strip() for o in lab.split(' + ')]; fr = frame(orbits)
            if fr in ('31', 'primed31'):
                yield dict(src='ext ' + p, sid=d['sid'], label=d['label'], idx=ev(d['idx']), sizes=ev(d['sizes']), depths=[float(x) for x in ev(d['depths'])], fr=fr)
def hull_planes(V):
    H = ConvexHull(V); E = H.equations; n = E[:, :3]; h = -E[:, 3]; return n, h, V[H.vertices]
st = json.load(open(os.path.join(HERE, '..', 'data', 'stations.json')))
O = np.array(st['O']['float']); rTI = np.array(st['rTI']['float'])
star = json.load(open(os.path.join(ST, '..', 'papers', 'dicto-star', 'data', 'dicto-star.json')))['pieces']
Vstar = np.vstack([np.array(v, float).reshape(-1, 3) for k, v in star.items() if k != 'icosidodecahedron' and len(np.array(v, float).ravel()) % 3 == 0] +
                  [np.array(star['icosidodecahedron'], float)]) @ SW
IDs = np.array(star['icosidodecahedron'], float) @ SW
D0 = np.array([s for s in itertools.product((1, -1), repeat=3)] + [np.roll((0, a / phi, b * phi), k) for a in (1, -1) for b in (1, -1) for k in range(3)], float)
Is = np.array([np.roll((0, a * phi, b), k) for a in (1, -1) for b in (1, -1) for k in range(3)], float)
sun = [D0]
for i in range(3):
    for sg in (1, -1):
        c = np.zeros(3); c[i] = 2 * sg; sun += [c + Is / phi ** 2, c + np.array(list(itertools.product((1, -1), repeat=3)), float)]
Vsun = np.vstack(sun)
GAPS = {'a': (O, hull_planes(rTI)), 'c': (IDs, hull_planes(Vstar)), 'd': (D0, hull_planes(Vsun))}
for g, (Xin, (n, h, V)) in GAPS.items():
    assert (Xin @ n.T / h).max() < 1 - 1e-6, g      # the inner station lies strictly inside the outer one
def rot5(k):
    a = np.array([0, phi, 1.]); a /= np.linalg.norm(a); t = 2 * np.pi * k / 5; K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
R5 = [rot5(k) for k in range(5)]
out = {g: [] for g in GAPS}; n_d = 0
for d in dice():
    U = DIRS[d['idx']]; U = U @ SW if d['fr'] == 'primed31' else U
    Dd = np.repeat(d['depths'], d['sizes'])
    V = HalfspaceIntersection(np.hstack([U, -Dd[:, None]]), np.zeros(3)).intersections
    n_d += 1
    for g, (Xin, (n, h, Vo)) in GAPS.items():
        for k, R in enumerate(R5 if g == 'd' else R5[:1]):
            UR, VR = U @ R.T, V @ R.T
            s1 = (Xin @ UR.T / Dd).max(); t1 = ((s1 * VR) @ n.T / h).max()
            out[g].append((float(t1), d['src'], str(d['sid']), d['label'], k, float(s1)))
    if n_d % 500 == 0: print('PROGRESS %.2f' % (n_d / 4039), flush=True)
res = dict(n_dice=n_d)
for g in GAPS:
    L = sorted(out[g]); fit = [x for x in L if x[0] <= 1 + 1e-9]; touch = [x for x in L if abs(x[0] - 1) < 1e-9]
    res[g] = dict(fits=len(fit), touches_both=len(touch), best=L[:12], touching=touch)
    print('gap', g, 'tests', len(L), 'fit', len(fit), 'touch both', len(touch), 'smallest reach t1:', [(round(x[0], 6), x[1], x[2], x[3], x[4]) for x in L[:6]])
json.dump(res, open(os.path.join(HERE, '..', 'data', 'gaps.json'), 'w'), indent=1)
print('FINAL ok' if n_d == 4039 else 'FINAL FAIL: %d dice' % n_d)
