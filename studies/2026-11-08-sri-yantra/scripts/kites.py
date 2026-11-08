"""Kite yantras (DICTO 11-08: distort the Cleo yantra to the kite proportion): the great pair with DIFFERENT slopes u (t7, from the
top) and v (t3, from the bottom), plus t1 and t9 base corners on the circle; count the pieces (traditional 43 = 14+10+10+8+1).
Candidates: Cleo/stella (2/phi^2, 1/sqrt2), stella/Cleo, golden/stella (phi/2, 1/sqrt2: near Huet classical), golden/Cleo."""
import mpmath as mp, json, subprocess
from model import solve, all_conditions, order_ok
mp.mp.dps = 60
phi = (1 + mp.sqrt(5)) / 2
C = {"Cleo-Icos 2/phi^2": 2 / phi**2, "stella 1/sqrt2": 1 / mp.sqrt(2), "golden phi/2": phi / 2}
def yan(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def corners(u, v):
    def f(Q, S):
        t = yan(u, v, Q, S); b, w = t["b"], t["w"]
        return [w[1]**2 + b[1]**2 - b[1], w[9]**2 + b[9]**2 - b[9]]
    return f
out = {}
for nu, nv in [("Cleo-Icos 2/phi^2", "stella 1/sqrt2"), ("stella 1/sqrt2", "Cleo-Icos 2/phi^2"), ("golden phi/2", "stella 1/sqrt2"), ("golden phi/2", "Cleo-Icos 2/phi^2")]:
    u, v = C[nu], C[nv]; sol = None
    for Q0 in [mp.mpf(x) / 100 for x in range(45, 62, 2)]:
        for S0 in [mp.mpf(x) / 100 for x in range(78, 96, 2)]:
            try:
                Q, S = mp.findroot(corners(u, v), (Q0, S0), tol=mp.mpf(10)**-50)
                t = yan(u, v, Q, S)
                if order_ok(t, mp.mpf(10)**-30) and max(abs(x) for n, x in all_conditions(t)) < mp.mpf(10)**-40: sol = (Q, S, t); break
            except Exception: pass
        if sol: break
    key = f"u {nu} / v {nv}"
    if not sol: print(key, ": no valid yantra", flush=True); continue
    Q, S, t = sol; b, w = t["b"], t["w"]
    a = {3: mp.mpf(1), 7: mp.mpf(0), 8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9]}
    s = lambda x: {"a": mp.nstr(x, 40)}
    name = "K" + str(len(out) + 1)
    out[name] = {"label": key, "b": {str(i): s(b[i]) for i in range(1, 10)}, "w": {str(i): s(w[i]) for i in range(1, 10)}, "apex": {str(i): s(a[i]) for i in range(1, 10)}}
    json.dump(out, open("kites.json", "w"), indent=1)
    r = subprocess.run(["/home/dicto/geom/bin/python", "figure.py", "kites.json", name, f"kite-{name}.svg", key], capture_output=True, text=True).stdout
    line = [l for l in r.splitlines() if "odd" in l][0]
    print(f"{name}  {key}: P,Q,R,S = {[mp.nstr(x, 5) for x in (v**2/(1+v**2), Q, 1/(1+u**2), S)]}  | {line.split(';', 1)[1].strip()}", flush=True)
print("FINAL ok" if out else "FINAL FAIL: no kite found")
