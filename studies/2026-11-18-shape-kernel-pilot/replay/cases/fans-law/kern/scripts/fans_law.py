"""Do the open fans follow one law? (13 Nov 2026; Platonic book Ch 4 open item; LEADS 2 and 3 of studies/2026-11-13-platonic-disc-ranking)
Exact in a real quadratic field Q(sqrt D), D in {5, 2, 3, 6} (rationals included), field class qf.py copied verbatim from the #87 study
(studies/2026-11-02-dicto-vacuus/scripts/qf.py).
For every solid of the app registry (389 solids, ../2026-11-13-platonic-disc-ranking/data/registry-solids.json) whose corners are
recognised exactly (each coordinate, after one common scale 1, 1/max|x| or 1/min|x|, = (a + b sqrt D)/N, N in {4, 12}, |a|, |b| <= 8N, unique within 1e-7):
  1. checks: closed oriented surface (every edge in exactly 2 faces, opposite directions), every face exactly planar, convexity.
  2. #87 discs exactly: fins O-A-B (O = mean of the corners, exact) join across a corner ray when coplanar and on opposite sides of the
     ray; a disc = a sheet that is one closed cycle winding once round O (signed count of fins over a fixed in-plane ray = +-1, all fins
     turning the same way). Float apex sum as a cross-check.
  3. For every central plane carrying a fin, the SECTION test: a face is CROSSED by the plane when it has corners strictly on both sides;
     the plane is EDGE-CLOSED when no face is crossed and no face lies in the plane (then the surface meets the plane only in edges
     and corners). Section components (corners in the plane, edges crossing it, joined by in-plane edges and crossed faces).
     Law tested: disc in the plane  <=>  plane edge-closed; and on every plane: open fans = maximal runs of in-plane edges.
Named results: Hexa-Key (exact disc sizes and share; volume 6 phi^3 = 3/4 of its bounding cube (2 phi)^3, as 48 of 64 in the Jewel
study); Delilah 3 x 4; controls octahedron 3 x 4, cube 0, cuboctahedron 4 x 6, icosidodecahedron 6 x 10, RD and RT: every edge plane
two opposite fans; Dogstar 0 discs, 12 planes 4 + 4 fins, 3 planes 3 + 3 (exact study).
Signs of plane tests use a float filter: when |float value| > 1e-6 its float sign is taken (coordinates exact, float error < 1e-12),
otherwise the sign is computed exactly.
Usage: fans_law.py registry-solids.json disc-ranking.json out.json [--pilot]"""
import sys, os, json, math, time, itertools
from fractions import Fraction as Fr
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'qf.py')).read(), globals())
PILOT = '--pilot' in sys.argv; args = [a for a in sys.argv[1:] if a != '--pilot']
S = json.load(open(args[0])); FLOAT = {r['id']: r for r in json.load(open(args[1]))['solids']}; OUT = args[2]
NAMED = ['D8', 'CUBE', 'CUBOCTAHEDRON', 'ICOSIDODECAHEDRON', 'DODECAHEDRON', 'RHOMBIC_DODECAHEDRON', 'RHOMBIC_TRIACONTAHEDRON',
         'DICTO_HEXA_KEY', 'DICTO_DELILAH', 'DOGSTAR', 'DODECA_TETRAHEDRAL_CLUSTER', 'DODECA_OCTAHEDRAL_CLUSTER']
if PILOT: S = [s for s in S if s['id'] in NAMED] + [s for s in S if s['id'] not in NAMED][:12]
CHECKS = []
def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok))); print(('ok   ' if ok else 'FAIL ') + name + (('  [' + detail + ']') if detail else ''), flush=True); return ok

