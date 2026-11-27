"""Which Star Cores stars come closest to a Vacuus-Solid? (27 Nov 2026; DICTO "yes please"). With Claude (Anthropic). For every shape,
rule (t = 2, phi) and turn: the star (solid S + a spike per face), its hull H, and the Vacuus-Solid of H whose pits reach down to the star
(pit bottom on each face axis = where the axis meets S). Reported: the share of that Vacuus-Solid's volume the star fills (1 = the star IS
it), and whether the pit bottoms lie at one common size (a genuine family member). Numerical (volumes by convex hulls)."""
import json, sys
import numpy as np
from scipy.spatial import ConvexHull
A = json.load(open(sys.argv[1])); rows = []
for sh in A:
    for T in sh['turns']:
        try:
            V = np.array(T['solid']['vertices'], float); F = T['solid']['faces']; tips = T['tips']
            if tips is None or len(tips) != len(F): continue
            tips = np.array(tips, float); c0 = V.mean(0); V = V - c0; tips = tips - c0
            star = ConvexHull(V).volume + sum(ConvexHull(np.vstack([V[f], [tp]])).volume for f, tp in zip(F, tips))
            P = np.vstack([V, tips]); h = ConvexHull(P); fs = {}
            for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(sm)
            Sp = []
            for f in F:
                X = V[f]; n = np.cross(X[1] - X[0], X[2] - X[0]); n /= np.linalg.norm(n); n = n if n @ X[0] > 0 else -n; Sp.append((n, n @ X[0]))
            pv = 0; lam = []
            for k, idx in fs.items():
                n = np.array(k[:3]); n /= np.linalg.norm(n); d = -k[3]; s = min(dd / (m @ n) for m, dd in Sp if m @ n > 1e-12)
                pv += ConvexHull(np.vstack([P[list(idx)], [s * n]])).volume; lam.append(s * d)
            vs = h.volume - pv; lam = np.array(lam); spread = float(np.ptp(lam) / lam.mean())
            rows.append(dict(D=sh['D'], name=sh['name'], t=sh['t'], turn=T['turn'], S_corners=len(V), S_faces=len(F), hull_faces=len(fs),
                             share=float(star / vs), one_size=bool(spread < 1e-6)))
        except Exception as ex:
            continue
rows.sort(key=lambda r: -r['share'] if r['share'] <= 1.0001 else -1)
print('tested', len(rows), 'stars (shape x rule x turn)')
for r in rows[:25]:
    print(f"{r['D']:6s} {r['name'][:28]:28s} t={r['t']:3s} turn {r['turn']}: star fills {100 * r['share']:5.1f}% of its hull's Vacuus-Solid; "
          f"pit bottoms at one size: {r['one_size']}; S {r['S_corners']}/{r['S_faces']}, hull faces {r['hull_faces']}", flush=True)
over = [r for r in rows if r['share'] > 1.0001]
if over: print('shares above 100% (the star bulges outside that Vacuus-Solid; test not meaningful there):', len(over))
json.dump(rows, open(sys.argv[2], 'w'), indent=1)
print('FINAL ok' if rows else 'FINAL FAIL (nothing tested)')
