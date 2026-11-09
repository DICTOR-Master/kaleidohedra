"""DICTO Golayantra: the spherical DICTO Yantra (GF1, Cleo-Antonius) as a gola-yantra of rings.

Gnomonic projection from the sphere's centre: the yantra (diameter-1 frame, depth d below the top point) sits on the
plane z = 1, its circle of radius 1/2 mapped to a cap of angular radius RHO about the pole Z = (0,0,1):
   (x, d) -> (x*sc, (1/2 - d)*sc, 1) / norm,   sc = 2 tan(RHO).
Every side line -> a great circle (ring) with unit normal n = P x Q.  Two rings meet in an antipodal pair of points.
A point where three or more rings meet <-> three or more lines concurrent in the projective plane (points at infinity
included: they land on the horizon ring z = 0).  Since the map is (scaling) o (gnomonic), the ring count and all
incidences are independent of RHO; the crossing angles are not.

Part 3 (DICTO proposed the polar reciprocal form): pole of ring i = +-n_i; rings concurrent at v <-> poles on the
great circle with pole v.  Checked directly by det(n_i, n_j, n_k) over all triples.

GF1 is recomputed here at 110 digits (findroot from the stored 40-digit values, same equations as golden_family.py),
so 'exact' below means |residual| < 1e-80 while every non-incidence is > 1e-6.
Outputs: ../data/rings.json, ../data/joints.csv, ../data/build_spec.csv, ../data/polar.json
"""
import json, itertools, csv, os, sys, math
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import solve, all_conditions, order_ok, MARMAS, CORNERS, APEX_ON_BASE
mp.mp.dps = 110
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
TOL = mp.mpf(10) ** -80
phi = (1 + mp.sqrt(5)) / 2

# ---------- GF1 at high precision ----------
G = json.load(open(os.path.join(DATA, 'golden_family.json')))['GF1']
p = 2 / phi ** 3
def yan(u, Q, S):
    v = p / u; P = v ** 2 / (1 + v ** 2); R = 1 / (1 + u ** 2)
    return solve(P, Q, R, S, v / (1 + v ** 2), u / (1 + u ** 2), mp.sqrt, root=1)
def inc(t, Q):
    b, w = t['b'], t['w']; m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw ** 2 + h ** 2))
    return b[5] + (r if Q > b[5] else -r)
def F(u, Q, S):
    t = yan(u, Q, S); b, w = t['b'], t['w']
    return [w[1] ** 2 + b[1] ** 2 - b[1], w[9] ** 2 + b[9] ** 2 - b[9], inc(t, Q) - mp.mpf(1) / 2]
u, Q, S = mp.findroot(F, (mp.mpf(G['u']), mp.mpf(G['b']['6']['a']), mp.mpf(G['b']['9']['a'])), tol=mp.mpf(10) ** -100)
T = yan(u, Q, S)
b, w = T['b'], T['w']
a = {3: mp.mpf(1), 7: mp.mpf(0), 8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9]}
T['a'] = a
res = max(abs(e) for _, e in all_conditions(T))
agree = max(abs(b[i] - mp.mpf(G['b'][str(i)]['a'])) for i in range(1, 10))
print(f'GF1 at 110 digits: u = {mp.nstr(u, 30)}, max condition residual {mp.nstr(res, 3)}, agrees with stored 40-digit data to {mp.nstr(agree, 3)}', flush=True)
assert res < TOL and agree < mp.mpf(10) ** -35 and order_ok(T, mp.mpf(10) ** -90)
UP = [i for i in range(1, 10) if a[i] < b[i]]   # apex above base (t6..t9)

def cross(p_, q_): return [p_[1] * q_[2] - p_[2] * q_[1], p_[2] * q_[0] - p_[0] * q_[2], p_[0] * q_[1] - p_[1] * q_[0]]
def dot(p_, q_): return sum(x * y for x, y in zip(p_, q_))
def unit(p_): n = mp.sqrt(dot(p_, p_)); return [x / n for x in p_]
def det(A, B, C): return dot(A, cross(B, C))

