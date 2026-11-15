#!/usr/bin/env python3
"""Lead from the golden-A4 study: in the 120-cell, four 60-point orbits of A5 (the Galois-twisted diagonal of 2I, the rotation part of the
A4 Weyl group S5 inside H4) kill degree 4, which A5 does not force.  Tests, all exact unless marked:
 1. the 15 A5-orbits, their tones T_1..T_20 and stabilisers in H4;
 2. dim of A5-invariant harmonics of degree 4 (Molien) and the signed degree-4 content c(O) of every orbit (exact cross-sums);
 3. the A5 outer automorphism: every element of H4 normalising A5 (that is +-S5), and every Double-Vision map g.sigma normalising A5:
    how they permute the 15 orbits and with which sign they act on the invariant degree-4 harmonic;
 4. whether a zero orbit, translated by one of its points, lies in a finite group of unit quaternions (then the twisted-class theorem applies).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hz_core import *
from hz_universes import *
from hz_twisted import qmul, qinv

def log(*a): print(*a, flush=True)
X, A, lab, Lp, Rp, St, sig = h4_ambient()
Y, lift = cell120_from(X, A)
U = Universe('120-cell', Y, 4, to_float(Y))
gal = galois_perm(Y)
labd = {tuple(map(int, t)): i for i, t in enumerate(lab)}
Xf = to_float(X) / 2
ki = {tuple(np.round(v, 9)): i for i, v in enumerate(Xf)}
NEG = [ki[tuple(np.round(-v, 9))] for v in Xf]
def el(l, r, s=0):
    return labd.get((l, r, s), labd.get((NEG[l], NEG[r], s)))
A5 = np.unique([el(l, int(sig[l])) for l in range(120)])
log(f'A5 (twisted diagonal of 2I): {len(A5)} elements')
assert len(A5) == 60
A5set = set(A5.tolist())
orbs = orbits_from_gens(lift[A5], 600)
log(f'A5-orbit sizes on the 120-cell: {sorted(len(o) for o in orbs)}')
mats = float_mats(U.Xf, lift, span_basis(U.Xf))
chi = harm_char_table(mats, 20, 4)
dA5 = np.rint(chi[A5].mean(0)).astype(int).tolist()
log(f'dim of A5-invariant harmonics, k = 0..20: {dA5}')
# normaliser of A5 in H4
norm = [g for g in range(A.n) if set(A.mul[A.mul[g, A5], A.inv[g]].tolist()) == A5set]
log(f'normaliser of A5 in H4: order {len(norm)}')
# exact signed degree-4 contents relative to a reference orbit
k = 4
def cross(Oa, Ob, k):
    cnt = np.bincount(U.IM[np.ix_(Oa, Ob)].ravel(), minlength=U.ncos)
    a = sum((int(n) * g[0] for n, g in zip(cnt, U.G[k]) if n), F(0)); b = sum((int(n) * g[1] for n, g in zip(cnt, U.G[k]) if n), F(0))
    return (a, b)
tones = [U.tones(o) for o in orbs]
zero4 = [i for i, o in enumerate(orbs) if tones[i][4] == (0, 0)]
log(f'orbits killing degree 4: {[(i, len(orbs[i])) for i in zero4]}')
ref = next(i for i, o in enumerate(orbs) if tones[i][4] != (0, 0))
c = [cross(orbs[ref], o, 4) for o in orbs]
orbit_of = np.empty(600, int)
for i, o in enumerate(orbs): orbit_of[o] = i
rows = []
for i, o in enumerate(orbs):
    S = np.array(o); inS = np.zeros(600, bool); inS[S] = True
    stab = np.nonzero(inS[lift[:, S]].all(1))[0]
    dS = np.rint(chi[stab].mean(0)).astype(int).tolist()
    gi = int(orbit_of[gal[o[0]]])
    rows.append({'orbit': i, 'size': len(o), 'zeros': [kk for kk in range(1, 21) if tones[i][kk] == (0, 0)], 'stab_order': len(stab),
                 'dim4_stab': dS[4], 'c4': qstr(c[i]), 'c4_float': qf(c[i]), 'galois_image_orbit': gi})
    log(f"orbit {i:2d} size {len(o):3d} stab {len(stab):4d} zeros {rows[-1]['zeros']} c4 = {qstr(c[i])} (~{qf(c[i]):.4f}) sigma -> orbit {gi}")
# how the normaliser permutes orbits and its sign on the invariant degree-4 harmonic (dim 1 for A5 here)
res_norm = []
for g in norm:
    if g in A5set: continue
    perm = [int(orbit_of[lift[g][o[0]]]) for o in orbs]
    grp = np.unique(np.concatenate([A5, [g]]))
    H = A.closure(list(A5) + [g])
    d4 = int(np.rint(chi[H].mean(0))[4])
    sign = '+1' if d4 == 1 else '-1'
    res_norm.append((tuple(perm), sign, int(round(np.linalg.det(mats[g])))))
uniq = sorted(set(res_norm))
log(f'normaliser cosets: {len(uniq)} distinct (orbit permutation, sign on f4, det) patterns')
for p, s_, d in uniq:
    fixed0 = [i for i in zero4 if p[i] == i]
    log(f'  det {d:+d} sign {s_} on f4; orbit permutation {p}; zero orbits fixed: {fixed0}')
# Double Vision composites: g o gal normalising A5 (as a permutation of the 120-cell); exact action on contents c -> sigma(c)
def is_norm_semilinear(perm):
    # perm o a o perm^-1 in lift[A5] for all a in A5 ?
    inv = np.argsort(perm); keys = {lift[a].tobytes() for a in A5}
    return all(perm[lift[a][inv]].tobytes() in keys for a in A5[:6]) and all(perm[lift[a][inv]].tobytes() in keys for a in A5)
dv = []
for g in range(A.n):
    p = lift[g][gal]
    if is_norm_semilinear(p):
        dv.append(tuple(int(orbit_of[p[o[0]]]) for o in orbs))
dv = sorted(set(dv))
log(f'Double Vision maps g.sigma normalising A5: {len(dv)} distinct orbit permutations')
for p in dv:
    log(f'  orbit permutation {p}; zero orbits fixed: {[i for i in zero4 if p[i] == i]}')
# finite-group test for zero orbits
def gen_group(Q, cap=400):
    key = lambda q: tuple(np.round(q, 7))
    S = {key(np.array([1.0, 0, 0, 0])): np.array([1.0, 0, 0, 0])}; fr = list(S.values())
    while fr:
        nf = []
        for x in fr:
            for g in Q:
                y = qmul(x, g); kk = key(y)
                if kk not in S:
                    S[kk] = y; nf.append(y)
                    if len(S) > cap: return None
        fr = nf
    return len(S)
fin = {}
for i in zero4:
    P = U.Xf[orbs[i]] / np.linalg.norm(U.Xf[orbs[i]][0])
    s0i = qinv(P[0])
    fin[i] = gen_group([qmul(s0i, p) for p in P])
    log(f'orbit {i}: group generated by s0^-1 O has order {fin[i] if fin[i] else ">400 (infinite or large)"}')
json.dump({'orbits': rows, 'dim_A5': dA5, 'normaliser_order': len(norm), 'normaliser_patterns': [list(u) for u in uniq],
           'double_vision_patterns': [list(p) for p in dv], 'zero4': zero4, 'finite_group_test': fin},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'lead120.json'), 'w'), default=str)
ok = len(zero4) == 4 and dA5[4] >= 1
print('FINAL ok' if ok else 'FINAL FAIL (lead not reproduced: zero-4 orbits != 4)')
