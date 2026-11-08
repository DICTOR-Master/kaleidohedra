# Sequences against DICTO's work (2026-11-08)

DICTO asked whether famous OEIS sequences (Recamán A005132, Busy Beaver A060843, Catalan A000108, primes A000040, Mersenne
A000043/A000668, Fibonacci A000045) explain or fill gaps. DICTO: keep the useful ones, leave the purely beautiful or decorative
ones (Recamán, Mersenne: only 31 = 2^5 - 1 mixes of the five solids).

1. Fibonacci/Lucas (fib_lucas.py, data-fib-lucas.txt, run on dicto-big-brother over dataset v8): phi^n = (L_n + F_n sqrt5)/2.
   8 of the 78 volumes in Q or Q(sqrt5) are exactly a rational multiple of a power of phi: Dodeca-13 Wedge 1/20 phi^3,
   Metaxyhexecontahedron 20/81 phi^10 (L10 = 123, F10 = 55), Palintriacontahedron 100/9 phi^2, DICTO Jewel 3/2 phi^3,
   Unborn Axes 2/3 phi^2, Keyaxes phi^2, Lion 160/3 phi^3, DICTO skewed rhombic dodecahedron phi^2 (all exact, re-multiplied).
   No two solids of one paper have a volume ratio that is a power of phi. FINAL ok.
2. Primes / periods (polytypes.py 14, data-polytypes.txt): close-packed stackings of exact period n, up to shift and relabelling
   (0,1,1,1,1,2,3,6,10,18,31,59,105,198 = OEIS A011957, ZnS polytypes) and also up to reversal (= A011768, Barlow packings):
   both KNOWN, which checks the count. NEW (no OEIS hit, 8 Nov 2026, several offsets tried): the same counts split by the number
   of h layers (hexagonality), a triangle whose row sums are A011957 and A011768. Candidate OEIS entries (after A400949 is approved).
3. Busy Beaver: HexOct (book, Version 2, HexOct-K) already proves keyed tiles run Rule 110 (universal) and inherit Wang
   undecidability. Lead for the next HexOct version (destination: HexOct-K chapter): then the longest run of a finite HexOct-K
   stack that stops grows faster than any computable function (the Busy Beaver function, A060843). One sentence, no new claim.
4. Catalan: counts triangulations of polygons; a possible tool for counting Goldberg-style dissections; no current gap needs it.