# rings: name -> (point1, point2) in yantra coords (x, d)
RINGS = {}
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (mp.mpf(0), a[i])
    RINGS[f'B{i}'] = (L, R); RINGS[f'R{i}'] = (R, A); RINGS[f'L{i}'] = (L, A)
NAMES = list(RINGS)

def geometry(RHO):
    sc = 2 * mp.tan(RHO)
    P3 = lambda q: [q[0] * sc, (mp.mpf(1) / 2 - q[1]) * sc, mp.mpf(1)]
    N = {k: unit(cross(P3(s[0]), P3(s[1]))) for k, s in RINGS.items()}
    return sc, P3, N

def canon(v):
    """sign-normalise an antipodal pair: z > 0, else x > 0, else y > 0"""
    for c in (2, 0, 1):
        if abs(v[c]) > mp.mpf(10) ** -60: return v if v[c] > 0 else [-x for x in v]
    return v

def joints(N):
    pts = []   # list of (canon unit vector, frozenset of rings)
    for i, j in itertools.combinations(NAMES, 2):
        c = cross(N[i], N[j]); nc = mp.sqrt(dot(c, c))
        assert nc > mp.mpf(10) ** -6, f'rings {i},{j} coincide'
        v = canon(unit(c))
        on = frozenset(k for k in NAMES if abs(dot(N[k], v)) < TOL)
        if not any(on == s for _, s in pts): pts.append((v, on))
    return pts

def classify(S):
    for (p_, q_, r_) in MARMAS:
        for side in 'RL':
            if S == frozenset({f'{side}{p_}', f'B{q_}', f'{side}{r_}'}): return f'marma ({p_},{q_},{r_}) {side}'
    for (p_, q_, r_) in CORNERS:
        for side in 'RL':
            if S == frozenset({f'{side}{p_}', f'B{q_}', f'{side}{r_}'}): return f'corner touch ({p_},{q_},{r_}) {side}'
    for (p_, q_) in APEX_ON_BASE:
        if S == frozenset({f'R{p_}', f'L{p_}', f'B{q_}'}): return f'apex t{p_} on base t{q_}'
    if S == frozenset(f'B{i}' for i in range(1, 10)): return 'base pole (all nine bases)'
    return 'HIDDEN'

def deg(x): return x * 180 / mp.pi

out = {'GF1_u_110': mp.nstr(u, 60), 'condition_residual': mp.nstr(res, 3), 'rings': NAMES, 'by_rho': {}}
# exact Cleo cap: angle from icosahedron face centre to edge midpoint
I = [[mp.mpf(0), mp.mpf(1), phi], [mp.mpf(0), mp.mpf(-1), phi], [phi, mp.mpf(0), mp.mpf(1)]]   # one face (0,1,phi),(0,-1,phi),(phi,0,1)
cen = unit([sum(c) for c in zip(*I)]); mid = unit([(x + y) / 2 for x, y in zip(I[0], I[1])])
RHO_CLEO = mp.acos(dot(cen, mid))
print(f'Cleo cap rho = {mp.nstr(deg(RHO_CLEO), 20)} deg; tan(rho) = {mp.nstr(mp.tan(RHO_CLEO), 20)} (= 1/(sqrt3 phi^2)? {mp.nstr(1 / (mp.sqrt(3) * phi ** 2), 20)})', flush=True)
RHOS = {'60': mp.pi / 3, 'cleo': RHO_CLEO}
for r in (10, 30, 45, 75, 85): RHOS[str(r)] = mp.radians(r)

