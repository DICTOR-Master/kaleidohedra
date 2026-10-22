# DICTO 2026-10-21: Heikegani, two stylings of the Tetoktjiru ("both"): STYLE=samurai, the Heike crab (an angry samurai face on
# every face of each Tetjiru body: brow ridges in a V, eye hollows, nose, down-turned moustache groove, cheeks; the Oktjiru legs in
# armour bands) and STYLE=skull, skull and crossbones (eye sockets, nose hole, teeth, cranium on the bodies; the Oktjiru legs as
# bones with knobbed ends and a slimmer shaft). The relief is added to each piece's own distance, so the pieces still split space with
# no gaps or overlaps (the partition is untouched as a rule; only where the walls run changes). One face on each of the body's four
# sides (opposite each leg), each the same in the body's own frame, so every Tetjiru of a turn is still one shape.
# Run like the two-tone figures: args 0.14 0.05 0.24 0.08, TET_LEN=0.72, STEP=0.015, TEX=0.008 TEX_KIND=tri (the low relief).
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MAIN = "if __name__ == " + "'__main__':"
STYLE = os.environ.get('STYLE', 'samurai'); AMP = float(os.environ.get('AMP', '1.0')); FSC = float(os.environ.get('FSC', '1.0'))   # FSC: feature size
exec(open(os.path.join(HERE, 'jacks_octet.py')).read().split(MAIN)[0])
gauss = lambda a, b, a0, b0, s: np.exp(-((a - a0) ** 2 + (b - b0) ** 2) / (2 * s * s))
def seg(a, b, p, q, w):                                     # soft line from p to q in the face plane
    p, q = np.array(p), np.array(q); d = q - p; t = np.clip(((a - p[0]) * d[0] + (b - p[1]) * d[1]) / (d @ d), 0, 1)
    return np.exp(-((a - p[0] - t * d[0]) ** 2 + (b - p[1] - t * d[1]) ** 2) / (2 * w * w))
def arc(a, b, pts, w):                                      # soft groove along a polyline
    return np.max([seg(a, b, p, q, w) for p, q in zip(pts, pts[1:])], axis=0)
def face_relief(a, b):                                      # > 0 raises, < 0 sinks (face-plane units, body radius about 0.22)
    if STYLE == 'real':
        # the real Heike crab (Heikea japonica): the face is CARVED, deep grooves leaving swollen lobes (DICTO 2026-10-21)
        xs = np.linspace(-0.11, 0.11, 9)
        r = sum(0.022 * gauss(a, b, s_ * .085, -.03, .05) for s_ in (1, -1)) + 0.016 * gauss(a, b, 0, .075, .055)   # cheek and brow lobes swell
        r -= 0.034 * arc(a, b, [(x, .035 + 5.5 * x * x) for x in xs], .012)                                         # the brow groove, a U over the eyes
        r -= sum(0.040 * gauss(a, b, s_ * .045, .015, .019) for s_ in (1, -1))                                       # the eye hollows
        r -= 0.026 * seg(a, b, (0, .03), (0, -.035), .009)                                                           # the groove down the middle
        r -= 0.046 * arc(a, b, [(x, -.06 - 4.5 * x * x) for x in np.linspace(-.1, .1, 9)], .013)                     # the scowling mouth, turned down
        r -= sum(0.03 * seg(a, b, (s_ * .12, .02), (s_ * .1, -.1), .012) for s_ in (1, -1))                          # the cheek grooves
        return r
    if STYLE == 'samurai':
        r = sum(0.028 * seg(a, b, (s * .11, .075), (s * .02, .035), .016) for s in (1, -1))          # brows in a V
        r -= sum(0.032 * gauss(a, b, s * .062, .018, .021) for s in (1, -1))                          # eye hollows
        r += 0.018 * seg(a, b, (0, .02), (0, -.03), .012)                                             # nose
        r -= sum(0.022 * seg(a, b, (0, -.055), (s * .09, -.1), .012) for s in (1, -1))               # moustache groove, turned down
        r += sum(0.016 * gauss(a, b, s * .095, -.035, .028) for s in (1, -1))                         # cheeks
        return r
    r = 0.016 * gauss(a, b, 0, .1, .06)                                                               # cranium
    r -= sum(0.048 * gauss(a, b, s * .058, .025, .029) for s in (1, -1))                             # eye sockets
    r -= 0.034 * (gauss(a, b, -.012, -.03, .013) + gauss(a, b, .012, -.03, .013) + gauss(a, b, 0, -.045, .011))  # nose hole
    r -= 0.018 * seg(a, b, (-.07, -.068), (.07, -.068), .008)                                         # line of the teeth
    r += sum(0.016 * gauss(a, b, x, -.083, .011) for x in np.arange(-.06, .061, .024))              # teeth
    return r
