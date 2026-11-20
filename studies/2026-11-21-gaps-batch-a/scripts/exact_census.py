# exact_census.py -- exact re-check of the Star / Star Halo census (census.py + collect.py, copied unchanged from study 2026-11-02-halo-census)
# for the 5 Platonic (controls), 13 Archimedean and 13 Catalan solids, in each solid's own number field (nf.py; all contain sqrt5).
#  1. Star Halo (centre halo: hull of t x the feet; shape independent of t), Polar Halo (hull of the poles of the face planes), Star at
#     t = 2 and Golden Star at t = phi (the solid with each face pyramid turned out to t x foot; a surface, neighbours merged only when
#     exactly coplanar): recomputed exactly; corners, faces and faces by sides must equal census.py's (which is exact only in Q(sqrt5)).
#  2. Every "known" match of collect.py (float: same corners, scaled distances 1e-6, an orthogonal map) is re-checked exactly: the corner set
#     equals the target's up to scale under one of the 48 signed permutations (the targets of the Platonic/Archimedean/Catalan set and the
#     DICTO Solids v7 entries in Q(sqrt5) are exact). For a star the faces must agree too; same corners with other faces = "same corners only".
#  3. Every NEW object: the nearest registry object with the same number of corners, and its distance-key margin (float, for the record).
# Usage: python -u exact_census.py <work dir> <out json> [slug ...]
import sys, os, json, itertools, time, glob
from fractions import Fraction as Fr
import numpy as np
from nf import fields, vsub, vadd, vmul, dot, cross, key, iszerov
from exactgeo import exact_hull, sides, feet_and_poles, star_surface
W, OUT = sys.argv[1:3]; ONLY = sys.argv[3:]; T0 = time.time()
Q5, Q25, QT5, QXI = fields(); FIELDS = {F.name: F for F in (Q5, Q25, QT5, QXI)}
EX = json.load(open(os.path.join(W, 'ds', 'exact.json')))
CEN = {(c['slug'], c['part']): c for c in json.load(open(os.path.join(W, 'census', 'census.json')))}
SH = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(W, 'census', 'shapes', '*.json'))}
def load(slug):
    d = EX[slug]; F = FIELDS[d['field']]
    return F, [[F(*[Fr(c) for c in x]) for x in v] for v in d['coords']], d['faces']
SP = [np.diag(s) @ np.eye(3)[list(p)] for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
def to_field(F, P):
    """embed exact points of another field into F where possible (Q(sqrt5) points into any of the four fields)"""
    if P and P[0][0].F is F: return P
    assert P[0][0].F is Q5
    s5 = {Q5.name: Q5(0, 1)}.get(F.name)
    if s5 is None:
        if F is Q25: th = F.gen(); r2 = (th * th * th - th * 11) / 6; s5 = th - r2
        elif F is QXI: x = F.gen(); s5 = (x * x * x - x * 2) * 2 - 1
        else:
            from mpmath import pslq, mpf
            r = pslq([mpf(5) ** 0.5 * 1] + F.pw, maxcoeff=10 ** 8, maxsteps=10 ** 6, tol=mpf(10) ** -120)
            s5 = F(*[Fr(-r[i + 1], r[0]) for i in range(F.n)])
        assert s5 * s5 == F(5)
    return [[F(x.c[0]) + s5 * x.c[1] for x in v] for v in P]
def same_up_to_scale(A, B, FA=None, FB=None):
    """exact: B (as a set) = lambda * M A for one of the 48 signed permutations M and some lambda > 0 (both centred at the origin);
    returns the map or None. Faces compared when FA, FB given (as sets of corner sets)."""
    if len(A) != len(B): return None
    ra = max(dot(v, v).mp() for v in A); rb = max(dot(v, v).mp() for v in B)
    a0 = max(A, key=lambda v: dot(v, v).mp()); b0 = max(B, key=lambda v: dot(v, v).mp())
    lam2 = dot(b0, b0) / dot(a0, a0)
    Bf = np.array([[float(x) for x in v] for v in B])
    for M in SP:
        perm = [int(np.argmax(np.abs(M[i]))) for i in range(3)]; sg = [int(M[i][perm[i]]) for i in range(3)]
        MA = [[v[perm[i]] * sg[i] for i in range(3)] for v in A]
        lam = float(lam2) ** .5; ok = True; mp_ = []
        for v in MA:
            vf = np.array([float(x) * lam for x in v]); cand = list(np.where(np.linalg.norm(Bf - vf, axis=1) < 1e-6 * (1 + np.abs(Bf).max()))[0])
            j = next((j for j in cand if iszerov(cross(v, B[j])) and dot(v, B[j]).sign() > 0 and (dot(B[j], B[j]) - lam2 * dot(v, v)).iszero()), None)
            if j is None: ok = False; break
            mp_.append(j)
        if ok and len(set(mp_)) == len(B):
            if FA is not None:
                fa = {frozenset(mp_[i] for i in f) for f in FA}; fb = {frozenset(f) for f in FB}
                return ('same solid' if fa == fb else 'same corners only', M.tolist())
            return ('same', M.tolist())
    return None
def v7_exact(slug):
    import sympy as sp
    d = json.load(open(os.path.join(W, 'dsall', 'solids', slug + '.json')))
    r = sp.sqrt(5)
    def parse(s):
        e = sp.expand(sp.sympify(s, locals={'sqrt': sp.sqrt})); b = e.coeff(r); a = sp.expand(e - b * r)
        return Q5(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)))
    V = [[parse(x) for x in v['exact']] for v in d['vertices']]
    c = [sum((v[i] for v in V), Q5(0)) / len(V) for i in range(3)]
    return [vsub(v, c) for v in V], d['faces'], d.get('convex', True)
