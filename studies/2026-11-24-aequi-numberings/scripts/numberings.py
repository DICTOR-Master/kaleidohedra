"""Four face numberings of each of the 1232 Aequi (24 Nov 2026), plus each die's name.

Face order = the Aequi picker's: the planes of the die's orbits in the order of die.o, each orbit's directions in the group's
listed order; every plane is a face (checked), so face index i = plane i.

Face lattice.  Directions exact in Q(phi)^3 (classify.py of study 2026-11-24-aequi-vacuus-scutoids), depths the 60-digit fair depths
of the search records (studies 2026-11-19-aequi-complete, 2026-11-20-aequi-two-placements), matched to the app depths as there.
Candidate vertices are found in float64; each is then recomputed at 70 digits from three of its planes: every incident plane must pass
through it (residual < 1e-45) and every other plane must clear it by a slack recorded per die (minimum over the die, must be > 1e-12).
Then: F = N, V = corners, side counts = catalogue, every edge on exactly two faces, V - E + F = 2.

Schemes (face index -> number 1..N):
 plain     i -> i + 1.
 opposite  only for centrally symmetric dice (classification CSV, exact): faces paired by exactly opposite directions; the k-th pair
           in app order (by its lower face index) gets k on its lower face and N + 1 - k on the other.
 balanced  CP-SAT: stage 1 minimise (max - min) of the corner sums (sum of the numbers on the faces at each corner); stage 2, with the
           corner spread held at the stage-1 value, minimise (max - min) of the neighbour sums (sum of the numbers on the faces
           sharing an edge with each face).  Status per stage: OPTIMAL (proved) or FEASIBLE with the solver's lower bound.
 spin_down consecutive numbers on adjacent faces: Hamiltonian cycle of the face-adjacency graph (CP-SAT AddCircuit); if none is
           proved absent, a Hamiltonian path.  Cycle: 1 on face 0, 2 on its lower-index cycle neighbour.  Path: 1 at the end with the
           lower face index.
Solver runs are deterministic (fixed seed, interleaved search, deterministic time limits).
Usage: python numberings.py OUTDIR [first last] [--procs P]"""
import csv, json, os, sys, time, itertools
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
SIB = os.path.join(STUDY, "../2026-11-24-aequi-vacuus-scutoids")
sys.path.insert(0, os.path.join(SIB, "scripts"))
import classify as C
mp.mp.dps = 70

T1 = float(os.environ.get("T1", 60)); T2 = float(os.environ.get("T2", 30)); T3 = float(os.environ.get("T3", 30))
WORKERS = int(os.environ.get("WORKERS", 4)); ITERS = int(os.environ.get("ITERS", 200000))

# ---------------- names (proposal for DICTO)
READ = {0: ["o", "re", "maru"], 1: ["i", "hi"], 2: ["ni", "fu"], 3: ["mi", "sa"], 4: ["yo", "shi"], 5: ["go", "ko"],
        6: ["mu", "ro"], 7: ["na"], 8: ["ya", "ha"], 9: ["ku"]}
def name_of(n):
    """digit by digit: the first reading, but the next reading in the digit's list when the first would repeat the syllable just
    before it (7 has one reading only, so 'na na' stays)."""
    out = []
    for ch in str(n):
        rs = READ[int(ch)]; s = rs[0]
        if out and s == out[-1] and len(rs) > 1: s = rs[1]
        out.append(s)
    w = "".join(out); return w[0].upper() + w[1:]
def decode_all(word):
    """every digit string whose syllables spell `word` (any reading), by exhaustive parsing."""
    w = word.lower(); SYL = {s: d for d, rs in READ.items() for s in rs}; res = []
    def go(i, acc):
        if i == len(w): res.append(acc); return
        for s, d in SYL.items():
            if w.startswith(s, i): go(i + len(s), acc + str(d))
    go(0, ""); return res

# ---------------- data
D = json.load(open(os.path.join(STUDY, "src/dice.json")))
ED = C.exact_dirs(D["dirs"]); U = [v for v, f in ED]
ROWS = {int(r["n"]): r for r in csv.DictReader(open(os.path.join(SIB, "data/aequi_classification.csv")))}
def qf(q): return mp.mpf(q.a.numerator) / q.a.denominator + mp.mpf(q.b.numerator) / q.b.denominator * mp.sqrt(5)

