# The OCD Stella with octahedra, exact (DICTO 2026-10-20: "the Stella with holes")
First found 2026-10-16 (DICTO: "it would also fill well with an octahedron ... perhaps utilising the stella"; float, studies/2026-10-16-ocd-pyrochlore: stella_octahedra.py, stella_octa_pyro.py; app: OCD Stella Crystals, partner Octahedra, Notches). Mentioned in #31a as ≈ 96.33% (float).

`stella_octa_exact.py` (dicto-node, exact in ℚ(√5); builds the Stella with ../2026-10-19-og-gyrated-octet/stella_twin_exact.py) → `stella-octa-exact.log` (10 PASS), `stella-octa-exact.json`.
- Frame of #37: OCD packing sites (2R/3)(a,b,c), all even or all odd; cell = truncated octahedron (512 + 256√5)/729; the octahedron of the 8 joint planes = |x|+|y|+|z| ≤ R = 9/8 of the cell; each tip beyond a square wall 1/48 of the cell.
- Only the 6 square neighbours' octahedra reach a Stella; **one notch 392/2187 − 88√5/1215 ≈ 0.017287** (all six equal; 8.00% of the Stella for six; 55.78% of the tip); **notched Stella −1616/243 + 12784√5/3645 ≈ 1.192289**.
- Octahedra: hexagon neighbours face to face; square neighbours would overlap tip to tip ((64 + 32√5)/2187) → no two octahedra may be square neighbours; farther never overlap.
- **Pyrochlore (octahedra on one diamond network): 1423/32 − 3113√5/160 ≈ 96.3252%**; rock salt (a quarter): 3839/64 − 8453√5/320 ≈ 91.7242%; Stellas alone 151/2 − 267√5/8 ≈ 87.1231%. The float values of 10-16 agree. Space groups (float, spglib, 10-16): Fd-3 (pyrochlore), Fm-3 (rock salt).
- App: K note now says exact (7 languages); tests/browser/ocd-stella.mjs requires it.
