# DICTO 2026-10-19 (Gothic figures, Michelangelo's David): spires made to LOOK golden from a chosen viewpoint. Float.
# A pinhole camera at eye E looks at the spire's middle; in the picture we compare the spire's height (base centre -> tip) with its
# width (the base's extent across the line of sight). "Seen" height = the true height that makes picture height / picture width equal
# the true star's ratio seen head-on from far away (height / base width). Viewpoints (DICTO chose both):
#   A inside: the eye at a core corner beside the spike (standing in the valley at its foot), looking up at it;
#   B outside: the eye on the spire's base plane, 6 base radii from its axis, looking at it.
import numpy as np
exec(open('kp.py').read().split('# spike heights')[0])
def picture_ratio(E, base, axis, H):
    c = base.mean(0); tip = c + axis * H; M = c + axis * H / 2
    f = (M - E) / np.linalg.norm(M - E); up = axis - f * (axis @ f); up /= np.linalg.norm(up); rt = np.cross(f, up)
    pr = lambda X: np.array([(X - E) @ rt, (X - E) @ up]) / ((X - E) @ f)
    h = np.linalg.norm(pr(tip) - pr(c)); w = max(abs(pr(p)[0] - pr(q)[0]) for p in base for q in base)
    return h / w
def seen(E, base, axis, target):
    lo, hi = 1e-3, 100.0
    if picture_ratio(E, base, axis, hi) < target: return None
    for _ in range(200):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if picture_ratio(E, base, axis, m) < target else (lo, m)
    return m
for name, core, spk, f in [('great stellated', I, GSD, 3.0), ('small stellated', D1, SSD, 5 ** .5)]:
    base = spk[0][:-1]; c = base.mean(0); axis = c / np.linalg.norm(c); Htrue = np.linalg.norm(spk[0][-1] - c)
    r = np.linalg.norm(base - c, axis=1).max(); width0 = max(np.linalg.norm(p - q) for p in base for q in base)
    target = Htrue / width0                                       # the true spire's ratio seen head-on
    # A: the eye at a core corner beside the spike but not one of its base corners (standing in the valley)
    others = [v for v in core if np.min(np.linalg.norm(base - v, axis=1)) > 1e-9]
    EA = min(others, key=lambda v: np.linalg.norm(v - c))
    side = np.cross(axis, [0.3, 0.7, 0.1]); side /= np.linalg.norm(side)
    EB = c + side * 6 * r
    for lab, E in [('A inside, in the valley at its foot', EA), ('B outside, on its base plane at 6 base radii', EB)]:
        Hs = seen(E, base, axis, target); seen_txt = f'{Hs:.3f} (x{Hs / Htrue:.2f})' if Hs else 'no height reads right from here'
        print(f'{name}: true height {Htrue:.3f}, ratio {target:.3f}; as seen from {lab}: true spire looks {picture_ratio(E, base, axis, Htrue):.3f}; seen height {seen_txt}')