def lattice(n):
    e = D["dice"][n - 1]; row = ROWS[n]
    rec = json.load(open(os.path.join(STUDY, "..", "2026-11-19-aequi-complete" if e["s"] == "A" else "2026-11-20-aequi-two-placements", "data/dice", row["record"])))
    d60 = [mp.mpf(x) for x in rec["depths_60_digits"]]
    dep = []
    for x in e["d"]:
        j = [t for t in range(len(d60)) if abs(d60[t] - x) < 1e-9 and t not in dep]
        dep.append(j[0] if len(j) == 1 else len(dep))
    dirs, Dm = [], []
    for k, oi in enumerate(e["o"]):
        for i in D["groups"][e["g"]][oi]["dirs"]:
            dirs.append(i); Dm.append(d60[dep[k]])
    N = len(dirs)
    nm = []
    for i in dirs:
        u = [qf(c) for c in U[i]]; L = mp.sqrt(sum(c * c for c in u)); nm.append([c / L for c in u])
    nf = np.array([[float(c) for c in v] for v in nm]); df = np.array([float(x) for x in Dm])
    # float candidates
    cand = {}
    for a, b, c in itertools.combinations(range(N), 3):
        A = nf[[a, b, c]]
        if abs(np.linalg.det(A)) < 1e-9: continue
        x = np.linalg.solve(A, df[[a, b, c]])
        s = nf @ x - df
        if s.max() > 1e-8: continue
        key = frozenset(np.nonzero(np.abs(s) < 1e-7)[0].tolist())
        cand.setdefault(key, (a, b, c))
    keys = list(cand)
    # 70-digit certification
    minslack = mp.mpf(10); maxres = mp.mpf(0); verts = []
    for key in keys:
        a, b, c = cand[key]
        A = mp.matrix([nm[a], nm[b], nm[c]]); x = mp.lu_solve(A, mp.matrix([Dm[a], Dm[b], Dm[c]]))
        for q in range(N):
            r = sum(nm[q][t] * x[t] for t in range(3)) - Dm[q]
            if q in key: maxres = max(maxres, abs(r))
            else: minslack = min(minslack, -r)
        verts.append(sorted(key))
    assert maxres < mp.mpf("1e-45") and minslack > mp.mpf("1e-12"), (n, maxres, minslack)
    assert len(set(map(tuple, verts))) == len(verts)
    # faces: cyclic vertex order (float)
    vx = [np.linalg.solve(nf[list(cand[k])], df[list(cand[k])]) for k in keys]
    faces = []
    for p in range(N):
        on = [v for v in range(len(verts)) if p in verts[v]]
        cpt = np.mean([vx[v] for v in on], axis=0); u0 = vx[on[0]] - cpt; u0 /= np.linalg.norm(u0); w0 = np.cross(nf[p], u0)
        on.sort(key=lambda v: np.arctan2((vx[v] - cpt) @ w0, (vx[v] - cpt) @ u0)); faces.append(on)
    # edges: consecutive on a face; each must be on exactly two faces, and those two faces = the planes shared by its ends
    E = {}
    for p, f in enumerate(faces):
        for t in range(len(f)):
            k = tuple(sorted((f[t], f[(t + 1) % len(f)]))); E.setdefault(k, []).append(p)
    assert all(len(v) == 2 for v in E.values()), n
    for (a, b), ps in E.items(): assert sorted(set(verts[a]) & set(verts[b])) == sorted(ps), (n, "edge planes")
    from collections import Counter
    got = sorted(Counter(len(f) for f in faces).items()); want = Counter()
    for s in e["f"]:
        c_, g_ = s.split("×"); want[int(g_.split("-")[0])] += int(c_)
    assert all(len(f) >= 3 for f in faces) and len(faces) == e["N"] and len(verts) == e["c"] and got == sorted(want.items()), n
    assert len(verts) - len(E) + len(faces) == 2, n
    adj = sorted(set(tuple(sorted(ps)) for ps in E.values()))
    # opposite pairs (exact directions)
    opp = None
    if row["centrally_symmetric"] == "True":
        opp = {}
        for i in range(N):
            neg = [-c for c in U[dirs[i]]]
            j = [k for k in range(N) if C.same_ray(neg, U[dirs[k]])]
            assert len(j) == 1 and abs(Dm[i] - Dm[j[0]]) < mp.mpf("1e-50"), (n, "opposite"); opp[i] = j[0]
    return dict(e=e, N=N, dirs=dirs, verts=verts, faces=faces, adj=adj, opp=opp, minslack=float(minslack), maxres=float(maxres))

