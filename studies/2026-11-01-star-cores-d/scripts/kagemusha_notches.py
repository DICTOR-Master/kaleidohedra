# Star Cores paper D, follow-up (2026-11-01): is Kagemusha's growth the valley law at its reflex edges (the notches)?
# Part 1 (exact, sympy over Q(sqrt5)): every edge of Kagemusha (D86): interior dihedral delta, notch angle 360 - delta at the reflex
#   edges, alpha and alpha' (tan alpha = d / rho, valley_law.py's definitions), alpha + alpha' = delta checked; predicted beta_k (k = 1-3)
#   at t = 2 and phi. The same reflex-edge check for the other six eccentric pieces.
# Part 2 (float64, the valley rule of star_valley.py rebuilt): Kagemusha steps 1-3 at t = 2 and phi, every spike's volume attributed to
#   its site: step 1 = its face (notch face = next to a reflex edge, or other); steps 2-3 = the valley of the solid's edge e whose two ends
#   lie in the triangle (reflex or convex edge), else a ridge triangle of a notch face or of another face. Also the opening at every
#   reflex edge after each step, full / cut-back / flat spike counts per site, and the check sum(spike volumes) = volume gained.
# Usage: kagemusha_notches.py <dataset dir> <star-cores.json> <out dir>
import json, os, sys, math, numpy as np, sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-10-30-star-cores/scripts'))
import valley_law as L
from star_core import faces_info, polyvol, vol, load
from star_valley import clash, geo
DS, SC, OUT = sys.argv[1:4]; phi = L.phi; TAU = 2 * math.pi
PIECES = ['D77', 'D80', 'D82', 'D6', 'D71', 'D81', 'D86']
s5 = sp.sqrt(5)
def exactV(d): return [sp.Matrix([sp.sympify(x, locals={'sqrt': sp.sqrt}) for x in v['exact']]) for v in d['vertices']]

def reflex_edges(V, F):
    FI = faces_info(V, F); E = {}
    for i, (f, n, c) in enumerate(FI):
        for k in range(len(f)):
            a, b = f[k], f[(k + 1) % len(f)]; E.setdefault(tuple(sorted((a, b))), []).append((i, a, b, n))
    out = []
    for e, ((i, a, b, n1), (j, _, _, n2)) in E.items():
        s = np.cross(n1, n2) @ (V[b] - V[a])     # face i runs a->b (ccw outward): s > 0 convex, s < 0 reflex
        dih = math.pi - math.acos(np.clip(n1 @ n2, -1, 1)); dih = dih if s > 0 else TAU - dih
        out.append((e, i, j, math.degrees(dih), s < -1e-12))
    return out

