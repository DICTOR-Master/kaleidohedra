# DICTO · dictospheres.com — exact checks for the paper on Grünbaum's zone question at k = 10, from the data of
# studies/2026-11-15-grunbaum-k10 (tile12.json: cells and lattice of GET A and GET B; search6.json: their faces and the
# faces of candidate 2, the Hall/Inchbald solid). Everything in Z[φ] (integer pairs) or Z^6; no floats. Each fact is an
# assert, and the values go to ../data/get-exact.json for the audit and the figures.
#   1. the 16 cells of each solid: their union's boundary is exactly the 30 faces of search6.json;
#   2. the surface: F, V, E, χ = 2, closed, every vertex link one cycle, adjacent normals at 36°, 72° or 108°, none coplanar;
#   3. one face shape: |e|² = φ + 2, diagonals 2 and 2φ, for all 15 axis pairs;
#   4. zones: six, each one cycle of 10 faces; two faces of each of the 15 pair types (every two zones cross twice);
#   5. cells: 10 prolate and 6 oblate; types: 16 of 20, missing 015, 023, 124, 345, each axis in two of them;
#   6. volume = covolume = 20 + 32φ; the face-pair vectors λ lie in the lattice and generate it (index 1); 14 neighbours;
#   7. the triacontahedron T (zonotope of the six axes): 30 faces, 20 + 12 corners, zones of 10, volume 40 + 64φ … found
#      exactly as GET ∪ four oblate cells; the four removed cells and the four dimpled corners of T;
#   8. the 120 symmetries of the star; symmetries of A (2 + 2), B (3 + 0), candidate 2 (12 + 0); no map A -> B or its mirror.
import json, os, itertools
from math import gcd
from getlib import *

LOG = []
def log(s): LOG.append(s); print(s)

S6, T12 = load()
cands = S6['candidates_rank_le_3']
res = {r['index']: r for r in T12['results']}
B = res[0]['basis']; assert res[1]['basis'] == B
out = {'basis': B}
names = {0: 'GET A', 1: 'GET B', 2: 'candidate 2'}

# ---------- T, the rhombic triacontahedron ----------
TF = {}
for a, b in PAIRS:
    plus = [0] * N; minus = [0] * N
    for c in range(N):
        if c in (a, b): continue
        (plus if sgn(D[(a, b, c)]) > 0 else minus)[c] = 1
    TF[(tuple(plus), a, b)] = 1; TF[(tuple(minus), a, b)] = -1
Tst = surface_stats(TF); Tz = zones(TF)
assert Tst['F'] == 30 and Tst['V'] == 32 and Tst['E'] == 60 and Tst['chi'] == 2 and Tst['closed']
assert all(Tz[d][0] == 10 and Tz[d][1] for d in range(N))
vols = sorted({cell_volume(t) for t in TRIPLES}, key=flt)
assert len(vols) == 2
OBL, PRO = vols                                          # the oblate cell has the smaller volume
nP = sum(cell_volume(t) == PRO for t in TRIPLES); nO = 20 - nP
assert nP == 10 and nO == 10
volT = (0, 0)
for t in TRIPLES: volT = add(volT, cell_volume(t))
log(f'T: F, V, E = 30, 32, 60; corners of valence {Tst["valence"]}; six zones of 10; 20 cell types, 10 prolate (volume {zstr(PRO)}) and 10 oblate ({zstr(OBL)}); volume {zstr(volT)}')
out['T'] = {'F': 30, 'V': 32, 'E': 60, 'prolate_volume': PRO, 'oblate_volume': OBL, 'volume': volT}

# ---------- the face shape ----------
e2 = vdot(AX[0], AX[0]); assert all(vdot(e, e) == e2 for e in AX) and e2 == (2, 1)       # φ + 2
for a, b in PAIRS:
    d1 = vdot(vadd(AX[a], AX[b]), vadd(AX[a], AX[b])); d2 = vdot(vadd(AX[a], vscale(-1, AX[b])), vadd(AX[a], vscale(-1, AX[b])))
    assert sorted([d1, d2], key=flt) == [(4, 0), (4, 4)], (a, b, d1, d2)                  # 4 and 4φ² = 4 + 4φ: diagonals 2 and 2φ
assert all(sgn(D[t]) != 0 for t in TRIPLES)                                               # any three axes are independent
log('one face shape: side² = φ + 2, diagonals 2 and 2φ, for all 15 pairs of axes; any three axes independent')

G = symmetries(); assert len(G) == 120 and sum(g[2] > 0 for g in G) == 60
log('symmetries of the six-axis star: 120 (60 rotations)')

