"""Disc ranking under two rules (13 Nov 2026; Platonic book Ch 4 lead; lead 1 of studies/2026-11-13-platonic-exact-checks).
For every solid of the app registry (389 solids, data/registry-solids.json: corners V, faces F, the same file the 11-11 census read):
  rule 11-11 (studies/2026-11-11-orbit-polytopes/scripts/vacuus_census.py): a disc = a central plane carrying >= 3 edges;
  rule #87  (studies/2026-11-02-dicto-vacuus/scripts/vacuus.py; exact form in studies/2026-11-13-platonic-exact-checks): the fins O-A-B
            of the edges join into flat sheets across a shared corner ray when coplanar and on opposite sides of the ray; a central
            disc = a sheet whose apex angles sum to 2 pi. Decided twice: (a) the float apex sum (|sum - 2 pi| < 1e-6, the #87 test);
            (b) combinatorially (the sheet is one closed cycle of corners winding once round O). Both must agree.
Share = edges on discs / edges. Centre = mean of the corners (as in the 11-11 census). Float geometry: the registry stores corners
to about 1e-8, so the run is repeated at three tolerances (1e-5, 1e-6, 1e-7) and every solid whose result moves is listed.
Controls: the 11-11 numbers of data/vacuus_census.json are reproduced for all 389 solids at tol 1e-6 (same rule, same file);
#87: octahedron 3 square discs, cube 0, cuboctahedron 4 x 6, icosidodecahedron 6 x 10, dodecahedron 0; Dogstar 0 discs (exact result
of the 13 Nov study). Usage: disc_ranking.py registry-solids.json census-11-11.json out.json"""
import json, sys, math, time, re
from collections import Counter
import numpy as np
T0 = time.time()
PILOT = '--pilot' in sys.argv; sys.argv = [x for x in sys.argv if x != '--pilot']
S = json.load(open(sys.argv[1])); C11 = {c['id']: c for c in json.load(open(sys.argv[2]))}; OUT = sys.argv[3]
if PILOT: S = [s for s in S if s['id'] in ('D8', 'CUBE', 'CUBOCTAHEDRON', 'ICOSIDODECAHEDRON', 'DODECAHEDRON', 'DOGSTAR')] + S[:30]; S = list({s['id']: s for s in S}.values()); C11 = {i: C11[i] for i in (s['id'] for s in S)}
CHECKS = []
def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok))); print(('ok   ' if ok else 'FAIL ') + name + (('  [' + detail + ']') if detail else ''), flush=True)

def edges_of(F):
    E = set()
    for f in F:
        for i in range(len(f)): E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
    return sorted(E)

