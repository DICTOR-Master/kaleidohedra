# Supplementary files for "The all-contact case of the 24-cell conjecture"

Tejasvi S. Tomar (ORCID 0000-0003-4668-3639)

These files prove the inequality behind the paper's main theorem (Theorem 1.1). Let C be a kissing configuration in S^3,
that is, unit vectors with pairwise inner products at most 1/2. If |C| <= 23, then

    T_3(C) >= 2 pi^2 - 1828197/156250 - 253 eps2 - 1771 eps3 = 8.0369770014675... > 8,

where eps2 = 2.8111e-12 and eps3 = 1e-6. The certificate value is 2 pi^2 - 1828197/156250 = 8.0387480021787...,
and 253 and 1771 are the numbers of pairs and triples of 23 points.

The files use their own names for the quantities of the paper: T3* is T_3, S0 is omega_1, S0r is omega_1^+, Pi0
is omega_2, Theta0 is omega_3, p2+ is p_2, p3+ is p_3, and KFIX is kappa.

## Folders

| folder | contents |
|---|---|
| `certificate/` | The exact rational level-2 certificate (`certificate.txt.gz`) and its checker. It proves Theorem 3.2 of the paper, F(C) >= 2 pi^2 - KFIX for every kissing configuration with at most 23 points. `CHECK_RESULT.txt` quotes the checker's verdict. |
| `one_sidedness/` | The interval-arithmetic proofs (`PROOF.md`) of Lemma 4.1 of the paper: that S0 <= S0r, that p2+ <= Pi0 + eps2 on [0, 1/2], and that p3+ >= Theta0 - eps3 on the triples with q >= 0, with the verifiers and their logs. |
| `verification/` | Further checks of the rows and of the zonal matrices. Each 3- and 4-point row identity holds exactly on a principal lattice, which is unisolvent for all polynomials of degree at most 16, so no symmetry is assumed (`detcheck_aggregate.log`). All 490 zonal matrix entries agree exactly with those computed by the package of de Laat, Leijenhorst and de Muinck Keizer (`zonal_compare.log`), and have the degrees the construction requires (`zonal_degree_check.log`). |
| `build/` | The scripts that build the programme. `BUILD.md` names the package version and describes the package folder that the Julia scripts need. |
| `polytope/` | The 24-facet polytope of Remark 6.2, on the packing constraint. It contains the unit ball, and its volume is 7.9655697... < 8, computed exactly by two independent methods. |

## Software

- Julia 1.10.12, with LasserreSphericalCodes 0.1.0 (not included; see `build/BUILD.md`). Its Manifest.toml
  pins ClusteredLowRankSolver 1.0.3, Nemo 0.43.1 and Arblib 0.8.1.
- Python 3.12 with python-flint 0.9.0 (`one_sidedness/`), numpy 2.5.4 and scipy 1.18.1 (`polytope/exact_cc.py`)
  and pycddlib 2.1.7 (`polytope/verify_polytope.py`). numba 0.68.0 is needed only for the self-test of
  `one_sidedness/theta0_rig.py`.

## Rerunning the checks

Each block of commands starts in this folder. `PKG` is the package folder described in `build/BUILD.md`, and
`EXACT`, `OUT` and `RUN` are new empty folders.

**Certificate.** The Julia scripts run from the package folder.

    SUPP=$PWD
    cd PKG
    for w in $(seq 1 40); do
      julia --project=. -t 1 $SUPP/certificate/scripts/gen_exact.jl 14 16 $SUPP/certificate/data/objS_deg16.txt EXACT $w 40 &
    done; wait
    (cd EXACT && sha256sum -c $SUPP/certificate/ex1416.sha256)
    julia --project=. -t 32 $SUPP/certificate/scripts/check_cert.jl 14 16 $SUPP/certificate/data/objS_deg16.txt EXACT $SUPP/certificate/certificate.txt.gz 10 3

The first step writes the 209 files of exact row data, and their sha256 must equal `certificate/ex1416.sha256`.
It takes about 8 minutes with 40 workers. The check takes about 22 minutes on 32 threads and 8 GB of memory, and
ends with `ALL CHECKS PASSED`. It regenerates 10 random chunks of rows and compares them with the stored ones,
and it tests every identity at 3 random points per piece. Its last lines subtract the one-sidedness budget with
eps2 = 2.81e-12. The proved eps2 is slightly larger, so the bound above uses eps2 = 2.8111e-12 (see
`certificate/CHECK_RESULT.txt`).

