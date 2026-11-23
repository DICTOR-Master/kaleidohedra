# Palomar entries: why the papers' PDFs display badly (study, 24 Nov 2026)

INVESTIGATION ONLY: nothing published, no record changed. Report: DICTO saw "too much data or a similar issue" when opening the papers of his Palomar entries.

**Conclusion.** Palomar does not hold or embed the PDFs: each record lists the paper as a source with its Zenodo concept DOI, and the PDF is shown by Zenodo's own pdf.js previewer, which downloads the whole file at once. All four PDFs carry very large raster figures (up to 920 ppi, one of 25.7 megapixels), which is where both the size and the memory go. A light build (figures above 450 ppi resampled to 300 ppi at their printed size, lossless) makes #113 2.77 MB instead of 8.06 MB with identical text, and its slowest page renders 8 times faster. Since every Palomar record cites the concept DOI ("all versions"), a new Zenodo version fixes the display with no Palomar change.

## 1. How Palomar shows the paper

| Entry | Paper | Cited in the record as | Resolves to (latest Zenodo version) |
|---|---|---|---|
| PALOMAR-2026-11-20-000003 v1 | #113 Dehn Canon | doi:10.5281/zenodo.24383552 (concept) | record 24391370 (v2), 8,059,014 B |
| PALOMAR-2026-11-21-000004 v1 | #116 4D Dehn–Hadwiger | doi:10.5281/zenodo.24393967 (concept) | record 24429531 (v4), 6,320,886 B |
| PALOMAR-2026-11-20-000013 v1 | #115 Grünbaum k = 10 | doi:10.5281/zenodo.24389006 (concept) | record 24396137 (v2), 3,596,588 B |
| PALOMAR-2026-11-17-000006 v2 | #103 Kulaichev Yantra | doi:10.5281/zenodo.24052633 (concept) | record 24393733 (v8), 7,542,872 B |

The local PDFs are byte-identical in size to the Zenodo files (checked through the Zenodo API).

- The registry site (palomar-registry.org, PalomarWeb `bibliography.mjs`) turns `doi:` identifiers into plain links to doi.org. Its only iframe (`challenge-presentation.mjs`) shows the Challenge rendering (Verso HTML from data.palomar-registry.org), never a PDF. No PDF is uploaded to Palomar or taken from the GitHub repositories (the source trees hold no PDF).
- Palomar's docs (submit.palomar-registry.org/llms.txt, PalomarPolicy CONTRIBUTING and specification linked there) state limits only for Lean sources (10,000 lines per file; Challenge 1,000 lines and 100 KiB; HTTPS intake scan 32 files, 1 MiB each, 4 MiB total). No PDF limit, because Palomar handles no PDF.
- Zenodo shows a PDF with invenio-previewer's pdf.js previewer (zenodo-rdm `invenio.cfg`: `PREVIEWER_PREFERENCE` puts `pdfjs` first) and sets `PREVIEWER_PDF_JS_DOCUMENT_INIT_PARAMS = {disableStream, disableRange, disableAutoFetch: True}`: the whole file is fetched before page 1 appears. invenio-previewer's pdfjs extension sets no size limit for PDFs (`PREVIEWER_MAX_FILE_SIZE_BYTES` = 1 MB applies only to previewers that load whole text-like files).
- Scripted access to Zenodo's preview URL was refused (HTTP 403, "Access to this resource has been restricted due to unusual traffic from your network"). So the exact page DICTO saw was not reproduced here; see Open points.

## 2. Diagnosis of the four PDFs

