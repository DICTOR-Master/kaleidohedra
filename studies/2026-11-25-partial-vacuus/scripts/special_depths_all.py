# DICTO · partial Vacuus, part 1b (26 Nov 2026): special pit depths for every Platonic, Archimedean and Catalan solid P, pits ending on
# any of them Q (same centre, Q scaled freely). With Claude (Anthropic). Floating point (1e-8), every wall of every pit checked.
# Pit on face f of P: apex on the line from O perpendicular to f, at a = s d_f (0 < s < 1). Wall through edge (u, v) of f:
# normal m(a) = u x v - a (u x n_f + n_f x v), linear in a. The depth is special when one s and one scale lam make EVERY wall a face
# plane of lam Q: m(a) parallel to a face normal w of Q, and the wall's distance from O equal to lam d_Q(w).
# Solids: the 163 of study 2026-11-24-vacuus-resonus-catalogue as extracted in study 2026-11-25-tacitus (data/polyhedra.json);
# only families Platonic / Archimedean / Catalan used. Control: dodecahedron on icosahedron at 5 - 2 sqrt5 and icosahedron on
# dodecahedron at 3 sqrt5 - 6 (part 1, exact).
import json, os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
POLY = json.load(open(os.path.join(HERE, '../../2026-11-25-tacitus/data/polyhedra.json')))
sel = [p for p in POLY if p.get('family', '').lower().split()[0] in ('platonic', 'archimedean', 'catalan')]
print('solids', len(sel), sorted({p['family'] for p in sel}), flush=True)
def prep(p):
    V = np.array(p['verts'], float); V -= V.mean(0) * 0   # centre at the origin as given (centrally placed)
    F = p['faces']; N, D = [], []
    for f in F:
        P = V[f]; c = P.mean(0); n = np.zeros(3)
        for a, b in zip(P, np.roll(P, -1, 0)): n += np.cross(a - c, b - c)
        n /= np.linalg.norm(n)
        if n @ c < 0: n = -n
        N.append(n); D.append(n @ P[0])
    return V, F, np.array(N), np.array(D)
def rot_axes(V):
    """axes of the half-turn and quarter-turn symmetries of the corner set (numerical)"""
    Vn = V; axes = []
    cand = list(Vn / np.linalg.norm(Vn, axis=1)[:, None])
    for a, b in itertools.combinations(range(len(V)), 2):
        m = V[a] + V[b]
        if np.linalg.norm(m) > 1e-9: cand.append(m / np.linalg.norm(m))
    for w in cand:
        R = 2 * np.outer(w, w) - np.eye(3)      # half-turn about w
        W = V @ R.T
        if all(np.min(np.linalg.norm(V - x, axis=1)) < 1e-7 for x in W):
            if not any(abs(abs(w @ u) - 1) < 1e-7 for u in axes): axes.append(w)
    return axes
def canon(V):
    ax = rot_axes(V)
    for a, b, c in itertools.combinations(ax, 3):
        if abs(a @ b) < 1e-7 and abs(a @ c) < 1e-7 and abs(b @ c) < 1e-7:
            R = np.array([a, b, np.cross(a, b)]); return R
    return None
FRAME = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i, j in enumerate(perm): M[i, j] = sg[i]
        if np.linalg.det(M) > 0: FRAME.append(M)
assert len(FRAME) == 24
S = {}
for p in sel:
    V, F, N, D = prep(p); R = canon(V)
    if R is None: print('no orthogonal axis triple:', p['name'], flush=True); continue
    S[p['name']] = (V @ R.T, F, N @ R.T, D)
print('canonical frames:', len(S), flush=True)
def walls(V, F, N, D):
    out = []
    for fi, f in enumerate(F):
        for a1, b1 in zip(f, f[1:] + f[:1]):
            u, v = V[a1], V[b1]; out.append((fi, np.cross(u, v), -(np.cross(u, N[fi]) + np.cross(N[fi], v)), u))
    return out
found = []
for P, (V, F, N, D) in S.items():
    W = walls(V, F, N, D)
    for Q, (VQ, FQ, NQ0, DQ) in S.items():
      seen_q = set()
      for M in FRAME:
        NQ = NQ0 @ M.T
        key = tuple(sorted(tuple(np.round(n, 6)) for n in NQ))
        if key in seen_q: continue
        seen_q.add(key)
        # candidate (s, lam) from the first wall, checked on all others
        fi, m0, m1, u = W[0]; cands = set()
        for w, dq in zip(NQ, DQ):
            A_ = np.cross(m1, w); B_ = -np.cross(m0, w)
            if np.linalg.norm(A_) < 1e-12: continue
            a = float(A_ @ B_ / (A_ @ A_))
            if np.linalg.norm(np.cross(m0 + a * m1, w)) > 1e-8 or not (1e-6 * D[fi] < a < D[fi] - 1e-9): continue
            m = m0 + a * m1; m /= np.linalg.norm(m); lam = abs(m @ u) / dq
            if lam > 1e-6: cands.add((round(a / D[fi], 8), round(lam, 8)))
        for s, lam in sorted(cands):
            ok = True
            for fj, m0j, m1j, uj in W:
                a = s * D[fj]; m = m0j + a * m1j; m /= np.linalg.norm(m); dist = abs(m @ uj)
                if not any(abs(abs(m @ w) - 1) < 1e-8 and abs(dist - lam * dq) < 1e-7 for w, dq in zip(NQ, DQ)): ok = False; break
            if ok and not any(f['P'] == P and f['Q'] == Q and abs(f['s'] - s) < 1e-7 for f in found):
                found.append(dict(P=P, Q=Q, s=s, lam=lam)); print(f'{P:40s} pits end on {Q:40s} s = {s:.8f}  scale {lam:.6f}', flush=True)
json.dump(found, open(os.path.join(HERE, '../data-special-all.json'), 'w'), indent=1)
ctrl = any('dodecahedron' == f['P'].lower().replace('_', ' ') and 'icosahedron' == f['Q'].lower().replace('_', ' ') and abs(f['s'] - (5 - 2 * 5 ** .5)) < 1e-6 for f in found)
print('special depths found', len(found), '; control (dodecahedron on icosahedron at 5-2sqrt5):', ctrl)
print('FINAL ok' if ctrl else 'FINAL FAIL (control)')
