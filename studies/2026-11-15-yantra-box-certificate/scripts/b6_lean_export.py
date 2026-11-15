"""Step 6: Lean pilot export.  Writes a Lean file = lean/BoxCheck.lean (the proved monotone-split evaluator) + one polynomial of the
certificate (rescaled to the unit cube, integer coefficients, exactly as b4_check.py) + N leaves on which the monotone split fixes its
sign, + the kernel-checked statement (decide +kernel, no native_decide) and its corollary (no zero of the polynomial in those leaves).
A second section times an (unproved, computable) slope-form checker on N slope leaves, to estimate the cost of the full certificate.
Usage: b6_lean_export.py polys.json bnb.json POLYNAME N out.lean [mode mono|slope|both]"""
import json, sys, os
from fractions import Fraction as Fq
from math import comb, gcd
psrc, bsrc, name, N, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
mode = sys.argv[6] if len(sys.argv) > 6 else 'both'
OFF = int(sys.argv[7]) if len(sys.argv) > 7 else 0
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(psrc)); cert = json.load(open(bsrc))
box = [[Fq(a), Fq(b)] for a, b in data['box']]; A = [a for a, b in box]; W = [b - a for a, b in box]
def rescale(p):
    outd = {}
    for e, c in p:
        c = Fq(int(c))
        parts = [[(e[j], W[j]**e[j])] if A[j] == 0 else [(k, Fq(comb(e[j], k)) * A[j]**(e[j] - k) * W[j]**k) for k in range(e[j] + 1)] for j in range(3)]
        for k0, c0 in parts[0]:
            for k1, c1 in parts[1]:
                for k2, c2 in parts[2]:
                    key = (k0, k1, k2); outd[key] = outd.get(key, 0) + c * c0 * c1 * c2
    den = 1
    for v in outd.values(): den = den * v.denominator // gcd(den, v.denominator)
    return [(k, int(v * den)) for k, v in outd.items() if v != 0]
p = rescale(data['F'][name]); D = [max(e[j] for e, c in p) for j in range(3)]
def mono_split(cell):
    lo = hi = 0
    for e, c in p:
        a = 1; b = 1
        for j, (d, i) in enumerate(cell): a *= i**e[j] << ((D[j] - e[j]) * d); b *= (i + 1)**e[j] << ((D[j] - e[j]) * d)
        if c > 0: lo += c * a; hi += c * b
        else: lo += c * b; hi += c * a
    return lo > 0 or hi < 0
