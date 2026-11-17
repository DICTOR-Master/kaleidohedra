"""Lead 1 (stage 1): did web-of-bonds (#52) ever decide a sign near the 80-digit failure regime?
Runs samples.py in a scratch copy with E.sign wrapped: every decided sign is re-evaluated at 400 digits; logs disagreements,
the smallest |value| decided and the largest coefficient height. Control: a planted large-height near-zero unit must be
caught (wrong or refused) at 80 digits. Study outputs go to the scratch copy only. FINAL ok / FINAL FAIL."""
import sys, os, runpy
src = sys.argv[1]; sys.path.insert(0, src); os.chdir(src)
import mpmath as mp, lib
stats = {"n": 0, "bad": 0, "minabs": None, "maxh": 0}
orig = lib.E.sign
ROOTS = {"Q": lambda: mp.mpf(0), "Q(sqrt5)": lambda: mp.sqrt(5), "Q(sqrt2)": lambda: mp.sqrt(2), "Q(sqrt6)": lambda: mp.sqrt(6),
         "Q(cbrt2)": lambda: mp.cbrt(2), "Q(cbrt6)": lambda: mp.cbrt(6)}
def hp(e):
    with mp.workdps(400):
        r = ROOTS[e.F.name]()
        return sum(mp.mpf(a.numerator) / a.denominator * r**k for k, a in enumerate(e.c))
def wrapped(self):
    s = orig(self)
    if s != 0:
        v = hp(self); t = 1 if v > 0 else -1
        stats["n"] += 1; stats["bad"] += (t != s)
        a = abs(v); stats["minabs"] = a if stats["minabs"] is None or a < stats["minabs"] else stats["minabs"]
        stats["maxh"] = max(stats["maxh"], max(max(abs(c.numerator), c.denominator) for c in self.c))
    return s
a, b = 1, 1
for _ in range(119): a, b = a + 2*b, a + b          # (1+√2)^120 = a + b√2, so a - b√2 = (√2-1)^120 > 0, tiny
ctrl = lib.Q2(a, -b)
try:
    ctl_ok = orig(ctrl) != (1 if hp(ctrl) > 0 else -1)
except AssertionError:
    ctl_ok = True
print(f"control (unit of height {float(a):.2e}, value {mp.nstr(hp(ctrl), 3)}) caught at 80 digits: {ctl_ok}")
lib.E.sign = wrapped
runpy.run_path("samples.py", run_name="__main__")
print(f"AUDIT signs decided {stats['n']}, wrong {stats['bad']}, smallest |value| {mp.nstr(stats['minabs'], 5) if stats['minabs'] is not None else '-'}, largest coefficient height {stats['maxh']}")
print("FINAL ok" if ctl_ok and stats["bad"] == 0 and stats["n"] > 0 else "FINAL FAIL")
