"""Pull-apart render of an Aequus amber cell (24 Nov 2026): the die (core) at the centre in the app's face-family colours, the scutoid
frusta of the resin moved outward (each along the ray through its bottom face's centre), in two neutral tones: light = keeps its side
count, dark = changes it.  Painter's order per polygon, Lambert shading, crisp dark edges only along true edges (coplanar triangles
merged).  Usage: python render.py CELL.json OUT.png "TITLE" """
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection

COL = {"C": "#488e48", "O": "#e8c852", "T": "#cd3e28", "D": "#8a5cc4", "I": "#3a70cd", "RD": "#b3a489", "RT": "#8e9aa5"}
KEEP, CHANGE, EDGE = np.array([0.86, 0.85, 0.82]), np.array([0.42, 0.44, 0.47]), "#1b1b1b"
def hexrgb(h): return np.array([int(h[i:i+2], 16)/255 for i in (1, 3, 5)])

def main():
    cell, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
    R = json.load(open(cell)); A = json.load(open(sys.argv[4]))
    n = int(R["solid"].split("-")[1]); e = A["dice"][n - 1]
    dirs = np.array(A["dirs"]); col_of = {}
    for oi in e["o"]:
        o = A["groups"][e["g"]][oi]; c = hexrgb(COL[o["col"].rstrip("2")])
        if o["col"].endswith("2") or "′" in o["lab"] and "+" not in o["lab"]: c = 0.55*c + 0.45
        for i in o["dirs"]: col_of[i] = c
    V = np.array(R["solid_V"]); objs = []   # each object: list of (outward-oriented polygon, rgb)
    core = []
    for f in R["solid_faces"]:
        P = V[f]; nrm = np.cross(P[1] - P[0], P[2] - P[0]); nrm /= np.linalg.norm(nrm)
        if nrm @ P.mean(0) < 0: P = P[::-1]; nrm = -nrm
        j = int(np.argmax(dirs @ nrm)); core.append((P, col_of[j]))
    objs.append(("core", core))
    pieces = {p["F"]: p for p in R["pieces"]}
    for g in R["geom"]:
        pc = pieces[g["F"]]; T = np.array(g["tris"])
        vol = sum(np.linalg.det(t) for t in T)/6          # signed volume: orientation of the closed surface
        if vol < 0: T = T[:, ::-1]
        shift = 1.1*T.reshape(-1, 3).mean(0)   # pull apart: each piece moved out along the ray through its own centre
        rgb = CHANGE if pc["sides_in"] != pc["sides_out"] else KEEP
        objs.append((("p", g["F"]), [(t + shift, rgb) for t in T]))
    el, az = np.radians(22), np.radians(32)
    vdir = np.array([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])   # toward the viewer
    up = np.array([0, 0, 1.0]); rx = np.cross(up, vdir); rx /= np.linalg.norm(rx); ry = np.cross(vdir, rx)
    light = 0.6*vdir + 0.6*ry + 0.35*rx; light /= np.linalg.norm(light)
    from collections import defaultdict
    def k7(x): return tuple(np.round(x, 7))
    draw = []
    for gid, faces in objs:
        cen = np.vstack([P for P, c in faces]).mean(0)
        # true edges of this object: triangle edges whose two triangles are not coplanar
        emap = defaultdict(list); nr = []
        for k, (P, c) in enumerate(faces):
            n_ = np.cross(P[1] - P[0], P[2] - P[0]); n_ /= np.linalg.norm(n_); nr.append(n_)
            for a in range(len(P)): emap[tuple(sorted((k7(P[a]), k7(P[(a+1) % len(P)]))))].append(k)
        items = []
        for k, (P, c) in enumerate(faces):
            if nr[k] @ vdir <= 1e-9: continue                         # back face
            shade = 0.72 + 0.28*max(0.0, nr[k] @ light)
            segs = []
            for a in range(len(P)):
                ks = emap[tuple(sorted((k7(P[a]), k7(P[(a+1) % len(P)]))))]
                if len(ks) != 2 or abs(nr[ks[0]] @ nr[ks[1]] - 1) > 1e-6: segs.append([[P[a] @ rx, P[a] @ ry], [P[(a+1) % len(P)] @ rx, P[(a+1) % len(P)] @ ry]])
            items.append((P.mean(0) @ vdir, np.c_[P @ rx, P @ ry], np.clip(np.array(c)*shade, 0, 1), segs))
        items.sort(key=lambda x: x[0])
        draw.append((cen @ vdir, items))
    draw.sort(key=lambda x: x[0])
    fig, ax = plt.subplots(figsize=(9, 9.6), dpi=220)
    allp = []
    for d0, items in draw:
        for z, P2, c, segs in items:
            ax.add_collection(PolyCollection([P2], facecolors=[c], edgecolors=[c], linewidths=0.3)); allp.append(P2)
            if segs: ax.add_collection(LineCollection(segs, colors=EDGE, linewidths=0.9))
    allp = np.vstack(allp); m = allp.min(0); M = allp.max(0); pad = 0.04*(M - m).max()
    ax.set_xlim(m[0] - pad, M[0] + pad); ax.set_ylim(m[1] - pad, M[1] + pad); ax.set_aspect("equal"); ax.axis("off")
    nk = sum(1 for p in R["pieces"] if p["sides_in"] == p["sides_out"]); nc = len(R["pieces"]) - nk
    ax.set_title(title, fontsize=13, pad=10)
    fig.text(0.5, 0.045, f"Pull-apart view: the die at the centre (app face colours); its {len(R['pieces'])} scutoid frusta moved outward.\n"
             f"Light grey: keeps its side count ({nk}).  Dark grey: changes its side count ({nc}).  Mould: {R['lattice']} Voronoi cell at 6/5 s0.",
             ha="center", fontsize=9.5)
    fig.text(0.985, 0.012, "DICTO", ha="right", fontsize=10, color="#8a5cc4", weight="bold")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); print("wrote", out)

if __name__ == "__main__":
    main()