# ------------------------------------------------------------------ exact helpers
def dv(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cr(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def sub(u, v): return (u[0] - v[0], u[1] - v[1], u[2] - v[2])
def iszero(v): return all(x == 0 for x in v)
def sgn(x): return x.sign() if isinstance(x, QF) else (x > 0) - (x < 0)
def fsgn(n, nf, p, pf):
    """sign of n . p, float filter then exact"""
    f = nf[0] * pf[0] + nf[1] * pf[1] + nf[2] * pf[2]
    if abs(f) > 1e-6: return 1 if f > 0 else -1
    return sgn(dv(n, p))
def key(n):
    k = next(i for i in range(3) if n[i] != 0); return tuple(x / n[k] for x in n)

def recog_solid(Vf):
    """one common field and scale for all coordinates; returns (D, scale label, exact corners, max residual) or None"""
    m = max(abs(x) for p in Vf for x in p); mn = min(abs(x) for p in Vf for x in p if abs(x) > 1e-6)
    for D in (5, 2, 3, 6):
        r5 = math.sqrt(D)
        for sc_lab, sc in (('1', 1.0), ('1/max|x|', 1 / m), ('1/min|x|', 1 / mn)):
            for N in (4, 12):
                out = []; res = 0.0; ok = True
                for p in Vf:
                    q = []
                    for x in p:
                        x = x * sc; hits = []
                        for bq in range(-8 * N, 8 * N + 1):
                            aq = round((x - bq / N * r5) * N)
                            if abs(aq) <= 8 * N:
                                e = abs(aq / N + bq / N * r5 - x)
                                if e < 1e-7: hits.append((aq, bq, e))
                        if len(hits) != 1: ok = False; break
                        aq, bq, e = hits[0]; res = max(res, e); q.append((Fr(aq, N), Fr(bq, N)))
                    if not ok: break
                    out.append(q)
                if ok: return D, sc_lab, N, out, res
    return None

def edges_of(F):
    E = set()
    for f in F:
        for i in range(len(f)): E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
    return sorted(E)

def loop_winding(cyc, V, m):
    """signed winding number round O of a closed loop of corners in the central plane with normal m (exact): count of fins crossed
    by a fixed in-plane ray that meets no corner of the loop, each crossing with the fin's turning sense; also: all fins turn the same way?"""
    ok_r = None
    for t in range(1000, 1100):
        rr = tuple(V[cyc[0]][k] + V[cyc[1]][k] / t for k in range(3))
        if not any(iszero(cr(rr, V[x])) for x in cyc): ok_r = rr; break
    w = 0; orient = set()
    for k in range(len(cyc)):
        a, b = V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]; o = sgn(dv(cr(a, b), m)); orient.add(o)
        if o != 0 and sgn(dv(cr(a, ok_r), m)) == o and sgn(dv(cr(ok_r, b), m)) == o: w += o
    return w, len(orient) == 1

def analyse(s):
    rec = recog_solid(s['V'])
    if rec is None: return dict(id=s['id'], name=s['name'], recognised=False)
    D, sc_lab, N, raw, res = rec
    QF.D = D
    V0 = [tuple(QF(a, b) for a, b in p) for p in raw]
    n = len(V0); c = tuple(sum((p[i] for p in V0), QF(0)) / n for i in range(3))
    V = [sub(p, c) for p in V0]; Vf = [tuple(float(x) for x in p) for p in V]
    F = [list(f) for f in s['F']]; E = edges_of(F)
    R = dict(id=s['id'], name=s['name'], recognised=True, field=f'Q(sqrt{D})', scale=sc_lab, denom=N, max_residual=res,
             corners=n, faces=len(F), edges=len(E), centre_zero=iszero(c))
    # ---- surface checks
    dirs = {}
    for f in F:
        for i in range(len(f)):
            a, b = f[i], f[(i + 1) % len(f)]; dirs[(a, b)] = dirs.get((a, b), 0) + 1
    closed = all(dirs.get((a, b), 0) == 1 and dirs.get((b, a), 0) == 1 for a, b in E) and sum(dirs.values()) == 2 * len(E)
    FN = []; planar = True
    for f in F:
        nn = (QF(0), QF(0), QF(0))
        for i in range(len(f)):                     # Newell normal (exact)
            nn = tuple(nn[k] + cr(V[f[i]], V[f[(i + 1) % len(f)]])[k] for k in range(3))
        if iszero(nn): planar = False; FN.append(None); continue
        if any(dv(nn, sub(V[x], V[f[0]])) != 0 for x in f): planar = False
        FN.append(nn)
    R.update(closed_surface=closed, planar=planar, euler=n - len(E) + len(F))
    if closed and planar:
        vol = QF(0)
        for f in F:
            for i in range(1, len(f) - 1): vol = vol + dv(V[f[0]], cr(V[f[i]], V[f[i + 1]]))
        vol = vol / 6; R['volume'] = [str(vol.a), str(vol.b)]; R['volume_float'] = float(vol)
        R['outward'] = vol.sign() > 0
        sgn_out = 1 if vol.sign() > 0 else -1
        convex = all(all(sgn(dv(FN[i], sub(V[x], V[f[0]]))) * sgn_out <= 0 for x in range(n)) for i, f in enumerate(F))
        R['convex'] = convex
        R['face_cones_positive'] = all(sgn(dv(FN[i], V[f[0]])) * sgn_out > 0 for i, f in enumerate(F))
    else:
        R['convex'] = None
    # ---- #87 sheets (exact)
    through = {e for e in E if iszero(cr(V[e[0]], V[e[1]]))}
    fins = [e for e in E if e not in through]
    pf = list(range(len(fins)))
    def fp(x):
        while pf[x] != x: pf[x] = pf[pf[x]]; x = pf[x]
        return x
    at = {}
    for i, (a, b) in enumerate(fins): at.setdefault(a, []).append(i); at.setdefault(b, []).append(i)
    for v, l in at.items():
        for i, j in itertools.combinations(l, 2):
            a = fins[i][0] if fins[i][1] == v else fins[i][1]; b = fins[j][0] if fins[j][1] == v else fins[j][1]
            if dv(V[v], cr(V[a], V[b])) == 0 and sgn(dv(cr(V[v], V[a]), cr(V[v], V[b]))) < 0: pf[fp(i)] = fp(j)
    comp = {}
    for i in range(len(fins)): comp.setdefault(fp(i), []).append(i)
    sheets = []
    for r_, l in comp.items():
        m = cr(V[fins[l[0]][0]], V[fins[l[0]][1]])
        deg = {}
        for i in l:
            for x in fins[i]: deg[x] = deg.get(x, 0) + 1
        closed_c = len(l) >= 3 and all(d == 2 for d in deg.values())
        if closed_c:
            adj = {}
            for i in l:
                a, b = fins[i]; adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
            st = [fins[l[0]][0]]; seen = set(st)
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); st.append(y)
            closed_c = len(seen) == len(deg)
        orient = set()                                   # turning sense of each fin, taken along the cycle (closed sheets only)
        w = None
        if closed_c:
            # signed count, cycle traversed in order
            start = fins[l[0]][0]; cyc = [start]; prev = None; cur = start
            while True:
                nb = adj[cur]; nxt = nb[0] if nb[0] != prev else nb[1]
                if nxt == start: break
                cyc.append(nxt); prev, cur = cur, nxt
            rr = V[cyc[0]]; w = 0                         # fixed in-plane ray: through the first corner (exact, never degenerate)
            for k in range(len(cyc)):
                a, b = V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]; o = sgn(dv(cr(a, b), m)); orient.add(o)
                same = iszero(cr(a, rr)) and dv(a, rr).sign() > 0                         # rr on the ray of a: half-open sector [a, b)
                if same or (sgn(dv(cr(a, rr), m)) == o and sgn(dv(cr(rr, b), m)) == o): w += o
        apex = sum(math.acos(max(-1.0, min(1.0, sum(Vf[a][k] * Vf[b][k] for k in range(3)) / math.sqrt(sum(x * x for x in Vf[a]) * sum(x * x for x in Vf[b]))))) for a, b in (fins[i] for i in l))
        disc = closed_c and w is not None and abs(w) == 1 and len(orient) == 1
        sheets.append(dict(plane=key(m), fins=[fins[i] for i in l], disc=disc, closed=closed_c, wind=w, monotone=len(orient) == 1, apex=apex))
    R['apex_agree'] = all((abs(sh['apex'] - 2 * math.pi) < 1e-7) == sh['disc'] for sh in sheets)
    sizes = {}
    for sh in sheets:
        if sh['disc']: sizes[len(sh['fins'])] = sizes.get(len(sh['fins']), 0) + 1
    R['disc_sizes87'] = {str(k): v for k, v in sorted(sizes.items())}
    R['discs87'] = sum(sizes.values()); R['on87'] = sum(len(sh['fins']) for sh in sheets if sh['disc'])
    R['share87'] = [R['on87'], len(E)]
    fl = FLOAT.get(s['id'])
    R['float_agree'] = fl is not None and fl['disc_sizes87'] == R['disc_sizes87']
    # ---- plane-by-plane section test
    if not (closed and planar): R['planes'] = None; return R
    byplane = {}
    for sh in sheets: byplane.setdefault(sh['plane'], []).append(sh)
    Ffl = [[Vf[x] for x in f] for f in F]
    planes = []
    for pk, shs in byplane.items():
        nf = tuple(float(x) for x in pk)
        sv = [fsgn(pk, nf, V[i], Vf[i]) for i in range(n)]
        crossed = [i for i, f in enumerate(F) if any(sv[x] > 0 for x in f) and any(sv[x] < 0 for x in f)]
        inplane_faces = [i for i, f in enumerate(F) if all(sv[x] == 0 for x in f)]
        inE = [e for e in E if sv[e[0]] == 0 and sv[e[1]] == 0]          # edges in the plane (incl. through O)
        edge_closed = not crossed and not inplane_faces
        # edge runs = components of the in-plane edge graph (fins only)
        par = {}
        def f2(x):
            while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a, b in inE:
            if (a, b) in through: continue
            par[f2(a)] = f2(b)
        runs = {}
        for a, b in inE:
            if (a, b) in through: continue
            runs.setdefault(f2(a), set()).add((a, b))
        run_sets = sorted([frozenset(r_) for r_ in runs.values()], key=len)
        sheet_sets = sorted([frozenset(sh['fins']) for sh in shs], key=len)
        # section components: nodes = corners in plane ('v', i) and transverse edges ('e', a, b); joined by in-plane edges and crossed faces
        P2 = {}
        def g(x):
            while P2.setdefault(x, x) != x: P2[x] = P2[P2[x]]; x = P2[x]
            return x
        for a, b in inE: P2[g(('v', a))] = g(('v', b))
        cross_nodes = []; nonconvex_cut = 0
        for i in crossed:
            f = F[i]; nodes = [('v', x) for x in f if sv[x] == 0]
            for k in range(len(f)):
                a, b = f[k], f[(k + 1) % len(f)]
                if sv[a] * sv[b] < 0: nodes.append(('e',) + tuple(sorted((a, b))))
            if len(nodes) != 2: nonconvex_cut += 1
            for x in nodes[1:]: P2[g(nodes[0])] = g(x)
            cross_nodes.append(nodes[0])
        for x in [('v', i) for i in range(n) if sv[i] == 0]: g(x)
        crossed_roots = {g(x) for x in cross_nodes}
        disc_info = []
        for sh in shs:
            if sh['disc']:
                rt = g(('v', sh['fins'][0][0])); members = [x for x in P2 if g(x) == rt]
                disc_info.append(dict(size=len(sh['fins']), component_edge_only=rt not in crossed_roots,
                                      component_is_disc=rt not in crossed_roots and set(members) == {('v', x) for e in sh['fins'] for x in e}))
        comps = {}
        for x in P2: comps.setdefault(g(x), []).append(x)
        edge_loops = []          # non-convex solids: every section component made of edges only, as a loop round O or not
        if R['convex'] is False:
            for rt, mem in comps.items():
                if rt in crossed_roots: continue
                cs = {x[1] for x in mem if x[0] == 'v'}
                le = [e for e in inE if e[0] in cs and e not in through]
                if len(le) < 3: continue
                dg_ = {}
                for a_, b_ in le: dg_[a_] = dg_.get(a_, 0) + 1; dg_[b_] = dg_.get(b_, 0) + 1
                simple = all(d == 2 for d in dg_.values()) and len(dg_) == len(le)
                w_ = mono = None
                if simple:
                    adj_ = {}
                    for a_, b_ in le: adj_.setdefault(a_, []).append(b_); adj_.setdefault(b_, []).append(a_)
                    st_ = le[0][0]; cyc_ = [st_]; pv = None; cu = st_
                    while True:
                        nb = adj_[cu]; nx = nb[0] if nb[0] != pv else nb[1]
                        if nx == st_: break
                        cyc_.append(nx); pv, cu = cu, nx
                    simple = len(cyc_) == len(le)
                    if simple: w_, mono = loop_winding(cyc_, V, pk)
                turn_back = sum(1 for v_ in dg_ if dg_[v_] == 2 and (lambda nbs: sgn(dv(cr(V[v_], V[nbs[0]]), cr(V[v_], V[nbs[1]]))) > 0)([x for e in le if v_ in e for x in e if x != v_]))
                edge_loops.append(dict(edges=len(le), simple_loop=simple, winding=w_, monotone=mono, turn_back_corners=turn_back))
        open_sh = [sh for sh in shs if not sh['disc']]
        neg_ok = None
        if len(open_sh) == 2:     # opposite fans: the corner sets are negatives of each other
            vi = {V[i]: i for i in range(n)}
            A = {x for e in open_sh[0]['fins'] for x in e}; B = {x for e in open_sh[1]['fins'] for x in e}
            negA = {vi.get(tuple(-y for y in V[x])) for x in A}
            neg_ok = negA == B
        planes.append(dict(plane=[str(x) for x in pk], plane_float=[round(x, 6) for x in nf], fins_in_plane=sum(len(sh['fins']) for sh in shs),
                           edges_in_plane=len(inE), discs=len(disc_info), disc_sizes=sorted(d['size'] for d in disc_info),
                           open_fans=len(open_sh), fan_sizes=sorted(len(sh['fins']) for sh in open_sh), fans_opposite=neg_ok,
                           crossed_faces=len(crossed), faces_in_plane=len(inplane_faces), edge_closed=edge_closed,
                           sheets_equal_runs=run_sets == sheet_sets, components=len(comps), crossed_components=len(crossed_roots),
                           edge_only_components=len(comps) - len(crossed_roots), nonconvex_face_cuts=nonconvex_cut, disc_info=disc_info,
                           edge_loops=edge_loops, law=(len(disc_info) > 0) == edge_closed))
    R['planes'] = planes
    return R

