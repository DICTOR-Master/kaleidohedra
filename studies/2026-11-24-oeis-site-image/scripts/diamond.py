"""Diamond network picture for the OEIS link on dictospheres.com (24 Nov 2026).
Atoms of diamond (two fcc lattices, offset (1/4,1/4,1/4)), bonds = nearest neighbours (length sqrt(3)/4 of the cube edge).
One closed non-backtracking walk is shown in gold: a six-atom ring (the shortest closed non-backtracking walk on diamond, length 6;
A400949 counts these walks per atom). Usage: python diamond.py <out.html>  (render3d.write; frames by shots.mjs)."""
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/renders/scripts"))
from render3d import write
fcc = [(0,0,0),(0,.5,.5),(.5,0,.5),(.5,.5,0)]
pts = []
for i,j,k in itertools.product(range(-2,3), repeat=3):
    for b in fcc:
        for o in [(0,0,0),(.25,.25,.25)]:
            pts.append((i+b[0]+o[0], j+b[1]+o[1], k+b[2]+o[2]))
P = np.unique(np.round(np.array(pts),6), axis=0)
c0 = np.array([.125,.125,.125])            # bond centre in the middle of the picture
P = P[np.linalg.norm(P-c0, axis=1) <= float(os.environ.get("RCUT", "1.05"))]
while True:   # drop loose ends: keep atoms with at least two bonds inside the cluster
    D = np.linalg.norm(P[:,None]-P[None], axis=2); deg = (np.abs(D-np.sqrt(3)/4) < 1e-6).sum(1)
    if (deg >= 2).all(): break
    P = P[deg >= 2]
bonds = [(a,b) for a in range(len(P)) for b in range(a+1,len(P)) if abs(D[a,b]-np.sqrt(3)/4) < 1e-6]
# a six-atom ring through the two central atoms: (0,0,0)->(1/4,1/4,1/4)->(1/2,1/2,0)->(3/4,3/4,1/4)? no: use a verified ring by search
adj = {i: [b for a,b in bonds if a==i]+[a for a,b in bonds if b==i] for i in range(len(P))}
VIEW = np.array([float(x) for x in os.environ.get("VIEW", "1,0.72,0.42").split(",")]); VIEW = VIEW/np.linalg.norm(VIEW)
Pc = P - P.mean(axis=0); near = np.linalg.norm(Pc, axis=1) < 0.55
start = int(np.argmax(np.where(near, Pc @ VIEW, -9)))   # ring at the front, near the middle
ring = None
def dfs(path):
    global ring
    if ring: return
    if len(path)==6:
        if start in adj[path[-1]]: ring = path[:]
        return
    for n in adj[path[-1]]:
        if n not in path and (len(path)<2 or n!=path[-2]): dfs(path+[n])
dfs([start])
assert ring and len(set(ring))==6 and all(ring[(i+1)%6] in adj[ring[i]] for i in range(6))
ringE = {tuple(sorted((ring[i], ring[(i+1)%6]))) for i in range(6)}
GOLD, SILVER, BOND, OUT = "#e0b84a", "#d9dde3", "#9aa3ad", "#1b2230"
V = (P - P.mean(axis=0)).tolist()
tubes = [[a,b, GOLD if (a,b) in ringE else BOND, OUT] for a,b in bonds]
balls = [[i, GOLD if i in ring else SILVER] for i in range(len(P))]
part = {"v": np.round(V,6).tolist(), "t": [], "c": [], "a": 1, "tubes": tubes, "rad": 0.011, "balls": []}
atoms = {"v": np.round(V,6).tolist(), "t": [], "c": [], "a": 1, "tubes": [], "rad": 0.034, "balls": balls}
nv = np.cross(P[ring[1]]-P[ring[0]], P[ring[2]]-P[ring[0]]); nv = nv/np.linalg.norm(nv)
views = [VIEW.tolist(), (VIEW + np.array([0,0.15,0.1])).tolist(), (VIEW*1.0 + 0.35*nv).tolist(), [1,0.9,0.6]]
scenes = [{"E": float(os.environ.get("E","1.55")), "dir": list(map(float,d)), "parts": [part, atoms]} for d in views]
write(sys.argv[1], scenes)
print("atoms", len(P), "bonds", len(bonds), "ring", ring, "FINAL ok" if len(bonds) > 0 else "FINAL FAIL")
