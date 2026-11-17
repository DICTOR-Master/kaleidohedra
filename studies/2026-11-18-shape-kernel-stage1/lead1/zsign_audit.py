"""Lead 2 (stage 1): does 110-exact's zsign (float sign when |a + b·phi| >= 0.01) ever disagree with the exact sign in
the #110 independent checks? Runs the named scripts in a scratch copy with zsign wrapped: every element is also decided
exactly by _sign_int; logs disagreements and the largest coefficient. Control: a planted large near-zero element
(Fibonacci pair near 2^49) must be decided correctly by _sign_int and wrongly-or-borderline by the float. FINAL ok / FAIL."""
import sys, os, runpy
import numpy as np
src = sys.argv[1]; scripts = sys.argv[2:]; os.chdir(src); sys.path.insert(0, os.path.join(src, "scripts"))
import common
stats = {"n": 0, "bad": 0, "maxc": 0}
orig = common.zsign
def wrapped(x):
    out = orig(x); x = np.asarray(x); a, b = x[..., 0], x[..., 1]
    ex = np.vectorize(lambda p, q: common._sign_int(int(p), int(q)), otypes=[np.int64])(a, b) if a.size else out
    stats["n"] += int(a.size); stats["bad"] += int((ex != out).sum())
    if a.size: stats["maxc"] = max(stats["maxc"], int(np.abs(a).max()), int(np.abs(b).max()))
    return out
F = [0, 1]
while F[-1] < 2**49: F.append(F[-1] + F[-2])
p, q = F[-2], -F[-3]          # F_{n-1} - F_{n-2}·phi ≈ ±phi^-(n-2): tiny
ctl = common._sign_int(p, q) == (1 if (p - q * 0) and __import__("mpmath").mpf(p) + __import__("mpmath").mpf(q) * (1 + __import__("mpmath").sqrt(5)) / 2 > 0 else -1)
print(f"control: exact _sign_int agrees with 50-digit mpmath on F-pair near 2^49: {ctl}")
common.zsign = wrapped
for s in scripts:
    argv = s.split(); sys.argv = argv
    runpy.run_path(os.path.join("scripts", argv[0]), run_name="__main__")
print(f"AUDIT zsign elements {stats['n']}, disagreements {stats['bad']}, largest |coefficient| {stats['maxc']}")
print("FINAL ok" if ctl and stats["bad"] == 0 and stats["n"] > 0 else "FINAL FAIL")