res = []
for k, s in enumerate(S):
    r = analyse(s); res.append(r)
    if (k + 1) % 13 == 0 or k + 1 == len(S) or PILOT:
        print(f"PROGRESS {(k + 1) / len(S):.3f} {s['id']}: recognised {r['recognised']}" + (f", {r['field']}, discs {r['disc_sizes87']}, convex {r['convex']}" if r['recognised'] else '') + f' ({time.time() - T0:.0f} s)', flush=True)
B = {r['id']: r for r in res}

# ------------------------------------------------------------------ checks
for i in NAMED:
    check(f'X1 {i} recognised exactly and a closed oriented planar surface', B[i]['recognised'] and B[i]['closed_surface'] and B[i]['planar'] and B[i]['centre_zero'] in (True, False),
          f"{B[i].get('field')}, scale {B[i].get('scale')}, /{B[i].get('denom')}, residual {B[i].get('max_residual', 0):.1e}, centre at origin {B[i].get('centre_zero')}")
hk = B['DICTO_HEXA_KEY']
QF.D = 5; PHI = QF(Fr(1, 2), Fr(1, 2))
hv = QF(Fr(hk['volume'][0]), Fr(hk['volume'][1]))
check('X2 Hexa-Key: volume exactly 6 phi^3 = 3/4 of its bounding cube of edge 2 phi (Jewel study: 48 of 64)', hv == 6 * PHI * PHI * PHI, f"{hk['volume']} = {hk['volume_float']:.9f}")
check(f"X2 Hexa-Key exact #87 discs {hk['disc_sizes87']}, {hk['on87']} of {hk['edges']} edges on discs (float census: 3 x 8, 6 x 12, 96 of 360)",
      hk['disc_sizes87'] == {'8': 3, '12': 6} and hk['on87'] == 96 and hk['edges'] == 360, f"convex {hk['convex']}, Euler {hk['euler']}")
