# exploration (floating point, the 4 Nov DFS code): edge-to-edge search with pieces from a finite set of RT frames.
# frame of a piece = the RT (round its apex) it is a centre pyramid of, up to translation; class O = frame 0.
# F1 = frame 0 plus the 16 frames one 'swapped-end' move away: frame 0 turned 36 deg about one of its 6 five-fold axes or 60 deg about one of its 10 three-fold axes.
import sys, os, numpy as np, time, math, itertools
maxd = int(sys.argv[1]); cap = int(sys.argv[2]); level = int(sys.argv[3])
sys.argv = [sys.argv[0], '1', '1', 'RT']
src = open(os.path.expanduser('~/k-research/studies/2026-11-04-rt-pyramids/scripts/rt_pyramids.py')).read().split('maxd = int(')[0]
exec(src)
A0 = (P0[1:] - P0[0]).T; _n = np.linalg.norm(RTV, axis=1); THR = (_n.min() + _n.max())/2
fivef = np.array([v for v in RTV if np.linalg.norm(v) > THR]); fivef = fivef/np.linalg.norm(fivef, axis=1)[:, None]
threef = np.array([v for v in RTV if np.linalg.norm(v) < THR]); threef = threef/np.linalg.norm(threef, axis=1)[:, None]
assert len(fivef) == 12 and len(threef) == 20
def fkey_from_g(g):
    w = (g @ fivef.T).T; w = np.array([x if (x[np.argmax(np.abs(x) > 1e-6)] > 0) else -x for x in w])
    return tuple(sorted(tuple(np.round(x, 5)) for x in w))
def gof(t): return (t[1:] - t[0]).T @ np.linalg.pinv(A0)
def R(ax, ang):
    ax = ax/np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]]); return np.eye(3) + math.sin(ang)*K + (1 - math.cos(ang))*K @ K
frames = {fkey_from_g(np.eye(3)): np.eye(3)}; layer = [np.eye(3)]
for lv in range(level):
    nl = []
    for g in layer:
        for a in (g @ fivef.T).T[:6] if False else (g @ fivef.T).T:
            h = R(a, math.radians(36)) @ g; k = fkey_from_g(h)
            if k not in frames: frames[k] = h; nl.append(h)
        for d in (g @ threef.T).T:
            h = R(d, math.radians(60)) @ g; k = fkey_from_g(h)
            if k not in frames: frames[k] = h; nl.append(h)
    layer = nl
print('frames allowed', len(frames), flush=True)
_sc = sector_candidates
def sector_candidates(t, i, j, dih): return [[c for c in cs if fkey_from_g(gof(c)) in frames] for cs in _sc(t, i, j, dih)]
st = {'nodes': 0, 'cap': cap, 'capped': False, 't0': time.time(), 'maxd': maxd}
todo = [(0, a, b, d, kk) for a, b, d in E0 for kk in range(int(round(2*math.pi/d)) - 1)]
KIND = f'RTframes{level}'
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'), exist_ok=True)
ok = search([P0], todo, maxd, st)
used = {fkey_from_g(gof(np.array(t))) for t in []}
print({'frames_level': level, 'frames': len(frames), 'best_patch': st.get('best_patch'), 'some_branch_reaches_max': ok, 'nodes': st['nodes'], 'capped': st['capped'], 'seconds': round(time.time() - st['t0'])}, flush=True)
