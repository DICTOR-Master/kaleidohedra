# window_controls.py, DICTO OG Galois-twin window test (queued 12 Nov 2026), CONTROLS for the window detector.
# The detector (window_tools.classify) reads a sequence of growing point sets in Q(sqrt5)^d through their Galois twins (sqrt5 -> -sqrt5):
#   UNBOUNDED  twin radius grows (more than x10 over the run)
#   COLLAPSE   twin radius shrinks to the centre (last/first < 1e-3)
#   WINDOW     twin radius settles AND the twins fill their hull (covering ratio rho -> small, falling as the patch grows)
# Controls with known answers (each must be classified as stated, or FINAL FAIL):
#   P1 Fibonacci chain (substitution L -> LS, S -> L; L = phi, S = 1): a model set, window an interval of length phi  -> WINDOW
#   P2 Fibonacci cube (product of three chains): a 3D model set, window a cube                                       -> WINDOW
#   P3 icosahedral model set from Z^6 (Ammann-Kramer type): window = the rhombic triacontahedron (zonotope of the six
#      twin five-fold axes); its twin hull must read 32 corners, 30 rhombi                                               -> WINDOW
#   N1 arithmetic progression n*phi (not a model set: twin -n/phi)                                                     -> UNBOUNDED
#   N2 powers phi^n (Pisot: twin (-1/phi)^n -> 0; not relatively dense, not a model set)                               -> COLLAPSE
# Exact arithmetic: numbers a + b sqrt5 as integer/rational pairs; twins computed exactly then rounded once.
# usage: python -u window_controls.py <out.json>
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from window_tools import classify, hull_fingerprint, ico_axes, covering_ratio
t0 = time.time(); OUT = sys.argv[1]; ok = True; res = {}
S5 = 5 ** .5
def val(a, b): return float(a) + float(b) * S5            # real embedding
def twin(a, b): return float(a) - float(b) * S5           # Galois twin (a, b exact; inputs here are small, no cancellation issue)
def report(name, want, levels):
    global ok
    c = classify(levels); good = c['class'] == want; ok &= good
    print(f'{name}: class {c["class"]} (want {want}) {"ok" if good else "FAIL"} | twin radius by level {["%.3g" % r for r in c["R"]]} | '
          f'covering ratio {["%.3g" % r for r in c["rho"]]}', flush=True)
    res[name] = dict(c, want=want, ok=bool(good))
    return c
# ---- P1 Fibonacci chain: positions are sums of tiles; phi = (1 + sqrt5)/2 -> L = (1/2, 1/2), S = (1, 0)
w = 'L'
for _ in range(22): w = ''.join('LS' if ch == 'L' else 'L' for ch in w)
pos = [(Fr(0), Fr(0))]
for ch in w:
    a, b = pos[-1]; pos.append((a + Fr(1, 2), b + Fr(1, 2)) if ch == 'L' else (a + 1, b))
lv = []
for n in (200, 800, 3200, 12800, 51200):
    P = np.array([[twin(a, b)] for a, b in pos[:n]]); lv.append(P)
report('P1 Fibonacci chain', 'WINDOW', lv)
L1 = float(np.ptp(lv[-1])); print(f'  P1 window length {L1:.6f} (model set: phi = {(1 + S5) / 2:.6f})', flush=True); ok &= abs(L1 - (1 + S5) / 2) < 1e-3
# ---- P2 Fibonacci cube
lv = []
for n in (8, 16, 32, 64):
    t = [twin(a, b) for a, b in pos[:n]]
    lv.append(np.array([(x, y, z) for x in t for y in t for z in t]))
