#!/usr/bin/env python3
"""Scutoid Frusta: enumerate convex combinatorial types with parallel planar ends, n, m <= NMAX, up to KMAX Y-corners.

Model (see README): cross-section at height t in [0,1] is a convex polygon whose edges have fixed normals and support
numbers linear in t. A Y-corner is an event where one lateral face ends (dies) or starts (is born). Every lateral face
meets an end, so only bottom faces die and only new faces are born. Each event sequence is realised by a small LP
(float, HiGHS) and the rounded rational polyhedron is then checked EXACTLY (Fractions): vertices, simplicity, facets,
face graph, n, m, k; the combinatorial type is a canonical code of the oriented map (mirror and end swap allowed).
"""
import sys, json, math, random, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 2
OUT = sys.argv[3] if len(sys.argv) > 3 else "types.json"


def sequences(m, kmax):
    """event sequences from bottom m-gon; first event normalised to touch face 0 (rotation of the bottom)."""
    res = []

    def rec(active, glob, ev, nxt):
        res.append((list(active), list(glob), list(ev)))
        if len(ev) == kmax:
            return
        L = len(active)
        if L > 3:
            for j in active:
                if j < m and (ev or j == 0):
                    rec([x for x in active if x != j], glob, ev + [("del", j)], nxt)
        for p in range(L):
            a, b = active[p], active[(p + 1) % L]
            if not ev and a != 0:
                continue
            g = list(glob); g.insert(g.index(b) if g.index(b) > 0 else len(g), nxt)
            rec(active[:p + 1] + [nxt] + active[p + 1:], g, ev + [("ins", nxt, a, b)], nxt + 1)

    rec(list(range(m)), list(range(m)), [], m)
    return res


def actives(m, ev):
    act = [list(range(m))]
    for e in ev:
        a = list(act[-1])
        if e[0] == "del":
            a.remove(e[1])
        else:
            a.insert(a.index(e[2]) + 1, e[1])
        act.append(a)
    return act


def meets_twice(m, ev):
    """True if two lateral faces would be adjacent in two separate height ranges (they would share two edges:
    the face graph is then not 3-connected, so by Steinitz no convex polyhedron has it)."""
    act = actives(m, ev); seen = {}
    for e, a in enumerate(act):
        L = len(a)
        for r in range(L):
            pr = frozenset((a[r], a[(r + 1) % L]))
            seen.setdefault(pr, []).append(e)
    return any(v != list(range(v[0], v[-1] + 1)) for v in seen.values())


def gaps_ok(ang, act_list):
    for act in act_list:
        th = sorted(ang[i] for i in act)
        g = [(th[(i + 1) % len(th)] - th[i]) % (2 * math.pi) for i in range(len(th))]
        if max(g) >= math.pi - 0.05:
            return False
    return True


def solve(m, glob, ev, ang):
    N = len(glob)
    nv = {i: np.array([math.cos(ang[i]), math.sin(ang[i])]) for i in glob}
    act = actives(m, ev)
    k = len(ev)
    T = [e / (k + 1) for e in range(k + 2)]  # T[0]=0, event e at T[e+1], T[k+1]=1
    idx = {f: q for q, f in enumerate(glob)}
    NV = 2 * N + 1
    A_ub, b_ub, A_eq, b_eq = [], [], [], []

    def hvec(i, t):
        v = np.zeros(NV); v[idx[i]] = 1 - t; v[N + idx[i]] = t; return v

    def vert(p, q, t):  # 2 x NV linear map giving V(p,q)
        M = np.array([nv[p], nv[q]]); C = np.linalg.inv(M)
        return np.outer(C[:, 0], hvec(p, t)) + np.outer(C[:, 1], hvec(q, t))

    def length(i, p, q, t):
        d = np.array([-nv[i][1], nv[i][0]])
        return d @ (vert(i, q, t) - vert(p, i, t))

    for e in range(k + 1):
        A = sorted(act[e], key=lambda f: ang[f])  # ccw order
        lo, hi = T[e], T[e + 1]
        born = ev[e - 1][1] if e > 0 and ev[e - 1][0] == "ins" else None
        dies = ev[e][1] if e < k and ev[e][0] == "del" else None
        inactive = [f for f in glob if f not in A]
        for t, tag in ((lo, "lo"), ((lo + hi) / 2, "mid"), (hi, "hi")):
            for r, i in enumerate(A):
                p, q = A[r - 1], A[(r + 1) % len(A)]
                L = length(i, p, q, t)
                if (tag == "lo" and i == born) or (tag == "hi" and i == dies):
                    A_eq.append(L); b_eq.append(0.0)
                else:
                    row = -L; row[-1] = 1; A_ub.append(row); b_ub.append(0.0)  # s - L <= 0
            for x in inactive:
                # the face that died at lo / will be born at hi touches its vertex there: skip that endpoint
                skip = (tag == "lo" and e > 0 and ev[e - 1][0] == "del" and ev[e - 1][1] == x) or \
                       (tag == "hi" and e < k and ev[e][0] == "ins" and ev[e][1] == x)
                if skip:
                    continue
                for r in range(len(A)):
                    p, q = A[r], A[(r + 1) % len(A)]
                    row = nv[x] @ vert(p, q, t) - hvec(x, t); row = row.copy(); row[-1] = 1
                    A_ub.append(row); b_ub.append(0.0)
    c = np.zeros(NV); c[-1] = -1
    bounds = [(-10, 10)] * (2 * N) + [(None, 1)]
    r = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq) if A_eq else None,
                b_eq=b_eq if b_eq else None, bounds=bounds, method="highs")
    if r.status != 0 or r.x[-1] <= 1e-6:
        return None
    return r.x, idx


