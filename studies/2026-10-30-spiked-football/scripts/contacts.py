# Spiked football: exact contacts with the twelve stations scaled by phi^k (k = -2..4): spike tips on a station's faces, at its
# corners, or a station's corners on the faces of the spike hull; and the snug fits (spiked football inside a scaled station with
# tips touching, or a scaled station inside the spike hull touching it). Float screen at 1e-9 (the coordinates are exact in Q(sqrt5)).
import json, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
NUM = {k: np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in V]) for k, V in raw.items()}
del NUM['Cleo star tips']
P = NUM['TI']; h = ConvexHull(P); T = []
seen = set()
for eq in h.equations:
    k = tuple(np.round(eq, 7))
    if k in seen: continue
    seen.add(k); ids = [i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8]; T.append(2 * P[ids].mean(0))
T = np.array(T); A = np.vstack([P, T]); HT = ConvexHull(A); HP = A[HT.vertices]
res = []
for name, R0 in NUM.items():
    for k in range(-2, 5):
        R = R0 * phi ** k; hr = ConvexHull(R)
        dT = T @ hr.equations[:, :3].T + hr.equations[:, 3]
        tips_on_faces = int(np.sum(np.any(np.abs(dT) < 1e-9, axis=1)))
        tips_at_corners = int(sum(np.min(np.linalg.norm(R - t, axis=1)) < 1e-9 for t in T))
        dR = R @ HT.equations[:, :3].T + HT.equations[:, 3]
        corners_on_hull = int(np.sum(np.any(np.abs(dR) < 1e-9, axis=1)))
        spiked_inside = bool(np.all(dT <= 1e-9)) and bool(np.all(P @ hr.equations[:, :3].T + hr.equations[:, 3] <= 1e-9))
        station_inside = bool(np.all(dR <= 1e-9))
        if tips_on_faces or tips_at_corners or corners_on_hull:
            res.append(dict(station=name, k=k, tips_on_faces=tips_on_faces, tips_at_corners=tips_at_corners,
                            station_corners_on_spike_hull=corners_on_hull, spiked_inside_station=spiked_inside, station_inside_spike_hull=station_inside))
for r in res: print(r)
json.dump(res, open('data/contacts.json', 'w'), indent=1, ensure_ascii=False)
print('pentagon tip / hexagon tip radius', np.linalg.norm(T, axis=1).max() / np.linalg.norm(T, axis=1).min())
