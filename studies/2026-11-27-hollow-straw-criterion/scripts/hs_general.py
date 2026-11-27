"""Hollow-straw criterion, step 1 (27 Nov 2026; DICTO: "attack gap 1, the Hollow-straw criterion"). With Claude (Anthropic).
DICTO's Hollow-straw transformation for ANY core K and fair die D with the same number of faces: both ends fixed, each face plane of K
moves and turns into its partner face of D, all together: a_k(lam) = (1 - lam) a_k + lam m_sigma(k) (planes a . x = 1).
Question: WHEN is it nested (every intermediate solid inside the next, so the straws fill the shell without overlap), and does it then
use exactly the fewest swaps (one per neighbour pair to gain)? Step 1 is numerical exploration to find the pattern; anything found is
then proved exactly as for C116.
Per pair: (1) the core floats (floating resin, DICTO): random turns, assign faces by largest total cosine (Hungarian), refit the turn
(Kabsch, mirror allowed), repeat; keep the best; (2) neighbour pairs kept and swaps needed (edges - kept); (3) at core sizes rho (core
circumradius / die inradius) the transformation on a grid of lam: start and end patterns, every face present, nested (every face moving
outward at its corners), number of pattern changes, and whether the changes are exactly the needed swaps.
Usage: CORE=GPc_1_1|C116 DICE=1,18,27 RHO=0.5,0.7,0.9 python hs_general.py"""
import os, sys, json, time
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import HalfspaceIntersection
from scipy.spatial.transform import Rotation
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
argv = list(sys.argv); sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-vacuus-scutoids/scripts'))
import amber_aequus as A
sys.argv = argv
def pr(*a): print(*a, flush=True)
CORE = os.environ.get('CORE', 'GPc_1_1'); DICE = [int(x) for x in os.environ.get('DICE', '1').split(',')]
RHO = [float(x) for x in os.environ.get('RHO', '0.5,0.7,0.9').split(',')]; NG = int(os.environ.get('NG', 300)); NST = int(os.environ.get('NST', 200))
def core_planes(name):
    if name == 'C116':
        d = json.load(open(os.path.join(ST, '2026-11-24-aequi-vacuus-scutoids/data/c116/pairing.json'))); P = np.array(d['P']); out = []
        for f in d['faces']:
            X = P[f]; c0 = X.mean(0); n = np.linalg.svd(X - c0)[2][2]; n = n if n @ c0 > 0 else -n; out.append(n / (n @ c0))
        return np.array(out)
    import importlib.util
    g = os.path.join(ST, '2026-11-21-amber-goldberg/scripts')
    old = sys.modules.pop('resin', None)                    # the Goldberg study has its own resin.py (60-digit reals)
    spec_r = importlib.util.spec_from_file_location('resin', os.path.join(g, 'resin.py')); Rm = importlib.util.module_from_spec(spec_r)
    sys.modules['resin'] = Rm; spec_r.loader.exec_module(Rm)
    spec = importlib.util.spec_from_file_location('gsolids', os.path.join(g, 'solids.py')); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
    if old is not None: sys.modules['resin'] = old
    m, n = map(int, name.split('_')[1:3]); pts, ico, T = S.geodesic(m, n)
    if name.startswith('GPc_'): pts = S.canonical(pts, m, n)
    return np.array([[float(x) for x in p] for p in pts])
def poly(Aa):
    P = HalfspaceIntersection(np.hstack([Aa, -np.ones((len(Aa), 1))]), np.zeros(3)).intersections
    sc = np.abs(P).max(); pts = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in pts): pts.append(p)
    P = np.array(pts); tight = np.abs(Aa @ P.T - 1) < 1e-8
    faces = [set(np.where(tight[k])[0]) for k in range(len(Aa))]
    pairs = {(k, l) for k in range(len(Aa)) for l in range(k + 1, len(Aa)) if len(faces[k] & faces[l]) >= 2}
    return P, faces, pairs
def float_resin(Nc, Nd, rng):
    best = None
    for s in range(NST):
        R = Rotation.random(random_state=rng).as_matrix()
        if s % 2: R = -R                                   # mirror allowed
        for it in range(40):
            C = (Nc @ R.T) @ Nd.T; r, c = linear_sum_assignment(-C); sig = c
            H = Nc.T @ Nd[sig]; U, _, Vt = np.linalg.svd(H); R2 = (U @ Vt).T
            if np.allclose(R2, R, atol=1e-12): break
            R = R2
        tot = float(((Nc @ R.T) * Nd[sig]).sum(1).sum())
        if best is None or tot > best[0] + 1e-9: best = (tot, R, sig.copy())
    return best
OUTJ = os.path.join(HERE, f'../data/hs_{CORE}_{os.environ.get("TAG", "run")}.jsonl')   # one line per die, written at once
done_ = set()
if os.path.exists(OUTJ):
    for line in open(OUTJ): done_.add(json.loads(line)['die'])
