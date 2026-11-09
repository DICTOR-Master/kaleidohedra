# Splash determinants, part S2: the second dual sweep CO ∩ mu·RD (study 2026-11-04-co-rd-sweep), exact in Q.
# CO = {|x_i| <= 1, |x|+|y|+|z| <= 2}, RD = {|x_i| + |x_j| <= 1}; mu in [1, 2]. Incidence events = roots of 4-plane determinants
# (affine in mu) whose common point lies on S(mu) and where the face lattice changes. Also the hopscotch turn: the polar of the
# family is not in the family (three plane families), so no turn is claimed; we list mu -> 2/mu partners for the record only.
import itertools, json, os
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data")
planes = []   # (normal, const, coef of mu)
for i in range(3):
    for s in (1, -1):
        n = [0, 0, 0]; n[i] = s; planes.append((tuple(n), Fr(1), Fr(0)))
for sg in itertools.product((1, -1), repeat=3):
    planes.append((sg, Fr(2), Fr(0)))
for i, j in itertools.combinations(range(3), 2):
    for a, b in itertools.product((1, -1), repeat=2):
        n = [0, 0, 0]; n[i] = a; n[j] = b; planes.append((tuple(n), Fr(0), Fr(1)))


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def solve3(M, b):
    D = det3(M)
    if D == 0: return None
    out = []
    for k in range(3):
        Mk = [list(r) for r in M]
        for r in range(3): Mk[r][k] = b[r]
        out.append(det3(Mk) / D)
    return out


def verts(mu):
    V = set()
    for t in itertools.combinations(planes, 3):
        x = solve3([p[0] for p in t], [p[1] + p[2] * mu for p in t])
        if x is None: continue
        if all(sum(a * b for a, b in zip(p[0], x)) <= p[1] + p[2] * mu for p in planes): V.add(tuple(x))
    return V


def faces(mu):
    V = verts(mu); f = []
    for p in planes:
        k = sum(1 for x in V if sum(a * b for a, b in zip(p[0], x)) == p[1] + p[2] * mu)
        if k >= 3: f.append(k)
    return len(V), tuple(sorted(f))


roots = {}
for q in itertools.combinations(range(len(planes)), 4):
    # det [n_i, -(c_i + e_i mu)] = d0 + mu d1 (expand along last column)
    d0 = d1 = Fr(0)
    for r in range(4):
        minor = [planes[q[k]][0] for k in range(4) if k != r]
        cof = (-1) ** (r + 3) * det3(minor)
        d0 += cof * (-planes[q[r]][1]); d1 += cof * (-planes[q[r]][2])
    if d1 == 0: continue
    mu = -d0 / d1
    if not (1 <= mu <= 2): continue
    x = None
    for t in itertools.combinations(q, 3):
        x = solve3([planes[k][0] for k in t], [planes[k][1] + planes[k][2] * mu for k in t])
        if x is not None: break
    if x is None: continue
    if all(sum(a * b for a, b in zip(p[0], x)) <= p[1] + p[2] * mu for p in planes):
        roots.setdefault(mu, q)
res = []
for mu in sorted(roots):
    e = Fr(1, 1000)
    a = faces(mu - e) if mu - e >= 1 else None; b = faces(mu + e) if mu + e <= 2 else None
    res.append(dict(mu=str(mu), faces_below=str(a), faces_at=str(faces(mu)), faces_above=str(b), change=(a != b) or mu in (1, 2)))
    print(f"CO∩mu·RD: 4-plane root mu = {mu}: below {a}, at {faces(mu)}, above {b}", flush=True)
known = {Fr(1), Fr(4, 3), Fr(3, 2), Fr(2)}
found = {Fr(r["mu"]) for r in res if r["change"]}
json.dump(dict(events=res, known_breaks=[str(k) for k in sorted(known)]), open(os.path.join(DATA, "corrd-events.json"), "w"), indent=1)
print("events with a face-lattice change (and the ends):", sorted(str(x) for x in found))
print('FINAL ok' if found == known else f'FINAL FAIL: found {sorted(map(str, found))} vs known {sorted(map(str, known))}')
