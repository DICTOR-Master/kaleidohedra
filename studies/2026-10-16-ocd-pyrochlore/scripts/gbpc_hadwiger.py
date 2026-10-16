# Fable, GBPC pass 3 (2026-10-16): Hadwiger-Jessen edge invariant of G' (exact in Q(sqrt5); angles exact as multiples of pi/30, checked).
# For a polytope P, an edge direction l and a direction u (generic, perpendicular part only matters):
#   J_{l,u}(P) = sum over edges e of P parallel to l of  |e| * ( [u in C_e] + [-u in C_e] - angle(C_e)/pi ),
# C_e = the inner dihedral wedge of P at e. J is additive under ANY dissection (edges may lie inside faces of other pieces: their wedges
# are half-planes, weight 0; interior edges: full plane, weight 0). Every parallelepiped has J = 0 (its 4 edges parallel to l have
# wedges partitioning the plane: weight 1 + 1 - 2 = 0). So every finite union of parallelepipeds - golden rhombohedra of any sizes,
# face to face or not - has J = 0. For G' per bcc cell: J(G') = -J(union of RTs per cell) = 4 J(lens) - J(RT), lens = RT cap (RT + c).
import sys, io, os, contextlib, itertools, json, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
src = open(os.path.join(HERE, 'golden_fill.py')).read().split('# ---- all bodies')[0]
cwd = os.getcwd(); os.chdir(STUDY)
with contextlib.redirect_stdout(io.StringIO()):
    exec(src)
os.chdir(cwd)
out = []; say = lambda s: (print(s, flush=True), out.append(s))
say("DICTO · dictospheres.com — Fable, Hadwiger-Jessen edge invariant of G' (exact in Q(sqrt5) unless marked FLOAT)")
V5 = [v if sgn(next(x for x in v if x != Z)) > 0 else neg(v) for v in AX['5']]
def edge_data(P):
    """per edge: (axis index, length in units of that five-fold vector (exact), outward normals n1, n2, angle/pi exact as Fraction)"""
    res = []
    for i, j in P['E']:
        d = sub(P['V'][j], P['V'][i]); k = next((a for a in range(6) if iszero(cross(d, V5[a]))), None)
        assert k is not None, 'edge not five-fold'
        c = next(t for t in range(3) if V5[k][t] != Z); mu = d[c] / V5[k][c]; mu = mu if sgn(mu) > 0 else -mu
        fs = [g for g in P['F'] if i in g[2] and j in g[2]]; assert len(fs) == 2
        n1, n2 = fs[0][0], fs[1][0]
        u1, u2 = fl(n1) / np.linalg.norm(fl(n1)), fl(n2) / np.linalg.norm(fl(n2))
        ang = np.pi - np.arccos(np.clip(u1 @ u2, -1, 1))          # inner dihedral angle (FLOAT), then snapped to pi/30
        q = Fr(round(ang / np.pi * 30), 30); assert abs(float(q) * np.pi - ang) < 1e-9, 'angle not a multiple of pi/30'
        res.append((k, mu, n1, n2, q))
    return res
def J(P, k, u):
    tot = Z
    for kk, mu, n1, n2, q in edge_data(P):
        if kk != k: continue
        inC = lambda x: sgn(dot(n1, x)) < 0 and sgn(dot(n2, x)) < 0
        assert sgn(dot(n1, u)) != 0 and sgn(dot(n2, u)) != 0, 'u not generic'
        tot = tot + mu * Q(int(inC(u)) + int(inC(neg(u))) - q)
    return tot
U = [[Q(Fr(1, 7)), Q(Fr(3, 11)), Q(1)], [Q(Fr(-5, 13)), Q(1), Q(Fr(2, 17))], [Q(1), Q(Fr(-4, 19)), Q(Fr(7, 23))]]
# sanity: a golden rhombohedron (and the RT, a zonohedron) must give 0
def parallelepiped(a, b, c):
    H = []
    for n in (cross(a, b), cross(b, c), cross(c, a)):
        pts = [[Z, Z, Z], a, b, c, add(a, b), add(b, c), add(c, a), add(add(a, b), c)]
        H.append((n, max((dot(n, x) for x in pts), key=lambda z: z.f()))); H.append((neg(n), max((dot(neg(n), x) for x in pts), key=lambda z: z.f())))
    return polytope(H)
PP = parallelepiped(V5[0], V5[1], neg(V5[3]))
chk_pp = all(J(PP, k, u) == Z for k in range(6) for u in U)
chk_rt = all(J(RT, k, u) == Z for k in range(6) for u in U)
say(f'sanity: J = 0 on a golden rhombohedron: {chk_pp}; on the rhombic triacontahedron: {chk_rt}')
nearRT = [c for c in near if np.linalg.norm(fl(c)) < 2 * RT['r'] + 1e-9]
lenses = []
for c in nearRT:
    try: X = polytope(RT['H'] + [(n, d + dot(n, c)) for n, d in RT['H']])
    except Exception: continue
    if len(X['V']) >= 4: lenses.append((c, X))
lenses = [(c, X) for c, X in lenses if pvol(X) != Z]
say(f'overlap lenses RT cap (RT + c): {len(lenses)} (the 8 joined neighbours); each has {len(lenses[0][1]["V"])} corners, volume {pvol(lenses[0][1])!r}')
ed = edge_data(lenses[0][1]); vol = pvol(lenses[0][1]); phi = Q(Fr(1, 2), Fr(1, 2))
say(f'each lens: {len(ed)} edges, all five-fold, lengths {sorted({repr(e[1]) for e in ed})} x|v| (2phi/9 = {phi * Q(Fr(2, 9))!r}); dihedral angles / pi {sorted({str(e[4]) for e in ed})};'
    f' volume = (2phi/9)^3 x oblate volume: {vol == (phi * Q(Fr(2, 9))) ** 3 * Q(376, -168) if hasattr(Q, "__pow__") else vol == (phi * Q(Fr(2, 9))) * (phi * Q(Fr(2, 9))) * (phi * Q(Fr(2, 9))) * Q(376, -168)}')
say(f'RT edge lengths {sorted({repr(e[1]) for e in edge_data(RT)})} x|v| (= phi/3)')
rows = []
for k in range(6):
    for ui, u in enumerate(U):
        jG = sum((J(X, k, u) for c, X in lenses), Z) * Q(Fr(1, 2)) - J(RT, k, u)   # per cell: half of the 8 lenses = 4 lenses
        rows.append((k, ui, jG))
nz = [r for r in rows if r[2] != Z]
say("J(G') per cell = (1/2) sum over the 8 lenses of J(lens) - J(RT), in units of |v| (exact), for the 6 five-fold directions l and 3 generic u:")
for k in range(6):
    say(f'  l = v{k + 1}: ' + ', '.join(f'u{ui + 1}: {jG!r}' for kk, ui, jG in rows if kk == k))
say("RESULT: J(G') != 0, so G' is NOT a finite union of parallelepipeds: no tiling by golden rhombohedra of finitely many sizes, in any arrangement"
    if nz else "RESULT: J(G') = 0 for all tested l, u: this invariant does not obstruct")
open(os.path.join(STUDY, 'data', 'gbpc-hadwiger.txt'), 'w').write('\n'.join(out) + '\n')
