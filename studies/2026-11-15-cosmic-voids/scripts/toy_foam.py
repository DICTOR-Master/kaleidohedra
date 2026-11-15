"""TOY for the cosmic-voids workstream of "One tissue, three scales" (DICTO, 15 Nov 2026): a 3D Voronoi foam (or power diagram)
of N slowly moving centres in a periodic unit box, with every topological event resolved one at a time.

Geometry: the power diagram of centres x_i with weights w_i is dual to the regular triangulation = lower convex hull of the lifted
points (x_i, |x_i|^2 - w_i) in R^4 (all weights 0: the Voronoi foam and the Delaunay triangulation). Qhull (Barber, Dobkin &
Huhdanpaa 1996) through scipy.spatial.ConvexHull computes the hull. Periodicity: centres within a margin m of the box faces are copied
across (all 26 neighbouring boxes); every kept simplex is checked to have its orthosphere inside the copied region (else the frame
FAILS). Robustness: the same frame is recomputed after a random periodic shift of all centres (same foam, different floating-point
input); any disagreement marks the frame near-degenerate and is counted.

Two cells are in contact when they share a 2D face = a Delaunay (regular) edge. A cell exists when its centre is a vertex of the
regular triangulation (in a power diagram a centre can be hidden: its cell is empty).

Events between times t0 < t1: the change of the contact set and the set of existing cells. If more than one elementary change happened
(one contact gained, one contact lost, one cell born with its 4 contacts, one cell died with its 4), the interval is halved until each
piece holds at most one change or is shorter than dtmin; a piece still holding several changes at dtmin is a SIMULTANEOUS event (a clump:
what Theorem 1' of #104 says does not happen for generic motion). The frames at all piece ends are passed in time order to the shared
event logger (studies/2026-11-15-event-logger/scripts/eventlog.py, imported unchanged; 3D vocabulary).

Motions: centres x_i(t) = x_i(0) + v_i t (mod 1), v_i Gaussian with r.m.s. speed s per component, in units of the mean spacing
h = N^(-1/3) per unit time. Weights: 'voronoi' (all 0); 'wiggle' (w_i(t) = A h^2 sin(omega_i t + phi_i), independent); 'walk' (two
classes of centres, random halves; the light class has weight -Delta(t), Delta(t) = A h^2 t / T rising linearly: the weight walk of
#51/#53/#56/#57, here on random centres); 'lattice' (NEGATIVE CONTROL: centres pass through the simple cubic lattice at t = T/2,
a degenerate configuration with 8 centres on each empty sphere).

Usage: toy_foam.py OUT.json N mode T dt0 dtmin s A seed workers [nwin]"""
import sys, os, json, time, itertools
import numpy as np
from multiprocessing import Pool
from collections import Counter, defaultdict
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-11-15-event-logger', 'scripts'))
import eventlog as EL

OFFS = np.array([o for o in itertools.product((-1, 0, 1), repeat=3) if o != (0, 0, 0)], float)


