# Self-building ring (Chain of Karma kit), shared geometry (2026-10-12).
# Kit pieces from the 2026-10-11 self-building-kit study (data/ms-kit-j2.json, Lotus frame): icosahedron I, AXE, FUJI, CLEO, J2
# (pentagonal pyramid, all edges 1), Mosseri-Sadoc t1..t6 and Kramer's T2 (all as placed in the Lotus frame), plus J11 and Danzer's
# A, B, C, K. The rings: DICTO's pyramid rule phi*P = P (tip at the apex) + P(1/phi) point-mirrored through the centre of the tip's base
# (its apex then touches the floor) + the side ring R. Here R is built explicitly as a non-convex polyhedron (its convex hull = the
# band, i.e. the frustum of phi*P below the tip, minus the inverted small pyramid).
import os, json, itertools, numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
PHI = (1 + 5 ** .5) / 2
KITFILE = os.path.expanduser('~/kaleidohedra/studies/2026-10-11-self-building-kit/data/ms-kit-j2.json')
if not os.path.exists(KITFILE): KITFILE = os.path.join(HERE, '../data/ms-kit-j2.json')
L = json.load(open(KITFILE))
_all = np.array([v for p in L if p['role'] in ('ico', 'axe', 'fuji', 'cleo') for v in p['vertices']]); O = _all.mean(0)

def rep(role, small=None):
    for p in L:
        if p['role'] != role: continue
        V = np.array(p['vertices']) - O
        if role == 'ico':
            e = min(np.linalg.norm(V[0] - w) for w in V[1:])
            if small is not None and (e < 0.9) != small: continue
        return V
KIT = {'I': rep('ico', small=False), 'AXE': rep('axe'), 'FUJI': rep('fuji'), 'CLEO': rep('cleo'), 'J2': rep('j2')}
for t in ('t1', 't2', 't3', 't4', 't5', 't6', 'T2'): KIT[t] = rep(t)
# J11 = icosahedron minus one J2 cap (gyroelongated pentagonal pyramid)
_I = KIT['I']; _a = _I[0]; _e = min(np.linalg.norm(_a - w) for w in _I[1:])
KIT['J11'] = np.array([w for w in _I if np.linalg.norm(w - _I[np.argmax(np.linalg.norm(_I - _a, axis=1))]) > 1e-9])   # drop the far corner
TAU = PHI
for k, V in {'A': [(0, 0, 0), (TAU**3, 0, TAU**2), (TAU**2, TAU**2, TAU**2), (TAU**2, 1, 0)],
             'B': [(0, 0, 0), (TAU**3, 0, TAU**2), (TAU**2, TAU**2, TAU**2), (TAU**2, TAU, 1)],
             'C': [(0, 0, 0), (-TAU, 0, 1), (TAU**2, TAU**2, TAU**2), (0, TAU**2, 1)],
             'K': [(0, 0, 0), (-1, TAU, 0), (TAU, TAU, TAU), (-0.5, 0.5 / TAU, TAU / 2)]}.items():
    KIT[k] = np.array(V, float) / 2

def planes(V, tol=1e-7):
    out = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < tol for q in out): out.append(e)
    return np.array(out)

def convex_edges(V, tol=1e-7):
    """Edges of a convex polytope: list of (i, j, length, dihedral in degrees)."""
    E = planes(V); out = []
    on = [set(np.where(np.abs(V @ e[:3] + e[3]) < tol)[0]) for e in E]
    for a, b in itertools.combinations(range(len(E)), 2):
        s = sorted(on[a] & on[b])
        if len(s) >= 2:
            # the edge = the two extreme points of s along the line
            d = np.cross(E[a][:3], E[b][:3]); pr = V[s] @ d; i, j = s[int(np.argmin(pr))], s[int(np.argmax(pr))]
            out.append((i, j, float(np.linalg.norm(V[i] - V[j])), float(np.degrees(np.pi - np.arccos(np.clip(E[a][:3] @ E[b][:3], -1, 1))))))
    return out

def pyramid_parts(V):
    """apex and base corners of a pyramid given as corners (the corner off the largest face plane)."""
    E = planes(V); best = None
    for e in E:
        on = np.where(np.abs(V @ e[:3] + e[3]) < 1e-7)[0]
        if len(on) == len(V) - 1 and (best is None or len(on) > len(best[1])): best = (e, on)
    e, on = best; apex = [i for i in range(len(V)) if i not in on][0]
    return V[apex], V[on]

def ring(name):
    """DICTO's ring for pyramid `name`: returns dict with band corners, hole corners, and the ring's faces as polygons."""
    apex, base = pyramid_parts(KIT[name])
    big = apex + PHI * (base - apex)                       # phi*P base (the floor), apex shared with the tip
    c1 = base.mean(0)
    hole_apex = c1 - (apex - c1) / PHI                     # point mirror of the small pyramid through c1
    hole_base = c1 - (base - c1) / PHI
    band = np.vstack([big, base])
    return dict(apex=apex, top=base, floor=big, c1=c1, hole_apex=hole_apex, hole_base=hole_base, band=band,
                hole=np.vstack([hole_base, hole_apex[None]]))

def vol(V): return ConvexHull(V).volume
