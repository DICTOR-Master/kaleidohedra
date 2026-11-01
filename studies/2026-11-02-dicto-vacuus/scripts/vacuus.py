# The DICTO Vacuus of one solid (DICTO 2026-11-02): centre O (the corner centroid); the centre pyramids (one per face, apex O) fill the
# solid; the Vacuus is the set of interface sheets between neighbouring pyramids, i.e. for every edge AB the flat triangle O-A-B, the fin.
# Computed per solid:
#  - well defined: O strictly on the inner side of every face plane (then the pyramids fill the solid without overlap: every ray from O
#    crosses the surface once); faces where this fails are counted and the Vacuus is flagged;
#  - fins: squared sides |OA|^2, |OB|^2, |AB|^2, apex angle AOB, right angles (at O, A or B), congruence classes (exact), symmetry
#    orbits (orthogonal maps of the corner set, 1e-7); apex angles tested exactly for rational multiples of pi (cos 2 theta in the field:
#    possible only for denominators 1-6, 8, 10, 12);
#  - wedges: the dihedral angle between the two neighbouring fins that meet along a corner ray Ov inside one face pyramid (= the angle of
#    the face's central projection at v). The same wedges, grouped around a corner ray, sum to 2 pi; grouped around a face pyramid they
#    sum to (n - 2) pi + the pyramid's solid angle; both sums are checked;
#  - the edge dihedral angle of the solid at each edge (for the dual comparison in collect.py).
# Exact in Q, Q(sqrt2), Q(sqrt3), Q(sqrt5) (vertex strings of DICTO Solids v7 / classical.py); other fields float64 (flagged).
# Usage: vacuus.py <solid json> <out json>
import sys, os, json, math, itertools, collections, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qf
from qf import QF, vsub, dot, cross, rational_pi, rational_pi_float
SRC, OUTF = sys.argv[1:3]
d = json.load(open(SRC)); F = [list(f) for f in d['faces']]
dq = qf.field(d.get('field', ''))
exact = dq is not None and d['vertices'][0].get('exact') is not None
if exact: V = [[qf.parse(x) for x in v['exact']] for v in d['vertices']]
else: V = [[float(x) for x in v['decimal']] for v in d['vertices']]
n = len(V); Z = (lambda: QF(0)) if exact else (lambda: 0.0)
c = [sum((p[i] for p in V), Z()) / n for i in range(3)]; V = [vsub(p, c) for p in V]      # centre O = corner centroid, at the origin
VF = np.array([[float(x) for x in p] for p in V]); SC = float(np.abs(VF).max())
def sg(x):
    if exact: return x.sign()
    return 0 if abs(x) < 1e-10 * SC * SC * SC else (1 if x > 0 else -1)
