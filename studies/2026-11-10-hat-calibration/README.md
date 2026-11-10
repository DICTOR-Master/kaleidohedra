# Calibrating the wall method on the 2D hat family (10 Nov 2026; DICTO: "yes calibrate on the 2D hat family")
Tile(a, b) built from the hat's exact outline (Kaplan's hatviz points; a-edges at 60° multiples scaled by a, b-edges at odd 30° by b;
closes for all a, b). Known answer: periodic at t = 0, 1/2, 1 (t = b/(a+b)), aperiodic otherwise (Smith, Myers, Kaplan, Goodman-Strauss 2023).
Method tried (scripts/hatwalls.py, job hat-walls): count side-by-side contacts of two copies (12 orientations, corner on corner, shared
boundary > 1e-4, overlap area < 1e-7), walls = changes along t. RESULT: METHOD-FAILED - the count jumps at almost every grid step (about 50
"walls" in (0, 0.16) alone; counts every 0.05: 14, 17, 16, 19, 23, 15, 21, 24, 24, 24, 18, 28, 27, 28, 37, 25, 33, 28, 22): the float
touching/overlap thresholds flip near-contacts in the noise. Not a result about the hat. Data: data-hat-walls.log.
Lesson kept: geometric walls (local contact repertoire) and behaviour walls (periodic / aperiodic) differ; behaviour can change only at a
geometric wall. NEXT: the exact version (corners linear in t; contact conditions decided exactly in Q(√3)(t), as #61's walls).