def rat_normal(theta):
    u = Fr(math.tan(theta / 2)).limit_denominator(60) if abs(math.cos(theta / 2)) > 1e-9 else None
    if u is None:
        return (Fr(-1), Fr(0))
    return ((1 - u * u) / (1 + u * u), 2 * u / (1 + u * u))


def det3(a, b, c):
    return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])


def polytope(planes):
    """planes: list of (nx,ny,nz,d) Fractions for nx x+ny y+nz z <= d. Returns (verts, tight sets) exactly or None if not simple."""
    verts = {}
    P = len(planes)
    for a, b, c in itertools.combinations(range(P), 3):
        A = [planes[a][:3], planes[b][:3], planes[c][:3]]
        D = det3(*A)
        if D == 0:
            continue
        d = [planes[a][3], planes[b][3], planes[c][3]]
        x = []
        for col in range(3):
            M = [list(r) for r in A]
            for row in range(3):
                M[row][col] = d[row]
            x.append(det3(*M) / D)
        x = tuple(x)
        if x in verts:
            continue
        ok = True; tight = []
        for i, p in enumerate(planes):
            s = p[0] * x[0] + p[1] * x[1] + p[2] * x[2] - p[3]
            if s > 0:
                ok = False; break
            if s == 0:
                tight.append(i)
        if ok:
            verts[x] = frozenset(tight)
    return verts


def build_map(planes, verts):
    V = list(verts); tight = [verts[v] for v in V]
    if any(len(t) != 3 for t in tight):
        return None, "not simple"
    faces = {}
    for i in range(len(planes)):
        vs = [j for j in range(len(V)) if i in tight[j]]
        if len(vs) < 3:
            return None, f"plane {i} not a facet"
        faces[i] = vs
    adj = {j: set() for j in range(len(V))}
    for a, b in itertools.combinations(range(len(V)), 2):
        if len(tight[a] & tight[b]) == 2:
            adj[a].add(b); adj[b].add(a)
    cyc = {}
    for i, vs in faces.items():
        S = set(vs); start = vs[0]; c = [start]; prev = None; cur = start
        while True:
            nb = [w for w in adj[cur] if w in S and i in (tight[cur] & tight[w]) and w != prev]
            nxt = nb[0] if prev is not None or True else None
            if prev is None:
                nxt = sorted(nb)[0]
            if nxt == start:
                break
            c.append(nxt); prev, cur = cur, nxt
            if len(c) > len(vs):
                return None, "face walk failed"
        if len(c) != len(vs):
            return None, "face walk short"
        n = planes[i][:3]
        p0, p1, p2 = V[c[0]], V[c[1]], V[c[2]]
        u = [p1[q] - p0[q] for q in range(3)]; w = [p2[q] - p1[q] for q in range(3)]
        cr = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        if sum(cr[q] * n[q] for q in range(3)) < 0:
            c = c[::-1]
        cyc[i] = c
    nxt = {j: {} for j in range(len(V))}
    for i, c in cyc.items():
        L = len(c)
        for r in range(L):
            u, v, w = c[r - 1], c[r], c[(r + 1) % L]
            nxt[v][w] = u
    for j in nxt:
        if len(nxt[j]) != 3:
            return None, "rotation"
    return dict(V=V, tight=tight, faces=cyc, adj=adj, nxt=nxt), None


def canon(mp, endmark, mirror=True):
    nxt = mp["nxt"]
    prv = {v: {b: a for a, b in d.items()} for v, d in nxt.items()}
    best = None
    for v0 in nxt:
        for v1 in nxt[v0]:
            for rot in ((nxt, prv) if mirror else (nxt,)):
                lab = {v0: 0}; order = [v0]; first = {v0: v1}; code = []; i = 0
                while i < len(order):
                    v = order[i]; u = first[v]
                    for _ in range(3):
                        if u not in lab:
                            lab[u] = len(order); order.append(u); first[u] = v
                        code.append((lab[u], endmark(v, u)))
                        u = rot[v][u]
                    i += 1
                code = tuple(code)
                if best is None or code < best:
                    best = code
    return best


