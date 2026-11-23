"""Pull-apart renders of the Aequus amber cells in the house renderer (24 Nov 2026).
Scenes for the three.js renderer of the gold-standard figures (render3d.py of study 2026-11-21-scutoid-stand-in, unchanged: solid faces with
polygon offset, edges as tubes, depth-tested so no hidden edge shows through a face), shot by shots.mjs, then composed in the house look
(compose.py of the same study: dark warm ground, title, subtitle, swatches, DICTO mark).
Die: the app's face-family colours (the solid each family stands for; primed families lightened as in the app).  Scutoid frusta: neutral
pearl (keeps its side count) or neutral bronze (changes it); each moved out along the ray through its own centre.  Edges: true edges only
(triangles of one flat facet are merged; the crease edges of bent walls are drawn).
Usage: python render_cells.py scenes   -> renders/cells.html ;  python render_cells.py compose -> renders/RENDER-aequus-amber-*.png"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts"))
COL = {"C": "#488e48", "O": "#e8c852", "T": "#cd3e28", "D": "#8a5cc4", "I": "#3a70cd", "RD": "#b3a489", "RT": "#8e9aa5"}
PEARL, ASH, EDGE = "#d9d1bf", "#9c7448", "#2b261e"   # pearl and bronze: neutral labels
CELLS = [  # (die no., mould, file tag, title, subtitle)
    (377, "bcc", "Th-RD12-D12-I12p-RT24p-60", "Th die RD12 + D12 + I12′ + RT24′ in its amber cell",
     "60 faces (picker no. 377, not yet named): 12 heptagons, 12 squares at the dodecahedron's sites, 36 hexagons · bcc mould at 6/5 s0"),
    (1, "bcc", "DI-32-Ih1", "Aequus DI-32, Ih 1 in its amber cell", "20 hexagons, 12 pentagons · bcc mould at 6/5 s0"),
    (5, "bcc", "CO-14-Oh1", "Aequus CO-14, Oh 1 in its amber cell", "6 squares, 8 hexagons · bcc mould at 6/5 s0"),
    (236, "bcc", "Td-O8-4a-RT24-RT24p-28", "Td die O8/4a + RT24+RT24′/24a in its amber cell",
     "28 faces (picker no. 236, not yet named; non-heart Vacuus) · bcc mould at 6/5 s0"),
    (61, "bcc", "TRT-16-T3", "Aequus TRT-16, T 3 in its amber cell", "4 triangles, 12 hexagons (non-heart Vacuus) · bcc mould at 6/5 s0"),
    (61, "sc", "TRT-16-T3", "Aequus TRT-16, T 3 in its amber cell", "cube mould (sc) at 6/5 s0: the one cell whose scutoid frusta change their side count"),
]
DIR = [0.62, 0.48, 1.0]

def lighten(h): c = np.array([int(h[i:i+2], 16) for i in (1, 3, 5)]); c = 0.55*c + 0.45*255; return "#%02x%02x%02x" % tuple(int(round(x)) for x in c)

def mesh_part(tris, cols, rad):
    """triangles (k,3,3) -> part with shared vertices; tubes on true edges (boundary of a flat facet)."""
    key = {}; V = []
    def vid(p):
        k = tuple(np.round(p, 7))
        if k not in key: key[k] = len(V); V.append(list(p))
        return key[k]
    T = [[vid(p) for p in t] for t in tris]
    N = []
    for t in tris:
        n = np.cross(t[1] - t[0], t[2] - t[0]); N.append(n/np.linalg.norm(n))
    em = {}
    for i, t in enumerate(T):
        for a in range(3): em.setdefault(tuple(sorted((t[a], t[(a+1) % 3]))), []).append(i)
    tubes = [[e[0], e[1], EDGE, None] for e, L in em.items() if len(L) != 2 or abs(N[L[0]] @ N[L[1]] - 1) > 1e-7]
    return {"v": np.round(np.array(V), 6).tolist(), "t": T, "c": cols, "a": 1.0, "tubes": tubes, "rad": rad, "balls": []}

def scene(n, lat):
    R = json.load(open(os.path.join(ROOT, f"data/cells/stand/amber_aequus-{n}_{lat}_6-5_cen.json")))
    A = json.load(open(os.path.join(ROOT, "src/dice.json"))); e = A["dice"][n - 1]; dirs = np.array(A["dirs"])
    col_of = {}
    for oi in e["o"]:
        o = A["groups"][e["g"]][oi]; c = COL[o["col"].rstrip("2")]
        if o["col"].endswith("2"): c = lighten(c)
        for i in o["dirs"]: col_of[i] = c
    V = np.array(R["solid_V"]); tris, cols = [], []
    for f in R["solid_faces"]:
        P = V[f]; nrm = np.cross(P[1] - P[0], P[2] - P[0]); nrm /= np.linalg.norm(nrm)
        if nrm @ P.mean(0) < 0: nrm = -nrm
        c = col_of[int(np.argmax(dirs @ nrm))]
        for a in range(1, len(f) - 1): tris.append(P[[0, a, a+1]]); cols.append(c)
    sc = np.abs(V).max()
    parts = [mesh_part(tris, cols, 0.0024)]
    pieces = {p["F"]: p for p in R["pieces"]}
    for g in R["geom"]:
        T = np.array(g["tris"]); pc = pieces[g["F"]]
        shift = 1.0*T.reshape(-1, 3).mean(0)
        c = ASH if pc["sides_in"] != pc["sides_out"] else PEARL
        parts.append(mesh_part(list(T + shift), [c]*len(T), 0.0018))
    from render3d import basis
    x, y, _ = basis(DIR); P = np.vstack([p["v"] for p in parts])
    E = 1.05*max(np.abs(P @ x).max(), np.abs(P @ y).max())
    nk = sum(1 for p in R["pieces"] if p["sides_in"] == p["sides_out"])
    return {"E": float(E), "dir": DIR, "parts": parts}, (len(R["pieces"]), nk, len(R["pieces"]) - nk)

if __name__ == "__main__":
    if sys.argv[1] == "scenes":
        from render3d import write
        scs, meta = [], []
        for n, lat, tag, t, s in CELLS:
            sc, m = scene(n, lat); scs.append(sc); meta.append(m)
        os.makedirs(os.path.join(ROOT, "renders/shots"), exist_ok=True)
        write(os.path.join(ROOT, "renders/shots/cells.html"), scs)
        json.dump(meta, open(os.path.join(ROOT, "renders/shots/meta.json"), "w")); print("scenes", len(scs))
    else:
        import types
        src = open(os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts/compose.py")).read()
        Cp = types.ModuleType("compose_defs"); Cp.__dict__["__file__"] = os.path.join(ROOT, "renders/x")
        exec(src[:src.index("s = lambda")], Cp.__dict__)      # the house compose functions only, not its own figures
        Cp.OUT = os.path.join(ROOT, "renders"); meta = json.load(open(os.path.join(ROOT, "renders/shots/meta.json")))
        Cp.MARK = "DICTO · dictospheres.com"
        hexrgb = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
        for i, (n, lat, tag, t, s) in enumerate(CELLS):
            tot, nk, nc = meta[i]
            Cp.figure(f"RENDER-aequus-amber-{tag}-{lat}.png", t, s,
                      [(os.path.join(ROOT, "renders/shots", f"p{i}.png"), "pulled apart",
                        f"the die and its {tot} scutoid frusta: {nk} keep their side count, {nc} change it")],
                      [(hexrgb(PEARL), "keeps its side count"), (hexrgb(ASH), "changes its side count")], cell=1000)
