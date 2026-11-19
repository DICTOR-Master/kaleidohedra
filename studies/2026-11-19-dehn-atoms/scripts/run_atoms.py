# Dehn atoms (19 Nov 2026): the Dehn invariant of every single-solid atom of The DICTOnary of Atoms, by the dehn-words tool
# (scripts/dehn_mp.py, copied unchanged from studies/2026-11-19-dehn-words: 80 digits, PSLQ among the distinct dihedrals and pi,
# ZERO at |sum| < 1e-45, NONZERO at > 1e-6, UNDECIDED between). This file only loads corners and faces and checks them:
#   exact model files (DICTO Solids format: exact strings in Q, Q(sqrt d), Q(2**(1/3)), Q(t) with field_definition) evaluated at 100 digits;
#   exact constructions (classical shapes and the app's exact definitions), at 80 digits;
#   AXE, CLEO, FUJI identified in Q(sqrt5) exactly as the dehn-words study did.
# Checks before the Dehn sum (each must hold, or the atom is reported FAIL and not screened): every edge in exactly two faces, used once
# each way (closed oriented surface); every face planar to 1e-60; volume positive; the file's stated volume (decimal) matched to 1e-12.
# Usage: run_atoms.py <manifest.json> <k-research root> <dataset parent> <out dir> <atom index> [<atom index> ...]
import json, os, sys, re, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dehn_mp as T                         # the tool, unchanged (mp.dps = 80 is set there)
from dehn_mp import mp, mpf, sqrt, pi, cross, dot, sub, nrm, hull_faces, dehn, pslq
import sympy, numpy as np
from scipy.spatial import ConvexHull
MAN, KR, MD, OUT = sys.argv[1:5]
R5 = sqrt(5); PHI = (1 + R5)/2
def path(p): return os.path.join(MD, p[len('math-data:'):]) if p.startswith('math-data:') else os.path.join(KR, p)
# ---------- exact model files ----------
def field_gen(doc):
    fd = doc.get('field_definition')
    if not fd: return {}
    g = sympy.Symbol(fd['generator']); P = sympy.Poly(sympy.sympify(fd['minimal_polynomial'], locals={fd['generator']: g}), g)
    lo, hi = [sympy.Rational(x) for x in fd['isolating_interval']]
    with mp.workdps(120):
        rr = [r for r in mp.polyroots([int(c) for c in P.all_coeffs()], maxsteps=400, extraprec=400) if abs(mp.im(r)) < mpf(10)**-90 and lo < mp.re(r) < hi]
    assert len(rr) == 1, rr
    with mp.workdps(120): root = sympy.Float(mp.nstr(mp.re(rr[0]), 115), 115)
    assert abs(float(root) - float(fd['decimal'])) < 1e-12
    return {g: root}
def ev(txt, loc, sub_):
    e = sympy.sympify(txt, locals={str(k): k for k in sub_}) if sub_ else sympy.sympify(txt)
    if sub_: e = e.subs(sub_)
    return mpf(sympy.N(e, 100).__str__()) if e != 0 else mpf(0)
def load_model(p):
    doc = json.load(open(path(p))); sub_ = field_gen(doc)
    V = [[ev(x, None, sub_) for x in v['exact']] for v in doc['vertices']]
    vol = doc.get('volume', {}).get('decimal') if isinstance(doc.get('volume'), dict) else None
    return V, [list(f) for f in doc['faces']], dict(field=doc.get('field'), convex=doc.get('convex'), stated_volume=vol, model_name=doc.get('name'))
# ---------- exact constructions ----------
ico, tet, octa = T.ico, T.tet, T.octa
def keep_hull(P):
    Pf = np.array([[float(c) for c in v] for v in P]); h = ConvexHull(Pf); return [P[i] for i in sorted(h.vertices)]
def zono(dirs):
    P = []
    for s in itertools.product((1, -1), repeat=len(dirs)):
        P.append([sum(si*d[k] for si, d in zip(s, dirs))/2 for k in range(3)])
    V = keep_hull(P); return V, hull_faces(V)
