#!/usr/bin/env python3
"""D. Hall's Dimpled Rhombic Triacontahedron (Sketchfab, 28 June 2016) against candidate 2 (Inchbald's solid), GET A and GET B.
Exact throughout: numbers in Q(phi) as Fraction pairs (x, y) = x + y*phi.
1. Hall's solid from his own description: the rhombic triacontahedron T (the zonotope of the six 5-fold axes); at each of four
   vertices with tetrahedral symmetry remove one golden rhombohedron. Every 4-set of vertices of T forming a regular tetrahedron
   centred at T's centre is tried (the description does not fix which set, so all are built).
2. Candidates 0 (GET A), 1 (GET B), 2 (Inchbald) from the face form of study 2026-11-15-grunbaum-k10 (data/search6.json).
3. House congruence test (corner matching): every orthogonal map M (det +1 or -1) taking three independent vertices of X to
   three vertices of Y with equal inner products, checked to map the whole vertex set and the whole face set of X onto Y.
   Solids are centred at their vertex centroid. Counts: proper maps (same hand) and improper maps (mirror hand).
Usage: hall_check.py <grunbaum-k10 dir> <out json>"""
import sys, json, itertools
from fractions import Fraction as Fr

def q(x, y=0): return (Fr(x), Fr(y))
def add(u, v): return (u[0] + v[0], u[1] + v[1])
def sub(u, v): return (u[0] - v[0], u[1] - v[1])
def mul(u, v): return (u[0]*v[0] + u[1]*v[1], u[0]*v[1] + u[1]*v[0] + u[1]*v[1])
def conj(u): return (u[0] + u[1], -u[1])
def norm(u): return mul(u, conj(u))[0]          # rational
def inv(u):
    c = conj(u); n = norm(u); return (c[0]/n, c[1]/n)
Z = q(0); ONE = q(1)
def vadd(a, b): return tuple(add(x, y) for x, y in zip(a, b))
def vsub(a, b): return tuple(sub(x, y) for x, y in zip(a, b))
def vneg(a): return tuple(sub(Z, x) for x in a)
def vscale(s, a): return tuple(mul(s, x) for x in a)
def dot(a, b):
    r = Z
    for x, y in zip(a, b): r = add(r, mul(x, y))
    return r
def cross(a, b): return (sub(mul(a[1], b[2]), mul(a[2], b[1])), sub(mul(a[2], b[0]), mul(a[0], b[2])), sub(mul(a[0], b[1]), mul(a[1], b[0])))
def det3(a, b, c): return dot(a, cross(b, c))

AX = [(q(1), q(0, 1), q(0)), (q(-1), q(0, 1), q(0)), (q(0), q(1), q(0, 1)), (q(0), q(-1), q(0, 1)), (q(0, 1), q(0), q(1)), (q(0, -1), q(0), q(1))]

def tri_T():
    """T as a face list: rhombus faces as 4-tuples of exact points (cyclic order)"""
    faces = []
    for a, b in itertools.combinations(range(6), 2):
        nrm = cross(AX[a], AX[b])
        base_hi = (Z, Z, Z); base_lo = (Z, Z, Z)
        for c in range(6):
            if c in (a, b): continue
            if sgn(dot(AX[c], nrm)) > 0: base_hi = vadd(base_hi, AX[c])
            else: base_lo = vadd(base_lo, AX[c])
        for p in (base_hi, base_lo):
            faces.append((p, vadd(p, AX[a]), vadd(vadd(p, AX[a]), AX[b]), vadd(p, AX[b])))
    return faces

def sgn(u):
    x, y = u; a, b = 2*x + y, y
    if a >= 0 and b >= 0: return 0 if a == 0 and b == 0 else 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a*a > 5*b*b else (1 if b > 0 else -1)

def verts_of(faces):
    V = []
    for f in faces:
        for v in f:
            if v not in V: V.append(v)
    return V

def euler(faces):
    V = verts_of(faces); E = set()
    for f in faces:
        for i in range(4): E.add(frozenset((f[i], f[(i+1) % 4])))
    return len(faces), len(V), len(E)

def remove_rhombohedron(faces, v):
    """v a 3-valent vertex: the three faces at v span the rhombohedron v + [0,1]u1 + [0,1]u2 + [0,1]u3 (u_i the edges at v).
    Remove it: the three faces at v are replaced by the three faces at v' = v + u1 + u2 + u3."""
    at = [f for f in faces if v in f]
    assert len(at) == 3, 'not 3-valent'
    us = set()
    for f in at:
        i = f.index(v)
        for w in (f[(i+1) % 4], f[(i-1) % 4]): us.add(vsub(w, v))
    us = list(us); assert len(us) == 3
    vp = vadd(vadd(vadd(v, us[0]), us[1]), us[2])
    new = [f for f in faces if v not in f]
    for i, j in itertools.combinations(range(3), 2):
        k = 3 - i - j
        p = vadd(v, us[k])
        new.append((p, vadd(p, us[i]), vadd(vadd(p, us[i]), us[j]), vadd(p, us[j])))
    return new, vp

def cand_faces(c):
    out = []
    for p, a, b, s in c['faces']:
        P = (Z, Z, Z)
        for i, m in enumerate(p): P = vadd(P, vscale(q(m), AX[i]))
        out.append((P, vadd(P, AX[a]), vadd(vadd(P, AX[a]), AX[b]), vadd(P, AX[b])))
    return out

def centred(faces):
    V = verts_of(faces); n = q(len(V))
    c = (Z, Z, Z)
    for v in V: c = vadd(c, v)
    c = vscale(inv(n), c)
    F = [tuple(vsub(v, c) for v in f) for f in faces]
    return F

