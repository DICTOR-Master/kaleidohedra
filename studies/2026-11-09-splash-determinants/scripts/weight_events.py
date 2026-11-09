# Splash determinants, part W (DICTO proposed reading the splash patterns for coverage: the areas where local rules suffice for now).
# Weight sliders (paraboloid quadric, power diagrams). For every STOP of an exact weight walk (both range ends and every interior
# stop), look for a local rule: a circuit Z of d+2 sites (d+1 affinely independent) whose lifted determinant
#     D(theta) = c * (S0 - sum_q theta_q S_q),  S0 = sum alpha_i (|p_i|^2 - w0_i),  S_q = sum alpha_i * dw_i/dtheta_q
# vanishes at the stop, is not identically zero, and whose power sphere at the stop is EMPTY (closed: no site of smaller power).
# Theorem A of the switch-theorem study says every interior flip has such a witness; here the claim is tested on every stop,
# range ends included, on more walks (pyrochlore #60, the #57 hole walk at several layer spacings, the perovskite chamber walls).
# Floats only choose candidates; every witness is decided in Fractions.
# Usage: python weight_events.py <group>   groups: relay | pyro | sfam | perov | sfam_predict
import json, os, sys, time, io, contextlib
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RELAY = os.path.join(ROOT, "2026-10-25-relay-census")
SWITCH = os.path.join(ROOT, "2026-11-08-switch-theorem")
sys.path.insert(0, os.path.join(RELAY, "scripts")); sys.path.insert(0, os.path.join(SWITCH, "scripts"))
from engine import Net, gdot, vsub, solve  # noqa: E402
from networks import NETS  # noqa: E402
import census  # noqa: E402
import extra_nets  # noqa: E402,F401
from circuits import exact_alpha  # noqa: E402
DATA = os.path.join(HERE, "..", "data"); WALKS = os.path.join(DATA, "walks"); os.makedirs(WALKS, exist_ok=True)

POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}


def holes_net(word, s):   # #57 hole walk (Splash Rules run 1 net), layer spacing d^2 = s * 2/3
    n = len(word); motif = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        z = lambda f: Fr(k, n) + f / n
        motif += [('oct', (*POS[Z], z(Fr(1, 2)))), ('tet', (*POS[X], z(Fr(3, 4)))), ('tet', (*POS[Y], z(Fr(1, 4))))]
    G = [[1, Fr(1, 2), 0], [Fr(1, 2), 1, 0], [0, 0, s * Fr(2, 3) * n * n]]
    return dict(name=f"#57 holes {word}, d^2 = {s}*2/3", G=G, T=[(1, 0, 0), (0, 1, 0), (0, 0, 1)], motif=motif,
                w={"tet": (0, 1), "oct": (0, 0)}, A="tet", B="oct", D2=12, units="ball spacing 1", expect=[], s=s, nlay=n)


def pyro_net(word):       # #60 pyrochlore walk (pyro_walk.py net)
    n = len(word); motif = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        z = lambda f: Fr(k, n) + f / n
        motif += [('atom', (*POS[X], z(Fr(0)))), ('atom', (*POS[X], z(Fr(3, 4)))), ('hole', (*POS[Z], z(Fr(1, 2)))), ('hole', (*POS[Y], z(Fr(1, 4))))]
    G = [[1, Fr(1, 2), 0], [Fr(1, 2), 1, 0], [0, 0, Fr(2, 3) * n * n]]
    return dict(name=f"#60 pyrochlore {word}", G=G, T=[(1, 0, 0), (0, 1, 0), (0, 0, 1)], motif=motif,
                w={"atom": (0, 1), "hole": (0, 0)}, A="atom", B="hole", D2=12, units="ball spacing 1", expect=[])


def get_walk(key):
    for p in (os.path.join(RELAY, "data", "raw", key + ".json"), os.path.join(SWITCH, "data", key + "-walk.json"),
              os.path.join(WALKS, key + ".json")):
        if os.path.exists(p):
            return json.load(open(p))
    census.NETS[key] = NETS[key]
    cwd = os.getcwd(); os.chdir(os.path.join(RELAY, "scripts"))
    with contextlib.redirect_stdout(io.StringIO()):
        C = census.Census(key); d = C.walk()
    os.chdir(cwd)
    fails = [c for c in C.checks if c[0] != 'PASS']
    d['_census_fails'] = len(fails)
    json.dump(d, open(os.path.join(WALKS, key + ".json"), "w"), indent=0, default=str)
    return d


