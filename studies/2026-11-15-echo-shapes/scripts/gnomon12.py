#!/usr/bin/env python3
"""Part C2, grown echoes beyond GET: can DICTO's gnomon (one whole zone layer added) grow GET into a k = 12 surface?
No seventh golden direction exists (six equiangular lines are the maximum in R^3, Lemmens-Seidel 1973), so a new zone must run
parallel to one of the six axes: cut the surface along a closed edge path that avoids direction a, shift one side by e_a, and close
the cut with a band of golden rhombi (d, a). A zone of direction d gains one face per path edge lying in it.
Counting lemma (proved in the README): starting from six zones of 10 and adding m parallel zones with paths P_1..P_m, all zones end
with k faces only if sum |P_i| = 3(k - 10) + m k / 2. For k = 12: m = 1 is impossible (the zone parallel to the new one would need
two edges of its own direction), and for m = 2 the paths are forced: |P_1| = 6 (two edges in each of three directions b, c, d, all
!= a), then P_2 along b with |P_2| = 12: six rungs of the new band, two a-edges of the old a-zone, two edges each of the two
directions e, f not yet used. This script enumerates that m = 2 case completely from GET A, GET B and candidate 2 (all paths,
both sides, all axis choices) and tests every result exactly (closed sphere, consistent orientation, every zone 12, embedding,
no coplanar adjacent faces, face pairs). Control: the same machinery on the triacontahedron with a 10-edge equator path gives the
expected profile. Usage: gnomon12.py out.json"""
import sys, os, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-grunbaum-k10', 'scripts'))
from zsurf import *        # exact golden-rhombus surfaces in Z^6 (GET study, 15 Nov 2026)
OUT = sys.argv[1] if len(sys.argv) > 1 else None; t0 = time.time(); FAILS = []
def check(c, msg):
    print(('CHECK ok   ' if c else 'CHECK FAIL ') + msg, flush=True)
    if not c: FAILS.append(msg)
G = Geo(6); N = 6

def fw_edge(f, s, e):
    """does face f with outward side s run along edge e = (q, d) from q to q + e_d (in its boundary orientation)?"""
    p, a, b = f; q, d = e
    if (q, d) == (p, a): fw = True
    elif (q, d) == (vadd(p, unit(N, a)), b): fw = True
    elif (q, d) == (vadd(p, unit(N, b)), a): fw = False
    elif (q, d) == (p, b): fw = False
    else: raise ValueError((f, e))
    return fw if s > 0 else not fw

def oriented_ok(S):
    use = {}
    for f, s in S.items():
        for e in edges_of(f, N):
            k = (e, fw_edge(f, s, e)); use[k] = use.get(k, 0) + 1
    return all(v == 1 for v in use.values()) and all((e, not d) in use for (e, d) in use)

def zone_of_edges(S):
    """map each edge (q, d) to a zone id (direction d, component)"""
    E = {}
    for f in S:
        for e in edges_of(f, N): E.setdefault(e, []).append(f)
    zid = {}; sizes = []; dirs = []
    for e0 in E:
        if e0 in zid: continue
        d = e0[1]; idx = len(sizes); st = [e0]; zid[e0] = idx; faces = set()
        while st:
            e = st.pop()
            for f in E[e]:
                faces.add(f); p, a, b = f; o = b if a == d else a
                for q in (p, vadd(p, unit(N, o))):
                    e2 = (q, d)
                    if e2 in E and e2 not in zid: zid[e2] = idx; st.append(e2)
        sizes.append(len(faces)); dirs.append(d)
    return zid, sizes, dirs

def cycles(S, avoid, need, zid=None, zneed=None, maxlen=None):
    """simple closed edge paths using exactly need[d] edges of each direction d (balanced senses), none of direction avoid;
    optional zneed: exact number of path edges in given zones"""
    L = sum(need.values()); adj = {}
    for f in S:
        for (q, d) in edges_of(f, N):
            if d == avoid or need.get(d, 0) == 0: continue
            r = vadd(q, unit(N, d))
            adj.setdefault(q, set()).add((r, (q, d), d, +1)); adj.setdefault(r, set()).add((q, (q, d), d, -1))
    found = set(); res = []
    verts = sorted(adj)
    for v0 in verts:
        st = [(v0, (v0,), (), {}, {}, {})]
        while st:
            v, path, es, cnt, bal, zc = st.pop()
            for (w, e, d, sg) in adj[v]:
                if cnt.get(d, 0) >= need[d]: continue
                nb = bal.get(d, 0) + sg
                if abs(nb) > need[d] - cnt.get(d, 0) - 1: continue      # must be able to rebalance
                z2 = zc
                if zneed is not None:
                    z = zid[e]
                    if zc.get(z, 0) + 1 > zneed.get(z, 0): continue
                    z2 = dict(zc); z2[z] = zc.get(z, 0) + 1
                if w == v0 and len(es) == L - 1:
                    key = frozenset(es + (e,))
                    if key not in found: found.add(key); res.append(list(es + (e,)))
                    continue
                if w in path or w < v0 or len(es) >= L - 1: continue
                c2 = dict(cnt); c2[d] = cnt.get(d, 0) + 1; b2 = dict(bal); b2[d] = nb
                st.append((w, path + (w,), es + (e,), c2, b2, z2))
    return res