counts = {}
summary_sets = None
near_global = []
for key, RHO in RHOS.items():
    sc, P3, N = geometry(RHO)
    pts = joints(N)
    multi = [(v, S) for v, S in pts if len(S) >= 3]
    sets = sorted((sorted(S), classify(S)) for v, S in multi)
    if summary_sets is None: summary_sets = sets
    same = sets == summary_sets
    counts[key] = dict(rings=len(N), points_pairs=len(pts), multi=len(multi), same_incidences=same)
    print(f'rho {key}: {len(N)} distinct great circles; {len(pts)} antipodal intersection pairs; {len(multi)} with >= 3 rings; incidences identical to rho=60: {same}', flush=True)
    if key in ('60', 'cleo'):
        # nearest non-incidences (near misses): third ring close to a pair point
        near = []
        for v, S in pts:
            for k in NAMES:
                if k in S: continue
                dd = deg(mp.asin(abs(dot(N[k], v))))
                near.append((dd, k, sorted(S)))
        near.sort(key=lambda t: t[0])
        minmiss = near[0][0]
        rec = {'sc': mp.nstr(sc, 30), 'joints': [], 'near_misses': [(mp.nstr(d_, 8), k, S) for d_, k, S in near[:12]], 'min_miss_deg': mp.nstr(minmiss, 10)}
        for v, S in sorted(multi, key=lambda t: classify(t[1])):
            ang = {f'{i}/{j}': mp.nstr(deg(mp.acos(abs(dot(N[i], N[j])))), 12) for i, j in itertools.combinations(sorted(S), 2)}
            rec['joints'].append({'type': classify(S), 'rings': sorted(S), 'xyz': [mp.nstr(c, 20) for c in v], 'angles_deg': ang,
                                  'on_cap_side': bool(v[2] > 0), 'inside_cap': bool(mp.acos(v[2]) <= RHO + mp.mpf(10) ** -30)})
        rec['normals'] = {k: [mp.nstr(c, 25) for c in N[k]] for k in NAMES}
        # base longitudes: base Bi is the meridian through +-X at angle lambda_i from Z
        rec['base_longitude_deg'] = {f'B{i}': mp.nstr(deg(mp.atan(sc * (mp.mpf(1) / 2 - b[i]))), 15) for i in range(1, 10)}
        rec['leg_inclination_to_equator_deg'] = {k: mp.nstr(deg(mp.acos(abs(N[k][0]))), 15) for k in NAMES if k[0] in 'RL'}
        out['by_rho'][key] = rec
        print(f'  nearest miss: {mp.nstr(minmiss, 6)} deg ({near[0][1]} near {near[0][2]})', flush=True)
out['counts'] = counts
hidden = [s for s in summary_sets if s[1] == 'HIDDEN']
types = {}
for s in summary_sets: types[s[1].split(' (')[0].split(' t')[0]] = types.get(s[1].split(' (')[0].split(' t')[0], 0) + 1
print('multi-ring points (antipodal pairs) by type:', types, flush=True)
print('hidden multi-ring points:', hidden, flush=True)
out['types'] = types; out['hidden'] = hidden

# ---------- the frame rings: equator (symmetry ring x = 0), horizon (z = 0), the yantra circle ----------
sc, P3, N = geometry(RHOS['60'])
X = [mp.mpf(1), 0, 0]
eq_ok = all(abs(dot(N[f'B{i}'], X)) < TOL for i in range(1, 10))               # bases pass through +-X
apex_on_eq = all(abs(unit(P3((0, a[i])))[0]) < TOL for i in range(1, 10))       # apexes on x = 0
horizon_in_pencil = True   # z = 0 contains X: the line at infinity belongs to the pencil of parallel bases
print('all bases through +-X:', eq_ok, '; every apex on the equator ring x = 0:', apex_on_eq, flush=True)

