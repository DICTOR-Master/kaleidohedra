"""Football scutoid study, step 3b part 1: resolve the move band finely. Slices every 0.002 of a period around the voxel height of the
move, fine pixels in a window round the reference cell X(0,0,0); ALL pair contacts in the window are tracked (not only the reference
cell's), so each event is a proper four-cell corner: one pair gains contact while another pair loses it (a T1).
Output: the list of events (height, gained pair, lost pair) -> data file; move_vertex.py then solves each quartet's corner exactly.
Run: STACK=tight python3 tools/runjob.py <this> <data file> <w centre> [half width]"""
import os, sys, json, itertools, numpy as np
WC = float(sys.argv[1]); HW = float(sys.argv[2]) if len(sys.argv) > 2 else 0.04
sys.argv = [sys.argv[0], '0.05']
exec(open('cut_cells.py').read().split('# slices')[0])
PIX = 0.025; R = 4.5                                      # window: R around the reference cell's centre line
ctr = centre(0, 0)
Ein = P1 / np.linalg.norm(P1); Fin = np.cross(n, Ein)
xs = np.arange(-R, R, PIX); X2, Y2 = np.meshgrid(xs, xs, indexing='ij')
name = lambda b: f"{'XY'[imgs[b][0]]}({imgs[b][1]:+d},{imgs[b][2]:+d},{imgs[b][3]:+d})"
NS = int(round(2 * HW / 0.002)) + 1
prev = None; events = []
for k in range(NS):
    w = WC - HW + k * 0.002
    X = ctr + X2[..., None] * Ein + Y2[..., None] * Fin + w * T
    _, idx = tree.query(X.reshape(-1, 3), workers=-1); L = lab[idx].reshape(X2.shape)
    pairs = {}
    for a1, a2 in ((L[1:], L[:-1]), (L[:, 1:], L[:, :-1])):
        d = a1 != a2
        for x, y in zip(a1[d], a2[d]): key = (min(x, y), max(x, y)); pairs[key] = pairs.get(key, 0) + 1
    # keep contacts away from the window edge: both cells must have pixels inside the inner disc
    inner = (X2 ** 2 + Y2 ** 2) < (R - 1.0) ** 2; seen = set(np.unique(L[inner]))
    cur = {p for p, c in pairs.items() if c >= 4 and p[0] in seen and p[1] in seen}
    if prev is not None and cur != prev:
        gained, lost = cur - prev, prev - cur
        events.append(dict(w=w, gained=[list(map(int, p)) for p in gained], lost=[list(map(int, p)) for p in lost]))
        print(f"w {w:+.4f}: gained {[name(a) + '|' + name(b) for a, b in gained]}  lost {[name(a) + '|' + name(b) for a, b in lost]}", flush=True)
    prev = cur
# quartets: a gained pair and a lost pair sharing no cell, all four in a T1
quart = []
for e in events:
    for g in e['gained']:
        for l in e['lost']:
            if not set(g) & set(l): quart.append(dict(w=e['w'], cells=[imgs[c] for c in g + l]))
json.dump(dict(events=events, quartets=quart), open(f"../data-move-events-{os.environ.get('STACK', 'loose')}-{WC:+.3f}.json", 'w'), default=int)
print(f"events {len(events)}, T1 quartets {len(quart)}")
print("FINAL ok" if events else "FINAL FAIL (no event in the band)")