def insert_par(S, cyc, a, shift_A):
    E = {}
    for f in S:
        for e in edges_of(f, N): E.setdefault(e, []).append(f)
    cut = set(cyc); f0 = next(iter(S)); A = {f0}; st = [f0]
    while st:
        f = st.pop()
        for e in edges_of(f, N):
            if e in cut: continue
            for g in E[e]:
                if g not in A: A.add(g); st.append(g)
    if len(A) == len(S): return None
    if not shift_A: A = set(S) - A
    B = set(S) - A; T = {}
    for f, s in S.items():
        p = f[0]
        if f in A: p = vadd(p, unit(N, a))
        T[(p, f[1], f[2])] = s
    for e in cyc:
        q, d = e; h = [g for g in E[e] if g in B][0]
        fw = fw_edge(h, S[h], e)
        s = -1 if fw else 1           # band face (q; d, a), normal e_d x e_a
        if d < a: key = (q, d, a)
        else: key = (q, a, d); s = -s
        if key in T: return None      # band face lands on an existing face
        T[key] = s
    return T

def full_tests(S):
    info, why = analyse(G, S)
    if info is None: return {'ok': False, 'why': why}
    if not oriented_ok(S): return {'ok': False, 'why': 'orientation'}
    zid, sizes, dirs = zone_of_edges(S)
    r = {'ok': True, 'F': len(S), 'zones': sorted(zip(dirs, sizes)), 'coplanar_adjacent': info['coplanar_adjacent']}
    return r

def embedded_partial_n(G, S):
    """exact necessary embedding test (as in the GET study's gnomon.py): faces with no common lattice vertex must be strictly apart"""
    fl = list(S); cs = [set(corners(f, G.n)) for f in fl]
    for i in range(len(fl)):
        for j in range(i + 1, len(fl)):
            if cs[i] & cs[j]: continue
            if G.relation(fl[i][0], (fl[i][1], fl[i][2]), fl[j][0], (fl[j][1], fl[j][2])) != 'apart': return False
    return True

def face_pairs_balanced(S):
    c = {}
    for (p, a, b), s in S.items(): c[(a, b, s)] = c.get((a, b, s), 0) + 1
    return all(c.get((a, b, 1), 0) == c.get((a, b, -1), 0) for (a, b, s) in c)

def cycles_cap(S, avoid, cap, zid, Lmin, Lmax, limit=None):
    """all simple closed edge paths of even length Lmin..Lmax avoiding direction avoid, with at most cap[zone] edges in each zone"""
    adj = {}
    for f in S:
        for (q, d) in edges_of(f, N):
            if d == avoid or cap.get(zid[(q, d)], 0) <= 0: continue
            r = vadd(q, unit(N, d))
            adj.setdefault(q, set()).add((r, (q, d), d, +1)); adj.setdefault(r, set()).add((q, (q, d), d, -1))
    found = set(); res = []
    for v0 in sorted(adj):
        st = [(v0, (v0,), (), {}, {})]
        while st:
            v, path, es, zc, bal = st.pop()
            for (w, e, d, sg) in adj[v]:
                z = zid[e]
                if zc.get(z, 0) + 1 > cap[z]: continue
                nb = bal.get(d, 0) + sg
                L = len(es) + 1
                if w == v0:
                    if Lmin <= L <= Lmax and L % 2 == 0:
                        key = frozenset(es + (e,))
                        if key not in found: found.add(key); res.append(list(es + (e,)))
                    continue
                if w in path or w < v0 or L >= Lmax: continue
                if sum(abs(x) for x in {**bal, d: nb}.values()) > Lmax - L: continue
                z2 = dict(zc); z2[z] = zc.get(z, 0) + 1; b2 = dict(bal); b2[d] = nb
                st.append((w, path + (w,), es + (e,), z2, b2))
            if limit and len(res) > limit: return res, True
    return res, False

