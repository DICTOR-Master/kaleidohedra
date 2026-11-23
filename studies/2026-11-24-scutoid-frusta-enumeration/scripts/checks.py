#!/usr/bin/env python3
"""Independent checks on the enumeration output + type list with IDs + tiling cells matched to IDs.
1. every stored polyhedron re-read from its planes: vertices satisfy all planes exactly; Euler V - E + F = 2; cubic graph;
   3-connected (removing any two vertices leaves it connected); n, m, k as recorded; lateral faces = (n + m + k)/2.
2. types pairwise distinct; counts against the hand formulas: (n,n,0): 1; (n,n+1,1): 1; (n,n+2,2): floor((n+2)/2) (both hands +1).
3. same polyhedron under several choices of ends (code without end marks).
4. the tiling cells of tilings.json named by ID."""
import sys, os, json, itertools, collections
sys.argv_save = sys.argv; sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import sf_enum as S
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
bad = 0
for fn, NM in (("types_n8_k2.json", 8), ("types_n14_k2.json", 14)):
    J = json.load(open(os.path.join(D, fn)))
    T = J["types"]
    T.sort(key=lambda t: (t["small_end"], t["large_end"], t["k"], t["vertices"], json.dumps(t["events"])))
    seen = set(); cnt = collections.Counter(); hands = collections.Counter()
    for t in T:
        planes = [tuple(Fr(c) for c in p) for p in t["planes"]]
        V = [tuple(Fr(c) for c in v) for v in t["verts"]]
        ok = all(p[0] * x[0] + p[1] * x[1] + p[2] * x[2] <= p[3] for p in planes for x in V)
        tight = [frozenset(i for i, p in enumerate(planes) if p[0] * x[0] + p[1] * x[1] + p[2] * x[2] == p[3]) for x in V]
        E = [(a, b) for a, b in itertools.combinations(range(len(V)), 2) if len(tight[a] & tight[b]) == 2]
        F = len(planes)
        deg = collections.Counter(); [deg.update(e) for e in E]
        ok &= len(V) - len(E) + F == 2 and all(deg[i] == 3 for i in range(len(V)))
        adj = collections.defaultdict(set)
        for a, b in E:
            adj[a].add(b); adj[b].add(a)
        for x, y in itertools.combinations(range(len(V)), 2):
            rest = [i for i in range(len(V)) if i not in (x, y)]
            st = [rest[0]]; vis = {rest[0]}
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w not in vis and w not in (x, y):
                        vis.add(w); st.append(w)
            if len(vis) != len(rest):
                ok = False; break
        n = sum(1 for i in range(len(V)) if 1 in tight[i]); m = sum(1 for i in range(len(V)) if 0 in tight[i])
        k = len(V) - n - m
        ok &= (n, m, k) == (t["top"], t["bottom"], t["k"]) and 2 * (F - 2) == n + m + k
        key = json.dumps(t["code"]); ok &= key not in seen; seen.add(key)
        if not ok:
            bad += 1; print("CHECK FAILED", fn, t["small_end"], t["large_end"], t["k"], t["events"])
        cnt[(t["small_end"], t["large_end"], t["k"])] += 1; hands[(t["small_end"], t["large_end"], t["k"])] += 2 if t["chiral"] else 1
    for n in range(3, NM + 1):
        if cnt[(n, n, 0)] != 1: bad += 1; print("formula k=0 fails", n)
        if n + 1 <= NM and cnt[(n, n + 1, 1)] != 1: bad += 1; print("formula k=1 fails", n)
        if n + 2 <= NM and (cnt[(n, n + 2, 2)], hands[(n, n + 2, 2)]) != ((n + 2) // 2, (n + 2) // 2 + 1):
            bad += 1; print("formula (n,n+2,2) fails", n)
    print(fn, "types", len(T), "checked (exact, Euler, cubic, 3-connected, n m k, lateral law, distinct); failures so far", bad)
    print("  (n,n,2) for n = 3..%d up to mirror:" % NM, [cnt[(n, n, 2)] for n in range(3, NM + 1)],
          " both hands:", [hands[(n, n, 2)] for n in range(3, NM + 1)])
    if NM == 8:
        ids = {}; per = collections.Counter(); rows = []
        for t in T:
            g = (t["small_end"], t["large_end"], t["k"]); per[g] += 1
            tid = f"SF {g[0]}-{g[1]}-{g[2]}" + (f".{per[g]}" if cnt[g] > 1 else "")
            ids[json.dumps(t["code"])] = tid; t["id"] = tid
            sizes = sorted(len(c) for f, c in t["faces"].items() if f not in ("0", "1"))
            rows.append(dict(id=tid, small_end=g[0], large_end=g[1], Y=g[2], chiral=t["chiral"], vertices=t["vertices"],
                             faces=len(t["faces"]), lateral_face_sides=sizes, bottom=t["bottom"], top=t["top"],
                             events=" ".join(("end " + str(e[1])) if e[0] == "del" else (f"start {e[1]} between {e[2]},{e[3]}") for e in t["events"])))
        groups = collections.defaultdict(list)
        for t in T:
            groups[json.dumps(t["code_no_ends"])].append(t["id"])
        multi = [v for v in groups.values() if len(v) > 1]
        print("  polyhedra that are Scutoid Frusta for more than one choice of ends:", multi)
        json.dump(dict(rows=rows, same_polyhedron_other_ends=multi), open(os.path.join(D, "type_list.json"), "w"), indent=0)
        with open(os.path.join(D, "type_list.csv"), "w") as f:
            f.write("id,small_end,large_end,Y,chiral,vertices,faces,lateral_face_sides,bottom,top,events_from_bottom\n")
            for r in rows:
                f.write(f"{r['id']},{r['small_end']},{r['large_end']},{r['Y']},{r['chiral']},{r['vertices']},{r['faces']},\"{' '.join(map(str, r['lateral_face_sides']))}\",{r['bottom']},{r['top']},{r['events']}\n")
        TL = json.load(open(os.path.join(D, "tilings.json")))
        for name, v in TL.items():
            for lab, c in v["cells"].items():
                if isinstance(c, dict):
                    print("  tiling", name, lab, "cell", c["bottom"], "->", c["top"], "Y", c["Y"], "= type", ids.get(json.dumps(c["code"]), "outside the n,m<=8, Y<=2 table"))
print("FINAL ok" if bad == 0 else "FINAL FAILED")
sys.exit(0 if bad == 0 else 1)
