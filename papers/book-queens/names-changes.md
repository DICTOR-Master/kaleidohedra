# Alicia in Wonderland: The Red & White Queens, Version 6 draft of 17 November 2026: changes

DICTO's answers of 17 Nov 2026 to the three questions of the status box: "split it, leave nothing out, go ahead". Also: #109 and #110 fold fully into this book (consolidation map rows #109, #110); the golden station of #110 is named Valley Charge.

Files edited: paper.html (the book source; assemble.py is no longer re-run, as paper.html carries hand edits since v4), front.html (Opening and "What this book will show" kept equal to paper.html), epilogue.html (equal to the Epilogue in paper.html). Figures: figures/ch10 → figures/ch11 (five #110 figures moved with their section), figures/ch11/fig-opener.png and figures/chA/ (six figures) copied from #109's folder. Not touched: papers #107, #109, #110; plates; cover; series page; assemble.py, build_next.sh. Nothing committed. Backups of paper.html, front.html and epilogue.html as they were: the session scratchpad, bk-queens/.

## 1. Structure

| before | after |
|---|---|
| Ch 10 "The Queens' walls and their cats" (working title) | Ch 10 "The Queens' walls" (working title): §1 the Vacuus in three kinds; §2 the walls the Queens share (cross walls justified from the 25 inscribed 24-cells, as in #110 v2), the Mirror Law and the Queens' faces (#107), Table 10.1, the midpoint; §3 Valley Charge; §4 what is known |
| | Ch 11 "The Queens' cats" (working title): the cat and the meat; §1 the silent solids hidden in the White Queen's walls (Lemma 3, Theorem A, Table 11.1); §2 hidden is not silent (the controls); §3 weighing the cat; §4 the cats in the Red Queen (Theorem B, Table 11.2, the half-cats); §5 the dual cats (Theorem B′); §6 what is known |
| Plates, Epilogue, Appendix. Sources by chapter | Plates, Epilogue, **Appendix A** (#109 in full), **Appendix B** (#110 in full), **Appendix C**. Sources by chapter |

Choice: the full papers are appendix chapters after the Epilogue, not a closing Part before it, so the story runs unbroken from Chapter 1 to the Epilogue, and the proofs follow as the record. Contents, "What this book will show" (now eleven results), the Epilogue (story paragraph, results table with rows 10, 11 and A–B, open problem (9) added) and the Index (recounted for Chapters 10, 11, A and B; new terms Valley Charge, Golden Truncated 5-cell, Golden Cantellated 5-cell, Mirror Law, snub 24-cell, grand antiprism, Schläfli) follow the new structure.

Working titles for DICTO: Chapter 10 "The Queens' walls", Chapter 11 "The Queens' cats" (marked as his to name in the status box).

## 2. What came in from each paper (leave nothing out)

**#109 Silent Running: Twisted Silence, Version 2** (DICTO DOI 10.5281/zenodo.24272473; v2 record 10.5281/zenodo.24295161). Appendix A gives all of it: credits and DICTO's contributions (from the meta line), abstract, §1 Running silent, §2 tones/silence/labels and reproduction, §3 Main theorem, Theorems 1, 2, 4, Propositions 3, 5, 6, 7, Tables A.1 (twisted characters) and A.2 (V_k restricted to 2I), Figure A.1 (five orbits), A.2 (moment rigidity); §4 all proofs; §5 the two silent solids with Figures A.3, A.4; §6 the census of 3232 sets (Table A.3), the Sym6 and E8 cases, signatures across groups (Table A.4); §7 the sonar dial (Figure A.5), the inverse question; §8 the crystallographic analogy (Proposition 8); §9 the fourth kind of forced law (Figure A.6); §10 open problems and prior art; references [1]–[40]; sources checked. Not repeated: the opening figure (now Figure 11.1) and the lofargram (Figure 9.1). Chapter 9 §6 keeps its retelling and now points to Appendix A.

**#110 Walls of Silence: The Walls of the 4D 600-cell and 120-cell, Version 2** (DICTO DOI 10.5281/zenodo.24272477; v2 record 10.5281/zenodo.24296556). Appendix B gives all of it: credits and DICTO's contributions, abstract, §2 definitions (with the justification of the cross walls), reproduction, §3 Lemma 1, Proposition 2 and Table B.1 (index law on S5-orbits), §4 Lemma 3, Theorem A, Proposition 4 (the special cuts, their count 314,248,344), §5 Theorem B, Proposition 5 (the half-cat patterns), Theorem B′ with the fewest covers certified optimal by DRAT proofs (CaDiCaL, checked by drat-trim; HiGHS and CP-SAT agree), §6 Theorem C (chambers of the 360 and the 1560 walls, the 298 pieces of 15 types), §7 Table B.2 and Proposition 6 (Valley Charge), §8 what "hidden" shows (chance baseline, ordinary orbits), §9 conjectures and questions, §10 observations (skeletons, volumes and overlaps, censuses), §11 the intersection lattices (Table B.3; the paper's Appendix B), references [1]–[21], sources checked. Not repeated: its nine figures (Figures 5.4, 5.5, 10.1, 10.2, 11.2–11.6) and its Tables 2 and 3 (Tables 11.1, 11.2); its §1 opening story (told in Chapter 11) and its §10 Shadows (given in full in Chapter 5 §10) are pointers.

Into the story chapters as well (from the old "Kept out" list, now in): the special-cut count, the chance baseline and the off-corner orbits (Ch 11 §2); the volumes and overlaps (Ch 11 §3); the half-cat patterns (Ch 11 §4); the DRAT certificate, (e) and (f) of Theorem B′, the skeletons (Ch 11 §5); the 15 uniform H4 solids (Ch 10 §2); DICTO's wood-and-trees image and his proposal that found the dual cats (Ch 11). Still out, as before: the longer story of the cat and the meat (its home is A Brief Geometry of Space).

## 3. Names and credits

Rule: memory feedback-known-names-rediscovery (regular name* (discoverer, year); classical shapes he only named: "* Named X in DICTO's books."), applied with common sense because the title and the story use the Queens as characters.

| name in the book | what was done | where |
|---|---|---|
| 600-cell (White Queen) | first use in the book: "the 600-cell* (Schläfli, 1852)", note "* Named the White Queen in DICTO's books." | Opening (paper.html and front.html) |
| 120-cell (Red Queen) | "the 120-cell** (Schläfli, 1852)", note "** Named the Red Queen in DICTO's books." | Opening |
| both | "(Schläfli, 1852)" again at first use in Ch 10, Ch 11, Appendix A (abstract) and Appendix B (abstract); theorem statements in Ch 11 use the regular names (Lemma 3, Theorem A "hidden in the 600-cell", Theorem B and B′ in terms of the 120-cell and its inscribed 600-cells) | Ch 10 §1, Ch 11 §1, §4, §5, App A, App B |
| the Queens in the story | kept: "the White Queen", "the Red Queen" in the story's voice, chapter titles (Ch 6, Ch 8) and the plates | throughout |
| solid A, solid B | DICTO's names (#109/#110 v2): "the Golden Truncated 5-cell (A)", "the Golden Cantellated 5-cell (B)", DICTO's names, at first use; then A and B (labels in tables, theorems and figures) | Ch 9 §6, Ch 10 Fig 10.2, Ch 11 §1, Definitions used |
| C3 | "the uniform expanded 5-cell, labelled C3 here" (as in #110); orbit credited to Koca, Koç, Al-Barwani and Al-Farsi (2006). C3 kept as a label beside A and B | Ch 11 §1 |
| golden station of #110 | **Valley Charge** (DICTO, 17 Nov): Ch 10 §3 (new short section with Proposition 6), "What this book will show" (10), Epilogue, App B Proposition 6, §9 conjecture (iv) and prior-art list; added to "Definitions used" and the Index | Ch 10, App B |
| snub 24-cell | (Gosset, 1900) | Ch 11 §2, §6 |
| grand antiprism | (Conway and Guy, 1965) | Ch 11 §2, §6; Ch 10 §2 (the uniform H4 list, with Möller 2004) |
| special cuts | (Dutour Sikirić and Myrvold, 2008), with their count | Ch 10 Fig 10.2, Ch 11 §2 |
| A and B as hulls | credit corrected: the orbits are Koca et al.'s (Dynkin labels fixing the patterns), the cells, edges and faces are worked out in #109, the names and the Vacuus reading are DICTO's (was: "their description as the solids A and B ... are DICTO's") | Ch 11 §1, Ch 9 §6 |
| compound of ten 600-cells | (Coxeter, Regular Polytopes, Table VII) at its use | Ch 11 §4 |
| CaDiCaL, drat-trim | named as the tools of the certificate | Ch 11 §5, §6 |

### 3b. Known shapes in Chapters 1–9, front matter, plates, Epilogue, Index (second pass, 17 Nov)

DICTO, 17 Nov: "name rules apply everywhere … shapes mainly AXE etc should return to their origins"; published titles stay as published. Wording and notes as in the DICTOnary v1.4 and Quanta of Space v2.3 drafts: first use in each chapter = regular name* (discoverer, year); the note at the end of the chapter; later uses the short regular name. 119 replacements (log: session scratchpad names_log.tsv); backup before this pass: scratchpad bk-queens/paper-before-names.html.

| DICTO's name | regular name (short form) | credit | note | where |
|---|---|---|---|---|
| AXE | Mosseri–Sadoc tile t6, scaled by 1/φ (t6, tile t6) | Mosseri and Sadoc, 1982 | DICTO's name: AXE, for its axe-head shape, its sharp edge the blade. | Ch 1 (all ~34 uses, tables, captions, formulas such as I(φ²) = 12 I(1) + I(1/φ) + 60 t6 + 20 FUJI + 20 t4), Ch 3, Ch 4, Ch 5, "What this book will show" (1), Epilogue table |
| CLEO | Mosseri–Sadoc tile t4, scaled by 1/φ (t4) | Mosseri and Sadoc, 1982 | DICTO's name: CLEO, after Cleopatra's Needle, the obelisk in London. | Ch 1, Ch 2 ("reached from the Mosseri–Sadoc tile t4"), Ch 3, Ch 4, Ch 5, front, Epilogue |
| Tricap | Mosseri–Sadoc tile t3 | Mosseri and Sadoc, 1982 | DICTO's name: Tricap. | Ch 3, Ch 4, Ch 5 |
| Hound Tooth | Mosseri–Sadoc tile t2 | Mosseri and Sadoc, 1982 | DICTO's name: Hound Tooth. | Ch 4 (incl. "four t1 and two t2" for J13) |
| Cleo-Icos | the icosahedron's (face) pyramid; "icosahedron face pyramid" at first use | classical; Mackay, 1962 | DICTO's name: Cleo-Icos. | Ch 2 (25 uses, incl. Corollary 3 heading), Ch 3, Ch 4, Ch 5, Ch 6 (core of 20 face pyramids), Ch 8, front (2), (4), (6), Plate 14 table, Epilogue, Appendix C data notes |
| Dogstar | George Hart's dodecahedron stellation 8 (stellation 8) | Hart, 1996 | DICTO's name: Dogstar. | Ch 2 |
| DESHI | Gray's cage of twelve icosahedra | Gray, 2002 | DICTO's name: DESHI. | Ch 1 |
| Icosaxes | truncated octahedron x = φ | Koca et al., 2015 | DICTO's name: Icosaxes. | Ch 9 §5.1 |
| Alicia | cell-first section of the 600-cell at height 0 | Boole Stott, 1900 | Rediscovered by DICTO as Alicia. (front note also names Unicorn, Bandersnatch, Humpty Dumpty) | Opening ("Alicia and Alice"), Plate 8 table |
| Humpty Dumpty (D85) | cell-first section of the 600-cell at height 1 + √5/2 = (2 + √5)/2; "the 48-corner (cell-first) section" | Boole Stott, 1900 | Rediscovered by DICTO as Humpty Dumpty. | Ch 6 (abstract, Table, Fig 6.1/6.2 captions, §7, §8, conclusion), Plate 11 table, Definitions used |
| Unicorn | cell-first section at height (3 + √5)/2 | Boole Stott, 1900 | Rediscovered by DICTO as the Unicorn. | Plate 12 table |
| Bandersnatch | cell-first section at height (5 + 3√5)/4 | Boole Stott, 1900 | Rediscovered by DICTO as the Bandersnatch. | Plate 13 table |
| J11 | Johnson solid J11 | Johnson, 1966; Zalgaller, 1969 | (credit added; audit D) | Ch 1 abstract |

Kept, with the reason:
- Titles as published: "Chapter 1. AXE, CLEO and FUJI" (in Contents and Appendix C), the paper titles in references and in "Papers referred to" (#94 "… Finds Icosaxes, and Only Icosaxes").
- Credit lines and reference entries that record what DICTO named (Appendix C, Ch 1 credits "the names AXE, CLEO, FUJI, … DESHI … are DICTO's"), as in Quanta v2.3.
- Plate names (the large headings and the plate list: Alicia, Humpty Dumpty, Unicorn, Bandersnatch; "Cleo core", "Cleo shells") as the plates' titles; each plate's table now gives the regular name, Boole Stott's credit and the note. The plates' intro says these four are sections of her series under DICTO's names.
- Ch 6 §7 heading "six impossible things, and Humpty Dumpty's fall" and the three Carroll quotations (story's voice, quoted text); the running text of §7 uses Boole Stott's section.
- The cover description (WONDER square: "D Humpty Dumpty", "O Alicia") describes the cover art.
- The Queens as characters (as in §3 above); FUJI, Antonius, Admiral Cap, Kagemusha, Weirdstone, Tadpole, Fallen Humpty, the Lotus seed and DICTO's other new shapes keep his names.
- Index: AXE, CLEO, Tricap, Hound Tooth, Cleo-Icos, Humpty Dumpty entries renamed to the regular names with "(DICTO's …)"; Definitions used: the known names (Alicia, Bandersnatch, CLEO, Cleo-Icos, Dogstar, Icosaxes, Unicorn) dropped, D85 described as Boole Stott's section.
- Status box: the names question removed (answered); the pass described.

## 4. Errors, clarity, repetition

- Ch 9 §6: "the double silences occur only at isolated points, and the signatures ... only at X, F and their negatives" claimed more than #109 proves. Now: isolated points and the signatures only at X, F, −X, −F on the two edge circles (exact); a certified, not exhaustive, search off the circles found no others.
- Ch 9 §6: Theorem 1's scope "general for any finite subgroup of a compact group" → "for any finite group and any automorphism of it" (as #109 states it).
- Ch 9 §6: the box "Theorem 4 (the golden silences)" clashed with #109's own Theorem 4 (degree linkage), now in Appendix A; it is now "The golden silences (#109, Main theorem)". Same for Ch 10/11 labels: "Lemma 2 (face lemmas; #110 Lemma 3)" → "Lemma 3"; "Lemma 1 and the index law" → "Lemma 1 and Proposition 2"; "Theorem 1 (the Mirror Law)" and "Corollary 2" → "The Mirror Law (#107, Theorem 1)" and "The Queens' faces (#107, Corollary 2)", so every label matches its source and none clashes with Appendix B.
- Ch 10/11 face lemmas: "the counts per wall by symmetry, floating point" → exact (#110 v2's second implementation made the W(H4)-transitivity exact). Appendix B's proof of Lemma 3 says so (the paper's own proof text still says floating point; see ledger).
- Source lines: "#109 ... version 1, DICTO DOI 10.5281/zenodo.24272473" named the all-versions DOI as version 1; now Version 2 with the all-versions DOI (v2 record DOIs in the appendix heads). Same for #110 (Ch 5 §10, Ch 10, Ch 11).
- "What this book will show": "Each chapter is one paper, kept word for word" was not true of Chapters 3, 9, 10, 11; now says which chapters keep a paper word for word, which are first published here, which retell.
- DICTO's contributions written as proposals, not questions (print guard): Ch 11 "DICTO's idea of 16 November", "DICTO proposed that a premise might be at fault", App B "DICTO's proposal of 16 November", #109's credit "the questions" → "the proposals".
- Version history removed from the appendices (books state only what is right): #110 "stated in floating point in Version 1, is now exact" → "is exact"; #109 "now read" → "read"; the papers' "Version 2 adds/has ..." lines not carried. The book's own "Version 6 adds" line removed from the draft (it is written at publication); its content is in the status box.
- One AI credit line: the papers' "Computation, proofs, verification and drafting with Claude (Anthropic)." not repeated in the appendices (the book's meta line has it).
- Story told once: the cat and the meat now opens Chapter 11 only (it opened the old Chapter 10; Chapter 10 has its own hook); App B §1 points to it; "steak" → "meat" (the book's one meaning); Schrödinger's image told in Ch 11 §4, pointed to from App B §5.
- Appendix C (sources): two empty "References" headings (Chapters 3 and 9) removed; entries added for Chapters 10 (#107's sources and sources checked, word for word) and 11 (pointer to Appendices A and B). "Papers referred to, not in this book": #33, #107 and #108 added.
- Ch 5 §10 and Ch 9 §6 point to Appendices B and A; Ch 9's last paragraph points to Chapter 11 (was Chapter 10).

## 5. Ledger entries applied

- 17 Nov, DICTOnary: Atlas labels "W1: … R115:" → "slice N of #63/#65:" (also in: Alicia). Checked: this book carries no W-number or R-number atlas labels in its text, plates or captions (the plates already say "slice"); nothing to change. Marked carried for Alicia.
- No other ledger entry names this book.

## 6. Ledger lines added for other works

See consolidation-ledger.md (17 Nov, Alicia v6 draft): #110 Lemma 3 proof text vs its Reproduction paragraph (transitivity exact); #109/#110 now in full in the book (Concordance, consolidation map rows #109 and #110: PART → IN at publication); Valley Charge in #110's next version; Chapter 9's dial wording if retold elsewhere (A Brief Geometry plan).
