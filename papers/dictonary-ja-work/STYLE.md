# Japanese DICTOnary of Atoms: accuracy pass rules (same rules as the Japanese Quanta v2, published 24028277) (DICTO 11-07: accuracy, not linguistic style)
Each unit NNN in units/ has NNN-en.html (the English source, The DICTOnary of Atoms v1.1 — the authority) and NNN-ja.html (the Japanese draft, made from v1.0, to correct in place). The English v1.1 added two atoms, D133 DICTO Void Keeper and D134 DICTO Golden Skin (unit 004 has 102 atom entries in English, 100 in Japanese): add them, translated, in the same place and format.

## What to fix
1. Meaning: every claim, number, count, name, date, DOI, condition and qualifier in the English must be in the Japanese, correctly. Nothing added that the English does not say. Missing sentences → translate and add. Mistranslations → fix (example found in ch.6: "icosidodecahedron" had become 二十面体; "snub" had become いぶし; four-dimensional regular solids had become 正多面体).
2. Terms: use glossary.tsv (536 entries: English, Japanese, note) wherever its English term occurs, consistently. Piece and shape names exactly as in the glossary (e.g. Kagemusha → 影武者; Cleo-Icos → クレオ・イコス; White/Red Queen → 白の女王/赤の女王; Kepler–Poinsot → ケプラー・ポアンソ).
3. Standard terms (Japanese Wikipedia / Miyazaki): regular polytope 正多胞体; 600-cell 正六百胞体; 120-cell 正百二十胞体; tesseract 正八胞体（テッセラクト）; cell/face/edge/corner 胞/面/辺/頂点; polar partner 双対; uniform polytope 一様多胞体; icosidodecahedron 二十・十二面体; snub dodecahedron 変形十二面体; snub cube 変形立方体; Platonic solids プラトンの立体; Archimedean solids アルキメデスの立体; space-filling 空間充填; rhombic dodecahedron 菱形十二面体; rhombic triacontahedron 菱形三十面体; golden ratio 黄金比; golden cut 黄金切断 (never 黄金分割, which is the golden section); slice 断面; shadow 影; honeycomb 空間充填形（ハニカム）.
4. No English words left in running text, except: names in Latin capitals (DICTO, AXE, CLEO, FUJI, EKP, GTT…), DOIs/URLs, and a term with no settled Japanese equivalent, which is DESCRIBED in Japanese with the English once in （）, e.g. 頂点を辺の中点まで切り落とした六百胞体（rectified 600-cell）. Book titles in Japanese per glossary (Alicia in Wonderland → 『不思議の国のアリシア ― 赤の女王と白の女王』; "Full chapter:" → 全章：『…』第n章).
5. Broken markup in v1 (e.g. <h1><html><body><p>…</p></body></html></h1>) → plain <h1>…</h1>. Keep all other tags, classes, figure images, src paths and DOIs exactly.
6. The note （数式・計算の詳細は英語版をご覧ください。） only where formulas or computations of the English really were left out; delete it where nothing was left out.
7. Register: keep です・ます as in v1. Do not polish style; change wording only to fix meaning or terms.
8. Credit voice: "DICTO proposed / DICTO's idea" → DICTO が提案した / DICTO の着想; never "asked" (〜と尋ねた) or "selected by".

## Report
Write dictonary-ja-work/fixes-<batch>.md: per section, a numbered list of each fix (v1 → v2, one line, why). Then the count of fixes per section.

## Lead decisions after batch 3 (apply in the final sweep over ALL sections)
- Book titles: 『』 without <i> (Japanese convention).
- Data line: 第 II 巻 everywhere (not 巻 II, 第2巻).
- truncated triangle → 切頂三角形 (as 切頂四面体; DICTO's term, never the flat-ended form).
- disdyakis triacontahedron → 六方二十面体 (ja Wikipedia).
- Vajra (piece) → ヴァジュラ everywhere (one name per shape; glossary VAJRA).
- The DICTOnary of Atoms (Vol. II) cited as 『DICTO 原子辞典 ― 空間の量子 II』 (title of the Japanese edition).
- #29 "two exact stories" → 二通りの正確な道筋; "In the stations" → 段階ごとの版では.
- Names: Smarandache スマランダケ, Grünbaum グリュンバウム, Klitzing クリッツィング (batch-3 list accepted).
## Lead decisions after batch 2
- cut-and-project → 切断射影法; window → 窓 (first use 窓（受容領域）).
- scutoid → スクトイド.
- spinel law → スピネル式双晶則.
- Golden Cut names (DICTO's): 大黄金切断／小黄金切断＋solid (大黄金切断四面体, 小黄金切断立方体, 黄金切断菱形十二面体 …).
- Cleo-Ico (English variant) → クレオ・イコス (same piece).
- Volume II → 第 II 巻 (all batches).
- App labels: Japanese, as the apps' Japanese interface.

## DICTOnary specifics
- Book title (this Japanese edition): 『DICTO 原子辞典 ― 空間の量子 II』; Volume I: 『空間の量子 ― マニフェスト』 (第 I 巻). Katakana cover title: ディクトナリー・オブ・アトムズ.
- Atom names (D1…D134): Japanese per the glossary; where the glossary has none, translate common nouns and keep DICTO's coinages in katakana, with the English name once in （） in the catalogue entry only. The same atom must have the same Japanese name everywhere in the book (catalogue, data chapters, known-shapes list).
- Catalogue field labels (solid · finding · Volume I, …) translated consistently, the same in every entry.
- Reference lists, patent numbers, author names in citations: keep in Latin.
- Large tables of numbers: numbers and coordinates must be identical to the English; translate only headers and words.
