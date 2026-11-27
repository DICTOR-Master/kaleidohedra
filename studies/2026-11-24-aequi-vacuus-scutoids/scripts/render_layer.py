"""Renders of one C116 -> Minana #377 layer (27 Nov 2026): pulled apart and assembled. With Claude (Anthropic).
LAYER = float (floating-resin layer, amber cell, 18 Y vertices) or straw (Hollow-straw layer, flat walls, convex pieces).
House renderer and compose (as render_c116_one.py). Colours: neutral labels for the five kinds of piece."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts")); sys.path.insert(0, HERE)
from render_cells import mesh_part, DIR
from render_c116 import core_part, frame, STONE
L = os.environ.get('LAYER', 'float')
SRC = {'float': 'amber_c116-layer0float_layer_6-5_cen.json', 'straw': 'hollow_straw_float.json'}[L]
R = json.load(open(os.path.join(ROOT, 'data/cells/stand', SRC)))
KIND = {(5, 4): "#e8e1d0", (5, 7): "#cdbf9f", (6, 4): "#a89272", (6, 7): "#6f5c45", (6, 6): "#a7afb4"}
NAMES = {(5, 4): "pentagon to square", (5, 7): "pentagon to heptagon", (6, 4): "hexagon to square", (6, 7): "hexagon to heptagon", (6, 6): "keeps six sides"}
def pieces(shift):
    pcs = {p["F"]: p for p in R["pieces"]}; out = []
    for g in R["geom"]:
        T = np.array(g["tris"]); pc = pcs[g["F"]]; c = KIND[(pc["sides_in"], pc["sides_out"])]
        out.append(mesh_part(list(T + shift * T.reshape(-1, 3).mean(0)), [c] * len(T), 0.0018))
    return out
D = os.path.join(ROOT, f"renders/c116{L}")
if sys.argv[1] == "scenes":
    from render3d import write
    scs = []
    for sh in (0.9, 0.0):
        parts = [core_part(R)] + pieces(sh); scs.append({"E": frame(parts), "dir": DIR, "parts": parts})
    os.makedirs(D, exist_ok=True); write(os.path.join(D, f"c116{L}.html"), scs)
    from collections import Counter
    json.dump({f"{a}-{b}": c for (a, b), c in Counter((p['sides_in'], p['sides_out']) for p in R['pieces']).items()}, open(os.path.join(D, "meta.json"), "w"))
    print("scenes", len(scs))
else:
    import types
    src = open(os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts/compose.py")).read()
    Cp = types.ModuleType("compose_defs"); Cp.__dict__["__file__"] = os.path.join(ROOT, "renders/x")
    exec(src[:src.index("s = lambda")], Cp.__dict__)
    Cp.OUT = os.path.join(ROOT, "renders"); Cp.MARK = "DICTO · dictospheres.com"
    meta = json.load(open(os.path.join(D, "meta.json"))); hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    if L == 'float':
        title = "From C116 to Minana #377: the floating-resin layer"
        sub = "60 Scutoid-Frusta, 18 Y vertices, exact cell (volume gap 0) · the core floated to its best alignment: 156 of 174 neighbour pairs kept, 18 single swaps"
    else:
        title = "From C116 to Minana #377: Hollow-straw, flat walls"
        sub = "60 convex Scutoid-Frusta, 18 Y vertices · core: C116's face pattern, pressed parallel to the die's faces (not C116's own shape)"
    Cp.figure(f"RENDER-c116-minana-{L}.png", title, sub,
              [(os.path.join(D, "p0.png"), "pulled apart", "core in stone" if L == "float" else "core: C116 pattern, die-pressed"), (os.path.join(D, "p1.png"), "assembled", "outer surface = Minana #377")],
              [(hexrgb(STONE), "core")] + [(hexrgb(KIND[k]), f"{NAMES[k]} ({meta.get(f'{k[0]}-{k[1]}', 0)})") for k in KIND if f'{k[0]}-{k[1]}' in meta], cell=1000)
    print("composed")
