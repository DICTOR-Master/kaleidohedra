"""Job B: moving Poisson-Voronoi tessellations (periodic box, N seeds, mean spacing ell = N^(-1/d)).
Seeds move independently: LINEAR (constant velocity, components N(0, s^2)) or BROWNIAN (Gaussian steps).
At each time step the Delaunay contacts are recomputed; contact changes (2D: T1 swaps = one contact lost + one made;
3D: 2-3 / 3-2 flips = one contact made / lost) are counted between consecutive steps.
Displacement unit: rms seed displacement over the run, in units of ell (for Brownian: rms displacement of the whole run).
Time-step test: the same run is repeated with per-step rms displacement delta = 0.1, 0.03, 0.01, 0.003 ell.
Usage: moving.py DIM [--pilot] OUT.json"""
import sys, json, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nulllib import edge_keys

DIM = int(sys.argv[1]); PILOT = '--pilot' in sys.argv; OUT = sys.argv[-1]
N = (2000 if DIM == 2 else 1000) if PILOT else (20000 if DIM == 2 else 8000)
TOTAL = 0.3 if PILOT else 1.0            # total rms displacement in ell
DELTAS = [0.1, 0.03] if PILOT else [0.1, 0.03, 0.01, 0.003]
REPS = 2 if PILOT else 4
WORKERS = 4 if PILOT else int(dict(a.split('=') for a in sys.argv if a.startswith('workers=')).get('workers', 8))


def run(args):
    mode, delta, seed = args
    rng = np.random.default_rng(seed)
    ell = N ** (-1 / DIM)
    P = rng.random((N, DIM))
    steps = int(round(TOTAL / delta)) if mode == 'linear' else int(round((TOTAL / delta) ** 2))
    sig = delta * ell / np.sqrt(DIM)    # per-component step sd so that the rms step length is delta*ell
    if mode == 'linear':
        Vel = rng.normal(size=(N, DIM)) * sig
    E0 = edge_keys(P); E = E0
    lost = made = 0
    for k in range(steps):
        step = Vel if mode == 'linear' else rng.normal(size=(N, DIM)) * sig
        P = (P + step) % 1.0
        E1 = edge_keys(P)
        lost += len(np.setdiff1d(E, E1, assume_unique=True)); made += len(np.setdiff1d(E1, E, assume_unique=True))
        E = E1
    net_lost = len(np.setdiff1d(E0, E, assume_unique=True)); net_made = len(np.setdiff1d(E, E0, assume_unique=True))
    return {'mode': mode, 'delta': delta, 'seed': seed, 'steps': steps, 'N': N, 'lost': lost, 'made': made,
            'net_lost': net_lost, 'net_made': net_made, 'contacts_start': len(E0), 'contacts_end': len(E)}


if __name__ == '__main__':
    t0 = time.time()
    jobs = []
    for mode in ('linear', 'brownian'):
        for dl in DELTAS:
            if mode == 'brownian' and dl < 0.01:
                continue  # (TOTAL/delta)^2 steps: 0.003 would need 1.1e5 recomputations
            for r in range(REPS):
                jobs.append((mode, dl, 1000 * DIM + 100 * r + int(1000 * dl) + (7 if mode == 'brownian' else 0)))
    out = []
    with Pool(WORKERS) as pool:
        for i, res in enumerate(pool.imap_unordered(run, jobs)):
            out.append(res)
            print('RUN', res, flush=True)
            print(f'PROGRESS {(i + 1) / len(jobs):.3f} runs', flush=True)
    CH = []
    summ = {}
    for mode in ('linear', 'brownian'):
        for dl in DELTAS:
            rs = [r for r in out if r['mode'] == mode and r['delta'] == dl]
            if not rs:
                continue
            # contact changes per cell per ell of rms displacement
            ch = np.array([(r['lost'] + r['made']) / (r['N'] * TOTAL) for r in rs])
            net = np.array([(r['net_lost'] + r['net_made']) / (r['N'] * TOTAL) for r in rs])
            summ[f'{mode} {dl}'] = {'changes_per_cell_per_ell': ch.mean(), 'err': ch.std(ddof=1) / np.sqrt(len(ch)),
                                    'net_changes_per_cell': net.mean(), 'net_err': net.std(ddof=1) / np.sqrt(len(net)),
                                    'made_minus_lost': int(sum(r['made'] - r['lost'] for r in rs))}
            print('SUMMARY', mode, dl, summ[f'{mode} {dl}'], flush=True)

    def chk(name, ok, info=''):
        CH.append((name, bool(ok), str(info))); print(('X PASS ' if ok else 'X FAIL ') + name + ' ' + str(info), flush=True)

    lin = [summ[f'linear {d}']['changes_per_cell_per_ell'] for d in DELTAS]
    lerr = [summ[f'linear {d}']['err'] for d in DELTAS]
    # linear motion: counts converge as delta -> 0 (the two finest agree within errors + 3 %)
    chk('linear motion: contact-change rate is time-step independent at the finest steps',
        abs(lin[-1] - lin[-2]) < 3 * np.hypot(lerr[-1], lerr[-2]) + 0.03 * lin[-1], lin)
    if DIM == 2:
        chk('2D: every T1 loses one contact and makes one (made = lost exactly, contact count fixed = 3N)',
            all(r['made'] == r['lost'] and r['contacts_start'] == 3 * N for r in out))
    bd = [d for d in DELTAS if f'brownian {d}' in summ]
    if len(bd) >= 2:
        b = np.array([summ[f'brownian {d}']['changes_per_cell_per_ell'] for d in bd])
        expo = np.polyfit(np.log(bd), np.log(b), 1)[0]
        summ['brownian_exponent'] = expo
        chk('NEGATIVE control (expected to fail time-step independence): Brownian counts grow as delta^-1 (counts per fixed rms '
            'displacement) - not a usable rate', expo < -0.5, f'exponent {expo:.3f}')
        nb = [summ[f'brownian {d}']['net_changes_per_cell'] for d in bd]
        summ['brownian_net'] = nb
    json.dump({'dim': DIM, 'N': N, 'total_rms_disp_ell': TOTAL, 'runs': out, 'summary': summ, 'checks': CH,
               'wall_s': time.time() - t0}, open(OUT, 'w'), indent=1)
    nf = sum(not c[1] for c in CH)
    print(f'{len(CH)} checks, {nf} failed', flush=True)
    print('FINAL ok' if nf == 0 else 'FINAL FAIL', flush=True)