def part1():
    sc = {r['D']: r for r in json.load(open(SC))}; res = {}
    for D in PIECES:
        d, V, F = load(sc[D]['file']); V = V - V.mean(0); R = reflex_edges(V, F)
        res[D] = dict(name=sc[D]['name'], convex_flag=d.get('convex'), edges=len(R), reflex=[dict(e=list(e), dihedral=x) for e, i, j, x, r in R if r],
                      min_dihedral=min(x for *_, x, r in R))
    # exact, Kagemusha
    d, V, F = load(sc['D86']['file']); X = exactV(d); c = sum(X, sp.zeros(3, 1)) / len(X); X = [x - c for x in X]
    Vf = np.array([[float(t) for t in x] for x in X]); assert np.abs(Vf - (V - V.mean(0))).max() < 1e-12
    E = L.edges(Vf, F); refl = {tuple(r['e']) for r in res['D86']['reflex']}
    classes = {}
    for e, Lst in E.items():
        rows = []
        for (fi, al, dd, rho, n) in Lst:
            f = F[fi]; P = [X[v] for v in f]; N = (P[1] - P[0]).cross(P[2] - P[0]); N = N / sp.sqrt(N.dot(N))
            D_ = sp.nsimplify(sp.simplify(N.dot(P[0])))                     # plane distance from the centre
            a, b = X[e[0]], X[e[1]]; u = (b - a) / sp.sqrt((b - a).dot(b - a)); cm = sum(P, sp.zeros(3, 1)) / 3
            w = (cm - a) - (cm - a).dot(u) * u; w = w / sp.sqrt(w.dot(w)); Rho = sp.simplify((D_ * N - a).dot(w))
            rows.append((sp.radsimp(sp.simplify(D_ / Rho)), D_, Rho, N))
        cosint = sp.radsimp(sp.simplify(-rows[0][3].dot(rows[1][3])))          # cos of the dihedral (convex reading)
        key = (e in refl, round(float(math.degrees(E[e][0][1])), 6), round(float(math.degrees(E[e][1][1])), 6))
        key = (key[0],) + tuple(sorted(key[1:]))
        if key in classes: classes[key]['count'] += 1; continue
        ta = sorted([r[0] for r in rows], key=lambda z: float(sp.atan(z) % sp.pi))
        al = [float(sp.atan2(r[1], r[2])) for r in rows]; delta = sum(al)
        dint = math.degrees(math.pi - math.acos(float(-cosint))) if e not in refl else 360 - math.degrees(math.pi - math.acos(float(-cosint)))
        pred = {}
        for tn, t in (('2', 2.0), ('phi', phi)):
            b, bb = TAU - delta, []
            for k in range(1, 4):
                b -= sum(math.atan2((t - 1) ** k * float(r[1]), float(r[2])) for r in rows); bb.append(math.degrees(b))
            pred[tn] = bb
        classes[key] = dict(count=1, reflex=e in refl, cos_dihedral_convex_reading=str(cosint), tan_alpha=[str(z) for z in ta],
                            alpha_deg=sorted(math.degrees(a) for a in al), delta_deg=math.degrees(delta), dihedral_from_normals=dint,
                            notch_deg=360 - math.degrees(delta) if e in refl else None, rho_signs=[int(sp.sign(r[2])) for r in rows],
                            beta_deg=pred)
    res['D86_exact'] = list(classes.values())
    return res

