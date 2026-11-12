# Disc ranking under the #87 rule (13 Nov 2026; Platonic book Ch 4 lead)

**Conclusion (13 Nov 2026): under the #87 definition the Ch 4 ranking collapses. Of DICTO's solids only five have a central disc: Delilah 100 % (3 squares), Hexa-Key 26.7 % (9 discs), the Jewel tetrahedral cluster 6.7 %, Hexa 5.9 % and the Hexa rhombohedral cluster 2.8 %. The Sunstar tetrahedral cluster (93.9 % under the 11-11 rule), Dogstar (82.6 %), the Sunstar octahedral cluster (78.8 %), Lotus Jewel Axes (71.4 %), Icosaxes and Unborn Axes all have 0 discs. Across the whole registry: 8 solids have every edge on a #87 disc (21 under the 11-11 rule), and 361 of 389 have no #87 disc (281 under the 11-11 rule).**

The two rules:
- **11-11 rule** (studies/2026-11-11-orbit-polytopes/scripts/vacuus_census.py): a "disc" is a central plane carrying at least 3 edges.
- **#87 rule** (studies/2026-11-02-dicto-vacuus/scripts/vacuus.py; exact form in studies/2026-11-13-platonic-exact-checks): the
  fins O-A-B join into a flat sheet across a shared corner ray when they are coplanar and lie on opposite sides of the ray. A central
  disc is a sheet whose apex angles sum to 2 pi. Here it is decided twice: by the float apex sum, and combinatorially (one closed cycle
  of corners winding once round O). The two tests agree on every sheet of every solid.
Share = edges on discs / all edges. The centre is the mean of the corners, as in the 11-11 census.

## DICTO's solids, side by side (34 solids: id or name contains DICTO, the DICTO Jewel family, Dogstar, the Sunstar clusters, the seamed dodecahedron)
| solid | edges | 11-11: discs | 11-11 share | #87: discs | #87 share | #87 disc sizes |
|---|---|---|---|---|---|---|
| Delilah | 12 | 3 | 100 % | 3 | **100 %** | 3 × 4 |
| DICTO Hexa-Key | 360 | 30 | 80.0 % | 9 | **26.7 %** | 3 × 8, 6 × 12 |
| DICTO Jewel tetrahedral cluster | 360 | 28 | 70.0 % | 3 | **6.7 %** | 3 × 8 |
| DICTO Hexa | 408 | 41 | 75.5 % | 3 | **5.9 %** | 3 × 8 |
| DICTO Hexa rhombohedral cluster | 2616 | 232 | 72.5 % | 3 | **2.8 %** | 3 × 24 |
| Dodecahedron, seamed for Dogstars | 282 | 51 | 100 % | 0 | 0 | |
| Sunstar tetrahedral cluster | 984 | 115 | 93.9 % | 0 | 0 | |
| Dogstar | 138 | 15 | 82.6 % | 0 | 0 | |
| Sunstar octahedral cluster | 1208 | 304 | 78.8 % | 0 | 0 | |
| Lotus Jewel Axes | 84 | 15 | 71.4 % | 0 | 0 | |
| DICTO Jewel | 96 | 9 | 50.0 % | 0 | 0 | |
| DICTO Jewel octahedral cluster | 456 | 28 | 48.2 % | 0 | 0 | |
| Admiral Cap | 9 | 1 | 33.3 % | 0 | 0 | |
| DICTO skewed rhombic dodecahedron | 24 | 2 | 33.3 % | 0 | 0 | |
| Icosaxes | 36 | 3 | 33.3 % | 0 | 0 | |
| Unborn Axes | 36 | 3 | 33.3 % | 0 | 0 | |
| DICTO Hexa diamond cluster | 2148 | 155 | 31.2 % | 0 | 0 | |
| DICTO skewed elongated dodecahedron (16) | 28 | 2 | 28.6 % | 0 | 0 | |
| DICTO Dodeca-13 | 330 | 15 | 27.3 % | 0 | 0 | |
| DICTO Truncated-Icosahedral Hecatodihedron (Dharma stage 7) | 180 | 12 | 26.7 % | 0 | 0 | |
| DICTO Dodeca-13 Unit | 75 | 5 | 20.0 % | 0 | 0 | |
| Dodecaxes | 84 | 3 | 14.3 % | 0 | 0 | |
| DICTO Hexa trimmed Jewel | 96 | 3 | 13.5 % | 0 | 0 | |
| 11 others (Dodeca-13 Needle, Star, Wedge; Hexa roof; all-rhombus block; flattened rhombohedron; leaning hexagonal prism; skewed elongated dodecahedron (18); square-faced block; Samson; Unborn) | | 0 | 0 | 0 | 0 | |

