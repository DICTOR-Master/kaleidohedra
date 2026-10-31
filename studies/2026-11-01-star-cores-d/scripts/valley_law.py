# Star Cores paper D (eccentric pieces): the valley law. For every edge e of a shape (faces f, f'), with O the centre (mean of the
# corners, as in star_valley.py), alpha = the angle at e between face f and the plane (O, e), so the solid's dihedral angle is
# delta = alpha + alpha'. Prediction: while the spikes at e are full, the k-th spike meets e at gamma_k = atan2((t-1)^k d_f, rho_fe)
# (d_f: distance of f's plane from O; rho_fe: signed distance in f's plane from the foot of O to the line of e), and the valley at e stays
# open through step k iff beta_k = 2 pi - delta - sum_{j<=k} (gamma_j + gamma'_j) >= 0.
# Part 1 (all shapes of star-valley.json): the predicted open valleys at steps 1-3 (t = 2, phi) and in the limit, against the full-spike
#   counts of star-valley.json (every step-2 triangle is a valley triangle of exactly one edge, so full_2 <= open_2 must hold).
# Part 2 (the seven eccentric pieces + controls): star_valley.py's run, instrumented: for each valley triangle at an edge of the solid,
#   its spike height s and the measured opening angle at e after the step, against the formula; and whether a valley that closed
#   (opening 0) ever grows again.
# Usage: valley_law.py <dataset dir> <star-cores.json> <out dir> [jobs]
import json, os, sys, math, numpy as np, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-10-30-star-cores/scripts'))   # star_core, star_valley, figs_paper_a
from star_core import faces_info, polyvol, vol, load
from star_valley import clash, geo
phi = (1 + 5 ** .5) / 2; TAU = 2 * math.pi
DS, SC, OUT = sys.argv[1:4]; JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 4
PIECES = ['D77', 'D80', 'D82', 'D6', 'D71', 'D81', 'D86']; CONTROLS = ['D7', 'D29', 'D41', 'D89', 'D40']

def edges(V, F):
    """{(a,b) sorted: [(face index, alpha, d, rho), ...]} with alpha = atan2(d, rho)."""
    FI = faces_info(V, F); E = {}
    for i, (f, n, d) in enumerate(FI):
        c = V[f].mean(0); p = d * n
        for k in range(len(f)):
            a, b = f[k], f[(k + 1) % len(f)]; u = V[b] - V[a]; u /= np.linalg.norm(u)
            w = (c - V[a]) - ((c - V[a]) @ u) * u; w /= np.linalg.norm(w)        # in-face direction away from the edge, into f
            rho = (p - V[a]) @ w
            E.setdefault(tuple(sorted((a, b))), []).append((i, math.atan2(d, rho), d, rho, n))
    return E
def gam(d, rho, t, j): return math.atan2((t - 1) ** j * d, rho)
def predict(V, F, t, K=3, KINF=60):
    E = edges(V, F); out = []
    for e, L in E.items():
        (i, a1, d1, r1, n1), (i2, a2, d2, r2, n2) = L
        delta = a1 + a2
        cosang = float(np.clip(n1 @ n2, -1, 1)); convex = np.cross(n1, n2) @ (V[e[1]] - V[e[0]])  # check delta against the normals
        dn = math.pi - math.acos(cosang)
        beta, b = [], TAU - delta
        for j in range(1, KINF + 1):
            b -= gam(d1, r1, t, j) + gam(d2, r2, t, j)
            if j <= K: beta.append(b)
        out.append(dict(e=e, delta=delta, delta_normals=dn, beta=beta, beta_lim=b))
    return out
def part1(r):
    d, V, F = load(r['file']); V = V - V.mean(0); res = dict(D=r['D'], name=r['name'], convex=r['convex'], edges=len(edges(V, F)))
    for tn, t in (('2', 2.0), ('phi', phi)):
        P = predict(V, F, t)
        res['max_delta_check'] = max(abs(p['delta'] - p['delta_normals']) for p in P if r['convex']) if r['convex'] else None
        res['delta_deg'] = sorted({round(math.degrees(p['delta']), 3) for p in P})
        res[tn] = dict(open=[2 * sum(1 for p in P if p['beta'][k] >= -1e-9) for k in range(3)],
                       open_lim=2 * sum(1 for p in P if p['beta_lim'] >= -1e-9),
                       closed_at_1=2 * sum(1 for p in P if p['beta'][0] < -1e-9))
    return res

def opening(V, a, b, x1, x2, inward):
    u = V[b] - V[a]; u = u / np.linalg.norm(u)
    def ang(x):
        w = (x - V[a]) - ((x - V[a]) @ u) * u; w = w / np.linalg.norm(w); return math.atan2(np.cross(inward, w) @ u, inward @ w) % TAU
    A1, A2, AR = ang(x1), ang(x2), 0.0
    arc = (A2 - A1) % TAU
    return TAU - arc if (AR - A1) % TAU < arc else arc
