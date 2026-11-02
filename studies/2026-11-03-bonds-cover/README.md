# The DICTONIC square (book cover)

Request (2026-11-03): the cover for DICTO's book "DICTONIC Bonds: from the Octet to the Rule of Halves" (draft 105 pages), in the family of the GOLDEN, STAR CORES and HexOct covers.

**Conclusion:** front (8 x 8 DICTONIC square + title panel) and KDP wrap (back, spine, front; spine for 105 pages) made. Status: waiting for DICTO's read.

- Cyclic Latin square 8 x 8 of DICTONIC (row i, column j = position (i+j) mod 8): DICTONIC across the top and down the left; every position (piece) once in each row and column.
- Pieces in the book's order (preface), exact corners and faces from the DICTO Solids dataset v7: D Icosaxes, I Unborn Axes (Golden bond, gold); C Lotus Jewel Axes, T Dodecaxes (Keyed bond, violet); O Samson, N Delilah (Delian bond, teal); I Sonsam, C Lahdeli (Twinned Delian bond, blue). Face counts checked (14, 14, 54, 54, 10, 8, 13, 8); winding checked; one circumradius, the squares' one pose.
- Two pieces are not convex (dents, keys), so the pieces are drawn with a depth buffer; edges are the borders between visible face planes (~2 px at 2400 px).
- Letters: the HexOct LED letters (DSEG14 Classic, OFL) in the opposite palette colour, as Star Cores: violet on gold, gold on violet, red on teal, orange on blue.
- Title panel as Star Cores: DICTONIC BONDS (gold), FROM THE OCTET TO THE RULE OF HALVES (teal, shrunk to fit: 0.0325 N against 0.040), ◆ DICTO ◆ (red). No series line (not part of a series).
- KDP wrap: A4 trim, bleed 0.125 in, 300 dpi; spine = 105 x 0.002252 in = 0.2365 in (white paper, as the other books; check KDP's calculator before upload); spine text (105 > 79 pages). Back: blurb from the preface, author note, ◆ DICTO ◆ mark, logo, DOI line "(to come)", barcode area 2 x 1.2 in kept clear.
- scripts/bonds_square.py <dataset solids dir>, scripts/cover_title.py, scripts/kdp_cover.py (PAGES=, GUIDES=1); run on dicto-big-brother in ~/kres-tmp/bonds-cover/scripts.
