#!/usr/bin/env python3
"""Match traced file events against the synthetic truth (control for trace_files.py). Truth positions are in picture pixels
truth positions are carried into the rotated picture by synth.py. A detected split (head with a parent) / end (tail) matches a true one of
the same kind within 2 file spacings tangentially and 3 cell spacings radially (6 for ends: a tapering file's last
lumina are too small to segment, so the traced end lies a few cells inward of the true one); one-to-one. Window: the traced guarded window.
Usage: eval_synth.py IMAGE TRUTH OUT_JSON"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trace_files as TF
from PIL import Image
img = np.array(Image.open(sys.argv[1])); truth = json.load(open(sys.argv[2]))
P, A, sh = TF.lumina(img)
res, geo = TF.analyse(P, A, sh, rings=truth['meta']['rings'])
dt, dr = res['spacing']['tangential_px'], res['spacing']['radial_px']
F, L, R = geo['F'], geo['L'], geo['R']
w = res['window']
def inwin(x, y):
    # window in the traced frame: radial coordinate r (outward), between the guard files tangentially
    rr, tt = TF.frame_coords(np.array([[x, y]]), res['peaks']['radial_deg']); rr = rr[0] * res['outward']['sign']; tt = tt[0]
    if not (w['r0'] < rr < w['r1']): return None
    tl = np.interp(rr, F[L]['r'], F[L]['t']); tr = np.interp(rr, F[R]['r'], F[R]['t'])
    return (rr, tt) if tl < tt < tr else None
out = {}
for kind, det in (('split', [h for h in geo['heads'] if h['parent'] is not None]), ('end', geo['tails'])):
    tru = [e for e in truth['events'] if e['type'] == kind and e.get('xy') and inwin(*e['xy'])]
    tpos = [inwin(*e['xy']) for e in tru]
    dpos = []
    for d in det:
        f = F[d['file']]; i = 0 if kind == 'split' else -1
        dpos.append((f['r'][i], f['t'][i]))
    pairs = sorted((abs(a[0] - b[0]) / dr + abs(a[1] - b[1]) / dt, i, j) for i, a in enumerate(tpos) for j, b in enumerate(dpos)
                   if abs(a[0] - b[0]) <= (3 if kind == 'split' else 6) * dr and abs(a[1] - b[1]) <= 2 * dt)
    ut, ud, m = set(), set(), 0
    for _, i, j in pairs:
        if i in ut or j in ud: continue
        ut.add(i); ud.add(j); m += 1
    out[kind] = dict(true_in_window=len(tru), detected=len(det), matched=m, recall=m / max(len(tru), 1),
                     precision=m / max(len(det), 1))
out['insert_detected'] = sum(h['parent'] is None for h in geo['heads']); out['jumps_detected'] = res['jumps']
out['trace'] = {k: res[k] for k in ('spacing', 'window', 'per_file_per_cell', 'file_cells_in_window')}
json.dump(out, open(sys.argv[3], 'w'), indent=1, default=float)
print('EVAL', json.dumps({k: out[k] for k in ('split', 'end', 'insert_detected', 'jumps_detected')}))
if os.environ.get('EVAL_DEBUG'):
    allt = [(e['type'], inwin(*e['xy'])) for e in truth['events'] if e.get('xy') and inwin(*e['xy'])]
    for kind, det in (('split', [h for h in geo['heads'] if h['parent'] is not None]), ('end', geo['tails'])):
        for d in det:
            f = F[d['file']]; i = 0 if kind == 'split' else -1; p = (f['r'][i], f['t'][i])
            near = sorted(((abs(p[0] - q[0]) / dr + abs(p[1] - q[1]) / dt), ty, round((p[0] - q[0]) / dr, 1), round((p[1] - q[1]) / dt, 1)) for ty, q in allt)[:2]
            print('DBG', kind, round(p[0] / dr, 1), len(f['r']), near)