def body_relief(D, L):
    out = np.zeros(len(D))
    for i in (range(1) if STYLE == 'real' else range(4)):      # the real crab: one big face per body, the same side on every body
        u = -L[i]; v = L[(i + 1) % 4] - (L[(i + 1) % 4] @ u) * u; v /= np.linalg.norm(v); w = np.cross(u, v)
        h = D @ u; win = 1 / (1 + np.exp(-(h - .1) / .02))                                           # only on this side
        out += win * face_relief((D @ w) / FSC, (D @ v) / FSC)
    return out
PERP = {0: np.array([0., 1, 0]), 1: np.array([0., 0, 1]), 2: np.array([1., 0, 0])}
def leg_relief(D, L):
    out = np.zeros(len(D))
    for l in L:
        k = int(np.argmax(np.abs(l))); t = D @ l; on = np.exp(-np.sum((D - np.outer(t, l)) ** 2, 1) / (2 * .12 ** 2))
        if STYLE in ('samurai', 'real'):
            band = np.cos(np.pi * t / .11) ** 8; win = 1 / (1 + np.exp(-(t - .25) / .02)) / (1 + np.exp((t - .88) / .02))
            out += 0.014 * band * win * on
        else:
            p = PERP[k]; knob = sum(np.exp(-np.sum((D - (np.outer(np.full(len(D), .9), l) + s * .055 * p)) ** 2, 1) / (2 * .035 ** 2)) for s in (1, -1))
            mid = np.exp(-((t - .5) / .16) ** 2)
            out += 0.03 * knob * (t > 0) - 0.012 * mid * on
    return out
_f0 = field
def field(X, c, L, RHO0, RHO1):
    f = _f0(X, c, L, RHO0, RHO1); D = X - c
    return f - AMP * (leg_relief(D, L) if len(L) == 6 else body_relief(D, L))
TONE = {0: '#b8452f', 1: '#eea58c'}; orient = lambda t: int(round(np.sum(t) - 1.5)) % 2
src = open(os.path.join(HERE, 'jacks_twotone_figs.py')).read(); exec(src[src.index('def part('):src.index('scenes = []')])
scenes = []; add = lambda t_, s_, parts: scenes.append({'title': t_, 'sub': s_, 'parts': parts})
O = np.array([1.0, 0, 0]); TU = np.array([.5, .5, .5])
NAME = {'samurai': ('Heikegani: the samurai crab', 'a samurai face on each side of every body; armoured legs'),
        'skull': ('Heikegani: skull and crossbones', 'a skull on each side of every body; legs as bones'),
        'real': ('Heikegani: the real crab', 'one carved, scowling face per body, as on the Heike crab')}[STYLE]
add(NAME[0], NAME[1], [part(tetrapod_at(TU), TU)])
add('The body, turned', 'another face', [part(tetrapod_at(TU), TU, turn=90)])
add('The legs', 'DICTO Oktjiru', [part(jack(O), O)])
ps = [part(jack(O), O)]
for sg in itertools.product((1, -1), repeat=3):
    t = O + .5 * np.array(sg, float); ps.append(part(tetrapod_at(t), t, .5 * np.array(sg, float)))
add('One Oktjiru among eight bodies', 'drawn apart', ps)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
tail = src[src.index("html = open("):]
TAG = os.environ.get('TAG', ''); exec(tail.replace("'jacks-twotone.html'", f"'heike-{STYLE}{TAG}.html'").replace("'jacks-twotone-labels.json'", f"'heike-{STYLE}{TAG}-labels.json'").replace("print('jacks-twotone.html'", f"print('heike-{STYLE}.html'"))