# ---------- Part 3: polar reciprocal ----------
pol = {}
for key in ('60', 'cleo'):
    sc, P3, N = geometry(RHOS[key])
    coll = []
    for i, j, k in itertools.combinations(NAMES, 3):
        if abs(det(N[i], N[j], N[k])) < TOL: coll.append(frozenset({i, j, k}))
    # expected: every 3-subset of every multi-ring set
    exp = set()
    for S, _ in summary_sets:
        for t in itertools.combinations(S, 3): exp.add(frozenset(t))
    match = set(coll) == exp
    marma_ok = all(frozenset({f'{s}{p_}', f'B{q_}', f'{s}{r_}'}) in set(coll) for (p_, q_, r_) in MARMAS for s in 'RL')
    mindet = min(abs(det(N[i], N[j], N[k])) for i, j, k in itertools.combinations(NAMES, 3) if frozenset({i, j, k}) not in exp)
    # base poles on the equator great circle x = 0 (polar of X)
    bpe = all(abs(N[f'B{i}'][0]) < TOL for i in range(1, 10))
    # polar triangles
    tris = []; VERTS = []
    for i in range(1, 10):
        Lv, Rv, Av = [unit(P3(q)) for q in (RINGS[f'B{i}'][0], RINGS[f'B{i}'][1], (0, a[i]))]
        VERTS.append((Av, Lv, Rv))
        def side_pole(n, opp): return n if dot(n, opp) > 0 else [-x for x in n]
        Ap, Lp, Rp = side_pole(N[f'B{i}'], Av), side_pole(N[f'R{i}'], Lv), side_pole(N[f'L{i}'], Rv)
        def ang(V, P_, Q_):   # angle at V of spherical triangle V P Q
            t1 = unit([p - dot(P_, V) * v for p, v in zip(P_, V)]); t2 = unit([q - dot(Q_, V) * v for q, v in zip(Q_, V)])
            return mp.acos(dot(t1, t2))
        orig_ang = {'A': ang(Av, Lv, Rv), 'L': ang(Lv, Av, Rv), 'R': ang(Rv, Av, Lv)}
        orig_side = {'A': mp.acos(dot(Lv, Rv)), 'L': mp.acos(dot(Av, Rv)), 'R': mp.acos(dot(Av, Lv))}
        pol_side = {'A': mp.acos(dot(Lp, Rp)), 'L': mp.acos(dot(Ap, Rp)), 'R': mp.acos(dot(Ap, Lp))}
        pol_ang = {'A': ang(Ap, Lp, Rp), 'L': ang(Lp, Ap, Rp), 'R': ang(Rp, Ap, Lp)}
        ok = all(abs(pol_side[k] - (mp.pi - orig_ang[k])) < TOL and abs(pol_ang[k] - (mp.pi - orig_side[k])) < TOL for k in 'ALR')
        area_o = sum(orig_ang.values()) - mp.pi; area_p = sum(pol_ang.values()) - mp.pi
        # polar triangle contains the cap of radius 90 - rho about Z  (dual of 'triangle inside the cap of radius rho')
        # the sides of the polar triangle are the polars of the original vertices: distance Z -> side = 90 - angle(Z, vertex)
        dist_side = [90 - deg(mp.acos(V[2])) for V in (Av, Lv, Rv)]
        tris.append({'t': i, 'up': i in UP, 'ok_180_minus': ok,
                     'orig_angles_deg': {k: mp.nstr(deg(v), 12) for k, v in orig_ang.items()},
                     'orig_sides_deg': {k: mp.nstr(deg(v), 12) for k, v in orig_side.items()},
                     'polar_sides_deg': {k: mp.nstr(deg(v), 12) for k, v in pol_side.items()},
                     'polar_angles_deg': {k: mp.nstr(deg(v), 12) for k, v in pol_ang.items()},
                     'area_orig_sr': mp.nstr(area_o, 12), 'area_polar_sr': mp.nstr(area_p, 12),
                     'polar_vertices': {k: [mp.nstr(c, 15) for c in v] for k, v in (('A', Ap), ('L', Lp), ('R', Rp))},
                     'Z_to_polar_sides_min_deg': mp.nstr(min(dist_side), 15)})
    tri_ok = all(t['ok_180_minus'] for t in tris)
    core = mp.nstr(90 - deg(RHOS[key]), 12)
    tangent = [t['t'] for t in tris if abs(mp.mpf(t['Z_to_polar_sides_min_deg']) - (90 - deg(RHOS[key]))) < mp.mpf(10) ** -10]
    for t, (Av_, Lv_, Rv_) in zip(tris, VERTS):
        t['sides_tangent_to_core'] = [k for k, V in (('A', Av_), ('L', Lv_), ('R', Rv_)) if abs(mp.acos(V[2]) - RHOS[key]) < mp.mpf(10) ** -60]
    contains = all(mp.mpf(t['Z_to_polar_sides_min_deg']) >= 90 - deg(RHOS[key]) - mp.mpf(10) ** -10 for t in tris)
    pol[key] = {'collinear_pole_triples': len(coll), 'equals_dual_of_joints': match, 'all_36_marma_alignments': marma_ok,
                'min_noncollinear_det': mp.nstr(mindet, 6), 'base_poles_on_x0_great_circle': bpe, 'polar_triangles': tris,
                'polar_triangle_rule_ok': tri_ok, 'core_cap_radius_deg': core, 'all_contain_core_cap': contains,
                'polar_triangles_tangent_to_core': tangent,
                'poles': {k: [mp.nstr(c, 20) for c in N[k]] for k in NAMES}}
    print(f'polar rho {key}: {len(coll)} collinear pole triples; = dual of joint list: {match}; 36 marma alignments: {marma_ok}; '
          f'min other |det| {mp.nstr(mindet, 4)}; base poles on x=0: {bpe}; polar triangles sides = 180 - angles: {tri_ok}; '
          f'all contain cap {core} deg about Z: {contains}; tangent to it: {tangent}', flush=True)
