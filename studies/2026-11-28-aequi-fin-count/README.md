# Aequi picker: too many Vacuus "plates" (DICTO 28 Nov: "Lucky 7 ... I think it is a mistake throughout the catalog as all seem to have
too many fins for the numbers"). scripts/fins.js on the picker's own geom.js + dice.json (same files as the live app, md5 checked).
FINDING (confirmed): the picker's note "Vacuus: N plates, one triangle from the centre to each edge" counts EDGES, not plates. In #120 a
plate is a PLANE through the centre and an edge (full sheet / shared sheet / single fin by the edges it carries). Opposite or coplanar
edges share one plane, so the picker over-counts on 9,882 of the 10,725 catalogued dice.
Lucky 7 (catalogue No. 5, Oh, 14 faces, 24 corners): 36 edges drawn and counted as "36 plates", but 15 distinct Vacuus planes; 7 Resonus
planes; 3 planes in both families (drawn twice, once as Vacuus triangles and once as a Resonus cross-section).
Numerical (tolerance 1e-9). The papers define plates as planes (#120 section 2); their counts come from the study scripts, not the picker.
Fix proposed to DICTO (not applied: app change needs his word): count and colour by plane; mark planes in both families once.
