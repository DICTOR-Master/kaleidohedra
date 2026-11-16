"""Swaps traced through depth (README section "Swaps traced through depth", 16 Nov 2026; DICTO's diagnosis: "the same initial
problem as the shadows of the queens": only walls that stand upright through the layers give true neighbour changes).

The granules are segmented as cells of the vertical velocity uz (upflow cells bounded by downflow lanes; the primary setting of the
15 Nov census: threshold mean + 0.25 std, smoothing 1.5 pixels, marker watershed of tiles.py) on horizontal planes of the 3D
Bifrost run at FIXED depths below the mean tau = 1 height. Cells are tracked through time at each depth (tiles.match, the shared
event logger, the same swap pairing and persistence rule as census.py, so the per-depth counts reproduce census.py), and linked
across adjacent depths at every frame (mutual largest pixel overlap: the planes lie on the same horizontal grid).

A swap at depth d (lost contact a-b, gained c-e, at time t) is CONFIRMED at an adjacent depth d' when a persistent swap at d' within
|t' - t| <= tol (tol = max(30 s, one step)) has its lost pair equal to the depth-link of a-b (links at the frames before the change)
and its gained pair equal to the depth-link of c-e (links at the frames after): the same 2-2 change of the same four cell columns.
A swap counts as UPRIGHT at d when it is confirmed at every adjacent depth in the set (both neighbours inside, one at the ends).
Also: a looser 'near' match (any persistent swap at d' within 10 pixels and tol), and the share of contacts at d whose linked pair
also touches at d' (how many walls stand upright from d to d').

Usage:
  trace3d.py seg   DATA RUN DZ OUTDIR                  segment every frame at one depth -> OUTDIR/seg_dz<DZ>.npy (int16)
  trace3d.py link  OUTDIR DZ1 DZ2                      raw depth links per frame -> OUTDIR/link_<DZ1>_<DZ2>.pkl
  trace3d.py track DATA RUN OUTDIR DZ ORDER STEP W     ORDER real | shuf:SEED -> OUTDIR/track_<ORDER>_dz<DZ>_s<STEP>.pkl
  trace3d.py combine OUTDIR DEPTHS STEPS RESULTSDIR STUDYDIR   confirmations, controls, tables (summary.json, summary.md)
Data credit: Bifrost code, Gudiksen et al. 2011, A&A 531, A154; run en024048_hion, Carlsson, Hansteen, Gudiksen, Leenaarts & De
Pontieu 2016, A&A 585, A4; Hinode Science Data Centre Europe (sdc.uio.no)."""
import sys, os, json, itertools, pickle, time
import numpy as np
from collections import Counter, defaultdict
from scipy import ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts'))
import tiles as TL
import eventlog as EL

SIGMA, THR = 1.5, 0.25
NEAR_PX = 10


def order_of(order, n):
    if order == 'real': return np.arange(n)
    return np.random.default_rng(int(order.split(':')[1])).permutation(n)     # stepcal_prep.py uses default_rng(7).permutation


def cmd_seg(data, run, dz, out):
    F = np.load(f'{data}/{run}_uz_dz{dz}.npy', mmap_mode='r')
    n = min(F.shape[0], int(os.environ.get('TRACE_N', F.shape[0])))       # TRACE_N: first frames only (pilots)
    S = np.lib.format.open_memmap(f'{out}/seg_dz{dz}.npy', mode='w+', dtype=np.int16, shape=(n,) + F.shape[1:])
    for k in range(n):
        lab = TL.segment(np.asarray(F[k]), SIGMA, THR, method='thr')
        assert lab.max() < 32000
        S[k] = lab
        if k % 20 == 0: print(f'PROGRESS {(k + 1) / n:.4f} seg dz{dz} {k + 1}/{n}', flush=True)
    S.flush(); print('SEG_OK', dz, n, flush=True)


