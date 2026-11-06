"""DICTO 11-06 supercells of nests, route (c): "parts of the 120 and 600 or mid structure". First: the 120-cell's 1 + 12 = DICTO's
Dodeca-13 (13 dodecahedra + 30 wedges + 20 needles, studies/2026-10-09-dodeca-13), with a full five-solid nest in EVERY dodecahedron:
D > I (D's face centres) > O (six of I's edge midpoints) > C (O's face centres) > T (alternate corners of C). Checks: every solid regular,
each inside the next, every nest inside its own dodecahedron, nests of different dodecahedra disjoint; volumes."""
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
d = json.load(open('/home/dicto/k-research/studies/2026-10-09-dodeca-13/data/c13-parts-pieces-unit.json'))
parts = [(p['role'], np.array(p['vertices'], float)) for p in d['parts']]
def faces(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 5)), set()).update(sp)
    return [V[list(s)] for s in F.values()]
def edges(V):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min()
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - e) < 1e-6]
def regular(V, n):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min(); k = len(edges(V))
    return len(V) == n and k == {4: 6, 6: 12, 8: 12, 12: 30, 20: 30}[n]
def nest(Dv):
    c = Dv.mean(0)
    I = np.array([f.mean(0) for f in faces(Dv)])
    mids = np.array([(I[i] + I[j]) / 2 for i, j in edges(I)]) - c
    O = None
    for a, b, e in itertools.combinations(range(len(mids)), 3):
        u = mids[[a, b, e]]; r = np.linalg.norm(u, axis=1)
        if np.allclose(r, r[0], atol=1e-6) and abs(u[0] @ u[1]) < 1e-5 and abs(u[0] @ u[2]) < 1e-5 and abs(u[1] @ u[2]) < 1e-5:
            O = np.vstack([u, -u]) + c; break
    C = np.array([f.mean(0) for f in faces(O)])
    s = np.sign(np.linalg.det(np.array([C[1] - C[0], C[2] - C[0], C[3] - C[0]])))
    # tetrahedron: corners of C no two of which share an edge
    E = edges(C); T = [0]
    for k in range(1, 8):
        if all((min(k, t), max(k, t)) not in E for t in T): T.append(k)
    T = C[T[:4]]
    return {'I': I, 'O': O, 'C': C, 'T': T}
def inside(inner, outer):
    h = ConvexHull(outer); return bool(((inner @ h.equations[:, :3].T + h.equations[:, 3]) <= 1e-7).all())
dods = [V for r, V in parts if r == 'dodeca']
print(f"Dodeca-13: {len(dods)} dodecahedra, {sum(r == 'wedge' for r, _ in parts)} wedges, {sum(r == 'needle' for r, _ in parts)} needles")
nests = []; ok = True
for k, Dv in enumerate(dods):
    n = nest(Dv); nests.append(n)
    chk = [regular(Dv, 20), regular(n['I'], 12), regular(n['O'], 6), regular(n['C'], 8), regular(n['T'], 4),
           inside(n['I'], Dv), inside(n['O'], n['I']), inside(n['C'], n['O']), inside(n['T'], n['C'])]
    ok &= all(chk)
    if k == 0:
        eD = np.linalg.norm(Dv[0] - Dv[edges(Dv)[0][1]] ) if False else min(np.linalg.norm(Dv[i] - Dv[j]) for i, j in edges(Dv))
        sizes = {nm: min(np.linalg.norm(V[i] - V[j]) for i, j in edges(V)) for nm, V in [('D', Dv)] + list(n.items())}
        print("sizes (edge):", {k_: round(v, 6) for k_, v in sizes.items()}, "volumes:", {nm: round(ConvexHull(V).volume, 6) for nm, V in [('D', Dv)] + list(n.items())})
print("every nest regular and nested:", ok)
# nests of different dodecahedra disjoint: their icosahedra lie inside disjoint dodecahedra -> check dodecahedra pairwise by separating plane
def disjoint(A, B):
    for P, Q in ((A, B), (B, A)):
        h = ConvexHull(P)
        for eq in h.equations:
            if ((Q @ eq[:3] + eq[3]) >= -1e-7).all(): return True
    return False
print("dodecahedra pairwise disjoint (separating face plane):", all(disjoint(dods[a], dods[b]) for a, b in itertools.combinations(range(13), 2)))
json.dump({'dodecahedra': [V.tolist() for V in dods], 'nests': [{k: v.tolist() for k, v in n.items()} for n in nests],
           'wedges': [V.tolist() for r, V in parts if r == 'wedge'], 'needles': [V.tolist() for r, V in parts if r == 'needle']},
          open('../nest13.json', 'w'))
print("FINAL", "ok" if ok else "FAIL")
