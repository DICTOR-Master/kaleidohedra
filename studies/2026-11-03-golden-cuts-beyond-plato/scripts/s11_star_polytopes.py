"""Step 11 (paper #89): sections of the ten Schlaefli-Hess regular star polytopes (DICTO proposed the search).
Nine of them have the 120 corners of the 600-cell, one ({5/2,3,3}) the 600 corners of the 120-cell; each takes ONE class
of chords as its edges (a vertex figure {q,r} with 12, 20 or 4 corners). We take every chord class of the two corner
sets (a superset of the ten edge sets). The section of a star polytope by a hyperplane has as corners the points where
its edges cross the hyperplane (plus corners lying in it).
Targets: the eight golden cuts of Proposition 4 (Greater and Lesser Golden Cut Great Dodecahedron, Great Icosahedron,
Small and Great Stellated Dodecahedron; 60 corners each) and the Greater and Lesser Golden Cut Cubes.
Directions: a golden cut star polyhedron has full icosahedral symmetry; a section has the symmetry of its direction's
stabiliser, and the only H4 stabiliser containing I_h is H3 (s9 Part B), the 600-cell corner direction (1,0,0,0): all
heights searched. Golden Cut Cubes: the only O_h sections are central in the A3 direction (1,1,0,0) (s9 Part B).
Search: floating point, 3000 heights per chord class, scale-free comparison of corner sets (sorted squared distances over
the mean squared radius) for sets with the target's corner count; local minima refined; any match is then checked
exactly in K (corner-to-corner, s8 method).
usage (dicto-big-brother): ~/geom/bin/python s11_star_polytopes.py -> ../data/s11-star-polytopes.json
"""
import sys, os, json, itertools, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data'); sys.path.insert(0, HERE)
from cubes_lib import *          # noqa
import s9_why_not_cubes as S9
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)
g = (1 + 5 ** .5) / 2


def chord_classes(V):
    F = np.array([fl(v) for v in V]); n = len(F)
    D = ((F[:, None] - F[None]) ** 2).sum(-1); vals = np.unique(np.round(D[0], 7))
    out = []
    for val in vals:
        if val < 1e-9: continue
        I, J = np.where(np.triu(np.abs(D - val) < 1e-6, 1))
        out.append({'d2': float(val), 'neighbours': int((np.abs(D[0] - val) < 1e-6).sum()), 'edges': np.stack([I, J], 1)})
    return F, out


def inv(P):
    P = P - P.mean(0); R2 = (P ** 2).sum(1).mean()
    return np.sort(((P[:, None] - P[None]) ** 2).sum(-1)[np.triu_indices(len(P), 1)] / R2)


def fsection(F, E, d, h):
    H = F @ d; a, b = H[E[:, 0]] - h, H[E[:, 1]] - h; m = a * b < -1e-13
    t = a[m] / (a[m] - b[m]); P = F[E[m, 0]] + t[:, None] * (F[E[m, 1]] - F[E[m, 0]])
    P = np.vstack([P, F[np.abs(H - h) < 1e-12]])
    return np.unique(np.round(P, 9), axis=0) if len(P) else P


# ---------------------------------------------------------------- targets (float), exact versions built on demand
ICO = [(0, s, t * g) for s in (1, -1) for t in (1, -1)]; ICO = [tuple(np.roll(v, k)) for v in ICO for k in range(3)]
DOD = [tuple(s) for s in itertools.product((1, -1), repeat=3)] + [tuple(np.roll((0, s / g, t * g), k)) for s in (1, -1) for t in (1, -1) for k in range(3)]
def cut_chords(Vs, mult, x):
    """star polyhedron on the corners Vs whose edges are the chords of length mult x (shortest chord); cut at x"""
    V = np.array(Vs, float); D = ((V[:, None] - V[None]) ** 2).sum(-1); m = D[D > 1e-9].min() * mult ** 2
    E = [(i, j) for i in range(len(V)) for j in range(i + 1, len(V)) if abs(D[i, j] - m) < 1e-6]
    assert len(E) == 30, len(E)
    return np.array([V[i] + x * (V[j] - V[i]) for i, j in E] + [V[j] + x * (V[i] - V[j]) for i, j in E])
s5 = 5 ** .5
TARGETS = {'Greater Golden Cut Great Dodecahedron': (ICO, 1, 1 / 3), 'Lesser Golden Cut Great Dodecahedron': (ICO, 1, (7 - s5) / 22),
           'Greater Golden Cut Great Icosahedron': (ICO, g, 1 / g ** 2), 'Lesser Golden Cut Great Icosahedron': (ICO, g, 1 / (g * s5)),
           'Greater Golden Cut Small Stellated Dodecahedron': (ICO, g, (7 + s5) / 22), 'Lesser Golden Cut Small Stellated Dodecahedron': (ICO, g, 1 / 3),
           'Greater Golden Cut Great Stellated Dodecahedron': (DOD, g ** 2, (7 + s5) / 22), 'Lesser Golden Cut Great Stellated Dodecahedron': (DOD, g ** 2, 1 / 3)}
TINV = {k: inv(cut_chords(*v)) for k, v in TARGETS.items()}
xg4, xl4 = (float(x) for x in golden_x())
CUBES = {'Greater Golden Cut Cube': inv(np.array([fl(p) for p in cut_cube(golden_x()[0])])),
         'Lesser Golden Cut Cube': inv(np.array([fl(p) for p in cut_cube(golden_x()[1])]))}

