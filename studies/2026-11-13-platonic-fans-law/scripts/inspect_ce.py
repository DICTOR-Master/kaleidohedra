"""Follow-up to fans_law.py (13 Nov 2026): the structure of the edges in the counterexample planes, exact.
For the Sunstar tetrahedral cluster's 10 planes that cut no face but hold no disc, and the Admiral Cap's plane y = 0: fins in the plane,
edges through O in the plane, corner degrees (fins only, and all plane edges), number of connected pieces of the fin graph, and for each
piece whether it is a simple loop and its winding round O. Also: Hexa-Key, every central plane by type.
Usage: inspect_ce.py registry-solids.json fans-law.json"""
import sys, os, json, math, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'fans_law.py')).read()
# reuse the exact helpers and analyse() of fans_law.py without running its main part
head = src.split('\nres = []')[0]
REG, FANS = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], sys.argv[1], os.path.join(HERE, '..', '..', '2026-11-13-platonic-disc-ranking', 'data', 'disc-ranking.json'), '/dev/null'] + sys.argv[3:]
exec(head, globals())
S = {s['id']: s for s in json.load(open(REG))}
NCHK = [0]
def report(sid, want_planes=None):
    s = S[sid]; D, sc, N, raw, res_ = recog_solid(s['V']); QF.D = D
    V0 = [tuple(QF(a, b) for a, b in p) for p in raw]; n = len(V0)
    c = tuple(sum((p[i] for p in V0), QF(0)) / n for i in range(3)); V = [sub(p, c) for p in V0]; Vf = [tuple(float(x) for x in p) for p in V]
    E = edges_of(s['F'])
    through = {e for e in E if iszero(cr(V[e[0]], V[e[1]]))}
    planes = {}
    for e in E:
        if e in through: continue
        planes.setdefault(key(cr(V[e[0]], V[e[1]])), []).append(e)
    out = []
    for pk, fins in planes.items():
        nf = tuple(float(x) for x in pk)
        if want_planes is not None and not any(all(abs(nf[k] - w[k]) < 1e-5 for k in range(3)) for w in want_planes): continue
        sv = [fsgn(pk, nf, V[i], Vf[i]) for i in range(n)]
        thr = [e for e in through if sv[e[0]] == 0 and sv[e[1]] == 0]
        deg = {}; degall = {}
        for a, b in fins: deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
        for a, b in fins + thr: degall[a] = degall.get(a, 0) + 1; degall[b] = degall.get(b, 0) + 1
        par = {}
        def f2(x):
            while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a, b in fins: par[f2(a)] = f2(b)
        pieces = {}
        for a, b in fins: pieces.setdefault(f2(a), []).append((a, b))
        pinfo = []
        for pc in pieces.values():
            dg = {}
            for a, b in pc: dg[a] = dg.get(a, 0) + 1; dg[b] = dg.get(b, 0) + 1
            simple = all(d == 2 for d in dg.values()) and len(dg) == len(pc)
            w = None
            if simple:
                adj = {}
                for a, b in pc: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
                st = pc[0][0]; cyc = [st]; pv = None; cu = st
                while True:
                    nb = adj[cu]; nx = nb[0] if nb[0] != pv else nb[1]
                    if nx == st: break
                    cyc.append(nx); pv, cu = cu, nx
                w = loop_winding(cyc, V, pk)
            pinfo.append(dict(fins=len(pc), simple_loop=simple, winding_monotone=w, max_degree=max(dg.values())))
        hist = {}
        for v in deg.values(): hist[v] = hist.get(v, 0) + 1
        out.append(dict(plane=[round(x, 6) for x in nf], fins=len(fins), through_edges_in_plane=len(thr), fin_degree_histogram=dict(sorted(hist.items())),
                        corners_with_through_edge=sum(1 for v in deg if degall.get(v, 0) > deg[v]), pieces=sorted(pinfo, key=lambda d: -d['fins'])))
    return out
PH = (1 + math.sqrt(5)) / 2
print('== Sunstar tetrahedral cluster: planes x +- y +- z = 0 and the golden planes (1, phi^2, 0) family that cut no face')
d = json.load(open(FANS)); B = {r['id']: r for r in d['solids']}
want = [p['plane_float'] for p in B['DODECA_TETRAHEDRAL_CLUSTER']['planes'] if p['edge_closed'] and not p['discs']]
for r in report('DODECA_TETRAHEDRAL_CLUSTER', want): print('CE_A_DETAIL DODECA_TETRAHEDRAL_CLUSTER', json.dumps(r))
want = [p['plane_float'] for p in B['DICTO_EDGE_ROOF']['planes'] if p['edge_closed'] and not p['discs']]
for r in report('DICTO_EDGE_ROOF', want): print('CE_A_DETAIL DICTO_EDGE_ROOF', json.dumps(r))
print('PROGRESS 0.5 counterexample planes done', flush=True)
hk = B['DICTO_HEXA_KEY']['planes']; t = {}
for p in hk:
    k = (tuple(p['disc_sizes']), tuple(p['fan_sizes']), p['crossed_faces'] > 0, p['faces_in_plane'] > 0)
    t[k] = t.get(k, 0) + 1
for k, v in sorted(t.items(), key=lambda kv: -kv[1]): print(f'HEXAKEY_PLANES {v} planes | discs {k[0]} | fans {k[1]} | cuts faces {k[2]} | contains faces {k[3]}')
ok = len(want) == 1 and sum(t.values()) == len(hk)
print('PROGRESS 1.0 done', flush=True)
print('FINAL ok' if ok else 'FINAL FAIL')