c = report('P2 Fibonacci cube', 'WINDOW', lv)
fp = hull_fingerprint(lv[-1]); print(f'  P2 twin hull: {fp["corners"]} corners, faces {fp["faces"]} (cube: 8 corners, 6 four-sided)', flush=True)
ok &= fp['corners'] == 8 and fp['faces'] == {4: 6}
# ---- P3 icosahedral model set from Z^6: real e_i = five-fold axes (0, +-1, phi) cyclic, twin = (0, +-1, 1 - phi)
ax = [((0, 0), (1, 0), (Fr(1, 2), Fr(1, 2))), ((0, 0), (-1, 0), (Fr(1, 2), Fr(1, 2))), ((1, 0), (Fr(1, 2), Fr(1, 2)), (0, 0)),
      ((-1, 0), (Fr(1, 2), Fr(1, 2)), (0, 0)), ((Fr(1, 2), Fr(1, 2)), (0, 0), (1, 0)), ((Fr(1, 2), Fr(1, 2)), (0, 0), (-1, 0))]
E = np.array([[val(*c_) for c_ in v] for v in ax]); ET = np.array([[twin(*c_) for c_ in v] for v in ax])
win = np.array([sum(s * ET[i] for i, s in enumerate(sg)) for sg in np.array(np.meshgrid(*[[0, 1]] * 6)).T.reshape(-1, 6)])   # projection of the unit 6-cube
from scipy.spatial import ConvexHull
H = ConvexHull(win); Aw, bw = H.equations[:, :3], H.equations[:, 3]
B6 = 5; g = np.arange(-B6, B6 + 1); Z = np.array(np.meshgrid(*[g] * 6), dtype=np.int8).T.reshape(-1, 6)
Zt = Z @ ET; inside = (Zt @ Aw.T + bw).max(1) <= 1e-12; Zr = Z[inside] @ E; Zt = Zt[inside]
edge = np.abs(Z[inside]).max(1) == B6; RMAX = 12.0
box_ok = not (np.linalg.norm(Zr[edge], axis=1) <= RMAX).any(); ok &= box_ok
print(f'  P3 lattice box +-{B6}: no window point on the box edge within real radius {RMAX}: {box_ok}', flush=True)
del Z
lv = []
for R in (3.0, 6.0, 9.0, RMAX):
    sel = np.linalg.norm(Zr, axis=1) <= R; lv.append(Zt[sel])
report('P3 icosahedral (Z^6, triacontahedron window)', 'WINDOW', lv)
fp = hull_fingerprint(lv[-1], ico_axes(twin_frame=True)); fw = hull_fingerprint(win, ico_axes(twin_frame=True))
print(f'  P3 twin hull: {fp["corners"]} corners, faces {fp["faces"]}, support h5:h3:h2 = {fp["h"]} | window itself: {fw["corners"]} corners, faces {fw["faces"]}, h {fw["h"]}', flush=True)
ok &= fw['corners'] == 32 and fw['faces'] == {4: 30} and fp['corners'] == 32 and fp['faces'] == {4: 30}
res['triacontahedron_fingerprint'] = fw
# ---- N1 progression n*phi; N2 powers of phi (exact by the recurrence phi^(n+1) = phi^n + phi^(n-1) on (a, b) pairs)
report('N1 progression n*phi', 'UNBOUNDED', [np.array([[twin(Fr(n, 2), Fr(n, 2))] for n in range(N)]) for N in (10, 100, 1000, 10000)])
pw = [(Fr(1), Fr(0)), (Fr(1, 2), Fr(1, 2))]
for _ in range(80): pw.append((pw[-1][0] + pw[-2][0], pw[-1][1] + pw[-2][1]))
def twin_exact(a, b): return float(a * a - 5 * b * b) / (float(a) + float(b) * S5) if b else float(a)   # a - b sqrt5 = (a^2 - 5b^2)/(a + b sqrt5), a, b > 0: no cancellation
report('N2 powers phi^n (Pisot)', 'COLLAPSE', [np.array([[twin_exact(*pw[n])]]) for n in (1, 10, 20, 40, 80)])
json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(f'controls done in {time.time() - t0:.0f} s')
print('CONTROLS ok' if ok else 'CONTROLS FAIL')
sys.exit(0 if ok else 1)
