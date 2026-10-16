# Line-up C copy of studies/2026-10-16-interlock/scripts/interlock_exact.py (stations: 3·I in place of H). Interlock step 3: the exact check (DICTO, 2026-10-16). Every piece of both cycles and every interlock piece rebuilt with exact
# corners in Q(sqrt5): each corner is where three exact planes meet (Cramer), checked against its float position; float points that
# lie only on an edge are dropped (geomcheck rule 5). The flipped cycle is exact too: polar in rho^2 = phi^2/4 = (3 + sqrt5)/8, its
# next turn scaled by phi^3 = 2 + sqrt5. Claims: every original piece equals the sum of its interlock parts, exactly; per layer too.
import json, sys, os, io, contextlib, itertools, numpy as np
SET = sys.argv[1] if len(sys.argv) > 1 else 'ends'              # read before polar.py replaces sys.argv; 'middle': rho^2 = 3 (3 + sqrt5)/8
from scipy.spatial import ConvexHull
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())                  # exact stations, Q, det3, volume
os.chdir(here)
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
f = lambda v: np.array([x.f() for x in v]); F = lambda V: np.array([f(v) for v in V])
dot = lambda n, v: sum((n[i] * v[i] for i in range(3)), Q(0))
cross = lambda u, w: [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
sub = lambda u, w: [u[i] - w[i] for i in range(3)]
def exact_planes(V):
    Vf = F(V); out = []
    for e in ConvexHull(Vf).equations:
        idx = [i for i in range(len(V)) if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(o[0]) for o in out): continue
        for i0, i1, i2 in itertools.combinations(idx, 3):
            n = cross(sub(V[i1], V[i0]), sub(V[i2], V[i0]))
            if any(x.f() != 0 for x in n): break
        d = dot(n, V[i0]); s = 1 if sum(n[i].f() * e[i] for i in range(3)) > 0 else -1
        out.append((idx, [x * s for x in n], d * s))
    return out
def solve3(P3):
    (n1, d1), (n2, d2), (n3, d3) = P3; det = det3(n1, n2, n3)
    if det.f() == 0: return None
    return [det3(*[[(d1, d2, d3)[i] if j == k else (n1, n2, n3)[i][j] for j in range(3)] for i in range(3)]) / det for k in range(3)]
drop = [0]
def corners(Vf, planes):
    Ve = []; Vk = []
    for v in Vf:
        act, seen = [], []
        for p in planes:
            nf = f(p[0]); m = np.linalg.norm(nf)
            if abs(nf @ v - p[1].f()) < 1e-7 * max(1, m):
                key = np.r_[nf, p[1].f()] / m
                if not any(np.allclose(key, k_, atol=1e-9) for k_ in seen): seen.append(key); act.append(p)   # a face both parents share counts once
        sol = None
        for P3 in itertools.combinations(act, 3):
            s_ = solve3(P3)
            if s_ is not None and np.abs(f(s_) - v).max() < 1e-7: sol = s_; break
        if sol is None:
            rank = np.linalg.matrix_rank(np.array([f(p_[0]) / np.linalg.norm(f(p_[0])) for p_ in act]), tol=1e-7) if act else 0
            assert rank <= 2, ('no exact corner', v, len(act), rank); drop[0] += 1; continue   # planes meet in a line at most: an edge point
        Ve.append(sol); Vk.append(v)
    return Ve, np.array(Vk)
def cone_pieces(chain, FLtxt, scale=1.0):              # exact corners of the cone-cut pieces of a chain (as in polar_exact.py)
    FL = json.load(open(FLtxt)); out = []
    for k in range(len(chain) - 1):
        A, B = chain[k], chain[k + 1]; PA, PB = exact_planes(A), exact_planes(B); L = []
        for Vf in FL[list(FL)[k]]:
            Vp = np.array(Vf) * scale; uc = Vp.mean(0) / np.linalg.norm(Vp.mean(0))
            Fi = min((p for p in PA if sum(p[1][i].f() * uc[i] for i in range(3)) > 1e-12), key=lambda p: p[2].f() / sum(p[1][i].f() * uc[i] for i in range(3)))
            planes = [(p[1], p[2]) for p in PB] + [(Fi[1], Fi[2])]
            for i0, i1 in itertools.combinations(Fi[0], 2):
                n = cross(A[i0], A[i1])
                if any(x.f() != 0 for x in n): planes.append((n, Q(0)))
            Ve, Vk = corners(Vp, planes); L.append((Ve, Vk))
        out.append(L)
    return out
def _true(V):                                               # line-up C: true corners only (float rank test), and 3·I in place of the Hecatodihedron
    Vf = F(V); h = ConvexHull(Vf)
    return [V[i] for i in range(len(V)) if np.linalg.matrix_rank(np.array([e[:3] for e in h.equations if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]), tol=1e-6) == 3]
_st = dict(stations)
orig = [_true(_st[n]) for n in ('icosahedron', 'icosidodecahedron', 'dodecahedron', 'truncated icosahedron')] + [_true([[x * 3 for x in v] for v in _st['icosahedron']])] + \
       [_true(_st[n]) for n in ('rhombic triacontahedron', 'icosahedron (phi^3)')]
K = 1 if SET == 'ends' else 3
r2 = Q(Fr(3, 8), Fr(1, 8)) * Q(K); p3 = Q(2, 1); p3inv = Q(-2, 1)
assert abs(r2.f() - K * ((1 + 5 ** .5) / 2) ** 2 / 4) < 1e-14 and abs((p3 * p3inv).f() - 1) < 1e-15 and abs(p3.f() - ((1 + 5 ** .5) / 2) ** 3) < 1e-12
flipst = [[[c * r2 / d for c in n] for idx, n, d in exact_planes(X)] for X in orig[::-1]]   # polar: plane n.x = d -> point rho^2 n / d
# the float chains used for the cut must be these exact chains (same solids)
for (nm, Vf), Ve in zip(json.load(open('data/flip-ends-chain.json')), flipst):
    A, B = np.array(Vf) * K, F(Ve); assert len(A) == len(B) and all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-9 for a in A), nm
