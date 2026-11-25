"""Exhaustive decision of the combinatorial Sri Yantra in every shadow that passes the pencil test (shadows.py), by SAT
(CaDiCaL 1.5.3 through PySAT; A. Ignatiev, A. Morgado, J. Marques-Silva, SAT 2018; A. Biere, CaDiCaL).
Question per shadow: is there an injective map of the yantra's 27 lines to shadow lines such that each of the 31 yantra triple
points goes to its own drawn shadow point where its three image lines meet (with the interior conditions of yantra_inc.YREQ),
distinct triple points to distinct shadow points, and the 9 bases to one pencil (all parallel, or all through one drawn point)?
Encoding: x[y, l] (yantra line y -> shadow line l), z[t, p] (triple t -> point p), w[c] (pencil c); exactly-one and at-most-one
constraints by sequential counters; z[t, p] -> OR of x[y, l] over the lines l through p with the required status, for each member y.
UNSAT = no such map exists (exhaustive). Reads data/shadows.json, writes data/yantra-sat.json."""
import os, sys, json, time
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from yantra_inc import YTRIPLES, YREQ, NANY, NINT, NAMES
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153


def decide(inc, only_pencil=None):
    nl = len(inc["dir"]); pts = [{int(k): v for k, v in p.items()} for p in inc["points"]]
    through = defaultdict(list)
    for pid, p in enumerate(pts):
        for l in p: through[l].append(pid)
    nany = [len(through[l]) for l in range(nl)]
    nint = [sum(1 for pid in through[l] if pts[pid][l] == "int") for l in range(nl)]
    pencils = []
    bydir = defaultdict(list)
    for l, d in enumerate(inc["dir"]): bydir[d].append(l)
    pencils += [set(ls) for ls in bydir.values() if len(ls) >= 9]
    pencils += [set(p) for p in pts if len(p) >= 9]
    npen = len(pencils)
    if only_pencil is not None:
        if only_pencil >= npen: return {"sat": None, "why": "no such pencil", "pencils": npen}
        pencils = [pencils[only_pencil]]
    inpen = set().union(*pencils) if pencils else set()
    dom = {y: [l for l in range(nl) if nany[l] >= NANY[y] and nint[l] >= NINT[y] and (y >= 9 or l in inpen)] for y in range(27)}
    if not pencils or any(not dom[y] for y in range(27)):
        return {"sat": False, "why": "static domains empty"}
    pool = IDPool(); cnf = CNF()
    X = lambda y, l: pool.id(("x", y, l)); Z = lambda t, p: pool.id(("z", t, p)); W = lambda c: pool.id(("w", c))
    def exactly_one(lits):
        cnf.extend(CardEnc.equals(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses)
    def at_most_one(lits):
        if len(lits) > 1: cnf.extend(CardEnc.atmost(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses)
    for y in range(27): exactly_one([X(y, l) for l in dom[y]])
    users = defaultdict(list)
    for y in range(27):
        for l in dom[y]: users[l].append(X(y, l))
    for l, lits in users.items(): at_most_one(lits)
    domset = {y: set(dom[y]) for y in range(27)}
    zs = defaultdict(list)
    for t, (tr, rq) in enumerate(zip(YTRIPLES, YREQ)):
        feas = []
        for pid, p in enumerate(pts):
            opts = []
            for y, r in zip(tr, rq):
                o = [l for l, st in p.items() if l in domset[y] and (r is None or st == "int")]
                opts.append(o)
            if all(opts): feas.append((pid, opts))
        if not feas: return {"sat": False, "why": f"triple {t} has no feasible point"}
        exactly_one([Z(t, pid) for pid, _ in feas])
        for pid, opts in feas:
            zs[pid].append(Z(t, pid))
            for y, o in zip(tr, opts):
                cnf.append([-Z(t, pid)] + [X(y, l) for l in o])
    for pid, lits in zs.items(): at_most_one(lits)
    exactly_one([W(c) for c in range(len(pencils))])
    for y in range(9):
        for l in dom[y]:
            cnf.append([-X(y, l)] + [W(c) for c, P in enumerate(pencils) if l in P])
            for c, P in enumerate(pencils):
                if l not in P: cnf.append([-W(c), -X(y, l)])
    with Cadical153(bootstrap_with=cnf.clauses) as s:
        ok = s.solve()
        model = s.get_model() if ok else None
    out = {"sat": bool(ok), "vars": pool.top, "clauses": len(cnf.clauses), "pencils": len(pencils)}
    if ok:
        ms = set(v for v in model if v > 0)
        out["map"] = {NAMES[y]: next(l for l in dom[y] if X(y, l) in ms) for y in range(27)}
    return out


def _worker(inc, q, c=None):
    q.put(decide(inc, c))


def decide_timed(inc, secs, c=None):
    import multiprocessing as mp
    q = mp.Queue(); pr = mp.Process(target=_worker, args=(inc, q, c)); pr.start()
    t0 = time.time()
    while pr.is_alive() and time.time() - t0 < secs:
        pr.join(min(60, secs - (time.time() - t0)))
        if pr.is_alive() and secs > 120: print(f"HEARTBEAT {time.time() - t0:.0f} s solving", flush=True)
    if pr.is_alive():
        pr.terminate(); pr.join()
        return {"sat": None, "why": f"not decided within {secs} s"}
    return q.get()


def per_pencil(src, names, secs, out):
    """split an undecided instance by pencil (exactly one pencil holds the bases, so the instance is the union of these)"""
    D = json.load(open(src)); res = []
    for s in D["shadows"]:
        if not s.get("incidence") or f"{s['polyhedron']} | {s['direction']}" not in names: continue
        n = decide(s["incidence"], 10 ** 9)["pencils"]
        rows = []
        k, m = map(int, os.environ.get("STRIDE", "0/1").split("/"))
        print(f"PROGRESS 0.000 {s['polyhedron']} | {s['direction']}: {n} pencils, stride {k}/{m}", flush=True)
        for c in range(k, n, m):
            r = decide_timed(s["incidence"], secs, c); r["pencil"] = c; rows.append(r)
            print(f"PROGRESS {len(rows) / len(range(k, n, m)):.3f} {s['polyhedron']} | {s['direction']} | pencil {c}: SAT {r['sat']} {r.get('why', '')}", flush=True)
            if r["sat"]: break
        res.append({"polyhedron": s["polyhedron"], "direction": s["direction"], "pencils": n, "unsat": sum(r["sat"] is False for r in rows),
                    "sat": sum(bool(r["sat"]) for r in rows), "undecided": sum(r["sat"] is None for r in rows), "rows": rows})
    json.dump(res, open(out, "w"), indent=1)
    print("FINAL ok per_pencil", flush=True)


if __name__ == "__main__":
    if os.environ.get("PERPENCIL"):
        per_pencil(os.path.join(STUDY, "data/shadows.json"), os.environ["PERPENCIL"].split(";"), int(os.environ.get("SATSECS", "60")),
                   os.path.join(STUDY, "data/yantra-sat-pencils-%s.json" % os.environ.get("STRIDE", "0/1").replace("/", "of"))); sys.exit(0)
    LIMIT = int(os.environ.get("SATSECS", "900"))
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STUDY, "data/shadows.json")
    D = json.load(open(src))
    todo = [s for s in D["shadows"] if s.get("incidence")]
    res = []
    for i, s in enumerate(todo):
        t = time.time()
        r = decide_timed(s["incidence"], LIMIT)
        r.update({"polyhedron": s["polyhedron"], "kind": s["kind"], "direction": s["direction"], "secs": round(time.time() - t, 2)})
        res.append(r)
        print(f"PROGRESS {(i + 1) / len(todo):.3f} {s['polyhedron']} | {s['direction']} | SAT {r['sat']} {r.get('why', '')} ({r['secs']} s)", flush=True)
    json.dump(res, open(os.path.join(STUDY, "data/yantra-sat.json" if len(sys.argv) < 3 else sys.argv[2]), "w"), indent=1)
    print(f"shadows {len(res)}; UNSAT {sum(r['sat'] is False for r in res)}; SAT {sum(r['sat'] is True for r in res)}; undecided {sum(r['sat'] is None for r in res)}", flush=True)
    if len(res) == len(todo): print("FINAL ok yantra_sat", flush=True)
