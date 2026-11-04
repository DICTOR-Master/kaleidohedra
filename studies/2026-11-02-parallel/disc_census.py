# Disc test over the dataset (DICTO's slot-together Vacuus, 11-02): a solid's Vacuus can be slotted from flat board exactly when
# every fin (O, edge) lies in a plane whose fins close all the way round O. O = mean of the vertices (as in the census).
# Usage: disc_census.py <dataset dir> <star-cores scripts dir>  -> disc-census.json, prints the passing solids
import sys, os, json, glob, numpy as np
sys.path.insert(0, sys.argv[2]); from star_core import load
res = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'solids', '*.json'))):
    try: _, V, F = load(f)
    except Exception as e: continue
    V = np.array(V, float); V = V - V.mean(0); E = set()
    for fc in F:
        for i in range(len(fc)): E.add(tuple(sorted((fc[i], fc[(i + 1) % len(fc)]))))
    planes = {}
    for i, j in E:
        n = np.cross(V[i], V[j]); L = np.linalg.norm(n)
        if L < 1e-9: planes = None; break
        n /= L; k = np.argmax(np.abs(n)); n *= np.sign(n[k]); planes.setdefault(tuple(np.round(n, 6)), []).append((i, j))
    if planes is None: res.append(dict(solid=os.path.basename(f), discs=None)); continue
    ok = True; sizes = []
    for E2 in planes.values():
        deg = {}
        for i, j in E2: deg[i] = deg.get(i, 0) + 1; deg[j] = deg.get(j, 0) + 1
        sizes.append(len(E2)); ok &= len(E2) >= 3 and all(d == 2 for d in deg.values())
    res.append(dict(solid=os.path.basename(f), discs=bool(ok), planes=len(planes), sizes=sorted(set(sizes))))
json.dump(res, open('disc-census.json', 'w'), indent=1)
print(len(res), 'solids;', 'PASS:', [r['solid'] for r in res if r['discs']])
