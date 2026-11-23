"""Table of the permutahedron amber cells (data/amber_*_cen.json, written by amber_perm.py) -> data/amber-summary.md"""
import json, glob, os
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "../data")
NM = {"truncated_octahedron": "truncated octahedron (A3)", "B3_permutahedron_123": "B3 permutahedron (±1,±2,±3)", "truncated_icosidodecahedron": "truncated icosidodecahedron (H3)"}
SIDES = {"quad": 4, "hex": 6, "oct": 8, "dec": 10}
L = ["| core | mould | s | valid | pieces | kinds | with Y | Y vertices | kinds: face → solid-side / mould-side neighbours, Y, count per cell |", "|---|---|---|---|---|---|---|---|---|"]
for sol in NM:
    for lat in ("sc", "bcc", "fcc"):
        for fac in ("1", "6-5"):
            R = json.load(open(os.path.join(D, f"amber_{sol}_{lat}_{fac}_cen.json")))
            s = "s0 = " + R["s0"].replace("r5", "√5") if fac == "1" else "6/5 s0"
            if not R["valid"]:
                why = R["why"]
                if R.get("contact_faces") == R["n_faces"]: why = "all faces lie on the mould: the core IS its Voronoi cell (resin volume 0); it tiles alone"
                L.append(f"| {NM[sol]} | {lat} | {s} | no: {why[:90]} | | | | | |"); continue
            ks = "; ".join(f"{SIDES[k['kind']]}-gon → {len(k['Nin'])}/{len(k['Nout'])}, Y {k['Y']}, ×{len(k['members'])}" for k in R["kinds"])
            L.append(f"| {NM[sol]} | {lat} | {s} | yes | {len(R['pieces']) if len(R['pieces']) > len(R['kinds']) else sum(len(k['members']) for k in R['kinds'])} | {R['n_kinds']} | {R['n_scutoid_pieces']} | {R['n_Y']} | {ks} |")
open(os.path.join(D, "amber-summary.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
