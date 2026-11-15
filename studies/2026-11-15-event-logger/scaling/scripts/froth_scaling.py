"""Large dry 2D Potts froth run into its scaling state, for the Rutenberg-McCurdy count (One tissue, three scales; DICTO, 15 Nov 2026).

Model: the foam ladder's rung 1 (../../../2026-11-15-interstellar-bubbles/scripts/potts.py, unchanged): large-Q Potts model of a
coarsening dry froth (Glazier, Gross & Stavans 1987; Anderson, Srolovitz, Grest & Sahni 1984), 8-neighbour energy, Metropolis at
temperature T, periodic Voronoi start. Frames are built with tiles.py (the Sun stream's graph rules) exactly as foam_pairing.py /
rm_foam.py do, with one difference fixed before any run: clean_fragments is applied to a COPY of the label map for every recorded
frame and statistic, so the dynamics do not depend on how often frames are saved.

Output (OUTDIR):
  stats.jsonl   every `stats` MCS from the start: N, <A>, p(n) (n = distinct 4-adjacent neighbours, the logger's side number;
                beside it n2 = neighbours sharing at least 2 pixel edges, added after the pilot showed mu2 near 2.05 for n),
                mu2 = <(n - <n>)^2>, histogram of A/<A> (bins of 0.1 up to 6), and the von Neumann tally (dA/dt per n for cells that
                exist in both of two consecutive stat frames and keep the same n in both).
  frames.jsonl.gz  logger frames at EVERY MCS for win0 <= t < win1 (the scaling window, fixed before the run).
  areas.jsonl.gz   cell areas (pixels) of the same frames, one line each.
  final.json    parameters, run time, status.
Usage: froth_scaling.py OUTDIR L=2048 N0=262144 T=0.3 mcs=6000 stats=10 win0=1000 win1=6000 seed=1 maxwall=SECONDS"""
import sys, os, json, gzip, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
LOGGER = os.path.join(HERE, '..', '..', 'scripts')
FOAM = os.path.join(HERE, '..', '..', '..', '2026-11-15-interstellar-bubbles', 'scripts')
sys.path.insert(0, LOGGER); sys.path.insert(0, FOAM)
import eventlog as EL
import tiles, potts

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
P_ = dict(a.split('=', 1) for a in sys.argv[2:])
g = lambda k, d: type(d)(P_.get(k, d))
L, N0, Tm, MCS, ST = g('L', 2048), g('N0', 262144), g('T', 0.3), g('mcs', 6000), g('stats', 10)
W0, W1, seed, MAXWALL = g('win0', 1000), g('win1', 6000), g('seed', 1), g('maxwall', 1e9)
rng = np.random.default_rng(seed)
t0 = time.time()
BINS = np.arange(0, 6.01, 0.1)


def sides(lab):
    """Distinct 4-adjacent neighbours per label (periodic), the side number used by the logger frames."""
    pairs = []
    for B in (np.roll(lab, -1, 1), np.roll(lab, -1, 0)):
        m = lab != B
        pairs.append(np.stack([np.minimum(lab[m], B[m]), np.maximum(lab[m], B[m])], 1))
    up, cnt = np.unique(np.concatenate(pairs), axis=0, return_counts=True)
    m = int(lab.max()) + 1
    return np.bincount(up.ravel(), minlength=m), np.bincount(up[cnt >= 2].ravel(), minlength=m)


lab = potts.voronoi_labels((L, L), N0, rng)
sim = potts.Potts(lab, T=Tm, Jbl=None, rng=rng, nmax=N0 + 1)
fst = open(os.path.join(OUT, 'stats.jsonl'), 'w')
ffr = gzip.open(os.path.join(OUT, 'frames.jsonl.gz'), 'wt', compresslevel=3)
far = gzip.open(os.path.join(OUT, 'areas.jsonl.gz'), 'wt', compresslevel=3)
prev = None; nfr = 0; status = 'done'; moved_tot = 0
for step in range(MCS + 1):
    if step > 0: sim.sweep()
    t = step
    want_stat, want_frame = (t % ST == 0), (W0 <= t < W1)
    if want_stat or want_frame:
        cl, moved = tiles.clean_fragments(sim.lab.copy()); moved_tot += moved
        A = np.bincount(cl.ravel())
        if want_stat:
            ns, ns2 = sides(cl); alive = np.nonzero(A)[0]
            n = ns[alive]; n2 = ns2[alive]; a = A[alive].astype(float); Ab = a.mean()
            vn = {}
            if prev is not None:
                pt, pA, pns = prev; k = min(len(pA), len(A))
                keep = np.nonzero((A[:k] > 0) & (pA[:k] > 0) & (ns[:k] == pns[:k]))[0]
                r = (A[keep] - pA[keep]) / (t - pt)
                for kk in range(3, 13):
                    s = r[ns[keep] == kk]
                    if len(s): vn[kk] = [int(len(s)), float(s.sum()), float((s * s).sum())]
            prev = (t, A.copy(), ns.copy())
            h = np.histogram(a / Ab, BINS)[0]
            st = dict(t=t, N=int(len(alive)), Abar=float(Ab), mean_n=float(n.mean()), mu2=float(((n - n.mean()) ** 2).mean()),
                      p={int(k): int(c) for k, c in zip(*np.unique(n, return_counts=True))}, area_hist=h.tolist(),
                      mean_n2=float(n2.mean()), mu2_n2=float(((n2 - n2.mean()) ** 2).mean()),
                      p_n2={int(k): int(c) for k, c in zip(*np.unique(n2, return_counts=True))},
                      area_over=int((a / Ab >= 6).sum()), vn=vn, moved=int(moved), wall=round(time.time() - t0, 1))
            fst.write(json.dumps(st) + '\n'); fst.flush()
        if want_frame:
            G = tiles.graph(cl)
            T = tiles.to_tiling(EL.Tiling, cl, G, t)
            d = json.loads(T.to_json()); d['torus_euler'] = int(tiles.torus_euler(len(T.cells), G)); d['loops'] = int(G['loops'])
            ffr.write(json.dumps(d) + '\n')
            alive = np.nonzero(A)[0]
            far.write(json.dumps({str(int(c)): int(A[c]) for c in alive}) + '\n'); nfr += 1
    if step % max(1, MCS // 200) == 0:
        print(f'PROGRESS {step / MCS:.3f} mcs {step}/{MCS} cells {int((np.bincount(sim.lab.ravel()) > 0).sum())} frames {nfr} '
              f'wall {time.time() - t0:.0f} s', flush=True)
    if time.time() - t0 > MAXWALL: status = 'maxwall'; break
ffr.close(); far.close(); fst.close()
fin = dict(params=dict(L=L, N0=N0, T=Tm, mcs=MCS, stats=ST, win0=W0, win1=W1, seed=seed), status=status, last_mcs=step,
           frames=nfr, pixels_reassigned_in_copies=moved_tot, seconds=round(time.time() - t0, 1))
json.dump(fin, open(os.path.join(OUT, 'final.json'), 'w'), indent=1)
print('FROTH', json.dumps(fin))
print('FROTH_OK' if status == 'done' and nfr == max(0, min(W1, MCS + 1) - W0) else 'FROTH_FAIL')