NAME2SLUG = {d['name']: s for s, d in EX.items()}
def target_points(label, F):
    fam, nm = label.split(': ', 1)
    if fam in ('Platonic', 'Archimedean', 'Catalan'):
        s = nm.lower().replace('_', '-')
        if s in EX: G, P, Fc = load(s); return to_field(F, P) if G is not F else P, Fc, s
        return None
    if fam == 'v7':
        if nm in NAME2SLUG:
            s = NAME2SLUG[nm]; G, P, Fc = load(s); return (to_field(F, P) if G is not F else P), Fc, s
        for f in glob.glob(os.path.join(W, 'dsall', 'solids', 'dicto-*.json')):
            d = json.load(open(f))
            if (d['name'] + (f" ({d['D']})" if d.get('D') else '')) == nm and d.get('field') == 'Q(sqrt(5))':
                P, Fc, _ = v7_exact(os.path.basename(f)[:-5]); return to_field(F, P), Fc, os.path.basename(f)[:-5]
    return None

res = []; fails = []
def check(label, ok):
    print(('PASS ' if ok else 'FAIL ') + label, flush=True)
    if not ok: fails.append(label)
phiE = {}
order = [s for s in ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron'] if s in EX] + sorted(s for s in EX if EX[s]['family'] == 'Archimedean') + sorted(s for s in EX if EX[s]['family'] == 'Catalan')
for slug in order:
    if ONLY and slug not in ONLY: continue
    F, V, Fc = load(slug); rec = dict(slug=slug, name=EX[slug]['name'], family=EX[slug]['family'], field=F.name)
    phi = (1 + to_field(F, [[Q5(0, 1)] * 3])[0][0]) / 2
    feet, poles = feet_and_poles(V, Fc)
    rec['face_families'] = len({(len(f), str(dot(x, x).c)) for f, x in zip(Fc, feet)})
    objs = {}
    for part, P in (('centre_halo', feet), ('polar_halo', poles)):
        HF, ok = exact_hull(P); cr = sorted({i for f in HF for i in f})
        objs[part] = ([P[i] for i in cr], [[cr.index(i) for i in f] for f in HF], ok)
    for part, t in (('star_2', F(2)), ('star_phi', phi)):
        Q, SF, ok = star_surface(V, Fc, t); cr = sorted({i for f in SF for i in f})
        objs[part] = ([Q[i] for i in cr], [[cr.index(i) for i in f] for f in SF], ok)
    for part, (P, PF_, ok) in objs.items():
        cs = SH[slug].get(part); cm = CEN.get((slug, part), {})
        agree = cs is not None and cs['corners'] == len(P) and cs['faces'] == len(PF_) and {int(k): v for k, v in cs['faces_by_sides'].items()} == sides(PF_)
        r = dict(corners=len(P), faces=len(PF_), faces_by_sides=sides(PF_), exact_ok=ok, census_agrees=agree, symmetry=cs and cs['symmetry'],
                 collect_status=cm.get('status'), collect_matches=cm.get('matches', []))
        # convexity of a star (exact): every face plane has all corners on one side
        if part.startswith('star'):
            cv = True
            for f in PF_:
                a, b, c = P[f[0]], P[f[1]], P[f[2]]; n = cross(vsub(b, a), vsub(c, a)); sg = {dot(n, vsub(q, a)).sign() for q in P} - {0}
                if len(sg) > 1: cv = False; break
            r['convex'] = cv
        # exact confirmation of each float match
        conf = []
        for lab in cm.get('matches', []):
            tp = target_points(lab, F)
            if tp is None: conf.append((lab, 'not checked exactly (target not exact here)')); continue
            TP, TF, ts = tp
            m = same_up_to_scale(P, TP, PF_ if part.startswith('star') else None, TF if part.startswith('star') else None)
            conf.append((lab, m[0] if m else 'NO exact match'))
        r['exact_matches'] = conf
        check(f"{rec['name']} / {part}: exact hull/surface ok {ok}; {len(P)} corners, {len(PF_)} faces {sides(PF_)}; census.py agrees {agree}; collect: {r['collect_status']}; exact: {conf}",
              ok and agree and not any(c[1] == 'NO exact match' for c in conf) and (not conf or any(c[1] in ('same', 'same solid', 'same corners only') for c in conf)))
        rec[part] = r
    res.append(rec); json.dump(res, open(OUT, 'w'), indent=1, default=str)
    print(f'   {round(time.time() - T0)} s', flush=True)
print('FINAL ok' if not fails else 'FINAL FAIL: %d checks' % len(fails))