class Foam:
    def __init__(self, N, mode, T, s, A, seed):
        self.N, self.mode, self.T, self.A = N, mode, T, A
        rng = np.random.default_rng(seed)
        self.h = N ** (-1 / 3)
        if mode == 'lattice':
            n = round(N ** (1 / 3)); assert n ** 3 == N, 'lattice control needs N = n^3'
            g = (np.array(list(itertools.product(range(n), repeat=3)), float) + 0.5) / n
            self.v = rng.normal(0, s * self.h, (N, 3)); self.x0 = g - self.v * (T / 2)
        else:
            self.x0 = rng.random((N, 3)); self.v = rng.normal(0, s * self.h, (N, 3))
        self.om = rng.uniform(0.5, 1.5, N) * 2 * np.pi / T; self.ph = rng.uniform(0, 2 * np.pi, N)
        self.cls = rng.random(N) < 0.5
        self.shift = rng.random(3)
        wmax = A * self.h ** 2 if mode in ('wiggle', 'walk') else 0.0
        self.margin = min(0.5, 3.0 * self.h + wmax / self.h)

    def at(self, t):
        x = (self.x0 + self.v * t) % 1.0
        if self.mode == 'wiggle': w = self.A * self.h ** 2 * np.sin(self.om * t + self.ph)
        elif self.mode == 'walk': w = np.where(self.cls, -self.A * self.h ** 2 * t / self.T, 0.0)
        else: w = np.zeros(self.N)
        return x, w

    def state(self, t, shifted=False):
        """(alive frozenset, contacts frozenset of (i, j) i < j, n_tets, n_tris, ok_margin)."""
        x, w = self.at(t)
        if shifted: x = (x + self.shift) % 1.0
        m = self.margin
        P, I = [x], [np.arange(self.N)]
        for o in OFFS:
            y = x + o
            k = np.all((y > -m) & (y < 1 + m), axis=1)
            P.append(y[k]); I.append(np.nonzero(k)[0])
        P = np.concatenate(P); I = np.concatenate(I); W = w[I]
        lift = np.c_[P, (P ** 2).sum(1) - W]
        hull = ConvexHull(lift)
        low = hull.equations[:, 3] < 0
        S = hull.simplices[low]
        orig = S < self.N                                    # vertex is an original (unshifted copy) centre
        keep = orig.any(1)
        S = S[keep]
        # orthosphere check on kept simplices: centre c, radius^2 = |c - p|^2 - w_p
        eq = hull.equations[low][keep]
        c = -eq[:, :3] / (2 * eq[:, 3:4])
        p0 = P[S[:, 0]]; r2 = ((c - p0) ** 2).sum(1) - W[S[:, 0]]
        r = np.sqrt(np.maximum(r2, 0))
        ok_margin = bool(np.all((c - r[:, None] > -m) & (c + r[:, None] < 1 + m)))
        ids = I[S]
        # canonical copy of each simplex: the copy whose smallest-id vertex is the original centre
        def canon(simp_pos, simp_ids):
            amin = np.argmin(simp_ids, 1)
            return (simp_pos[np.arange(len(simp_pos)), amin] < self.N)
        tets = canon(S, ids)
        n_tet = int(tets.sum())
        # contacts and triangles from all kept simplices, deduplicated by sorted id tuples (encoded as integers)
        q = np.sort(ids, 1).astype(np.int64)
        n = self.N
        E = np.unique(np.concatenate([q[:, a] * n + q[:, b] for a, b in itertools.combinations(range(4), 2)]))
        F = np.unique(np.concatenate([(q[:, a] * n + q[:, b]) * n + q[:, c] for a, b, c in itertools.combinations(range(4), 3)]))
        alive = frozenset(np.unique(ids).tolist())
        E = frozenset(E.tolist())
        distinct = bool(all(len(set(q)) == 4 for q in ids.tolist()))   # no simplex holds two copies of one centre
        return alive, E, n_tet, len(F), ok_margin and distinct


foam_N = [0]


def elementary(A, B):
    """Number of elementary changes from state A to B (0, 1, or 2 meaning 'more than one')."""
    born, died = B[0] - A[0], A[0] - B[0]
    gained, lost = B[1] - A[1], A[1] - B[1]
    if not born and not died: n = len(gained) + len(lost); return min(n, 2)
    if len(born) == 1 and not died and not lost and len(gained) == 4 and all(next(iter(born)) in divmod(p, foam_N[0]) for p in gained): return 1
    if len(died) == 1 and not born and not gained and len(lost) == 4 and all(next(iter(died)) in divmod(p, foam_N[0]) for p in lost): return 1
    return 2


def resolve(foam, t0, t1, S0, S1, dtmin, out, stats):
    """Append (t, state) pieces in time order between t0 and t1 so that consecutive states differ by <= 1 elementary change."""
    k = elementary(S0, S1)
    if k <= 1 or t1 - t0 < dtmin:
        if k > 1: stats['simultaneous'] += 1
        out.append((t1, S1)); return
    tm = 0.5 * (t0 + t1); Sm = foam.state(tm); stats['evals'] += 1
    if not Sm[4]: stats['margin_fail'] += 1
    resolve(foam, t0, tm, S0, Sm, dtmin, out, stats)
    resolve(foam, tm, t1, Sm, S1, dtmin, out, stats)


