# Step 8, exact (pyrochlore paper prep, 2026-10-16): the conflict zone (two crossing limbs at a square-face centre) rebuilt in Q(sqrt5)
# from network.py's exact OCD, hexagon planes and bond vectors (no snapping). A limb is the prism between a free hexagon H (centre p) and
# its parallel copy H + v, v = c - 2p for a lattice vector c. The two limbs whose crossing is the float zone of conflict.py are matched,
# the zone's corners solved exactly as meeting points of three limb planes, and its faces tested exactly: rhombi, and golden rhombi
# (diagonal² ratio φ²). -> data/conflict-exact.txt
import json, itertools, numpy as np
exec(open('scripts/network.py').read().split('def where(D):')[0])
from fractions import Fraction as Fr
Z = np.array(json.load(open('data/conflict.json'))['zone'])
Tn = [f(t) for t in T]; Lf = []; Le = []
for m in itertools.product(range(-3, 4), repeat=4):
    if sum(abs(x) for x in m) > 6: continue
    pf = sum(k * t for k, t in zip(m, Tn))
    if 1e-9 < np.linalg.norm(pf) < 3.3 and not any(np.allclose(pf, q) for q in Lf):
        Lf.append(pf); s = [Q(0)] * 3
        for k, t in zip(m, T): s = add(s, [x * Q(k) for x in t])
        Le.append(s)
tn = [t / np.linalg.norm(t) for t in Tn]
free = [h for h in hexes if not any(abs(abs(unit(h[1]) @ u) - 1) < 1e-9 for u in tn)]
cent = lambda idx: [sum((OCD[i][k] for i in idx), Q(0)) / 6 for k in range(3)]
def limb_exact(h, c):                                            # corners of H and H + v
    H = [OCD[i] for i in h[0]]; p = cent(h[0]); v = sub(c, [x * 2 for x in p]); return H + [add(w, v) for w in H], v
found = []
for h in free:
    for c in Le:
        P, v = limb_exact(h, c); Pf = F(P)
        if f(v) @ unit(h[1]) <= 1e-9 or np.linalg.norm(f(v)) > 1.2: continue
        for q, qf in zip([[Q(0)] * 3] + Le, [np.zeros(3)] + Lf):
            if np.linalg.norm(Pf.mean(0) + qf - Z.mean(0)) > 0.7: continue
            Pq = [add(w, q) for w in P]; e = ConvexHull(Pf + qf).equations
            if (Z @ e[:, :3].T + e[:, 3]).max() < 1e-7 and not any(np.allclose(np.sort(F(Pq), 0), np.sort(F(X), 0)) for X in found): found.append(Pq)
out = ['DICTO · dictospheres.com', 'Conflict zone, exact in Q(√5) (limbs from the exact network; nothing snapped)', f'  limbs containing the float zone: {len(found)}']
def eplanes(V):
    Vf = F(V); res = []
    for e in ConvexHull(Vf).equations:
        idx = [i for i in range(len(V)) if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(o[0]) for o in res): continue
        for i0, i1, i2 in itertools.combinations(idx, 3):
            n = cross(sub(V[i1], V[i0]), sub(V[i2], V[i0]))
            if any(x.f() != 0 for x in n): break
        d = dot(n, V[i0]); s = 1 if sum(n[i].f() * e[i] for i in range(3)) > 0 else -1
        assert all(dot(n, V[i]) == d for i in idx); res.append((idx, [x * s for x in n], d * s))
    return res
PL = [(n, d) for X in found[:2] for _, n, d in eplanes(X)]
def solve3(P3):
    (n1, d1), (n2, d2), (n3, d3) = P3; det = det3(n1, n2, n3)
    if det.f() == 0: return None
    return [det3(*[[(d1, d2, d3)[i] if j == k else (n1, n2, n3)[i][j] for j in range(3)] for i in range(3)]) / det for k in range(3)]
Ze = []
for z in Z:
    act = [p for p in PL if abs(sum(p[0][i].f() * z[i] for i in range(3)) - p[1].f()) < 1e-7 * max(1, np.linalg.norm([x.f() for x in p[0]]))]
    sol = next((s for s in (solve3(c) for c in itertools.combinations(act, 3)) if s is not None and np.abs(f(s) - z).max() < 1e-8), None)
    assert sol is not None, ('no exact corner', z); Ze.append(sol)
ins = all(not ((dot(n, v) - d).f() > 0) for v in Ze for n, d in PL)
out.append(f'  zone: {len(Ze)} corners, each the exact meeting point of three limb planes; all inside or on both limbs: {ins}')
h = ConvexHull(Z); seen = []; phi2 = Q(Fr(3, 2), Fr(1, 2)); nq = nr = ng = 0; nf = 0
for e in h.equations:
    if any(np.allclose(e, q, atol=1e-7) for q in seen): continue
    seen.append(e); nf += 1; idx = [i for i in range(len(Z)) if abs(Z[i] @ e[:3] + e[3]) < 1e-7]
    if len(idx) != 4: continue
    nq += 1; Pf = Z[idx]; c = Pf.mean(0); a = Pf[0] - c; b = np.cross(e[:3], a); order = [idx[i] for i in np.argsort(np.arctan2((Pf - c) @ b, (Pf - c) @ a))]
    Fc = [Ze[i] for i in order]; sides = [dot(sub(Fc[i], Fc[(i + 1) % 4]), sub(Fc[i], Fc[(i + 1) % 4])) for i in range(4)]
    d1 = dot(sub(Fc[0], Fc[2]), sub(Fc[0], Fc[2])); d2 = dot(sub(Fc[1], Fc[3]), sub(Fc[1], Fc[3]))
    n0 = cross(sub(Fc[1], Fc[0]), sub(Fc[2], Fc[0])); planar = dot(n0, sub(Fc[3], Fc[0])) == 0
    rh = planar and all(s == sides[0] for s in sides); nr += rh; ng += rh and (d1 / d2 == phi2 or d2 / d1 == phi2)
out.append(f'  faces {nf}: quadrilaterals {nq}; exact rhombi {nr}; exact golden rhombi (diagonal² ratio φ², planar) {ng}')
print('\n'.join(out)); open('data/conflict-exact.txt', 'w').write('\n'.join(out) + '\n')