So 29 of these 34 have no #87 disc (11 under the 11-11 rule). The 11-11 README speaks of "66 DICTO solids", but its list was not
recorded, and no name rule we tried gives 66 (30, 34, 72, 78). So this table uses the stated 34-solid rule, and data/disc-ranking.json
holds all 389 solids for any other selection.

## Whole registry (389 solids; all 109 solids with a disc under either rule are in data/disc-ranking.log, lines ALL)
- Complete #87 Vacuus (every edge on a disc): octahedron, cuboctahedron, icosidodecahedron, tetrakis hexahedron, disdyakis
  dodecahedron, disdyakis triacontahedron, Delilah, Reuleaux octahedron (8; 21 under the 11-11 rule).
- Complete under 11-11 but **no** #87 disc: rhombic dodecahedron, rhombic triacontahedron, Bain RD, RD target 4, Spheroid-13 RD
  centre (0.35), pentakis dodecahedron, triakis icosahedron, deltoidal hexecontahedron, seamed dodecahedron. On their planes the fins
  form open fans, as on the Dogstar.
- Complete under 11-11 but only partly under #87: deltoidal icositetrahedron 3 of 9 (50 %), triakis octahedron 3 of 9 (33 %),
  triangular orthobicupola 1 of 7, pentagonal orthobirotunda 1 of 11.
- Same under both rules: the octahedron family above, the bipyramids D6 and D10, the bicupolae J28-J30, J15, J26, J91, Tadpole.

## Controls (all ok; data/disc-ranking.log)
R1: the 11-11 rule reproduces the 11-11 census JSON (discs, edges on discs, edges) for all 389 solids. R2: #87 octahedron 3 × 4,
cuboctahedron 4 × 6, icosidodecahedron 6 × 10; NEGATIVE cube 0, dodecahedron 0. R3: Dogstar has 0 #87 discs, and 15 planes carrying
114 edges under the 11-11 rule, as in the exact study. R4: the apex-sum and closed-cycle tests agree everywhere. R5: the #87 result
does not change at tolerances 1e-5, 1e-6, 1e-7. R6: #87 share <= 11-11 share for every solid. Cross-check after the run: on the 40
solids shared with #87's own census (data/vacuus-census.json of the #87 study), the #87 disc sizes agree for every one, including the
Catalan discs #87 lists (deltoidal icositetrahedron 3 octagons, disdyakis dodecahedron 9, disdyakis triacontahedron 15, tetrakis
hexahedron 6, triakis octahedron 3).
Float caveat: the registry stores corners to about 1e-8, so these are float decisions, stable over two orders of tolerance. Only the
controls and the Dogstar are exact (13 Nov exact study).

## Running
`scripts/disc_ranking.py` ran on the second compute host through the job gate, 4 GB cage, one process: pilot `discrank-pilot`
(36 solids, FINAL ok) and full run `discrank` (389 solids, 15 s, 10 checks, 0 failed, FINAL ok). Inputs:
data/registry-solids.json (the app registry export the 11-11 census read: corners and faces); data/registry-families.json (the same
registry's ids and names); data/census-11-11.json (copy of the 11-11 census output, the R1 control).

## Sources checked
studies/2026-11-13-platonic-exact-checks (README C, platonic_exact.py disc_census); studies/2026-11-11-orbit-polytopes (README census
section, vacuus_census.py, data/vacuus_census.json); studies/2026-11-02-dicto-vacuus (#87: README discs list, vacuus.py sheet code,
data/vacuus-census.json); papers/book-platonic/chapters/ch04.html §4.3-4.4 (read only, not edited); Concordance ledger [204] (whose
lead this is), [130], [131]. The reference library was not searched (no prior-art question).

## LEADS
1. Ch 4 (DICTO's to place): the sentence "the ranking ... has not been rerun" can now cite this table. Under #87, Delilah, then
   Hexa-Key, lead; the Sunstar and Dogstar family has none.
2. Hexa-Key's 9 discs (3 octagons, 6 dodecagons): an exact check in its field, and a figure next to the octahedron's 3 squares.
3. The RD and RT carry complete 11-11 planes but no #87 disc (open fans): the same "two fans per plane" picture as the Dogstar. Is it
   one law for the zonohedra?
4. Record the 66-solid list whenever a DICTO-solid ranking is quoted, so it can be rerun.

DICTO · dictospheres.com