All four: Chromium (Skia/PDF) print, A4, fonts embedded and subset (CID TrueType, Identity-H). Vector content is negligible (most pages under 10 path operators; maximum 162 on #103 p17). The weight is raster figures, stored Flate (lossless) at far more than print resolution.

| PDF | Pages | Size | Image streams | Largest figure (px) | Highest ppi |
|---|---|---|---|---|---|
| #113 | 23 | 8.06 MB | 7.76 MB | 6072 × 4236 (25.7 Mpx), p9 | 920 (p13) |
| #116 | 18 | 6.32 MB | 6.07 MB | 3760 × 3040 (11.4 Mpx), p6 | 542 |
| #115 | 14 | 3.60 MB | 3.40 MB | 4580 × 2736 (12.5 Mpx), p6 | 660 |
| #103 | 44 | 7.54 MB | 7.12 MB | 4268 × 4232 (18.1 Mpx), p34 | 724 |

The DICTO mark (360 × 360) on every page is one shared object: not a cost. Decoded for display, a 25.7 Mpx figure is about 103 MB of RGBA pixels; Safari on iPad and iPhone limits a canvas to 16.7 Mpx (4096 × 4096), which #113 p9 and #103 p34 exceed.

**pdf.js render timing** (pdfjs-dist 4.10.38 in headless Chromium, Zenodo's init parameters, every page drawn at scale 1.5, one run on a shared compute host at load average about 20, so times are indicative):

| PDF | Open | All pages | Slowest page | Peak memory (browser tree) | Failed pages |
|---|---|---|---|---|---|
| #113 | 105 ms | 2.26 s | p9, 749 ms (1,025 ms in an earlier run) | 741 MB | 0 |
| #116 | 110 ms | 0.87 s | p6, 141 ms | 614 MB | 0 |
| #115 | 156 ms | 1.44 s | p6, 438 ms | 644 MB | 0 |
| #103 | 130 ms | 1.92 s | p34, 200 ms | 781 MB | 0 |

On a desktop browser every page renders; nothing fails. The slow pages are exactly the pages with the largest figures. The likely failure is on a device with less memory (iPad: DICTO works on one), where the whole-file download plus the decoded large figures exceed the tab's limits; not tested on an iPad here.

## 3. The fix: a light print

`light-print.mjs` (this folder) is the same `page.pdf` call as `papers/print.mjs`, preceded by one step in the page: the page is laid out at its printed width (180 mm column = 680 CSS px), and every figure whose resolution there exceeds 450 ppi is redrawn on a canvas at 300 ppi of its printed size (high-quality smoothing, PNG kept lossless; JPEG sources would stay JPEG at quality 0.92). Milder resampling is skipped on purpose: smoothing makes flat-colour renders compress worse, and a 0.9 threshold left #103 at 7.37 MB. Fonts are already subset; vector figures need no rasterising (there are none heavy).

**#113 before and after** (test build with `light-print.mjs` from the released v2 source, paper.html unchanged since commit 994b5bc4):

| | Original v2 | Light |
|---|---|---|
| Size | 8.06 MB | 2.77 MB (−66 %) |
| Pages | 23 | 23 |
| Text (pdftotext) | | identical, 0 diff lines |
| Largest figure | 25.7 Mpx (103 MB decoded) | 3.7 Mpx (15 MB decoded) |
| Highest ppi | 920 | 412 (a figure left as it was) |
| pdf.js: all pages | 2.26 s | 1.00 s |
| pdf.js: slowest page | 749 ms (p9) | 89 ms (p1) |
| Peak memory | 741 MB | 605 MB |

A 300 dpi crop of p13 (the 63-piece icosahedron figure) shows no visible difference between the two.

**The other three** (light builds from the current sources, for size only; not checked against their released text):

| PDF | Original | Light | Largest figure after | Slowest page after |
|---|---|---|---|---|
| #116 | 6.32 MB | 2.96 MB | 3.65 Mpx | 82 ms |
| #115 | 3.60 MB | 1.69 MB | 2.70 Mpx | 133 ms |
| #103 | 7.54 MB | 5.77 MB | 4.30 Mpx | 141 ms |

#103 stays larger because it has some twenty mid-size figures at 250 to 380 ppi; 200 ppi for those gives 4.17 MB (section 4).

**Proposed target** for every paper: under 4 MB, no figure above 4 Mpx (inside the iPad canvas limit with room), every page under 0.3 s in the timing script. Proposed change: add the resampling step to `papers/print.mjs` as the default for final prints (an env switch for the full-resolution print), then run `papers/guard_regress.sh` as its header requires; add a guard that warns when a printed PDF exceeds 4 MB or carries an image above 4 Mpx.

**Records that would need a new version** (each only after DICTO's read ok of the new PDF): Zenodo #113 (concept 24383552), #116 (24393967), #115 (24389006), #103 (24052633). The Palomar records need no change: all four cite the concept DOI ("all versions"), which resolves to the newest Zenodo version.

## 4. Implemented (24 Nov 2026)

- `papers/print.mjs`: the light print is now the DEFAULT. Each figure's printed width is measured on a second page laid out at the printed column width (print media); figures above 450 ppi are redrawn at 300 ppi (lossless PNG; JPEG at quality 0.92) and swapped in, an unsized figure keeping its old width as a `width` attribute so the layout does not move. `FULL_RES=1` prints figures as they are.
- SIZE GUARD in `print.mjs` after every print: warning above 4 MB or for a figure above 4 Mpx (pdfimages); a figure above 16.7 Mpx (iPad and iPhone canvas cap) is an error: the PDF is removed, exit 11. A first version that swapped figures through `srcset` left Chromium printing the originals; the guard caught it (#113 p9 6072 × 4236), and the swap now goes through `src`.
- `guard_regress.sh` with the new `print.mjs`: all eight translated books (Quanta and Dictonary in ja, zh, fa, ar) "written".
- #113 end to end through its `build.sh`: figures, number audit (AUDIT OK), edgecheck, FIGCHECK OK; its last step stops as it should ("DRAFT without the red status box": the released source has no status box), so the final print was run by hand, `node print.mjs 2026-11-19-dehn-canon LIGHT-113.pdf "The Dehn Canon"`.

**Light PDFs, prepared, not published** (reading folder, `LIGHT-113.pdf` … `LIGHT-103.pdf`, each from its released source, same footer as released):

| PDF | Released | Light | Pages | Text against the released PDF |
|---|---|---|---|---|
| #113 v2 | 8.06 MB | 2.77 MB | 23 | identical |
| #116 v4 | 6.32 MB | 2.97 MB | 18 | identical apart from blank lines (pdftotext) |
| #115 v2 | 3.60 MB | 1.69 MB | 14 | identical |
| #103 v8 | 7.54 MB | 5.77 MB | 44 | same words; reference 12's kanji now set in Noto Sans CJK JP instead of WenQuanYi Zen Hei (the print host's font fallback, not the light print), so pdftotext orders them differently; the page looks the same |

#103 stays above 4 MB (warning only: one figure of 4.3 Mpx, p5); the 200 ppi option (`LIGHT_DPI=200`, tested) brings it to 4.17 MB, still just above the 4 MB mark; DICTO's choice. The released PDFs from 20–22 Nov were printed by Chromium m153, the light ones by m156.

New Zenodo versions of #113, #116, #115, #103 wait for DICTO's read ok; the Palomar records need no change.

## Open points

- The exact message and device: DICTO's words "too much data or a similar issue" were not reproduced. Which device and which paper showed it would confirm the cause (an iPad memory limit is the likely one; a Zenodo rate-limit page is the other possibility, since Zenodo answered scripted preview requests with "unusual traffic").

## Sources checked

- Palomar public records: data.palomar-registry.org `/entries/PALOMAR-2026-11-20-000003-v1.json`, `-11-21-000004-v1`, `-11-20-000013-v1`, `-11-17-000006-v2`; `/recent.json`; `/repositories/dictor-master/<repo>.json`.
- Palomar site code (palomar-registry.org assets: `app.js`, `bibliography.mjs`, `entry-pages.mjs`, `challenge-presentation.mjs`, `security.mjs`) and the page's Content-Security-Policy.
- Palomar docs: submit.palomar-registry.org/llms.txt and the PalomarPolicy documents it links.
- GitHub source trees of dehn-canon-lean and dehn-hadwiger-4d-lean at the registered commits (no PDF).
- Zenodo REST API records 24391370, 24429531, 24396137, 24393733; zenodo-rdm `invenio.cfg` and `site/zenodo_rdm/previewer/image_previewer.py`; invenio-previewer `config.py` and `extensions/pdfjs.py` (GitHub, master).

## Files

- `analyse_pdf.py`: per-page operator counts, content and image bytes (pikepdf); output `analysis.json`.
- `render.html`, `render-time.mjs`: pdf.js timing harness (served over local HTTP; Playwright); outputs `render-before.jsonl`, `render-final.jsonl`.
- `light-print.mjs`: the light print test.
