# Aequi picker: too many Vacuus "plates" (DICTO 28 Nov: "Lucky 7 ... I think it is a mistake throughout the catalog as all seem to have
too many fins for the numbers"). scripts/fins.js on the picker's own geom.js + dice.json (same files as the live app, md5 checked).
FINDING (confirmed): the picker's note "Vacuus: N plates, one triangle from the centre to each edge" counts EDGES, not plates. In #120 a
plate is a PLANE through the centre and an edge (full sheet / shared sheet / single fin by the edges it carries). Opposite or coplanar
edges share one plane, so the picker over-counts on 9,882 of the 10,725 catalogued dice.
Lucky 7 (catalogue No. 5, Oh, 14 faces, 24 corners): 36 edges drawn and counted as "36 plates", but 15 distinct Vacuus planes; 7 Resonus
planes; 3 planes in both families (drawn twice, once as Vacuus triangles and once as a Resonus cross-section).
Numerical (tolerance 1e-9). The papers define plates as planes (#120 section 2); their counts come from the study scripts, not the picker.
Fix proposed to DICTO (not applied: app change needs his word): count and colour by plane; mark planes in both families once.
FIX (k-mix branch aequi-plate-count, not deployed): geom.js vacuusPlanes (plates = planes; full / shared / fin), note counts planes, planes
in both families striped in both colours (DICTO: "maybe shared can be striped") and drawn once. Control scripts/check_planes.js: 0
mismatches on 10,725 dice; Lucky 7 = #120's truncated octahedron row (15 plates, 15 full, 7 Resonus, 3 both). Page checked headless
(scripts/aequi_shot.mjs, no page errors); before/after sheet in the reading folder.
LIVE STATE (28 Nov, checked on the live site, Lucky 7 and Iyai #181, four views, no page errors): Vacuus = fins + struts as #87 defines
(a flat-sheet variant was built and dropped: #87 joins two fins only when they share a strut); plates counted as planes; Vacuus in two
slates (lighter on a mirror); Resonus plates solid; shared fins striped in the Resonus colour and the Vacuus slate; "Shared only" button;
no construction lines (the die's edges not drawn where nothing of the die is drawn). Lucky 7 checked against #110 / Entry 8: fair to 1e-10,
r/R = cot(2 pi/7), sloping plates at 2 pi/7 to the cube axes; 15 plates, 7 Resonus, 3 shared. Near misses (true, not faults): 12 fins
7.118 deg from the 4 hexagon-direction Resonus plates.
