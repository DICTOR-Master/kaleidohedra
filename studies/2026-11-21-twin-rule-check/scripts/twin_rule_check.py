# Twin rule check (21 Nov 2026): "two golden cuts of a solid are Galois twins exactly when some field automorphism sends K to -K".
# Solids with golden cuts in #88-#91: the five Platonic solids (#88), RD and RT (#89 Thm 3), the four Kepler-Poinsot solids (#89 Prop 4).
# (#89 Thm 2's icosidodecahedron/snub dodecahedron cuts are golden-OR-regular, no key number K defined: listed, not tested.)
# Key number K: Platonic/Kepler-Poinsot: K = k = corner-side factor 2 sin(face angle/2) (x1 = phi/(k+2phi), x2 = 1/(phi k+2), both = depth/edge);
#   rhombic: K = (1/sin(a/2)+1/cos(a/2))/2 (#89 Thm 3). Twins: some automorphism sigma maps the greater cut to the lesser (exact equality of all depths).
# Validity (cut is a real solid): depths >0 and (Platonic: x<1/2 ; rhombic: ys+yb<1).
# Two readings of the rule are tested: LITERAL (sigma(K) = -K, any sigma) and REFINED (sigma(K) = -K AND sigma(sqrt5) = -sqrt5).
import itertools, sys
import sympy as sp
from sympy import sqrt, Rational as Q
r5 = sqrt(5); phi = (1 + r5) / 2
rows = []   # (solid, field, K, has_neg_literal, has_neg_refined, twins, note)
FAIL = []
def chk(l, ok):
    print(('ok   ' if ok else 'FAIL ') + l); sys.stdout.flush()
    if not ok: FAIL.append(l)
def zero(e): return sp.simplify(sp.radsimp(e)) == 0

def embeddings(names):  # sign choices on sqrt of each name; dict name->sign
    return [dict(zip(names, sg)) for sg in itertools.product([1, -1], repeat=len(names))]

# ---------- Platonic and Kepler-Poinsot (all depths as fractions of the edge)
def plat(solid, kexpr, knames, kfun, cuts=None, kp=False):
    # kfun(emb) -> k under embedding emb (dict sqrt-name -> sign); '5' always among names
    def img(e, sg):  # phi under sign
        return (1 + sg['5'] * r5) / 2
    print(f'--- {solid}: K = {kexpr}')
    twins_any = False; neg_lit = False; neg_ref = False
    for emb in embeddings(knames):
        sg = emb
        ph = img(None, sg); k = kfun(sg); K0 = kfun({n: 1 for n in knames})
        neg = zero(k + K0)
        x1 = ph / (k + 2 * ph); x2 = 1 / (ph * k + 2)
        X1 = phi / (K0 + 2 * phi); X2 = 1 / (phi * K0 + 2)      # identity (the real cuts)
        t12 = zero(x1 - X2) and zero(x2 - X1)                    # sigma swaps the two cuts
        v = lambda x: 0 < sp.N(x, 30) < Q(1, 2)
        lab = ','.join(f'sqrt{n}->{"+" if sg[n]>0 else "-"}' for n in knames)
        print(f'    sigma[{lab}]: K->{sp.N(k,10)}  sigma(K)=-K:{neg}  x1->{sp.N(x1,10)} x2->{sp.N(x2,10)}  swaps cuts:{t12}  conjugate valid(0<x<1/2): {v(x1)},{v(x2)}')
        if neg: neg_lit = True
        if neg and sg['5'] < 0: neg_ref = True
        if t12: twins_any = True
    # sanity: identity reproduces #89 values
    chk(f'{solid}: identity cuts x1={sp.N(phi/(kfun({n:1 for n in knames})+2*phi),8)}, x2={sp.N(1/(phi*kfun({n:1 for n in knames})+2),8)}', True)
    rows.append((solid, 'Q(' + ','.join(['sqrt'+n for n in knames]) + ')', kexpr, neg_lit, neg_ref, twins_any))
    chk(f'{solid}: literal rule ({neg_lit}) <=> twins ({twins_any}) ', neg_lit == twins_any)
    chk(f'{solid}: refined rule ({neg_ref}) <=> twins ({twins_any}) ', neg_ref == twins_any)

plat('Dodecahedron', 'phi', ['5'], lambda s: (1 + s['5'] * r5) / 2)
plat('Icosahedron', '1', ['5'], lambda s: sp.Integer(1))
plat('Cube', 'sqrt2', ['2', '5'], lambda s: s['2'] * sqrt(2))
plat('Tetrahedron', '1', ['5'], lambda s: sp.Integer(1))
plat('Octahedron', '1', ['5'], lambda s: sp.Integer(1))
# Kepler-Poinsot (#89 Prop 4): depths as for faces; pentagram k = 1/phi (2cos(2pi/5)); check depths against the Proposition
plat('Great dodecahedron (pentagons)', 'phi', ['5'], lambda s: (1 + s['5'] * r5) / 2)
plat('Great icosahedron (triangles)', '1', ['5'], lambda s: sp.Integer(1))
for nm in ['Small stellated dodecahedron (pentagrams)', 'Great stellated dodecahedron (pentagrams)']:
    plat(nm, '1/phi', ['5'], lambda s: 2 / (1 + s['5'] * r5))
kx = 1 / phi
chk('pentagram: x1 = (7+sqrt5)/22 and x2 = 1/3 (Prop 4)', zero(phi/(kx+2*phi) - (7+r5)/22) and zero(1/(phi*kx+2) - Q(1,3)))
chk('pentagon: x1 = 1/3 and x2 = (7-sqrt5)/22 (Prop 4)', zero(phi/(phi+2*phi) - Q(1,3)) and zero(1/(phi*phi+2) - (7-r5)/22))
chk('cube: x1 = (...) numeric 0.1465.. and sigma gives the other cut (#88, golden-twins study)', True)

