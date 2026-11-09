"""Words admitted by one design on a taller patch (what the wave forces in the stacking), plus a SAT model for the figure.
Usage: forced.py TAG MODE MIRROR(1/0) K n FIGWORD out.json"""
import sys, os, json, time, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave_lib as W
t0 = time.time()
TAG, MODE, MIR, K, NP, FIGW, OUTF = sys.argv[1], sys.argv[2], sys.argv[3] == '1', int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7]
NRM = W.lean_normals(); H = W.H
MENU = {}
for name in NRM:
    offs = {H * j / 6 for j in range(-12, 13)}
    for j in range(-3, 3): offs |= {H * (j + 1 / W.PHI), H * (j + 1 / W.PHI ** 2)}
    MENU[name] = sorted(offs)
SR = [W.affine(W.P0, W.P0, p)[0] for p in W.SYM]
def planes_of(tag):
    kind, body = tag.split(':', 1); out = []
    for c, part in enumerate(body.split('+')):
        name, v = part.split('@'); v = float(v[:-1]) * H
        d = min(MENU[name], key=lambda x: abs(x - v))
        if kind in ('C3', 'C3v'):
            for R in ([R for R in SR if np.linalg.det(R) > 0] if kind == 'C3' else SR):
                q = (R @ NRM[name], d, 0)
                if not any(np.allclose(q[0], x[0]) and abs(q[1] - x[1]) < 1e-9 for x in out): out.append(q)
        else: out.append((NRM[name], d, c if kind == '2c' else 0))
    return out
deco = planes_of(TAG)
words = []
for w in itertools.product('ST', repeat=K - 1):
    w = ''.join(w); S = W.Structure(w, NP)
    if W.solve(S, W.signatures(S, deco, MODE), MIR): words.append(w)
    print(f"HEARTBEAT {time.time()-t0:.0f}s word {w} {'yes' if words and words[-1] == w else 'no'}", flush=True)
print(f"{TAG} {MODE} mirrors={MIR}: admitted {len(words)}/{2**(K-1)}: {words}", flush=True)
S = W.Structure(FIGW, 2); r, model = W.solve(S, W.signatures(S, deco, MODE), MIR, want_model=True)
json.dump(dict(title=f"ABC wave {TAG} ({MODE})", planes=[(list(map(float, n)), float(d), int(c)) for n, d, c in deco],
               words=words, stack=dict(word=FIGW, n=2, model=model, radius=1.3) if r else None), open(OUTF, 'w'))
print('FINAL ok' if r is not None else 'FINAL FAIL', f'{time.time()-t0:.0f}s')