res = []
Ac = core_planes(CORE); Nc = Ac / np.linalg.norm(Ac, axis=1)[:, None]
Pc, Fc, Ec = poly(Ac); rc = np.linalg.norm(Pc, axis=1).max()
pr(f'core {CORE}: {len(Ac)} faces, {len(Pc)} corners, {len(Ec)} neighbour pairs, sizes {sorted({len(f) for f in Fc})}')
for n in DICE:
    if n in done_: continue
    t0 = time.time()
    try: S = A.build(f'aequus-{n}')
    except Exception as ex: pr(f'die {n}: cannot build ({type(ex).__name__}): skipped'); continue
    Md = np.array([[float(x) for x in u] for u, c in S['planes']]) / np.array([float(c) for u, c in S['planes']])[:, None]
    if len(Md) != len(Ac): pr(f'die {n}: {len(Md)} faces, core {len(Ac)}: skipped'); continue
    Nd = Md / np.linalg.norm(Md, axis=1)[:, None]; Pd, Fd, Ed = poly(Md); rin = (1 / np.linalg.norm(Md, axis=1)).min()
    tot, R, sig = float_resin(Nc, Nd, np.random.default_rng(n))
    inv = {int(v): k for k, v in enumerate(sig)}
    Ed_c = {tuple(sorted((inv[a], inv[b]))) for a, b in Ed}
    kept = len(Ec & Ed_c); need = len(Ed_c - Ec); need_lose = len(Ec - Ed_c)
    simple = all(len(f) == 3 for f in [set(np.where(np.abs(Md @ p - 1) < 1e-8)[0]) for p in Pd])
    Rc = Nc @ R.T; facing = 0
    for k in range(len(Ac)):
        mk = Md[sig[k]]; dk = Rc[k]
        if mk @ dk > 0:
            pnt = dk / (mk @ dk); facing += int((Md @ pnt <= 1 + 1e-9).all())
    rec_facing = facing
    rec = dict(core=CORE, die=n, faces=len(Ac), die_simple=simple, cos_total=tot, facing=rec_facing, kept=kept, edges_core=len(Ec), edges_die=len(Ed), to_gain=need, to_lose=need_lose, by_rho=[])
    def nested_at(rho):
        a0 = (Ac @ R.T) * (rc / (rho * rin)); a1 = Md[sig]
        for lam in np.linspace(0, 1, NG + 1):
            Aa = (1 - lam) * a0 + lam * a1
            try: P, F, E = poly(Aa)
            except Exception: return False
            for k in range(len(Aa)):
                if F[k] and ((a1[k] - a0[k]) @ P[list(F[k])].T).max() > 1e-9: return False
        return True
    if os.environ.get('BISECT'):
        lo, hi = 0.3, 1.0
        if not nested_at(lo): rec['rho_star'] = None
        else:
            for _ in range(7):
                mid = (lo + hi) / 2
                if nested_at(mid): lo = mid
                else: hi = mid
            rec['rho_star'] = round(lo, 4)
        pr(f'  die {n}: facing {rec_facing} of {len(Ac)} faces; largest nested core size about {rec.get("rho_star")}')
    for rho in RHO:
        a0 = (Ac @ R.T) * (rc / (rho * rin))                # core turned, scaled: circumradius = rho * die inradius (rho < 1: core inside die)
        a1 = Md[sig]
        prev = None; events = []; nested = True; allf = True; ok_start = ok_end = None
        for i, lam in enumerate(np.linspace(0, 1, NG + 1)):
            Aa = (1 - lam) * a0 + lam * a1
            try: P, F, E = poly(Aa)
            except Exception: nested = False; allf = False; break
            if any(len(f) < 3 for f in F): allf = False
            for k in range(len(Aa)):
                if F[k] and ((a1[k] - a0[k]) @ P[list(F[k])].T).max() > 1e-9: nested = False
            if i == 0: ok_start = (E == Ec)
            if i == NG: ok_end = (E == Ed_c)
            if prev is not None and E != prev: events.append((float(lam), len(prev - E), len(E - prev)))
            prev = E
        lost = sum(e[1] for e in events); gained = sum(e[2] for e in events)
        rec['by_rho'].append(dict(rho=rho, start_ok=ok_start, end_ok=ok_end, all_faces=allf, nested=nested, events=len(events),
                                  lost=lost, gained=gained, minimal=(lost == need_lose and gained == need)))
        pr(f'  die {n} rho {rho}: nested {nested}, all faces {allf}, start/end ok {ok_start}/{ok_end}, pattern changes {len(events)}, '
           f'pairs lost {lost} gained {gained} (needed {need_lose}/{need}) -> minimal {lost == need_lose and gained == need}')
    res.append(rec); open(OUTJ, 'a').write(json.dumps(rec) + '\n')
    pr(f'die {n}: simple corners {simple}; kept {kept} of {len(Ec)}, to lose {need_lose}, to gain {need}, total cosine {tot:.4f}  ({time.time() - t0:.0f} s)')
    pr(f'PROGRESS {len(res) / len(DICE):.3f}')
out = os.path.join(HERE, f'../data/hs_{CORE}_{os.environ.get("TAG", "run")}.json'); json.dump(res, open(out, 'w'), indent=1)
pr('FINAL ok' if res else 'FINAL FAIL (no pairs)')