def walk_stops(d):
    ivs = d["intervals"]
    st = [(Fr(ivs[0]["lo"]), "range end (low)")]
    st += [(Fr(iv["lo"]), "interior") for iv in ivs[1:]]
    st += [(Fr(ivs[-1]["hi"]), "range end (high)")]
    rho = max(s.get("rho", 0) for iv in ivs for s in iv["sites"])
    return st, rho


def enumerate_circuits(net, Dp2):
    """All (d+2)-sets with lexicographically smallest site in the motif and pairwise G-distance^2 <= Dp2 (float arrays)."""
    d = net.d; Gf = np.array([[float(x) for x in r] for r in net.G]); out = []
    m = net.m
    for i, (ki, ci) in enumerate(net.motif):
        near = [(j, kv, c) for j, kv, c in net.sites_near(i, Dp2) if tuple(c) > tuple(ci)]
        if len(near) < d + 1: continue
        Xn = np.array([[float(x) for x in c] for _, _, c in near])
        diff = Xn[:, None, :] - Xn[None, :, :]
        adj = np.einsum("abi,ij,abj->ab", diff, Gf, diff) <= float(Dp2) + 1e-9
        combos = []

        def grow(cur, cand):
            if len(cur) == d + 1:
                combos.append(tuple(cur)); return
            for t, v in enumerate(cand):
                grow(cur + [v], [u for u in cand[t + 1:] if adj[v, u]])
        grow([], list(range(len(near))))
        if not combos: continue
        C = np.array(combos)
        x0 = np.array([float(x) for x in ci])
        P = np.concatenate([np.broadcast_to(x0, (len(C), 1, d)), Xn[C]], axis=1)
        M = np.concatenate([P.transpose(0, 2, 1), np.ones((len(C), 1, d + 2))], axis=1)
        alpha = np.stack([(-1) ** q * np.linalg.det(np.delete(M, q, axis=2)) for q in range(d + 2)], axis=1)
        W = np.zeros((len(C), d + 2, m + 1))
        W[:, 0, :] = [float(x) for x in net.wc[ki]]
        wcn = np.array([[float(x) for x in net.wc[net.motif[near[q][0]][0]]] for q in range(len(near))])
        W[:, 1:, :] = wcn[C]
        sq = np.einsum("kpi,ij,kpj->kp", P, Gf, P)
        S0 = (alpha * (sq - W[:, :, 0])).sum(1)
        Sq = np.stack([(alpha * W[:, :, 1 + q]).sum(1) for q in range(m)], axis=1)
        scale = np.abs(alpha).sum(1)
        out.append(dict(i=i, near=near, C=C, P=P, S0=S0, Sq=Sq, scale=scale, W=W, sq=sq))
    return out


def exact_witness(net, pts, theta):
    """Exact test of one candidate (d+2 sites) at the parameter point theta: D(theta) = 0, D not identically 0, closed empty
    power sphere. Returns the witness record or None."""
    d = net.d
    Pq = [c for _, _, c in pts]; kinds = [net.motif[j][0] for j, _, _ in pts]
    al = exact_alpha(Pq)
    if all(a == 0 for a in al): return None
    wc = [net.wc[k] for k in kinds]
    S0 = sum(a * (gdot(net.G, p, p) - w[0]) for a, p, w in zip(al, Pq, wc))
    Sq = [sum(a * w[1 + q] for a, w in zip(al, wc)) for q in range(net.m)]
    if all(x == 0 for x in Sq): return None          # constant determinant: not an event factor
    if S0 - sum(t * x for t, x in zip(theta, Sq)) != 0: return None
    w = [w[0] + sum(t * w[1 + q] for q, t in enumerate(theta)) for w in wc]
    sol = None
    for sub in combinations(range(d + 2), d + 1):
        p0 = Pq[sub[0]]
        Am = [[2 * x for x in [sum(net.G[r][s] * (Pq[q][s] - p0[s]) for s in range(d)) for r in range(d)]] for q in sub[1:]]
        bm = [[(gdot(net.G, Pq[q], Pq[q]) - w[q]) - (gdot(net.G, p0, p0) - w[sub[0]])] for q in sub[1:]]
        X = solve(Am, bm)
        if X is not None:
            sol = tuple(X[r][0] for r in range(d)); break
    if sol is None: return None
    pi = gdot(net.G, vsub(sol, Pq[0]), vsub(sol, Pq[0])) - w[0]
    assert all(gdot(net.G, vsub(sol, q), vsub(sol, q)) - wq == pi for q, wq in zip(Pq, w))
    return dict(kinds=kinds, coords=[[str(x) for x in p] for p in Pq], alpha=[str(a) for a in al], S0=str(S0),
                S=[str(x) for x in Sq], vertex=sol, power=pi)


