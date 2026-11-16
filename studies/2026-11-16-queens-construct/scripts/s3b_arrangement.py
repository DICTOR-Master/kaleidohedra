#!/usr/bin/env python3
"""Part 3b: the pieces cut from the 600-cell by the facet hyperplanes of A and B (and, with option 'all', also of -A, -B, C3 hull).
Regions found by splitting with linear programs (floats), then every region is rebuilt exactly in Q(sqrt5) (one per S5 orbit;
S5 permutes the planes) and the volumes are summed: sum over orbits (orbit size x region volume) must equal the 600-cell exactly.
Also: the common core of the five hulls named exactly. Usage: s3b_arrangement.py out.json [AB|all]"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
OUT = sys.argv[1]; MODE = sys.argv[2] if len(sys.argv) > 2 else 'AB'; C = Checks(); t0 = time.time(); out = {'mode': MODE}
P5, X, Y = build_600(); n = len(P5); Pk = {vkey(p): i for i, p in enumerate(P5)}
P4 = [to4(p) for p in P5]; PP = Poly(P4); V = PP.volume()
perms = list(itertools.permutations(range(5)))
def orbit_of(p): return uniq([tuple(p[s] for s in sg) for sg in perms])
def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
hullsets = {'A': X, 'B': Y, '-A': [vneg(x) for x in X], '-B': [vneg(y) for y in Y]}
c3 = [p for p in P5 if vkey(p) not in {vkey(q) for S in hullsets.values() for q in S}]; hullsets['C3'] = c3
use = ['A', 'B'] if MODE == 'AB' else ['A', 'B', '-A', '-B', 'C3']
planes = []
for h in use:
    for on, nn, d in Poly([to4(p) for p in hullsets[h]]).facets: planes.append((h, nn, d))
C(len(planes) == {'AB': 30, 'all': 90}[MODE], f'{len(planes)} facet hyperplanes')
Phs = PP.halfspaces()
A0 = np.array([flt(nn) for nn, d in Phs]); b0 = np.array([float(d) for nn, d in Phs])
Np = np.array([flt(nn) for h, nn, d in planes]); dp = np.array([float(d) for h, nn, d in planes])
def lp_ext(extra, c):
    A = A0; b = b0
    if extra:
        A = np.vstack([A0] + [s*Np[j][None, :] for j, s in extra]); b = np.concatenate([b0, [s*dp[j] for j, s in extra]])
    r1 = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)]*4, method='highs'); r2 = linprog(-c, A_ub=A, b_ub=b, bounds=[(None, None)]*4, method='highs')
    return r1.fun, -r2.fun
def fverts(R):
    """float corners of region R (P plus extra constraints), via a Chebyshev centre; None if no interior"""
    A = np.vstack([A0] + [s*Np[j][None, :] for j, s in R]) if R else A0; b = np.concatenate([b0, [s*dp[j] for j, s in R]]) if R else b0
    nr = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, 0, -1], A_ub=np.hstack([A, nr[:, None]]), b_ub=b, bounds=[(None, None)]*4 + [(0, 10)], method='highs')
    if r.status != 0 or r.x[4] < 1e-8: return None
    return HalfspaceIntersection(np.hstack([A, -b[:, None]]), r.x[:4]).intersections
regions = [([], fverts([]))]
for j in range(len(planes)):
    new = []
    for R, Vt in regions:
        val = Vt @ Np[j] - dp[j]
        if val.min() < -1e-7 and val.max() > 1e-7:
            for sgn in (1, -1):
                R2_ = R + [(j, sgn)]; V2 = fverts(R2_)
                if V2 is not None: new.append((R2_, V2))
        else: new.append((R, Vt))
    regions = new
    print(f'PROGRESS {(j + 1)/len(planes):.3f} plane {j + 1}: {len(regions)} regions ({time.time() - t0:.0f} s)', flush=True)
regions = [R for R, Vt in regions]
out['regions'] = len(regions)
# full sign vectors from a Chebyshev centre
def centre(R):
    A = np.vstack([A0] + [s*Np[j][None, :] for j, s in R]) if R else A0; b = np.concatenate([b0, [s*dp[j] for j, s in R]]) if R else b0
    nr = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, 0, -1], A_ub=np.hstack([A, nr[:, None]]), b_ub=b, bounds=[(None, None)]*4 + [(0, 10)], method='highs')
    return r.x[:4], r.x[4]
sv = []
for R in regions:
    c, rad = centre(R); assert rad > 1e-8
    sv.append(tuple(1 if Np[j] @ c < dp[j] else -1 for j in range(len(planes))))
C(len(set(sv)) == len(regions), 'regions have distinct sign vectors')
# S5 action on planes
def pkey(nn, d):
    i = next(k for k in range(4) if not nn[k].iszero()); c = nn[i] if nn[i].sign() > 0 else -nn[i]; c = c.inv()
    return vkey(vscale(c, nn)) + (( d*c).key(),)
PKEY = {pkey(nn, d): k for k, (h, nn, d) in enumerate(planes)}
C(len(PKEY) == len(planes), 'the facet hyperplanes are distinct (oriented)')
def perm_plane(sg, j):
    h, nn, d = planes[j]
    m = tuple(list(nn) + [Q5(0)]); mp_ = [None]*5
    for i in range(5): mp_[sg[i]] = m[i]
    n2 = tuple(mp_[i] - mp_[4] for i in range(4))
    return PKEY[pkey(n2, d)]
pmap = [[perm_plane(sg, j) for j in range(len(planes))] for sg in perms]
svset = set(sv); reps = {}
for v in sv:
    imgs = {tuple(v[pm.index(k)] for k in range(len(planes))) for pm in pmap}
    can = min(imgs)
    if can not in reps: reps[can] = (v, len(imgs))
C(all(set(tuple(v[pm.index(k)] for k in range(len(planes))) for pm in pmap) <= svset for v in sv[:50]), 'S5 maps regions to regions (first 50 checked)')
out['region_orbits'] = len(reps)
tot = Q5(); classes = []
for can, (v, size) in reps.items():
    hs = Phs + [((nn if s == 1 else vneg(nn)), (d if s == 1 else -d)) for (h, nn, d), s in zip(planes, v)]
    Q = hs_intersect(hs); vol = Q.volume(); tot = tot + vol*size
    print(f'PROGRESS {len(classes)/len(reps):.3f} exact class {len(classes) + 1} of {len(reps)} ({time.time() - t0:.0f} s)', flush=True)
    corners_P = sum(1 for q in Q.P if vkey(to5(q)) in Pk)
    inside = [h for h in use if all(s == 1 for (hh, nn, d), s in zip(planes, v) if hh == h)]
    classes.append({'orbit_size': size, 'fvec': Q.fvec, 'cells': cell_census(Q), 'fraction': str(vol/V), 'fraction_float': float(vol/V),
                    'corners_of_P': corners_P, 'inside_hulls': inside})
classes.sort(key=lambda c: -c['fraction_float'])
out['classes'] = classes
C(tot == V, f'regions (orbit size x volume) sum exactly to the 600-cell ({len(regions)} regions, {len(reps)} S5 classes)')
C(sum(c['orbit_size'] for c in classes) == len(regions), 'orbit sizes add up to the region count')
for c in classes[:40]: print('CLASS', json.dumps(c), flush=True)
if MODE == 'AB':
    # core of all five hulls, named
    hs = sum((Poly([to4(p) for p in hullsets[h]]).halfspaces() for h in ['A', 'B', '-A', '-B', 'C3']), [])
    core = hs_intersect(hs); e2 = sorted({sqd(to5(core.P[a]), to5(core.P[b])).key() for a, b in (tuple(e) for e in core.edges)})
    cp = [to5(q) for q in core.P]; xs, blocks, gaps = orbit_pattern(cp[0])
    out['core'] = {'fvec': core.fvec, 'cells': cell_census(core), 'edge_lengths2': [str(Q5(*k)) for k in e2], 'blocks': blocks,
                   'gaps': [str(g) for g in gaps], 'A4_type': A4NAME.get(tuple(blocks)), 'one_S5_orbit': len(uniq(orbit_of(cp[0]))) == len(cp),
                   'coords_shifted': [str(x - xs[-1]) for x in xs], 'fraction': str(core.volume()/V)}
    print('CORE', out['core'], flush=True)
    C(out['core']['A4_type'] == 'bitruncated 5-cell' and len(e2) == 1, 'core of the five hulls = a uniform bitruncated 5-cell (one edge length)')
    # A cap B, named
    AB_ = hs_intersect(Poly([to4(p) for p in X]).halfspaces() + Poly([to4(p) for p in Y]).halfspaces())
    ap = [to5(q) for q in AB_.P]; xs, blocks, gaps = orbit_pattern(ap[0])
    e2 = sorted({sqd(to5(AB_.P[a]), to5(AB_.P[b])).key() for a, b in (tuple(e) for e in AB_.edges)})
    out['A_cap_B'] = {'fvec': AB_.fvec, 'cells': cell_census(AB_), 'blocks': blocks, 'A4_type': A4NAME.get(tuple(blocks)),
                      'one_S5_orbit': len(uniq(orbit_of(ap[0]))) == len(ap), 'edge_lengths2': [str(Q5(*k)) for k in e2],
                      'coords_shifted': [str(x - xs[-1]) for x in xs], 'gaps': [str(g) for g in gaps], 'fraction': str(AB_.volume()/V)}
    print('A_CAP_B', out['A_cap_B'], flush=True)
    C(out['A_cap_B']['one_S5_orbit'], 'A cap B is the hull of one S5 orbit')
out['seconds'] = time.time() - t0
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final()
