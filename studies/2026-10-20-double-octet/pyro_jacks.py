# DICTO 2026-10-21: Tetoktjiru with PYROCHLORE CHAINS ("swap the legs ... within the structure like a pyrochlore type"; chose the
# branching network). An eighth of the octet's tetrahedra form a true pyrochlore: an up and a down tetrahedron meet at every shared
# corner, each of its corners shared by exactly 2 (checked; half of all corners are on the network; centres on a diamond net: A = (1/2,1/2,1/2) + FCC of cube 4, B = A - (1,1,1)). Those
# Tetjiru SWAP their legs: from out through the faces to out to the 4 corners, where they meet the partner's leg, so together they
# form one continuous coral network, branching four ways at each Tetjiru. The other Tetjiru and the Oktjiru stay as they were and
# fill the rest of space (same skeleton-nearest partition as jacks_octet.py).
# Colours (DICTO: "more mixed with each other ... part of the patterning", "derived from the structure of the coral blocks itself"):
# closer coral tones, and the colour on a wall is set by the two pieces that meet there plus a lattice-periodic triangle-hexagon
# mottle, so both sides of a join carry the same pattern and the joins disappear into it; legs pale slightly towards the tips.
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "if __name__ == " + "'__main__':"
exec(open(os.path.join(HERE, 'jacks_octet.py')).read().split(MAIN)[0])
STEP = float(os.environ.get('STEP', '0.03')); PY0, PY1, PY_LEN = float(os.environ.get('PY0', '0.12')), float(os.environ.get('PY1', '0.07')), np.sqrt(3) / 2   # thinner network legs (DICTO 10-21; were 0.17, 0.11)
_FCC4 = [(0, 0, 0), (2, 2, 0), (2, 0, 2), (0, 2, 2)]
def pyro(q):
    """'A' (up) or 'B' (down) if the tetrahedron centred at q is in the pyrochlore network, else None"""
    v = np.round(np.array(q, float) - .5).astype(int)
    if tuple(v % 4) in _FCC4: return 'A'
    if tuple((v + 1) % 4) in _FCC4: return 'B'
def field(X, c, L, RHO0, RHO1, R0=None):
    R0 = R0 or (1.0 if len(L) == 6 else TET_LEN); D = X - c; ds = []
    for l in L:
        t = np.clip(D @ l / R0, 0, 1); ds.append(np.linalg.norm(D - np.outer(t * R0, l), axis=1) - (RHO0 * (1 - t) + RHO1 * t))
    ds = np.array(ds); m = ds.min(0); return m - K * np.log(np.exp(-(ds - m) / K).sum(0))
def kind(p):
    p = np.array(p, float)
    if np.allclose(p, np.round(p)): return 'okt'
    return 'net' if pyro(p) else 'tet'
def site(p):
    """(centre, legs, RHO0, RHO1, R0) of the piece at p"""
    p = np.array(p, float); k = kind(p)
    if k == 'okt': return (p, AX, RHO_OCT, TIP_OCT, 1.0)
    if k == 'net': return (p, tet_legs(p), PY0, PY1, PY_LEN)
    return (p, -tet_legs(p), RHO_TET, TIP_TET, TET_LEN)
def centres_near(c, rad):
    c = np.array(c, float); out = []; lo = np.floor(c - rad).astype(int); hi = np.ceil(c + rad).astype(int)
    for p in itertools.product(*[range(a, b + 1) for a, b in zip(lo, hi)]):
        p = np.array(p, float)
        if int(p.sum()) % 2 and np.linalg.norm(p - c) <= rad: out.append(site(p))
        if np.linalg.norm(p + .5 - c) <= rad: out.append(site(p + .5))
    return out
def classkey(p):
    """pieces whose positions differ by the pyrochlore period (FCC of cube 4) have the same surroundings, so the same shape"""
    p = np.array(p, float); off = p - np.floor(p); v = np.floor(p).astype(int)
    reps = [tuple((v - np.array(o)) % 4) for o in _FCC4]; return (tuple(np.round(off, 1)), min(reps))
_pc = {}
def piece(p):
    p = np.array(p, float); key = classkey(p)
    if key not in _pc:
        o = site(p); c = o[0]; half = 1.35; n = int(round(2 * half / STEP)) + 1; ax = np.linspace(-half, half, n)
        G = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3) + c
        others = [s for s in centres_near(c, 2 * half + .2) if np.linalg.norm(s[0] - c) > 1e-9]
        fc = field(G, *o); m = np.full(len(G), np.inf)
        for s in others: m = np.minimum(m, field(G, *s))
        g = gaussian_filter((fc - m).reshape(n, n, n), 1.2 * 0.02 / STEP)
        g[0], g[-1], g[:, 0], g[:, -1], g[:, :, 0], g[:, :, -1] = 1, 1, 1, 1, 1, 1
        V, F, _, _ = marching_cubes(g, 0.0, spacing=(STEP,) * 3); V = V - half + c
        mf = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(F, np.uint32)))
        if mf.volume() < 0 or mf.status() != m3.Error.NoError:
            mf = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(F[:, ::-1], np.uint32)))
        _pc[key] = (c, mf); print('mesh', kind(p), key, round(mf.volume(), 4), flush=True)
    c0, mf = _pc[key]; return mf.translate(list(p - c0))
