# Proof check: Kilpatrick, Shuffle squares in smooth binary words and the Kolakoski sequence (aiXiv 2610.00204 = arXiv 2610.02262v1)

Line-by-line read of every numbered result of the current version (12 results), 12 Nov 2026, by Claude Code (Opus) for DICTO.
Finite parts are covered by our own exact recomputation (`scripts/shuffle_smooth.py`, `scripts/shuffle_smooth_all.py`, logs in
`data/`) and by a rerun of the author's verifier (`data/author-verify.log`). No error found; no gap found.

| result | what we checked | verdict |
|---|---|---|
| Lemma 2.1 | Proof read. Interior runs of u are whole runs of w; a boundary run of u of length 2 is a whole run of w (runs <= 2), one of length 1 is deleted by D(u). If a whole run of w that is w's own boundary singleton is a boundary run of u, D(u) deletes it too, so the retained entries of D(u) are consecutive retained entries of D(w). | correct |
| Lemma 2.2 | Proof read (induction on derivative height; differentiability of u from runs <= 2). Smoothness implies all runs <= 2, since D only deletes boundary entries equal to 1. | correct |
| Lemma 2.3 | Proof read (concatenate supports). | correct |
| Lemma 2.4 | Proof read (U stream = D stream by FIFO matching). | correct |
| Lemma 3.1 | Proof read (cuts = returns of the prefix parity walk to 0, forced). | correct |
| Lemma 3.2 | Proof read in full: from parity (1,1) after 12, returns to (0,0) only at even positions, via a block 12 or 21, staying via 11 or 22; no 111/222 forces the first double block 11 and alternation, giving A_k, B_k; D(A_k) = 1 2^(2k+1) 1 and D(B_k) = 1 2^(2k+2) 1 checked by hand for k = 0, 1 and by our code for k = 0..6; k >= 1 not twice differentiable; the four k = 0 words and 11, 1212, 1221 are smooth (hand derivation); complements by D(complement) = D. | correct |
| Proposition 4.1 | Computational. Our own code generates all smooth words to length 40 (by extension, complete by Lemma 2.2) and decides shuffle-squareness of every smooth tangram EXACTLY (memoised FIFO search over (position, queue): sound and complete, since in any shuffle square the t-th position of the second copy matches the t-th of the first): Table 1 equal in all 20 rows, no non-shuffle tangram of length 18..40. Author's verifier: PASS (4,170 positive controls replayed). | correct |
| Theorem 1.1 | Proof read: strong induction; the first atom boundary c >= 18 has its predecessor <= 16 and the next atom <= 8 (Lemma 3.2), boundaries even, so 18 <= c <= 24; |v| >= 18; u, v smooth tangrams (factors, Lemma 2.2), shorter; Lemma 2.3. | correct |
| Corollary 1.2 | Theorem 1.1 plus Table 1: our code finds exactly 34 non-shuffle smooth tangrams, maximal length 16, equal word for word to the union of the ten Table 2 orbits (odd lengths are not tangrams). | correct |
| Lemma 6.1 | Proof read: an aligned pair toggles the parity of S(2m) iff mixed (11: +2, 22: +4, mixed: +3); the finitely-many-mixed case forces eventually all runs of length 2, so K eventually 2222..., contradicting runs <= 2. Our code: 1,676 mixed aligned pairs among the first 2,500, the last at pair 2,498. | correct |
| Theorem 1.3 | Proof read. The paper's one-line claim that every Kolakoski prefix is smooth is classical; we supplied the argument (a factor u of K has runs <= 2, D(u) is a factor of D(K) = K and shorter, induct on length) and confirmed it for every prefix up to 120 by computation. Tangram iff n and S(n) even (checked n <= 3000); tangram prefixes below 18 are exactly P4, P8, P16; P4, P8 not shuffle squares, P16 one (exact search). Extra cross-check: direct shuffle test of every prefix 1..60 agrees. | correct |
| Corollary 6.2 | Proof read: greedy blocks of 18..24 letters, each a smooth tangram hence a shuffle square; both colours in every block, so a monochromatic interval meets at most two blocks (<= 48). Our code on the first 4,990 letters: 247 blocks of lengths 18..24, all shuffle squares, U = D, longest monochromatic interval 7. | correct |

The concluding remarks are questions, not claims. The certificate (291,550 bytes, SHA-256 as printed) matches.
