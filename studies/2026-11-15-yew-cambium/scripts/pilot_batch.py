#!/usr/bin/env python3
"""Pilot batch for the yew / conifer cambium stream (One tissue; DICTO 15 Nov 2026 "yes scope the yew stream").
(A) synthetic controls with known file events (synth.py -> trace_files.py -> eval_synth.py): 3 seeds x
    {events 0.004 per file per cell, picture straight; same, turned 7 degrees; no events, turned 7 degrees (null)};
(B) the Conifer Lumen Segmentation (CoLuS) data set (Katzenmaier et al., CC BY 4.0, Zenodo 15096567): every patch traced twice,
    from our own lumen segmentation of the image and from the manual lumen outlines (labels), so the effect of segmentation
    on the event counts is measured.
Prints PROGRESS <fraction> lines; writes OUT/summary.json; last line PILOT_OK or PILOT_FAIL.
Usage: pilot_batch.py COLUS_DIR OUT_DIR [N_PATCHES] [PROCS]"""
import sys, os, json, subprocess, time
from multiprocessing import Pool
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import trace_files as TF
from PIL import Image

PY = sys.executable


def synth_job(args):
    seed, ps, rot, out = args
    pre = os.path.join(out, f'syn_s{seed}_p{ps}_r{rot}')
    a = subprocess.run([PY, '-I', os.path.join(HERE, 'synth.py'), pre, str(seed), str(ps), str(ps), '6', '24', '40', str(rot)],
                       capture_output=True, text=True)
    b = subprocess.run([PY, '-I', os.path.join(HERE, 'eval_synth.py'), pre + '.png', pre + '.truth.json', pre + '.eval.json'],
                       capture_output=True, text=True)
    ok = a.returncode == 0 and b.returncode == 0
    ev = json.load(open(pre + '.eval.json')) if ok else None
    # the trace itself (logger checks) on the same picture
    tr = None
    if ok:
        img = np.array(Image.open(pre + '.png')); P, A, sh = TF.lumina(img)
        tr, _ = TF.analyse(P, A, sh, rings=6)
    try: os.remove(pre + '.png')                         # pictures are regenerated from the seed; keep JSON only
    except OSError: pass
    return dict(seed=seed, ps=ps, rot=rot, ok=ok, eval=ev, err=(a.stderr + b.stderr)[-400:],
                logger={h: v['logger'] for h, v in (tr or {}).get('steps', {}).items()}, trace_ok=(tr or {}).get('ok'))


def patch_job(args):
    path, mask, out = args
    name = os.path.basename(path).split('.')[0]
    res = {}
    for mode in ('image', 'mask'):
        try:
            img = np.array(Image.open(path))
            m = np.array(Image.open(mask)) if mode == 'mask' else None
            P, A, sh = TF.lumina(img, mask=m)
            r, _ = TF.analyse(P, A, sh)
            r.pop('chain_lengths', None)
            res[mode] = r
        except Exception as e:                            # recorded, never hidden
            res[mode] = dict(ok=False, why=f'error: {type(e).__name__}: {e}')
    json.dump(res, open(os.path.join(out, name + '.json'), 'w'), default=float)
    return name, res


def tally(rs):
    t = dict(patches=len(rs), traced=0, files_cells=0.0, split=0, insert=0, end=0, jump=0, logger_ok=0, neg_caught=0,
             swaps=0, clumps=0, euler_fail_frames=0, balance_fail=0, why={})
    for r in rs:
        if not r.get('window'):
            w = r.get('why', 'no window'); t['why'][w] = t['why'].get(w, 0) + 1; continue
        t['traced'] += 1; t['files_cells'] += r['file_cells_in_window']
        t['split'] += r['heads']['with_parent']; t['insert'] += r['heads']['no_parent']; t['end'] += r['tails']
        t['jump'] += r['jumps']
        lg = r['steps'][min(r['steps'], key=float)]['logger']          # finest step
        t['logger_ok'] += bool(lg['ok']); t['neg_caught'] += bool(lg.get('neg_control_caught'))
        t['swaps'] += lg['counts'].get('swap', 0); t['clumps'] += lg['counts'].get('clump', 0)
        t['euler_fail_frames'] += lg['n_frames_failing']; t['balance_fail'] += lg['n_balance_failures']
    fc = max(t['files_cells'], 1)
    t['per_file_per_cell'] = {k: t[k] / fc for k in ('split', 'insert', 'end', 'jump')}
    t['per_file_per_cell']['all_starts_and_ends'] = (t['split'] + t['insert'] + t['end']) / fc
    return t