# colours: close coral tones
TONE = {'okt': np.array([196, 81, 60]), 'tet': np.array([229, 138, 111]), 'net': np.array([214, 104, 74])}
MOT_N = 5
def mottle(X):                       # lattice-periodic triangle-hexagon pattern in -1..1 (same at a point for both sides of a wall)
    w = np.cos(np.pi * MOT_N * (X @ _TD.T)).sum(1); return np.tanh(3.0 * w)
def colours(mf, p):
    """per-triangle colour: the two pieces meeting at the wall, mixed by the mottle; slightly paler towards the leg tips"""
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts); X = P[T].mean(1)
    p = np.array(p, float); own = kind(p); others = [s for s in centres_near(p, 2.9) if np.linalg.norm(s[0] - p) > 1e-9]
    D = np.array([field(X, *s) for s in others]); nb = [kind(others[i][0]) for i in D.argmin(0)]
    u = 0.5 + 0.5 * mottle(X)
    order = ['okt', 'net', 'tet']
    pair = [sorted([own, b], key=order.index) for b in nb]
    col = np.array([TONE[a] * w + TONE[b] * (1 - w) for (a, b), w in zip(pair, u)])
    r = np.linalg.norm(X - p, axis=1); pale = np.clip((r - 0.35) / 0.6, 0, 1)[:, None] * 0.18
    col = col * (1 - pale) + 255 * pale
    return ['#%02x%02x%02x' % tuple(int(round(x)) for x in c) for c in np.clip(col, 0, 255)]
def part(p, shift=(0, 0, 0)):
    mf = piece(p); me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]) + np.array(shift)
    return {'v': np.round(P, 5).tolist(), 't': np.asarray(me.tri_verts).tolist(), 'c': colours(mf, p), 'e': None, 'a': 1.0}
if __name__ == '__main__':
    A0 = np.array([.5, .5, .5])
    corners = A0 + tet_legs(A0) * PY_LEN; Bs = [2 * cn - A0 for cn in corners]        # the 4 down partners, across the 4 corners
    assert pyro(A0) == 'A' and all(pyro(b) == 'B' for b in Bs)
    As = {tuple(np.round(2 * cn - b, 3)) for b in Bs for cn in b + tet_legs(b) * PY_LEN} - {tuple(A0)}
    assert all(pyro(a) == 'A' for a in As)
    # check: one period (4 x 4 x 4 box) is filled exactly once
    box = m3.Manifold.cube([4, 4, 4]); tot = 0.0; vols = {}
    for q in itertools.product(range(-1, 6), repeat=3):
        for p in [np.array(q, float), np.array(q, float) + .5]:
            if np.allclose(p, np.round(p)) and int(p.sum()) % 2 == 0: continue
            if np.any(p < -0.9) or np.any(p > 4.9): continue
            mf = piece(p); vols.setdefault(kind(p), set()).add(round(mf.volume(), 3)); tot += (mf ^ box).volume()
    print('volumes by kind:', {k: sorted(v) for k, v in vols.items()})
    print(f'4 x 4 x 4 box (one period): pieces sum to {tot:.4f} (64; marching-cubes mesh, step {STEP})')
    scenes = []; add = lambda t_, s_, parts: scenes.append({'title': t_, 'sub': s_, 'parts': parts})
    add('Network Tetjiru', 'legs swapped: out to its 4 corners', [part(A0)])
    add('A branch of the network', 'up and down Tetjiru joined corner to corner', [part(A0)] + [part(b) for b in Bs] + [part(np.array(a)) for a in sorted(As)])
    add('DICTO Oktjiru', 'six legs, beside the network', [part((1, 0, 0))])
    add('DICTO Tetjiru', 'four legs, out through its faces', [part((1.5, .5, .5))])
    blk = []
    for q in itertools.product(range(0, 3), repeat=3):
        for p in [np.array(q, float), np.array(q, float) + .5]:
            if np.allclose(p, np.round(p)) and int(p.sum()) % 2 == 0: continue
            if np.any(p > 2.6): continue
            blk.append(part(p, (p - 1.25) * 0.22))
    add('A block', 'network, Oktjiru and Tetjiru, slightly apart', blk)
    for s in scenes:
        pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
        for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
        s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
    html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
    html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
    html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
    html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
    os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
    open(os.path.join(HERE, 'renders', 'pyro-jacks.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
    json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'pyro-jacks-labels.json'), 'w'), indent=1)
    print('pyro-jacks.html', len(scenes))
