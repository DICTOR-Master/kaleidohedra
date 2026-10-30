# Star Cores, building on the star with SHORTER SPIKES IN THE VALLEYS (DICTO 2026-10-30). The local rule of star_build.py (tip = A + s
# (p - A), A the far point of the piece beneath the triangle, p the foot from A, full height s = t), but each spike is shortened until it
# touches no piece already built: s_i = the largest s in (1, t] with the spike free of every old piece (bisection, 30 halvings); then the
# new spikes are checked against each other and every clashing pair is shortened to a common s (the same rule for both, so symmetric
# triangles keep equal spikes) until none clash. Reported per step: triangles, how many spikes kept full height, the distinct heights
# (as fractions of full), radius and volume over the step before. t = phi and 2, steps 1-3. Usage: star_valley.py <ds> <star-cores.json> <out> [jobs]
import json, os, sys, numpy as np, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_core import faces_info, polyvol, vol, load
from star_build import axes
phi = (1 + 5 ** .5) / 2
DS, SC, OUT = sys.argv[1:4]; JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 8; STEPS = 3
def clash(Q, g1, P, g2):
    if g1 is None or g2 is None: return False
    (A1, c1, r1), (A2, c2, r2) = g1, g2
    if np.linalg.norm(c1 - c2) > r1 + r2 + 1e-9: return False
    for ax in A1[0] + A2[0] + [np.cross(u, v) for u in A1[1] for v in A2[1]]:
        nn = np.linalg.norm(ax)
        if nn < 1e-12: continue
        pa, pb = Q @ (ax / nn), P @ (ax / nn)
        if pa.max() <= pb.min() + 1e-7 or pb.max() <= pa.min() + 1e-7: return False
    return True
def geo(Q):
    if vol(Q) <= 1e-12: return None   # a flat spike (no height) takes no space
    try: return axes(Q), Q.mean(0), np.linalg.norm(Q - Q.mean(0), axis=1).max()
    except Exception: return None
def run(item):
    name, dnum, fn, t = item
    try:
        d, V, F = load(fn); V = V - V.mean(0)
        old = [np.vstack([V[f], np.zeros(3)]) for f in F]; OG = [geo(Q) for Q in old]; below = list(old)
        steps = []; R0 = np.linalg.norm(V, axis=1).max(); VOL0 = polyvol(V, F)
        for k in range(1, STEPS + 1):
            FI = faces_info(V, F); base = []
            for (f, n, c), P in zip(FI, below):
                h = (P - V[f[0]]) @ n; A = P[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
            spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
            def free_old(i, s):
                Q = spike(i, s); g = geo(Q); return not any(clash(Q, g, P, G) for P, G in zip(old, OG))
            S = []
            for i in range(len(base)):
                if free_old(i, t): S.append(t); continue
                lo, hi = 1.0, t
                for _ in range(30):
                    mid = (lo + hi) / 2
                    if free_old(i, mid): lo = mid
                    else: hi = mid
                S.append(lo)
            for _ in range(12):                                  # new spikes against each other
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
            V2 = list(V); F2 = []; B2 = []
            for i, (f, A, foot) in enumerate(base):
                if S[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); continue
                tip = A + S[i] * (foot - A); ti = len(V2); V2.append(tip); Q = np.vstack([V[f], tip]); old.append(Q); OG.append(geo(Q))
                for a in range(len(f)): F2.append([f[a], f[(a + 1) % len(f)], ti]); B2.append(Q)
            V2 = np.array(V2); R = np.linalg.norm(V2, axis=1).max(); VOL = polyvol(V2, F2)
            fr = [(s - 1) / (t - 1) for s in S]
            steps.append(dict(step=k, triangles=len(F2), full=sum(1 for x in fr if x > 1 - 1e-9), flat=sum(1 for x in fr if x < 1e-9),
                              height_kinds=sorted({round(x, 4) for x in fr}), radius_over_last=R / R0, volume_over_last=VOL / VOL0))
            V, F, below, R0, VOL0 = V2, F2, B2, R, VOL
            if len(F) > 2500: break
        return dict(name=name, D=dnum, t='phi' if t == phi else '2', steps=steps)
    except Exception as e:
        return dict(name=name, D=dnum, t='phi' if t == phi else '2', error=type(e).__name__ + ' ' + str(e).splitlines()[0][:120])
if __name__ == '__main__':
    sc = json.load(open(SC)); items = [(r['name'], r['D'], r['file'], t) for r in sc if r.get('pyramids_add_up') and r.get('faces', 999) <= 200 for t in (phi, 2.0)]
    out = []
    with mp.Pool(JOBS) as pool:
        for r in pool.imap_unordered(run, items):
            out.append(r); print(r['D'], r['name'][:30], r['t'], '|', r.get('error') or ' '.join(f"[{x['triangles']}t full{x['full']} flat{x['flat']} kinds{len(x['height_kinds'])} r{x['radius_over_last']:.4f} v{x['volume_over_last']:.4f}]" for x in r['steps']), flush=True)
            json.dump(out, open(os.path.join(OUT, 'star-valley.json'), 'w'), indent=1, default=float)
    print('done', len(out))