leaves = [l for l in cert['leaves'] if l[6] == 'F' and l[7] == name]
mono_all = [l for l in leaves if mono_split(((l[0], l[1]), (l[2], l[3]), (l[4], l[5])))]
mono = mono_all[OFF:OFF + N]
mset = set(map(tuple, mono_all)); slp = [l for l in leaves if tuple(l) not in mset][OFF:OFF + N]
print(f'{name}: {len(p)} terms, degrees {D}; leaves closed by it {len(leaves)}; mono-provable taken {len(mono)}; slope taken {len(slp)}')
pk = lambda e, c: (((abs(c) * 2 + (1 if c < 0 else 0)) * 128 + e[0]) * 128 + e[1]) * 128 + e[2]
core = open(os.path.join(HERE, 'lean', 'BoxCheck.lean')).read()
lf = lambda l: str((((l[0] << 64) + l[1]) << 144) + (((l[2] << 64) + l[3]) << 72) + ((l[4] << 64) + l[5]))
src = [core, '', 'set_option maxHeartbeats 0', 'set_option maxRecDepth 100000', '', 'namespace BoxCheck', '',
       '/-- slope form (Krawczyk and Neumaier 1985), computable; timing only in this pilot (soundness not yet proved in Lean) -/',
       'def snum (x m : Nat) : Nat → Nat', '  | 0 => 0', '  | k + 1 => x * snum x m k + m ^ k',
       'def sh (D a e : Nat) : Nat := 2 ^ ((D - a) * e)',
       'def slopeOK (Dx Dy Dz : Nat) (p : Poly) (l : Leaf) : Bool :=',
       '  let ex := l.dx + 1; let ey := l.dy + 1; let ez := l.dz + 1',
       '  let Lx : Nat := 2 * l.ix; let Ly : Nat := 2 * l.iy; let Lz : Nat := 2 * l.iz',
       '  let Mx := Lx + 1; let My := Ly + 1; let Mz := Lz + 1; let Hx := Lx + 2; let Hy := Ly + 2; let Hz := Lz + 2',
       '  let r := p.foldl (fun (acc : Int × Int × Int × Int × Int × Int × Int) (t : Term) =>',
       '    let c := t.1; let a := t.2.1; let b := t.2.2.1; let g := t.2.2.2',
       '    let mx := Mx ^ a * sh Dx a ex; let my := My ^ b * sh Dy b ey; let mz := Mz ^ g * sh Dz g ez',
       '    let v : Int := c * ((mx * my * mz : Nat) : Int)',
       '    let ahi : Int := ((snum Hx Mx a * sh Dx a ex * (Hy ^ b * sh Dy b ey) * (Hz ^ g * sh Dz g ez) : Nat) : Int)',
       '    let alo : Int := ((snum Lx Mx a * sh Dx a ex * (Ly ^ b * sh Dy b ey) * (Lz ^ g * sh Dz g ez) : Nat) : Int)',
       '    let bhi : Int := ((mx * (snum Hy My b * sh Dy b ey) * (Hz ^ g * sh Dz g ez) : Nat) : Int)',
       '    let blo : Int := ((mx * (snum Ly My b * sh Dy b ey) * (Lz ^ g * sh Dz g ez) : Nat) : Int)',
       '    let chi : Int := ((mx * my * (snum Hz Mz g * sh Dz g ez) : Nat) : Int)',
       '    let clo : Int := ((mx * my * (snum Lz Mz g * sh Dz g ez) : Nat) : Int)',
       '    let (s0, au, al, bu, bl, cu, cl) := acc',
       '    if 0 ≤ c then (s0 + v, au + c * ahi, al + c * alo, bu + c * bhi, bl + c * blo, cu + c * chi, cl + c * clo)',
       '    else (s0 + v, au + c * alo, al + c * ahi, bu + c * blo, bl + c * bhi, cu + c * clo, cl + c * chi)) (0, 0, 0, 0, 0, 0, 0)',
       '  let (s0, au, al, bu, bl, cu, cl) := r',
       '  let rad : Int := ((max au.natAbs al.natAbs + max bu.natAbs bl.natAbs + max cu.natAbs cl.natAbs : Nat) : Int)',
       '  decide (0 < s0 - rad) || decide (s0 + rad < 0)', '',
       '/-- packed data: a term is ((|c| * 2 + sign) * 128 + a) * 128 + b) * 128 + e; a leaf packs (d, i) pairs as d * 2^64 + i, base 2^72 -/',
       'def unpack (n : Nat) : Term :=',
       '  let e := n % 128; let n1 := n / 128; let b := n1 % 128; let n2 := n1 / 128; let a := n2 % 128; let n3 := n2 / 128',
       '  ((if n3 % 2 = 1 then -((n3 / 2 : Nat) : Int) else ((n3 / 2 : Nat) : Int)), a, b, e)',
       'def unpackLeaf (n : Nat) : Leaf :=',
       '  let B : Nat := 2 ^ 72; let z := n % B; let n1 := n / B; let y := n1 % B; let x := n1 / B',
       '  ⟨x / 2 ^ 64, x % 2 ^ 64, y / 2 ^ 64, y % 2 ^ 64, z / 2 ^ 64, z % 2 ^ 64⟩',
       f'def PN : List Nat := [{", ".join(str(pk(e, c)) for e, c in p)}]',
       'def P : Poly := PN.map unpack',
       '/-- Nat-only slope form: on the grid of the cell centre, H - M = M - L = 1, so S_k(H, M) = H^k - M^k and S_k(L, M) = M^k - L^k -/',
       'structure Acc where (v a0h a0l a1h a1l a2h a2l : Nat)',
       'def NT := Nat × Nat × Nat × Nat',
       'def unpackN (n : Nat) : NT := let e := n % 128; let n1 := n / 128; let b := n1 % 128; let n2 := n1 / 128; (n2 / 128 / 2, n2 % 128, b, e)',
       'def isNeg (n : Nat) : Bool := (n / 128 / 128 / 128) % 2 == 1',
       'def stepN (Dx Dy Dz ex ey ez Lx Mx Hx Ly My Hy Lz Mz Hz : Nat) (acc : Acc) (t : NT) : Acc :=',
       '  match t with',
       '  | (c, a, b, g) =>',
       '    let sx := (Dx - a) * ex; let sy := (Dy - b) * ey; let sz := (Dz - g) * ez',
       '    let mx := Mx ^ a <<< sx; let my := My ^ b <<< sy; let mz := Mz ^ g <<< sz',
       '    let hx := Hx ^ a <<< sx; let hy := Hy ^ b <<< sy; let hz := Hz ^ g <<< sz',
       '    let lx := Lx ^ a <<< sx; let ly := Ly ^ b <<< sy; let lz := Lz ^ g <<< sz',
       '    ⟨acc.v + c * (mx * my * mz), acc.a0h + c * ((hx - mx) * hy * hz), acc.a0l + c * ((mx - lx) * ly * lz),',
       '     acc.a1h + c * (mx * (hy - my) * hz), acc.a1l + c * (mx * (my - ly) * lz),',
       '     acc.a2h + c * (mx * my * (hz - mz)), acc.a2l + c * (mx * my * (mz - lz))⟩',
       'def absDiff (a b : Nat) : Nat := if b ≤ a then a - b else b - a',
       'def slopeNat (Dx Dy Dz : Nat) (pos neg : List NT) (l : Leaf) : Bool :=',
       '  let ex := l.dx + 1; let ey := l.dy + 1; let ez := l.dz + 1',
       '  let st := stepN Dx Dy Dz ex ey ez (2 * l.ix) (2 * l.ix + 1) (2 * l.ix + 2) (2 * l.iy) (2 * l.iy + 1) (2 * l.iy + 2) (2 * l.iz) (2 * l.iz + 1) (2 * l.iz + 2)',
       '  let z : Acc := ⟨0, 0, 0, 0, 0, 0, 0⟩',
       '  let P := pos.foldl st z; let N := neg.foldl st z',
       '  -- A_j upper = P.ajh - N.ajl, lower = P.ajl - N.ajh (as integers); radius = sum_j max |.|',
       '  let r0 := max (absDiff P.a0h N.a0l) (absDiff P.a0l N.a0h)',
       '  let r1 := max (absDiff P.a1h N.a1l) (absDiff P.a1l N.a1h)',
       '  let r2 := max (absDiff P.a2h N.a2l) (absDiff P.a2l N.a2h)',
       '  let rad := r0 + r1 + r2',
       '  Nat.blt (N.v + rad) P.v || Nat.blt (P.v + rad) N.v',
       f'def PPN : List Nat := [{", ".join(str(pk(e, c)) for e, c in p if c > 0)}]',
       f'def PNN : List Nat := [{", ".join(str(pk(e, -c)) for e, c in p if c < 0)}]',
       'def PPos : List NT := PPN.map unpackN',
       'def PNeg : List NT := PNN.map unpackN',
       f'def Dx : Nat := {D[0]}', f'def Dy : Nat := {D[1]}', f'def Dz : Nat := {D[2]}', '',
       'theorem P_deg : degOK Dx Dy Dz P = true := by decide +kernel', '']
if mode in ('mono', 'both'):
    src += [f'def LMN : List Nat := [{", ".join(lf(l) for l in mono)}]', 'def LM : List Leaf := LMN.map unpackLeaf', '',
            '/-- kernel check of the leaves (monotone split) -/',
            'theorem LM_ok : LM.all (signFixed Dx Dy Dz P) = true := by decide +kernel', '',
            '/-- the certified conclusion: the polynomial has no zero in any of these leaves -/',
            'theorem LM_no_zero : ∀ l ∈ LM, ∀ x y z, InLeaf l x y z → evalR P x y z ≠ 0 :=',
            '  no_zero_all Dx Dy Dz P LM P_deg LM_ok', '']
if mode in ('slope', 'both') and slp:
    src += [f'def LSN : List Nat := [{", ".join(lf(l) for l in slp)}]', 'def LS : List Leaf := LSN.map unpackLeaf', '',
            '/-- kernel run of the slope checker (timing; its soundness lemma is the next step) -/',
            'theorem LS_ok : LS.all (slopeNat Dx Dy Dz PPos PNeg) = true := by decide +kernel', '']
src += ['end BoxCheck', '']
open(out, 'w').write('\n'.join(src))
print('wrote', out)
