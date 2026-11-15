"""Cosmic-void basins through time (cosmic-voids workstream of "One tissue, three scales", DICTO 15 Nov 2026).

Input: density-contrast grids delta_KKKK.npy (one per snapshot, periodic box) from nbody_pm.py.
Per snapshot (stage 1):
  - smooth delta with a Gaussian of r.m.s. width R (Mpc/h; fixed for the whole run, stated in the output);
  - watershed basins by steepest descent: every voxel points to its lowest neighbour among the 26 around it (periodic) when that is
    lower than itself; a voxel with no lower neighbour is a minimum; a basin = all voxels whose descent path ends at one minimum.
    This is the zone definition of ZOBOV (Neyrinck 2008) applied on a grid with 26-neighbour connectivity, as Wojtak, Powell & Abel
    2016 do; basins are NOT merged into larger voids (no hierarchy), so the basins tile the box;
  - two basins are in contact when they share a wall: at least one pair of face-adjacent voxels (6-connectivity) carries their two
    labels; wall area = number of such voxel faces.
Between snapshots (stage 2; Wojtak et al. 2016 rule, by volume not by particles): basin A at the earlier snapshot is linked to the later
basin that contains A's minimum voxel, and later basin B to the earlier basin containing B's minimum. A later basin keeps the label
of the earlier basin it is linked to both ways; if several earlier minima fall in one later basin and none is linked both ways, it keeps
the label of the largest. Earlier basins whose label is not kept have merged into the basin holding their minimum (lineage heirs = 1).
A later basin linked to no earlier minimum is new: lineage parent = the earlier basin holding its minimum (a split) .
The frames go in time order to the shared event logger (studies/2026-11-15-event-logger/scripts/eventlog.py, unchanged, 3D vocabulary).
Variants: snapshot spacing k (use every k-th snapshot), wall-area threshold amin (contacts with area < amin voxel faces ignored).
Usage: void_basins.py DATA_DIR OUT_PREFIX R workers [a_min]  (a_min: use only snapshots with a >= a_min)"""
import sys, os, json, time, glob, itertools, re
import numpy as np
from multiprocessing import Pool
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-11-15-event-logger', 'scripts'))
import eventlog as EL

OFF26 = [o for o in itertools.product((-1, 0, 1), repeat=3) if o != (0, 0, 0)]


def smooth(delta, R, L):
    G = delta.shape[0]
    k = 2 * np.pi * np.fft.fftfreq(G, L / G); kz = 2 * np.pi * np.fft.rfftfreq(G, L / G)
    k2 = k[:, None, None] ** 2 + k[None, :, None] ** 2 + kz[None, None, :] ** 2
    return np.fft.irfftn(np.fft.rfftn(delta.astype(np.float64)) * np.exp(-0.5 * k2 * R * R), s=delta.shape)


def basins(f):
    G = f.shape[0]
    best = f.copy(); arg = np.full(f.shape, -1, np.int8)
    for n, o in enumerate(OFF26):
        r = np.roll(f, shift=(-o[0], -o[1], -o[2]), axis=(0, 1, 2))     # r[x] = f[x + o]
        m = r < best; best[m] = r[m]; arg[m] = n
    ix = np.indices(f.shape)
    tgt = np.arange(G ** 3, dtype=np.int64).reshape(f.shape)
    O = np.array(OFF26 + [(0, 0, 0)])
    a = arg.astype(np.int64); a[a < 0] = 26
    tx = (ix[0] + O[a, 0]) % G; ty = (ix[1] + O[a, 1]) % G; tz = (ix[2] + O[a, 2]) % G
    p = ((tx * G + ty) * G + tz).ravel()
    del tx, ty, tz, ix
    while True:
        q = p[p]
        if np.array_equal(q, p): break
        p = q
    mins, lab = np.unique(p, return_inverse=True)
    return lab.reshape(f.shape).astype(np.int32), mins