dl = B['DICTO_DELILAH']
check(f"X3 Delilah exact #87 discs {dl['disc_sizes87']}, {dl['on87']} of {dl['edges']} edges (float: 3 x 4, 100 %)", dl['disc_sizes87'] == {'4': 3} and dl['on87'] == dl['edges'] == 12)
want = {'D8': {'4': 3}, 'CUBE': {}, 'CUBOCTAHEDRON': {'6': 4}, 'ICOSIDODECAHEDRON': {'10': 6}, 'DODECAHEDRON': {}}
for i, w in want.items():
    check(f"X4 control {B[i]['name']}: #87 discs {B[i]['disc_sizes87']} (expect {w})", B[i]['disc_sizes87'] == w)
# RD: 6 planes, each two opposite fans of 2 fins; RT (pilot finding 13 Nov, kept as the control): 15 planes, each 4 single-fin fans
for i, nplanes, fans in (('RHOMBIC_DODECAHEDRON', 6, (2, 2)), ('RHOMBIC_TRIACONTAHEDRON', 15, (1, 1, 1, 1))):
    pl = [p for p in B[i]['planes'] if p['fins_in_plane'] >= 3]
    check(f"X5 control {B[i]['name']}: 0 discs; {len(pl)} planes with >= 3 edges (expect {nplanes}), each holding open fans {fans}, crossed by faces",
          B[i]['discs87'] == 0 and len(pl) == nplanes and all(tuple(p['fan_sizes']) == fans and not p['edge_closed'] for p in pl),
          str(sorted({(tuple(p['fan_sizes']), p['crossed_faces'], p['fans_opposite']) for p in pl})))
