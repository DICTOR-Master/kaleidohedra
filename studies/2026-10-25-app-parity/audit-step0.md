# App parity with papers — audit step 0 (2026-10-25, live app k-mix 68711e5)
Method: grep of app code (src/app, krp-core) and UI strings (i18n.js) for each paper's named solids/worlds; Almanac paper refs.
## In the app (names + UI strings present)
#48 Icosaxes, Unborn Axes, Lotus Jewel Axes, Dodecaxes · #51 Samson, Delilah · #42 Sunstar, Dogstar · #45 Reuleaux · #44 Aristotle ·
#47 Platonic mix (world, few strings) · #28 Hecatodihedron · OTT · DICTONIC world · #53 Global Web of Bonds world (square, honeycomb, rock salt).
## Missing from the app
- #56: Sonsam, Lahdeli, Ian Dury, Blockhead, Sonsam-K, Lahdeli-K, Ian Dury-K, Rhombo-K; the twinned-octet walk.
- #55: Goliath, David (A15 walk stop λ = 3/4).
- #54: gnomon steps, Julias, Pimentels; polar of the keyed pair.
- Keyed pairs (unpublished): Samson-K, Delilah-K, Goliath-K, David-K.
- #53 phase 2 networks: zinc blende, twinned octet, A15, C15, perovskite.
- #50 One Move Each (classical cut-and-glue space-fillers): no trace.
- #43 Kyushindo Cores: Aktis/tower geometry in code (3 files) but no UI strings — likely not reachable.
- #42 Sunstar-Hexa / Sunstar-Hexa-Key: not in app.
- #40 OG on every stacking: 1 file, 4 strings — check depth.
## Almanac
Paper entries: #10–#39, #44, #45, #47, #48, #49, #51, #53. Missing: #40, #41, #42, #43, #50, #52, #54, #55, #56 (and #1–#9 by other refs?).
## Next (step 1, with DICTO)
Confirm list in the running app (not only code), decide one home per item (no crossover), then plan.

# Step 1 (live apps, Playwright DOM probe on dicto-big-brother, 2026-10-25)
- Kaleidohedra main door: confirms step 0 (present: Samson, Delilah, Icosaxes, Dodecaxes, Sunstar, Dogstar, Reuleaux, Aristotle, Platonic, DICTONIC, Global Web; absent: all #54–#56 items, Goliath/David, keyed -K pairs, zinc blende/A15/C15/perovskite, One Move, Sunstar-Hexa).
- Polyhedraverse: HAS #43's Aktis and Cleo Towers (so #43 is in the app, in P; correction to step 0). Still absent there: Kyushindo name, One Move, Sunstar-Hexa, OG on every stacking.
- Rhombiverse: none of the gap items.
- /dicto door renders a small shell first (5.5k chars), so it was not a useful probe.
Confirmed gaps: #56, #55, #54, keyed pairs, Global Web phase 2, #50, #42 Sunstar-Hexa/Hexa-Key, #40 stackings (check), Almanac entries #40–#43, #50, #52, #54–#56.
