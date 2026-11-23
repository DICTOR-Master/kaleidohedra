# (study 2026-11-24-aequi-certify-extend, Part 2(b) caps: unchanged copy of the 2026-11-19-aequi-complete solver, box e^±1.5)
# Double-precision search: for one group class and a slice of its orbit subsets, solve the m-1 fairness equations
# (mean solid angle of orbits 2..m = 4π/N, from the frame centre) in the m-1 free log-depths (orbit 1 at depth 1),
# from a grid of starts; record every distinct solution with every face at 4π/N (all faces then present).
# Solid angles: Van Oosterom–Strackee (1983) triangle formula on a fan from the face centre (Equanimity's method).
# usage: solve.py classes.json CLASS_INDEX M SLICE_I SLICE_N NPROC out.jsonl
import json, sys, itertools, time, numpy as np
from multiprocessing import Pool
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS, DFAM
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import root, linprog
from scipy.stats import qmc
def tri(a, b, c):
    return 2 * np.arctan2(np.abs(np.einsum('ij,ij->i', a, np.cross(b, c))),
                          1 + np.einsum('ij,ij->i', a, b) + np.einsum('ij,ij->i', b, c) + np.einsum('ij,ij->i', c, a))
def face_omegas(Nrm, D):
    H = np.hstack([Nrm, -D[:, None]])
    hs = HalfspaceIntersection(H, np.zeros(3))
    V = hs.intersections
    om = np.zeros(len(D))
    res = np.abs(V @ Nrm.T - D[None, :])
    for f in range(len(D)):
        P = V[res[:, f] < 1e-9 * max(1, D[f])]
        if len(P) < 3: continue
        P = np.unique(np.round(P, 12), axis=0)
        if len(P) < 3: continue
        c = P.mean(0); n = Nrm[f]; e1 = P[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        P = P[np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]
        Q = np.roll(P, -1, 0)
        cu = c / np.linalg.norm(c) if np.linalg.norm(c) > 1e-12 else n
        om[f] = tri(np.repeat(cu[None], len(P), 0), P / np.linalg.norm(P, axis=1)[:, None], Q / np.linalg.norm(Q, axis=1)[:, None]).sum()
    return om
def bounded(V):
    if np.linalg.matrix_rank(np.asarray(V), tol=1e-9) < 3: return False
    n = len(V); c = np.zeros(n + 1); c[-1] = -1
    Aeq = np.zeros((4, n + 1)); Aeq[:3, :n] = V.T; Aeq[3, :n] = 1
    Aub = np.hstack([-np.eye(n), np.ones((n, 1))])
    r = linprog(c, A_ub=Aub, b_ub=np.zeros(n), A_eq=Aeq, b_eq=[0, 0, 0, 1], bounds=[(0, None)] * n + [(None, None)])
    return r.status == 0 and -r.fun > 1e-9
def starts(d):
    lo, hi = np.log(0.65), np.log(1.7)
    if d == 1: return [[x] for x in np.linspace(lo, hi, 21)]
    if d <= 5:
        k = {2: 9, 3: 6, 4: 4, 5: 3}[d]
        return [list(p) for p in itertools.product(np.linspace(lo, hi, k), repeat=d)] + [[0.0] * d]
    S = qmc.Sobol(d, seed=1).random(256)
    return [list(lo + (hi - lo) * s) for s in S] + [[0.0] * d]
BLOCK = 12
def solve_block(args):
    orbs, S, b0 = args
    idx = [j for i in S for j in orbs[i]]; Nrm = DIRS[idx]; N = len(idx)
    sizes = [len(orbs[i]) for i in S]; m = len(S); T = 4 * np.pi / N
    cut = np.cumsum([0] + sizes)
    def depths(x): return np.repeat(np.exp(np.r_[0.0, x]), sizes)
    def F(x):
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 1.5: return np.full(m - 1, 10.0) + np.abs(np.nan_to_num(x, nan=9.0)).max()
        try: om = face_omegas(Nrm, depths(x))
        except Exception: return np.full(m - 1, 10.0)
        return np.array([om[cut[k]:cut[k + 1]].mean() - T for k in range(1, m)])
    sols = []
    for x0 in starts(m - 1)[b0:b0 + BLOCK]:
        try: r = root(F, x0, method='hybr', options=dict(xtol=1e-14, maxfev=40 * m))
        except Exception: continue
        x = r.x
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 3: continue
        try: om = face_omegas(Nrm, depths(x))
        except Exception: continue
        if np.abs(om - T).max() < 1e-10 and not any(np.abs(x - y).max() < 1e-7 for y in sols): sols.append(x)
    return tuple(S), b0, [list(x) for x in sols]
def record(orbs, S, xs):
    sols = []
    for x in xs:
        if not any(np.abs(np.array(x) - np.array(y)).max() < 1e-7 for y in sols): sols.append(x)
    sizes = [len(orbs[i]) for i in S]
    return dict(subset=list(S), sizes=sizes, N=sum(sizes), fams=[sorted(set(DFAM[j] for j in orbs[i])) for i in S],
                sols=[np.exp(np.r_[0.0, x]).tolist() for x in sols], nstarts=len(starts(len(S) - 1)))
if __name__ == '__main__':
    cls = json.load(open(sys.argv[1])); ci = int(sys.argv[2]); m = int(sys.argv[3]); si, sn = int(sys.argv[4]), int(sys.argv[5])
    npr = int(sys.argv[6]); out = sys.argv[7]
    C = cls[ci]; orbs = C['orbits']; k = len(orbs); Np = [tuple(p) for p in C['normaliser_perms']]
    reps = sorted({min(tuple(sorted(P[i] for i in S)) for P in Np) for S in itertools.combinations(range(k), m)})
    reps = [S for S in reps if bounded(DIRS[[j for i in S for j in orbs[i]]])]
    mine = reps[si::sn]
    import os
    done = set(); bdone = set(); blk = out + '.blocks'
    if os.path.exists(out):
        for L in open(out):
            try: r = json.loads(L)
            except Exception: continue
            if r['cls'] == ci and r['m'] == m: done.add(tuple(r['subset']))
    acc = {}; cnt = {}
    if os.path.exists(blk):
        for L in open(blk):
            try: r = json.loads(L)
            except Exception: continue
            if r['cls'] == ci and r['m'] == m:
                S = tuple(r['subset']); bdone.add((S, r['b'])); acc.setdefault(S, []).extend(r['xs']); cnt[S] = cnt.get(S, 0) + 1
    mine = [S for S in mine if tuple(S) not in done]
    print('class', ci, C['name'], 'm', m, 'bounded reduced subsets', len(reps), 'this slice', len(mine), flush=True)
    t0 = time.time()
    ns = len(starts(m - 1)); units = [(orbs, S, b) for S in mine for b in range(0, ns, BLOCK) if (tuple(S), b) not in bdone]
    nb = len(range(0, ns, BLOCK))
    print('units', len(units), flush=True)
    with Pool(npr) as pool, open(out, 'a') as fo, open(blk, 'a') as fb:
        for S, b, xs in pool.imap_unordered(solve_block, units):
            fb.write(json.dumps(dict(cls=ci, m=m, subset=list(S), b=b, xs=xs)) + '\n'); fb.flush()
            acc.setdefault(S, []).extend(xs); cnt[S] = cnt.get(S, 0) + 1
            if cnt[S] == nb:
                r = record(orbs, S, acc[S]); r.update(cls=ci, group=C['name'], m=m); fo.write(json.dumps(r) + '\n'); fo.flush()
    print('done', len(mine), 'sets', len(units), 'units in', round(time.time() - t0, 1), 's; FINAL ok', flush=True)
