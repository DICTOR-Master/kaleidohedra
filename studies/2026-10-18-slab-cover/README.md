# Slab cover of the OCD golden envelope — DICTO 2026-10-18

DICTO · dictospheres.com

**Question (DICTO):** "can we not just cover in the golden envelope" — fill G′ by covering each OCD's golden envelope (RT on the bcc sites).

## Found
- The RT envelopes **overlap their 8 nearest neighbours** (1.2456 apart; each reaches 0.7136): 35.3% of the RT surface is buried (sampled), drawn red in `renders/puzzler-72.html`.
- Towards the **6 second neighbours** (1.4383 apart) each RT has a parallel face pair: a flat slab of gap **(−88+40√5)/9 ÷ |N| = 0.104919** (exact; all six equal — check in `data/slab-exact.json`).
- **Exact:** the slab is two layers, each an **oblate golden rhombohedron at λ/φ** or a **prolate at λ/φ²** (height 0.052460 each). No single piece fits; no piece of the RB set (¼λ, ½λ, 1λ rhombohedra, Bodhi pieces) stacks to it.
- So puzzler seeds 12/13 (best 72 tiles, 15.83%, `data/puzzle-RB-1{2,3}f.json`) could never cover the slabs: all 72 tiles sit on the 24 non-slab faces.

## Open (for DICTO)
- Do the λ/φ, λ/φ² layers also fit where the slab meets the wedges? (Bands in the section are drawn only across the shared face.)
- If yes: cover slabs first, then let the puzzler solve only the wedges (RX piece set).

## Files
- `scripts/slab_exact.py` → `data/slab-exact.json` (exact Q(√5), checks)
- `scripts/section_110.py`, `scripts/draw_section.py` → `renders/slab-section.html` (2D (110)-type cut)
- `renders/puzzler-72.html` — 3D 72-tile layout + red/green zones
- Pages: claude.ai/artifact/NACMK1i9YzZ73ceimG1Yzv (3D), claude.ai/artifact/JhhbeK4Dnc4XqBZyV331Hv (section)
