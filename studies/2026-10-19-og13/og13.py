# OG-13 (DICTO 2026-10-19): one OG at the centre, 12 OGs free to find their own touch-only places around it, NO symmetry imposed.
# Hard-body Monte Carlo compression, float: each outer OG moves and turns at random; a move is refused if it makes any two OGs
# overlap, otherwise accepted by Metropolis on E = sum |p_i|^2 (pulls everything in) with slow annealing, then a cold quench.
# Overlap test during the run: bounding-sphere cull, then corner-inside-other both ways. The finished clusters are re-checked with
# the full separating-axis test (all face normals + all edge-pair cross products), so an edge-edge overlap cannot slip through.
# Then the symmetry that actually falls out: any symmetry of the cluster must fix the centre OG, so it is one of the centre's 120
# icosahedral operations; each is tested on all 13x102 corners at tolerances 1e-2 / 3e-2 / 6e-2.
import json, sys, itertools, numpy as np
from multiprocessing import Pool
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation

O = np.array(json.load(open('network.json'))['ocd']); H = ConvexHull(O)
pl = []
for e in H.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
pl = np.array(pl); NF = pl[:, :3]; DF = -pl[:, 3]                    # unit normals, distances (80 faces)
assert len(pl) == 80, len(pl)
RIN, ROUT = DF.min(), np.linalg.norm(O, axis=1).max()
EDGES = sorted({tuple(sorted(s)) for f in H.simplices for s in itertools.combinations(f, 2)
                if sum(np.all(np.abs(pl[:, :3] @ O[list(s)].T - DF[:, None]) < 1e-7, axis=1)) >= 2})
ED = np.array([O[b] - O[a] for a, b in EDGES]); ED /= np.linalg.norm(ED, axis=1)[:, None]
FACESIZE = np.array([int(np.sum(np.abs(O @ n - d) < 1e-7)) for n, d in zip(NF, DF)])  # 6 = hexagon, 4 = kite

def inside(VA, RB, pB, eps=1e-9):
    """Any corner of A (world coords VA) strictly inside B?"""
    X = (VA - pB) @ RB
    return np.any(np.max(X @ NF.T - DF, axis=1) < -eps)

EA_, EB_ = np.array([e[0] for e in EDGES]), np.array([e[1] for e in EDGES])

def edge_through(VA, RB, pB, eps=1e-9):
    """Does any edge of A (world corners VA) pass through the interior of B? Clip each edge against B's 80 half-spaces.
    Two convex solids overlap iff some edge of one passes through the other, so this both ways is a complete test."""
    X = (VA - pB) @ RB; a = X[EA_]; b = X[EB_]
    num = DF[None] - a @ NF.T; den = (b - a) @ NF.T                     # inside face f  <=>  t * den < num
    with np.errstate(divide='ignore', invalid='ignore'):
        t = num / den
    lo = np.max(np.where(den < -1e-14, t, 0.0), axis=1); lo = np.maximum(lo, 0.0)
    hi = np.min(np.where(den > 1e-14, t, 1.0), axis=1); hi = np.minimum(hi, 1.0)
    par_ok = np.all(np.where(np.abs(den) <= 1e-14, num > eps, True), axis=1)
    L = np.linalg.norm(b - a, axis=1)
    return np.any(par_ok & ((hi - lo) * L > eps))

def overlap(RA, pA, RB, pB):
    d = np.linalg.norm(pA - pB)
    if d >= 2 * ROUT: return False
    if d < 2 * RIN: return True
    VA = O @ RA.T + pA; VB = O @ RB.T + pB
    return edge_through(VA, RB, pB) or edge_through(VB, RA, pA)

def sat_overlap(RA, pA, RB, pB, eps=1e-9):
    """Exact-in-float separating-axis test for two convex polytopes."""
    VA = O @ RA.T + pA; VB = O @ RB.T + pB
    axes = [NF @ RA.T, NF @ RB.T]
    EA = ED @ RA.T; EB = ED @ RB.T
    C = np.cross(EA[:, None, :], EB[None, :, :]).reshape(-1, 3); n = np.linalg.norm(C, axis=1); C = C[n > 1e-9] / n[n > 1e-9, None]
    axes.append(C); A = np.vstack(axes)
    pa = VA @ A.T; pb = VB @ A.T
    gap = np.maximum(pb.min(0) - pa.max(0), pa.min(0) - pb.max(0))
    return gap.max() < -eps                                            # every axis shows a strict overlap -> they overlap

def energy(P): return float(np.sum(P * P))