def mutual_links(l1, l2):
    """Mutual largest-overlap links between two label maps on the same grid: {label1: label2}."""
    K = np.int64(l2.max()) + 1
    u, c = np.unique(l1.astype(np.int64) * K + l2, return_counts=True)
    a, b = u // K, u % K
    b1, b2 = {}, {}
    for x, y, n in zip(a.tolist(), b.tolist(), c.tolist()):
        if n > b1.get(x, (0, 0))[1]: b1[x] = (y, n)
        if n > b2.get(y, (0, 0))[1]: b2[y] = (x, n)
    return {x: y for x, (y, n) in b1.items() if b2[y][0] == x}


def contacts(lab):
    return set(TL.graph(lab)['contacts'])


def cmd_link(out, dz1, dz2):
    A = np.load(f'{out}/seg_dz{dz1}.npy', mmap_mode='r'); B = np.load(f'{out}/seg_dz{dz2}.npy', mmap_mode='r')
    n = A.shape[0]; links, upright = [], []
    for k in range(n):
        a, b = np.asarray(A[k]), np.asarray(B[k])
        L = mutual_links(a, b); links.append(L)
        if k % 10 == 0:            # walls standing upright: contacts at dz1 whose linked pair also touches at dz2
            ca, cb = contacts(a), contacts(b)
            both = [(x, y) for x, y in ca if x in L and y in L]
            kept = sum(1 for x, y in both if (min(L[x], L[y]), max(L[x], L[y])) in cb)
            upright.append(dict(frame=k, cells1=int(len(np.unique(a))), cells2=int(len(np.unique(b))), linked=len(L),
                                contacts1=len(ca), contacts_linked=len(both), contacts_kept=kept))
        if k % 20 == 0: print(f'PROGRESS {(k + 1) / n:.4f} link {dz1}-{dz2} {k + 1}/{n}', flush=True)
    pickle.dump(dict(links=links, upright=upright), open(f'{out}/link_{dz1}_{dz2}.pkl', 'wb'))
    print('LINK_OK', dz1, dz2, flush=True)


def periodic_mean(pts, L):
    th = 2 * np.pi * np.asarray(pts, float) / L
    return (np.arctan2(np.sin(th).mean(0), np.cos(th).mean(0)) % (2 * np.pi)) * L / (2 * np.pi)