def part2(item):
    D, name, fn, t = item
    d, V, F = load(fn); V = V - V.mean(0); n0 = len(V)
    E = edges(V, F); P = {p['e']: p for p in predict(V, F, t)}
    inward = {e: -(L[0][4] + L[1][4]) / np.linalg.norm(L[0][4] + L[1][4]) for e, L in E.items()}
    old = [np.vstack([V[f], np.zeros(3)]) for f in F]; OG = [geo(Q) for Q in old]; below = list(old)
    log = []; closed = set(); regrow = 0; formula_err = 0.0; viol = 0
    for k in range(1, 4):
        FI = faces_info(V, F); base = []
        for (f, n, c), Pc in zip(FI, below):
            h = (Pc - V[f[0]]) @ n; A = Pc[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
        spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
        def free_old(i, s):
            Q = spike(i, s); g = geo(Q); return not any(clash(Q, g, Pq, G) for Pq, G in zip(old, OG))
        S = []
        for i in range(len(base)):
            if free_old(i, t): S.append(t); continue
            lo, hi = 1.0, t
            for _ in range(30):
                mid = (lo + hi) / 2
                if free_old(i, mid): lo = mid
                else: hi = mid
            S.append(lo)
        for _ in range(12):
            Qs = [spike(i, s) for i, s in enumerate(S)]; Gs = [geo(Q) if s > 1 + 1e-9 else None for Q, s in zip(Qs, S)]
            pairs = [(i, j) for i in range(len(S)) for j in range(i + 1, len(S)) if Gs[i] and Gs[j] and clash(Qs[i], Gs[i], Qs[j], Gs[j])]
            if not pairs: break
            for i, j in pairs:
                lo, hi = 1.0, min(S[i], S[j])
                for _ in range(30):
                    mid = (lo + hi) / 2; A_, B_ = spike(i, min(S[i], mid)), spike(j, min(S[j], mid))
                    if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                    else: lo = mid
                S[i] = min(S[i], lo); S[j] = min(S[j], lo)
        # valley triangles at the solid's edges (step >= 2: triangles holding both ends of an edge e)
        val = {}
        if k >= 2:
            for i, (f, A, foot) in enumerate(base):
                for e in E:
                    if e[0] in f and e[1] in f: val.setdefault(e, []).append(i)
        V2 = list(V); F2 = []; B2 = []; tipof = {}
        for i, (f, A, foot) in enumerate(base):
            if S[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); tipof[i] = None; continue
            tip = A + S[i] * (foot - A); ti = len(V2); V2.append(tip); Q = np.vstack([V[f], tip]); old.append(Q); OG.append(geo(Q)); tipof[i] = tip
            for a in range(len(f)): F2.append([f[a], f[(a + 1) % len(f)], ti]); B2.append(Q)
        V2 = np.array(V2); rows = []
        for e, ii in val.items():
            if len(ii) != 2: continue
            fr = [(S[i] - 1) / (t - 1) for i in ii]
            x = [tipof[i] if tipof[i] is not None else V[[v for v in base[i][0] if v not in e][0]] for i in ii]
            b = opening(V2, e[0], e[1], x[0], x[1], inward[e])
            full_before = all(r_['full'] for r_ in log if r_['e'] == e)
            pred = P[e]['beta'][k - 1]
            if all(f_ > 1 - 1e-9 for f_ in fr) and full_before: formula_err = max(formula_err, abs(b - pred))
            if pred < -1e-9 and full_before and all(f_ > 1 - 1e-9 for f_ in fr): viol += 1          # closed by the formula, yet both full
            if e in closed and any(f_ > 1e-6 for f_ in fr): regrow += 1
            rows.append(dict(e=e, full=all(f_ > 1 - 1e-9 for f_ in fr), frac=fr, opening=b, predicted=pred, full_before=full_before))
            if b < 1e-6: closed.add(e)
        log += rows
        n_open = sum(1 for r_ in rows if r_['opening'] > 1e-6)
        print(D, name[:20], 'phi' if t == phi else '2', 'step', k, 'valleys', len(rows), 'open', n_open, 'closed', len(closed), flush=True)
        V, F, below = V2, F2, B2
    return dict(D=D, name=name, t='phi' if t == phi else '2', formula_max_err=formula_err, closed_yet_full=viol, regrown_after_closing=regrow,
                closed_edges=len(closed), edges=len(E), steps=[dict(step=k, valleys=sum(1 for r_ in log if r_.get('k') == k)) for k in (2, 3)],
                rows=[dict(e=list(r_['e']), full=r_['full'], frac=r_['frac'], opening=r_['opening'], predicted=r_['predicted']) for r_ in log])
if __name__ == '__main__':
    sc = json.load(open(SC)); sv = json.load(open(os.path.join(os.path.dirname(SC), 'star-valley.json')))
    names = {r['D'] for r in sv}
    p1 = [part1(r) for r in sc if r['D'] in names]
    json.dump(p1, open(os.path.join(OUT, 'valley-law-predict.json'), 'w'), indent=1, default=float); print('part 1:', len(p1), 'shapes', flush=True)
    items = [(r['D'], r['name'], r['file'], t) for r in sc if r['D'] in PIECES + CONTROLS for t in (2.0, phi)]
    with mp.Pool(JOBS) as pool: p2 = pool.map(part2, items)
    json.dump(p2, open(os.path.join(OUT, 'valley-law-run.json'), 'w'), indent=1, default=float)
    for r in p2: print(r['D'], r['name'][:24], r['t'], 'formula err %.2e' % r['formula_max_err'], 'closed-yet-full', r['closed_yet_full'], 'regrown', r['regrown_after_closing'], 'closed', r['closed_edges'], '/', r['edges'])
