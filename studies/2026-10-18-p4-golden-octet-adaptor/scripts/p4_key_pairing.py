# DICTO 2026-10-18 keyed Penrose pattern on the star-centred W, "while maintaining singularity as the piece adaptor" (one piece type).
# Which faces of W can carry bumps and which dents so that every shared face pairs a bump with a dent, with all W identical?
# For each face F of W(m): neighbour m' across F; a structure symmetry g (Th at an OCD centre + fcc translation) with g(m) = m';
# the same physical face is g(F') for a face F' of W(m). Faces F -- F' form a graph; a bump/dent split exists iff it is bipartite
# (a face paired with itself needs a pattern that is its own opposite: half bumps, half dents). -> data/p4-key-pairing.json
import json, itertools, os, numpy as np
from scipy.spatial import ConvexHull
H = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data', 'step10-input.json'))); R = D['R']; L = np.array(D['L'])
m = np.array([0, R / 2, R / 2])
C = np.array([[0, 0, 0], [0, R, R], [0, R, 0], [0, 0, R], [R / 2, R / 2, R / 2], [-R / 2, R / 2, R / 2]])
h = ConvexHull(C); faces = [(sorted(s.tolist()), eq) for s, eq in zip(h.simplices, h.equations)]
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
lat = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
def face_key(P): return tuple(sorted(tuple(np.round(p, 6)) for p in P))
fkeys = [face_key(C[s]) for s, _ in faces]
out = []
for i, (s, eq) in enumerate(faces):
    n = eq[:3]; d = eq[3] + n @ m; mp = m - 2 * d * n; F = C[s]
    hits = []
    for G in ops:
        for t in lat:
            if np.allclose(G @ m + t, mp):
                Fp = (np.linalg.inv(G) @ (F - t).T).T          # preimage of the shared face in W(m)'s frame
                k = face_key(Fp)
                if k in fkeys: hits.append((fkeys.index(k), G.tolist(), t.tolist()))
    out.append(dict(face=i, corners=(F / R).round(3).tolist(), neighbour=(mp / R).round(3).tolist(), partners=sorted({hp[0] for hp in hits})))
# bipartite test over all partner choices: a face may have several possible partners (different g); try to 2-colour
adj = {o['face']: set(o['partners']) for o in out}
for a in list(adj):
    for b in adj[a]: adj.setdefault(b, set()).add(a)
def bipartite():
    col = {}
    for s0 in adj:
        if s0 in col: continue
        col[s0] = 0; stack = [s0]
        while stack:
            a = stack.pop()
            for b in adj[a]:
                if b not in col: col[b] = 1 - col[a]; stack.append(b)
                elif col[b] == col[a]: return None
    return col
self_paired = [o['face'] for o in out if o['face'] in o['partners']]
col = bipartite()
res = dict(faces=out, self_paired=self_paired, bipartite=col is not None, colouring=col,
           note='edges join each face to every face it can be paired with under some symmetry; one consistent choice per face suffices')
print(json.dumps({k: v for k, v in res.items() if k != 'faces'}, indent=1))
for o in out: print(o['face'], o['corners'], '->', o['partners'])
json.dump(res, open(os.path.join(H, '..', 'data', 'p4-key-pairing.json'), 'w'), indent=1)