# ---------------- local search (start point for CP-SAT; seeded, so reproducible)
def anneal(groups, N, iters, seed, start=None, cap=None, groups2=None):
    """swap search: minimise the spread of the group sums (then, if groups2 given with cap, the spread of groups2 with groups' spread <= cap).
    returns the best numbering found."""
    rng = np.random.default_rng(seed)
    def mk(gs):
        M = np.zeros((len(gs), N))
        for r, g in enumerate(gs):
            for f in g: M[r, f] += 1
        return M
    A = mk(groups); A2 = mk(groups2) if groups2 is not None else None
    x = np.array(start, float) if start is not None else rng.permutation(N) + 1.0
    def energy(x):
        s = A @ x; sp = s.max() - s.min()
        if A2 is None: return sp + 1e-3 * s.var(), sp
        t = A2 @ x; sp2 = t.max() - t.min()
        return 1e3 * max(0, sp - cap) + sp2 + 1e-3 * t.var(), (sp, sp2)
    E, key = energy(x); best = (E, x.copy()); T = 2.0
    for it in range(iters):
        f, g = rng.integers(N, size=2)
        if f == g: continue
        x[f], x[g] = x[g], x[f]; E2, k2 = energy(x)
        if E2 <= E or rng.random() < np.exp((E - E2) / T):
            E = E2
            if E < best[0]: best = (E, x.copy())
        else: x[f], x[g] = x[g], x[f]
        T = max(0.02, 2.0 * (1 - it / iters))
    return [int(v) for v in best[1]]

# ---------------- solvers
from ortools.sat.python import cp_model
def params(limit):
    p = cp_model.CpSolver(); s = p.parameters
    s.max_deterministic_time = limit; s.num_workers = WORKERS; s.interleave_search = True; s.random_seed = 0
    s.max_time_in_seconds = 20 * limit   # safety only; the deterministic limit governs
    return p
def st(code): return {cp_model.OPTIMAL: "OPTIMAL", cp_model.FEASIBLE: "FEASIBLE", cp_model.INFEASIBLE: "INFEASIBLE"}.get(code, "UNKNOWN")

def balanced(L):
    N, verts = L["N"], L["verts"]; nb = {i: [] for i in range(N)}
    for a, b in L["adj"]: nb[a].append(b); nb[b].append(a)
    def model(cap_vs):
        m = cp_model.CpModel(); B = [[m.NewBoolVar("") for k in range(N)] for f in range(N)]
        for f in range(N): m.AddExactlyOne(B[f])
        for k in range(N): m.AddExactlyOne(B[f][k] for f in range(N))
        x = [sum((k + 1) * B[f][k] for k in range(N)) for f in range(N)]
        def spread(groups):
            lo_ = min(len(g) for g in groups); hi_ = max(len(g) for g in groups)
            lo = m.NewIntVar(lo_, hi_ * N, ""); hi = m.NewIntVar(lo_, hi_ * N, "")
            for g in groups:
                s = sum(x[f] for f in g); m.Add(s >= lo); m.Add(s <= hi)
            return hi - lo
        sv = spread(verts)
        return m, B, x, sv, spread
    m, B, x, sv, spread = model(None); m.Minimize(sv)
    h = anneal(verts, N, ITERS, seed=0, start=L.get("_opp_num"))
    for f in range(N):
        for k in range(N): m.AddHint(B[f][k], k + 1 == h[f])
    S = params(T1); c1 = S.Solve(m)
    assert c1 in (cp_model.OPTIMAL, cp_model.FEASIBLE), (L["e"].get("num"), st(c1))
    v1 = int(S.ObjectiveValue()); b1 = int(round(S.BestObjectiveBound())); sol1 = [sum((k + 1) for k in range(N) if S.Value(B[f][k])) for f in range(N)]
    # stage 2
    m2, B2, x2, sv2, spread2 = model(None); m2.Add(sv2 <= v1); sf = spread2([nb[f] for f in range(N)]); m2.Minimize(sf)
    h2 = anneal(verts, N, ITERS, seed=1, start=sol1, cap=v1, groups2=[nb[f] for f in range(N)])
    if spread_of(h2, verts) > v1: h2 = sol1
    for f in range(N):
        for k in range(N): m2.AddHint(B2[f][k], k + 1 == h2[f])
    S2 = params(T2); c2 = S2.Solve(m2)
    if c2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [sum((k + 1) for k in range(N) if S2.Value(B2[f][k])) for f in range(N)]
        v2 = int(S2.ObjectiveValue()); b2 = int(round(S2.BestObjectiveBound())); s2 = st(c2)
    else:
        sol = sol1; v2 = None; b2 = None; s2 = "UNKNOWN (stage-1 numbering kept)"
    return dict(numbers=sol, corner_spread=v1, corner_spread_lower_bound=b1, corner_status="OPTIMAL" if c1 == cp_model.OPTIMAL else "FEASIBLE",
                neighbour_spread=spread_of(sol, [nb[f] for f in range(N)]), neighbour_spread_lower_bound=b2 if b2 is not None else 0,
                neighbour_status=s2 if s2 != "OPTIMAL" else "OPTIMAL", det_time=[T1, T2])

