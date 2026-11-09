"""Stage 3 (finding the exact point; the proof is stage 4, which checks everything exactly).
usage: python -u stage3_hensel.py D|K digits
K = Q(y0), y0 = u0^2, minimal polynomial g(y) = f(sqrt y). Take a prime p with g irreducible mod p, so F_q = F_p[y]/(g) is a
field. Solve there  Ec(S) = 0 and Fc = Eb = Ed = 0 (stage 2), dropping solutions where a divisor of the model vanishes; every
non-degenerate solution in F_q is lifted by Newton's method in (Z/p^k)[y]/(g) (square system Ec, Fc, Eb; Ed is checked at the
end), and each unknown z is rebuilt as z = v(y)/g'(y), v in Q[y] of degree < deg g, by rational reconstruction of the
coefficients of z g'(y) mod p^k. This is done at modulus ~10^digits and at ~10^(2 digits); a solution is accepted when both agree.
The solution whose real embedding (y -> y0) matches the stored numerical yantra to 30 digits is the geometric one.
Case D also needs sqrt5 in K: sqrt5 = -A(y)/B(y), from the factor A(y) + w B(y) of g over Q(sqrt5) through y0 (stage 1).
Writes stage3-<case>.json."""
import sys, json, time
import cypari2
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
pari = cypari2.Pari(); pari.allocatemem(20 * 10**9); pari.set_real_precision(400)
case = sys.argv[1]; digits = int(sys.argv[2])
f = pari(open({'D': 'dicto-yantra-exact-u.txt', 'K': 'kulaichev-minpoly-u.txt'}[case]).read().strip().replace('x', 'u'))
g = pari.substpol(f, pari('u^2'), pari('y')); n = int(pari.poldegree(g, 'y')); dg = pari.deriv(g, 'y')
st1 = json.load(open(f'stage1-{case}.json')); y0 = pari(st1['u_1000_digits']) ** 2
st2 = json.load(open(f'stage2-{case}.json'))
stored = {'K': {'t': '0.103270075308203946272572702702691751496327239362942147553129',
                'Q': '0.550705232975448904641094020607886607493801159518652756832912',
                'S': '0.920060145909595975294968707108293454053174101126889036281854'},
          'D': {'t': '0.04397772610421809944376588907842364688956', 'Q': '0.576510321707840427511505969737023869726',
                'S': '0.9682686074586943741422847787587545440601'}}[case]
polys = {k: pari(st2[k]) for k in ('Fc', 'Eb', 'Ec', 'Ed')}
if case == 'D':
    w = pari.varlower('w')
    facs = [pari(l) for l in open('stage1-D-g-over-Qsqrt5.txt').read().split('\n') if l.strip()]
    AB = []
    for F in facs:
        L = pari.lift(pari.Mod(pari.liftall(F), w**2 - 5))
        A_, B_ = pari.polcoef(L, 0, 'w'), pari.polcoef(L, 1, 'w')
        AB.append((A_, B_, abs(pari.subst(A_, 'y', y0) + pari.sqrt(5) * pari.subst(B_, 'y', y0))))
    Ay, By, v0 = min(AB, key=lambda r: r[2])
    say('factor through y0: |value at y0| =', str(pari(f'Strprintf("%.3e", {v0})')), '; other factor:',
        str(pari(f'Strprintf("%.3e", {max(r[2] for r in AB)})')))
    open('stage3-D-sqrt5-AB.txt', 'w').write(str(Ay) + '\n' + str(By) + '\n')
names = ['S', 'Q', 't']
# 1. a prime with g irreducible mod p, and the non-degenerate solutions there
p = pari(2)**61
while True:
    p = pari.nextprime(p + 1)
    gp = g * pari.Mod(1, p)
    if pari.poldegree(gp, 'y') == n and pari.polisirreducible(gp) and all(
            pari.denominator(c) % p != 0 for k in polys for c in pari.Vec(pari.content(polys[k]))): break
