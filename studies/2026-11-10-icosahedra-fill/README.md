# Icosahedra filling space with Cleo-Icos and Antonius (DICTO 10 Nov 2026)
Motivation (DICTO): to make the icosahedron tile space, "as it was said not possible". The Cleo-Icos (#29, Aristotle's pyramid #44)
and Antonius (D65, #44) came from that search. Earlier status: icosahedra alone or with face pyramids are excluded (Dehn); icosahedra
with Antonius were left open (study 2026-10-27-five-pyramids).

**Step 1, Dehn balance (proof).** Dehn invariants add under dissection. The golden rhombohedron Cleo + Antonius + Cleo fills space by
translation, so D(rhombohedron) = 0 and D(Antonius) = −2 D(Cleo-Icos). The icosahedron is 20 Cleo-Icos round its centre (inner edges
close full turns, contributing rational multiples of π), so D(icosahedron) = 20 D(Cleo-Icos). Hence D(icosahedron) + 10 D(Antonius) = 0:
a filling must use icosahedra and Antonius in the ratio 1 : 10 (plus any Cleo–Antonius–Cleo groups). Necessary, not sufficient.

**Step 2 plan.** (a) which golden rhombohedron is Cleo + Antonius + Cleo (prolate or oblate); can the other split into Cleo-Icos and
Antonius (or what further piece it needs); (b) in Ammann–Kramer–Neri 3D Penrose tilings, the corners surrounded by 20 prolate
rhombohedra (a rhombic triacontahedron) each hold a full icosahedron of 20 inner Cleo-Icos: confirm they occur and their frequency;
(c) periodic version: do the cubic approximants (1/1, 2/1, …; study 2026-11-10-ab-line step 4) contain them.

**Step 2(a) (volumes, exact).** The prolate golden rhombohedron spanned by the three corners a, b, c of one icosahedron face (from
the centre) is Cleo + Antonius + Cleo: its acute corners are the Cleo-Icos conv(0, a, b, c) and its opposite; volume 6 Cleo, so
Antonius = 4 Cleo (#44). The oblate golden rhombohedron has volume (prolate)/φ = 6/φ ≈ 3.708 Cleo volumes, while every union of
Cleo-Icos (1), Antonius (4) and icosahedra (20) has a whole-number volume: the oblate rhombohedron cannot be cut into these pieces.
So the Ammann–Kramer–Neri tilings (both rhombohedra) do not decompose into DICTO's pieces as they stand.
Twenty prolate rhombohedra round one point (spanned by the 20 face triples) form the rhombic hexecontahedron (the '20 + 20 + 20' of
study 2026-10-27-five-pyramids): 20 inner Cleo-Icos = a whole icosahedron, then 20 Antonius, then 20 outer Cleo-Icos.
**Refined question.** Can space be filled by prolate golden rhombohedra alone, including rhombic-hexecontahedron stars? Each star holds
a whole icosahedron; everything else splits into Cleo-Icos and Antonius. Obstacle: de Bruijn (grid) tilings in the six icosahedral
directions always contain oblate tiles, so such a filling must be non-zonotopal. Next: exact search for a prolate-only surround of
one hexecontahedron star (icosahedral orientations, face-to-face).

**Step 2(b) result (10 Nov 2026).** surround.py (prolate tiles only, corners in Z<e1..e6>, nearest-open-face-first, backtracking):
the hexecontahedron star is surrounded to search radius 1.9/2.2 (+60 tiles), 2.6/3.0 (+180), 3.4 (+320), with almost no backtracking
(nodes = tiles + 14). verify_exact.py, exact in Q(√5) (separating axes, edge length 1): witnesses 2.6 (200 tiles, 2524 close pairs) and
3.4 (340 tiles, 4572 pairs): no two tiles overlap; no face is used by more than two tiles; no open face has its centre inside the radius.
Covered ball: at least radius 3.4 − (half the longest face diagonal, ≈ 0.85) ≈ 2.5 for the 3.4 witness. So locally a whole icosahedron
(20 Cleo-Icos) sits inside a filling of Cleo-Icos + Antonius. Open: all of space (periodic star arrangement, or a proof the shells close
for ever). DICTO 10 Nov: "octet and gyrated octet could both be used": restated to him, awaiting his confirmation.

**Step 3, the icosahedral (gyrated) octet (DICTO 10 Nov 2026, confirmed: "so new pieces for icosahedral gyrated octet").**
octet_gap.py (exact, sympy). Regular octahedron, corners (±1,0,0)…, edge √2. The regular icosahedron with its 12 corners on the 12 edges,
each edge divided in the golden ratio: icosahedron edge 3 − √5, volume 70/3 − 10√5 ≈ 0.97265 of the octahedron's 4/3. Eight
icosahedron faces lie in the eight octahedron faces; the other 12 come in 6 folded pairs, one pair facing each octahedron corner.
NEW PIECE (placeholder name: corner piece; name is DICTO's): octahedron minus icosahedron = 6 congruent corner pieces, each the octahedron
corner plus the 4 icosahedron corners on its 4 edges; volume (5√5 − 11)/3 ≈ 0.06011. Faces: 4 triangles in the octahedron faces + 2
icosahedron faces as a folded base. It is NOT convex: at the fold (an icosahedron edge) its inside angle is 360° − 138.19° = 221.81°.
It is two mirror-image tetrahedra glued on the triangle (corner, fold edge).
Filling: octet or gyrated octet, each octahedron = 1 icosahedron + 6 corner pieces, tetrahedra whole. Each octahedron's icosahedron has
two positions (the two golden divisions); octahedra meet only at corners, so the choice is free per octahedron, in both octets.
So icosahedra + corner pieces + tetrahedra fill space (immediate, exact). Dehn: the corner pieces carry the icosahedron's golden angles.
Next: corner piece angles and whether it relates to Cleo-Icos/Antonius; whether tetrahedron + corner pieces merge into nicer pieces.
