#!/bin/bash
# Palomar's comparator judge in separate steps, each fitting a 280 s foreground limit (generalised from the Grünbaum
# k = 10 entry, whose template run does not finish in one 280 s call). Same judge, same configuration. Run on the
# compute host, from anywhere: ENTRY (default: the current folder) is the assembled, built entry.
#
#   STEP=export        writes Challenge and Solution exports with the toolchain's leanexport, for the declaration list
#                      that `lake comparator` exports: Quot, Quot.mk, Quot.lift, Quot.ind, the comparator theorems and
#                      definitions (comparator.json order), the permitted axioms, then Lean's built-in Nat/String names.
#                      (Check once per toolchain against the "Exporting #[...]" line of a template run: STEP=decls
#                      prints the list.)
#   STEP=judge K=none  `lake comparator --challenge-from-export --solution-from-export` with the template's generated
#                      configuration and no external kernel: statement comparison, axiom check, Lean's kernel.
#                      (K=nanoda or K=con-ron adds that one kernel to the judge.)
#   STEP=kernel K=lean|nanoda|con-ron   one kernel directly on the solution export, with exactly the arguments
#                      `lake comparator` gives it (Lake/CLI/Check.lean): nanoda gets its config file (permitted axioms,
#                      4 threads, nat and string extensions); con-ron gets [--jobs=CJ] (Palomar: 2) and the export.
#                      Exit 0 = the kernel accepts. Only the bwrap sandbox is left out (the export is our own file).
#
# Every step: time limit TMO (default 280 s), memory cap MEM (default 14G) without swap, CPUs CPUS (e.g. 0-3; empty =
# all); CJ=default leaves con-ron at its own worker count with LEAN_NUM_THREADS = number of CPUs; /usr/bin/time gives wall time and the largest process, the cgroup's
# memory.peak the peak of the whole step; a sampler writes memory.current every 2 s to $LOG.mem. Exports go to
# EXPORTS (default $ENTRY/.lake/palomar-exports). Logs: $ENTRY/logs/comparator-split-*.log.
# Prints FINAL ok and exits 0 iff the step exits 0; otherwise prints FINAL FAIL and exits with the step's code (1 if
# that was 0). Wrappers must use the exit code.
STEP=${STEP:?STEP=decls|export|judge|kernel}; TMO=${TMO:-280}; MEM=${MEM:-14G}; CJ=${CJ:-2}; CPUS=${CPUS:-}
ENTRY=$(cd "${ENTRY:-.}" && pwd); cd "$ENTRY" || exit 1; mkdir -p logs
EXPORTS=${EXPORTS:-$ENTRY/.lake/palomar-exports}; mkdir -p "$EXPORTS"
export PATH=$HOME/.elan/bin:$PATH
PIN=""; if [ -n "$CPUS" ]; then PIN="taskset -c $CPUS"
  export LEAN_NUM_THREADS=$(python3 -c 'import sys; print(sum(int(r.split("-")[-1]) - int(r.split("-")[0]) + 1 for r in sys.argv[1].split(",")))' "$CPUS"); fi
DECLS=$(python3 - comparator.json <<'PY'
import json, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
base = "Quot Quot.mk Quot.lift Quot.ind".split()
tail = ("Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft "
        "Nat.shiftRight String.ofList Char.ofNat List eagerReduce Nat String String.mk Char optParam autoParam "
        "semiOutParam outParam").split()
print(" ".join(base + c["theorem_names"] + c.get("definition_names", []) + c["permitted_axioms"] + tail))
PY
)
# The judging binaries come from the entry's own toolchain (its lean-toolchain, read by elan from the entry folder),
# as in the template's verify-comparator.sh; stop at once if one is missing.
if [ "$STEP" != decls ]; then
  PFX=$(lean --print-prefix 2>/dev/null) || { echo "lean not found for the toolchain of $ENTRY"; echo "FINAL FAIL (no toolchain)"; exit 1; }
  for tool in lake leanexport leanchecker nanoda_bin con-ron; do
    [ -x "$PFX/bin/$tool" ] || { echo "the toolchain at $PFX has no $tool"; echo "FINAL FAIL (missing $tool)"; exit 1; }
  done
