"""Non-convex rule for #87 discs (13 Nov 2026; Platonic book Ch 4 open item, follow-up to fans_law.py).
RULE (Theorem N of the README). Let G(P) be the FIN GRAPH of a central plane P: the edges of the solid that lie in P and whose line
misses the centre O (edges pointing at O are left out). P holds a #87 disc exactly when some connected piece of G(P) is a simple
closed loop that goes once round O, every side turning the same way round O. The disc is that piece.
This script tests the rule against the #87 definition AS fans_law.py IMPLEMENTS IT (its analyse() is exec'd unchanged, only two
fields are exported: the sheets and the exact corners), plane by plane and sheet by sheet, exact, on every registry solid recognised
exactly (91 of 389), and in floats on all 389 against the float census (disc-ranking.json, disc_sizes87).
It also tests the relaxed rule R0 (a loop round O as above exists among the fins of P, extra fins at its corners allowed), the convex
corollary (rule <=> P cuts no face), and tallies which clause of the rule decides each plane without a disc.
Usage: fans_nonconvex.py registry-solids.json disc-ranking.json out.json [--pilot]"""
import sys, os, json, math, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
PILOT_ = '--pilot' in sys.argv; args = [a for a in sys.argv[1:] if a != '--pilot']
REG, DR, OUT_ = args
src = open(os.path.join(HERE, 'fans_law.py')).read()
head = src.split('\nres = []')[0]
INJ = "    R['apex_agree'] ="
assert head.count(INJ) == 1
head = head.replace(INJ, "    R['_sheets'] = sheets; R['_V'] = V; R['_Vf'] = Vf; R['_E'] = E; R['_F'] = F; R['_through'] = through\n" + INJ)
sys.argv = [sys.argv[0], REG, DR, '/dev/null']
exec(head, globals()); PILOT = PILOT_  # defines recog_solid, analyse, check, CHECKS, S (all 389), FLOAT, helpers; T0
T0 = time.time()
PIL = NAMED + ['DODECA_TETRAHEDRAL_CLUSTER', 'DICTO_EDGE_ROOF', 'DJ_TETRAHEDRAL_CLUSTER', 'STELLA_OCTANGULA', 'DICTO_HEXA']
if PILOT: S = [s for s in S if s['id'] in PIL]

# ------------------------------------------------------------------ the rule, exact
def fin_graph_rule(fins, V, m):
    """fins: in-plane edges of P not through O (exact). Returns (R1 loops, R0 flag, per-piece info).
    R1: pieces of the fin graph that are simple loops, monotone, winding +-1. R0: a monotone winding-1 loop exists at all."""
    adj = {}
    for a, b in fins: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen = set(); pieces = []
    for s0 in adj:
        if s0 in seen: continue
        st = [s0]; seen.add(s0); cs = [s0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y); cs.append(y)
        cset = set(cs); pe = [e for e in fins if e[0] in cset]
        pieces.append((cs, pe))
    loops = []; info = []
    for cs, pe in pieces:
        simple = len(pe) >= 3 and len(pe) == len(cs) and all(len(adj[x]) == 2 for x in cs)
        w = mono = None; usum = None
        if simple:
            cyc = [cs[0]]; prev = None; cur = cs[0]
            while True:
                nb = adj[cur]; nxt = nb[0] if nb[0] != prev else nb[1]
                if nxt == cs[0]: break
                cyc.append(nxt); prev, cur = cur, nxt
            ors = [sgn(dv(cr(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]), m)) for k in range(len(cyc))]
            mono = len(set(ors)) == 1 and 0 not in ors; w = 0
            if not mono:     # the half-open count below is a winding number only for a loop turning one way; report the float one instead
                w = round(sum(math.atan2(sum(float(c_) for c_ in [dv(cr(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]), m)]) / math.sqrt(sum(float(x) ** 2 for x in m)),
                                         float(dv(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]))) for k in range(len(cyc))) / (2 * math.pi))
            # winding: half-open ray through cyc[0], each side counted with its turning sense (independent of the sheet code's loop)
            rr = V[cyc[0]]
            for k in (range(len(cyc)) if mono else ()):
                a, b = V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]; o = ors[k]
                on = iszero(cr(a, rr)) and dv(a, rr).sign() > 0
                if on or (sgn(dv(cr(a, rr), m)) == o and sgn(dv(cr(rr, b), m)) == o): w += o
            usum = sum(ang(a, b) for a, b in pe)
        info.append(dict(edges=len(pe), simple_loop=simple, winding=w, monotone=mono, apex_sum_over_2pi=None if usum is None else usum / (2 * math.pi)))
        if simple and mono and abs(w) == 1: loops.append(frozenset(pe))
    # R0: directed graph, each fin oriented to turn positively round O (normal m); a winding-1 directed loop exists iff for some
    # crossing side u->w (half-open sector [u, w) holds the ray) w reaches u by non-crossing sides.
    r0 = False
    if fins:
        rr = V[fins[0][0]]; out = {}; cross_e = []
        for a, b in fins:
            u, v_ = (a, b) if sgn(dv(cr(V[a], V[b]), m)) > 0 else (b, a)
            on = iszero(cr(V[u], rr)) and dv(V[u], rr).sign() > 0
            if on or (sgn(dv(cr(V[u], rr), m)) > 0 and sgn(dv(cr(rr, V[v_]), m)) > 0): cross_e.append((u, v_))
            else: out.setdefault(u, []).append(v_)
        for u, v_ in cross_e:
            st = [v_]; sn = {v_}
            while st and not r0:
                x = st.pop()
                if x == u: r0 = True; break
                for y in out.get(x, []):
                    if y not in sn: sn.add(y); st.append(y)
            if r0: break
    return loops, r0, info

