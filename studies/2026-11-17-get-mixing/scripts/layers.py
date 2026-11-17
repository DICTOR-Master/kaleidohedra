#!/usr/bin/env python3
"""Q3/Q4: layer swaps (exact, combinatorial in Z^6).
For every image g.Y (Y in A, B, C; g among the 120 symmetries, images up to translation) with its face-to-face lattice L_g
(spanned by the face-pair vectors), and every primitive functional h on L_g with |h(lambda)| <= 1 for all 30 face-pair vectors
(so that every neighbour of a tile lies in the same layer or the next one up or down):
  the layer is g.Y + ker(h); its top surface is the set of faces f with h(lambda_f) = +1 (mod ker h), its bottom those with -1.
Two layer types U, V with the same plane lattice ker h are SWAPPABLE if some w in Z^6 gives
  Top_V + w = Top_U and Bot_V + w = Bot_U   (as periodic face sets, mod ker h).
Then the slab between Bot_U and Top_U is filled by a U-layer and by a V-layer (shifted by w), and slabs stack (the lattice tiling of
U is the stack), so each slab can be filled independently: every 0/1 sequence gives a face-to-face tiling.
A type is also tested against itself: a w not in ker h with the same property is a layer slide.
Usage: layers.py <k10 dir> <inchbald json> <out json>"""
import sys, json, time, math
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
from fractions import Fraction as Fr
t0 = time.time()
sol = load_solids(sys.argv[1], sys.argv[2])

def solve_coords(B, v):
    """exact rational coordinates c with c.B = v (B: 3 x 6 integer, rank 3), or None if v not in the rational span"""
    for cols in itertools.combinations(range(6), 3):
        M = [[Fr(B[r][c]) for r in range(3)] for c in cols]      # rows: equations for columns
        det = (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))
        if det == 0: continue
        # Cramer
        rhs = [Fr(v[c]) for c in cols]; c = []
        for k in range(3):
            Mk = [row[:] for row in M]
            for r in range(3): Mk[r][k] = rhs[r]
            dk = (Mk[0][0]*(Mk[1][1]*Mk[2][2] - Mk[1][2]*Mk[2][1]) - Mk[0][1]*(Mk[1][0]*Mk[2][2] - Mk[1][2]*Mk[2][0]) + Mk[0][2]*(Mk[1][0]*Mk[2][1] - Mk[1][1]*Mk[2][0]))
            c.append(dk/det)
        if all(sum(c[k]*B[k][j] for k in range(3)) == v[j] for j in range(6)): return c
        return None
    raise ValueError('rank < 3')

def face_lambdas(F):
    """for each face f: the translation lambda_f with f matched by the opposite face of its pair on F + lambda_f"""
    byp = {}
    for f, s in F.items(): byp.setdefault((f[1], f[2]), []).append((f, s))
    lam = {}
    for f, s in F.items():
        (g, sg), = [x for x in byp[(f[1], f[2])] if x[0] != f]
        assert sg == -s
        lam[f] = tuple(a - b for a, b in zip(f[0], g[0]))
    return lam

layer_types = []
for Y in 'ABC':
    imgs = {}
    for gi in range(120):
        imgs.setdefault(canon_t(tfaces(sol[Y]['faces'], gi, (0,)*6)), gi)
    for gi in sorted(imgs.values()):
        F = tfaces(sol[Y]['faces'], gi, (0,)*6); lam = face_lambdas(F)
        Bz = int_rank_basis([list(v) for v in lam.values()]); assert len(Bz) == 3
        coords = {f: solve_coords(Bz, v) for f, v in lam.items()}
        assert all(all(x.denominator == 1 for x in c) for c in coords.values())
        # complete enumeration of h: h is fixed by its values (each in -1, 0, 1) on three independent face-pair vectors
        cl = list(coords.values()); tri = None
        for a, b, c in itertools.combinations(range(len(cl)), 3):
            M = [cl[a], cl[b], cl[c]]
            d = (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))
            if d != 0: tri = M; break
        hs = set()
        for vals in itertools.product((-1, 0, 1), repeat=3):
            if vals == (0, 0, 0): continue
            # solve h . M[r] = vals[r]
            hh = []
            for k in range(3):
                Mk = [row[:] for row in tri]
                for r in range(3): Mk[r][k] = Fr(vals[r])
                dk = (Mk[0][0]*(Mk[1][1]*Mk[2][2] - Mk[1][2]*Mk[2][1]) - Mk[0][1]*(Mk[1][0]*Mk[2][2] - Mk[1][2]*Mk[2][0]) + Mk[0][2]*(Mk[1][0]*Mk[2][1] - Mk[1][1]*Mk[2][0]))
                hh.append(dk/d)
            if any(x.denominator != 1 for x in hh): continue
            h = tuple(int(x) for x in hh)
            if math.gcd(*h) != 1: continue
            if next(x for x in h if x) < 0: h = tuple(-x for x in h)
            hs.add(h)
        for h in sorted(hs):
            hv = {f: int(sum(h[k]*c[k] for k in range(3))) for f, c in coords.items()}
            if any(abs(x) > 1 for x in hv.values()): continue
            top = [f for f in F if hv[f] == 1]; bot = [f for f in F if hv[f] == -1]
            # a lattice vector u with h(u) = 1 (stacking step)
            layer_types.append({'Y': Y, 'g': gi, 'basis': Bz, 'h': h, 'F': F, 'top': top, 'bot': bot, 'n_top': len(top)})
