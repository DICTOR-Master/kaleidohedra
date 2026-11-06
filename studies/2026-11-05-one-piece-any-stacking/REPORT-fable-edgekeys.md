# Edge keys against the three relays of paper #97: 17 cannot become 14

Fable, 6 November 2026. Nothing in the study or the paper was edited; scratch scripts in `/tmp/edgekeys` (Pi and dicto-big-brother), logs there.

## Verdict

NO. The three relays cannot be replaced by edge keys, and the 17-piece set is the floor of the Kari architecture (14 tile pieces + 3 digit relays, proper motions only). The reason is not the shape of the keys but who fills the up sites: if the 14 tile pieces fill both sublattices of a slab, every slab holds two Kari rows, the up row multiplies against the down row, and the stacking multiplier per slab is q_down / q_up in {1, 3, 1/3}. With that multiplier set Kari's "no product equals 1" fails, and the periodic tilings it predicts exist on the real geometry: the 14 tile pieces alone tile periodically with a cell of two pieces (one down, one up, all joins turned). Edge keys cannot change this: they only add constraints, the up row stays a Kari row because the face keys are kept, and every key relation across a contact is symmetric under the flip of the slab (a proper motion), so a 14-tile set can never transmit "output above = input below" without also transmitting "input above = output below". Beyond 14, no merge of tile pieces is possible either (a piece in a row has a fixed rotation, so one piece is one Kari tile), and the relays need one piece per digit (the relay's rotation is fixed by its receiving quad; the digit cannot ride on the rotation). The 17 of paper #97 stand.

## Design tested

The replacement the task asked for, in two versions, on the real slab geometry (`n_slabs.build`, proper motions, actual face contacts, as in `keyed_n_sat.py`):

