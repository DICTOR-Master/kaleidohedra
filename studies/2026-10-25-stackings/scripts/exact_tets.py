# Follow-up to exact_halves.py: count failures by kind, and for tetrahedral sites test the alternatives exactly:
#  (A) whole piece = pure piece of the layer it sits on (the first guess), (B) of the other layer of its gap,
#  (C) split at the site's own height: each part congruent to the same part of a pure piece (cubic/hexagonal by side),
#  (D) split at the mid-plane of the gap (the octahedral site's height), parts as in (C).
exec(open('exact_halves.py').read().split('lams = ')[0])
def parts(c, lam, z):
    return tuple(fp(c.net.G, half(c, lam, z, True))), tuple(fp(c.net.G, half(c, lam, z, False)))
def ref_parts(t, lam, which):
    net, spec = REF[t]; out = {'up': set(), 'dn': set()}
    for i, (k, p) in enumerate(spec['motif']):
        if k != 'tet': continue
        c = cell(net, i, lam)
        if c is None: continue
        g = i // 3; z = Fr(p[2]) if which == 'own' else Fr(spec['motif'][3 * g][1][2])
        u, d = parts(c, lam, z); out['up'].add(u); out['dn'].add(d)
    return out
lams = [Fr(-7, 16), Fr(-1, 4), Fr(-1, 16), Fr(1, 300), Fr(1, 10), Fr(1, 4), Fr(1, 3)]
tally = {}; oct_bad = 0
for hc in itertools.product('hc', repeat=4):
    hc = ''.join(hc); word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word)
    for lam in lams:
        R = {t: ref_fps(t, lam) for t in 'hc'}; RP = {(t, w): ref_parts(t, lam, w) for t in 'hc' for w in ('own', 'mid')}
        g = 2
        for j in range(3):
            i = 3 * g + j; k, p = spec['motif'][i]; c = cell(net, i, lam)
            if c is None: continue
            if k == 'oct':
                u = tuple(fp(net.G, half(c, lam, Fr(p[2]), True))); d = tuple(fp(net.G, half(c, lam, Fr(p[2]), False)))
                up_t, dn_t = T[(g + 1) % n], T[g % n]
                oct_bad += not ((u in R[up_t]['oct_up'] or u in R[up_t]['oct_dn']) and (d in R[dn_t]['oct_dn'] or d in R[dn_t]['oct_up']))
                continue
            lay = g if j == 1 else g + 1; other = g + 1 if j == 1 else g; whole = tuple(fp(net.G, corners_at(c, lam)))
            res = {'A own layer': whole in R[T[lay % n]]['tet'], 'B other layer': whole in R[T[other % n]]['tet']}
            for w, z in (('own', Fr(p[2])), ('mid', Fr(spec['motif'][3 * g][1][2]))):
                u, d = parts(c, lam, z)
                # upper part decided by the layer above (g+1), lower part by the layer below (g)
                res[f'{"C" if w == "own" else "D"} split at {w} height'] = (u in RP[(T[(g + 1) % n], w)]['up']) and (d in RP[(T[g % n], w)]['dn'])
            for key, v in res.items(): tally.setdefault(key, [0, 0]); tally[key][0 if v else 1] += 1
print(f'octahedral sites failing the half rule: {oct_bad}')
for key, (a, b) in sorted(tally.items()): print(f'tetrahedral sites, rule {key}: {a} hold, {b} fail')
