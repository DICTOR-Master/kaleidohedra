"""Amber-cell sweep summary: reads ../data/amber_*.json, re-checks each claimed partition (exact volume gap 0, no problems, sampling with
0 miscounted points) and prints the table solid x mould.  FINAL ok only if every claimed partition re-checks and at least one exists."""
import glob, json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
SOL = ["C1", "C2", "dodecahedron", "icosahedron", "icosidodecahedron", "truncated_icosahedron", "rhombic_triacontahedron",
       "truncated_dodecahedron", "dodeca_icosa_compound"]
recs = [json.load(open(f)) for f in glob.glob(os.path.join(D, "amber_*.json"))]
recs.sort(key=lambda r: (SOL.index(r["solid"]), ["sc", "bcc", "fcc"].index(r["lattice"]), r["factor"] != "1"))
ok, nv = True, 0
print("solid | mould | s | contact v/e/f | valid | kinds | scutoids | Y | 157.76 | fins | sampling")
for r in recs:
    sc = "s0" if r["factor"] == "1" else r["factor"] + " s0"
    c = f"{len(r['contact_vertices'])}/{r['contact_edges']}/{r['contact_faces']}"
    if r["valid"]:
        nv += 1
        good = r.get("volume_gap") == "0" and not r.get("problems") and r["sampling"]["miscounted"] == 0
        ok &= good
        print(f"{r['solid']} | {r['lattice']} | {sc} = {r['s']:.6f} | {c} | yes{'' if good else ' RECHECK FAILED'} | {r['n_kinds']} | "
              f"{r['n_scutoid_pieces']}/{r['n_faces']} | {r['n_Y']} | {'present' if r['lambda_present'] else 'absent'} | {r.get('fins_cancelled', 0)} | "
              f"{r['sampling']['points']} pts, 0 miscounted")
    else:
        print(f"{r['solid']} | {r['lattice']} | {sc} = {r['s']:.6f} | {c} | no: {r['why'][:110]} | | | | | |")
print("s0 exact:", {(r["solid"], r["lattice"]): r["s0"] for r in recs if r["factor"] == "1"})
print("FINAL ok" if ok and nv else "FINAL FAIL")