def cmd_track(data, run, out, dz, order, step, W):
    """The census.py swap rule, unchanged, on the reordered frame sequence; keeps the swap LIST and the raw-to-persistent label maps."""
    S = np.load(f'{out}/seg_dz{dz}.npy', mmap_mode='r')
    times = np.load(f'{data}/{run}_times.npy')
    n = S.shape[0]; perm = order_of(order, n)
    idx = list(range(0, n, step))
    prev = None; next_id = 1; swaps = []; pend_lost = []; counts = Counter(); luts = []; cen = []
    euler_bad = 0; ncell_sum = 0; bad_bal = 0
    for q, k in enumerate(idx):
        raw = np.asarray(S[perm[k]]).astype(np.int64)
        if prev is None:
            lab = raw; next_id = int(lab.max()) + 1; par = her = {}
        else:
            lab, par, her, next_id = TL.match(prev_lab, raw, next_id)
        u = np.unique(raw * (1 << 32) + lab)
        luts.append({int(x >> 32): int(x & 0xffffffff) for x in u.tolist()})       # raw label -> persistent label at this frame
        G = TL.graph(lab); ncell = len(np.unique(lab)); ncell_sum += ncell
        if TL.torus_euler(ncell, G) != 0: euler_bad += 1
        ids = np.unique(lab); L = lab.shape[0]; yy, xx = np.indices(lab.shape); cc = {}
        for coord, j in ((yy, 0), (xx, 1)):
            th = 2 * np.pi * coord / L
            s_ = ndi.mean(np.sin(th), lab, ids); c_ = ndi.mean(np.cos(th), lab, ids)
            cc[j] = (np.arctan2(s_, c_) % (2 * np.pi)) * L / (2 * np.pi)
        cen.append({int(i): (float(y), float(x)) for i, y, x in zip(ids, cc[0], cc[1])})
        T = TL.to_tiling(EL.Tiling, lab, G, float(times[k]), par, None)
        if prev is not None:
            prev.heirs = {str(a): {str(b): s for b, s in v.items()} for a, v in her.items()}
            ev = EL.classify(prev, T)
            if not EL.balance(prev, T, ev)[0]: bad_bal += 1
            for e in ev:
                counts[e['type']] += 1
                cs = sorted(e['cells'])
                lost = [p for p in itertools.combinations(cs, 2) if p in prev.pairs and p not in T.pairs]
                gained = [p for p in itertools.combinations(cs, 2) if p in T.pairs and p not in prev.pairs]
                used = set()
                for l in lost:
                    cn = prev.nb[l[0]] & prev.nb[l[1]]
                    g = next((g for g in gained if g not in used and set(g) <= cn and set(l) <= (T.nb[g[0]] & T.nb[g[1]])), None)
                    if g is not None:
                        used.add(g); swaps.append((float(times[k]), frozenset(l), frozenset(g), 'same step', q, q))
                    elif e['net'] == 0 and not any(c not in prev.cells or c not in T.cells for c in cs):
                        pend_lost.append((float(times[k]), l, cn, q))
                for g in gained:
                    if g in used: continue
                    if e['net'] == 0 and not any(c not in prev.cells or c not in T.cells for c in cs):
                        j = next((j for j, (tl, l, cn, ql) in enumerate(pend_lost) if float(times[k]) - tl <= W + 1e-6 and set(g) <= cn
                                  and set(l) <= (T.nb[g[0]] & T.nb[g[1]])), None)
                        if j is not None:
                            tl, l, cn, ql = pend_lost.pop(j); swaps.append((float(times[k]), frozenset(l), frozenset(g), 'two steps', ql, q))
        prev, prev_lab = T, lab
        if q % 20 == 0: print(f'PROGRESS {(q + 1) / len(idx):.4f} track {order} dz{dz} s{step} {q + 1}/{len(idx)}', flush=True)
    # persistence (census.py flicker rule): a swap undone by the same four cells within W is removed with its reversal
    open_, drop = {}, set()
    for i, (t, lo, ga, how, ql, q) in enumerate(swaps):
        key = (ga, lo)
        if key in open_ and t - swaps[open_[key]][0] <= W + 1e-6:
            drop.add(i); drop.add(open_[key]); del open_[key]
        else:
            open_[(lo, ga)] = i
    pers = []
    for i, (t, lo, ga, how, ql, q) in enumerate(swaps):
        if i in drop: continue
        four = [int(c) for c in lo | ga]
        pts = [cen[q][c] if c in cen[q] else cen[max(ql - 1, 0)].get(c) for c in four]
        pos = periodic_mean([p for p in pts if p is not None], S.shape[1])
        pers.append(dict(t=t, lost=sorted(int(c) for c in lo), gained=sorted(int(c) for c in ga), how=how, q_lost=ql, q=q,
                         y=float(pos[0]), x=float(pos[1])))
    dur = float(times[idx[-1]] - times[idx[0]])
    res = dict(dz=dz, order=order, step=step, W=W, frames=len(idx), mean_cells=ncell_sum / len(idx), duration_s=dur,
               cell_minutes=ncell_sum / len(idx) * dur / 60.0, swaps_elementary=len(swaps), swaps_persistent=len(pers),
               counts=dict(counts), euler_bad=euler_bad, balance_failures=bad_bal, perm=perm.tolist(), idx=idx, luts=luts, swaps=pers)
    pickle.dump(res, open(f'{out}/track_{order.replace(":", "")}_dz{dz}_s{step}.pkl', 'wb'))
    print('TRACK', json.dumps({k: res[k] for k in ('dz', 'order', 'step', 'mean_cells', 'swaps_elementary', 'swaps_persistent', 'euler_bad', 'balance_failures')}), flush=True)
    print('TRACK_OK', flush=True)