**One-sidedness.**

    python3 one_sidedness/verify_p2.py certificate/data/objS_deg16.txt certificate/data/objS_deg16.txt 18
    python3 one_sidedness/eps2_digits.py certificate/data/objS_deg16.txt 18
    python3 one_sidedness/verify_p3.py certificate/data/objS_deg16.txt OUT/p3run_eps1e-6 6 11 1e-6 40

These reproduce `verify_p2_level18.log` (S0r - S0 > 0 and eps2, in a few seconds), `verify_p2_eps2_digits.log`,
and the cover of the triple piece: `p3run_eps1e-6.log`, `p3run_eps1e-6_summary.json` and `p3run_eps1e-6_ok.txt`,
which is shipped gzipped (about 9 minutes with 40 processes). `python3 one_sidedness/theta0_rig.py` compares the
rigorous enclosures of Theta0 with the floating-point evaluator `t3exact.py`.

**Deterministic row check.** Replace `__WORKDIR__` (this folder), `__SCRATCH__` and `__ENVDIR__` in
`verification/det_run.sh` (the latter holds `julia-1.10.12/`, `depot/` and the package folder as `lsc/`), then
run `bash verification/det_run.sh NW` with NW workers. Each worker runs

    julia --project=. -t 1 $SUPP/verification/det_check.jl $SUPP/certificate/scripts $SUPP/certificate/data/objS_deg16.txt $SUPP/certificate/certificate.txt.gz OUT w NW

from the package folder, and `python3 verification/det_aggregate.py OUT` collects the results. The full check
evaluates 969 + 969 + 74613 lattice points, about 54 core-hours in total.

**Zonal entries.** `bash verification/zonal_run.sh TAG MAXPAR verification/sigs_all.txt`, with the same
placeholders, recomputes all 60 signatures in a clean copy of the package and compares them with the package
folder's cache using `cmp_zonal.py`. `python3 verification/zonal_degree_check.py PKG/cache/zonalstore/4` checks
the degrees.

**Polytope.**

    cp polytope/mincc_best7965.npy RUN/
    python3 polytope/exact_cc.py RUN/mincc_best7965.npy
    cmp RUN/mincc_best7965_exact.txt polytope/mincc_best7965_exact.txt
    python3 polytope/verify_polytope.py RUN/mincc_best7965_exact.txt

`exact_cc.py` rounds the facet normals in `mincc_best7965.npy` to rationals and computes the exact volume
(`exact_cc.log`). `verify_polytope.py` recomputes the vertices with cddlib in exact arithmetic and the volume by
a pulling triangulation and by Lawrence's formula (`verify_polytope.log`). It writes
`mincc_best7965_exact_indep_volume.txt` next to its input.

## What is assumed

- The kissing number of R^4 is 24 (Musin), and every kissing configuration of 24 points is a D4 root system
  (de Laat, Leijenhorst and de Muinck Keizer, arXiv:2404.18794).
- The positive semidefinite pairing of the level-2 kernels from the same paper: for every finite code, the
  kernel part summed over its subsets of at most 4 points is nonnegative.
- The package LasserreSphericalCodes computes the constraint matrices correctly as functions of the inner
  products. The checks above test its output at the sample points, on the principal lattices and at random
  points.
- The correctness of Julia, Nemo, FLINT, Arb, python-flint and, for `polytope/`, cddlib.

The reduction from the cell to T_3 (Corollary 2.2) and the value T_3(D4) = 8 (Lemma 2.5) are proved in the paper.

## License

The code (.jl, .py and .sh files) is under the MIT License and the text and data are under CC BY 4.0
(`LICENSE.md`). Six files adapt parts of MIT-licensed code from github.com/creelie/d4-voronoi-cells; each names
its source in its first line, next to a copy of that license (`LICENSE-MIT-upstream`). The package
LasserreSphericalCodes is not included; `build/BUILD.md` names its version and source.

`SHA256SUMS` lists every file; check it with `sha256sum -c SHA256SUMS`.
