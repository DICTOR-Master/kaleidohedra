# Next OEIS sequence: which queued candidate has a citable source (24 Nov 2026)

DICTO's rule: a sequence goes in only if its terms or its formula are printed in a released paper with a DOI.
Released PDFs checked: #102 v6 (record 24241321) and #111 v2.1 (record 24429547) were downloaded from Zenodo and are
byte-identical to the local PDFs. #69 v2 (record 23723070) was read in the local v2 PDF; Zenodo refused the download (rate limit).
OEIS searched 24 Nov 2026 (fmt=short).

| Candidate | Printed in a released paper? | In OEIS? | Readiness |
|---|---|---|---|
| Sweep 2: closed tailless walks per pyrochlore site | YES. #102 v6 (DOI 10.5281/zenodo.24037664), Corollary 2: "loops 0, 0, 12, 12, 0, 276, 756, 2988, …" (n = 1..8), and the theorem that every stacking gives these counts. Formula (Ihara–Bass, q = 5, applied to the closed walks) is in the proofs (Lemma 3, proof of Cor. 2), not as a closed form | No (12,12,0,276,756,2988,16104: no match) | READY: n = 1..40, two methods agree for n = 1..30 (formula and direct Hashimoto count); a second count to n = 40 would match Sweep 1's standard |
| Entries 3, 4, 5: 6H coordination sequences | NO. #74 v2 and the HexOct book print only diamond's and lonsdaleite's shells (24, 42, 64, 92 / 25, 44, 67, 96) and a figure for 4H, 6H; no 6H terms, no g.f. | No (1,4,12,24,42,64,92,127,168,213: no match) | Not citable as it stands; needs a paper that prints the terms |
| Entry 6: the Fibonacci stacking word | YES. #69 v2 (DOI 10.5281/zenodo.23721038) prints the rule (types by c → ch, h → c; steps ±1, a cubic layer repeats the step, a hexagonal one reverses it) and the first 16 and 26 letters (ABACBCACBABCACBC, ABACBCACBABCACBCABACABCBAC) = a(0..25) | No. 16 terms hit A036581/A036579 (ternary Thue-Morse) by chance; 28 terms: no match | READY |
| Entry 8: cot(2π/7), r/R of the 14-face die | YES. #111 v2.1 (DOI 10.5281/zenodo.24379796): Theorem 2 (b) "r/R = cot(2π/7) = 0.797473…", proved; Table 1 r/R = 0.7974733889; abstract. (#112 does not state it.) So it need not wait for The Golden Ladder v8 | No (7,9,7,4,7,3,3,8,8,8,8,2,4,0: no match) | Nearly ready: irreducibility of 7x^6 − 35x^4 + 21x^2 − 1 and the PARI line still to run (ENTRIES.md) |

Type-B Vacuus count (5^n − 2·3^n + 1)/2 = 0, 0, 4, 36, 232, 1320, 7084, … = 2·A007798(n) (A007798 = 0, 0, 2, 18, 116, 660, 3542, …, offset 0, checked against its data). So it is a COMMENT on A007798, not a new sequence, and it waits for the Vacuus and Resonus paper's release.

RECOMMENDATION: Sweep 2 next. Its terms and the theorem behind them are printed in #102, it is not in the OEIS, it shares #102 and its working method with Sweep 1, and it completes the set with A400949 (diamond) and A402231 (fcc). Entry 8 comes after it: its home (#111) is now released.