a = pari.ffgen(gp, 'a')
pv = (2 * (-pari.subst(Ay, 'y', a) / pari.subst(By, 'y', a)) - 4) if case == 'D' else 0 * a
Pq = {k: pari.subst(pari.subst(v, 'y', a), 'p', pv) for k, v in polys.items()}
DV = [(pari.subst(pari.subst(pari(nm), 'y', a), 'p', pv), pari.subst(pari.subst(pari(dn), 'y', a), 'p', pv)) for nm, dn in st2['divisors']]
ev = lambda e, s: pari.subst(pari.subst(pari.subst(e, 'S', s[0]), 'Q', s[1]), 't', s[2])
sols, ndeg = [], 0
for fac in pari.factor(Pq['Ec'])[0]:
    if pari.poldegree(fac, 'S') != 1: continue
    Sv = -pari.polcoef(fac, 0, 'S') / pari.polcoef(fac, 1, 'S')
    Fc, Eb, Ed = (pari.subst(Pq[k], 'S', Sv) for k in ('Fc', 'Eb', 'Ed'))
    G = pari.gcd(pari.polresultant(Fc, Eb, 't'), pari.polresultant(Fc, Ed, 't'))
    if pari.poldegree(G, 'Q') < 1: continue
    for fq in pari.factor(G)[0]:
        if pari.poldegree(fq, 'Q') != 1: continue
        Qx = -pari.polcoef(fq, 0, 'Q') / pari.polcoef(fq, 1, 'Q')
        Ht = pari.gcd(pari.gcd(pari.subst(Fc, 'Q', Qx), pari.subst(Eb, 'Q', Qx)), pari.subst(Ed, 'Q', Qx))
        for ft in pari.factor(Ht)[0]:
            if pari.poldegree(ft, 't') != 1: continue
            tx = -pari.polcoef(ft, 0, 't') / pari.polcoef(ft, 1, 't')
            s = (Sv, Qx, tx)
            if any(ev(nm, s) == 0 or ev(dn, s) == 0 for nm, dn in DV): ndeg += 1
            else: sols.append(s)
say(f'prime p = {p}: g irreducible mod p; {len(sols)} non-degenerate solutions in F_q ({ndeg} degenerate dropped)')
# 2. Newton lifting (GP code)
pari('''topoly = (z) -> my(P = if (type(z) == "t_FFELT", z.pol, lift(lift(z)))); if (type(P) == "t_POL", subst(P, variable(P), y), P)''')
pari('''invR = (d, gpp, N, gN, p, k) -> my(i = Mod(topoly(1 / Mod(topoly(d) * Mod(1, p), gpp)) * Mod(1, N), gN));
  for (j = 1, ceil(log(k) / log(2)) + 2, i = i * (2 - d * i)); i''')
pari('''lift_one = (g, dg, p, k, F, X0, vars, extra) ->
  my(X, s5 = 0, sub, Fr, Jr, Fv, J, di, N, gN, gpp = g * Mod(1, p), Y, kk = 1, ks = List());
  while (kk < k, kk = min(2 * kk, k); listput(ks, kk));
  N = p; gN = g * Mod(1, N);
  X = vector(3, i, topoly(X0[i]));
  if (#extra, s5 = topoly(extra[1]));
  for (step = 1, #ks,
     N = p^ks[step]; gN = g * Mod(1, N); Y = Mod(Mod(1, N) * y, gN);
     X = vector(3, i, Mod(topoly(X[i]) * Mod(1, N), gN));
     if (#extra, s5 = Mod(topoly(s5) * Mod(1, N), gN); s5 = s5 - (s5^2 - 5) * invR(2 * s5, gpp, N, gN, p, ks[step]));
     sub = ((e) -> if (#extra, subst(subst(e, y, Y), 'p, 2 * s5 - 4), subst(e, y, Y)));
     Fv = vector(3, i, substvec(sub(F[i]), vars, X));
     J = matrix(3, 3, i, j, substvec(sub(deriv(F[i], vars[j])), vars, X));
     di = invR(matdet(J), gpp, N, gN, p, ks[step]);
     X = X - (matadjoint(J) * Fv~)~ * di);
  [X, s5]''')