def run(seed, sweeps=6000):
    rng = np.random.default_rng(seed)
    R = [np.eye(3)] + [Rotation.random(random_state=rng.integers(1 << 31)).as_matrix() for _ in range(12)]
    D = rng.normal(size=(12, 3)); D /= np.linalg.norm(D, axis=1)[:, None]
    P = np.vstack([np.zeros(3), 2.2 * D])                                # start loose, well apart
    for i in range(1, 13):                                                # make sure the start is overlap-free
        while any(overlap(R[i], P[i], R[j], P[j]) for j in range(13) if j != i): P[i] *= 1.05
    st, sr = 0.05, 0.08
    for s in range(sweeps):
        beta = 2.0 * 10 ** (4 * s / sweeps)                               # anneal 2 -> 2e4
        acc = 0
        for _ in range(12):
            i = rng.integers(1, 13)
            pn = P[i] + rng.normal(0, st, 3)
            Rn = Rotation.from_rotvec(rng.normal(0, sr, 3)).as_matrix() @ R[i]
            dE = pn @ pn - P[i] @ P[i]
            if dE > 0 and rng.random() > np.exp(-beta * dE): continue
            if any(overlap(Rn, pn, R[j], P[j]) for j in range(13) if j != i): continue
            P[i] = pn; R[i] = Rn; acc += 1
        if s % 50 == 49:                                                  # keep acceptance near 30 %
            f = 1.15 if acc > 4 else 0.87
            st = min(0.1, max(1e-4, st * f)); sr = min(0.2, max(2e-4, sr * f))
    bad = [(i, j) for i, j in itertools.combinations(range(13), 2) if sat_overlap(R[i], P[i], R[j], P[j])]
    return {'seed': seed, 'E': energy(P), 'P': P.tolist(), 'R': [r.tolist() for r in R], 'sat_bad': bad}

def ih_group():
    far = O[np.abs(np.linalg.norm(O, axis=1) - ROUT) < 1e-7]; assert len(far) == 12
    a, b = far[0], far[np.argsort(np.linalg.norm(far - far[0], axis=1))[1]]; ang = a @ b
    S = np.array([a, b, np.cross(a, b)]).T; G = []                       # rotations: send the pair (a, b) to any pair at the same angle
    for x in far:
        for y in far:
            if abs(x @ y - ang) < 1e-7: G.append(np.array([x, y, np.cross(x, y)]).T @ np.linalg.inv(S))
    G2 = []                                                               # add the improper half (times -1), keep true symmetries of O
    for M in G + [-M for M in G]:
        if np.allclose(M @ M.T, np.eye(3), atol=1e-9) and all(np.min(np.linalg.norm(O - v, axis=1)) < 1e-7 for v in O @ M.T):
            if not any(np.allclose(M, X, atol=1e-9) for X in G2): G2.append(M)
    assert len(G2) == 120, len(G2)
    return G2

def symmetry(res, G):
    V = np.vstack([O @ np.array(r).T + np.array(p) for r, p in zip(res['R'], res['P'])])
    out = {}
    for tol in (1e-2, 3e-2, 6e-2):
        keep = [M for M in G if np.max(np.min(np.linalg.norm((V @ M.T)[:, None] - V[None], axis=2), axis=1)) < tol]
        rot = sum(1 for M in keep if np.linalg.det(M) > 0)
        out[str(tol)] = {'order': len(keep), 'rotations': rot, 'has_inversion': any(np.allclose(M, -np.eye(3)) for M in keep)}
    return out

def describe(res):
    P = np.array(res['P']); R = [np.array(r) for r in res['R']]
    dist = np.linalg.norm(P[1:], axis=1)
    contact = []
    for i in range(1, 13):                                                # which centre face each neighbour sits on, and gap
        u = P[i] / np.linalg.norm(P[i]); f = int(np.argmax(NF @ u))
        X = (O @ R[i].T + P[i]); gap = float(np.min(X @ NF[f]) - DF[f])
        contact.append({'face_size': int(FACESIZE[f]), 'gap_to_centre_face': gap, 'dist': float(dist[i - 1])})
    nn = [float(np.linalg.norm(P[i] - P[j])) for i, j in itertools.combinations(range(1, 13), 2)]
    return {'dist_min': float(dist.min()), 'dist_max': float(dist.max()), 'contacts': contact,
            'outer_nn_min': min(nn), 'hexagon_contacts': sum(c['face_size'] == 6 for c in contact)}

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    print(f'OG: {len(O)} corners, 80 faces, inradius {RIN:.6f}, circumradius {ROUT:.6f}, {len(EDGES)} edges', flush=True)
    with Pool(4) as Pp:
        res = []
        for r in Pp.imap_unordered(run, range(n)):
            res.append(r); print(f"seed {r['seed']:3d}  E {r['E']:.6f}  sat_bad {r['sat_bad']}", flush=True)
    res.sort(key=lambda r: r['E']); G = ih_group()
    for r in res[:8]:
        r['sym'] = symmetry(r, G); r['desc'] = describe(r)
        d = r['desc']
        print(f"BEST seed {r['seed']} E {r['E']:.6f} sat_bad {r['sat_bad']} dist {d['dist_min']:.4f}-{d['dist_max']:.4f} "
              f"hex contacts {d['hexagon_contacts']}/12 outer nn min {d['outer_nn_min']:.4f} sym {r['sym']}", flush=True)
    json.dump(res, open('og13-results.json', 'w'))
