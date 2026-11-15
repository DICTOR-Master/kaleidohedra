"""Event census of a 3D grain-growth run (mbo3d.py output) with the shared event logger, used unchanged (md5 recorded).
Frames carry contacts with their areas (voxel faces); a contact counts when its area >= amin (amin = 1 and 4).
- logger (dim 3, contacts only: no edges or corners on a voxel grid) at strides 1, 2, 4; negative control;
- contact gains and losses between grains alive in both frames; persistence: the new (lost) contact lasts (had lasted) k frames
  (frames are written every 1% of grains lost, so k frames ~ k% coarsening; k = 1, 3, 5);
- identity check: in a steady state the faces per grain stay at <F>, so survivors' net contact change per vanished grain
  = f_v - <F>/2, where f_v = faces of the vanishing grain in its last frame (accounting identity; checked on the run);
- faces of vanishing grains at small volume (from the simulation).
Usage: census3d.py RUNDIR OUT.json"""
import sys, os, json, hashlib
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
LOGDIR = os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')
sys.path.insert(0, LOGDIR)
import eventlog as E
MD5 = hashlib.md5(open(os.path.join(LOGDIR, 'eventlog.py'), 'rb').read()).hexdigest()
run, outp = sys.argv[1], sys.argv[2]
fin = json.load(open(os.path.join(run, 'final.json'))); N0 = fin['params']['N0']
frames = [json.loads(l) for l in open(os.path.join(run, 'frames3d.jsonl'))]
out = dict(run=os.path.basename(run.rstrip('/')), logger_md5=MD5, params=fin['params'], status=fin['status'], frames=len(frames),
           faces_at_small_volume=fin['faces_at_small_volume'], by_amin={})
okall = True
for amin in (1, 4):
    sets = [{(a, b) for a, b, c in f['contacts'] if c >= amin} for f in frames]
    cells = [set(f['cells']) for f in frames]
    lg = {}
    for s in (1, 2, 4):
        idx = list(range(0, len(frames), s))
        cnt, bal, neg = Counter(), 0, None
        prevT = None
        for i in idx:
            T = E.Tiling(cells[i], sorted(sets[i]), None, 3, 'space', frames[i]['t'])
            if prevT is not None:
                ev = E.classify(prevT, T)
                if not E.balance(prevT, T, ev)[0]: bal += 1
                if neg is None and any(e['net'] for e in ev):
                    bad = [dict(e) for e in ev]; j = next(j for j, e in enumerate(bad) if e['net']); bad[j]['type'] = 'contact gained'
                    neg = not E.balance(prevT, T, bad)[0]
                for e in ev: cnt[e['type']] += 1
            prevT = T
        lg[f'stride{s}'] = dict(counts=dict(cnt), balance_failures=bal, neg_control_caught=neg)
        okall &= bal == 0 and neg is not False
    # contact histories (survivor gains / losses) with persistence, per window of grain number
    wins = [(N0, N0 // 2), (N0 // 2, N0 // 4), (N0 // 4, 0)]
    def win(Nv):
        for a, b in wins:
            if b < Nv <= a: return f'{a}-{b}'
    W = defaultdict(Counter)
    present = defaultdict(list)                      # pair -> list of frame indices present
    for i, S in enumerate(sets):
        for p in S: present[p].append(i)
    def run_len(p, i, fwd):                          # frames the contact stays (fwd) / had stayed (back) from frame i
        sset = set(present[p]); k = 0
        j = i
        while 0 <= j < len(sets) and j in sset: k += 1; j += 1 if fwd else -1
        return k, (j >= len(sets) or j < 0)
    for i in range(1, len(frames)):
        A, B = sets[i - 1], sets[i]; kept = cells[i - 1] & cells[i]; w = win(len(cells[i]))
        died = cells[i - 1] - cells[i]
        W[w]['vanished'] += len(died)
        fv = Counter(); [fv.update([a, b]) for a, b in A]
        W[w]['faces of vanished at last frame'] += sum(fv[g] for g in died)
        for p in B - A:
            if p[0] in kept and p[1] in kept:
                W[w]['gained'] += 1
                for k in (3, 5):
                    L1, cen = run_len(p, i, True)
                    if L1 >= k: W[w][f'gained persistent k{k}'] += 1
                    elif cen: W[w][f'gained censored k{k}'] += 1
        for p in A - B:
            if p[0] in kept and p[1] in kept:
                W[w]['lost'] += 1
                for k in (3, 5):
                    L1, cen = run_len(p, i - 1, False)
                    if L1 >= k: W[w][f'lost persistent k{k}'] += 1
    stats = [json.loads(l) for l in open(os.path.join(run, 'stats.jsonl'))]
    res = {}
    for w, c in W.items():
        if not c['vanished']: continue
        ss = [s for s in stats if w and int(w.split('-')[1]) < s['N'] <= int(w.split('-')[0])]
        mF = (sum(s['meanF'] if amin == 1 else s['meanF4'] for s in ss) / len(ss)) if ss else None
        d = c['vanished']
        r = {k + ' per vanished': v / d for k, v in c.items() if k != 'vanished'}
        r['vanished'] = d
        r['net (gained - lost) per vanished'] = (c['gained'] - c['lost']) / d
        r['mean F in window'] = mF
        if mF: r['identity: f_v - <F>/2'] = c['faces of vanished at last frame'] / d - mF / 2
        res[w] = r
    out['by_amin'][str(amin)] = dict(logger=lg, windows=res)
st = [json.loads(l) for l in open(os.path.join(run, 'stats.jsonl'))]
out['topology_last'] = {k: st[-1][k] for k in ('N', 'meanF', 'mu2F', 'meanF4', 'mu2F4', 'Rbar', 'sigma')}
out['meanF_series'] = [(s['N'], round(s['meanF'], 3), round(s['meanF4'], 3)) for s in st[:: max(1, len(st) // 30)]]
out['ok'] = okall
json.dump(out, open(outp, 'w'), indent=1)
print('CENSUS3D_OK' if okall else 'CENSUS3D_FAIL', out['run'], json.dumps(out['topology_last']))