def confirm(A, B, linkAB, tol):
    """For each persistent swap of track A (depth d), the matching swap of track B (depth d') or None; plus 'near' matches.
    linkAB[k]: raw label at d -> raw label at d' at ORIGINAL frame k."""
    inv_lut_B = []          # per sampled frame of B: raw -> persistent at d'
    for lt in B['luts']: inv_lut_B.append(lt)
    # persistent label at d -> raw label at d (per frame of A)
    rev_A = [{v: r for r, v in lt.items()} for lt in A['luts']]

    def map_cell(c, q):
        r = rev_A[q].get(c)
        if r is None: return None
        k = A['perm'][A['idx'][q]]
        r2 = linkAB[k].get(r)
        if r2 is None: return None
        return inv_lut_B[q].get(r2)            # A and B share the frame sequence (same order, same step)

    byB = defaultdict(list)
    for j, s in enumerate(B['swaps']): byB[(tuple(s['lost']), tuple(s['gained']))].append(j)
    used = set(); out = []; L = 504
    Bt = np.array([s['t'] for s in B['swaps']]) if B['swaps'] else np.zeros(0)
    By = np.array([s['y'] for s in B['swaps']]) if B['swaps'] else np.zeros(0)
    Bx = np.array([s['x'] for s in B['swaps']]) if B['swaps'] else np.zeros(0)
    for s in A['swaps']:
        qb, qa = max(s['q_lost'] - 1, 0), s['q']
        lost = [map_cell(c, qb) or map_cell(c, qa) for c in s['lost']]
        gained = [map_cell(c, qa) or map_cell(c, qb) for c in s['gained']]
        hit = None
        if None not in lost and None not in gained:
            key = (tuple(sorted(lost)), tuple(sorted(gained)))
            cands = [j for j in byB.get(key, []) if j not in used and abs(B['swaps'][j]['t'] - s['t']) <= tol + 1e-6]
            if cands:
                hit = min(cands, key=lambda j: abs(B['swaps'][j]['t'] - s['t'])); used.add(hit)
        near = False
        if len(Bt):
            dy = np.abs(By - s['y']); dy = np.minimum(dy, L - dy); dx = np.abs(Bx - s['x']); dx = np.minimum(dx, L - dx)
            near = bool(np.any((np.abs(Bt - s['t']) <= tol + 1e-6) & (dy * dy + dx * dx <= NEAR_PX ** 2)))
        out.append(dict(hit=hit, near=near, mapped=None not in lost and None not in gained))
    return out


