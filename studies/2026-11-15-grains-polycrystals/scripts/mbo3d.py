"""3D curvature-driven grain growth on a periodic voxel grid by threshold dynamics (diffusion-generated motion).
GRAINS stream of "One tissue, three scales" (DICTO, 15 Nov 2026).

Method, credited: the MBO scheme (Merriman, Bence & Osher, J. Comput. Phys. 112 (1994) 334) in the multi-phase form of Esedoglu &
Otto (Comm. Pure Appl. Math. 68 (2015) 808): with equal boundary energies each voxel joins the grain whose Gaussian-smoothed
indicator is largest. The per-grain local windows follow Elsey, Esedoglu & Smereka (J. Comput. Phys. 228 (2009) 8015). The code
is written here from scratch with numpy/scipy. Physical time per step dt = sigma^2/2 (heat kernel of variance 2 dt).
To avoid lattice pinning the kernel width grows with the grains: sigma^2 = c * Rbar (Rbar = mean equivalent radius in voxels), so a
mean-curvature front moves about c voxels per step.
At each recorded frame: stray fragments of a grain (not its largest 6-connected piece) are given to their most common neighbour
grain; the contacts (pairs of grains sharing voxel faces) are written with their areas (number of voxel faces).
Output OUTDIR: frames3d.jsonl ({t, cells, contacts: [[a,b,area],...], vol: {g: voxels}}), stats.jsonl, final.json.
Usage: mbo3d.py OUTDIR n=128 N0=4000 Nend=500 c=1.5 sigmin=2.0 seed=1 rec_frac=0.01 maxwall=SECONDS"""
import sys, os, json, time, math
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

args = dict(a.split('=') for a in sys.argv[2:])
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
n = int(args.get('n', 128)); N0 = int(args.get('N0', 4000)); NEND = int(args.get('Nend', 500))
C = float(args.get('c', 1.5)); SIGMIN = float(args.get('sigmin', 2.0)); SEED = int(args.get('seed', 1))
REC = float(args.get('rec_frac', 0.01)); MAXWALL = float(args.get('maxwall', 1e9))
THR = (0.05, 0.1, 0.2)
T0 = time.time()
rng = np.random.default_rng(SEED)
seeds = rng.random((N0, 3)) * n
g = np.indices((n, n, n), dtype=np.float32).reshape(3, -1).T + 0.5
lab = cKDTree(seeds, boxsize=n).query(g, workers=4)[1].astype(np.int32).reshape(n, n, n)
del g
H = n // 2

def boxes(lab):
    """Per grain and axis the index range (start, length) on the torus, from the plain and the half-shifted views."""
    o1 = ndimage.find_objects(lab + 1)
    o2 = ndimage.find_objects(np.roll(lab, (H, H, H), (0, 1, 2)) + 1)
    out = {}
    for gi in range(len(o1)):
        a, b = o1[gi], o2[gi] if gi < len(o2) else None
        if a is None: continue
        rng_ = []
        for k in range(3):
            s1 = (a[k].start, a[k].stop - a[k].start)
            s2 = ((b[k].start - H) % n, b[k].stop - b[k].start) if b is not None else s1
            rng_.append(s1 if s1[1] <= s2[1] else s2)
        out[gi] = rng_
    return out

def contacts(lab):
    keys, cnts = [], []
    G = np.int64(lab.max() + 1)
    for k in range(3):
        a = lab; b = np.roll(lab, -1, k); m = a != b
        x, y = a[m].astype(np.int64), b[m].astype(np.int64)
        key = np.minimum(x, y) * G + np.maximum(x, y)
        u, c = np.unique(key, return_counts=True); keys.append(u); cnts.append(c)
    u, inv = np.unique(np.concatenate(keys), return_inverse=True)
    c = np.bincount(inv, np.concatenate(cnts)).astype(np.int64)
    return u // G, u % G, c

def defragment(lab):
    """Give every stray piece of a grain (not its largest 6-connected piece) to its most common face neighbour. Returns voxels moved."""
    moved = 0
    bx = boxes(lab)
    for gi, r in bx.items():
        ix = [np.arange(s, s + l + 2) % n if l + 2 <= n else np.arange(n) for (s, l) in [(s - 1, l) for s, l in r]]
        w = lab[np.ix_(*ix)]
        m = w == gi
        cc, k = ndimage.label(m)
        if k <= 1: continue
        sizes = np.bincount(cc.ravel()); sizes[0] = 0; keep = sizes.argmax()
        stray = (cc > 0) & (cc != keep)
        for piece in range(1, k + 1):
            if piece == keep: continue
            pm = cc == piece
            ring = ndimage.binary_dilation(pm) & ~pm
            nbl = w[ring]; nbl = nbl[nbl != gi]
            if len(nbl) == 0: continue
            w[pm] = np.bincount(nbl).argmax(); moved += int(pm.sum())
        lab[np.ix_(*ix)] = w
    return moved

