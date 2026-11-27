"""C116 -> Minana #377, Hollow-straw layer (the paper's exact layer), in the Aequi colours (27 Nov 2026; DICTO: "a gold standard render
of C116 using the Aequis colours for the inside form and outside Scutoid-Frusta construction"). With Claude (Anthropic).
Colours are the Aequi page's own (k-mix/aequi/index.html: COL and colOf): every face of Minana #377 takes the colour of the solid whose
plane it lies on (12 rhombic dodecahedron, 12 dodecahedron, 12 icosahedron (second placement, lightened), 24 rhombic triacontahedron
(second placement, lightened)). Each Scutoid-Frustum k and each core face k of C116 take the colour of the Minana face sigma(k) they
turn into. Panels: the C116 core alone, pulled apart, assembled. House renderer and compose (as render_layer.py).
Usage: python render_aequi.py scenes | compose"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts")); sys.path.insert(0, HERE)
from render_cells import mesh_part, DIR
from render_c116 import frame
COL = {'C': '#488e48', 'O': '#e8c852', 'T': '#cd3e28', 'D': '#8a5cc4', 'I': '#3a70cd', 'RD': '#b3a489', 'RT': '#8e9aa5'}   # Aequi page
SOLID = {'RD': 'rhombic dodecahedron', 'D': 'dodecahedron', 'I': 'icosahedron', 'RT': 'rhombic triacontahedron'}
def mix(a, b, t): return '#' + ''.join('%02x' % round(int(a[1 + 2 * i:3 + 2 * i], 16) * (1 - t) + int(b[1 + 2 * i:3 + 2 * i], 16) * t) for i in range(3))
def colOf(key): base = COL[key.replace('2', '')]; return mix(base, '#ffffff', 0.45) if key.endswith('2') else base
D = os.path.join(ROOT, "renders/c116aequi")
if sys.argv[1] == "scenes":
    argv = list(sys.argv); sys.argv = sys.argv[:1]
    import amber_aequus as A
    sys.argv = argv
    from aequus_solid import build
    import aequus_solid as AS
    from collections import Counter
    R = json.load(open(os.path.join(ROOT, 'data/cells/stand/hollow_straw_float.json')))
    sig = {int(k): int(v) for k, v in json.load(open(os.path.join(ROOT, 'data/c116/onefloor_float.json')))['pairing'].items()}
    S = build("aequus-377")
    # orbit colour per Minana face: the app's dice.json orbit order, matched to each face by its exact plane direction
    Dd = json.load(open(os.path.join(ROOT, "src/dice.json"))); e = Dd["dice"][376]; ED = AS.C.exact_dirs(Dd["dirs"])
    lab = {}
    for oi in e["o"]:
        g = Dd["groups"][e["g"]][oi]
        for i in g["dirs"]: lab[A.key([AS.Q(c.a, c.b) for c in ED[i][0]])] = g["col"]      # exact direction, as build() makes it
    mcol = [lab[A.key(u)] for u, c in S["planes"]]
    print('Minana #377 faces by colour key:', dict(Counter(mcol)), flush=True)
    assert sorted(Counter(mcol).values()) == [12, 12, 12, 24]
    pcs = {int(p["F"]): p for p in R["pieces"]}          # hollow_straw.py numbers piece t by its MINANA face t (core face sigma^-1(t))
    pcol = {t: mcol[t] for t in range(60)}
    assert all(len(S["faces"][t][0]) == int(pcs[t]["sides_out"]) and sig[int(pcs[t]["core_face"])] == t for t in range(60)), "piece t must end on Minana face t"
    geo = {int(g["F"]): np.array(g["tris"]) for g in R["geom"]}
    def dist_to_piece(c, T):
        best = 9.0
        for t in T:
            a, b, cc = t; n = np.cross(b - a, cc - a); nn = np.linalg.norm(n)
            if nn < 1e-14: continue
            n /= nn; dpl = abs((c - a) @ n); p = c - ((c - a) @ n) * n
            w = [np.cross(b - a, p - a) @ n, np.cross(cc - b, p - b) @ n, np.cross(a - cc, p - cc) @ n]
            if min(w) >= -1e-9 or max(w) <= 1e-9: best = min(best, dpl)
        return best
    V = np.array(R["solid_V"]); ctris, ccols = [], []
    for f in R["solid_faces"]:
        P = V[f]
        for a in range(1, len(f) - 1):
            t = P[[0, a, a + 1]]; c = t.mean(0)
            k = min(range(60), key=lambda q: dist_to_piece(c, geo[q])); assert dist_to_piece(c, geo[k]) < 1e-6
            ctris.append(t); ccols.append(colOf(pcol[k]))
    core = mesh_part(ctris, ccols, 0.0024)
    def pieces(shift):
        return [mesh_part(list(T + shift * T.reshape(-1, 3).mean(0)), [colOf(pcol[k])] * len(T), 0.0018) for k, T in geo.items()]
    from render3d import write
    full = [core] + pieces(0.9)
    scs = [{"E": frame(full), "dir": DIR, "parts": [core]}]
    for sh in (0.9, 0.0):
        parts = [core] + pieces(sh); scs.append({"E": frame(full), "dir": DIR, "parts": parts})
    os.makedirs(D, exist_ok=True); write(os.path.join(D, "c116aequi.html"), scs)
    json.dump(dict(Counter(mcol)), open(os.path.join(D, "meta.json"), "w"))
    print("scenes", len(scs), flush=True)
else:
    import types
    src = open(os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts/compose.py")).read()
    Cp = types.ModuleType("compose_defs"); Cp.__dict__["__file__"] = os.path.join(ROOT, "renders/x")
    exec(src[:src.index("s = lambda")], Cp.__dict__)
    Cp.OUT = os.path.join(ROOT, "renders"); Cp.MARK = "DICTO · dictospheres.com"
    meta = json.load(open(os.path.join(D, "meta.json"))); hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    Cp.figure("RENDER-c116-minana-aequi.png", "From C116 to Minana #377: one layer of Scutoid-Frusta",
              "Every core face and every piece in the colour of the Aequus face it becomes · 60 convex Scutoid-Frusta, 18 Y vertices, exact",
              [(os.path.join(D, "p0.png"), "the core", "fullerene C116"), (os.path.join(D, "p1.png"), "pulled apart", "core and 60 Scutoid-Frusta"),
               (os.path.join(D, "p2.png"), "assembled", "outer surface = Minana #377")],
              [(hexrgb(colOf(k)), f"{SOLID[k.replace('2', '')]} planes ({meta[k]})") for k in ('D', 'I2', 'RD', 'RT2') if k in meta], cell=1000)
    print("composed")
    out = os.path.join(ROOT, "renders/RENDER-c116-minana-aequi.png")
    print("FINAL ok" if os.path.exists(out) and os.path.getsize(out) > 100000 else "FINAL FAIL (no composed figure)")