def key(x): return (x.a, x.b) if exact else round(x / R2, 9)
def ex(x): return str(x) if exact else None
# global orientation (signed volume) -> faces ccw seen from outside
vol = sum(float(qf.det3(V[f[0]], V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1))
if vol < 0: F = [f[::-1] for f in F]
R2 = max(float(dot(p, p)) for p in V)
# faces: Newell normal, O inside the plane?
NF = []; bad = []
for i, f in enumerate(F):
    N = [Z(), Z(), Z()]
    for k in range(len(f)): N = [x + y for x, y in zip(N, cross(V[f[k]], V[f[(k + 1) % len(f)]]))]
    NF.append(N)
    if sg(dot(N, V[f[0]])) <= 0: bad.append(i)
well = not bad
# edges
E = {}
for i, f in enumerate(F):
    for k in range(len(f)): a, b = f[k], f[(k + 1) % len(f)]; E.setdefault((min(a, b), max(a, b)), []).append(i)
manifold = all(len(l) == 2 for l in E.values())
EL = sorted(E)
# symmetry of the corner set (numerical, as census.py)
def sym_group(P, tol=1e-7):
    P = P / np.linalg.norm(P, axis=1).max(); r = np.linalg.norm(P, axis=1)
    order = np.argsort(-r); i1 = order[0]; same1 = [i for i in range(len(P)) if abs(r[i] - r[i1]) < tol]
    i2 = next(i for i in order if np.linalg.norm(np.cross(P[i1], P[i])) > 1e-3)
    same2 = [i for i in range(len(P)) if abs(r[i] - r[i2]) < tol]
    B = np.array([P[i1], P[i2], np.cross(P[i1], P[i2])]); d12 = np.linalg.norm(P[i1] - P[i2]); G = []; T = cKDTree(P)
    for a in same1:
        for b in same2:
            if abs(np.linalg.norm(P[a] - P[b]) - d12) > tol: continue
            for s in (1, -1):
                C = np.array([P[a], P[b], s * np.cross(P[a], P[b])]); M = np.linalg.solve(B, C)
                if not np.allclose(M @ M.T, np.eye(3), atol=1e-6): continue
                dd, idx = T.query(P @ M)
                if np.all(dd < tol * 10): G.append(idx)
    return G, P
G, PN = sym_group(VF)
eidx = {e: i for i, e in enumerate(EL)}; par = list(range(len(EL)))
def fd(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for perm in G:
    for e in EL:
        a, b = perm[e[0]], perm[e[1]]; j = eidx.get((min(a, b), max(a, b)))
        if j is not None: par[fd(eidx[e])] = fd(j)
orbit = [fd(i) for i in range(len(EL))]
# fins
fins = []; classes = {}
for i, (a, b) in enumerate(EL):
    A, B = V[a], V[b]; a2, b2 = dot(A, A), dot(B, B); ab = dot(A, B); D = vsub(B, A); c2 = dot(D, D)
    Af, Bf = np.array([float(x) for x in A]), np.array([float(x) for x in B]); th = math.atan2(np.linalg.norm(np.cross(Af, Bf)), Af @ Bf)
    c2t = 2 * ab * ab / (a2 * b2) - 1
    rp = rational_pi(c2t, th) if exact else rational_pi_float(th)
    right = [w for w, z in (('O', ab), ('A', dot(A, D)), ('B', -dot(B, D))) if sg(z) == 0]
    s1, s2 = sorted([a2, b2], key=float)
    k = (key(s1), key(s2), key(c2)); classes.setdefault(k, []).append(i)
    # edge dihedral of the solid at AB (interior), from the two face normals
    f1, f2 = E[(a, b)] if len(E[(a, b)]) == 2 else (E[(a, b)][0], E[(a, b)][0])
    n1 = np.array([float(x) for x in NF[f1]]); n2 = np.array([float(x) for x in NF[f2]])
    dih = math.pi - math.acos(max(-1, min(1, n1 @ n2 / np.linalg.norm(n1) / np.linalg.norm(n2))))
    fins.append(dict(edge=[a, b], OA2=float(s1), OB2=float(s2), AB2=float(c2), OA2_exact=ex(s1), OB2_exact=ex(s2), AB2_exact=ex(c2),
                     apex=th, apex_deg=math.degrees(th), cos2apex_exact=ex(c2t), apex_rational_pi=rp, right_angle=right, solid_dihedral=dih, orbit=orbit[i]))
# wedges (face f, corner v): dihedral at the ray Ov between the fins of the two edges of f at v, inside the pyramid of f
wedges = []; per_corner = {}; per_face = []
for i, f in enumerate(F):
    m = len(f); s = 0.0
    for k in range(m):
        u, v, w = V[f[k - 1]], V[f[k]], V[f[(k + 1) % m]]
        vv = dot(v, v); up = vsub(u, [x * (dot(u, v) / vv) for x in v]); wp = vsub(w, [x * (dot(w, v) / vv) for x in v])
        cw = dot(up, wp); uu, ww = dot(up, up), dot(wp, wp)
        upf, wpf = np.array([float(x) for x in up]), np.array([float(x) for x in wp]); ang = math.atan2(np.linalg.norm(np.cross(upf, wpf)), upf @ wpf)
        reflex = sg(dot(cross(vsub(v, u), vsub(w, v)), NF[i])) < 0
        psi = 2 * math.pi - ang if reflex else ang
        c2p = 2 * cw * cw / (uu * ww) - 1
        rp = rational_pi(c2p, ang) if exact else rational_pi_float(ang)
        if rp and reflex: rp = f'2 - {rp}'
        wedges.append(dict(face=i, corner=f[k], psi=psi, psi_deg=math.degrees(psi), cos2_exact=ex(c2p), sign_cos=sg(cw), reflex=reflex, rational_pi=rp))
        per_corner.setdefault(f[k], []).append(psi); s += psi
    per_face.append(s - (m - 2) * math.pi)
corner_err = max(abs(sum(l) - 2 * math.pi) for l in per_corner.values())
solid_angle_err = abs(sum(per_face) - 4 * math.pi)
# congruence classes of fins (exact), wedge classes
fc = []
for k, l in sorted(classes.items(), key=lambda kv: (-len(kv[1]), fins[kv[1][0]]['apex'])):
    r = fins[l[0]]
    fc.append(dict(count=len(l), orbits=len({orbit[i] for i in l}), OA2=r['OA2'] / R2, OB2=r['OB2'] / R2, AB2=r['AB2'] / R2,
                   OA2_exact=r['OA2_exact'], OB2_exact=r['OB2_exact'], AB2_exact=r['AB2_exact'], apex_deg=r['apex_deg'],
                   cos2apex_exact=r['cos2apex_exact'], apex_rational_pi=r['apex_rational_pi'], right_angle=r['right_angle'], example_edge=r['edge']))
wc = {}
for w in wedges: wc.setdefault((round(w['psi'], 9)), []).append(w)
wcl = [dict(count=len(l), psi_deg=l[0]['psi_deg'], cos2_exact=l[0]['cos2_exact'], rational_pi=l[0]['rational_pi'], reflex=l[0]['reflex'])
       for _, l in sorted(wc.items())]
def pattern(groups):
    c = {}
    for l in groups: t = tuple(sorted(round(math.degrees(x), 4) for x in l)); c[t] = c.get(t, 0) + 1
    return [dict(count=v, wedges_deg=list(k)) for k, v in sorted(c.items(), key=lambda kv: -kv[1])]
fw = {}
for w in wedges: fw.setdefault(w['face'], []).append(w['psi'])
res = dict(src=os.path.basename(SRC), name=d['name'], family=d.get('family', 'DICTO Solids v7'), field=d.get('field'), exact=exact,
           convex=d.get('convex'), V=n, E=len(EL), F=len(F), manifold=manifold, well_defined=well, faces_O_not_inside=len(bad),
           symmetry_order=len(G), fins=len(EL), fin_classes=len(fc), fin_orbits=len(set(orbit)), all_congruent=len(fc) == 1,
           accidental_congruence=len(fc) < len(set(orbit)),
           right_fins=sum(1 for f in fins if f['right_angle']), rational_apex=sum(1 for f in fins if f['apex_rational_pi']),
           corner_sum_err=corner_err, solid_angle_err=solid_angle_err, R2=R2, classes=fc, wedge_classes=wcl,
           face_patterns=pattern(fw.values()), corner_patterns=pattern(per_corner.values()),
           apex_multiset=sorted(round(f['apex'], 9) for f in fins), dihedral_multiset=sorted(round(f['solid_dihedral'], 9) for f in fins),
           wedge_multiset=sorted(round(w['psi'], 9) for w in wedges),
           face_angle_multiset=None, fin_list=fins, points=VF.tolist(), faces=F, note=d.get('note', ''))
# face angles of the solid (for the dual comparison)
fa = []
for f in F:
    m = len(f)
    for k in range(m):
        u, v, w = VF[f[k - 1]], VF[f[k]], VF[f[(k + 1) % m]]; x, y = u - v, w - v
        fa.append(round(math.acos(max(-1, min(1, x @ y / np.linalg.norm(x) / np.linalg.norm(y)))), 9))
res['face_angle_multiset'] = sorted(fa)
# STRUTS view (DICTO 2026-11-02: "possibly struts is enough, or both as views"): one strut O -> each corner (the lines where fins meet),
# optionally the solid's own edges. Strut length classes exact; angles between struts joined by an edge = the fin apex angles; the
# smallest angle between any two struts; distinct lengths of centre struts and of edges (buildability with bottles / struts).
sc = {}
for i, p in enumerate(V): sc.setdefault(key(dot(p, p)), []).append(i)
struts = [dict(count=len(l), L2=float(dot(V[l[0]], V[l[0]])) / R2, L2_exact=ex(dot(V[l[0]], V[l[0]])), L=math.sqrt(float(dot(V[l[0]], V[l[0]]))))
          for k, l in sorted(sc.items(), key=lambda kv: -float(dot(V[kv[1][0]], V[kv[1][0]])))]
U = VF / np.linalg.norm(VF, axis=1)[:, None]; Gm = U @ U.T; np.fill_diagonal(Gm, -2)
edge_len = {}
for f in fins: edge_len.setdefault(round(f['AB2'] / R2, 9), [f['AB2_exact'], 0])[1] += 1
# fin planes: fins lying in one plane through O merge into one flat sheet (float64, 1e-9 on unit normals up to sign)
pl = set()
for f in fins:
    m = np.cross(VF[f['edge'][0]], VF[f['edge'][1]]); m /= np.linalg.norm(m); m = m if (m[np.argmax(np.abs(m) > 1e-9)] > 0) else -m
    pl.add(tuple(np.round(m, 9)))
# flat sheets: fins that share a corner ray and lie in one plane join into one flat sheet (exact det = 0 where exact)
pf = list(range(len(fins)))
def fp(x):
    while pf[x] != x: pf[x] = pf[pf[x]]; x = pf[x]
    return x
at = {}
for i, f in enumerate(fins):
    for v in f['edge']: at.setdefault(v, []).append(i)
for v, l in at.items():
    for i, j in itertools.combinations(l, 2):
        a = [x for x in fins[i]['edge'] if x != v][0]; b = [x for x in fins[j]['edge'] if x != v][0]
        if sg(qf.det3(V[v], V[a], V[b])) == 0 and sg(dot(cross(V[v], V[a]), cross(V[v], V[b]))) < 0: pf[fp(i)] = fp(j)
comp = {}
for i in range(len(fins)): comp.setdefault(fp(i), []).append(i)
discs = collections.Counter(len(l) for l in comp.values() if abs(sum(fins[i]['apex'] for i in l) - 2 * math.pi) < 1e-9)
sheets = collections.Counter(collections.Counter(fp(i) for i in range(len(fins))).values())
res.update(fin_planes=len(pl), flat_sheets=sum(sheets.values()), sheet_sizes={str(k): v for k, v in sorted(sheets.items())}, central_discs={str(k): v for k, v in sorted(discs.items())}, struts=n, strut_classes=struts, strut_lengths=len(struts), strut_min_angle_deg=math.degrees(math.acos(min(1, Gm.max()))),
           edge_lengths=len(edge_len), edge_length_classes=[dict(AB2=k, AB2_exact=v[0], count=v[1]) for k, v in sorted(edge_len.items())],
           frame_lengths=len(set(round(s['L2'], 9) for s in struts) | set(edge_len)))
os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True); json.dump(res, open(OUTF, 'w'))
print(os.path.basename(SRC), 'fins', len(EL), 'classes', len(fc), 'orbits', len(set(orbit)), 'well', well, 'bad', len(bad),
      'struts', n, 'strut lengths', len(struts), 'edge lengths', len(edge_len), 'corner_err %.1e' % corner_err, 'omega_err %.1e' % solid_angle_err, 'exact', exact, flush=True)
