# Solid catalogue and search: stage 1 spec (fingerprints)

Status: draft, 2026-10-06. Public, open source, like the rest of this repo.

## Scope
All solids, not only space-fillers: Platonic, Archimedean, Catalan, Johnson, the space-filling cells in TARGETS.md, and user-submitted shapes. Each entry has a `type` field saying what it is.

## Record (one per solid)
- `id` (stable, never reused), `names` (any number of names, with language), `type`
- `generator`: how the geometry is produced (Wythoff group and node, zonotope vectors, explicit coordinates), with its version
- `geometry`: vertices, edges, faces at edge 1 (or stated scale)
- `fingerprint`: see below
- `sources`: each value with its source and page or DOI, so a misprint can be traced to every entry that copied it
- `status`: Generated, Candidate, Recognized, Verified, Curated, or Unresolved
- `verification`: the build check (passed or not, with date and version)
- `novelty`: Known / Candidate / Not found, with the search that supports it

## Fingerprint (stage 1)
Cheap, exact invariants. Two solids with different fingerprints are different. Matching uses the fingerprint first, then a full congruence check only for close matches.
- face counts by type (and by number of sides)
- vertex count, edge count, face count (Euler check)
- vertex figures (the faces around each vertex type, in order)
- dihedral angles (set of values with multiplicities)
- symmetry group order
- volume and surface area at edge 1, and their ratio
- edge-graph spectrum (eigenvalues of the adjacency matrix)

## Acceptance (user decision, 2026-10-06)
- Approved by the repo owner.
- One independent build from the recorded generator and data is required. How a build counts depends on the data supplied, case by case.
- Accepted does not mean novel. Novelty is recorded separately under `novelty`.

## Submission
A submitted shape is checked automatically: valid polyhedron, faces close, edges consistent, Euler check, and fingerprint computed. The result is a Candidate until the owner accepts it.

## Not in stage 1
Wythoff generation (stage 2), optical signatures (stage 3), packing (stage 4), crystal-structure links.
