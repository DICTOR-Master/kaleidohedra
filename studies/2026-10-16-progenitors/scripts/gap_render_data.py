# Adds the gap member (scripts/gap_member.py: hull of the RT's 12 five-fold corners and the 20 face centres of I·φ³, edge ratio 9/φ⁴) to
# data/full-cycle.json as st.G, from that file's own RT and I·φ³ (float corners of exact stations), with a check that it touches both.
import json, numpy as np
from scipy.spatial import ConvexHull
J = json.load(open('data/full-cycle.json'))
print('stations:', list(J['st']))
RT = np.array(J['st']['RT']['v']); IP = np.array(J['st']['Ip3']['v'])
r = np.linalg.norm(RT, axis=1); five = RT[np.abs(r - r.max()) < 1e-6]; assert len(five) == 12
h = ConvexHull(IP); E = []
for e in h.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in E): E.append(e)
fc = np.array([IP[np.abs(IP @ e[:3] + e[3]) < 1e-6].mean(0) for e in E]); assert len(fc) == 20
G = np.vstack([five, fc]); hg = ConvexHull(G)
faces = [list(map(int, s)) for s in hg.simplices]
# outward winding
for f in faces:
    a, b, c = G[f]
    if np.cross(b - a, c - a) @ a < 0: f[1], f[2] = f[2], f[1]
P = [e for e in hg.equations]
inside = max(((RT @ np.array(P)[:, :3].T) / (-np.array(P)[:, 3])).max(), 0)
outer = max((G @ np.array(E)[:, :3].T / (-np.array(E)[:, 3])).max(), 0)
print(f'RT reaches {inside:.9f} of G (1 = touching); G reaches {outer:.9f} of I·φ³; G faces {len(faces)}')
J['st']['G'] = {'v': np.round(G, 7).tolist(), 'f': faces}
json.dump(J, open('data/full-cycle.json', 'w'))