VFL = {}
def ang(a, b):
    a, b = VFL[a], VFL[b]
    return math.acos(max(-1.0, min(1.0, sum(a[k] * b[k] for k in range(3)) / math.sqrt(sum(x * x for x in a) * sum(x * x for x in b)))))

# ------------------------------------------------------------------ the rule, floats (all 389 solids)
import numpy as np
def float_rule(Vin, Fin):
    V = np.array(Vin, float); V = V - V.mean(0); E = edges_of(Fin)
    planes = {}
    for a, b in E:
        n_ = np.cross(V[a], V[b])
        if np.linalg.norm(n_) < 1e-9: continue
        n_ /= np.linalg.norm(n_); n_ = n_ if n_[next(i for i in range(3) if abs(n_[i]) > 1e-6)] > 0 else -n_   # first non-zero entry positive
        planes.setdefault(tuple(np.round(n_, 6)), []).append((a, b))
    sizes = Counter()
    for pk, fins in planes.items():
        adj = {}
        for a, b in fins: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        seen = set()
        for s0 in adj:
            if s0 in seen: continue
            st = [s0]; seen.add(s0); cs = [s0]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); st.append(y); cs.append(y)
            cset = set(cs); pe = [e for e in fins if e[0] in cset]
            if not (len(pe) >= 3 and len(pe) == len(cs) and all(len(adj[x]) == 2 for x in cs)): continue
            cyc = [cs[0]]; prev = None; cur = cs[0]
            while True:
                nb = adj[cur]; nxt = nb[0] if nb[0] != prev else nb[1]
                if nxt == cs[0]: break
                cyc.append(nxt); prev, cur = cur, nxt
            m = np.cross(V[pe[0][0]], V[pe[0][1]]); m = m / np.linalg.norm(m)   # unrounded normal, as in the float census
            t = [math.atan2(float(np.dot(np.cross(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]), m)), float(np.dot(V[cyc[k]], V[cyc[(k + 1) % len(cyc)]]))) for k in range(len(cyc))]
            if (all(x > 1e-9 for x in t) or all(x < -1e-9 for x in t)) and abs(abs(sum(t)) - 2 * math.pi) < 1e-6: sizes[len(pe)] += 1
    return {str(k): v for k, v in sorted(sizes.items())}

# ------------------------------------------------------------------ run
rows = []; fl_bad = []; tallies = Counter(); r0_extra = []; ce_rows = []
for k, s in enumerate(S):
    fr = float_rule(s['V'], s['F'])
    if fr != FLOAT[s['id']]['disc_sizes87']: fl_bad.append((s['id'], fr, FLOAT[s['id']]['disc_sizes87']))
    R = analyse(s)
    if not R['recognised']:
        rows.append(dict(id=s['id'], recognised=False, float_rule=fr)); continue
    V = R['_V']; VFL.clear(); VFL.update(enumerate(R['_Vf'])); E = R['_E']; F = R['_F']; through = R['_through']
    byp = {}
    for sh in R['_sheets']: byp.setdefault(sh['plane'], []).append(sh)
    finsby = {}
    for e in E:
        if e in through: continue
        finsby.setdefault(key(cr(V[e[0]], V[e[1]])), []).append(e)
    assert set(finsby) == set(byp)
    n = len(V); prow = []
    for pk, shs in byp.items():
        fins = finsby[pk]
        assert sorted(fins) == sorted(e for sh in shs for e in sh['fins'])
        loops, r0, info = fin_graph_rule(fins, V, pk)
        defd = {frozenset(sh['fins']) for sh in shs if sh['disc']}
        nf = tuple(float(x) for x in pk)
        sv = [fsgn(pk, nf, V[i], R['_Vf'][i]) for i in range(n)]
        cut = sum(1 for f in F if any(sv[x] > 0 for x in f) and any(sv[x] < 0 for x in f))
        inface = sum(1 for f in F if all(sv[x] == 0 for x in f))
        radial = sum(1 for e in through if sv[e[0]] == 0 and sv[e[1]] == 0)
        # which clause decides a plane without a disc
        if defd: why = 'disc'
        elif r0: why = 'loop round O exists but a third fin meets one of its corners'
        elif any(i['simple_loop'] and (i['winding'] == 0 or not i['monotone']) for i in info): why = 'a loop of fins that does not go once round O (winding 0 or turning back)'
        elif radial and cut == 0 and inface == 0: why = 'section of edges only, but broken by edges pointing at O'
        else: why = 'no loop of fins (open fans only)'
        tallies[(R['convex'], why)] += 1
        p = dict(plane=[round(x, 6) for x in nf], fins=len(fins), radial_in_plane=radial, cut_faces=cut, faces_in_plane=inface,
                 def_discs=sorted(len(d) for d in defd), rule_discs=sorted(len(d) for d in loops), rule_equal=set(loops) == defd,
                 r0=r0, r0_equal=r0 == bool(defd), edge_closed=cut == 0 and inface == 0, why=why, pieces=info)
        prow.append(p)
        if r0 != bool(defd): r0_extra.append((s['id'], p['plane']))
        if R['convex'] is False and (bool(defd) != p['edge_closed']): ce_rows.append((s['id'], s['name'], p))
    rows.append(dict(id=s['id'], name=s['name'], recognised=True, convex=R['convex'], field=R['field'], float_rule=fr, planes=prow))
    if (k + 1) % 13 == 0 or k + 1 == len(S) or PILOT:
        print(f"PROGRESS {(k + 1) / len(S):.3f} {s['id']}: {len(prow)} planes, discs {sum(len(p['def_discs']) for p in prow)} ({time.time() - T0:.0f} s)", flush=True)

