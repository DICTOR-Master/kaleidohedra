"""Renders of the C116 -> Minana #377 shell (26 Nov 2026, night). With Claude (Anthropic). House renderer and compose (as render_cells.py).
Scenes: each layer pulled apart (core neutral stone, pieces pearl = keeps its side count, bronze = changes it); then the whole shell:
the three layers nested (layer 2 scaled by layer 1's factor, layer 3 by both), each piece pulled out a little, colour by layer.
Colours are neutral labels (no solid stands behind them). Usage: python render_c116.py scenes | compose"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts"))
sys.path.insert(0, HERE)
from render_cells import mesh_part, PEARL, ASH, DIR
STONE = "#8c8579"; LAYER = ["#d9d1bf", "#b9a88a", "#8f7a5c"]   # neutral, light to dark outward
R = [json.load(open(os.path.join(ROOT, f"data/cells/stand/amber_c116-layer{L}_layer_6-5_cen.json"))) for L in (1, 2, 3)]
def core_part(Rl, scale=1.0):
    V = np.array(Rl["solid_V"]) * scale; tris = []
    for f in Rl["solid_faces"]:
        P = V[f]
        for a in range(1, len(f) - 1): tris.append(P[[0, a, a + 1]])
    return mesh_part(tris, [STONE] * len(tris), 0.0024 * scale)
def pieces(Rl, scale, shift, colour=None):
    pcs = {p["F"]: p for p in Rl["pieces"]}; out = []
    for g in Rl["geom"]:
        T = np.array(g["tris"]) * scale; pc = pcs[g["F"]]
        c = colour or (ASH if pc["sides_in"] != pc["sides_out"] else PEARL)
        out.append(mesh_part(list(T + shift * T.reshape(-1, 3).mean(0)), [c] * len(T), 0.0018 * scale))
    return out
def frame(parts):
    from render3d import basis
    x, y, _ = basis(DIR); P = np.vstack([p["v"] for p in parts])
    return float(1.05 * max(np.abs(P @ x).max(), np.abs(P @ y).max()))
if __name__ == "__main__":
    if sys.argv[1] == "scenes":
        from render3d import write
        scs, meta = [], []
        for L in range(3):
            parts = [core_part(R[L])] + pieces(R[L], 1.0, 1.0)
            scs.append({"E": frame(parts), "dir": DIR, "parts": parts})
            meta.append([len(R[L]["pieces"]), R[L]["n_keep_sides"], R[L]["n_change_sides"], R[L]["n_Y"]])
        s1, s2 = R[0]["s"], R[1]["s"]
        parts = [core_part(R[0])] + pieces(R[0], 1.0, 0.25, LAYER[0]) + pieces(R[1], s1, 0.25, LAYER[1]) + pieces(R[2], s1 * s2, 0.25, LAYER[2])
        scs.append({"E": frame(parts), "dir": DIR, "parts": parts})
        os.makedirs(os.path.join(ROOT, "renders/c116"), exist_ok=True)
        write(os.path.join(ROOT, "renders/c116/c116.html"), scs)
        json.dump(meta, open(os.path.join(ROOT, "renders/c116/meta.json"), "w")); print("scenes", len(scs))
    else:
        import types
        src = open(os.path.join(ROOT, "../2026-11-21-scutoid-stand-in/renders/scripts/compose.py")).read()
        Cp = types.ModuleType("compose_defs"); Cp.__dict__["__file__"] = os.path.join(ROOT, "renders/x")
        exec(src[:src.index("s = lambda")], Cp.__dict__)
        Cp.OUT = os.path.join(ROOT, "renders"); meta = json.load(open(os.path.join(ROOT, "renders/c116/meta.json")))
        Cp.MARK = "DICTO · dictospheres.com"
        hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
        names = ["C116 to floor 1", "floor 1 to floor 2", "floor 2 to Minana #377"]
        for L in range(3):
            tot, nk, nc, ny = meta[L]
            Cp.figure(f"RENDER-c116-minana-layer{L + 1}.png", f"Layer {L + 1} of 3: {names[L]}",
                      f"{tot} Scutoid-Frusta, pulled apart round their core; {ny} Y vertices · exact cell (volume gap 0)",
                      [(os.path.join(ROOT, "renders/c116", f"p{L}.png"), "pulled apart", f"{nk} keep their side count, {nc} change it")],
                      [(hexrgb(PEARL), "keeps its side count"), (hexrgb(ASH), "changes its side count")], cell=1000)
        Cp.figure("RENDER-c116-minana-shell.png", "From C116 to Minana #377 in three layers",
                  "The fullerene C116 (its one Th isomer) grows into the 60-face fair die Minana #377 through two floors · 180 Scutoid-Frusta",
                  [(os.path.join(ROOT, "renders/c116", "p3.png"), "nested, pulled apart a little", "core C116; layers 1, 2, 3 outward")],
                  [(hexrgb(STONE), "C116 core"), (hexrgb(LAYER[0]), "layer 1"), (hexrgb(LAYER[1]), "layer 2"), (hexrgb(LAYER[2]), "layer 3")], cell=1000)
        print("composed 4")