out['polar'] = pol

# ---------- Cleo sphere: do rings of different caps coincide? ----------
sc, P3, N0 = geometry(RHO_CLEO)
Iv = [unit(list(pp)) for c in [(0, 1, phi), (1, phi, 0), (phi, 0, 1)] for pp in itertools.product(*[(x, -x) if x else (0,) for x in c])]
E = min(mp.sqrt(dot([x - y for x, y in zip(Iv[i], Iv[j])], [x - y for x, y in zip(Iv[i], Iv[j])])) for i, j in itertools.combinations(range(12), 2))
faces = [t for t in itertools.combinations(range(12), 3) if all(abs(mp.sqrt(dot([x - y for x, y in zip(Iv[i], Iv[j])], [x - y for x, y in zip(Iv[i], Iv[j])])) - E) < mp.mpf(10) ** -40 for i, j in itertools.combinations(t, 2))]
allN = []
for t in faces:
    c = unit([sum(z) for z in zip(*[Iv[k] for k in t])]); up = [x - dot(Iv[t[0]], c) * y for x, y in zip(Iv[t[0]], c)]; up = unit(up); rt = cross(up, c)
    def Pf(q): return [c[m] + q[0] * sc * rt[m] + (mp.mpf(1) / 2 - q[1]) * sc * up[m] for m in range(3)]
    for k, s in RINGS.items(): allN.append(unit(cross(Pf(s[0]), Pf(s[1]))))
dup = 0; parent = list(range(len(allN))); kinds = {}
def fnd(i):
    while parent[i] != i: i = parent[i]
    return i
for i, j in itertools.combinations(range(len(allN)), 2):
    c = cross(allN[i], allN[j])
    if mp.sqrt(dot(c, c)) < mp.mpf(10) ** -40:
        dup += 1; parent[fnd(i)] = fnd(j); kk = tuple(sorted((NAMES[i % 27], NAMES[j % 27]))); kinds[kk] = kinds.get(kk, 0) + 1
cleo_rings = len({fnd(i) for i in range(len(allN))})
print('coincident ring kinds (cap A ring, cap B ring): count', sorted(kinds.items()), flush=True)
mult = {}
for i in range(len(allN)): mult[fnd(i)] = mult.get(fnd(i), 0) + 1
print('multiplicity histogram:', sorted({m: list(mult.values()).count(m) for m in set(mult.values())}.items()), flush=True)
print(f'Cleo sphere: {len(faces)} caps x 27 = {len(allN)} rings, coincident pairs {dup}, distinct rings {cleo_rings}', flush=True)
out['cleo_sphere'] = {'caps': len(faces), 'rings_total': len(allN), 'coincident_pairs': dup, 'distinct': cleo_rings, 'kinds': {f'{x}={y}': c for (x, y), c in kinds.items()}}