solids = {}
for idx in (0, 1, 2):
    Fo = faces_from_json(cands[idx]['faces']); assert len(Fo) == 30
    r = {}
    if idx in (0, 1):
        cells = [(tuple(p), tuple(t)) for p, t in res[idx]['cells']]
        assert len(cells) == 16 and boundary(cells) == Fo, f'{names[idx]}: cells do not give the faces'
        types = sorted(''.join(map(str, t)) for _, t in cells)
        assert types == res[idx]['cell_types'] and len(set(types)) == 16
        missing = sorted(set(''.join(map(str, t)) for t in TRIPLES) - set(types))
        assert missing == ['015', '023', '124', '345']
        assert all(sum(str(i) in m for m in missing) == 2 for i in range(N))
        assert all(cell_volume(tuple(map(int, m))) == OBL for m in missing)
        np_ = sum(cell_volume(t) == PRO for _, t in cells); no_ = 16 - np_
        assert (np_, no_) == (10, 6)
        vol = (0, 0)
        for _, t in cells: vol = add(vol, cell_volume(t))
        cov = covolume(B); assert vol == cov == (20, 32) == tuple(res[idx]['det'])
        assert vol == sub(volT, mul((4, 0), OBL))
        r.update(cells=[[list(p), list(t)] for p, t in cells], cell_types=types, missing=missing, prolate=np_, oblate=no_, volume=vol, covolume=cov)
    st = surface_stats(Fo); z = zones(Fo)
    assert (st['F'], st['V'], st['E'], st['chi']) == (30, 32, 60, 2) and st['closed'] and st['vertex_links_one_cycle']
    assert st['coplanar_adjacent'] == 0 and set(st['normal_angles']) <= {36, 72, 108}
    assert all(z[d][0] == 10 and z[d][1] for d in range(N))
    assert all(sum((f[1], f[2]) == pr for f in Fo) == 2 for pr in PAIRS)
    lam = face_pair_vectors(Fo); co = {}
    for pr, v in lam.items():
        c = lattice_member(B, v); assert c is not None, (names[idx], pr, v); co[pr] = c
    minors = [abs(x[0] * (y[1] * w[2] - y[2] * w[1]) - x[1] * (y[0] * w[2] - y[2] * w[0]) + x[2] * (y[0] * w[1] - y[1] * w[0]))
              for x, y, w in itertools.combinations(list(co.values()), 3)]
    ind = 0
    for m in minors: ind = gcd(ind, m)
    nb = {tuple(v) for v in lam.values()} | {tuple(-c for c in v) for v in lam.values()}
    r.update(stats=st, zones=[z[d][0] for d in range(N)], lambda_index=ind, neighbours=len(nb), neighbour_vectors=sorted(nb))
    # T + t contains it: 18 faces of T kept, 12 dimple faces
    best = None
    for f, s in Fo.items():
        for g, s2 in TF.items():
            if f[1:] == g[1:] and s == s2:
                t = psub(f[0], g[0]); k = sum(((padd(q, t), a, b) in Fo and Fo[(padd(q, t), a, b)] == s3) for (q, a, b), s3 in TF.items())
                if best is None or k > best[0]: best = (k, t)
    kept, t = best; assert kept == 18
    TFt = {(padd(q, t), a, b): s for (q, a, b), s in TF.items()}
    R = dict(TFt)
    for f, s in Fo.items():
        R[f] = R.get(f, 0) - s
    R = {f: s for f, s in R.items() if s}
    assert len(R) == 24                                   # 12 faces of T removed + 12 dimple faces (reversed)
    pts = {c for f in R for c in corners(*f)}
    rem = []
    for tt in TRIPLES:
        if cell_volume(tt) != OBL: continue
        for p in pts:
            cf = cell_faces(p, tt)
            if all(R.get(f) == s for f, s in cf.items()): rem.append((p, tt))
    assert len(rem) == 4 and boundary(rem) == R, (names[idx], rem)
    # the dimpled corners of T: the corner of each removed cell where its three faces on T meet
    dim = []
    for p, tt in rem:
        on = [f for f in cell_faces(p, tt) if f in TFt]
        assert len(on) == 3
        c = set(corners(*on[0])) & set(corners(*on[1])) & set(corners(*on[2])); assert len(c) == 1
        dim.append(c.pop())
    d2 = sorted(vdot(*(2 * [pos(psub(a, b))])) for a, b in itertools.combinations(dim, 2))
    r.update(T_shift=list(t), removed=[[list(p), list(tt)] for p, tt in rem], removed_types=sorted(''.join(map(str, tt)) for _, tt in rem),
             dimples=[list(c) for c in dim], dimple_dist2=d2)
    if idx == 2:
        r['missing'] = r['removed_types']
    solids[idx] = (Fo, r)
    log(f'{names[idx]}: F, V, E = 30, 32, 60, χ = 2, closed, vertex links one cycle; zones {r["zones"]}; adjacent normals at {st["normal_angles"]}°, '
        f'coplanar adjacent 0; λ in the lattice, index {ind}; {len(nb)} face neighbours; T + t keeps 18 faces; removed cells {r["removed_types"]}; '
        f'dimple distances² {[zstr(x) for x in d2]}' + (f'; cells 10 prolate + 6 oblate, volume = covolume = {zstr(r["volume"])}' if idx < 2 else ''))
    out[names[idx]] = r