dg = B['DOGSTAR']; pl = [p for p in dg['planes'] if p['fins_in_plane'] >= 3]
check('X6 Dogstar exact: 0 discs; 15 planes with >= 3 edges: 12 with fans 4 + 4, 3 with 3 + 3, all opposite (exact study)',
      dg['discs87'] == 0 and len(pl) == 15 and sorted(tuple(p['fan_sizes']) for p in pl).count((4, 4)) == 12 and sorted(tuple(p['fan_sizes']) for p in pl).count((3, 3)) == 3 and all(p['fans_opposite'] for p in pl))
rec = [r for r in res if r['recognised']]; val = [r for r in rec if r['closed_surface'] and r['planar']]
cvx = [r for r in val if r['convex']]; ncv = [r for r in val if r['convex'] is False]
check(f'X7 apex-sum (float) and closed-cycle (exact) disc tests agree on every sheet of all {len(rec)} recognised solids', all(r['apex_agree'] for r in rec), str([r['id'] for r in rec if not r['apex_agree']][:8]))
fa = [r['id'] for r in rec if not r['float_agree']]
check(f'X8 exact #87 disc sizes equal the float census on all {len(rec)} recognised solids', not fa, str(fa[:8]))
bad = [(r['id'], p['plane_float']) for r in cvx for p in r['planes'] if not p['law']]
check(f'T1 THEOREM, convex solids ({len(cvx)} recognised, {sum(len(r["planes"]) for r in cvx)} planes): disc in the plane <=> plane edge-closed', not bad, str(bad[:5]))
bad = [(r['id'], p['plane_float']) for r in cvx for p in r['planes'] if not p['sheets_equal_runs'] or p['discs'] > 1]
check('T2 THEOREM, convex solids: the sheets in each plane are exactly the runs of in-plane edges (each run one fan, or the whole loop one disc)', not bad, str(bad[:5]))
bad = [r['id'] for r in cvx if not r['face_cones_positive']]
check('T3 convex solids: centre strictly inside (every face cone from O has positive volume)', not bad, str(bad[:5]))
# non-convex: the law as a finding, with counterexamples
ce_a = [(r['id'], r['name'], p) for r in ncv for p in r['planes'] if p['edge_closed'] and not p['discs']]
ce_b = [(r['id'], r['name'], p) for r in ncv for p in r['planes'] if p['discs'] and not p['edge_closed']]
ok_n = sum(1 for r in ncv for p in r['planes'] if p['law'])
print(f'\nNONCONVEX {len(ncv)} solids, {sum(len(r["planes"]) for r in ncv)} planes: law holds on {ok_n}; edge-closed without disc {len(ce_a)}; disc without edge-closed {len(ce_b)}')
for lab, ce in (('CE_A edge-closed, no disc', ce_a), ('CE_B disc, not edge-closed', ce_b)):
    cnt = {}
    for i, nm, p in ce: cnt[(i, nm)] = cnt.get((i, nm), 0) + 1
    for (i, nm), c in sorted(cnt.items(), key=lambda t: -t[1]): print(f'{lab} | {i} | {nm} | {c} planes')