def part2(t):
    sc = {r['D']: r for r in json.load(open(SC))}
    d, V, F = load(sc['D86']['file']); V = V - V.mean(0); n0 = len(V); F0 = [list(f) for f in F]
    R = reflex_edges(V, F); refl = [e for e, i, j, x, r in R if r]; notchface = {i for e, i, j, x, r in R if r} | {j for e, i, j, x, r in R if r}
    alle = [e for e, *_ in R]; FI0 = faces_info(V, F)
    inward = {e: -(FI0[i][1] + FI0[j][1]) / np.linalg.norm(FI0[i][1] + FI0[j][1]) for e, i, j, x, r in R}
    anc = list(range(len(F)))
    ecls = {e: 'alpha %.2f/%.2f' % tuple(sorted(math.degrees(x[1]) for x in Lst)) for e, Lst in L.edges(V, F).items()}
    old = [np.vstack([V[f], np.zeros(3)]) for f in F]; OG = [geo(Q) for Q in old]; below = list(old); VOL0 = polyvol(V, F); VOLS = [VOL0]
    steps = []
    for k in range(1, 4):
        FI = faces_info(V, F); base = []
        for (f, n, c), Pc in zip(FI, below):
            h = (Pc - V[f[0]]) @ n; A = Pc[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
        spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
        def free_old(i, s):
            Q = spike(i, s); g = geo(Q); return not any(clash(Q, g, Pq, G) for Pq, G in zip(old, OG))
        S = []
        for i in range(len(base)):
            if free_old(i, t): S.append(t); continue
            lo, hi = 1.0, t
            for _ in range(30):
                mid = (lo + hi) / 2
                if free_old(i, mid): lo = mid
                else: hi = mid
            S.append(lo)
        for _ in range(12):
            Qs = [spike(i, s) for i, s in enumerate(S)]; Gs = [geo(Q) if s > 1 + 1e-9 else None for Q, s in zip(Qs, S)]
            pairs = [(i, j) for i in range(len(S)) for j in range(i + 1, len(S)) if Gs[i] and Gs[j] and clash(Qs[i], Gs[i], Qs[j], Gs[j])]
            if not pairs: break
            for i, j in pairs:
                lo, hi = 1.0, min(S[i], S[j])
                for _ in range(30):
                    mid = (lo + hi) / 2; A_, B_ = spike(i, min(S[i], mid)), spike(j, min(S[j], mid))
                    if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                    else: lo = mid
                S[i] = min(S[i], lo); S[j] = min(S[j], lo)
        if k == 1:                                      # why the notch faces stay flat: which old pieces their spike meets
            why = {}
            for i in sorted(notchface)[:2]:
                for s_ in (1 + 1e-6, 1 + (t - 1) / 4, 1 + (t - 1) / 2, t):
                    Q = spike(i, s_); g = geo(Q)
                    why.setdefault(str(i), []).append(dict(frac=(s_ - 1) / (t - 1), clashes=[('own' if j == i else 'mirror notch face' if j in notchface else 'other') + ' %d' % j
                                                            for j, (Pq, G) in enumerate(zip(old, OG)) if clash(Q, g, Pq, G)],
                                                       tip_angle_from_face_deg=None))
        site = []
        for i, (f, A, foot) in enumerate(base):
            if k == 1: site.append('notch face' if i in notchface else 'other face'); continue
            if any(sorted(f) == sorted(g) for g in F0): site.append('notch face, still flat' if anc[i] in notchface else 'face, still flat'); continue
            es = [e for e in alle if e[0] in f and e[1] in f]
            if es: site.append('valley, reflex edge' if es[0] in refl else 'valley, convex edge ' + ecls[es[0]])
            else: site.append('ridge, notch face' if anc[i] in notchface else 'ridge, other face')
        V2 = list(V); F2 = []; B2 = []; A2 = []; acc = {}
        for i, (f, A, foot) in enumerate(base):
            fr = (S[i] - 1) / (t - 1); a_ = acc.setdefault(site[i], dict(spikes=0, full=0, cut=0, flat=0, volume=0.0))
            a_['spikes'] += 1; a_['full' if fr > 1 - 1e-9 else 'flat' if fr < 1e-9 else 'cut'] += 1
            if S[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); A2.append(anc[i]); continue
            tip = A + S[i] * (foot - A); ti = len(V2); V2.append(tip); Q = np.vstack([V[f], tip]); old.append(Q); OG.append(geo(Q))
            a_['volume'] += vol(Q)
            for a in range(len(f)): F2.append([f[a], f[(a + 1) % len(f)], ti]); B2.append(Q); A2.append(anc[i])
        V2 = np.array(V2); VOL = polyvol(V2, F2)
        opn = []
        for e in refl:
            xs = [V2[[v for v in g if v not in e][0]] for g in F2 if e[0] in g and e[1] in g]
            opn.append(math.degrees(L.opening(V2, e[0], e[1], xs[0], xs[1], inward[e])))
        gained = VOL - VOLS[-1]
        steps.append(dict(step=k, volume_over_last=VOL / VOLS[-1], volume_over_solid=VOL / VOL0, gained=gained,
                          spikes_sum=sum(a['volume'] for a in acc.values()), sites=acc,
                          share={s: a['volume'] / gained for s, a in acc.items()} if gained > 1e-12 else {},
                          reflex_opening_deg=sorted(set(round(x, 6) for x in opn)), **({'notch_flat_why': why} if k == 1 else {})))
        V, F, below, anc = V2, F2, B2, A2; VOLS.append(VOL)
    return dict(t='phi' if t == phi else '2', steps=steps, reflex_edges=[list(e) for e in refl], notch_faces=sorted(notchface))

if __name__ == '__main__':
    out = dict(part1=part1(), part2=[part2(2.0), part2(phi)])
    json.dump(out, open(os.path.join(OUT, 'kagemusha-notches.json'), 'w'), indent=1, default=float)
    p1 = out['part1']
    for D in PIECES: print(D, p1[D]['name'], 'convex flag', p1[D]['convex_flag'], 'reflex edges', len(p1[D]['reflex']), 'min dihedral %.3f' % p1[D]['min_dihedral'])
    for c in p1['D86_exact']: print(c)
    for r in out['part2']:
        for s in r['steps']:
            print(r['t'], 'step', s['step'], 'vol x%.4f' % s['volume_over_last'], 'gained %.5f sum %.5f' % (s['gained'], s['spikes_sum']), 'reflex opening', s['reflex_opening_deg'])
            if 'notch_flat_why' in s: print('   why flat', s['notch_flat_why'])
            for k_, a in s['sites'].items(): print('   ', k_, a, 'share %.3f' % s['share'].get(k_, 0))
