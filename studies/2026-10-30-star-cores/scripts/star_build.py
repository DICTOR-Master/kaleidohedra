# Star Cores, study 0b (DICTO 2026-10-30: "build on those stars pointing out and see what arises", "perhaps both approaches to see what
# numbers fall out"). Approach B, building on the star: S0 = the shape (from its centre), S1 = its star (every face replaced by the side
# triangles of its spike, tip t x the foot of the perpendicular from the centre), S2 = the star of S1 (every triangle of S1 spiked the
# same way), S3 likewise. Approach A (wrapping: the hull of the tips) is study 0 (star_core.py); both are tabulated side by side.
# Per step: triangles, faces facing the centre or through it (no spike possible), triangle shapes (by sorted edge lengths), outer radius
# and volume as multiples of the step before, and overlaps among all convex pieces built so far (S0's pyramids + every spike), by the
# separating-axis test with a bounding-sphere filter. t = phi and 2.
# RULE=local (DICTO 10-30, "try the local spike rule too"): the tip over each triangle is placed from the piece directly beneath it,
# not from the centre: with A the point of that piece farthest from the triangle's plane (ties averaged) and p the foot of the
# perpendicular from A, tip = A + t (p - A). For the first step the piece beneath each face is its pyramid from the centre, A = the
# centre, so the rule is exactly #78's; later steps spike each triangle from its own spike. Usage: star_build.py <dataset dir> <star-cores.json> <out dir> [jobs]
import json, os, sys, itertools, multiprocessing as mp, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_core import faces_info, polyvol, vol, load
phi = (1 + 5 ** .5) / 2
RULE = os.environ.get('RULE', 'centre')
DS, SC, OUT = sys.argv[1:4]; JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 8; STEPS = 3
def axes(Q):
    hq = ConvexHull(Q); ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return [eq[:3] for eq in hq.equations], [Q[b] - Q[a] for a, b in ed]
class Pieces:
    def __init__(s): s.P, s.A, s.C, s.R = [], [], [], []
    def add(s, Q):
        if vol(Q) <= 1e-12: return 0
        A = axes(Q); c = Q.mean(0); r = np.linalg.norm(Q - c, axis=1).max(); bad = 0
        for P2, A2, c2, r2 in zip(s.P, s.A, s.C, s.R):
            if np.linalg.norm(c - c2) > r + r2 + 1e-9: continue
            for ax in A[0] + A2[0] + [np.cross(u, v) for u in A[1] for v in A2[1]]:
                nn = np.linalg.norm(ax)
                if nn < 1e-12: continue
                pa, pb = Q @ (ax / nn), P2 @ (ax / nn)
                if pa.max() <= pb.min() + 1e-7 or pb.max() <= pa.min() + 1e-7: break
            else: bad += 1
        s.P.append(Q); s.A.append(A); s.C.append(c); s.R.append(r); return bad
def tri_kind(V, f): return tuple(sorted(round(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])), 5) for i in range(len(f))))
def run(item):
    name, dnum, fn, t = item
    try:
        d, V, F = load(fn); V = V - V.mean(0)
        pcs = Pieces(); [pcs.add(np.vstack([V[f], np.zeros(3)])) for f in F]
        below = [np.vstack([V[f], np.zeros(3)]) for f in F]            # the piece beneath each face
        steps = []; R0 = np.linalg.norm(V, axis=1).max(); VOL0 = polyvol(V, F)
        for k in range(1, STEPS + 1):
            FI = faces_info(V, F); V2 = list(V); F2 = []; B2 = []; blocked = 0; over = 0
            for (f, n, c), P in zip(FI, below):
                if RULE == 'local':
                    h = (P - V[f[0]]) @ n; far = P[np.abs(h - h.min()) < 1e-9]; A = far.mean(0)
                    if h.min() > -1e-12: blocked += 1; F2.append(list(f)); B2.append(P); continue
                    foot = A + (c - A @ n) * n; tip = A + t * (foot - A)
                else:
                    if c <= 1e-9: blocked += 1; F2.append(list(f)); B2.append(P); continue
                    tip = t * c * n
                ti = len(V2); V2.append(tip); Q = np.vstack([V[f], tip])
                over += pcs.add(Q)
                for i in range(len(f)): F2.append([f[i], f[(i + 1) % len(f)], ti]); B2.append(Q)
            V2 = np.array(V2); R = np.linalg.norm(V2, axis=1).max(); VOL = polyvol(V2, F2)
            steps.append(dict(step=k, triangles=len(F2), blocked_faces=blocked, triangle_kinds=len({tri_kind(V2, f) for f in F2}),
                              radius_over_last=R / R0, volume_over_last=VOL / VOL0, overlaps_new=over))
            V, F, below, R0, VOL0 = V2, F2, B2, R, VOL
            if over or len(F) > 6000: break
        return dict(name=name, D=dnum, t='phi' if t == phi else '2', steps=steps)
    except Exception as e:
        return dict(name=name, D=dnum, t='phi' if t == phi else '2', error=type(e).__name__ + ' ' + str(e).splitlines()[0][:120])
if __name__ == '__main__':
    sc = json.load(open(SC)); items = [(r['name'], r['D'], r['file'], t) for r in sc if r.get('pyramids_add_up') for t in (phi, 2.0)]
    out = []
    with mp.Pool(JOBS) as pool:
        for r in pool.imap_unordered(run, items):
            out.append(r); s = r.get('steps', []); print(r['D'], r['name'], r['t'], '|', r.get('error') or ' '.join(f"{x['triangles']}t r{x['radius_over_last']:.4f} v{x['volume_over_last']:.4f} ov{x['overlaps_new']} bl{x['blocked_faces']}" for x in s), flush=True)
            json.dump(out, open(os.path.join(OUT, f'star-build-{RULE}.json'), 'w'), indent=1, default=float)
    print('done', len(out))
