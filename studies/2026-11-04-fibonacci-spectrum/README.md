# Spectrum of the Fibonacci stacking (#69), 4 Nov 2026 — DICTO: "can fibonacci be harmonized to any degree" / "run the fibonacci spectrum"
fib_spectrum.py, fib-spectrum.json (compute-host; word length F_28 = 317811).
(1) The c/h word (h density 1/φ²): pure point. Every peak sits at q/φ² (mod 1) and its amplitude is EXACTLY |sin(πq/φ²)|/(πq) —
    checked to 5 decimals on the 12 strongest (q = ±1, ±2, ±4, ±3, ±6, ±7). Brightest pair: the two golden frequencies 1/φ² and 1/φ.
    So the word is harmonized to every degree, each harmonic with a closed-form strength.
(2) The crystal it builds (layer positions A, B, C; rod with h − k ≠ 0 mod 3): strongest features at l = 1/2 and at l = (√5 − 1)/4 = cos 72°
    and 1 − cos 72° (golden), plus a dense cluster accumulating at l = 1/2. Scaling test (N = 46368, 121393, 317811): these amplitudes FALL
    as the crystal grows (l = 1/2: 0.147, 0.126, 0.094; l = cos 72°: 0.098, 0.084, 0.063) — not sharp Bragg peaks. The positions A/B/C
    (a 3-valued cocycle over the word) give a smeared, probably singular-continuous spectrum, like the Thue–Morse word.
CONTRAST: the word that decides straight or twisted is perfectly harmonic; the stacking it produces is not. A Fibonacci-stacked crystal would show
structured but non-sharp rods, peaking at l = 1/2 and at the golden positions cos 72°.
LEADS: confirm singular continuity (scaling exponent; literature on diffraction of aperiodic polytypes, Fibonacci stackings); compare with the
per-ball c/h fingerprint (#94 §4), which reads the word exactly.
