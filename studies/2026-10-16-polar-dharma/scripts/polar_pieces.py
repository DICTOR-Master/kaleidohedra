# Polar Dharma step 2 (2026-10-16): each reversed layer A ⊂ B cut into one piece per face F of A: cone(F) ∩ B ∩ {beyond F}, convex by
# construction (the Kion construction of Theaetetus, #29). Reports per layer: piece kinds (by shape), corners, faces, volumes, and the sum
# against the layer; then which neighbouring pieces fuse without a dent.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
CL = json.load(open('data/reversed-chain.json')); names = [n for n, _ in CL]; C = {n: V for n, V in CL}
def faces(P):
    h = ConvexHull(P); F = []
    for e in h.equations:
        idx = tuple(sorted(i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7))
        if idx not in [f for f, _ in F]: F.append((idx, e))
    return F
def order(P, idx, n):
    Q = P[list(idx)]; c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    return [idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]
def ray(h, u):
    nu = h.equations[:, :3] @ u; m = nu > 1e-12; return np.min(-h.equations[m, 3] / nu[m])
def shape(P):
    h = ConvexHull(P); planes = []
    for e, s in zip(h.equations, h.simplices):
        for p in planes:
            if np.allclose(p['e'], e, atol=1e-7): p['i'] |= set(s); break
        else: planes.append({'e': e, 'i': set(s)})
    sides = tuple(sorted(len(p['i']) for p in planes))
    L = sorted(round(np.linalg.norm(P[a] - P[b]), 5) for a, b in itertools.combinations(range(len(P)), 2))
    return len(P), sides, round(h.volume, 6), tuple(L)
out = []
allpieces = {}
for k in range(len(names) - 1):
    A, B = np.array(C[names[k]]), np.array(C[names[k + 1]]); hA, hB = ConvexHull(A), ConvexHull(B)
    pieces = []; empty = 0
    for idx, e in faces(A):
        n = e[:3]; ring = order(A, idx, n); Fc = A[ring].mean(0)
        hs = [np.r_[-n, -e[3]]]                                   # beyond the face plane
        for i in range(len(ring)):
            a, b = A[ring[i]], A[ring[(i + 1) % len(ring)]]; m = np.cross(a, b); m = m if m @ Fc > 0 else -m
            hs.append(np.r_[-m, 0.0])                             # inside the cone over the face
        hs += list(hB.equations)
        u = Fc / np.linalg.norm(Fc); r0 = np.linalg.norm(Fc); r1 = ray(hB, u); pt = u * (r0 + r1) / 2
        if r1 - r0 < 1e-9: empty += 1; continue            # this face of A lies on B's surface: nothing beyond it
        HS = HalfspaceIntersection(np.array(hs), pt); V = np.unique(np.round(HS.intersections, 9), axis=0)
        pieces.append(V)
    kinds = {}
    for V in pieces:
        s = shape(V); kinds.setdefault(s[:3] + (s[3],), []).append(V)
    tot = sum(ConvexHull(V).volume for V in pieces); lay = hB.volume - hA.volume
    out.append(f'{names[k]} -> {names[k + 1]}: {len(pieces)} pieces ({empty} faces of the inner solid lie on the outer one), {len(kinds)} kind(s); volumes {tot:.9f} vs layer {lay:.9f}')
    for s, L in kinds.items():
        out.append(f'    {len(L):3d} x  {s[0]} corners, faces {dict((x, s[1].count(x)) for x in sorted(set(s[1])))}, volume {s[2]}')
    # fusions: pairs of pieces sharing a face whose union has no dent
    key = lambda p: tuple(np.round(p, 6))
    fus = {}
    for i, j in itertools.combinations(range(len(pieces)), 2):
        P, Q = pieces[i], pieces[j]; sp = {key(p) for p in P}
        if sum(key(q) in sp for q in Q) < 3: continue
        U = np.unique(np.round(np.vstack([P, Q]), 9), axis=0)
        if abs(ConvexHull(U).volume - ConvexHull(P).volume - ConvexHull(Q).volume) < 1e-8:
            s = shape(U); fus.setdefault((s[0], s[1]), 0); fus[(s[0], s[1])] += 1
    for (nc, sd), cnt in fus.items():
        out.append(f'      fuses without a dent: {cnt} pair(s) -> {nc} corners, faces {dict((x, sd.count(x)) for x in sorted(set(sd)))}')
    allpieces[f'{names[k]} -> {names[k + 1]}'] = [V.tolist() for V in pieces]
    print('\n'.join(out[-1 - len(kinds) - len(fus):]), flush=True)
open('data/polar-step2.txt', 'w').write('\n'.join(out) + '\n'); json.dump(allpieces, open('data/polar-pieces.json', 'w'))
