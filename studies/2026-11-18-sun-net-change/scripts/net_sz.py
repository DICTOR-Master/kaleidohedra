"""Net change of neighbours after a fixed elapsed time tau, for one granulation setting, at several sampling steps.

Segments every snapshot once (tiles.segment, the census setting), then for each sampling step s tracks labels along every s-th
snapshot (tiles.match, mutual best overlap, the census rule) and records, at every sampled frame, the labels, their periodic
centroids and the contact pairs (pixel-edge adjacency, periodic). For start frames every START frames and every tau in TAUF:
survivors = labels present at both ends; net_lost / net_made = survivor pairs touching at the start and not at the end / the
reverse (the null study's definition, moving.py); all-label counts too; centroid displacement of survivors and change of
separation of survivor pairs touching at the start.

Usage: net_sz.py DATA RUN VAR DZ SIGMA [hmax:|thr:]H OUT.json [NFRAMES|all] [steps=1,2,4,8] [tauf=8,16,...]"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-17-sun-step-zero', 'scripts'))
import tiles as TL

START = 8          # starts every 8 snapshots (80 s): divisible by every step
BIG = 10 ** 7


def prep(img, var):
    return 10.0 ** img if var == 'lgtg' else img     # as census_sz.py


def pairs_of(lab):
    """Contact pairs (a < b) encoded a * BIG + b: labels sharing a pixel edge, periodic (= keys of tiles.graph contacts)."""
    out = []
    for B in (np.roll(lab, -1, 1), np.roll(lab, -1, 0)):
        m = lab != B
        a = np.minimum(lab[m], B[m]).astype(np.int64); b = np.maximum(lab[m], B[m]).astype(np.int64)
        out.append(a * BIG + b)
    return np.unique(np.concatenate(out))


def centroids(lab, L):
    """Periodic centroids (circular means) of every label: (ids, array n x 2) in pixels."""
    f = lab.ravel().astype(np.int64); M = int(f.max()) + 1
    yy, xx = np.divmod(np.arange(L * L), L)
    n = np.bincount(f, minlength=M); ids = np.nonzero(n)[0]
    c = []
    for co in (yy, xx):
        th = 2 * np.pi * co / L
        cs = np.bincount(f, weights=np.cos(th), minlength=M); sn = np.bincount(f, weights=np.sin(th), minlength=M)
        c.append((np.arctan2(sn, cs) * L / (2 * np.pi)) % L)
    return ids, np.stack(c, 1)[ids]


def wrap(d, L):
    return (d + L / 2) % L - L / 2


def run(data, run_, var, dz, sigma, h, out, nframes=None, method='thr', steps=(1, 2, 4, 8), tauf=(8, 16, 24, 32, 48, 64)):
    t0 = time.time()
    F = np.load(f'{data}/{run_}_{var}_dz{dz}.npy', mmap_mode='r')
    times = np.load(f'{data}/{run_}_times.npy')
    nt = len(times) if nframes is None else min(nframes, len(times))
    L = F.shape[1]
    raw = [TL.segment(prep(np.asarray(F[k]), var), sigma, h, method=method) for k in range(nt)]
    print(f'PROGRESS segment {nt} frames {time.time() - t0:.0f} s', flush=True)
    # check: pairs_of equals the keys of tiles.graph contacts on three frames
    chk = all(set((int(p // BIG), int(p % BIG)) for p in pairs_of(raw[k])) == set(TL.graph(raw[k])['contacts'])
              for k in (0, nt // 2, nt - 1))
    mean_cells = float(np.mean([len(np.unique(r)) for r in raw]))
    ell = (L * L / mean_cells) ** 0.5
    res = dict(run=run_, var=var, dz=dz, sigma=sigma, h=h, method=method, frames=nt, L_px=L, mean_cells=mean_cells, ell_px=ell,
               dt_s=float(np.median(np.diff(times))), start_every=START, pairs_check=bool(chk), steps={})
    for s in steps:
        rec = {}; prev = None; next_id = 1
        for k in range(0, nt, s):
            if prev is None:
                lab = raw[k].astype(np.int64); next_id = int(lab.max()) + 1
            else:
                lab, _, _, next_id = TL.match(prev, raw[k], next_id)
            prev = lab
            if k % START == 0:               # starts and ends (tau is a multiple of START)
                ids, cen = centroids(lab, L)
                rec[k] = (ids, cen, pairs_of(lab))
        R = {}
        for tf in tauf:
            rows = []
            for k0 in range(0, nt - tf, START):
                k1 = k0 + tf
                i0, c0, E0 = rec[k0]; i1, c1, E1 = rec[k1]
                S = np.intersect1d(i0, i1)
                a0, b0 = E0 // BIG, E0 % BIG; a1, b1 = E1 // BIG, E1 % BIG
                E0s = E0[np.isin(a0, S) & np.isin(b0, S)]; E1s = E1[np.isin(a1, S) & np.isin(b1, S)]
                lost = int(np.setdiff1d(E0s, E1s, assume_unique=True).size); made = int(np.setdiff1d(E1s, E0s, assume_unique=True).size)
                all_lost = int(np.setdiff1d(E0, E1, assume_unique=True).size); all_made = int(np.setdiff1d(E1, E0, assume_unique=True).size)
                p0 = {int(i): c0[j] for j, i in enumerate(i0)}; p1 = {int(i): c1[j] for j, i in enumerate(i1)}
                dS = np.array([wrap(p1[int(i)] - p0[int(i)], L) for i in S]) if len(S) else np.zeros((0, 2))
                d2 = float((dS ** 2).sum())
                disp = {int(i): dS[j] for j, i in enumerate(S)}
                rel2 = 0.0
                for p in E0s:
                    a, b = int(p // BIG), int(p % BIG)
                    rel2 += float(((disp[b] - disp[a]) ** 2).sum())
                rows.append([k0, len(i0), len(i1), int(S.size), int(E0s.size), int(E1s.size), lost, made, all_lost, all_made,
                             int(E0.size), int(E1.size), round(d2, 3), round(rel2, 3)])
            R[str(tf)] = dict(tau_s=tf * res['dt_s'], cols=['k0', 'n0', 'n1', 'surv', 'E0s', 'E1s', 'lost', 'made', 'all_lost',
                                                           'all_made', 'E0', 'E1', 'd2_px2', 'rel2_px2'], rows=rows)
            r = np.array(rows, float)
            if len(r):
                print(f'NET step {s} tau {tf * res["dt_s"]:.0f} s starts {len(r)} surv/cell {r[:, 3].sum() / r[:, 1].sum():.3f} '
                      f'net/surv {(r[:, 6] + r[:, 7]).sum() / r[:, 3].sum():.4f} D/l {np.sqrt(r[:, 12].sum() / r[:, 3].sum()) / ell:.4f}',
                      flush=True)
        res['steps'][str(s)] = R
        print(f'PROGRESS step {s} done {time.time() - t0:.0f} s', flush=True)
    res['wall_s'] = time.time() - t0
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    json.dump(res, open(out, 'w'))
    return res


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if '=' not in x]
    kw = dict(x.split('=') for x in sys.argv[1:] if '=' in x)
    data, run_, var, dz, sigma, h, out = a[:7]
    nf = int(a[7]) if len(a) > 7 and a[7] != 'all' else None
    method, hv = h.split(':')
    steps = tuple(int(x) for x in kw.get('steps', '1,2,4,8').split(','))
    tauf = tuple(int(x) for x in kw.get('tauf', '8,16,24,32,48,64').split(','))
    res = run(data, run_, var, dz, float(sigma), float(hv), out, nf, method, steps, tauf)
    ok = res['pairs_check'] and all(len(v['rows']) > 0 for R in res['steps'].values() for v in R.values())
    print(f'WALL {res["wall_s"]:.0f} s', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL (pairs check or empty tau)', flush=True)
