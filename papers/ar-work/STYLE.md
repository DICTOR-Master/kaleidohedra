# Arabic editions of DICTO's Quanta of Space (Vol. I, EN v2.1) and The DICTOnary of Atoms (Vol. II, EN v1.2)
DICTO 2026-11-07: "farsi next maybe arabic after that" · "no both same for arabic". Accuracy is what matters.
The English files (quanta/NN-en.html, dictonary/NNN-en.html) are the authority. Write the Arabic next to each: quanta/NN-ar.html, dictonary/NNN-ar.html.

## Rules
1. Meaning: every claim, number, count, name, date, DOI, condition and qualifier of the English, correctly; nothing added. Numbers, formulas, coordinates and table values identical.
2. Script and direction: Modern Standard Arabic in Arabic script (Arabic ي and ك; standard hamza and taa marbuta). The page is right-to-left (the lead sets dir="rtl" on <html>). Keep LATIN DIGITS 0–9 everywhere (not ۰–۹), so numbers match the English exactly. Wrap every formula, number expression with operators or letters (e.g. 1/φ², (3,1,0,0), μ = √3, x + y = k), every DOI/URL/file path and every Latin name run in <span dir="ltr">…</span> so it is not reordered.
3. Terms: glossary-ar.tsv (English → Arabic) is binding once the lead's glossary pass has written it; atom-names-ar.tsv likewise. Standard geometry terms follow Arabic Wikipedia and standard Arabic mathematical usage (extracts in wikipedia-ar/).
4. DICTO's names: Latin-capital names (DICTO, AXE, CLEO, FUJI, EKP, HexOct, GTT, Kaleidohedra, Polyhedraverse) stay in Latin inside <span dir="ltr">. Other piece/shape names: translated by meaning where they are ordinary words (White Queen الملكة البيضاء, Red Queen الملكة الحمراء — as in Arabic translations of Through the Looking-Glass), transliterated when coined; the English name once in () at the first use in each book. Same shape = same Arabic name everywhere.
5. No English words left in running text except: Latin-capital names, DOIs/URLs, file paths, software names, reference lists (authors, journals, titles stay in Latin, each list item may be dir="ltr"), and a term with no settled Arabic form, described in Arabic with the English once in ().
6. Book titles in «» (guillemets), without <i>: Quanta of Space: A Manifesto → «كمّات الفضاء — بيان» (lead may refine); The DICTOnary of Atoms → «معجم ذرات DICTO — كمّات الفضاء II»; others translated, DOI kept.
7. Credit lines: "DICTO proposed / DICTO's idea" → «اقترح DICTO» / «فكرة DICTO»; never "asked". "Computation … with Claude (Anthropic)" → «الحسابات … بالتعاون مع Claude (Anthropic)». Title page adds: «الترجمة بالتعاون مع Claude (Anthropic)».
8. Keep every HTML tag, class, img src path, link and DOI exactly (adding only the <span dir="ltr"> wrappers). Volume labels: المجلد I / المجلد II. Register: formal Modern Standard Arabic.

## Report
Return the report as text in your final message (subagents cannot write report files): per file, terms added or unsure, problems in the English.


## Lead decisions (after the glossary pass)
- glossary-ar.tsv (613) and atom-names-ar.tsv (207) are BINDING; the UNSURE picks stand (Hypsicles in the classical form إبسقلاوس; Through the Looking-Glass «عبر المرآة»).
- Volume labels: المجلد I / المجلد II. The Arabic Wikipedia extracts are in wikipedia-ar/.
- The Alice note (Quanta ch. 6, div.namesbox) is translated like any text.
- Book titles in «» without <i> (rule 6 wins over keeping <i>).