# the three removed sets of cell types: A and B remove the same four types; candidate 2 removes four oblate types too
assert solids[0][1]['removed_types'] == solids[1][1]['removed_types'] == ['015', '023', '124', '345']
out['candidate 2']['removed_types_note'] = 'types of the four removed oblate cells'
# the 20 three-valent corners of T: are the dimples of each solid on T's three-valent corners?
TV = {c for f in TF for c in corners(*f)}
val = {v: sum(v in corners(*f) for f in TF) for v in TV}
assert sorted(val.values()).count(3) == 20 and sorted(val.values()).count(5) == 12
for idx in (0, 1, 2):
    t = solids[idx][1]['T_shift']
    assert all(val[psub(tuple(c), tuple(t))] == 3 for c in solids[idx][1]['dimples'])
# the five cubes inscribed in T (8 three-valent corners each, edge² = 4 + 4φ): which cube holds the four dimples?
C3 = sorted(v for v in TV if val[v] == 3)
d2 = {(u, v): vdot(pos(psub(u, v)), pos(psub(u, v))) for u in C3 for v in C3}
s2 = (4, 4)
cubes = []
for S in itertools.combinations(C3, 8):
    ds = sorted((d2[(u, v)] for u, v in itertools.combinations(S, 2)), key=flt)
    if ds == [s2] * 12 + [(8, 8)] * 12 + [(12, 12)] * 4: cubes.append(frozenset(S))
assert len(cubes) == 5 and all(sum(v in c for c in cubes) == 2 for v in C3)
kinds = {}
for idx in (0, 1, 2):
    t = solids[idx][1]['T_shift']; dm = [psub(tuple(c), tuple(t)) for c in solids[idx][1]['dimples']]
    hold = [c for c in cubes if all(v in c for v in dm)]
    assert len(hold) == 1, names[idx]
    cube = hold[0]; e = sum(d2[(u, v)] == s2 for u, v in itertools.combinations(dm, 2))
    deg = sorted(sum(d2[(u, v)] == s2 for v in dm if v != u) for u in dm)
    kind = {(4, (2, 2, 2, 2)): 'the four corners of a square face of the cube', (3, (1, 1, 1, 3)): 'a corner of the cube and its three neighbours on it',
            (0, (0, 0, 0, 0)): 'four alternate corners of the cube (a regular tetrahedron)'}[(e, tuple(deg))]
    kinds[names[idx]] = kind; out[names[idx]]['dimple_kind'] = kind
    out[names[idx]]['cube'] = sorted(list(padd(v, tuple(t))) for v in cube)
assert out['GET A']['cube'] == out['GET B']['cube'] == out['candidate 2']['cube']
assert all(solids[i][1]['T_shift'] == [0] * 6 for i in (0, 1, 2))
RM = {i: {(tuple(p), tuple(t)) for p, t in solids[i][1]['removed']} for i in (0, 1, 2)}
shared = {'GET A, GET B': len(RM[0] & RM[1]), 'GET B, candidate 2': len(RM[1] & RM[2]), 'GET A, candidate 2': len(RM[0] & RM[2])}
assert shared == {'GET A, GET B': 3, 'GET B, candidate 2': 3, 'GET A, candidate 2': 2}
out['shared_removed_cells'] = shared
log(f'in the search frame the three solids are indentations of one copy of T, their dimples on one inscribed cube; removed cells in common: {shared}')
log(f'T has 5 inscribed cubes on its 20 three-valent corners; the four dimpled corners lie on one cube for each solid: {kinds}')

# ---------- symmetry and congruence ----------
U = {i: [f for f in solids[i][0]] for i in (0, 1, 2)}
sym = {names[i]: congruences(U[i], U[i], G) for i in (0, 1, 2)}
assert sym == {'GET A': (2, 2), 'GET B': (3, 0), 'candidate 2': (12, 0)}, sym
cong = {f'{names[i]} -> {names[j]}': congruences(U[i], U[j], G) for i, j in [(0, 1), (0, 2), (1, 2)]}
assert all(v == (0, 0) for v in cong.values()), cong
out['symmetries'] = {k: list(v) for k, v in sym.items()}; out['congruences'] = {k: list(v) for k, v in cong.items()}
log(f'symmetries (rotations, reflections): {sym}; maps between the three solids, either hand: {cong}')

# cross-check with the Hall study (exact corner matching there)
H = json.load(open(os.path.join(STUDIES, '2026-11-20-hall-2016-check', 'data', 'hall_check.json')))
for h in H['hall']:
    assert h['sym_proper'] == 12 and h['sym_improper'] == 0
    assert h['candidate 0 = GET A'] == {'same_hand_maps': 0, 'mirror_maps': 0} and h['candidate 1 = GET B'] == {'same_hand_maps': 0, 'mirror_maps': 0}
    assert sum(h['candidate 2 (Inchbald)'].values()) == 12
log("Hall's solid (10 corner sets, study 2026-11-20-hall-2016-check): 12 symmetries, all rotations; = candidate 2 in one hand or the other; never GET A or GET B (agrees)")

json.dump(out, open(os.path.join(HERE, '..', 'data', 'get-exact.json'), 'w'), indent=1, default=list)
open(os.path.join(HERE, '..', 'data', 'get-exact.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n')
print('FINAL ok')