def analyse(planes, mp):
    tight = mp["tight"]; B, T = 0, 1
    m = len(mp["faces"][B]); n = len(mp["faces"][T])
    onB = {j for j in range(len(mp["V"])) if B in tight[j]}; onT = {j for j in range(len(mp["V"])) if T in tight[j]}
    if onB & onT:
        return None
    Y = [j for j in range(len(mp["V"])) if j not in onB and j not in onT]
    lat_ok = all((set(c) & (onB | onT)) for i, c in mp["faces"].items() if i > 1)

    def em_swap(v, u):
        return 1 if ((v in onB and u in onB) or (v in onT and u in onT)) else 0

    def em_ord(v, u):
        return 1 if (v in onB and u in onB) else (2 if (v in onT and u in onT) else 0)
    return dict(n=n, m=m, k=len(Y), lateral_faces=len(mp["faces"]) - 2, every_lateral_meets_end=lat_ok,
                code=canon(mp, em_swap), code_nomirror=canon(mp, em_swap, mirror=False))


def realise(m, glob, ev, tries=40, seed=1):
    act = actives(m, ev)
    N = len(glob); rnd = random.Random(seed * 1000 + m)
    for t in range(tries):
        if t == 0:
            ang = {f: 2 * math.pi * q / N for q, f in enumerate(glob)}
        else:
            th = sorted(rnd.uniform(0, 2 * math.pi) for _ in range(N))
            ang = {f: th[q] for q, f in enumerate(glob)}
        if not gaps_ok(ang, act):
            continue
        # snap the angles to exact rational normals (and use the snapped angles in the LP)
        nr = {f: rat_normal(ang[f]) for f in glob}
        ang = {f: math.atan2(float(nr[f][1]), float(nr[f][0])) % (2 * math.pi) for f in glob}
        if not gaps_ok(ang, act):
            continue
        sol = solve(m, glob, ev, ang)
        if sol is None:
            continue
        x, idx = sol
        planes = [(Fr(0), Fr(0), Fr(-1), Fr(0)), (Fr(0), Fr(0), Fr(1), Fr(1))]
        order = list(glob)
        for f in order:
            a = Fr(x[idx[f]]).limit_denominator(10 ** 4); b = Fr(x[N + idx[f]]).limit_denominator(10 ** 4)
            planes.append((nr[f][0], nr[f][1], a - b, a))
        verts = polytope(planes)
        mp, why = build_map(planes, verts)
        if mp is None:
            continue
        an = analyse(planes, mp)
        if an is None or an["m"] != m or an["n"] != len(act[-1]) or an["k"] != len(ev) or not an["every_lateral_meets_end"]:
            continue
        return planes, mp, an
    return None


def main():
    types = {}; fails = []; excluded = []; nseq = 0
    for m in range(3, NMAX + 1):
        for active, glob, ev in sequences(m, KMAX):
            n = len(actives(m, ev)[-1])
            if not (3 <= n <= NMAX and m <= NMAX):
                continue
            nseq += 1
            if meets_twice(m, ev):
                excluded.append(dict(m=m, ev=ev)); continue
            r = realise(m, glob, ev)
            if r is None:
                fails.append(dict(m=m, ev=ev)); print("FAIL", m, ev, flush=True); continue
            planes, mp, an = r
            key = json.dumps(an["code"])
            if key not in types:
                chiral = an["code"] != an["code_nomirror"] or None
                # chirality: mirror image has a different orientation-preserving code
                mpm = dict(mp); mpm["nxt"] = {v: {b: a for a, b in d.items()} for v, d in mp["nxt"].items()}
                onB = {j for j in range(len(mp["V"])) if 0 in mp["tight"][j]}; onT = {j for j in range(len(mp["V"])) if 1 in mp["tight"][j]}
                em = lambda v, u: 1 if ((v in onB and u in onB) or (v in onT and u in onT)) else 0
                chiral = canon(mp, em, mirror=False) != canon(mpm, em, mirror=False)
                lo, hi = sorted((an["n"], an["m"]))
                types[key] = dict(code=an["code"], code_no_ends=canon(mp, lambda v, u: 0), small_end=lo, large_end=hi, k=an["k"], chiral=chiral, bottom=m, top=an["n"], events=ev,
                                  lateral_faces=an["lateral_faces"], vertices=len(mp["V"]),
                                  planes=[[str(c) for c in p] for p in planes],
                                  faces={str(i): c for i, c in mp["faces"].items()},
                                  verts=[[str(c) for c in v] for v in mp["V"]])
        print(f"PROGRESS {m / NMAX:.2f} bottom m={m} types so far {len(types)}", flush=True)
    counts = {}
    for t in types.values():
        kk = f"{t['small_end']},{t['large_end']},{t['k']}"
        c = counts.setdefault(kk, [0, 0]); c[0] += 1; c[1] += 2 if t["chiral"] else 1
    json.dump(dict(NMAX=NMAX, KMAX=KMAX, sequences=nseq, fails=fails, excluded_two_shared_edges=excluded, counts=counts, types=list(types.values())),
              open(OUT, "w"), indent=0)
    print("sequences", nseq, "excluded (two faces share two edges)", len(excluded), "types", len(types), "fails", len(fails))
    for kk in sorted(counts, key=lambda s: tuple(map(int, s.split(",")))):
        print("n,m,k =", kk, " types (mirror pairs as one):", counts[kk][0], " counting both hands:", counts[kk][1])
    print("FINAL ok" if not fails else "FINAL with failures")


if __name__ == "__main__":
    main()