def pyramid_on(V, F, f, c):
    W = [V[i] for i in f] + [c]; return W, hull_faces(W)
def face_classes(V, F, c, sides):
    """the face pyramids to c over faces with this many sides, grouped by congruence (sorted squared edge lengths, 30 digits)"""
    cl = {}
    for f in F:
        if len(f) != sides: continue
        W = [V[i] for i in f] + [c]; d2 = sorted(mp.nstr(dot(sub(a, b), sub(a, b)), 30) for a, b in itertools.combinations(W, 2))
        cl.setdefault(tuple(d2), []).append(f)
    return sorted(cl.values(), key=len)
def model_mean(p):
    V, F, _ = load_model(p); c = [sum(v[k] for v in V)/len(V) for k in range(3)]; return V, F, c
def ident(name):
    P = json.load(open(os.path.join(KR, 'studies/2026-10-14-axe-cleo-fuji/nets/pieces.json')))
    def exact(x):                           # the dehn-words rule, unchanged
        if abs(x) < 1e-12: return mpf(0)
        r = pslq([mpf(repr(x)), mpf(1), R5], maxcoeff=400, maxsteps=10**5, tol=mpf(10)**-8)
        assert r and r[0] != 0, x
        v = (-mpf(r[1]) - r[2]*R5)/r[0]; assert abs(v - x) < 2e-9, (x, v); return v
    V = [[exact(x) for x in v] for v in P[name]['vertices']]
    return V, hull_faces(V), dict(field='Q(sqrt(5))', convex=True, stated_volume=None)