def walls(lab):
    nb = int(lab.max()) + 1
    keys = []
    for ax in range(3):
        l2 = np.roll(lab, -1, axis=ax); m = lab != l2
        a, b = lab[m].astype(np.int64), l2[m].astype(np.int64)
        keys.append(np.minimum(a, b) * nb + np.maximum(a, b))
    u, c = np.unique(np.concatenate(keys), return_counts=True)
    return np.stack([u // nb, u % nb], 1), c


def stage1(args):
    path, R, L, cache = args
    if os.path.exists(cache):
        z = np.load(cache); return dict(cache=cache, nb=int(z['nb']))
    f = smooth(np.load(path), R, L)
    lab, mins = basins(f)
    pairs, area = walls(lab)
    vol = np.bincount(lab.ravel())
    assert (vol > 0).all()
    np.savez_compressed(cache, lab=lab, mins=mins, pairs=pairs, area=area, vol=vol, nb=len(mins), fmin=f.ravel()[mins])
    return dict(cache=cache, nb=len(mins))


def parse(pat):
    return dict(zip(('born', 'died', 'lost', 'gained'), map(int, re.findall(r'\d+', pat))))


def stage2(caches, k, amin, a_of):
    idx = list(range(0, len(caches), k))
    if idx[-1] != len(caches) - 1: idx.append(len(caches) - 1)
    prev = None; pid_prev = None; next_pid = 0
    tot = Counter(); pats = Counter(); per_step = []; deg = []; nbs = []; bal_fail = 0
    flick_prev_lost = set(); flicker = 0; lost_total = 0
    derived = Counter()
    for j in idx:
        z = np.load(caches[j]); lab = z['lab']; mins = z['mins']; vol = z['vol']; nb = int(z['nb'])
        pairs = z['pairs'][z['area'] >= amin]
        if prev is None:
            pid = np.arange(nb); next_pid = nb; parents, heirs = {}, {}
        else:
            plab, pmins, pvol = prev
            fA = lab.ravel()[pmins]                    # later basin holding each earlier minimum
            gB = plab.ravel()[mins]                    # earlier basin holding each later minimum
            pid = np.full(nb, -1, np.int64); parents, heirs = {}, {}
            cands = {}
            for A, B in enumerate(fA): cands.setdefault(int(B), []).append(A)
            for B in range(nb):
                c = cands.get(B)
                if c:
                    A = int(gB[B]) if int(gB[B]) in c else max(c, key=lambda a: pvol[a])
                    pid[B] = pid_prev[A]
                else:
                    pid[B] = next_pid; next_pid += 1
                    parents[str(pid[B])] = {str(pid_prev[int(gB[B])]): 1.0}
            kept = set(pid.tolist())
            for A in range(len(pmins)):
                if pid_prev[A] not in kept: heirs[str(pid_prev[A])] = {str(pid[fA[A]]): 1.0}
        cells = [str(x) for x in pid]
        bnd = [(str(pid[a]), str(pid[b])) for a, b in pairs]
        Tn = EL.Tiling(cells, bnd, dim=3, surface='space', t=float(a_of[j]), parents=parents)
        deg.append(2 * len(Tn.pairs) / nb); nbs.append(nb)
        if prev is not None:
            Tp.heirs = heirs
            ev = EL.classify(Tp, Tn)
            ok, _, _ = EL.balance(Tp, Tn, ev)
            if not ok: bal_fail += 1
            c = Counter(e['type'] for e in ev); tot.update(c)
            for e in ev:
                P = parse(e['pattern'])
                if e['type'] == 'clump': pats[e['pattern']] += 1
                ch = P['lost'] + P['gained']
                if e['type'] in ('contact gained', 'contact lost'): derived['contact changes, alone'] += ch
                elif P['born'] == 0 and P['died'] == 0: derived['contact changes, clumped with other contact changes'] += ch
                else: derived['contact changes, with a merge/split/birth/death'] += ch
                derived['cells died (merge or death)'] += P['died']; derived['cells born (split or birth)'] += P['born']
                if e['type'] == 'merge' or (e['type'] == 'clump' and P['died'] and not P['born']): derived['merge-type events'] += 1
            lostp = Tp.pairs - Tn.pairs
            gainp = Tn.pairs - Tp.pairs
            flicker += len(gainp & flick_prev_lost); lost_total += len(lostp)
            flick_prev_lost = set(lostp)
            per_step.append(dict(a0=float(a_of[prev_j]), a1=float(a_of[j]), basins=nb, counts=dict(c)))
        prev = (lab, mins, vol); pid_prev = pid; Tp = Tn; prev_j = j
    cc = derived['contact changes, alone'] + derived['contact changes, clumped with other contact changes'] + \
        derived['contact changes, with a merge/split/birth/death']
    return dict(k=k, amin=amin, snapshots_used=len(idx), counts=dict(tot), top_clump_patterns=dict(pats.most_common(12)),
                derived=dict(derived), contact_changes_total=cc,
                fraction_alone=derived['contact changes, alone'] / cc if cc else None,
                contact_changes_per_merge=cc / derived['cells died (merge or death)'] if derived['cells died (merge or death)'] else None,
                regained_next_step=flicker, lost_total=lost_total, balance_failures=bal_fail,
                basins_first_last=(nbs[0], nbs[-1]), mean_contacts_first_last=(deg[0], deg[-1]), per_step=per_step)


def main():
    data, outp, R, workers = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
    t0 = time.time()
    meta = json.load(open(f'{data}/meta.json'))
    L = meta['L_Mpc_h']; snaps = meta['snapshots']
    a_min = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    snaps = [s for s in snaps if s['a'] >= a_min - 1e-9]; a_of = [s['a'] for s in snaps]
    cdir = f'{data}/basins-R{R:g}'; os.makedirs(cdir, exist_ok=True)
    jobs = [(f'{data}/delta_{s["k"]:04d}.npy', R, L, f'{cdir}/b_{s["k"]:04d}.npz') for s in snaps]
    with Pool(workers) as pool:
        for i, r in enumerate(pool.imap(stage1, jobs)):
            print(f'PROGRESS {0.7 * (i + 1) / len(jobs):.3f} stage1 {i + 1}/{len(jobs)} basins {r["nb"]} t={time.time() - t0:.0f}s', flush=True)
    caches = [j[3] for j in jobs]
    variants = [(k, 1) for k in (1, 2, 4, 8)] + [(1, 10), (4, 10)]
    out = dict(R_Mpc_h=R, a_min=a_min, grid=meta['grid'], L_Mpc_h=L, nbody=meta, rule='steepest-descent basins, 26-neighbour, Gaussian smoothing R; '
               'contact = shared voxel face; tracking by minimum containment (Wojtak et al. 2016)', variants=[])
    for i, (k, amin) in enumerate(variants):
        r = stage2(caches, k, amin, a_of); out['variants'].append(r)
        print(f'PROGRESS {0.7 + 0.3 * (i + 1) / len(variants):.3f} stage2 k={k} amin={amin} counts={r["counts"]} t={time.time() - t0:.0f}s', flush=True)
    json.dump(out, open(f'{outp}.json', 'w'), indent=1)
    ok = all(v['balance_failures'] == 0 for v in out['variants'])
    for v in out['variants']:
        print(f"k={v['k']} amin={v['amin']} contact changes {v['contact_changes_total']} alone {v['fraction_alone']:.3f} per merge "
              f"{v['contact_changes_per_merge']} basins {v['basins_first_last']} mean contacts {v['mean_contacts_first_last']} "
              f"balance failures {v['balance_failures']}")
    print('WALL', time.time() - t0)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
