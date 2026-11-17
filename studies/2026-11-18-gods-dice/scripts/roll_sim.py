#!/usr/bin/env python3
"""God's Dice, test 3 side check (COMPUTED, Monte Carlo): a second, quasi-static model of the die.
DICTO · dictospheres.com

Model (Varkonyi-Domokos style quasi-static rolling): the die touches the table with a uniformly random down-direction u;
it then rolls without bouncing so that its centre (= centre of mass) always goes down: u follows the steepest descent of the
support height h(u) = max_v v.u on the sphere until it settles at a face normal. P(face) = measure of its basin.
This is NOT the solid-angle model (which counts the cone over the face from the centre); the two differ in general.
Controls: cube 1/6 per face, octahedron 1/8 per face (by symmetry); solid-angle values at the same mu for comparison.
Run: python roll_sim.py [N]   (numpy; on a compute host). Output data/roll-sim.json; FINAL line conditional."""
import itertools, json, math, os, sys, time
import numpy as np

T0 = time.time()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
rng = np.random.default_rng(20261118)
U0 = rng.normal(size=(N, 3)); U0 /= np.linalg.norm(U0, axis=1)[:, None]

def corners(mu):
    if mu <= 1: base = (mu, 0, 0)
    elif mu <= 2: base = (1, mu - 1, 0)
    else: base = (1, 1, mu - 2)
    s = set()
    for p in itertools.permutations(base):
        for g in itertools.product((1, -1), repeat=3):
            s.add(tuple(round(a * b, 15) for a, b in zip(p, g)))
    return np.array(sorted(s))
CN = np.vstack([np.eye(3), -np.eye(3)])
ON = np.array(list(itertools.product((1, -1), repeat=3))) / math.sqrt(3)
FN = np.vstack([CN, ON])        # 6 cube-plane faces, then 8 octahedron-plane faces

def roll(mu, U=U0, iters=900):
    V = corners(mu); u = U.copy()
    for k in range(iters):
        eta = 0.06 * (1 - k / iters) + 0.0005
        idx = np.argmax(u @ V.T, axis=1); v = V[idx]
        g = v - np.sum(v * u, axis=1)[:, None] * u          # gradient of v.u on the sphere
        u = u - eta * g; u /= np.linalg.norm(u, axis=1)[:, None]
    # u descends AWAY from the touching corner?  h(u) = v.u decreases along -g: yes, steepest descent.
    lab = np.argmax(u @ FN.T, axis=1)
    near = np.max(u @ FN.T, axis=1)
    return lab, near

def solid_angle_pC(mu):
    if mu <= 2:
        b = mu - 1; return math.atan(b * b / 2 / math.sqrt(1 + b * b)) / math.pi
    a = mu - 2; t = (1 - a)**2 * (a + 2) / (math.sqrt(a * a + 2) * (a * a + 6 * a + 5))
    return 1 / 6 - 2 * math.atan(t) / (3 * math.pi)

CHECKS = []
def check(n, ok, info=''):
    CHECKS.append((n, bool(ok))); print(('  ok  ' if ok else '  FAIL') + ' ' + n + ('  ' + str(info) if info != '' else ''), flush=True)

res = {}
def run(mu, name):
    lab, near = roll(mu)
    pC = np.mean(lab < 6) / 6; pO = np.mean(lab >= 6) / 8
    se = math.sqrt(np.mean(lab < 6) * (1 - np.mean(lab < 6)) / N) / 6
    res[name] = dict(mu=mu, p_cube_face=pC, p_oct_face=pO, se_cube_face=se, min_alignment=float(near.min()),
                     solid_angle_p_cube_face=solid_angle_pC(mu))
    print(f'  {name:24s} mu={mu:.6f}  quasi-static p_C={pC:.5f} ± {se:.5f}  p_O={pO:.5f}   solid-angle p_C={solid_angle_pC(mu):.5f}   min cos to face normal {near.min():.6f}', flush=True)
    return pC, se, near

print(f'quasi-static rolling, N = {N}', flush=True)
pc, se, near = run(3.0, 'cube (control)')
check('control cube: p = 1/6 per face within 4 SE', abs(pc - 1 / 6) < 4 * se + 1e-12)
pc, se, near = run(1.0, 'octahedron (control)')
check('control octahedron: cube-plane faces absent (p_C = 0), 1/8 each otherwise', pc == 0 and abs(res['octahedron (control)']['p_oct_face'] - 1 / 8) < 1e-12)
for mu, nm in [(1.5, 'Kelvin 3/2'), (math.sqrt(3), 'turn fixed point sqrt3'), (1.7565821359450421, 'solid-angle fair mu_f'),
               (2.0, 'cuboctahedron 2'), (1 + math.sqrt(2), 'truncated cube 1+sqrt2')]:
    pc, se, near = run(mu, nm)
    check(f'{nm}: every sample settled on a face (cos to nearest face normal > 0.9999)', near.min() > 0.9999)
# quasi-static fair point by bisection on p_C = 1/14 (common random numbers)
lo, hi = 1.3, 2.4
Ns = min(N, 40000)
for it in range(12):
    m = (lo + hi) / 2
    lab, _ = roll(m, U0[:Ns], iters=700)
    if np.mean(lab < 6) / 6 < 1 / 14: lo = m
    else: hi = m
muq = (lo + hi) / 2
lab, _ = roll(muq)
res['quasi_static_fair'] = dict(mu=muq, p_cube_face_at_it=float(np.mean(lab < 6) / 6), note='bisection, 12 steps, N=4e4 common random numbers; statistical, not exact')
print(f'  quasi-static fair point mu_q ≈ {muq:.4f} (solid-angle fair point 1.75658); p_C there with N={N}: {np.mean(lab < 6) / 6:.5f}', flush=True)
check('quasi-static fair point found inside chamber I (1,2)', 1 < muq < 2)
ok = all(c[1] for c in CHECKS)
res['checks'] = CHECKS; res['ok'] = ok; res['N'] = N; res['seconds'] = round(time.time() - T0, 1); res['mark'] = 'DICTO · dictospheres.com'
json.dump(res, open(os.path.join(OUT, 'roll-sim.json'), 'w'), indent=1)
print(f'{time.time() - T0:.0f} s'); print('FINAL ok' if ok else 'FINAL FAIL: ' + '; '.join(n for n, o in CHECKS if not o))