def empty_sphere(net, i, sol, pi, theta, R2):
    cloud = net.sites_near(i, R2) + [(i, (0,) * net.d, net.motif[i][1])]
    on = 0
    for j, _, c in cloud:
        k = net.motif[j][0]; wj = net.wc[k][0] + sum(t * net.wc[k][1 + q] for q, t in enumerate(theta))
        pw = gdot(net.G, vsub(sol, c), vsub(sol, c)) - wj
        if pw < pi: return False, 0
        on += pw == pi
    return True, on


def witness_at(net, circ, theta, Rcl2, maxtry=int(os.environ.get("MAXTRY", "400"))):
    """Search a witness at the parameter point theta among the enumerated circuits (floats pick, Fractions decide)."""
    th = np.array([float(t) for t in theta])
    tried = 0
    for blk in circ:
        D = blk["S0"] - blk["Sq"] @ th
        nz = np.abs(blk["Sq"]).sum(1) > 1e-9 * blk["scale"]
        sel = np.where((np.abs(D) < 1e-8 * np.maximum(blk["scale"], 1)) & nz & (blk["scale"] > 1e-9))[0]
        if len(sel) and "cloud" not in blk:
            cl = net.sites_near(blk["i"], Rcl2) + [(blk["i"], (0,) * net.d, net.motif[blk["i"]][1])]
            blk["cloud"] = (np.array([[float(x) for x in c] for _, _, c in cl]),
                            np.array([[float(x) for x in net.wc[net.motif[j][0]]] for j, _, _ in cl]))
        Gf = np.array([[float(x) for x in r] for r in net.G])
        for k in sel:
            # float pre-filter: power vertex and empty sphere (Fractions decide afterwards)
            Pk = blk["P"][k]; wk = blk["W"][k][:, 0] + blk["W"][k][:, 1:] @ th
            sq = blk["sq"][k]
            Aq = 2 * (Pk[1:] - Pk[0]) @ Gf; bq = (sq[1:] - wk[1:]) - (sq[0] - wk[0])
            cvx, *_ = np.linalg.lstsq(Aq, bq, rcond=None)
            pi_f = (cvx - Pk[0]) @ Gf @ (cvx - Pk[0]) - wk[0]
            Xc, Wc = blk["cloud"]; dv = Xc - cvx
            pw = np.einsum("ai,ij,aj->a", dv, Gf, dv) - (Wc[:, 0] + Wc[:, 1:] @ th)
            if pw.min() - pi_f < -1e-7: continue
            pts = [(blk["i"], (0,) * net.d, net.motif[blk["i"]][1])] + [blk["near"][q] for q in blk["C"][k]]
            wit = exact_witness(net, pts, theta)
            tried += 1
            if wit is None: continue
            ok, on = empty_sphere(net, blk["i"], wit["vertex"], wit["power"], theta, Rcl2)
            if ok:
                wit["cell_sites"] = on; wit["vertex"] = [str(x) for x in wit["vertex"]]; wit["power"] = str(wit["power"])
                return wit, tried
            if tried > maxtry: return None, tried
    return None, tried


def run_net(key, spec=None, extra=None):
    if spec is not None: NETS[key] = spec
    spec = NETS[key]; t0 = time.time()
    d = get_walk(key)
    net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"])
    stops, rho = walk_stops(d)
    Dp2 = Fr((2 * rho * 1.001) ** 2).limit_denominator(1000) + Fr(1, 100)
    span = max(abs(s[0]) for s in stops)
    Rcl = 2 * rho + np.sqrt(rho ** 2 + 2 * float(span)) + 1.0
    circ = enumerate_circuits(net, Dp2)
    res = []
    for lam, typ in stops:
        wit, tried = witness_at(net, circ, (lam,), Fr(Rcl ** 2).limit_denominator(100))
        res.append(dict(value=str(lam), where=typ, covered=wit is not None, witness=wit, tried=tried))
        print(f"  {key}: stop {lam} ({typ}): " + (f"WITNESS {''.join(k[0] for k in wit['kinds'])} S0 = {wit['S0']} SA = {wit['S'][0]}"
              f" root {Fr(wit['S0']) / Fr(wit['S'][0])}, dual cell {wit['cell_sites']} sites" if wit else f"no witness ({tried} tried)"), flush=True)
    out = dict(key=key, name=spec["name"], census_fails=d.get("_census_fails", 0), rho=rho, stops=res, seconds=round(time.time() - t0, 1))
    if extra: out.update(extra)
    return out