fst = open(os.path.join(OUT, 'stats.jsonl'), 'w'); ffr = open(os.path.join(OUT, 'frames3d.jsonl'), 'w')
t = 0.0; step = 0; nframes = 0; moved_total = 0
small_faces = {th: {} for th in THR}
last_rec_N = None; status = 'running'

def record():
    global nframes, moved_total, last_rec_N
    moved_total += defragment(lab)
    vol = np.bincount(lab.ravel())
    alive = np.nonzero(vol)[0]
    a, b, c = contacts(lab)
    F = np.bincount(a, minlength=len(vol)) + np.bincount(b, minlength=len(vol))
    F4 = np.bincount(a[c >= 4], minlength=len(vol)) + np.bincount(b[c >= 4], minlength=len(vol))
    Vb = vol[alive].mean()
    for th in THR:
        d = small_faces[th]
        for gi in alive[vol[alive] < th * Vb]:
            if int(gi) not in d: d[int(gi)] = [int(F[gi]), int(F4[gi]), int(vol[gi])]
    fa = F[alive]; f4 = F4[alive]
    st = dict(t=t, step=step, N=int(len(alive)), Vbar=float(Vb), Rbar=float((3 * Vb / 4 / math.pi) ** (1 / 3)), sigma=float(sig),
              meanF=float(fa.mean()), mu2F=float(fa.var()), meanF4=float(f4.mean()), mu2F4=float(f4.var()),
              pF=np.bincount(fa, minlength=40)[:40].tolist(), moved=moved_total, wall=time.time() - T0)
    fst.write(json.dumps(st) + '\n'); fst.flush()
    ffr.write(json.dumps(dict(t=t, cells=alive.tolist(), contacts=np.stack([a, b, c], 1).tolist(),
                              vol={int(x): int(vol[x]) for x in alive})) + '\n'); ffr.flush()
    nframes += 1; last_rec_N = len(alive)

sig = SIGMIN
record()
next_prog = time.time()
while True:
    vol = np.bincount(lab.ravel()); alive = np.nonzero(vol)[0]; Nn = len(alive)
    if Nn <= NEND: status = 'done'; break
    if time.time() - T0 > MAXWALL: status = 'maxwall'; break
    Rb = (3 * vol[alive].mean() / 4 / math.pi) ** (1 / 3)
    sig = max(SIGMIN, math.sqrt(C * Rb))
    pad = int(math.ceil(3 * sig))
    bestv = np.full(lab.shape, -1.0, np.float32); bestl = lab.copy()
    for gi, r in boxes(lab).items():
        ix = [np.arange(s - pad, s + l + pad) % n if l + 2 * pad <= n else np.arange(n) for (s, l) in r]
        I = np.ix_(*ix)
        w = (lab[I] == gi).astype(np.float32)
        mode = ['constant' if len(x) < n else 'wrap' for x in ix]
        v = ndimage.gaussian_filter(w, sig, mode=mode, truncate=3.0)
        bv = bestv[I]; m = v > bv
        bv[m] = v[m]; bestv[I] = bv
        bl = bestl[I]; bl[m] = gi; bestl[I] = bl
    lab = bestl
    t += sig * sig / 2; step += 1
    vol = np.bincount(lab.ravel()); Nn = int((vol > 0).sum())
    if last_rec_N - Nn >= max(1, REC * last_rec_N): record()
    if time.time() > next_prog:
        print(f'PROGRESS {math.log(N0 / Nn) / math.log(N0 / NEND):.3f} N={Nn} t={t:.2f} step={step} sigma={sig:.2f}', flush=True)
        next_prog = time.time() + 30
record()
fst.close(); ffr.close()
sf = {}
for th, d in small_faces.items():
    v = np.array([x[0] for x in d.values()]); v4 = np.array([x[1] for x in d.values()])
    sf[str(th)] = dict(n=len(v), mean=float(v.mean()) if len(v) else None, mean_area4=float(v4.mean()) if len(v4) else None,
                       hist={str(i): int(c) for i, c in enumerate(np.bincount(v)) if c} if len(v) else {})
fin = dict(params=dict(n=n, N0=N0, Nend=NEND, c=C, sigmin=SIGMIN, seed=SEED, rec_frac=REC), status=status, t=t, steps=step,
           frames=nframes, defrag_moved=moved_total, faces_at_small_volume=sf, wall=time.time() - T0)
json.dump(fin, open(os.path.join(OUT, 'final.json'), 'w'), indent=1)
print('MBO3D', status, json.dumps(dict(steps=step, frames=nframes, moved=moved_total)))
