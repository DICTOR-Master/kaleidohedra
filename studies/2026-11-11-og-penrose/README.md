# Penrose order in the five-fold views of the OG family? (11 Nov 2026)
DICTO: "the penrose and the icosahedral are mixed" → (b): the family is icosahedral (the 6D side) but its views perpendicular to a five-fold
axis might carry five-fold, Penrose-type order, as icosahedral quasicrystals do on their five-fold planes.
scripts/og_fivefold_view.py, data/og-fivefold-20.json (the compute machine, k = 0 … 20).
CAP (faces within 20° of a five-fold axis, projected on the plane, as a 2D tiling): tile shapes grow 1 → 21 (k = 0 … 20); the two
commonest shapes come in equal numbers (10 : 10 from k = 12; a Penrose patch has 2 shapes in ratio → φ); edge directions on multiples
of 36°: 0.14–0.33 of the edges from k = 9 (Penrose: all). No Penrose-type order in the cap.
CENTRAL SECTION perpendicular to the axis: its edge lengths show NO consecutive ratio equal to a power of φ at any level; but the edge
COUNTS fail the five-fold control at several levels (13, 47, 68, 99, 111, 137 …), a collinear-merge fault in the section code, so the
counts are not reliable (the script ends FINAL FAIL for that reason). The cap result stands; the section counts need the fix (exact
collinearity from face membership, as section_track.py does) before they are quoted.
Verdict so far: the five-fold views carry the five-fold SYMMETRY but not Penrose ORDER (shapes proliferate, no golden frequencies, edges
not on the five directions). Consistent with §28 (twin family collapses: no window, no model set).
