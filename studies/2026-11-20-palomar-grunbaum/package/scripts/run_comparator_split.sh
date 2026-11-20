#!/bin/bash
# The template comparator run in parts, for a machine rule that limits every foreground command to 280 s (the template
# run of this entry takes longer than that in one piece). Same judge, same configuration, split two ways:
#   STEP=export      writes the challenge and solution exports with the toolchain's leanexport (lean4export), for the
#                    same declaration list that `lake comparator` exports (copied from its log line "Exporting #[...]");
#   STEP=judge K=..  runs `lake comparator --challenge-from-export --solution-from-export` with the template's generated
#                    configuration (comparator.json; enable_nanoda dropped; external_kernels set from the toolchain), but
#                    keeping only the external kernels named in K: K=none (Lean's kernel only), K=nanoda, K=con-ron.
#                    Lean's own kernel, the statement comparison and the axiom check run in every judge step;
#   STEP=kernel K=.. runs one kernel directly (K=lean: Lean's own, as `leanchecker --silent --from-export`) on the solution export, with exactly the arguments `lake
#                    comparator` gives it (Lake/CLI/Check.lean of the toolchain, runExternalKernel): K=nanoda gets the
#                    same nanoda-style config file (use_stdin false, the export path, the permitted axioms,
#                    unpermitted_axiom_hard_error false, num_threads 4, nat and string extensions); K=con-ron gets
#                    [--jobs=CJ] and the export path (CRX: extra con-ron options, e.g. --progress=1000, for a heartbeat
#                    on stderr only). As in the comparator, exit code 0 means the kernel accepts.
#                    (Only the bwrap sandbox around the kernel is left out: the export is our own file.)
# CJ sets con-ron's worker count (default: con-ron's own). Each step: limit TMO (default 280 s), memory cap MEM (default
# 14G), no swap; with FIT=1 also on CPUs 0-3 with LEAN_NUM_THREADS=4 (the fit check). Exports go to $EXPORTS.
# Usage (from the entry root): EXPORTS=<dir> STEP=export bash scripts/run_comparator_split.sh
#                              EXPORTS=<dir> STEP=judge K=none [FIT=1] [LOG=...] bash scripts/run_comparator_split.sh
#                              EXPORTS=<dir> STEP=kernel K=con-ron [CJ=2] [FIT=1] [MEM=..] bash scripts/run_comparator_split.sh
# FINAL ok iff the step exits 0.
STEP=${STEP:?}; EXPORTS=${EXPORTS:?}; TMO=${TMO:-280}; MEM=${MEM:-14G}; CJ=${CJ:-default}
ENTRY=$(cd "$(dirname "$0")/.." && pwd); cd "$ENTRY" || exit 1; mkdir -p logs "$EXPORTS"
export PATH=$HOME/.elan/bin:$PATH
PIN=""; [ "${FIT:-0}" = 1 ] && { PIN="taskset -c 0-3"; export LEAN_NUM_THREADS=4; }
DECLS="Quot Quot.mk Quot.lift Quot.ind GrunbaumK10.cube_everyZoneHas GrunbaumK10.rhombicDodecahedron_everyZoneHas
GrunbaumK10.grunbaum_k10 GrunbaumK10.grunbaum_k10_parallelohedron propext Quot.sound Classical.choice Nat.add Nat.sub
Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight
String.ofList Char.ofNat List eagerReduce Nat String String.mk Char optParam autoParam semiOutParam outParam"
case $STEP in
  export) LOG=${LOG:-logs/comparator-split-export.log}
    CMD="for M in Challenge Solution; do lake env leanexport \$M -- $(echo $DECLS) > $EXPORTS/\$M.ndjson || exit 1; done" ;;
  judge) K=${K:?}; LOG=${LOG:-logs/comparator-split-$K.log}
    CFG=$EXPORTS/config-$K.json
    python3 - comparator.json "$CFG" "$(lean --print-prefix)" "$K" "$CJ" <<'PY' || exit 1
import json, pathlib, sys
source, destination, prefix, k, cj = sys.argv[1:]
config = json.loads(pathlib.Path(source).read_text(encoding="utf-8"))
assert "external_kernels" not in config
config.pop("enable_nanoda", None)
conron = [f"{prefix}/bin/con-ron"] + ([] if cj == "default" else [f"--jobs={cj}"])
kernels = {"nanoda": [f"{prefix}/bin/nanoda_bin"], "con-ron": conron}
config["external_kernels"] = {} if k == "none" else {k: kernels[k]}
pathlib.Path(destination).write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PY
    cat "$CFG"
    CMD="lake comparator --config $CFG --challenge-from-export $EXPORTS/Challenge.ndjson --solution-from-export $EXPORTS/Solution.ndjson" ;;
  kernel) K=${K:?}; LOG=${LOG:-logs/comparator-split-kernel-$K.log}; PFX=$(lean --print-prefix)
    case $K in
      nanoda) NCFG=$EXPORTS/nanoda-config.json
        python3 -c 'import json,sys; json.dump({"use_stdin": False, "export_file_path": sys.argv[1], "permitted_axioms": json.load(open(sys.argv[2]))["permitted_axioms"], "unpermitted_axiom_hard_error": False, "num_threads": 4, "nat_extension": True, "string_extension": True}, open(sys.argv[3], "w"))' \
          $EXPORTS/Solution.ndjson comparator.json $NCFG || exit 1
        cat $NCFG; echo
        CMD="LEAN_ABORT_ON_PANIC=1 $PFX/bin/nanoda_bin $NCFG && echo nanoda kernel accepts the solution" ;;
      lean) CMD="LEAN_ABORT_ON_PANIC=1 $PFX/bin/leanchecker --silent --from-export $EXPORTS/Solution.ndjson && echo Lean default kernel accepts the solution" ;;
      con-ron) J=""; [ "$CJ" = default ] || J="--jobs=$CJ"
        CMD="LEAN_ABORT_ON_PANIC=1 $PFX/bin/con-ron $J ${CRX:-} $EXPORTS/Solution.ndjson && echo con-ron kernel accepts the solution" ;;
    esac ;;
esac
# a sampler writes the step's memory.current and memory pressure every 2 s to $LOG.mem; the inner time limit
# (TMO - 20 s, then SIGKILL after 5 s) lets the scope report memory.peak and the wall time even when a step is cut off
timeout $TMO systemd-run --user --scope -q -p MemoryMax=$MEM -p MemorySwapMax=0 $PIN bash -c \
  "cg=/sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup); ( while sleep 2; do echo \$(date +%s) \$(cat \$cg/memory.current) \$(grep -E '^(full|some)' \$cg/memory.pressure | tr '\n' ' '); done ) > $LOG.mem & smp=\$!
   /usr/bin/time -v timeout -k 5 $((TMO - 20)) bash -c '$CMD'; s=\$?; kill \$smp; [ \$s -eq 124 ] && echo 'STEP CUT OFF at the time limit'
   echo \"cgroup memory.peak (bytes, whole step): \$(cat /sys/fs/cgroup\$(cut -d: -f3 /proc/self/cgroup)/memory.peak)\"
   exit \$s" > $LOG 2>&1; cs=$?
grep -aE "Maximum resident|Elapsed \(wall|memory.peak" $LOG
grep -av "linter\|^warning\|^Note\|^$\|^Exporting" $LOG | grep -av "^	" | tail -8 | cut -c1-300
[ $cs -eq 0 ] && echo "FINAL ok" || echo "FINAL FAIL (exit $cs)"