for lab, ce in (('CE_A', ce_a), ('CE_B', ce_b)):
    seen_ = set()
    for i, nm, p in ce:
        sig = (i, tuple(p['disc_sizes']), tuple(p['fan_sizes']), p['crossed_faces'], json.dumps(p['edge_loops'], sort_keys=True))
        if sig in seen_: continue
        seen_.add(sig)
        print(f"{lab}-WHY {i} | plane {p['plane_float']} | discs {p['disc_sizes']} | fans {p['fan_sizes']} | crossed faces {p['crossed_faces']} | section components {p['components']} (crossed {p['crossed_components']}) | edge-only loops {p['edge_loops']}")
dd = [r for r in ncv if r['discs87']]
for r in dd:
    for p in r['planes']:
        if p['discs']: print(f"NCDISC {r['id']} | plane {p['plane_float']} | discs {p['disc_sizes']} | open fans {p['fan_sizes']} | crossed faces {p['crossed_faces']} | faces in plane {p['faces_in_plane']} | disc's section component made of edges only {[d['component_edge_only'] for d in p['disc_info']]}, disc = whole component {[d['component_is_disc'] for d in p['disc_info']]} | components {p['components']} (crossed {p['crossed_components']})")
sub_ = [(r['id'], p['plane_float']) for r in ncv for p in r['planes'] if not p['sheets_equal_runs']]
print(f'NONCONVEX planes where sheets differ from in-plane edge runs: {len(sub_)} (e.g. {sub_[:4]})')
for i in NAMED:
    r = B[i]; pl = [p for p in r['planes'] if p['fins_in_plane'] >= 3]
    tally = {}
    for p in pl: tally[(tuple(p['disc_sizes']), tuple(p['fan_sizes']), p['edge_closed'], p['fans_opposite'])] = tally.get((tuple(p['disc_sizes']), tuple(p['fan_sizes']), p['edge_closed'], p['fans_opposite']), 0) + 1
    print(f"NAMED {i} | {r['name']} | convex {r['convex']} | discs {r['disc_sizes87']} | planes >=3 edges by (discs, fans, edge-closed, fans opposite): {tally}")
summ = dict(solids=len(res), recognised=len(rec), valid_surface=len(val), convex=len(cvx), nonconvex=len(ncv),
            not_recognised=[r['id'] for r in res if not r['recognised']], invalid_surface=[r['id'] for r in rec if not (r['closed_surface'] and r['planar'])],
            nonconvex_law_holds=ok_n, ce_edge_closed_no_disc=len(ce_a), ce_disc_not_edge_closed=len(ce_b))
print('SUMMARY', json.dumps(summ))
for r in res: r.pop('planes_detail', None)
json.dump(dict(summary=summ, solids=res, checks=CHECKS), open(OUT, 'w'), indent=1, default=str)
nf = sum(1 for _, o in CHECKS if not o)
print(f'{len(CHECKS)} checks, {nf} failed, {time.time() - T0:.0f} s')
print('FINAL ok' if nf == 0 else f'FINAL FAIL ({nf} checks)')