def main():
    colus, out = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    os.makedirs(out, exist_ok=True); os.makedirs(os.path.join(out, 'synthetic'), exist_ok=True)
    os.makedirs(os.path.join(out, 'colus'), exist_ok=True)
    t0 = time.time()
    sjobs = [(s, ps, rot, os.path.join(out, 'synthetic')) for s in (1, 2, 3) for ps, rot in ((0.004, 0), (0.004, 7), (0.0, 7))]
    imgs = sorted(os.listdir(os.path.join(colus, 'images')))[:n]
    pjobs = [(os.path.join(colus, 'images', f), os.path.join(colus, 'labels', f.replace('.jpg', '.png')), os.path.join(out, 'colus'))
             for f in imgs]
    total = len(sjobs) + len(pjobs); done = 0
    with Pool(procs) as pool:
        syn = []
        for r in pool.imap_unordered(synth_job, sjobs):
            syn.append(r); done += 1; print(f'PROGRESS {done / total:.3f} synthetic {r["seed"]} {r["ps"]} {r["rot"]} ok={r["ok"]}', flush=True)
        pat = {}
        for name, r in pool.imap_unordered(patch_job, pjobs, chunksize=4):
            pat[name] = r; done += 1
            if done % 20 == 0: print(f'PROGRESS {done / total:.3f} patches', flush=True)
    # synthetic summary
    S = {}
    for r in syn:
        key = f"ps{r['ps']}_rot{r['rot']}"
        S.setdefault(key, []).append(dict(seed=r['seed'], ok=r['ok'], eval=r['eval'], trace_ok=r['trace_ok'],
                                          logger_counts={h: v['counts'] for h, v in r['logger'].items()},
                                          neg={h: v.get('neg_control_caught') for h, v in r['logger'].items()}))
    def agg(key, kind, f):
        v = [x['eval'][kind][f] for x in S.get(key, []) if x['eval']]
        return sum(v) if f in ('true_in_window', 'detected', 'matched') else None
    syn_sum = {}
    for key in S:
        d = {}
        for kind in ('split', 'end'):
            tr, de, ma = (agg(key, kind, f) for f in ('true_in_window', 'detected', 'matched'))
            d[kind] = dict(true=tr, detected=de, matched=ma, recall=ma / max(tr, 1) if tr else None, precision=ma / max(de, 1) if de else None)
        d['false_per_file_cell'] = sum((x['eval'][k]['detected'] - x['eval'][k]['matched']) for x in S[key] if x['eval'] for k in ('split', 'end')) / \
            max(sum(x['eval']['trace']['file_cells_in_window'] for x in S[key] if x['eval']), 1)
        d['jumps'] = sum(x['eval']['jumps_detected'] for x in S[key] if x['eval'])
        d['inserts'] = sum(x['eval']['insert_detected'] for x in S[key] if x['eval'])
        syn_sum[key] = d
    # patches
    TI = tally([pat[k]['image'] for k in pat]); TM = tally([pat[k]['mask'] for k in pat])
    both = [k for k in pat if pat[k]['image'].get('window') and pat[k]['mask'].get('window')]
    def ev(r): return r['heads']['total'] + r['tails']
    a = np.array([ev(pat[k]['image']) for k in both], float); b = np.array([ev(pat[k]['mask']) for k in both], float)
    corr = float(np.corrcoef(a, b)[0, 1]) if len(both) > 2 and a.std() > 0 and b.std() > 0 else None
    sign_agree = float(np.mean([pat[k]['image']['outward']['sign'] == pat[k]['mask']['outward']['sign'] for k in both])) if both else None
    rings = [pat[k]['mask']['rings']['n'] for k in pat if pat[k]['mask'].get('rings')]
    summ = dict(seconds=round(time.time() - t0, 1), synthetic=syn_sum, synthetic_runs=S, colus_image=TI, colus_mask=TM,
                colus_both_traced=len(both), per_patch_event_correlation_image_vs_mask=corr, outward_sign_agreement=sign_agree,
                colus_rings_estimated=dict(zip(*np.unique(rings, return_counts=True))) if rings else {},
                colus_patch_files=dict(median=float(np.median([pat[k]['mask']['spacing']['files'] for k in pat if pat[k]['mask'].get('spacing')]))))
    summ['colus_rings_estimated'] = {str(int(k)): int(v) for k, v in summ['colus_rings_estimated'].items()}
    # checks
    checks = {
        'synthetic all ran': all(r['ok'] for r in syn),
        'synthetic logger ok (Euler + balance) every run and step': all(v['ok'] for r in syn for v in r['logger'].values()),
        'synthetic negative control caught where events exist': all(v.get('neg_control_caught') in (True, None) for r in syn for v in r['logger'].values()),
        'null synthetic: no splits or ends detected': syn_sum.get('ps0.0_rot7', {}).get('split', {}).get('detected', 1) + syn_sum.get('ps0.0_rot7', {}).get('end', {}).get('detected', 1) == 0,
        'straight synthetic: split recall >= 0.8': (syn_sum.get('ps0.004_rot0', {}).get('split', {}).get('recall') or 0) >= 0.8,
        'straight synthetic: end recall >= 0.8': (syn_sum.get('ps0.004_rot0', {}).get('end', {}).get('recall') or 0) >= 0.8,
        'colus: no swaps logged (impossible in one section)': TI['swaps'] == 0 and TM['swaps'] == 0,
        'colus: logger Euler and balance hold in every traced patch': TI['euler_fail_frames'] == 0 and TM['euler_fail_frames'] == 0 and TI['balance_fail'] == 0 and TM['balance_fail'] == 0,
        'colus: most patches traced (>= 50% in both modes)': TI['traced'] >= 0.5 * len(pat) and TM['traced'] >= 0.5 * len(pat),
    }
    summ['checks'] = checks
    json.dump(summ, open(os.path.join(out, 'summary.json'), 'w'), indent=1, default=float)
    for k, v in checks.items(): print(('CHECK ok   ' if v else 'CHECK FAIL ') + k, flush=True)
    print(json.dumps(dict(synthetic=syn_sum, image=TI['per_file_per_cell'], mask=TM['per_file_per_cell'], corr=corr,
                          sign=sign_agree, traced=(TI['traced'], TM['traced'])), default=float), flush=True)
    print('PILOT_OK' if all(checks.values()) else 'PILOT_FAIL', flush=True)


if __name__ == '__main__':
    main()