def construct(key):
    info = dict(field=None, convex=True, stated_volume=None)
    if key == 'cleo_icos':
        F = hull_faces(ico); W = [ico[i] for i in F[0]] + [[mpf(0)]*3]; return W, hull_faces(W), dict(info, field='Q(sqrt(5))')
    if key == 'tetra_face_pyramid':
        W = tet[:3] + [[mpf(0)]*3]; return W, hull_faces(W), dict(info, field='Q')
    if key == 'half_octahedron':
        W = [[mpf(1), 0, 0], [mpf(-1), 0, 0], [0, mpf(1), 0], [0, mpf(-1), 0], [0, 0, mpf(1)]]; W = [[mpf(x) for x in v] for v in W]
        return W, hull_faces(W), dict(info, field='Q', stated_volume=mp.nstr(mpf(2)/3, 20))
    if key == 'brick':
        s = 1/sqrt(2); W = [[i*s, j*s, 2*k*s] for i in (0, 1) for j in (0, 1) for k in (0, 1)]; return W, hull_faces(W), dict(info, field='Q(sqrt(2))', stated_volume=mp.nstr(2*s**3, 20))
    if key == 'hex_prism':
        H = [[mp.cos(k*pi/3), mp.sin(k*pi/3)] for k in range(6)]; W = [[h[0], h[1], mpf(z)] for z in (0, 1) for h in H]
        return W, hull_faces(W), dict(info, field='Q(sqrt(3))', note='side 1, height 1; every height gives the same dihedrals 90 and 120 degrees')
    if key in ('id_stage_third', 'id_stage_golden'):
        x = mpf(1)/3 if key == 'id_stage_third' else 1/(PHI*R5)
        base = [[0, 0, PHI], [mpf(1)/2, PHI/2, PHI**2/2]]; IDV = []
        for b in base:
            for s in itertools.product((1, -1), repeat=3):
                for r in range(3):
                    v = [s[(i - r) % 3]*b[(i - r) % 3] for i in range(3)]
                    if not any(all(abs(p - q) < mpf(10)**-60 for p, q in zip(v, w)) for w in IDV): IDV.append(v)
        assert len(IDV) == 30
        E = [(a, b) for a, b in itertools.combinations(IDV, 2) if abs(nrm(sub(a, b)) - 1) < mpf(10)**-60]; assert len(E) == 60
        W = [[a[k] + x*(b[k] - a[k]) for k in range(3)] for a, b in E] + [[b[k] + x*(a[k] - b[k]) for k in range(3)] for a, b in E]
        F = hull_faces(W); return W, F, dict(info, field='Q(sqrt(5))', cut=mp.nstr(x, 20))
    if key == 'bain_rd' or key == 'regular_hex_ed':
        r2 = sqrt(2); D = [[mpf(a)/2, mpf(b)/2, c*r2/2] for a, b, c in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
        if key == 'regular_hex_ed': D.append([mpf(1), mpf(0), mpf(0)])
        V, F = zono(D); return V, F, dict(info, field='Q(sqrt(2))')
    if key in ('all_rhombus_block', 'flattened_rhombohedron', 'skewed_rd_check'):
        s3 = sqrt(3); c72 = mp.cos(2*pi/5); y = 2*c72/s3
        v = [mpf(1)/2, s3/2, mpf(0)]; w = [-mpf(1)/2, s3/2, mpf(0)]; d = [mpf(0), y, sqrt(1 - y*y)]
        X = list(mp.lu_solve(mp.matrix([v, w, d]), mp.matrix([-mpf(1)/2, c72, mpf(1)/2])))
        dirs = {'all_rhombus_block': [v, w, d], 'flattened_rhombohedron': [v, w, X], 'skewed_rd_check': [v, w, d, X]}[key]
        V, F = zono(dirs); return V, F, dict(info, field='Q(sqrt3, sqrt5, sqrt(1 - y^2)) at 80 digits')
    if key == 'admiral_cap':
        V = [[PHI/2, 0, -mpf(1)/2], [PHI/2, 0, mpf(1)/2], [PHI**2/2, 0, 0], [mpf(1)/2, -PHI/2, 0], [mpf(1)/2, PHI/2, 0]]
        V = [[mpf(x) for x in v] for v in V]
        F = [[2, 1, 3], [2, 3, 0], [1, 0, 3], [2, 4, 1], [2, 0, 4], [4, 0, 1]]
        return V, F, dict(info, field='Q(sqrt(5))', convex=False, stated_volume=mp.nstr(PHI/12, 20))
    if key in ('hex_aktis', 'deltoid_aktis', 'triaktis', 'tetraktis'):
        src = 'math-data:studies/2026-10-22-math-data-dicto-solids/solids/' + ('dicto-ogdoecontahedron.json' if key in ('hex_aktis', 'deltoid_aktis') else 'dicto-ott.json')
        V, F, c = model_mean(src); sides = {'hex_aktis': 6, 'deltoid_aktis': 4, 'triaktis': 3, 'tetraktis': 4}[key]
        cl = face_classes(V, F, c, sides); counts = [len(x) for x in cl]
        want = {'hex_aktis': [20], 'deltoid_aktis': [60], 'triaktis': [8, 24], 'tetraktis': [6]}[key]
        assert counts == want, (key, counts)
        f = cl[-1][0]; W, G = pyramid_on(V, F, f, c)
        return W, G, dict(info, field='Q(sqrt(5))', classes=counts)
    raise KeyError(key)
# ---------- checks ----------
def checks(V, F):
    E = {}
    for fi, f in enumerate(F):
        for i in range(len(f)): E[(f[i], f[(i+1) % len(f)])] = E.get((f[i], f[(i+1) % len(f)]), 0) + 1
    closed = all(c == 1 for c in E.values()) and all(E.get((b, a), 0) == 1 for (a, b) in E)
    pl = mpf(0)
    for f in F:
        n = [mpf(0)]*3
        for i in range(len(f)): n = [x + y for x, y in zip(n, cross(V[f[i]], V[f[(i+1) % len(f)]]))]
        L = nrm(n); n = [x/L for x in n]
        pl = max([pl] + [abs(dot(n, sub(V[j], V[f[0]]))) for j in f])
    vol = sum(dot(V[f[0]], cross(V[f[i]], V[f[i+1]])) for f in F for i in range(1, len(f)-1))/6
    return dict(closed_oriented=bool(closed), edges=len(E)//2, max_planarity=mp.nstr(pl, 3), planar=bool(pl < mpf(10)**-60), volume=mp.nstr(abs(vol), 25), volume_sign=int(mp.sign(vol)))
def screen(V, F, name, info):
    ch = checks(V, F); ok = ch['closed_oriented'] and ch['planar'] and ch['volume_sign'] != 0
    if info.get('stated_volume'):
        sv = mpf(info['stated_volume']); ch['stated_volume_match'] = bool(abs(abs(mpf(ch['volume'])) - sv) <= mpf(10)**-12*max(1, sv)); ok = ok and ch['stated_volume_match']
    r = dict(name=name, corners=len(V), checks=ch, info={k: v for k, v in info.items() if k != 'stated_volume'})
    if not ok: r['verdict'] = 'FAIL (data checks)'; return r
    t0 = time.time(); d = dehn(V, F, name); d['seconds'] = round(time.time() - t0, 1); r.update(d); return r
if __name__ == '__main__':
    man = json.load(open(MAN)); os.makedirs(OUT, exist_ok=True)
    for i in map(int, sys.argv[5:]):
        a = man['atoms'][i]; res = dict(index=i, no=a['no'], name=a['name'], kind=a['kind'], book=a['book'], source=a['source'], solids=[])
        try:
            if a['source'] in ('file', 'set'):
                for p in a['files']:
                    V, F, info = load_model(p); info['file'] = p; res['solids'].append(screen(V, F, info.get('model_name') or a['name'], info))
            elif a['source'] == 'cons':
                V, F, info = construct(a['key']); info['construction'] = a['key']; res['solids'].append(screen(V, F, a['name'], info))
                if a['key'] == 'all_rhombus_block':      # the app's definition reproduces the dataset's D1 (same distinct dihedrals)
                    V2, F2, _ = construct('skewed_rd_check'); D1, G1, _ = load_model('math-data:studies/2026-10-22-math-data-dicto-solids/solids/dicto-skewed-rhombic-dodecahedron.json')
                    s2, s1 = dehn(V2, F2, 'x'), dehn(D1, G1, 'y'); res['d1_check'] = dict(construction_faces=len(F2), dataset_faces=len(G1), construction_verdict=s2['verdict'], dataset_verdict=s1['verdict'], distinct=(s2['distinct_dihedrals'], s1['distinct_dihedrals']))
            elif a['source'] == 'ident':
                V, F, info = ident(a['key']); info['identified'] = a['key']; res['solids'].append(screen(V, F, a['key'], info))
            else:
                res['verdict'] = {'float': 'data float only — skipped', 'skip': 'skipped (' + a.get('key', '') + ')', 'same': 'same solid as ' + a.get('key', '')}.get(a['source'], 'skipped')
        except Exception as ex:
            res['error'] = repr(ex)[:500]
        if res['solids']:
            vs = [s.get('verdict') for s in res['solids']]
            res['verdict'] = vs[0] if len(set(vs)) == 1 else 'mixed: ' + ', '.join(vs)
        json.dump(res, open(os.path.join(OUT, 'atom-%03d.json' % i), 'w'), indent=1, ensure_ascii=False)
        for s in res['solids']:
            print('ATOM %3d %-6s %-44s %-9s faces %4d corners %4d dihedrals %3s indep %3s max %-10s %ss checks closed=%s planar=%s vol=%s' % (
                i, a['no'][:6], s['name'][:44], s.get('verdict'), len(s.get('faces', [])) if isinstance(s.get('faces'), list) else s.get('faces', 0), s['corners'],
                s.get('distinct_dihedrals', '-'), s.get('independent_mod_pi', '-'), s.get('max_coefficient_sum', '-'), s.get('seconds', '-'),
                s['checks']['closed_oriented'], s['checks']['planar'], s['checks'].get('stated_volume_match', 'n/a')), flush=True)
        if not res['solids']: print('ATOM %3d %-6s %-44s %s %s' % (i, a['no'][:6], a['name'][:44], res.get('verdict', ''), res.get('error', '')), flush=True)
