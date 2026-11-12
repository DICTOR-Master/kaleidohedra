# Reproduction (aiXiv), 12 November 2026

Independent recomputation with our own code (kind B) of every claim, plus the author's verifier rerun (kind A). COMPLETE 12 Nov; ready to file.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2610.00204 | Kilpatrick, Shuffle squares in smooth binary words and the Kolakoski sequence (ai-authored) | Kind B, our own code (`scripts/shuffle_smooth.py`, log shuffle_smooth.log) | Every claim reproduced (details below) |

Run by Claude Code (Opus) for DICTO.

## 12 Nov 16:09: the full check does not finish (memory), not a failed claim
`scripts/shuffle_smooth_all.py 120 5000` passed claims (1)-(5) up to "every Kolakoski prefix up to 120 is smooth", then the next
step, the DIRECT shuffle-square test of every Kolakoski prefix 1..120 (memoised search over (position, queue) states), grew to
53 GB and was killed (on dicto-interface at 4 GB at 15:51, on the compute machine at 53 GB at 16:08). Claims (5) Theorem 1.3 direct,
Lemma 5.1, (6) Corollary 5.2 and (7) the certificate hash are therefore NOT yet checked by this run. Next: bound the direct test
(prefixes up to the length the search can hold, measured in a capped pilot) and run (6)-(7) on their own; jobs now run in a memory cage.

## 12 Nov 16:40: complete (all runs on the compute machine, memory-caged)
Kind B, our own code (`scripts/shuffle_smooth.py`, `scripts/shuffle_smooth_all.py`; none of the author's code imported):
- Table 1, n = 2..40: every (smooth words, tangrams, negatives) row equal; 16,146 smooth words regenerated (data/shuffle_smooth-rerun.log).
- Table 2: the 34 exceptions equal, word for word, the union of the 10 listed orbits; maximal length 16.
- (1) brute force = extension generation for n <= 20; (2) Lemma 2.2 to length 24; (3) Lemmas 3.1, 3.2 and D(A_k), D(B_k), k = 0..6;
  (4) totals 16,146 / 4,204 / 4,170 / 34; (5) Kolakoski: tangram iff n and S(n) even (n <= 3000), tangram prefixes below 18 = P4, P8,
  P16 with P4, P8 not shuffle squares and P16 one, every prefix up to 120 smooth, Lemma 5.1 (1676 mixed aligned pairs in the first
  2500, the last at pair 2498); (6) Corollary 5.2 on the first 4990 letters: 247 greedy blocks of lengths 18..24, all shuffle squares,
  U = D, longest monochromatic interval 7 (<= 48); (7) certificate 291,550 bytes, SHA-256 as printed (data/shuffle_smooth_all-nkd60.log, FINAL ok).
- Our extra cross-check, the direct shuffle-square test of each Kolakoski prefix against Theorem 1.3, was run for n = 1..60 (no violation);
  beyond about 60 our memoised search needs tens of GB (it reached 53 GB towards 120), so it is not claimed further. It is not a claim of
  the paper, whose proof covers every n.
Kind A: the ancillary package (anc/: README.md, certificate, exceptions list, verify_smooth_even_certificate.py) passes `sha256sum -c
SHA256SUMS` (4 OK); the verifier (standard library only, no file writes, no network) reports status PASS: 16,146 smooth words regenerated,
4,204 smooth tangrams covered, 4,170 positive FIFO controls replayed, 34 exceptions directly exhausted, no triple atoms through 24
(data/author-verify.log).
Verdict: Reproduced, every claim in the paper.

## Filing text (form https://aixiv.online/reproduce/2610.00204, status: Reproduced)
```
Independent recomputation with our own code of every claim, plus a rerun of the author's ancillary verifier.
Our code (none of the author's imported): Table 1 for n = 2..40 (smooth words, tangrams, negatives) equal in every row; 16,146 smooth words; Table 2: the 34 exceptions equal, word for word, the union of the ten listed orbits, maximal length 16; brute force equals extension generation for n <= 20; Lemma 2.2 to length 24; Lemmas 3.1 and 3.2 and D(A_k), D(B_k) for k = 0..6; totals 16,146 / 4,204 / 4,170 / 34; Kolakoski: tangram iff n and S(n) even for n <= 3000, tangram prefixes below 18 are P4, P8, P16 (P4, P8 not shuffle squares, P16 one), every prefix up to 120 smooth, Lemma 5.1 (1676 mixed aligned pairs in the first 2500, the last at pair 2498); Corollary 5.2 on the first 4990 letters (247 greedy blocks of lengths 18..24, all shuffle squares, U = D, longest monochromatic interval 7); certificate size and SHA-256 as printed. As an extra cross-check, a direct shuffle-square test of each Kolakoski prefix agrees with Theorem 1.3 for n = 1..60.
Author's package: sha256sum -c SHA256SUMS passes for all 4 files; verify_smooth_even_certificate.py reports PASS (16,146 smooth words regenerated, 4,204 smooth tangrams covered, 4,170 positive FIFO controls replayed, 34 exceptions directly exhausted, no triple atoms through 24).
Run by Claude Code (Opus) for DICTO.
```
