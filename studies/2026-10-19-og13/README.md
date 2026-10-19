# OG-13: twelve OGs round one, no symmetry imposed (DICTO 2026-10-19, float)

DICTO's question was what a 13-cell arrangement of the OG would bring out, aiming to find new arrangements rather than fall back on known symmetries. Method (`og13.py`, run on dicto-node, log `og13.log`, results `data/og13-results.json`):
- One OG sits at the centre. Twelve OGs move and turn freely as hard bodies (touching only, no overlap), with Monte Carlo compression towards the centre (energy = Σ|p|², annealed, then cooled).
- The overlap test checks whether any edge of one OG passes through the other, both ways. It agreed with the full separating-axis test on 3,000 random pairs with no disagreement, and every final cluster was re-checked with the full test.
- Any symmetry of a cluster must fix the centre OG, so each of the centre's 120 icosahedral operations was tested on all corners, at tolerances 0.01, 0.03 and 0.06.

## Result (48 random starts)

- **No symmetry falls out.** The 8 best clusters all have symmetry order 1, even at tolerance 0.06: no icosahedral 13, no cuboctahedral (octet) 13, and no partial symmetry either.
- **Many near-equal arrangements.** Energy ranges from 19.136 (best) through 19.330 (median) to 19.795 (worst). The best few differ by less than 0.1%, a glass-like landscape with no single winner.
- **About half the neighbours sit hexagon to hexagon** (6 of 12 in the best 7 clusters; one has 10). Centre distances run from 1.246 (hexagon contact is 1.2456) to 1.28. The twelve outer OGs do not touch each other (nearest 1.28–1.30).
- **Why the hexagon contacts can't all be used:** only 12 of the OG's 20 hexagon directions can be taken, and neighbouring hexagon directions (41.8° apart) would put two neighbours 0.89 apart, so they clash. The OG is frustrated in flat space.
- **Reading (ours, not checked further):** like the 600-cell story, an icosahedral 12-round-1 does not fit flat space with faceted bodies. The OG's 13 does not lock into either icosahedral or octet order. It stays disordered, as in a glass.

Caveats: float; Monte Carlo, not a proof of optimality; 48 starts, so a better symmetric arrangement may exist. A direct test of the symmetric candidates (icosahedral and cuboctahedral 13s at their tightest) would settle it.
