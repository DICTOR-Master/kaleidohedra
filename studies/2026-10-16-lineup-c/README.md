DICTO · dictospheres.com

# Line-up C: the Spheres of Dharma with 3·I as the seventh station (2026-10-16)

Asked by DICTO after Fable's advice on P4 (*Double Vision – Both Cycles in One Space*, DICTO DOI 10.5281/zenodo.23407107). The TI → RT layer has two convex
in-between stages: the Hecatodihedron (stage 7, used by *Inverted Shells* and P4) and the icosahedron 3·I (the truncated icosahedron with its 12 caps
restored). Neither contains the other, so a line-up takes one. This study takes 3·I.

## Step 1 (exact, Q(√5)): `scripts/lineup_c.py` → `data/lineup-c-step1.txt`

- The chain I ⊂ ID ⊂ D ⊂ TI ⊂ 3·I ⊂ RT ⊂ I·φ³ nests exactly. The 60 truncated-icosahedron corners all lie on faces of 3·I (they are its edge thirds), and the 12 corners of 3·I lie on faces of RT.
- Its polar reversal (unit sphere) is all classical: D·φ⁻³ ⊂ ID ⊂ D/3 ⊂ PD ⊂ I ⊂ RT ⊂ D.
- **Toggle, ends (ρ² = φ²/4):** shared I ↔ D, as in P4.
- **Toggle, middle (ρ² = 3φ²/4):** shared ID ↔ RT **and D ↔ 3·I**. The middle setting shares four stations, not two.
- Every ρ² that makes any pair of stations coincide is one of these two settings, up to a factor φ³. So "no sphere gives both" still holds.
- Station lists are cleaned to true corners first: the float hull lists of TI and RT carry 8 and 24 extra points that lie on faces but are not corners.

Next: the interlock (pairwise intersection of the two cycles' cone-cut pieces) for line-up C in both settings, exact counts and kinds.

## Step 2 (float cut, exact check): `scripts/c_chains.py` → `scripts/interlock.py ../_lib ends|middle` → `scripts/interlock_exact.py ends|middle`

- `c_chains.py B` (P4's line-up) reproduces P4's 174 original and 154 reversed cone pieces: the known-case check.
- Line-up C cone cut: 114 original pieces per turn (20, 20, 12, 12, 20, 30) and 154 reversed.
- **Ends setting: 536 pieces, 12 kinds**, exact (every original piece and every layer is the sum of its parts, remainder 0 in Q(√5); kinds agree by volume and by orbit under Ih). Per original layer 80 · 60 · 12 · 24 · 120 · 240. The total equals P4's 536 because TI → 3·I → RT and TI → H → RT cut the same TI → RT region into 144 pieces either way; the split and four of the kinds differ.
- **Middle setting: 322 pieces, 8 kinds**, exact. Per original layer 120 · 20 (whole) · 72 · 60 · 20 (whole) · 30 (whole). Sharing four stations, the two cycles cut each other far less than in P4's middle setting (502 pieces, 11 kinds).
- Outputs: `data/interlock-{ends,middle}.json|txt`, `data/interlock-{ends,middle}-exact.txt`, log `data/run-interlock.log`.
