# Aim step 3 (DICTO 5 Nov 2026, "definitely set it up ... exciting"): the hierarchy on its side, with Kari's aperiodic Wang tiles as the engine.
# Rows of tiles = layers of the stacking. Kari (1996): each row multiplies a real number by q = 2 (x in [1/2,1]) or 2/3 (x in [1,2]); tile =
# (north digit, south digit, west carry, east carry) with q*n + w = s + e (Beatty digits B_k(x) = floor(kx) - floor((k-1)x), carries
# c_k = q*floor(kx) - floor(k*q*x)). Carries are tagged by q, so a row never mixes multipliers: the ROW LABEL comes for free.
# Key: layer type c <-> x2 row, h <-> x2/3 row; the stacking word must then follow Kari's aperiodic orbit.
# Tests: (A) calibration: rectangles exist, tori (periodic tilings) do not; (B) coupled shifts: the left/right shift of each row in the vertical
# plane decides c/h (c iff consecutive shifts equal); tori UNSAT; list the stacking words allowed in finite blocks. Float-free (Fractions).
import sys, time, itertools, json
from fractions import Fraction as Fr
from math import floor
from pysat.solvers import Cadical153
t0 = time.time(); LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 280; TMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 12
def hb(msg): print(f"HEARTBEAT {time.time() - t0:.0f}s {msg}", flush=True)
# ---- tiles
T = set()
for q, lo, hi in ((Fr(2), Fr(1, 2), Fr(1)), (Fr(2, 3), Fr(1), Fr(2))):
    for den in (97, 101, 103, 107, 211, 307):
        for a in range(int(lo*den), int(hi*den) + 1):
            x = Fr(a, den)
            if not (lo <= x <= hi): continue
            for k in range(1, 400):
                n = floor(k*x) - floor((k - 1)*x); s = floor(k*q*x) - floor((k - 1)*q*x)
                w = q*floor((k - 1)*x) - floor((k - 1)*q*x); e = q*floor(k*x) - floor(k*q*x)
                T.add((str(q), n, s, str(q) + ":" + str(w), str(q) + ":" + str(e)))   # carries tagged by q: a row cannot mix multipliers
T = sorted(T); print("tiles", len(T), [t for t in T], flush=True)
for (q, n, s, w, e) in T: assert Fr(q)*n + Fr(w.split(":")[1]) == s + Fr(e.split(":")[1])
TAG = {t: (0 if t[0] == "2" else 1) for t in T}   # 0: x2 row (c), 1: x2/3 row (h)
def model(W, H, torus, shifts=False):
    S = Cadical153(); v = {}; nv = [0]
    def var(key):
        if key not in v: nv[0] += 1; v[key] = nv[0]
        return v[key]
    for i in range(W):
        for j in range(H):
            xs = [var(("t", i, j, a)) for a in range(len(T))]; S.add_clause(xs)
            for a, b in itertools.combinations(xs, 2): S.add_clause([-a, -b])
    for i in range(W):
        for j in range(H):
            for a, ta in enumerate(T):
                if torus or i + 1 < W:
                    S.add_clause([-var(("t", i, j, a))] + [var(("t", (i + 1) % W, j, b)) for b, tb in enumerate(T) if tb[3] == ta[4]])
                if torus or j + 1 < H:   # row j+1 is above; its south output feeds... convention: north of row j = south of row j+1
                    S.add_clause([-var(("t", i, j, a))] + [var(("t", i, (j + 1) % H, b)) for b, tb in enumerate(T) if tb[2] == ta[1]])
    for j in range(H):   # row label: type of row j (all tiles of a row share the multiplier; tie to the first cell)
        for a in range(len(T)):
            S.add_clause([-var(("t", 0, j, a)), var(("type", j)) if TAG[T[a]] else -var(("type", j))])
    if shifts:           # shift s_j of row j relative to row j-1 (True = right); layer type c (type 0) iff s_j == s_{j+1}
        for j in range(H):
            if not torus and j + 1 >= H: continue
            sj, sk, ty = var(("s", j)), var(("s", (j + 1) % H)), var(("type", j))
            # ty = 1 (h) <-> sj != sk
            S.add_clause([-ty, sj, sk]); S.add_clause([-ty, -sj, -sk]); S.add_clause([ty, -sj, sk]); S.add_clause([ty, sj, -sk])
    return S, v
# (A) calibration
res = {"tiles": len(T)}
S, v = model(24, 24, False); ok = S.solve(); res["rect_24x24"] = ok; hb(f"open 24x24 rectangle: {'SAT' if ok else 'UNSAT'}")
if ok:
    m = set(x for x in S.get_model() if x > 0); res["rect_types"] = "".join("h" if v[("type", j)] in m else "c" for j in range(24))
S.delete()
tor = []
for W in range(1, TMAX + 1):
    for H in range(1, TMAX + 1):
        S, v = model(W, H, True); ok = S.solve(); S.delete(); tor.append((W, H, ok))
        if ok: print(f"!! periodic tiling on torus {W}x{H}", flush=True)
        if time.time() - t0 > LIM*0.6: break
    hb(f"tori W={W} up to H={H}: periodic found {sum(1 for x in tor if x[2])}")
    if time.time() - t0 > LIM*0.6: break
res["tori_checked"] = len(tor); res["tori_periodic"] = [x[:2] for x in tor if x[2]]
# (B) the key: shifts decide c/h; torus must be UNSAT; list the stacking words of height H in an open W x H block
S, v = model(12, 12, True, shifts=True); res["key_torus_8x8"] = S.solve(); S.delete(); hb(f"key on torus 8x8: {'SAT' if res['key_torus_8x8'] else 'UNSAT'}")
words = {}
HS = [int(x) for x in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['6','8','10'])]; WW = int(sys.argv[4]) if len(sys.argv) > 4 else 16
# itinerary words of Kari's map itself (x2 on [1/2,1], x2/3 on (1,2]), from a dense rational grid, for comparison
def itin(x, H):
    w = ''
    for _ in range(H):
        if x <= 1: w += 'c'; x = 2*x
        else: w += 'h'; x = Fr(2, 3)*x
    return w
for H in HS:
    ORB = {itin(Fr(a, 4099), H) for a in range(2050, 8199)}
    hb(f"Kari orbit words of height {H}: {len(ORB)}"); res.setdefault('orbit', {})[H] = len(ORB)
for H in HS:
    S, v = model(WW, H, False, shifts=True); found = set()
    while S.solve() and len(found) < 5000 and time.time() - t0 < LIM:
        m = set(x for x in S.get_model() if x > 0); w = "".join("h" if v[("type", j)] in m else "c" for j in range(H)); found.add(w)
        S.add_clause([-v[("type", j)] if w[j] == "h" else v[("type", j)] for j in range(H)])
    S.delete(); words[H] = sorted(found); ORBH = {itin(Fr(a, 4099), H) for a in range(2050, 8199)}
    rev = {w[::-1] for w in found}
    hb(f"height {H}, width {WW}: {len(found)} stacking words allowed; Kari orbit words {len(ORBH)}; read top-down: allowed but not an orbit word {len(rev - ORBH)}, orbit words not allowed {len(ORBH - rev)}; read bottom-up: {len(found - ORBH)}, {len(ORBH - found)}")
res["words"] = {k: v_ for k, v_ in words.items()}
json.dump(res, open("kari-key.json", "w"), indent=1)
print(f"FINAL ok tori_checked={res['tori_checked']} periodic={len(res['tori_periodic'])} {time.time() - t0:.0f}s", flush=True)
