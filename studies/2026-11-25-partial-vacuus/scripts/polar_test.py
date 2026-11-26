# DICTO · is there a Resonus counterpart of the Vacuus-Solids? Polar test of the twelve special sizes (26 Nov 2026).
# With Claude (Anthropic). DICTO: "get it happening asap; even a negative result is a result".
# Hypothesis (from the polar link: Vacuus plates <-> polar edges, Resonus planes <-> polar corners): the polar reciprocal of a special
# Vacuus-Solid of P is a SPIKED P* (pyramids raised on the faces of the polar P*, tips on P*'s face axes) at an exact height.
# Polar reciprocal (in the unit sphere) of the pit surface E: one corner per distinct wall PLANE (its pole; coplanar walls give one
# corner, as in the classical star polyhedra), one face per corner of E (the poles of the walls round it).
# Each corner of the reciprocal D is classified against P*: (a) a corner of P* (scaled), (b) on a face axis of P* (= a corner direction
# of P) beyond that face: a spike tip, (c) on an edge line of P*, (d) other. The hypothesis holds for a solid when D's corners are
# P*'s own corners plus spike tips only. Control: the great dodecahedron (icosahedron at 3sqrt5 - 6) must give the small stellated
# dodecahedron (12 corners, all spike tips on the dodecahedron's face axes, at the known height).
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])
EX = json.load(open(os.path.join(HERE, '../data-exact-forms.json'))); out = []
def uniq(X, tol=1e-7):
    U = []
    for x in X:
        if not any(np.linalg.norm(x - u) < tol for u in U): U.append(x)
    return np.array(U)
for e in EX:
    V, F, N, D_ = S[e['P']]; s = e['s']; A = s * D_[:, None] * N
    poles = []
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]):
            n = np.cross(V[b] - V[a], A[fi] - V[a]); n /= np.linalg.norm(n); d = n @ V[a]
            poles.append(n / d)                      # pole of the wall plane n.x = d (d may be negative: plane on the far side)
    Dv = uniq(np.array(poles))
    # P*: corners n_f / d_f (P's face poles); its face axes = P's corner directions; its faces: planes v.x = 1 for corners v of P
    Pstar = N / D_[:, None]; vdir = V / np.linalg.norm(V, axis=1)[:, None]
    cls = {'P* corner': 0, 'spike tip on a P* face axis': 0, 'on a P* edge line': 0, 'other': 0}; heights = set()
    E2 = []
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            pass
    for x in Dv:
        if any(np.linalg.norm(x - p) < 1e-7 for p in Pstar): cls['P* corner'] += 1; continue
        on_axis = [k for k, u in enumerate(vdir) if np.linalg.norm(np.cross(x, u)) < 1e-7 * max(1, np.linalg.norm(x)) and x @ u > 0]
        if on_axis:
            k = on_axis[0]; h = (x @ vdir[k]) * np.linalg.norm(V[k])   # height in units of P*'s face distance 1/|v|: h = |x| / (1/|v|)
            cls['spike tip on a P* face axis'] += 1; heights.add(round(h, 9)); continue
        # edge line of P*: the line of two adjacent P* corners (faces f, g of P sharing an edge)
        hit = False
        for fi in range(len(F)):
            for gj in range(fi + 1, len(F)):
                if len(set(F[fi]) & set(F[gj])) == 2:
                    p, q = Pstar[fi], Pstar[gj]; dvec = q - p
                    if np.linalg.norm(np.cross(x - p, dvec)) < 1e-7 * np.linalg.norm(dvec): hit = True; break
            if hit: break
        cls['on a P* edge line' if hit else 'other'] += 1
    spiked = cls['on a P* edge line'] == 0 and cls['other'] == 0 and cls['spike tip on a P* face axis'] > 0
    r = dict(P=e['P'], Q=e['Q'], s=e['closed'], reciprocal_corners=len(Dv), classes=cls, spike_heights=sorted(heights), spiked_Pstar=spiked)
    out.append(r); print(f"{e['P']:24s} on {e['Q']:28s} s={e['closed']:24s} D corners {len(Dv):3d} {cls}  spike heights {sorted(heights)}  SPIKED P*: {spiked}", flush=True)
json.dump(out, open(os.path.join(HERE, '../data-polar-test.json'), 'w'), indent=1)
gd = next(r for r in out if r['P'] == 'icosahedron' and r['Q'] == 'dodecahedron')
ctrl = gd['reciprocal_corners'] == 12 and gd['classes']['spike tip on a P* face axis'] == 12
print('control (great dodecahedron -> small stellated dodecahedron: 12 spike tips on the dodecahedron face axes):', ctrl)
print('hypothesis holds for', sum(r['spiked_Pstar'] for r in out), 'of', len(out))
print('FINAL ok' if ctrl else 'FINAL FAIL (control)')
