# deep_check.py (12 Nov 2026): survivors of the hopeful-piece hunt, tested on LARGER tori (more pieces per period) and a larger ball.
# For each poly-RD survivor (n cells): every fcc torus of index N, N a multiple of n with NMIN <= N <= NMAX (one per O_h orbit);
# SAT = periodic (killed N). Also the ball of radius RB. Uses hunt.py's functions unchanged (exec of its part above "modes").
# usage: deep_check.py <summary.json> NMIN NMAX RB
import sys, json, os, time
here = os.path.dirname(os.path.abspath(__file__)); SUM, NMIN, NMAX, RB = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
sys.argv = ['hunt.py', 'none']; exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
surv = [tuple(map(tuple, s[1])) for s in json.load(open(SUM))['survivors'] if s[0] == 'P']
log(f'{len(surv)} poly survivors; tori index {NMIN}..{NMAX} (multiples of n), ball R{RB}')
out = []
for si, P in enumerate(surv):
    n = len(P); reps, tot = tori(NMAX, list(range(48)), n); reps = [r for r in reps if r[0] >= NMIN]
    verdict = None
    for i, (N, M, c, nbr) in enumerate(reps):
        W = np.array(M) @ B3; Gi = np.linalg.inv(W.T.astype(float))
        def red(v, Gi=Gi, W=W):
            f = Gi @ np.array(v, float); f = f - np.floor(f + 1e-9); return tuple(np.rint(f @ W).astype(int).tolist())
        S = sorted({red(x) for x in torus_points(M)}); assert len(S) == N
        print(f'PROGRESS {(si + (i + 1) / len(reps)) / len(surv):.3f} survivor {si} torus {i + 1}/{len(reps)} index {N}', flush=True)
        if poly_sat(P, S, S, red): verdict = f'killed {N}'; break
    if verdict is None:
        bx = ball_xyz(RB); verdict = f'no torus {NMIN}..{NMAX}; ' + ('fills ball R%d' % RB if poly_sat(P, bx, bx, lambda y: y) else 'untileable R%d' % RB)
    log(f'survivor {si} {P}: {verdict}'); out.append([list(P), verdict])
json.dump(out, open(SUM.replace('.json', '') + '_deep.json', 'w'))   # 12 Nov fix: was one shared deep_check.json (six parts overwrote it; logs s*.log are the record)
print('FINAL ok', flush=True)