F = pari.vector(3, [polys['Ec'], polys['Fc'], polys['Eb']])
vars_ = pari('[S, Q, t]')
results = []
for idx, s in enumerate(sols):
    k = digits // 18 + 1
    t1 = time.time()
    extra = pari.vector(1, [(-pari.subst(Ay, 'y', a) / pari.subst(By, 'y', a))]) if case == 'D' else pari.vector(0)
    X, s5 = pari('lift_one')(g, dg, p, k, F, pari.vector(3, list(s)), vars_, extra)
    say(f'solution {idx}: lifted to {digits} digits in {time.time() - t1:.1f} s')
    vals = list(X) + ([s5] if case == 'D' else [])
    Nf = p**k; gNf = g * pari.Mod(1, Nf); Yf = pari.Mod(pari.Mod(1, Nf) * pari('y'), gNf)
    chk = lambda e: pari.substvec(pari.subst(pari.subst(e, 'y', Yf), 'p', (2 * s5 - 4) if case == 'D' else 0), vars_, X)
    say('   residuals mod p^k are zero: ' + ', '.join(f'{nm} {chk(polys[nm]) == 0}' for nm in ('Ec', 'Fc', 'Eb', 'Ed')))
    for nm, z in zip(names, vals):
        for lab, zz in (('z', pari.lift(pari.lift(z))), ("z g'", pari.lift(pari.lift(z * pari.Mod(dg, g))))):
            okk = []
            for frac in (16, 8, 4, 2, 1):
                try: r = pari.bestappr(pari.Mod(1, p**(k // frac)) * zz); okk.append(pari.type(r) in ('t_POL', 't_INT', 't_FRAC'))
                except Exception: okk.append(False)
            say(f'   {nm} as {lab}: reconstruction succeeds at k/16, k/8, k/4, k/2, k: {okk}')
    zs = [pari.lift(pari.lift(z * pari.Mod(dg, g))) for z in vals]   # integer polys: coefficients of z g' mod (g, p^k)
    recs = []; level = None
    for frac in (16, 8, 4, 2, 1):
        kk = k // frac; Nk = p**kk
        rec = []
        for zz in zs:
            try: r = pari.bestappr(pari.Mod(1, Nk) * zz); rec.append(r if pari.type(r) in ('t_POL', 't_INT', 't_FRAC') else None)
            except Exception: rec.append(None)
        recs.append(rec)
        if len(recs) >= 2 and all(r1 is not None and r1 == r2 for r1, r2 in zip(recs[-2], recs[-1])):
            level = kk * 18; break
    say(f'solution {idx}: stable reconstruction from {level} digits on' if level else f'solution {idx}: no stable reconstruction up to {digits} digits')
    recs = recs[-2:]
    agree = level is not None
    rec = recs[1]
    emb = {}
    for k_, z in zip(names + (['w'] if case == 'D' else []), rec):
        emb[k_] = pari.subst(z, 'y', y0) / pari.subst(dg, 'y', y0) if z is not None and pari.type(z) == 't_POL' else None
    match = agree and all(emb[k_] is not None and abs(emb[k_] - pari(stored[k_])) < pari('1e-30') for k_ in names)
    size = max(len(str(abs(pari.numerator(c)))) + len(str(pari.denominator(c))) for z in rec if z is not None and pari.type(z) == 't_POL' for c in pari.Vec(z)) if agree else -1
    say(f'solution {idx}: reconstructions at both precisions agree: {agree}; largest coefficient {size} digits; real embedding ' +
        ', '.join(f'{k_} = {str(pari(f"Strprintf(\"%.20f\", {emb[k_]})")) if emb[k_] is not None else "?"}' for k_ in emb) +
        f'; matches the stored yantra: {match}')
    results.append({'agree': bool(agree), 'geometric': bool(match), 'v': {k_: str(z) for k_, z in zip(emb, rec)}})
geo = [r for r in results if r['geometric']]
json.dump({'case': case, 'prime': str(p), 'digits': digits, 'solutions': results}, open(f'stage3-{case}.json', 'w'))
print('FINAL ok' if len(geo) == 1 else f'FINAL FAIL: {len(geo)} reconstructed solutions match the stored yantra')