def matinv(A):
    """inverse of 3x3 (rows) over Q(phi)"""
    d = det3(A[0], A[1], A[2]); di = inv(d)
    cols = [cross(A[1], A[2]), cross(A[2], A[0]), cross(A[0], A[1])]   # A^{-1} columns = these / d
    return [[mul(cols[j][i], di) for j in range(3)] for i in range(3)]

def congruences(FX, FY):
    """list of det signs of all orthogonal maps M with M(X) = Y (vertex sets and face sets)"""
    VX, VY = verts_of(FX), verts_of(FY)
    if len(VX) != len(VY) or len(FX) != len(FY): return []
    setY = set(VY)
    facesY = set(frozenset(f) for f in FY)
    # three independent vertices of X
    for tr in itertools.combinations(VX, 3):
        if det3(*tr) != Z: x = tr; break
    G = [[dot(a, b) for b in x] for a in x]
    Xi = matinv([list(r) for r in x])          # rows x_i; M x_i = y_i  =>  M = Y^T (X^T)^{-1}
    res = []
    for y in itertools.permutations(VY, 3):
        if any(dot(y[i], y[j]) != G[i][j] for i in range(3) for j in range(i, 3)): continue
        # M = sum_i y_i (row i of (X^T)^{-1})^T ; (X^T)^{-1} = (X^{-1})^T, so M[r][c] = sum_i y_i[r] * Xi[c][i]
        M = [[Z]*3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                s = Z
                for i in range(3): s = add(s, mul(y[i][r], Xi[c][i]))
                M[r][c] = s
        # orthogonal?
        ok = all(dot([M[k][a] for k in range(3)], [M[k][b] for k in range(3)]) == (ONE if a == b else Z) for a in range(3) for b in range(a, 3))
        if not ok: continue
        ap = lambda v: tuple(dot(M[r], v) for r in range(3))
        img = {v: ap(v) for v in VX}
        if set(img.values()) != setY: continue
        if set(frozenset(img[v] for v in f) for f in FX) != facesY: continue
        d = det3(*[[M[k][c] for k in range(3)] for c in range(3)])
        res.append(1 if d == ONE else -1)
    return res

def main(K10, OUT):
    T = tri_T()
    print('T: F, V, E =', euler(T))
    VT = verts_of(T)
    val = {v: sum(1 for f in T if v in f) for v in VT}
    three = [v for v in VT if val[v] == 3]
    cT = centred(T)  # T is centred at sum(AX)/2
    c0 = vscale(q(Fr(1, 2)), tuple(add(add(add(add(add(AX[0][i], AX[1][i]), AX[2][i]), AX[3][i]), AX[4][i]), AX[5][i]) for i in range(3)))
    print('3-valent vertices', len(three), '5-valent', sum(1 for v in VT if val[v] == 5))
    d2 = lambda a, b: dot(vsub(a, b), vsub(a, b))
    tets = []
    for S in itertools.combinations(VT, 4):
        ds = {d2(a, b) for a, b in itertools.combinations(S, 2)}
        if len(ds) != 1: continue
        cen = (Z, Z, Z)
        for v in S: cen = vadd(cen, v)
        if cen != vscale(q(4), c0): continue
        tets.append(S)
    print('regular tetrahedra of vertices of T centred at its centre:', len(tets), '; all 3-valent:', all(val[v] == 3 for S in tets for v in S))

    data = json.load(open(K10 + '/data/search6.json'))
    cands = data['candidates_rank_le_3'][:3]
    names = ['candidate 0 = GET A', 'candidate 1 = GET B', 'candidate 2 (Inchbald)']
    CF = [centred(cand_faces(c)) for c in cands]
    for nm, F in zip(names, CF): print(nm, 'F, V, E =', euler(F), 'symmetries (+1 proper, -1 improper):', sorted(congruences(F, F)))

    out = {'T': euler(T), 'tetrahedra': len(tets), 'hall': []}
    for t, S in enumerate(tets):
        F = T; newv = []
        for v in S:
            F, vp = remove_rhombohedron(F, v); newv.append(vp)
        fve = euler(F)
        sym = congruences(centred(F), centred(F))
        row = {'tet': t, 'FVE': fve, 'sym_proper': sym.count(1), 'sym_improper': sym.count(-1),
               'removed_cells_inside_T_moves_vertex_inward': all(sgn(sub(d2(vp, c0), d2(v, c0))) < 0 for v, vp in zip(S, newv))}
        for nm, C in zip(names, CF):
            m = congruences(centred(F), C)
            row[nm] = {'same_hand_maps': m.count(1), 'mirror_maps': m.count(-1)}
        out['hall'].append(row); print(row)
    ok = (len(tets) == 10 and all(r['FVE'] == (30, 32, 60) and r['sym_proper'] == 12 and r['sym_improper'] == 0 for r in out['hall'])
          and all(r[names[0]] == r[names[1]] == {'same_hand_maps': 0, 'mirror_maps': 0} for r in out['hall'])
          and all((r[names[2]]['same_hand_maps'] == 12) != (r[names[2]]['mirror_maps'] == 12) for r in out['hall']))
    hands = [('same' if r[names[2]]['same_hand_maps'] else 'mirror') for r in out['hall']]
    out['hands_vs_candidate2'] = hands
    print('hands vs candidate 2:', hands)
    json.dump(out, open(OUT, 'w'), indent=1)
    print('FINAL ok' if ok else 'FINAL FAIL')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