def tiling(t, S):
    n = foam_N[0]
    return EL.Tiling([str(i) for i in S[0]], [(str(p // n), str(p % n)) for p in S[1]], dim=3, surface='space', t=t)


def window(args):
    """Resolve one time window; log events with the shared logger; collect per-cell data."""
    N, mode, T, s, A, seed, ta, tb, dt0, dtmin = args
    foam = Foam(N, mode, T, s, A, seed); foam_N[0] = N
    stats = Counter(); deg_samples = []
    times = np.arange(ta, tb + 1e-12, dt0)
    if times[-1] < tb - 1e-12: times = np.append(times, tb)
    S = foam.state(times[0]); stats['evals'] += 1
    base = [(times[0], S)]
    counts, patterns = Counter(), Counter()
    events = []          # (t, type, cells)
    prev_T = tiling(times[0], S)
    euler_fail = 0; robust_fail = 0; bal_fail = 0
    def frame_checks(St):
        nonlocal euler_fail
        alive, E, nt, nf, okm = St
        if len(alive) - len(E) + nf - nt != 0: euler_fail += 1
        if not okm: stats['margin_fail'] += 1
    frame_checks(S)
    for t0, t1 in zip(times[:-1], times[1:]):
        S1 = foam.state(t1); stats['evals'] += 1; frame_checks(S1)
        R = foam.state(t1, shifted=True); stats['evals'] += 1
        if R[0] != S1[0] or R[1] != S1[1]: robust_fail += 1
        base.append((t1, S1))
        pieces = []
        resolve(foam, t0, t1, S, S1, dtmin, pieces, stats)
        for tp, Sp in pieces:
            B = tiling(tp, Sp)
            ev = EL.classify(prev_T, B)
            ok, _, _ = EL.balance(prev_T, B, ev)
            if not ok: bal_fail += 1
            for e in ev:
                counts[e['type']] += 1
                if e['type'] == 'clump': patterns[e['pattern']] += 1
                events.append((float(tp), e['type'], e['cells']))
            prev_T = B
        S = S1
        deg_samples.append(2 * len(S[1]) / len(S[0]))
    # coarse logs: the same base frames at steps 1, 2, 5, 10 x dt0 through the logger (no bisection)
    coarse = {}
    for k in (1, 2, 5, 10):
        fr = [tiling(t, St) for t, St in base[::k]]
        if (len(base) - 1) % k: fr.append(tiling(*base[-1]))
        c = Counter()
        for X, Y in zip(fr, fr[1:]):
            for e in EL.classify(X, Y): c[e['type']] += 1
        coarse[k] = dict(c)
    return dict(ta=ta, tb=tb, counts=dict(counts), patterns=dict(patterns), events=events, stats=dict(stats), euler_fail=euler_fail,
                robust_fail=robust_fail, balance_fail=bal_fail, deg=deg_samples, coarse=coarse, nbase=len(base),
                alive_end=sorted(base[-1][1][0]) if tb >= T - 1e-12 else None, alive_start=sorted(base[0][1][0]) if ta <= 1e-12 else None)


def main():
    out, N, mode, T, dt0, dtmin, s, A, seed, workers = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), \
        float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), int(sys.argv[9]), int(sys.argv[10])
    nwin = int(sys.argv[11]) if len(sys.argv) > 11 else workers * 4
    t_start = time.time()
    edges = np.linspace(0, T, nwin + 1)
    jobs = [(N, mode, T, s, A, seed, edges[i], edges[i + 1], dt0, dtmin) for i in range(nwin)]
    res = []
    with Pool(workers) as pool:
        for i, r in enumerate(pool.imap(window, jobs)):
            res.append(r); print(f'PROGRESS {(i + 1) / nwin:.3f} window {i + 1}/{nwin} t={time.time() - t_start:.0f}s', flush=True)
    counts, patterns, stats, coarse = Counter(), Counter(), Counter(), defaultdict(Counter)
    events = []
    for r in res:
        counts.update(r['counts']); patterns.update(r['patterns']); stats.update(r['stats']); events += r['events']
        for k, c in r['coarse'].items(): coarse[k].update(c)
    deg = [d for r in res for d in r['deg']]
    # per-cell contact changes; lifetimes (cells born and died inside the run)
    events.sort(key=lambda e: e[0])
    born_t, died_t, per_life = {}, {}, {}
    for t, typ, cells in events:
        if typ == 'birth' and len(cells) == 1: born_t[cells[0]] = t; per_life[cells[0]] = 0
        elif typ == 'death' and len(cells) == 1:
            c = cells[0]
            if c in born_t and c not in died_t: died_t[c] = t
        elif typ in ('contact gained', 'contact lost'):
            for c in cells:
                if c in per_life and c not in died_t: per_life[c] += 1
    full = [c for c in died_t]                        # cells born and died inside the run (first life only)
    life = dict(n_full_lives=len(full), mean_lifetime=float(np.mean([died_t[c] - born_t[c] for c in full])) if full else None,
                mean_contact_changes_per_life=float(np.mean([per_life[c] for c in full])) if full else None,
                births=len([1 for e in events if e[1] == 'birth']), deaths=len([1 for e in events if e[1] == 'death']))
    contact_changes = counts.get('contact gained', 0) + counts.get('contact lost', 0)
    summary = dict(N=N, mode=mode, T=T, dt0=dt0, dtmin=dtmin, s=s, A=A, seed=seed, windows=nwin, counts=dict(counts),
                   clump_patterns=dict(patterns), stats=dict(stats), euler_fail=sum(r['euler_fail'] for r in res),
                   robust_fail=sum(r['robust_fail'] for r in res), balance_fail=sum(r['balance_fail'] for r in res),
                   base_frames=sum(r['nbase'] for r in res) - nwin + 1,
                   mean_contacts_per_cell=float(np.mean(deg)), mean_contacts_sd_over_frames=float(np.std(deg)),
                   contact_changes_per_cell_per_unit_time=contact_changes / N / T,
                   lives=life, coarse={str(k): dict(v) for k, v in coarse.items()}, wall_s=time.time() - t_start)
    json.dump(dict(summary=summary, events=events), open(out, 'w'))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