def census(V, F, tol):
    V = np.array(V, float); V = V - V.mean(0); E = edges_of(F)
    nrm = np.linalg.norm(V, axis=1)
    # ---- rule 11-11 (identical to vacuus_census.py: unit normal rounded to 6 digits, sign fixed)
    planes = {}; through = []
    for a, b in E:
        n = np.cross(V[a], V[b])
        if np.linalg.norm(n) < 1e-9: through.append((a, b)); continue
        n /= np.linalg.norm(n); n = n if n[np.argmax(np.abs(n))] > 0 else -n
        planes.setdefault(tuple(np.round(n, 6)), []).append((a, b))
    d11 = {p: v for p, v in planes.items() if len(v) >= 3}
    on11 = sum(len(v) for v in d11.values())
    # ---- rule #87
    fins = [e for e in E if e not in set(through)]
    pf = list(range(len(fins)))
    def fp(x):
        while pf[x] != x: pf[x] = pf[pf[x]]; x = pf[x]
        return x
    at = {}
    for i, (a, b) in enumerate(fins): at.setdefault(a, []).append(i); at.setdefault(b, []).append(i)
    ambiguous = 0
    for v, l in at.items():
        for ii in range(len(l)):
            for jj in range(ii + 1, len(l)):
                i, j = l[ii], l[jj]
                a = fins[i][0] if fins[i][1] == v else fins[i][1]; b = fins[j][0] if fins[j][1] == v else fins[j][1]
                dt = np.dot(V[v], np.cross(V[a], V[b])) / (nrm[v] * nrm[a] * nrm[b])
                if abs(dt) > tol: continue
                side = np.dot(np.cross(V[v], V[a]), np.cross(V[v], V[b])) / (nrm[v] ** 2 * nrm[a] * nrm[b])
                if abs(side) < 1e-4: ambiguous += 1; continue
                if side < 0: pf[fp(i)] = fp(j)
    comp = {}
    for i in range(len(fins)): comp.setdefault(fp(i), []).append(i)
    discs = []; disagree = 0
    for r, l in comp.items():
        apex = sum(math.acos(max(-1.0, min(1.0, float(np.dot(V[a], V[b]) / (nrm[a] * nrm[b]))))) for a, b in (fins[i] for i in l))
        deg = Counter(x for i in l for x in fins[i])
        closed = len(l) >= 3 and all(d == 2 for d in deg.values())
        if closed:   # one cycle?
            adj = {}
            for i in l:
                a, b = fins[i]; adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
            start = fins[l[0]][0]; seen = {start}; st = [start]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); st.append(y)
            closed = len(seen) == len(deg)
        wind = None
        if closed:   # winding number round O: sum of signed angles in the sheet's plane
            m = np.cross(V[fins[l[0]][0]], V[fins[l[0]][1]]); m /= np.linalg.norm(m)
            cyc = [start]; prev = None; cur = start
            while True:
                nb = adj[cur]; nxt = nb[0] if nb[0] != prev else nb[1]
                if nxt == start: break
                cyc.append(nxt); prev, cur = cur, nxt
            tw = sum(math.atan2(np.dot(np.cross(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]), m), np.dot(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]])) for k in range(len(cyc)))
            wind = round(abs(tw) / (2 * math.pi), 6)
        comb = closed and wind is not None and abs(wind - 1) < 1e-6
        byapex = abs(apex - 2 * math.pi) < 1e-6
        if comb != byapex: disagree += 1
        if comb and byapex: discs.append(len(l))
    on87 = sum(discs)
    return dict(edges=len(E), planes11=len(planes), discs11=len(d11), on11=on11, share11=on11 / max(1, len(E)),
                per_plane11={str(k): v for k, v in sorted(Counter(len(v) for v in planes.values()).items())},
                sheets87=len(comp), discs87=len(discs), disc_sizes87={str(k): v for k, v in sorted(Counter(discs).items())},
                on87=on87, share87=on87 / max(1, len(E)), apex_vs_cycle_disagree=disagree, ambiguous_side=ambiguous, through=len(through))

TOLS = [1e-6, 1e-5, 1e-7]
res = {}
for k, s in enumerate(S):
    r = {t: census(s['V'], s['F'], t) for t in TOLS}
    res[s['id']] = dict(id=s['id'], name=s['name'], **r[1e-6], stable=all(r[t]['discs87'] == r[1e-6]['discs87'] and r[t]['on87'] == r[1e-6]['on87'] for t in TOLS),
                        by_tol={str(t): (r[t]['discs87'], r[t]['on87']) for t in TOLS})
    if (k + 1) % 13 == 0 or k + 1 == len(S):
        print(f'PROGRESS {(k + 1) / len(S):.3f} {s["id"]}: 11-11 {r[1e-6]["discs11"]} discs ({r[1e-6]["share11"]:.0%}); #87 {r[1e-6]["discs87"]} discs ({r[1e-6]["share87"]:.0%}) ({time.time() - T0:.0f} s)', flush=True)