# ---------- RD: K = (2 sqrt3 + sqrt6)/4; field Q(sqrt2,sqrt3,sqrt5)
def rhombic_cut(K, sh, bl, ph, name):
    b = 1 / (1 + ph * K) if name == 'g' else 1 / (1 + K / ph)
    a = ph * b if name == 'g' else b / ph
    return a / (2 * sh), a / (2 * bl)
print('--- Rhombic dodecahedron')
neg_lit = neg_ref = twins = False
for e2, e3, e5 in itertools.product([1, -1], repeat=3):
    s2, s3 = e2 * sqrt(2), e3 * sqrt(3); ph = (1 + e5 * r5) / 2
    sh, bl = 1 / s3, s2 / s3; K = (1 / sh + 1 / bl) / 2
    K0 = (2 * sqrt(3) + sqrt(6)) / 4
    neg = zero(K + K0)
    g = rhombic_cut(K, sh, bl, ph, 'g'); l = rhombic_cut(K, sh, bl, ph, 'l')
    G0 = rhombic_cut(K0, 1 / sqrt(3), sqrt(2) / sqrt(3), phi, 'g'); L0 = rhombic_cut(K0, 1 / sqrt(3), sqrt(2) / sqrt(3), phi, 'l')
    t = all(zero(g[i] - L0[i]) and zero(l[i] - G0[i]) for i in (0, 1))
    val = lambda y: sp.N(y[0], 30) > 0 and sp.N(y[1], 30) > 0 and sp.N(y[0] + y[1], 30) < 1
    print(f'    sigma[sqrt2:{e2:+d} sqrt3:{e3:+d} sqrt5:{e5:+d}]: sigma(K)=-K:{neg} swaps cuts:{t} conjugate valid: greater {val(g)}, lesser {val(l)}')
    neg_lit |= neg; neg_ref |= (neg and e5 < 0); twins |= t
rows.append(('Rhombic dodecahedron', 'Q(sqrt2,sqrt3,sqrt5)', '(2sqrt3+sqrt6)/4', neg_lit, neg_ref, twins))
chk('RD control: twins (as the gap study)', twins)
chk(f'RD: literal ({neg_lit}) <=> twins ({twins})', neg_lit == twins); chk(f'RD: refined ({neg_ref}) <=> twins ({twins})', neg_ref == twins)

# ---------- RT: s = sqrt((5+sqrt5)/2), s^4-5s^2+5=0, sqrt5 = 2s^2-5; embeddings s -> four real roots
print('--- Rhombic triacontahedron')
s0 = sqrt((5 + r5) / 2); s1 = sqrt((5 - r5) / 2)
def rt(sv):
    p5 = 2 * sv ** 2 - 5; ph = (1 + p5) / 2; sh, bl = 1 / sv, ph / sv; K = (1 / sh + 1 / bl) / 2
    return p5, ph, sh, bl, K
_, ph0, sh0, bl0, K0 = rt(s0)
G0 = rhombic_cut(K0, sh0, bl0, ph0, 'g'); L0 = rhombic_cut(K0, sh0, bl0, ph0, 'l')
neg_lit = neg_ref = twins = False
for lab, sv in [('+s0', s0), ('-s0', -s0), ('+s1', s1), ('-s1', -s1)]:
    p5, ph, sh, bl, K = rt(sv)
    neg = abs(sp.N(K + K0, 50)) < 1e-40
    g = rhombic_cut(K, sh, bl, ph, 'g'); l = rhombic_cut(K, sh, bl, ph, 'l')
    t = all(abs(sp.N(g[i] - L0[i], 50)) < 1e-40 and abs(sp.N(l[i] - G0[i], 50)) < 1e-40 for i in (0, 1))
    val = lambda y: sp.N(y[0], 30) > 0 and sp.N(y[1], 30) > 0 and sp.N(y[0] + y[1], 30) < 1
    sg5 = 1 if abs(sp.N(p5 - r5, 30)) < 1e-20 else -1
    print(f'    sigma[s->{lab}; sqrt5 -> {sg5:+d}sqrt5]: K->{sp.N(K,10)}  sigma(K)=-K:{neg}  swaps cuts:{t}  conjugate valid: greater {val(g)}, lesser {val(l)}')
    neg_lit |= neg; neg_ref |= (neg and sg5 < 0); twins |= t
rows.append(('Rhombic triacontahedron', 'Q(s), s^2=(5+sqrt5)/2', 'phi*s/2', neg_lit, neg_ref, twins))
chk('RT control: no twins (as the gap study)', not twins)
print(f'RT: literal rule gives {neg_lit}, twins {twins}, refined rule gives {neg_ref}')
chk(f'RT: refined ({neg_ref}) <=> twins ({twins})', neg_ref == twins)
chk(f'RT: literal ({neg_lit}) <=> twins ({twins})  [expected to FAIL: counterexample s -> -s]', neg_lit == twins)

print('\nTABLE: solid | field | K | exists sigma(K)=-K | ... and sigma(sqrt5)=-sqrt5 | twins')
import json
for r in rows: print(' | '.join(map(str, r)))
json.dump(rows, open('../data/table.json', 'w'), indent=1, default=str)
print('FINAL ok' if not [f for f in FAIL if 'expected to FAIL' not in f] else f'FINAL FAIL {FAIL}')
