"""Check: g90's other roots in (0, 1) are not events of the admissible member (no tangential touch of C = 0)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
mp.mp.dps = 60
import yfam as Y
W = json.load(open(os.path.join(Y.ROOT, 'data', 'window-exact.json')))
for r in W['g90_roots_01']:
    c = mp.mpf(r); u = mp.sqrt(c); ms = Y.members(u, u)
    for y in ms:
        d = Y.dets(y)
        print(f"c = {r[:14]}: members {len(ms)}; C-triple det (R4, R6, base5) = {mp.nstr(d[('R4', 'R6', 'base5')], 6)}; H1-free check t = {mp.nstr(y['t'], 8)}")
    if not ms: print(f'c = {r[:14]}: no admissible member')