# ---- controls
mism = [i for i, r in res.items() if i in C11 and (r['discs11'] != C11[i]['discs'] or r['on11'] != C11[i]['edges_on_discs'] or r['edges'] != C11[i]['edges'])]
check(f'R1 rule 11-11 reproduces the 11-11 census (discs, edges on discs, edges) for all {len(C11)} solids', not mism and len(C11) == len(S) == (len(S) if PILOT else 389), str(mism[:5]))
want = {'D8': {'4': 3}, 'CUBE': {}, 'CUBOCTAHEDRON': {'6': 4}, 'ICOSIDODECAHEDRON': {'10': 6}, 'DODECAHEDRON': {}}
for i, w in want.items():
    check(f'R2 #87 control {res[i]["name"]}: disc sizes {res[i]["disc_sizes87"]} (expect {w})', res[i]['disc_sizes87'] == w)
check(f'R3 #87 Dogstar: {res["DOGSTAR"]["discs87"]} discs (exact study: 0); 11-11 rule: {res["DOGSTAR"]["discs11"]} planes, {res["DOGSTAR"]["on11"]} of 138 edges (exact study: 15, 114)',
      res['DOGSTAR']['discs87'] == 0 and res['DOGSTAR']['discs11'] == 15 and res['DOGSTAR']['on11'] == 114)
dis = [i for i, r in res.items() if r['apex_vs_cycle_disagree']]
check('R4 #87 apex-sum test and closed-cycle test agree on every sheet of every solid' + (f' (disagree: {dis})' if dis else ''), not dis)
amb = [i for i, r in res.items() if r['ambiguous_side']]
print('note: coplanar fin pairs with an ambiguous side test (|side| < 1e-4), skipped:', {i: res[i]['ambiguous_side'] for i in amb})
unstable = [i for i, r in res.items() if not r['stable']]
check('R5 #87 result unchanged at tolerances 1e-5, 1e-6, 1e-7 for every solid' + (f' (moves: {unstable})' if unstable else ''), not unstable)
check('R6 every #87 disc lies on a plane that the 11-11 rule counts (#87 share <= 11-11 share)', all(r['on87'] <= r['on11'] for r in res.values()))

# ---- ranking
DICTO = lambda r: 'DICTO' in r['id'] or 'DICTO' in r['name'] or re.match('DJ_|DRAGON|DOGSTAR|DODECA_|SEAMED', r['id'])
rows = sorted(res.values(), key=lambda r: (-r['share87'], -r['share11'], r['name']))
print('\nRANK DICTO solids (id or name contains DICTO, the DICTO Jewel family, Dogstar, the Sunstar clusters, the seamed dodecahedron)')
print('RANK name | edges | 11-11: discs, share | #87: discs, share | #87 disc sizes')
for r in rows:
    if DICTO(r): print(f"RANK {r['name']} | {r['edges']} | {r['discs11']}, {r['share11']:.1%} | {r['discs87']}, {r['share87']:.1%} | {r['disc_sizes87']}")
print('\nALL registry solids with a disc under either rule')
for r in rows:
    if r['discs11'] or r['discs87']: print(f"ALL {r['id']} | {r['name']} | {r['edges']} | {r['discs11']}, {r['share11']:.1%} | {r['discs87']}, {r['share87']:.1%} | {r['disc_sizes87']}")
summ = dict(n=len(res), complete11=sum(1 for r in res.values() if r['share11'] == 1), complete87=sum(1 for r in res.values() if r['share87'] == 1),
            nodisc11=sum(1 for r in res.values() if r['discs11'] == 0), nodisc87=sum(1 for r in res.values() if r['discs87'] == 0),
            dicto=sum(1 for r in res.values() if DICTO(r)), dicto_nodisc11=sum(1 for r in res.values() if DICTO(r) and r['discs11'] == 0),
            dicto_nodisc87=sum(1 for r in res.values() if DICTO(r) and r['discs87'] == 0))
print('SUMMARY', summ)
json.dump(dict(summary=summ, solids=rows, checks=CHECKS), open(OUT, 'w'), indent=1)
nf = sum(1 for _, o in CHECKS if not o)
print(f'{len(CHECKS)} checks, {nf} failed, {time.time() - T0:.0f} s')
print('FINAL ok' if nf == 0 else f'FINAL FAIL ({nf} checks)')
