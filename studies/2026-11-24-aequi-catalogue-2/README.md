# Aequi catalogue, second batch: Nos. 1233–10725 (24 November 2026)

DICTO · dictospheres.com · study 2026-11-24-aequi-catalogue-2 · with Claude (Anthropic).

DATA ONLY (no app change, no deploy). **checks.py: FINAL ok** (checks.out).

## Result

- **Nos. 1233–1235 are reserved** for the three face-transitive permutahedron duals, as decided: 1233 Inimisa (TO-24, Oh, N = 24),
  1234 Inimiyo (TCO-48, Oh, N = 48), 1235 Inimigo (TID-120, Ih, N = 120). They are fair by symmetry; being face-transitive,
  they are **not among the certified batches** (the extension study sets face-transitive solids aside), so their rows carry
  no source id.
- **Nos. 1236–10725: 9 490 new certified Aequi**, from the 9 556 of study 2026-11-24-aequi-certify-extend (Part 2(a) 5 935;
  caps batches 336 + 1 375 + 1 910). **66 of the 9 556 are repeats** and are left out (duplicates.csv): the 21 D3d dice of caps
  batch 2 and the 45 D3d dice of caps batch 3 are each congruent to one D3d die of caps batch 1 (met again under the subgroups S6
  and D3; depths agree to 3.6e-13). So the extension's count of new Aequi is 9 490, not 9 556; the earlier batch keeps the die
  (first name wins).
- Each name is the catalogue number read by the approved rule of study 2026-11-24-aequi-numberings (first goroawase reading of each
  digit; the second only to avoid repeating the syllable just before), shown as "Name (No.N)". All 10 725 names (with the 1232)
  are distinct, and each decodes to exactly its own number.
- **Row 95** of study 2026-11-20-aequi-two-placements (Td: D12+D12′/24 + RT24+RT24′/24, N = 48) is **not new**: it is in the
  catalogued 1232 as **Niyoo (No.240)**. Decision 2 of the extension study ("named in the next numbering batch") is thereby met
  already.
- Off-axis families are not in these batches (decided: one name per family, later).

| group (order) | dice | Nos. from–to |
|---|---|---|
| D6h (24) | 2 | 1236–1237 |
| D4h (16) | 441 | 1238–1678 |
| D3h, D3d (12) | 3 + 1 293 | 1679–2974 |
| D2d, D2h, D4, C4h (8) | 1 207 + 2 311 + 279 + 451 | 2975–7222 |
| D3, S6 (6) | 1 611 + 1 392 | 7223–10225 |
| C2h, D2, S4 (4) | 327 + 96 + 77 | 10226–10725 |

## Order

As decided: group order descending, then m (face orbits) ascending, then N ascending. Stable tie-break: Schoenflies group name
(alphabetical), then corner count, then batch (2a, 2caps, 2caps2, 2caps3), then the die's index in its batch. Because m comes before
the group name, groups of equal order interleave (for example D2d and D2h, both of order 8). Keeping each group in one block
instead is a one-key change in common.py (sort_key), if wanted.

## Files

- catalogue.csv: No, name, name_shown, group, m, N, source batch, source id. Source batch b and id i = entry i of the `new` list of
  data/aequi&lt;b&gt;.json.gz of study 2026-11-24-aequi-certify-extend (the same index is `sid` in its certify&lt;b&gt;.jsonl.gz and
  dice&lt;b&gt;-new.json).
- duplicates.csv: the 66 left out, each with the batch die kept and its No.
- common.py (loaders, name rule, order key, congruence signature), build.py (writes the two CSVs), checks.py → checks.out.

## Checks (checks.py, FINAL ok)

1. Counts: Nos. consecutive from 1233; 3 + 9 490 rows; every die of every batch catalogued once or left out as a repeat.
2. Names: the rule reproduces all 1232 names of names.csv; every new name follows it; name_shown matches `^Name \(No\.N\)$`;
   all 10 725 distinct; every name parses in exactly one way, to its own number.
3. Order: the sort key is strictly increasing; group, m, N agree with the source data; no new die has a full group containing T.
4. Certification: every source die has its certify record (same label and N), status certified, or (11 dice of 2a) split box with
   split Krawczyk ok.
5. Congruence (both icosahedron placements and mirror images included): signature = depths scaled by the smallest, grouped into
   levels, with the Gram matrix of the unit face normals (per face: its level and the sorted multiset of (dot, level) over all faces),
   plus sorted depth vectors agreeing to 1e-6. Stability is checked: dots lie ≥ 2.7e-7 from a rounding boundary, depth levels are
   ≥ 1.6e-6 apart and ≤ 9.1e-12 wide. Results: the 9 490 are mutually non-congruent; each of the 66 left out matches exactly one
   catalogued die of an earlier batch; none of the 9 490 matches any of the 4 553 dice of study 2026-11-19-aequi-complete or any of
   the catalogued 1232. Positive control: the 52 + 108 + 50 dice that the extension study set aside as congruent to 2026-11-19 dice
   are all found again.
6. Row 95 is picker no. 240 (classification CSV of study 2026-11-24-aequi-vacuus-scutoids), Niyoo (No.240).

Method credit: the congruence test follows the idea of the extension study's post2a.py (scale-free plane distances, mirror images
included); the name rule and parser are copied from study 2026-11-24-aequi-numberings.

## Notes for DICTO

- The 4 404 dice of study 2026-11-19-aequi-complete whose groups do not contain T are not in the catalogue (the 1232 hold only its
  149 frame-group dice) and not certified; the new batches exclude dice congruent to them. Numbering them is a separate decision.
- The per-die files data/dice/NNNN.json of study 2026-11-24-aequi-numberings show "(no. 240)" (lower case, with a space); names.csv
  there and this catalogue use the decided "(No.240)". Not changed here.

## LEADS

1. Correct the count "9 556 new" to 9 490 in the extension study's README at its next edit.
2. When the off-axis families are named, number them after No. 10725.
