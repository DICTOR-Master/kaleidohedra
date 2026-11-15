# Series line on every front cover (15 Nov 2026)

DICTO: "the orders of space labels aren't on all book front covers in the series".

Rule (one for all covers): the series line of THE FIVE ORDERS OF SPACE, worded by papers/series-five-orders/series_line.py
(e.g. "Book Two · Earth 地 · The Five Orders of Space"; Quanta I and II: "Book One, I" / "Book One, II"), white LED letters as
on the Platonic Solids cover (size 0.030 W fitted to W - 360 s, s = W/2400), is the TOP line of the lettering, 87 s above the
next line; an existing sub-series line ("Cycles of Growth Part I/II") stays beneath it, then title, subtitle and mark. The
picture is not touched; the lettering block (pixels copied) moves down only as far as needed for 50 s of ground above the line.

Run: python scripts/series_covers.py <papers>; python scripts/compare_sheet.py <papers> COVERS-series-line.png.
Result: FINAL ok, 10 covers, each written as <cover>-series-v2.png beside the book's cover (old cover kept).
Translations (Quanta and DICTOnary ar/fa/ja/zh) have no translated series wording yet: left unchanged.

## Series line in the element colour (15 Nov 2026, v3)

DICTO: "the line representing the order should be fully or partially in the element colour". Partial version chosen: the ring
word and its kanji (e.g. "Wind 風") in the ring's element colour, the rest white; same LED letters, size and position. Ring colours
(papers/series-five-orders/series_line.py ON_DARK, the exact element colours of the DICTO square): Earth (cube) green (72, 142, 72),
Water (icosahedron) blue (58, 112, 205), Fire (tetrahedron) red (205, 62, 40), Wind (octahedron) yellow (232, 200, 82), Void
(dodecahedron) violet (138, 92, 196). Legibility on the cover ground (20, 15, 11), contrast ratio: green 4.75, blue 3.97, red 3.91,
yellow 11.6, violet 4.00 (all above 3 for large lettering; read whole and at thumbnail size on the compare sheet), so no colour was lightened.

Run: python scripts/series_covers.py <papers> element (-> <cover>-series-v3.png); Platonic Solids: SERIESCOL=element python
../2026-11-15-platonic-cover-circle/scripts/compose.py <papers>/book-platonic/cover/platonic-cover-front-series.png
<papers>/book-platonic/cover/platonic-cover-front-series-v2.png (SERIESCOL=full -> platonic-cover-front-series-full.png in this
folder, the whole line in yellow, for comparison only); python scripts/compare_sheet.py <papers> COVERS-series-line-colour.png colour.
Checks: the white mode reproduces all ten v2 covers and the Platonic cover byte for byte; each v3 differs from its v2 only inside
the series line's box; FINAL ok for all eleven covers. Not in any book yet: each takes its cover at its next version (concordance next_versions).

## DECIDED 16 Nov 2026: fully (v4)

DICTO: "3 fully". The whole series line is in the ring's element colour (python scripts/series_covers.py <papers> full ->
<cover>-series-v4.png; Platonic Solids: platonic-cover-front-series-full.png copied to book-platonic/cover/platonic-cover-front-series-v4.png).
FINAL ok for all ten covers plus the Platonic cover. The partial (v3) files stay for comparison only. Each book takes its v4 cover at
its next version (Concordance next_versions updated); no cover-only releases.