| Piece set | Hexagon | Quads | Triangles |
|---|---|---|---|
| k17 (paper #97, control) | tile: input digit n + 3 bumps (x2: corners not over mid corners; x2/3: over them); relay: digit d + 3 holes over its mid corners | tile: Q0 = output s, Q1, Q2 = "tile"; relay: one receives d, two "relay" | tile: carry out e / carry in w, tagged by q, four plain; relay: six plain |
| k14 | 14 tile pieces only, filling both sublattices. Hexagon mates hexagon: equal digit, bump patterns complementary (bumps on hollows; the only physical way two three-bump hexagons can meet) | Q0 mates Q0 with equal s; Q1, Q2 mate each other (plain) | as k17 |
| k14q | k14, plus a multiplier tag on Q0: bump for x2, hollow for x2/3, so Q0 mates Q0 only across different multipliers (forbids slabs whose two rows share q) | | |

In k14 the join type still reads the multipliers through the hexagon bumps, but now between two tiles: a straight join needs the two hexagons' bumps on different corner classes, so straight means q_down(k) differs from q_up(k+1), turned means they are equal. The arithmetic per slab: the down row gives mean(s_D) = q_D mean(n_D); the Q0 link gives mean(s_U) = mean(s_D); the up row (a Kari row read upward) gives mean(n_U) = mean(s_U)/q_U; the hexagon link to the slab below gives x_(k-1) = mean(n_U(k)). So x_(k-1) = (q_D/q_U) x_k with q_D/q_U in {1, 3, 1/3}.

Edge-key additions were designed and discarded on paper before any run (Obstructions B and C below); none can repair this arithmetic.

## Checks

Script `/tmp/edgekeys/tworow_sat.py MODEL patch|torus ...` (CaDiCaL through PySAT, dicto-big-brother, each run under 3 min except the last, heartbeat per case, FINAL line). Torus test: for every primitive periodic stacking word up to PMAX joins and its double, every in-plane sublattice of index <= IMAX in Hermite normal form and EVERY skew representative (the gap found in the spiral scan is closed here), sites are identified by the translation group and the SAT question is whether a keyed filling repeats. Rotated translates in one class are handled by naming placements by their rotation matrix.

| Run | Result |
|---|---|
| k17 patch, W=6, D=2, 3 joins (136-156 sites, ~510 contacts) | 7 of 8 words SAT, TTT UNSAT: reproduces #97 |
| k17 torus, PMAX=2, IMAX=2 (words SS, T, TT, STST; 7 tori each incl. skews) | all 28 UNSAT: no periodic keyed tiling, as Theorem 2 says |
| k17 torus, PMAX=3, IMAX=3 (19 tori per word, words up to 6 joins) | all 133 tori UNSAT (words SS, T, TT, SST, STST, SSTSST, STTSTT; 19 tori each, every skew), 722 s. The 17-piece set has no periodic keyed tiling with a vertical period up to 6 slabs and in-plane index up to 3, skews included |
| k14 patch, same block | 8 of 8 words SAT, including TTT: the range limit of Kari's digits no longer bites, since the up row undoes the down row |
| k14 torus, PMAX=2, IMAX=2 | PERIODIC, 14 tori. Word T (all joins turned), lattice (1,0,1), skew 0, 2 classes: one x2 tile piece as every down piece and one as every up piece, in-plane period 1, vertical period one slab. Also on every larger torus tested (an x2/3 version too); word TT likewise; SS and STST UNSAT |
| k14q patch | SSS, SST, TSS UNSAT (two slabs of multiplier 3 in a row already leave [1/2, 2]); the other 5 words SAT |
| k14q torus, PMAX=2, IMAX=2 | PERIODIC, 6 tori. Word TT, vertical period two slabs: slab types alternate (down x2, up x2/3) and (down x2/3, up x2), multipliers 3 and 1/3, every join turned, on all six tori of index 2; T, SS, STST UNSAT |

The k14 periodic tiling is the smallest possible: two keyed copies of Narcissus, the fcc stacking of Covenants.

## Why Kari's proof does not survive

Flip lemma. A rotation by 180 degrees about a horizontal axis is a proper motion that maps a Narcissus slab stacking onto a Narcissus slab stacking, exchanging down and up pieces and reversing the stacking word (checked on the slab: down X, up Y, mid corners over Z goes to a translate of itself). A keyed tiling stays a keyed tiling under any proper motion. So whatever relation the keys impose between the down piece and the up piece of a contact (face or edge line, with the neighbours on that line) holds with the roles exchanged. In a set where up sites are filled by tile pieces, a link that enforces n_down = s_up at every hexagon contact therefore also enforces s_down = n_up there.

Two-row theorem. Let both sublattices of every slab be filled by the 14 tile pieces, with the carry keys kept. Then each slab has two Kari rows, mean(s) = q mean(n) in both. The hexagon link and the Q0 link each transmit n to n, or s to s, or (by the lemma) both n to s and s to n. Case by case: like-to-like on both links gives x_(k-1) = (q_D/q_U)^(+-1) x_k (k14 realises it); like-to-like with the same digit on both links makes mean(n) constant down the stack (no arithmetic at all); both-ways on either link forces q_D q_U = 1, impossible for 2 and 2/3, so no tiling. In every surviving case the multiplier set is closed under inversion (the flip exchanges q_D and q_U) and contains 1 whenever the two rows may share q. Kari's step "a period P gives a product 2^a (2/3)^b, never 1" is false for {1, 3, 1/3}: the constant word (all slabs (2,2)) and the alternating word ((2, 2/3), (2/3, 2), ...) both give product 1, and the SAT tori above show that both are realised by genuine keyed tilings. Forbidding the shared-q slabs (k14q) leaves only the strict alternation, which is periodic. Nothing else can be forbidden without emptying the set: after a multiplier 3 the mean leaves [1/2, 2] unless 1/3 follows.

So the relays are not an accident of the 17 design: a piece that passes a digit unchanged, with no carries of its own, is what keeps the slab's arithmetic to one multiplication. Any piece with Kari carries divides as soon as it sits upside down.

## Obstructions found (counts and proofs)

A. Two rows (above): 14 tile pieces alone, with any extra keys (face or edge), either tile periodically or not at all.

B. Relays need one piece per digit, with proper motions. The relay's rotation is fixed: its receiving quad must face the tile's Q0, and from the two other tiles around that up site the up site lies at the Q1 and Q2 azimuths, so only one rotation serves. Putting the receiver on all three quads makes the three tiles around a relay share s (periodic rows). Hence the digit must be in the piece's identity: 3 relays. A mirror placement would add one state per relay, but a mirror-image keyed copy is a second physical object, so the count of objects does not fall.

C. Edge keys cannot carry the digit across the interface. The only edge lines shared by consecutive slabs are the six hexagon edges, each shared by the two hexagons below and the same two hexagons above (valence 4; the apex of the slab above only touches the plane at a point). A rod there must be notched by the neighbour in the same slab as well, so a digit pattern of rods on a hexagon's edges is read by its in-slab neighbours too; with the row direction below free, the readable patterns are the rotation-invariant ones (two values, not three), and the neighbour coupling forces equal digits along the honeycomb. "Accept either" (a notch takes anyone's rod) adds freedom about who owns the rod, never about which value a rigid piece shows. The face key on the whole hexagon, one-to-one and rotation-invariant for a three-fold digit mark, is the right tool, and it is what #97 uses.

D. Tile pieces cannot merge. In a slab all tile pieces share one rotation (the row direction), so a piece has exactly one state per slab and one piece is one Kari tile; two tiles that differ only in their carries need two pieces because the carry out is fixed by the piece. Kari's 14 are all used (every tile occurs for some slope), so 14 tile pieces is the floor. Together with B: 17.

What would change the count: counting a keyed piece and its mirror image as one (mirror placements), or leaving Kari's multiplication for a different aperiodic engine. Those are routes (a) and (b) already in the README, not edge keys.

## Scripts and logs

- `/tmp/edgekeys/tworow_sat.py` (Pi and dicto-big-brother): models k17, k14, k14q; `patch W D m` and `torus PMAX IMAX [MULT]`; uses `n_slabs.py` copied beside it.
- Logs on dicto-big-brother `/tmp/edgekeys/`: `k14-patch.log`, `k14q-patch.log`, `k17-torus-pilot.log`, `k14-torus.log`, `k14q-torus.log`, `k17-torus-3-3.log`. No job of mine is left running.