print('layer types (solid image, plane with |h| <= 1):', len(layer_types), {Y: sum(1 for L in layer_types if L['Y'] == Y) for Y in 'ABC'}, flush=True)

def kernel_member(L, v):
    c = solve_coords(L['basis'], v)
    return c is not None and all(x.denominator == 1 for x in c) and sum(L['h'][k]*c[k] for k in range(3)) == 0

def same_plane(U, V):
    """ker h_U = ker h_V as sublattices of Z^6: test the kernel bases both ways"""
    def kbasis(L):
        h = L['h']; B = L['basis']; vs = []
        # for primitive h the vectors e_i x h generate ker h in Z^3 (true for h = e_1, and equivariant under SL(3, Z))
        for c in ((0, h[2], -h[1]), (-h[2], 0, h[0]), (h[1], -h[0], 0)):
            if any(c): vs.append(tuple(sum(c[k]*B[k][j] for k in range(3)) for j in range(6)))
        return int_rank_basis([list(v) for v in vs])
    KU, KV = kbasis(U), kbasis(V)
    return len(KU) == 2 and len(KV) == 2 and all(kernel_member(V, v) for v in KU) and all(kernel_member(U, v) for v in KV)

def surf_match(U, V, w):
    """Top_V + w == Top_U and Bot_V + w == Bot_U mod ker h_U (face sets with sides; counts equal per period)"""
    for SU, SV in ((U['top'], V['top']), (U['bot'], V['bot'])):
        if len(SU) != len(SV): return False
        for f in SV:
            fw = tuple(a + b for a, b in zip(f[0], w)); s = V['F'][f]
            if not any(g[1:] == f[1:] and U['F'][g] == s and kernel_member(U, tuple(a - b for a, b in zip(fw, g[0]))) for g in SU): return False
    return True

swaps = []; slides = []
for i, U in enumerate(layer_types):
    for j, V in enumerate(layer_types):
        if j < i: continue
        if U['n_top'] != V['n_top']: continue
        if not same_plane(U, V): continue
        # candidate shifts: pair one top face of V with each top face of U of the same pair and side
        f0 = V['top'][0]; ws = set()
        for g in U['top']:
            if g[1:] == f0[1:] and U['F'][g] == V['F'][f0]: ws.add(tuple(a - b for a, b in zip(g[0], f0[0])))
        for w in ws:
            if not surf_match(U, V, w): continue
            if i == j:
                if not kernel_member(U, w) and any(x for x in w):
                    # is w a lattice vector of U (then it is just the next layer's shift within the lattice tiling)?
                    c = solve_coords(U['basis'], w)
                    slides.append({'type': i, 'w': list(w), 'w_in_lattice': c is not None and all(x.denominator == 1 for x in c)})
            else:
                swaps.append({'U': i, 'V': j, 'w': list(w)})
    if i % 20 == 0: print('  checked', i, f't={time.time()-t0:.0f}s', flush=True)
def desc(k): L = layer_types[k]; return f"{L['Y']} g{L['g']} h{L['h']}"
print('swappable pairs of layer types:', len(swaps))
for s in swaps[:60]: print('   SWAP', desc(s['U']), '<->', desc(s['V']), 'w', s['w'])
mixed = [s for s in swaps if layer_types[s['U']]['Y'] != layer_types[s['V']]['Y']]
same = [s for s in swaps if layer_types[s['U']]['Y'] == layer_types[s['V']]['Y']]
print('mixed-solid swaps:', len(mixed), ' same-solid (different image) swaps:', len(same))
print('layer slides (w not in the plane, surfaces kept):', len(slides), [ (desc(s['type']), s['w'], s['w_in_lattice']) for s in slides[:20]])
json.dump({'layer_types': [{k: (v if k != 'F' and k not in ('top', 'bot') else None) for k, v in L.items()} for L in layer_types],
           'swaps': swaps, 'slides': slides}, open(sys.argv[3], 'w'), default=str)
print(f't={time.time()-t0:.0f}s')
print('FINAL ok' if len(layer_types) > 0 else 'FINAL FAIL: no layer types')
