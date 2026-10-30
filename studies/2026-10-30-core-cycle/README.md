# The TI Star core's own cycle (DICTO 2026-10-30)
DICTO's idea: give the TI Star core (D105) its own pentagonal and hexagonal pyramid core and spikes, as #78 did for the truncated icosahedron, and follow it.

**Conclusion: the core and the truncated icosahedron are a two-step cycle.** The core's own turn gives back a regular truncated icosahedron (larger), whose turn gives the core again: TI → core → TI → …
- Why: both solids are cut by the same two families of planes (pentagons on the 5-fold axes, hexagons on the 3-fold). A turn puts the next core's hexagon planes where the pentagon tips were and its pentagon planes where the hexagon tips were, so the ratio pentagon-distance / hexagon-distance is inverted: TI 1.02653, core 0.97415 = 1/1.02653.
- Scale per two turns: t² (5+2√5)/15 (t = φ: 1.6532; t = 2: 2.5259); (5+2√5)/15 is the square of the icosahedron's inradius/circumradius.
- The hull of the core's 32 tips is the Catalan pentakis dodecahedron (the polar of TI), just as the hull of TI's tips (the Star Halo) is the polar of the core: the two halos are each other's partners too.
- The core's star has φ × (or 2 ×) its volume, as TI's; layer 1 fills exactly with 150 pieces (60 corner pieces + 90 edge tetrahedra, 3 kinds), no overlaps; star inside its hull. Both t = φ and t = 2.
Status: numerical (scipy) with the 2-cycle explained geometrically; exact Q(√5) confirmation not yet run. Placement: a section for #78 v2 (or Golden Cycle v3) — DICTO to choose.
Scripts: scripts/core_cycle.py <stations-exact.json of #78> (T=phi|2); data/core-cycle-*.json.
