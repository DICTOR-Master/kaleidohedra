"""Renders of the ONE-layer C116 -> Minana #377 shell (27 Nov 2026; best alignment, c116_orbitpairs.py / c116_onefloor.py).
With Claude (Anthropic). House renderer and compose (as render_c116.py). Colours are neutral labels for the four kinds of piece:
hexagon -> square, pentagon -> hexagon, hexagon -> heptagon, keeps its side count. Usage: python render_c116_one.py scenes | compose"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts")); sys.path.insert(0, HERE)
from render_cells import mesh_part, DIR
from render_c116 import core_part, frame, STONE
KIND = {(6, 4): "#e8e1d0", (5, 6): "#b9a88a", (6, 7): "#7d6a50", (6, 6): "#a7afb4"}
NAMES = {(6, 4): "hexagon to square", (5, 6): "pentagon to hexagon", (6, 7): "hexagon to heptagon", (6, 6): "keeps six sides"}
R = json.load(open(os.path.join(ROOT, "data/cells/stand/amber_c116-layer0_layer_6-5_cen.json")))
def pieces(shift):
    pcs = {p["F"]: p for p in R["pieces"]}; out = []
    for g in R["geom"]:
        T = np.array(g["tris"]); pc = pcs[g["F"]]; c = KIND[(pc["sides_in"], pc["sides_out"])]
        out.append(mesh_part(list(T + shift * T.reshape(-1, 3).mean(0)), [c] * len(T), 0.0018))
    return out
if __name__ == "__main__":
    if sys.argv[1] == "scenes":
        from render3d import write
        scs = []
        for sh in (0.9, 0.0):
            parts = [core_part(R)] + pieces(sh); scs.append({"E": frame(parts), "dir": DIR, "parts": parts})
        os.makedirs(os.path.join(ROOT, "renders/c116one"), exist_ok=True)
        write(os.path.join(ROOT, "renders/c116one/c116one.html"), scs)
        from collections import Counter
        json.dump(dict(Counter(f"{p['sides_in']}-{p['sides_out']}" for p in R["pieces"])), open(os.path.join(ROOT, "renders/c116one/meta.json"), "w"))
        print("scenes", len(scs))
    else:
        import types
        src = open(os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts/compose.py")).read()
        Cp = types.ModuleType("compose_defs"); Cp.__dict__["__file__"] = os.path.join(ROOT, "renders/x")
        exec(src[:src.index("s = lambda")], Cp.__dict__)
        Cp.OUT = os.path.join(ROOT, "renders"); Cp.MARK = "DICTO · dictospheres.com"
        meta = json.load(open(os.path.join(ROOT, "renders/c116one/meta.json")))
        hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
        Cp.figure("RENDER-c116-minana-one-layer.png", "From C116 to Minana #377 in ONE layer",
                  f"60 Scutoid-Frusta, 30 Y vertices, exact cell (volume gap 0) · best alignment: 144 of 174 neighbour pairs kept, 30 single swaps",
                  [(os.path.join(ROOT, "renders/c116one", "p0.png"), "pulled apart", "core C116 (stone)"),
                   (os.path.join(ROOT, "renders/c116one", "p1.png"), "assembled", "outer surface = Minana #377")],
                  [(hexrgb(STONE), "C116 core")] + [(hexrgb(KIND[k]), f"{NAMES[k]} ({meta.get(f'{k[0]}-{k[1]}', 0)})") for k in KIND], cell=1000)
        print("composed 1")
