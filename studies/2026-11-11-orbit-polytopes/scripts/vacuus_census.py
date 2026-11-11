"""Vacuus census (DICTO 11 Nov: "will other orbit groups be Vacuus"; "have the rest of the study vacuus gone through the test").
For every solid in the app's registry: its edges (from its faces), the central plane each edge spans with the centre, and how the edges
gather on those planes. A disc is a central plane carrying at least 3 edges. Reported: planes, discs, edges on discs (share), the
largest disc, faces lying on central planes. Controls: octahedron (3 planes x 4 edges), cuboctahedron (4 x 6). Float, tol 1e-6."""
import json, sys
import numpy as np
from collections import Counter
S = json.load(open(sys.argv[1])); out = []; ctrl = {}
for k, s in enumerate(S):
    V = np.array(s['V'], float); V = V - V.mean(0); F = s['F']
    E = set()
    for f in F:
        for i in range(len(f)): E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
    planes = {}; through = 0
    for a, b in E:
        n = np.cross(V[a], V[b])
        if np.linalg.norm(n) < 1e-9: through += 1; continue
        n /= np.linalg.norm(n); n = n if n[np.argmax(np.abs(n))] > 0 else -n
        planes.setdefault(tuple(np.round(n, 6)), []).append((a, b))
    sizes = Counter(len(v) for v in planes.values()); discs = {p: v for p, v in planes.items() if len(v) >= 3}
    on = sum(len(v) for v in discs.values()); cent = 0
    for f in F:
        P = V[f]; n = np.cross(P[1] - P[0], P[2] - P[0])
        if np.linalg.norm(n) > 1e-12 and abs((n / np.linalg.norm(n)) @ P[0]) < 1e-6: cent += 1
    r = {'id': s['id'], 'name': s['name'], 'edges': len(E), 'planes': len(planes), 'discs': len(discs), 'edges_on_discs': on,
         'share': round(on / max(1, len(E)), 3), 'largest_disc': max([len(v) for v in planes.values()] or [0]), 'edges_per_plane': dict(sorted(sizes.items())),
         'central_faces': cent, 'faces': len(F), 'edges_through_centre': through}
    out.append(r)
    if s['id'] in ('D8', 'CUBOCTAHEDRON'): ctrl[s['id']] = r
    print(f"PROGRESS {(k + 1) / len(S):.3f} {s['id']}: {len(E)} edges, {len(planes)} planes, {len(discs)} discs carry {on} ({r['share']:.0%}), largest {r['largest_disc']}", flush=True)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
ok = ctrl.get('D8', {}).get('edges_per_plane') == {4: 3} and ctrl.get('CUBOCTAHEDRON', {}).get('edges_per_plane') == {6: 4}
print('controls:', {k: v['edges_per_plane'] for k, v in ctrl.items()})
print('FINAL ok' if ok else 'FINAL FAIL (control)')
