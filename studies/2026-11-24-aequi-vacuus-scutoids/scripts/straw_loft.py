"""The straw loft shared by app_data.py and loft_full.py (28 Nov 2026). With Claude (Anthropic)."""
import numpy as np

def unit(a): return a / (np.linalg.norm(a) or 1)
def pnormal(Q): return unit(sum(np.cross(Q[i], Q[(i + 1) % len(Q)]) for i in range(len(Q))))
def clean(Q):
    out = []
    for q in Q:
        if not out or np.linalg.norm(q - out[-1]) > 1e-12: out.append(q)
    while len(out) > 1 and np.linalg.norm(out[0] - out[-1]) <= 1e-12: out.pop()
    return np.array(out)
def shrink(Q, h):
    n = pnormal(Q); out = [q.copy() for q in Q]
    for e in range(len(Q)):
        p_, q_ = Q[e], Q[(e + 1) % len(Q)]; ed = q_ - p_
        if np.linalg.norm(ed) < 1e-12: continue
        m = unit(np.cross(n, ed)); off = m @ p_ + h; res = []
        for i in range(len(out)):
            a, b = out[i], out[(i + 1) % len(out)]; fa, fb = m @ a - off, m @ b - off
            if fa >= 0: res.append(a)
            if (fa >= 0) != (fb >= 0): t = fa / (fa - fb); res.append(a + t * (b - a))
        out = res
        if not out: break
    return clean(out) if len(out) >= 3 else np.array([Q.mean(0)])
def loft(F, k, h):
    polys = [clean(P[fc[k]]) for P, fc, labs, A_ in F]
    if h > 0: polys = [shrink(Q, h) for Q in polys]
    Pts, T, ids = [], [], []
    for Q in polys: ids.append(list(range(len(Pts), len(Pts) + len(Q)))); Pts += list(Q)
    a0, aN = ids[0], ids[-1]
    for t in range(1, len(a0) - 1): T.append([a0[0], a0[t + 1], a0[t]])
    for t in range(1, len(aN) - 1): T.append([aN[0], aN[t], aN[t + 1]])
    for f in range(len(polys) - 1):
        A, B, ia, ib = polys[f], polys[f + 1], ids[f], ids[f + 1]
        nc = unit((pnormal(A) if len(A) > 2 else 0) + (pnormal(B) if len(B) > 2 else 0))
        u = unit(np.cross(nc, [1, 0, 0]) if abs(nc[0]) < 0.9 else np.cross(nc, [0, 1, 0])); w = np.cross(nc, u)
        def ang(Q, i): e = Q[(i + 1) % len(Q)] - Q[i]; m = np.cross(e, nc); return np.arctan2(m @ w, m @ u)
        frm = lambda x: ((x - np.pi) % (2 * np.pi) + 2 * np.pi) % (2 * np.pi)
        sa, sb = int(np.argmin(A @ u + 1e-9 * (A @ w))), int(np.argmin(B @ u + 1e-9 * (B @ w)))
        na, nb = (len(A) if len(A) > 1 else 0), (len(B) if len(B) > 1 else 0); x = y = 0
        while x < na or y < nb:
            ca, cb = ia[(sa + x) % len(A)], ib[(sb + y) % len(B)]
            if y >= nb or (x < na and frm(ang(A, (sa + x) % na)) <= frm(ang(B, (sb + y) % nb))):
                T.append([ca, ia[(sa + x + 1) % len(A)], cb]); x += 1
            else:
                T.append([ca, ib[(sb + y + 1) % len(B)], cb]); y += 1
    return np.array(Pts), np.array(T)