# ---------- build spec (rho = 60 deg, sphere diameter 60 cm) ----------
RAD = 30.0
sc, P3, N = geometry(RHOS['60'])
rec = out['by_rho']['60']
def ring_frame(k):
    """zero mark: the ring's crossing with the equator ring x = 0 on the cap side (z > 0); bases: their point on x = 0;
    legs: the apex.  Degrees increase towards +x (the right half of the yantra)."""
    n = N[k]
    e0 = unit(cross(X, n)) if abs(dot(n, X)) < 1 - mp.mpf(10) ** -30 else None
    if e0[2] < 0: e0 = [-x for x in e0]
    e1 = cross(n, e0)
    if (e1[0] < 0) != (k[0] == 'L'): e1 = [-x for x in e1]   # right legs and bases count towards +x, left legs towards -x (mirror)
    return e0, e1
def ring_deg(k, v):
    e0, e1 = ring_frame(k); return float(deg(mp.atan2(dot(v, e1), dot(v, e0)))) % 360
def sd(x): return x - 360 if x > 180 else x   # signed degrees
rows = []
for k in NAMES:
    s = RINGS[k]; d1, d2 = ring_deg(k, unit(P3(s[0]))), ring_deg(k, unit(P3(s[1])))
    marks = []
    for J in rec['joints']:
        if k in J['rings']:
            v = [mp.mpf(c) for c in J['xyz']]
            for sgn in (1, -1):
                vv = [sgn * c for c in v]; marks.append((round(ring_deg(k, vv), 3) % 360, J['type'] + ('' if sgn == 1 else ' (antipode)')))
    marks.sort()
    rows.append({'ring': k, 'kind': 'base (meridian through the poles +-X)' if k[0] == 'B' else ('right leg' if k[0] == 'R' else 'left leg'),
                 'radius_cm': RAD, 'yantra_arc_from_deg': round(min(sd(d1), sd(d2)), 3), 'yantra_arc_to_deg': round(max(sd(d1), sd(d2)), 3),
                 'yantra_arc_cm': round(RAD * math.radians(max(sd(d1), sd(d2)) - min(sd(d1), sd(d2))), 2),
                 'joints': '; '.join(f'{m:.3f} {t}' for m, t in marks)})
with open(os.path.join(DATA, 'build_spec.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
with open(os.path.join(DATA, 'joints.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(['rho', 'type', 'rings', 'x', 'y', 'z', 'inside_cap', 'crossing_angles_deg'])
    for key in ('60', 'cleo'):
        for J in out['by_rho'][key]['joints']:
            wr.writerow([key, J['type'], ' '.join(J['rings'])] + [mp.nstr(mp.mpf(c), 12) for c in J['xyz']] + [J['inside_cap'], '; '.join(f'{p_} {v}' for p_, v in J['angles_deg'].items())])
# every crossing on every ring (full-ring build): degree mark on each ring, partner rings, crossing angle
with open(os.path.join(DATA, 'crossings_rho60.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(['ring', 'mark_deg', 'other_rings_at_this_point', 'n_rings', 'angle_to_each_deg', 'inside_yantra_cap'])
    for k in NAMES:
        seen = []
        for j in NAMES:
            if j == k: continue
            v = unit(cross(N[k], N[j]))
            for sgn in (1, -1):
                vv = [sgn * c for c in v]; m = round(ring_deg(k, vv), 3) % 360
                if any(abs(m - x) < 1e-6 or abs(abs(m - x) - 360) < 1e-6 for x in seen): continue
                seen.append(m)
                others = [o for o in NAMES if o != k and abs(dot(N[o], vv)) < TOL]
                wr.writerow([k, f'{m:.3f}', ' '.join(others), len(others) + 1,
                             ' '.join(f'{o}:{float(deg(mp.acos(abs(dot(N[k], N[o]))))):.3f}' for o in others), bool(mp.acos(vv[2]) <= RHOS['60'])])
json.dump(out, open(os.path.join(DATA, 'rings.json'), 'w'), indent=1, default=str)

ok = (all(c['rings'] == 27 and c['same_incidences'] for c in counts.values()) and eq_ok and apex_on_eq
      and all(pol[k]['equals_dual_of_joints'] and pol[k]['all_36_marma_alignments'] and pol[k]['polar_triangle_rule_ok'] and pol[k]['all_contain_core_cap'] for k in pol))
print('FINAL ok' if ok else 'FINAL FAIL: see lines above')