rec = [r for r in rows if r['recognised']]
cv = [r for r in rec if r['convex']]; nc = [r for r in rec if r['convex'] is False]
npl_c = sum(len(r['planes']) for r in cv); npl_n = sum(len(r['planes']) for r in nc)
bad = [(r['id'], p['plane']) for r in rec for p in r['planes'] if not p['rule_equal']]
check(f'N1 RULE = #87 definition, disc for disc (same edge sets), on every plane of all {len(rec)} exactly recognised solids: convex {len(cv)} solids {npl_c} planes, non-convex {len(nc)} solids {npl_n} planes', not bad, str(bad[:5]))
bad = [(r['id'], p['plane']) for r in cv for p in r['planes'] if (len(p['rule_discs']) > 0) != p['edge_closed']]
check('N2 COROLLARY, convex: rule <=> plane cuts no face (and holds no face)', not bad, str(bad[:5]))
bad = [(r['id'], p['plane']) for r in rec for p in r['planes'] if p['def_discs'] and not p['r0']]
check('N3 every disc plane has a loop round O among its fins (relaxed rule R0 is necessary)', not bad, str(bad[:5]))
check('N3b (finding) planes where R0 holds but there is no disc: a third fin meets a corner of the loop (the clause is needed)', True, f'{len(r0_extra)} planes: {r0_extra}')
bad = [(r['id'], p['plane']) for r in rec for p in r['planes'] for i in p['pieces'] if i['simple_loop'] and i['monotone'] and abs(i['winding']) == 1 and abs(i['apex_sum_over_2pi'] - 1) > 1e-9]
check('N4 every loop the rule accepts has apex angles summing to 2 pi (float)', not bad, str(bad[:5]))
bad = [(r['id'], p['plane']) for r in rec for p in r['planes'] for i in p['pieces'] if i['simple_loop'] and not (i['monotone'] and abs(i['winding']) == 1) and abs(i['apex_sum_over_2pi'] - 1) < 1e-9]
check('N5 (finding) loops of fins with apex sum 2 pi that the rule rejects (sum alone not enough)', True, f'{len(bad)} such loops: {bad[:5]}')
check(f'N6 float rule = float census disc sizes on all {len(S)} registry solids', not fl_bad, str(fl_bad[:5]))
if not PILOT:
    check('N7 plane totals as in fans-law.json: convex 1390, non-convex 2914', npl_c == 1390 and npl_n == 2914, f'{npl_c}, {npl_n}')
    check('N8 the 20 old exceptions reproduced (11 edge-closed without disc, 9 discs in planes that cut faces)',
          sum(1 for _, _, p in ce_rows if p['edge_closed']) == 11 and sum(1 for _, _, p in ce_rows if not p['edge_closed']) == 9, str(len(ce_rows)))
print()
for (cvx, why), c in sorted(tallies.items(), key=lambda t: (str(t[0][0]), -t[1])): print(f'CLAUSE convex={cvx} | {why} | {c} planes')
for i, nm, p in ce_rows:
    print(f"OLDEXC {i} | {nm} | plane {p['plane']} | def {p['def_discs']} rule {p['rule_discs']} | cut {p['cut_faces']} radial {p['radial_in_plane']} | {p['why']} | pieces {[(x['edges'], x['simple_loop'], x['winding'], x['monotone']) for x in p['pieces']]}")
json.dump(dict(rows=rows, checks=CHECKS, tallies={f'{a}|{b}': c for (a, b), c in tallies.items()}), open(OUT_, "w"), indent=1, default=str)
nfail = sum(1 for _, o in CHECKS if not o)
print(f'{len(CHECKS)} checks, {nfail} failed, {time.time() - T0:.0f} s')
print('FINAL ok' if nfail == 0 else f'FINAL FAIL ({nfail} checks)')
