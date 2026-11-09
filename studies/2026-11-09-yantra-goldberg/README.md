# Hexagram (Ṣaṭkoṇa) network on the smallest sphere: study 2026-11-09

**Conclusion: on the icosidodecahedron, the 20 triangles + their 60°-turned copies give 20 hexagrams on the Cleo-sphere circles
(20.9052°); the turned tips sit 5 round each pentagon centre (16.4722° from it) and close up as 12 pentagrams: one network.**
Status: picture + float checks (FINAL ok); exact values not yet derived.

DICTO asked (9 Nov) whether the known hexagonal yantra can make a network of a Goldberg sphere, as small as possible, maybe an
icosidodecahedron. Construction and pictures with Claude (Anthropic). The bare star-in-every-face pattern on polyhedra is known
(Hankin's polygons-in-contact method; Kaplan's Islamic star patterns on polyhedra); the Cleo-circle hexagram reading is ours.

- Red (up): the ID triangles; their sides lie on the ID's 6 great circles (the 6 decagons, classical).
- Blue (turned 60°): 30 great circles, each carrying two antipodal arcs.
- Violet (pentagrams through the turned tips): 30 more great circles, none shared with the blue ones. Total 66.
- Figure: figures/id-hexagram-network.png (A hexagrams only, B with pentagrams). Scripts: scripts/id_hexagram_net.py, gc_check.py.

LEADS: exact tip distance (16.4722°) and pentagram size in Q(√5); next sizes = Goldberg GP(1,1) (truncated icosahedron, 20 hexagons),
GP(2,0) (dual of the 81 sphere); which turn angle (not 60°) makes blue and violet share great circles (one continuous line network).

## Cleo sphere: do yantra lines run on as great circles? (DICTO 9 Nov, seen in Mandalaspheres)
scripts/cleo_lines.py, data/cleo-lines.log. Every yantra line is a great circle (gnomonic). Antipodal yantras share all their circles
(trivial, excluded). Scale λ = yantra size / Cleo incircle (app: λ = 1, top to a face corner).
- At the app's own scale λ = 1 the **t3 sides run on EXACTLY** into neighbouring yantras' t3 sides (16 pairs, 0.0000°): DICTO's
  observation is exact for t3. (Top-to-edge orientation: the t7 sides do the same.)
- Every other line family lines up only at its own scale (corner orientation): t1 base 0.548, t6 sides 0.678, t8 sides 0.725,
  t2 base 0.858, t5 sides 0.980, t2 sides 1.068, t3 sides again 1.411, t3 base 1.434, t4 sides 1.613 …; never two families at one scale
  except single cross pairs (t2 side / t9 base at 1.068, t4 side / t8 at 1.613). So one scale cannot make the whole network continuous;
  the 20-yantra layout carries one continuous family at a time. Paused for #43 (DICTO); next idea queued: diamond yantras (two Cleo-Icos).
