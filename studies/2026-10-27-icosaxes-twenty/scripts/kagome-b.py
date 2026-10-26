# B (DICTO 2026-10-27): Kagome networks of the golden split, as #17's Kagome hulls in the Stella-Jewel lattice. Icosaxes on the sites
# n in (2Z)^3, Unborn Axes on (2Z+1)^3 (sites scaled by phi/2). A hull: Icosaxes at anchor + offsets (anchor on an Icosaxes site, or on
# an Unborn Axes site for hulls centred there), with the Unborn Axes strictly inside. Kagome rules (#17): no Icosaxes in more than two
# clusters, no two clusters sharing more than one. Every anchor lattice tried; kept when the rules hold. Reported: neighbours per
# cluster, and the share of all Icosaxes held twice / once / by none, in a window.
import itertools, json, numpy as np
from scipy.spatial import ConvexHull
ax = lambda k, s: tuple(s * 2 * (i == k) for i in range(3))
HULLS = {   # name: (anchor on 'I' (Icosaxes) or 'U' (Unborn Axes), offsets of the Icosaxes)
  'octa7':     ('I', [(0, 0, 0)] + [ax(k, s) for k in range(3) for s in (1, -1)]),
  'octa6':     ('I', [ax(k, s) for k in range(3) for s in (1, -1)]),
  'cube8':     ('U', list(itertools.product((-1, 1), repeat=3))),
  'cubocta12': ('I', [p for p in itertools.product((-2, 0, 2), repeat=3) if sorted(map(abs, p)) == [0, 2, 2]]),
  'cubocta13': ('I', [(0, 0, 0)] + [p for p in itertools.product((-2, 0, 2), repeat=3) if sorted(map(abs, p)) == [0, 2, 2]]),
  'cube27':    ('I', list(itertools.product((-2, 0, 2), repeat=3))),
  'rd14':      ('I', [p for p in itertools.product((-4, -2, 0, 2, 4), repeat=3) if sorted(map(abs, p)) in ([0, 0, 4], [2, 2, 2])]),
  'rd15':      ('I', [(0, 0, 0)] + [p for p in itertools.product((-4, -2, 0, 2, 4), repeat=3) if sorted(map(abs, p)) in ([0, 0, 4], [2, 2, 2])]),
}
def inside(offs, odd):
    P = np.array(offs, float); H = ConvexHull(P) if len(P) > 4 else None
    cand = itertools.product(range(-5, 6), repeat=3)
    return [c for c in cand if all((x % 2 == 1) == odd for x in c) and H is not None and (H.equations[:, :3] @ np.array(c) + H.equations[:, 3] < -1e-9).all()]
def lattices():
    out = {}
    for k in (2, 4, 6, 8):
        out[f'sc{k}'] = [np.array(v) * k for v in np.eye(3, dtype=int)]
        out[f'bcc{k}'] = [np.array(v) * (k // 2) for v in ([1, 1, -1], [1, -1, 1], [-1, 1, 1])] if k % 2 == 0 else None
        out[f'fcc{k}'] = [np.array(v) * (k // 2) for v in ([1, 1, 0], [1, 0, 1], [0, 1, 1])]
    return {k: v for k, v in out.items() if v is not None}
R = 5
results = {}
for name, (kind, offs) in HULLS.items():
    base = np.array([1, 1, 1]) if kind == 'U' else np.zeros(3, int)
    odd_inside = inside(offs, kind == 'I')            # relative to the anchor: Unborn Axes sites have odd offsets from an I anchor
    found = []
    for ln, B in lattices().items():
        anchors = [base + sum(c * b for c, b in zip(cf, B)) for cf in itertools.product(range(-R, R + 1), repeat=3)]
        if any(any(x % 2 for x in a + np.array(o)) for a in anchors[:1] for o in offs): continue      # Icosaxes on even sites
        if any(any((x % 2 == 0) for x in a) for a in anchors) and kind == 'U': continue
        if any(any((x % 2 == 1) for x in a) for a in anchors) and kind == 'I': continue
        C = [frozenset(tuple(int(x) for x in a + np.array(o)) for o in offs) for a in anchors]
        cnt = {}
        for c in C:
            for s in c: cnt[s] = cnt.get(s, 0) + 1
        i0 = min(range(len(anchors)), key=lambda i: np.abs(anchors[i] - base).sum())
        share = [len(C[i0] & c) for i, c in enumerate(C) if i != i0]
        W = [s for s in itertools.product(range(-6, 7, 2), repeat=3)]
        if max(cnt.get(s, 0) for s in W) > 2 or max(share) > 1 or max(share) == 0: continue
        found.append({'lattice': ln, 'neighbours': sum(share), 'twice': round(sum(cnt.get(s, 0) == 2 for s in W) / len(W), 3),
                      'once': round(sum(cnt.get(s, 0) == 1 for s in W) / len(W), 3), 'none': round(sum(cnt.get(s, 0) == 0 for s in W) / len(W), 3)})
    results[name] = {'icosaxes': len(offs), 'unbornInside': len(odd_inside), 'anchor': kind, 'nets': found}
    print(f"{name}: {len(offs)} Icosaxes + {len(odd_inside)} Unborn Axes inside, anchored on {'an Unborn Axes' if kind == 'U' else 'an Icosaxes'}")
    for f in found: print('    ', f)
json.dump(results, open('kagome-b.json', 'w'), indent=1)
