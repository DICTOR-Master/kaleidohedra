"""Renders of the hidden associahedra (24 Nov 2026) in the house renderer (render3d.py of study 2026-11-21-scutoid-stand-in, unchanged:
solid faces, edges as tubes, see-through faces hide what is behind them) and the house compose (compose.py of the same study).
Colours are labels only (neutral palette): associahedron faces by side count; permutahedron facets kept (pearl) or removed (bronze).
Usage: python render_assoc.py scenes -> ../renders/shots/assoc.html ; node shots.mjs ... ; python render_assoc.py compose"""
import json, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts"))
SIDES = {4: "#7f93a8", 5: "#d6b46a", 6: "#c99e95", 7: "#8f8a80"}     # slate, gold, rose, grey (neutral labels)
NAME = {4: "squares", 5: "pentagons", 6: "hexagons", 7: "heptagons"}
PEARL, BRONZE, GLASS, EDGE = "#e2ded6", "#9c7448", "#78808a", "#2b261e"
C = "s1 s2 s3"
TYPES = [("A3", "truncated octahedron"), ("B3", "truncated cuboctahedron"), ("H3", "truncated icosidodecahedron")]
DIR = [0.62, 0.48, 1.0]

def part(V, faces, cols, alpha, rad):
    tris, tc, tubes, seen = [], [], [], set()
    for f, c in zip(faces, cols):
        for a in range(1, len(f) - 1): tris.append([f[0], f[a], f[a + 1]]); tc.append(c)
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            if e not in seen: seen.add(e); tubes.append([e[0], e[1], EDGE, None])
    return {"v": np.round(np.array(V), 6).tolist(), "t": tris, "c": tc, "a": alpha, "tubes": tubes, "rad": rad, "balls": []}

def scenes():
    from render3d import write
    out, meta = [], []
    for typ, nm in TYPES:
        R = json.load(open(os.path.join(ROOT, f"data/assoc-{typ}.json")))["results"][C]
        V = np.array(R["_V"]); F = R["_faces"]; P = np.array(R["_perm_V"])
        sc = np.abs(V).max()
        a = part(V, F, [SIDES[len(f)] for f in F], 1.0, 0.004)
        E = 1.08 * np.linalg.norm(V, axis=1).max()
        out.append({"E": float(E), "dir": DIR, "parts": [a]})
        glass = part(V, F, [GLASS] * len(F), 0.22, 0.0025)
        pk = part(P, R["_perm_faces_kept"] + R["_perm_faces_removed"],
                  [PEARL] * len(R["_perm_faces_kept"]) + [BRONZE] * len(R["_perm_faces_removed"]), 1.0, 0.003)
        out.append({"E": float(E), "dir": DIR, "parts": [pk, glass]})
        c0 = P.mean(0); P0 = P - c0
        pk0 = part(P0, R["_perm_faces_kept"] + R["_perm_faces_removed"],
                   [PEARL] * len(R["_perm_faces_kept"]) + [BRONZE] * len(R["_perm_faces_removed"]), 1.0, 0.004)
        out.append({"E": float(1.12 * np.linalg.norm(P0, axis=1).max()), "dir": DIR, "parts": [pk0]})
        meta.append({"typ": typ, "nm": nm, "fs": R["faces_by_sides"], "kept": R["kept_facets"], "removed": R["removed_facets"],
                     "V": R["vertices"], "shared": R["shared_vertices_with_perm"], "kept_by": R["kept_by_sides"], "rem_by": R["removed_by_sides"]})
    os.makedirs(os.path.join(ROOT, "renders/shots"), exist_ok=True)
    write(os.path.join(ROOT, "renders/shots/assoc.html"), out)
    json.dump(meta, open(os.path.join(ROOT, "renders/shots/meta.json"), "w"))
    print("scenes", len(out))

def compose():
    src = open(os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts/compose.py")).read()
    Cp = types.ModuleType("compose_defs"); Cp.__dict__["__file__"] = os.path.join(ROOT, "renders/x")
    exec(src[:src.index("s = lambda")], Cp.__dict__)
    Cp.OUT = os.path.join(ROOT, "renders"); Cp.MARK = "DICTO · dictospheres.com"
    meta = json.load(open(os.path.join(ROOT, "renders/shots/meta.json")))
    hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    WORD = {4: "squares", 6: "hexagons", 8: "octagons", 10: "decagons"}
    for i, m in enumerate(meta):
        fs = {int(k): v for k, v in m["fs"].items()}
        facedesc = ", ".join(f"{fs[k]} {NAME[k]}" for k in sorted(fs))
        rem = ", ".join(f"{v} {WORD[int(k)]}" for k, v in sorted(m["rem_by"].items(), key=lambda kv: int(kv[0])))
        kept = ", ".join(f"{v} {WORD[int(k)]}" for k, v in sorted(m["kept_by"].items(), key=lambda kv: int(kv[0])))
        Cp.figure(f"RENDER-associahedron-{m['typ']}.png",
                  f"The {m['typ']} associahedron hidden in the {m['nm']}",
                  f"Hohlweg–Lange–Thomas construction, Coxeter element s1 s2 s3: remove {m['removed']} facets of the permutahedron, keep {m['kept']}; "
                  f"{m['V']} corners, {m['shared']} shared with the permutahedron",
                  [(os.path.join(ROOT, "renders/shots", f"p{3 * i}.png"), "the associahedron", facedesc),
                   (os.path.join(ROOT, "renders/shots", f"p{3 * i + 1}.png"), "the permutahedron inside it", "same scale, associahedron see-through"),
                   (os.path.join(ROOT, "renders/shots", f"p{3 * i + 2}.png"), "the permutahedron, close up",
                    f"kept: {kept} · removed: {rem}")],
                  [(hx(SIDES[k]), NAME[k]) for k in sorted(fs)] + [(hx(PEARL), "kept facet"), (hx(BRONZE), "removed facet"), (hx(GLASS), "associahedron, see-through")],
                  cell=640)

if __name__ == "__main__":
    scenes() if sys.argv[1] == "scenes" else compose()
