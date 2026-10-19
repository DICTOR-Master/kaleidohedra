# The UP cycle (2026-10-19, float): from the ID the step rule gives RT -> golden TI -> Q -> ID again, 10/phi^4 times larger; stage 7 = RT
# times the same. Also re-checks stages 2 and 3 by random points (a volume match alone cannot rule out an overlap hiding a hole).
import json
from scipy.spatial import Delaunay
from stepper import *
RT = np.vstack([u5 * t5, u3 * t3]); S = nxt(nxt(nxt(RT))); k = np.linalg.norm(S[0]) / r
res = {'mark': 'DICTO Universal PiTet (UP) cycle check, 2026-10-19 (float)', 'scale': k, 'scale_is_10_over_phi4': abs(k - 10 / PHI ** 4) < 1e-12,
       'ID_returns': float(np.max(np.linalg.norm(S[:, None] - (ID * k)[None], axis=2).min(1))),
       'RT_returns': float(np.max(np.linalg.norm(nxt(S)[:, None] - (RT * k)[None], axis=2).min(1)))}
rng = np.random.default_rng(1)
def cover(inner, outer, pcs):
    ti, to = Delaunay(inner), Delaunay(outer); P = rng.uniform(-outer.max(), outer.max(), (300000, 3)); P = P[(to.find_simplex(P) >= 0) & (ti.find_simplex(P) < 0)]
    c = sum((Delaunay(q).find_simplex(P) >= 0).astype(int) for q in pcs); return {str(a): int(b) for a, b in Counter(c).items()}
res['stage2_cover'] = cover(D, ID, [np.vstack([D[np.argsort(-(D @ u))[:5]], ID[np.argsort(-(ID @ u))[:5]]]) for u in u5])
pc = [np.vstack([ID[np.argsort(-(ID @ u))[:5]], u * t5]) for u in u5] + [np.vstack([ID[np.argsort(-(ID @ u))[:3]], u * t3]) for u in u3]
e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(ID, 2))
for i, j in [(i, j) for i, j in itertools.combinations(range(30), 2) if abs(np.linalg.norm(ID[i] - ID[j]) - e) < 1e-9]:
    m = (ID[i] + ID[j]) / 2; pc.append(np.array([ID[i], ID[j], u5[np.argmax(u5 @ m)] * t5, u3[np.argmax(u3 @ m)] * t3]))
res['stage3_cover'] = cover(ID, RT, pc)
print(json.dumps(res, indent=1, default=float)); json.dump(res, open('data/cycle.json', 'w'), indent=1, default=float)