def spread_of(num, groups):
    s = [sum(num[f] for f in g) for g in groups]; return max(s) - min(s)

def spin(L):
    N = L["N"]; arcs = []
    def solve(path):
        m = cp_model.CpModel(); lit = {}
        for a, b in L["adj"]:
            lit[(a, b)] = m.NewBoolVar(""); lit[(b, a)] = m.NewBoolVar("")
        A = [(a, b, l) for (a, b), l in lit.items()]
        if path:
            for f in range(N):
                lit[(N, f)] = m.NewBoolVar(""); lit[(f, N)] = m.NewBoolVar(""); A += [(N, f, lit[(N, f)]), (f, N, lit[(f, N)])]
        m.AddCircuit(A); S = params(T3); c = S.Solve(m)
        succ = {a: b for (a, b), l in lit.items() if c in (cp_model.OPTIMAL, cp_model.FEASIBLE) and S.Value(l)}
        return c, succ
    c, succ = solve(False)
    if c in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        nb0 = [succ[0], [a for a, b in succ.items() if b == 0][0]]; nxt = min(nb0)
        order = [0, nxt]
        while len(order) < N:
            a = order[-1]; cands = [b for b in (succ.get(a), [p for p, q in succ.items() if q == a][0]) if b != order[-2]]; order.append(cands[0])
        kind = "cycle"; cyc = "found"
    else:
        cyc = "proved absent" if c == cp_model.INFEASIBLE else "unknown (not found within the limit)"
        c2, succ = solve(True); assert c2 in (cp_model.OPTIMAL, cp_model.FEASIBLE), (L["e"].get("num"), "no path")
        order = []; a = succ[N]
        while a != N: order.append(a); a = succ[a]
        if order[-1] < order[0]: order.reverse()
        kind = "path"
    num = [0] * N
    for k, f in enumerate(order): num[f] = k + 1
    return dict(numbers=num, kind=kind, hamiltonian_cycle=cyc)

def one(n, out):
    try: return one_(n, out)
    except Exception as ex: return n, "DIE FAILED %r" % (ex,)

def one_(n, out):
    fn = os.path.join(out, "%04d.json" % n)
    if os.path.exists(fn): return n, "skip"
    t0 = time.time(); L = lattice(n); e = L["e"]; N = L["N"]
    res = dict(n=n, name=name_of(n), name_shown="%s (no. %d)" % (name_of(n), n), catalogue=e["name"] if e["s"] == "A" else None,
               group=e["g"], group_no=e.get("num"), N=N, corners=len(L["verts"]),
               face_direction=L["dirs"], face_vertices=L["faces"], corner_faces=L["verts"],
               lattice_check=dict(min_slack=L["minslack"], max_residual=L["maxres"]),
               corner_degrees=sorted(set(len(v) for v in L["verts"])))
    sch = {"plain": dict(numbers=list(range(1, N + 1)))}
    if L["opp"]:
        num = [0] * N; k = 0
        for i in range(N):
            j = L["opp"][i]
            if i < j: k += 1; num[i] = k; num[j] = N + 1 - k
        sch["opposite"] = dict(available=True, numbers=num); L["_opp_num"] = num
    else:
        sch["opposite"] = dict(available=False, reason="not centrally symmetric")
    sch["balanced"] = balanced(L)
    sch["spin_down"] = spin(L)
    res["schemes"] = sch; res["seconds"] = round(time.time() - t0, 1)
    json.dump(res, open(fn + ".tmp", "w"), separators=(",", ":")); os.replace(fn + ".tmp", fn)
    return n, "%s N=%d corner %d/%d %s spin %s" % (res["name"], N, sch["balanced"]["corner_spread"], sch["balanced"]["corner_spread_lower_bound"],
                                                  sch["balanced"]["corner_status"], sch["spin_down"]["kind"])

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    a = sys.argv[2:]; procs = 1
    if "--procs" in a: procs = int(a[a.index("--procs") + 1]); a = a[:a.index("--procs")]
    ids = list(range(int(a[0]), int(a[1]) + 1)) if a else list(range(1, len(D["dice"]) + 1))
    ids.sort(key=lambda n: -D["dice"][n - 1]["N"])   # largest first, for even load
    from multiprocessing import Pool
    done = 0
    with Pool(procs) as P:
        for n, msg in P.imap_unordered(lambda_ := None or __import__("functools").partial(one, out=out), ids):
            done += 1; print("PROGRESS %.4f %d/%d no. %d %s" % (done / len(ids), done, len(ids), n, msg), flush=True)
    print("ALL DONE", len(ids))