fi
case $STEP in
  decls) echo "$DECLS"; exit 0 ;;
  export) LOG=${LOG:-logs/comparator-split-export.log}
    CMD="for M in Challenge Solution; do lake env leanexport \$M -- $DECLS > $EXPORTS/\$M.ndjson || exit 1; done; sha256sum $EXPORTS/*.ndjson" ;;
  judge) K=${K:?K=none|nanoda|con-ron}; LOG=${LOG:-logs/comparator-split-judge-$K.log}; CFG=$EXPORTS/config-$K.json
    python3 - comparator.json "$CFG" "$PFX" "$K" "$CJ" <<'PY' || exit 1
import json, pathlib, sys
source, destination, prefix, k, cj = sys.argv[1:]
config = json.loads(pathlib.Path(source).read_text(encoding="utf-8"))
assert "external_kernels" not in config, "external_kernels is not a submitter field"
config.pop("enable_nanoda", None)
kernels = {"nanoda": [f"{prefix}/bin/nanoda_bin"], "con-ron": [f"{prefix}/bin/con-ron"] + ([] if cj == "default" else [f"--jobs={cj}"])}
config["external_kernels"] = {} if k == "none" else {k: kernels[k]}
pathlib.Path(destination).write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PY
    CMD="lake comparator --config $CFG --challenge-from-export $EXPORTS/Challenge.ndjson --solution-from-export $EXPORTS/Solution.ndjson" ;;
  kernel) K=${K:?K=lean|nanoda|con-ron}; LOG=${LOG:-logs/comparator-split-kernel-$K.log}
    case $K in
      nanoda) NCFG=$EXPORTS/nanoda-config.json
        python3 -c 'import json,sys; json.dump({"use_stdin": False, "export_file_path": sys.argv[1], "permitted_axioms": json.load(open(sys.argv[2]))["permitted_axioms"], "unpermitted_axiom_hard_error": False, "num_threads": 4, "nat_extension": True, "string_extension": True}, open(sys.argv[3], "w"))' \
          "$EXPORTS/Solution.ndjson" comparator.json "$NCFG" || exit 1
        CMD="LEAN_ABORT_ON_PANIC=1 $PFX/bin/nanoda_bin $NCFG && echo nanoda kernel accepts the solution" ;;
      lean) CMD="LEAN_ABORT_ON_PANIC=1 $PFX/bin/leanchecker --silent --from-export $EXPORTS/Solution.ndjson && echo Lean default kernel accepts the solution" ;;
      con-ron) CMD="LEAN_ABORT_ON_PANIC=1 $PFX/bin/con-ron $([ "$CJ" = default ] || echo "--jobs=$CJ") ${CRX:-} $EXPORTS/Solution.ndjson && echo con-ron kernel accepts the solution" ;;
      *) echo "K must be lean, nanoda or con-ron"; exit 1 ;;
    esac ;;
  *) echo "STEP must be decls, export, judge or kernel"; exit 1 ;;
esac
# the inner limit (TMO - 20 s, then SIGKILL after 5 s) lets the scope report memory.peak and wall time when cut off
timeout "$TMO" systemd-run --user --scope -q -p MemoryMax="$MEM" -p MemorySwapMax=0 $PIN bash -c \
  "cg=/sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup); ( while sleep 2; do echo \$(date +%s) \$(cat \$cg/memory.current); done ) > $LOG.mem & smp=\$!
   /usr/bin/time -v timeout -k 5 $((TMO - 20)) bash -c '$CMD'; s=\$?; kill \$smp; [ \$s -eq 124 ] && echo 'STEP CUT OFF at the time limit'
   echo \"cgroup memory.peak (bytes, whole step): \$(cat \$cg/memory.peak)\"
   exit \$s" > "$LOG" 2>&1; cs=$?
echo "step $STEP ${K:-}: exit $cs; CPUS=${CPUS:-all} MEM=$MEM CJ=$CJ; log $LOG"
grep -aE "Maximum resident|Elapsed \(wall|memory.peak" "$LOG"
grep -av "linter\|^warning\|^Note\|^$\|^Exporting" "$LOG" | grep -av "^	" | tail -6 | cut -c1-300
if [ $cs -eq 0 ]; then echo "FINAL ok"; exit 0; fi
echo "FINAL FAIL (exit $cs)"; exit $cs