def cmd_combine(out, depths, steps, rdir, sdir):
    depths = [float(d) for d in depths.split(',')]; steps = [int(s) for s in steps.split(',')]
    os.makedirs(rdir, exist_ok=True)
    cal = json.load(open(f'{sdir}/results/stepcal/summary.json'))['detection']
    fcal = {s: 0.5 * (cal['v1_z0']['60'][str(s)] + cal['v1_z1']['60'][str(s)]) for s in steps}     # Sun-like detection, P = 60 s
    links = {}
    for a, b in zip(depths, depths[1:]):
        Lk = pickle.load(open(f'{out}/link_{a}_{b}.pkl', 'rb'))
        links[(a, b)] = Lk['links']; links[(b, a)] = [{v: k for k, v in L.items()} for L in Lk['links']]
        links[('up', a, b)] = Lk['upright']
    R = dict(depths=depths, steps_s=[10 * s for s in steps], tol_s={str(s): max(30, 10 * s) for s in steps}, near_px=NEAR_PX,
             detection_sunlike_P60={str(s): fcal[s] for s in steps}, upright_walls={}, orders={})
    for a, b in zip(depths, depths[1:]):
        U = links[('up', a, b)]
        R['upright_walls'][f'{a}-{b}'] = dict(cells_linked_share=float(np.mean([u['linked'] / u['cells1'] for u in U])),
                                               contacts_kept_share=float(np.sum([u['contacts_kept'] for u in U]) / np.sum([u['contacts1'] for u in U])),
                                               cells1=float(np.mean([u['cells1'] for u in U])), cells2=float(np.mean([u['cells2'] for u in U])))
    figdata = None
    for order in ('real', 'shuf7'):
        R['orders'][order] = {}
        for s in steps:
            tr = {d: pickle.load(open(f'{out}/track_{order}_dz{d}_s{s}.pkl', 'rb')) for d in depths}
            tol = max(30, 10 * s)
            conf = {}
            for i, d in enumerate(depths):
                for j in (i - 1, i + 1):
                    if 0 <= j < len(depths): conf[(d, depths[j])] = confirm(tr[d], tr[depths[j]], links[(d, depths[j])], tol)
            row = {}
            for i, d in enumerate(depths):
                nb = [depths[j] for j in (i - 1, i + 1) if 0 <= j < len(depths)]
                N = len(tr[d]['swaps'])
                up = sum(1 for k in range(N) if all(conf[(d, e)][k]['hit'] is not None for e in nb))
                cm = tr[d]['cell_minutes']
                row[str(d)] = dict(cells=tr[d]['mean_cells'], cell_minutes=cm, euler_bad=tr[d]['euler_bad'], frames=tr[d]['frames'],
                                   balance_failures=tr[d]['balance_failures'], plain=N, plain_rate=N / cm, plain_rate_corrected=N / cm / fcal[s],
                                   upright=up, upright_rate=up / cm,
                                   confirmed={str(e): sum(1 for x in conf[(d, e)] if x['hit'] is not None) for e in nb},
                                   mapped={str(e): sum(1 for x in conf[(d, e)] if x['mapped']) for e in nb},
                                   near={str(e): sum(1 for x in conf[(d, e)] if x['near']) for e in nb},
                                   near_all=sum(1 for k in range(N) if all(conf[(d, e)][k]['near'] for e in nb)))
            # chains from the top plane downward: how deep does the same change reach?
            reach = Counter()
            for k in range(len(tr[depths[0]]['swaps'])):
                cur, dd = k, 0
                while dd + 1 < len(depths):
                    h = conf[(depths[dd], depths[dd + 1])][cur]['hit']
                    if h is None: break
                    cur, dd = h, dd + 1
                reach[str(depths[dd])] += 1
            row['top_chain_reach'] = dict(reach)
            R['orders'][order][str(s)] = row
            if order == 'real' and s == steps[0]:
                d0 = depths[0]; dfig = depths[1] if len(depths) > 2 else depths[0]
                figdata = dict(dz=dfig, swaps=tr[dfig]['swaps'], perm=tr[dfig]['perm'], idx=tr[dfig]['idx'], luts=tr[dfig]['luts'],
                               up=[all(conf[(dfig, e)][k]['hit'] is not None for e in [depths[j] for j in (depths.index(dfig) - 1, depths.index(dfig) + 1) if 0 <= j < len(depths)])
                                   for k in range(len(tr[dfig]['swaps']))])
            print(f'PROGRESS {(list(R["orders"]).index(order) * len(steps) + steps.index(s) + 1) / (2 * len(steps)):.4f} combine {order} s{s}', flush=True)
    pickle.dump(figdata, open(f'{out}/figdata.pkl', 'wb'))
    # controls
    ctrl = {}
    for d in depths:
        rr = [R['orders']['real'][str(s)][str(d)] for s in steps]; ss = [R['orders']['shuf7'][str(s)][str(d)] for s in steps]
        R.setdefault('per_depth', {})[str(d)] = dict(
            real_over_shuf_upright=[r['upright'] / s_['upright'] if s_['upright'] else None for r, s_ in zip(rr, ss)],
            real_over_shuf_plain=[r['plain'] / s_['plain'] if s_['plain'] else None for r, s_ in zip(rr, ss)],
            upright_change_10_80=rr[-1]['upright_rate'] / rr[0]['upright_rate'] - 1 if rr[0]['upright_rate'] else None,
            plain_change_10_80=rr[-1]['plain_rate'] / rr[0]['plain_rate'] - 1,
            corrected_change_10_80=rr[-1]['plain_rate_corrected'] / rr[0]['plain_rate_corrected'] - 1)
    json.dump(R, open(f'{rdir}/summary.json', 'w'), indent=1)
    # table
    L = ['# Swaps traced through depth (generated by trace3d.py combine)', '',
         f'Bifrost en024048_hion, uz planes at {", ".join(f"{d:g}" for d in depths)} Mm below the mean tau = 1 height; segmentation thr 0.25, '
         f'smoothing 1.5; persistence P = 60 s; depth tolerance in time: max(30 s, one step).', '',
         '## Walls standing upright between adjacent depths (every 10th frame)', '',
         '| depths (Mm) | cells (upper / lower) | cells linked (mutual overlap) | contacts kept (linked pair also touching below) |', '|---|---|---|---|']
    for k, v in R['upright_walls'].items():
        L.append(f'| {k} | {v["cells1"]:.0f} / {v["cells2"]:.0f} | {v["cells_linked_share"]:.2f} | {v["contacts_kept_share"]:.2f} |')
    for order, name in (('real', 'Real frame order'), ('shuf7', 'SHUFFLED frames (control; same permutation as the step-0 section)')):
        L += ['', f'## {name}: persistent swaps per depth', '',
              '| step (s) | depth (Mm) | cells | Euler-bad frames | plain | plain per cell per min | corrected by f | confirmed above / below | upright (all adjacent) | upright per cell per min | near (all adjacent) |',
              '|---|---|---|---|---|---|---|---|---|---|---|']
        for s in steps:
            for d in depths:
                r = R['orders'][order][str(s)][str(d)]
                cf = ' / '.join(str(r['confirmed'].get(str(e), '-')) for e in [depths[j] if 0 <= j < len(depths) else None for j in (depths.index(d) - 1, depths.index(d) + 1)])
                L.append(f'| {10 * s} | {d:g} | {r["cells"]:.0f} | {r["euler_bad"]}/{r["frames"]} | {r["plain"]} | {r["plain_rate"]:.3f} | {r["plain_rate_corrected"]:.3f} | {cf} | {r["upright"]} | {r["upright_rate"]:.4f} | {r["near_all"]} |')
            L.append(f'| {10 * s} | top-plane chains reach | | | | | | | {R["orders"][order][str(s)]["top_chain_reach"]} | | |')
    L += ['', '## Controls per depth', '', '| depth (Mm) | real / shuffled, upright, steps ' + ', '.join(str(10 * s) for s in steps) + ' s | real / shuffled, plain | upright rate change 10 to 80 s | plain change | corrected plain change |', '|---|---|---|---|---|---|']
    fm = lambda x: '-' if x is None else f'{x:.2f}'
    for d in depths:
        p = R['per_depth'][str(d)]
        L.append(f'| {d:g} | {", ".join(fm(x) for x in p["real_over_shuf_upright"])} | {", ".join(fm(x) for x in p["real_over_shuf_plain"])} | '
                 f'{fm(p["upright_change_10_80"])} | {fm(p["plain_change_10_80"])} | {fm(p["corrected_change_10_80"])} |')
    open(f'{rdir}/summary.md', 'w').write('\n'.join(L) + '\n')
    ok = all(R['orders'][o][str(s)][str(d)]['balance_failures'] == 0 for o in R['orders'] for s in steps for d in depths)
    print('COMBINE_OK' if ok else 'COMBINE_FAIL', flush=True)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'seg': cmd_seg(sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5])
    elif c == 'link': cmd_link(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
    elif c == 'track': cmd_track(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), sys.argv[6], int(sys.argv[7]), float(sys.argv[8]))
    elif c == 'combine': cmd_combine(*sys.argv[2:7])