def run_perov():
    """Two weights: each wall or boundary line of #53's perovskite chamber map, tested at the midpoint of each of its segments."""
    spec = dict(name="perovskite ABX3", G=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
                motif=[("A", (0, 0, 0)), ("B", (1, 1, 1)), ("X", (1, 1, 0)), ("X", (1, 0, 1)), ("X", (0, 1, 1))],
                w={"A": (0, 1, 0), "B": (0, 0, 1), "X": (0, 0, 0)})
    net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"], m=2)
    raw = json.load(open(os.path.join(RELAY, "data", "raw", "perovskite.json")))
    segs = {}
    for ch in raw["chambers"]:
        V = [tuple(Fr(x) for x in v) for v in ch["verts"]]
        for a, b in zip(V, V[1:] + V[:1]):
            segs[tuple(sorted((a, b)))] = 1
    circ = enumerate_circuits(net, Fr(9))
    res = []
    for (a, b) in sorted(segs):
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        # line through a, b: c0 + c1 lam + c2 mu = 0
        c1, c2 = b[1] - a[1], a[0] - b[0]; c0 = -(c1 * a[0] + c2 * a[1])
        wit, tried = witness_at(net, circ, mid, Fr(60), maxtry=4000)
        same = False
        if wit:
            S0, SA, SB = Fr(wit["S0"]), Fr(wit["S"][0]), Fr(wit["S"][1])
            # D = S0 - lam SA - mu SB must be proportional to c0 + c1 lam + c2 mu
            same = S0 * c1 == -SA * c0 and S0 * c2 == -SB * c0 and SA * c2 == SB * c1
        res.append(dict(segment=[[str(x) for x in a], [str(x) for x in b]], line=[str(c0), str(c1), str(c2)], midpoint=[str(x) for x in mid],
                        covered=bool(wit) and same, witness=wit, tried=tried))
        print(f"  perovskite segment {a}-{b} line {c0} + {c1} lam + {c2} mu: " +
              (f"WITNESS {''.join(k for k in wit['kinds'])} S0 {wit['S0']} SA {wit['S'][0]} SB {wit['S'][1]} same line {same}" if wit else "none"), flush=True)
    return dict(key="perovskite", segments=res)


if __name__ == "__main__":
    group = sys.argv[1]
    out = {}
    if group == "relay":
        keys = sys.argv[2:] or ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15", "hbn", "sodalite"]
        for k in keys: out[k] = run_net(k)
        if sys.argv[2:]: group = "relay-" + "-".join(sys.argv[2:])
    elif group == "pyro":
        for w in ["ABC", "AC", "ACBC"]: out["py_" + w] = run_net("py_" + w, pyro_net(w))
    elif group in ("sfam", "sfam_predict", "pilot"):
        S = {"sfam": ["1/2", "3/4", "1", "3/2", "2"], "sfam_predict": ["5/8", "5/4"], "pilot": ["1"]}[group]
        words = ["ABC", "AC"]
        if sys.argv[2:]: S = [sys.argv[2]]; group = group + "-" + sys.argv[2].replace("/", "o")
        for s in S:
            for w in words:
                k = f"h57_{w}_{s.replace('/', 'o')}"
                out[k] = run_net(k, holes_net(w, Fr(s)), extra=dict(word=w, s=s))
    elif group == "perov":
        out["perovskite"] = run_perov()
    json.dump(out, open(os.path.join(DATA, f"weight-{group}.json"), "w"), indent=1, default=str)
    if group == "perov":
        segs = out["perovskite"]["segments"]; n = len(segs); c = sum(s["covered"] for s in segs)
    else:
        n = sum(len(v["stops"]) for v in out.values()); c = sum(s["covered"] for v in out.values() for s in v["stops"])
        cf = sum(v["census_fails"] for v in out.values())
        print(f"census check failures in new walks: {cf}")
    print(f"{group}: {c}/{n} events with a single-circuit witness")
    ok = n > 0 and (group == "perov" or cf == 0)
    if group.startswith("relay"):   # regression: Theorem A (switch-theorem study) says every interior flip has a witness
        ok = ok and all(s["covered"] for v in out.values() for s in v["stops"] if s["where"] == "interior")
    print('FINAL ok' if ok else f'FINAL FAIL: n={n}')