OP = cone_pieces(orig, 'data/orig-pieces.json'); FPc = cone_pieces(flipst, 'data/flip-ends-pieces.json', K)
print('cone pieces exact:', sum(len(L) for L in OP), 'original,', sum(len(L) for L in FPc), 'flipped; edge points dropped', drop[0], flush=True)
vol = lambda Ve, Vk: volume(Ve, Vk)
J = json.load(open(f'data/interlock-{SET}.json')); parts = {}; vols = {}; exactV = []
for i, q in enumerate(J['pieces']):
    li, k = q['o']; t, lj, kk = q['f']
    P, Pk = OP[li][k]; Qv, Qk = FPc[lj][kk]
    if t: m_ = p3 if t == 1 else p3inv; Qv = [[c * m_ for c in v] for v in Qv]; Qk = Qk * m_.f()
    planes = [(n, d) for _, n, d in exact_planes(P)] + [(n, d) for _, n, d in exact_planes(Qv)]
    Ve, Vk = corners(np.array(q['v']), planes); v = vol(Ve, Vk); exactV.append(F(Ve))
    parts[(li, k)] = parts.get((li, k), Q(0)) + v; vols.setdefault(v, 0); vols[v] += 1
    if i % 100 == 0: print('interlock piece', i, flush=True)
bad = [(key, parts[key] - vol(*OP[key[0]][key[1]])) for key in parts if not (parts[key] - vol(*OP[key[0]][key[1]])) == Q(0)]
missing = [(li, k) for li, L in enumerate(OP) for k in range(len(L)) if (li, k) not in parts]
lay = {}
for (li, k), s in parts.items(): lay[li] = lay.get(li, Q(0)) + s
laycheck = [lay[li] - (volume(orig[li + 1], F(orig[li + 1])) - volume(orig[li], F(orig[li]))) for li in sorted(lay)]
out = [f'exact interlock ({SET} setting): {len(J["pieces"])} pieces; float edge points dropped {drop[0]}',
       f'every original piece = sum of its parts, exactly: {not bad and not missing} (mismatches {len(bad)}, original pieces without parts {len(missing)})',
       f'every original layer = sum of its interlock pieces, exactly: {all(x == Q(0) for x in laycheck)}',
       f'distinct exact piece volumes: {len(vols)}',
       f'kinds by symmetry orbit on the exact corners: {len(gc.kinds(exactV, gc.group(gc.icosa_axes(F(orig[0])))))}']
for v, c in sorted(vols.items(), key=lambda kv: -kv[0].f()): out.append(f'    {c:3d} x  {v!r} = {v.f():.9f}')
print('\n'.join(out)); open(f'data/interlock-{SET}-exact.txt', 'w').write('\n'.join(out) + '\n')