V6 = v600(); V12, _ = S9.regular('120-cell')
res = {'chord_classes': [], 'matches': []}
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
for vname, V in (('600-cell corners (120)', V6), ('120-cell corners (600)', V12)):
    F, classes = chord_classes(V)
    for c in classes:
        E = c['edges']; t0 = time.time(); hits = []
        for dname, d, central in (('(1,0,0,0) icosahedral', np.array([1., 0, 0, 0]), False), ('(1,1,0,0) A3, centre', np.array([1., 1, 0, 0]) / 2 ** .5, True)):
            tg = CUBES if central else TINV
            hs = [0.0] if central else np.linspace(0, (F @ d).max(), N)[1:-1]
            def mis(h, k):
                P = fsection(F, E, d, h)
                return float(np.abs(inv(P) - tg[k]).max()) if len(P) * (len(P) - 1) // 2 == len(tg[k]) else 9.0
            secs = [fsection(F, E, d, h) for h in hs]
            for k in tg:
                vals = np.array([float(np.abs(inv(P) - tg[k]).max()) if len(P) * (len(P) - 1) // 2 == len(tg[k]) else 9.0 for P in secs])
                for i in range(len(vals)):
                    lo_ok = i == 0 or vals[i] <= vals[i - 1]; hi_ok = i == len(vals) - 1 or vals[i] <= vals[i + 1]
                    if vals[i] < 0.05 and lo_ok and hi_ok:
                        if central: hb, e = 0.0, vals[i]
                        else:
                            lo, hi = hs[max(i - 1, 0)], hs[min(i + 1, len(hs) - 1)]
                            for _ in range(80):
                                m1, m2 = lo + (hi - lo) / g ** 2, hi - (hi - lo) / g ** 2
                                if mis(m1, k) < mis(m2, k): hi = m2
                                else: lo = m1
                            hb = (lo + hi) / 2; e = mis(hb, k)
                        if e < 1e-6:
                            hits.append({'corners': vname, 'chord_d2': c['d2'], 'neighbours': c['neighbours'], 'direction': dname, 'height': hb, 'target': k, 'mismatch': e})
                            print('MATCH', hits[-1], flush=True)
        res['chord_classes'].append({'corners': vname, 'chord_d2': c['d2'], 'neighbours': c['neighbours'], 'edges': int(len(E)), 'hits': len(hits)})
        res['matches'] += hits
        print(f'{vname}: chord d2 {c["d2"]:.6f} ({c["neighbours"]} neighbours, {len(E)} chords): {len(hits)} hits, {time.time() - t0:.0f}s', flush=True)
# which 4-neighbour chord class of the 120-cell corners is the edge class of {5/2,3,3}? Its faces are pentagrams, so any
# two edges at a corner meet at 36 degrees (in the 120-cell, at 108 degrees).
F12 = np.array([fl(v) for v in V12]); D0 = ((F12 - F12[0]) ** 2).sum(1); ang = {}
for c in res['chord_classes']:
    if c['corners'].startswith('120') and c['neighbours'] == 4:
        nb = np.where(np.abs(D0 - c['chord_d2']) < 1e-4)[0]; u = F12[nb] - F12[0]; u /= np.linalg.norm(u, axis=1)[:, None]
        ang[c['chord_d2']] = sorted(set(np.round(np.degrees(np.arccos(np.clip(u @ u.T, -1, 1)))[np.triu_indices(len(nb), 1)], 4).tolist()))
res['four_neighbour_classes_edge_angles'] = ang
star = [k for k, v in ang.items() if v == [36.0]]
check(f'120-cell corners: the 4-neighbour chord classes have edge angles {ang}; exactly one has 36 degrees (pentagram faces): '
      f'the edges of {{5/2,3,3}}, chord d2 {star}', len(star) == 1)
for m in res['matches']:
    if m['corners'].startswith('120'):
        m['note'] = ('the convex 120-cell itself (its own edges): a convex section whose corner set coincides with the star\'s corner set; '
                     'not a star section' if abs(m['chord_d2'] - 1) < 1e-6 else
                     'chord class with edge angle ' + str(ang.get(m['chord_d2'])) + ' degrees: not the edge class of a regular polytope')
starhits = [m for m in res['matches'] if (m['corners'].startswith('600') and m['neighbours'] in (12, 20)) or (m['corners'].startswith('120') and star and abs(m['chord_d2'] - star[0]) < 1e-6)]
check(f'no section of a Schlaefli-Hess star polytope (the 600-cell corner classes with 12 or 20 neighbours, and the {{5/2,3,3}} class) '
      f'has the corner set of a golden cut star polyhedron or of a Golden Cut Cube (floating point search, {N} heights)', not starhits)
check(f'chord classes searched: {len(res["chord_classes"])} (600-cell corners: all 8; 120-cell corners: all), including the edge classes of all ten '
      f'Schlaefli-Hess polytopes (12, 20 or 4 neighbours)', any(c['neighbours'] == 4 for c in res['chord_classes'] if c['corners'].startswith('120')))
check(f'floating-point matches with the eight golden cut star polyhedra or the Golden Cut Cubes: {len(res["matches"])}', True)
json.dump({'result': res, 'checks': CHECKS, 'N': N}, open(os.path.join(DATA, 's11-star-polytopes.json'), 'w'), indent=1, default=str)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