def general_search(starts, K, M, budget_s):
    """all sequences of m <= M parallel-band insertions from the starts, every zone kept <= K, ending with every zone = K;
    deficit rule D' = D + K - 2L prunes (D = sum of (K - zone size)). Surfaces are deduplicated up to translation."""
    tstart = time.time(); st = {'nodes': 0, 'paths': 0, 'valid': 0, 'hits': 0, 'capped': False}; hits = []
    level = [(nm, S, 0) for nm, S in starts.items()]
    for depth in range(M):
        nxt = {}; r_after = M - depth - 1
        for li, (nm, S, _) in enumerate(level):
            if li % 200 == 0: print(f'PROGRESS {(depth + li/len(level))/M:.4f} K={K} depth {depth + 1} surface {li}/{len(level)} stats {st}', flush=True)
            zid, sizes, dirs = zone_of_edges(S)
            if any(x > K for x in sizes): continue
            D = sum(K - x for x in sizes)
            cap = {i: K - sizes[i] for i in range(len(sizes))}
            for a in range(6):
                if time.time() - tstart > budget_s: st['capped'] = True; break
                Lmin = max(4, (D + K - r_after*K + 1)//2 if r_after == 0 else 4)
                paths, capped = cycles_cap(S, a, cap, zid, 4, K, limit=200000)
                if capped: st['capped'] = True
                for P in paths:
                    L = len(P); D2 = D + K - 2*L
                    if D2 < 0 or D2 > r_after*K or (r_after == 0 and D2 != 0): continue
                    st['paths'] += 1
                    for side in (True, False):
                        T = insert_par(S, P, a, side)
                        if T is None: continue
                        st['nodes'] += 1
                        t = full_tests(T)
                        if not t['ok']: continue
                        st['valid'] += 1
                        if all(x[1] == K for x in t['zones']):
                            st['hits'] += 1
                            fb = face_pairs_balanced(T); nc = t['coplanar_adjacent'] == 0
                            st['hits_noncoplanar'] = st.get('hits_noncoplanar', 0) + nc
                            st['hits_balanced'] = st.get('hits_balanced', 0) + fb
                            if nc and fb:
                                emb = embedded_partial_n(G, T)
                                st['hits_strong_embedded'] = st.get('hits_strong_embedded', 0) + emb
                                if emb:
                                    hits.append({'start': nm, 'depth': depth + 1, 'zones': t['zones'],
                                                 'faces': [[list(p), x, y, s] for (p, x, y), s in T.items()]})
                        elif r_after > 0:
                            key = canon_t(T)
                            if key not in nxt: nxt[key] = (nm, T, depth + 1)
        level = list(nxt.values())
        print(f'PROGRESS {(depth + 1)/M:.3f} K={K} depth {depth + 1}: {len(level)} surfaces to extend, stats {st}', flush=True)
        if st['capped']: break
    st['seconds'] = time.time() - tstart
    return st, hits

def main():
    D = json.load(open(os.path.join(HERE, '..', '..', '2026-11-15-grunbaum-k10', 'data', 'search6.json')))
    starts = {}
    for idx, nm in ((0, 'GET A'), (1, 'GET B'), (2, 'candidate 2')):
        S = {(tuple(p), a, b): s for p, a, b, s in D['candidates_rank_le_3'][idx]['faces']}
        starts[nm] = S
        t = full_tests(S); check(t['ok'] and t['zones'] == [(d, 10) for d in range(6)], f'{nm}: closed sphere, oriented, six zones of 10')
    # control: triacontahedron, parallel zone along axis 0 through a 10-edge path avoiding direction 0 (a zone equator of axis 0)
    TRI = zonotope(G)
    cyc = cycles(TRI, 0, {d: 2 for d in range(1, 6)})
    good = 0; prof = set()
    for c in cyc:
        for side in (True, False):
            T = insert_par(TRI, c, 0, side)
            if T is None: continue
            t = full_tests(T)
            if t['ok']: good += 1; prof.add(tuple(sorted(x[1] for x in t['zones'])))
    check(good > 0 and prof == {(10, 10, 12, 12, 12, 12, 12)}, f'control: triacontahedron + one parallel zone: {good} results, zone profiles {sorted(prof)} (predicted 10,10,12x5)')
    stats = {'step1_paths': 0, 'step1_surfaces': 0, 'step1_valid': 0, 'step2_paths': 0, 'step2_surfaces': 0, 'step2_valid': 0,
             'all_zones_12': 0, 'embedded': 0, 'noncoplanar': 0, 'face_pairs_balanced': 0}
    found = []; jobs = [(nm, a, b) for nm in starts for a in range(6) for b in range(6) if b != a]
    for jn, (nm, a, b) in enumerate(jobs):
        S0 = starts[nm]
        others = [d for d in range(6) if d not in (a, b)]
        for c, d in itertools.combinations(others, 2):
            need1 = {b: 2, c: 2, d: 2}
            for P1 in cycles(S0, a, need1):
                stats['step1_paths'] += 1
                for side1 in (True, False):
                    S1 = insert_par(S0, P1, a, side1)
                    if S1 is None: continue
                    stats['step1_surfaces'] += 1
                    t1 = full_tests(S1)
                    if not t1['ok']: continue
                    stats['step1_valid'] += 1
                    zid, sizes, dirs = zone_of_edges(S1)
                    # zones: the old a-zone has 10 faces, the new band a' has 6
                    za_new = [i for i in range(len(sizes)) if dirs[i] == a and sizes[i] == 6]
                    za_old = [i for i in range(len(sizes)) if dirs[i] == a and sizes[i] == 10]
                    if len(za_new) != 1 or len(za_old) != 1: continue
                    e_, f_ = [x for x in range(6) if x not in (a, b, c, d)]
                    ze = [i for i in range(len(sizes)) if dirs[i] == e_]; zf = [i for i in range(len(sizes)) if dirs[i] == f_]
                    zneed = {za_new[0]: 6, za_old[0]: 2, ze[0]: 2, zf[0]: 2}
                    # diagnostic (first surfaces of each job only, for cost): the same direction counts without the zone split
                    if stats.get('diag_done', 0) < (jn + 1)*3:
                        stats['diag_done'] = stats.get('diag_done', 0) + 1
                        stats['diag_paths_dir_counts_only'] = stats.get('diag_paths_dir_counts_only', 0) + len(cycles(S1, b, {a: 8, e_: 2, f_: 2}))
                        stats['diag_paths_a6ef'] = stats.get('diag_paths_a6ef', 0) + len(cycles(S1, b, {a: 6, e_: 2, f_: 2}))
                        stats['diag_paths_a4ef'] = stats.get('diag_paths_a4ef', 0) + len(cycles(S1, b, {a: 4, e_: 2, f_: 2}))
                    for P2 in cycles(S1, b, {a: 8, e_: 2, f_: 2}, zid=zid, zneed=zneed):
                        stats['step2_paths'] += 1
                        for side2 in (True, False):
                            S2 = insert_par(S1, P2, b, side2)
                            if S2 is None: continue
                            stats['step2_surfaces'] += 1
                            t2 = full_tests(S2)
                            if not t2['ok']: continue
                            stats['step2_valid'] += 1
                            if any(x[1] != 12 for x in t2['zones']): continue
                            stats['all_zones_12'] += 1
                            emb = embedded_partial_n(G, S2)
                            if not emb: continue
                            stats['embedded'] += 1
                            if t2['coplanar_adjacent'] == 0: stats['noncoplanar'] += 1
                            fb = face_pairs_balanced(S2)
                            if fb: stats['face_pairs_balanced'] += 1
                            found.append({'start': nm, 'a': a, 'b': b, 'P1': [[list(q), dd] for q, dd in P1], 'P2': [[list(q), dd] for q, dd in P2],
                                          'sides': [side1, side2], 'coplanar_adjacent': t2['coplanar_adjacent'], 'face_pairs_balanced': fb,
                                          'faces': [[list(p), x, y, s] for (p, x, y), s in S2.items()]})
        print(f'PROGRESS {(jn + 1)/len(jobs):.3f} {nm} a={a} b={b} stats {stats}', flush=True)
    G12 = int(os.environ.get('GEN_M12', '3')); G14 = int(os.environ.get('GEN_M14', '2')); BUD = float(os.environ.get('GEN_BUDGET', '3000'))
    gen12 = general_search(starts, 12, G12, BUD); print(f'GENERAL K=12 M={G12}: {gen12[0]}', flush=True)
    gen14 = general_search(starts, 14, G14, BUD); print(f'GENERAL K=14 M={G14}: {gen14[0]}', flush=True)
    json.dump({'stats': stats, 'k12_surfaces': found, 'general_k12': {'M': G12, 'stats': gen12[0], 'hits': gen12[1]},
               'general_k14': {'M': G14, 'stats': gen14[0], 'hits': gen14[1]}, 'fails': FAILS, 'seconds': time.time() - t0}, open(OUT, 'w'), indent=1)
    print(f'RESULT {stats}; {len(found)} embedded k = 12 surfaces; {time.time() - t0:.0f} s')
    print('FINAL ok' if not FAILS else 'FINAL FAIL')

if __name__ == '__main__': main()
