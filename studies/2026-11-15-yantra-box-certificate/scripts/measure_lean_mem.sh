#!/bin/bash
# Peak memory of every module of a BUILT entry: each module is recompiled alone (`lake env lean -o <scratch>`), exactly as
# lake compiles it, inside its own systemd unit, which reports the cgroup "Memory peak" (anonymous memory plus newly charged
# page cache; the imported .olean files are already cached). /usr/bin/time adds wall seconds and max RSS (RSS counts the
# mmapped imports too). P modules run at a time (independent: each only reads the built imports).
# Usage: ENTRY=<built entry> OUT=<tsv> [P=6] [LIST=<file of module names>] measure_lean_mem.sh
# Output: module <tab> seconds <tab> max_rss_kb <tab> cgroup_peak_bytes <tab> exit. FINAL ok iff every module compiled.
ENTRY=${ENTRY:?}; OUT=${OUT:?}; P=${P:-6}
export PATH=$HOME/.elan/bin:$PATH
cd "$ENTRY" || exit 1
TMPD=$(mktemp -d); export TMPD ENTRY
if [ -n "$LIST" ]; then cp "$LIST" $TMPD/mods.txt
else find YantraCert -name '*.lean' | sed 's#\.lean$##; s#/#.#g' | sort > $TMPD/mods.txt; printf 'Challenge\nSolution\n' >> $TMPD/mods.txt; fi
N=$(wc -l < $TMPD/mods.txt); export N OUT; : > $OUT
one() {
  m=$1; f=$(echo $m | sed 's#\.#/#g').lean; o=$TMPD/$(echo $m | tr . _)
  systemd-run --user --wait -p MemorySwapMax=0 -E PATH=$PATH --working-directory=$ENTRY \
    /usr/bin/time -f "%e %M" -o $o.time lake env lean -o $o.olean $f > $o.unit 2>&1; ec=$?
  pk=$(grep -o 'Memory peak: [0-9.]*[KMGT]' $o.unit | awk '{v=$3; u=substr(v,length(v)); n=substr(v,1,length(v)-1); m=(u=="K")?1024:(u=="M")?1048576:(u=="G")?1073741824:1099511627776; printf "%d", n*m}')
  read t r < $o.time 2>/dev/null
  printf '%s\t%s\t%s\t%s\t%s\n' "$m" "${t:-NA}" "${r:-NA}" "${pk:-NA}" "$ec" >> $OUT
  rm -f $o.olean $o.ilean $o.c $o.time
  n=$(wc -l < $OUT); [ $((n % 50)) -eq 0 ] && echo "PROGRESS $(python3 -c "print(round($n / $N, 3))") $n/$N"
}
export -f one
xargs -P $P -I{} bash -c 'one {}' < $TMPD/mods.txt
bad=$(awk -F'\t' '$5 != 0' $OUT | wc -l)
echo "modules $(wc -l < $OUT), failed $bad"
sort -t$'\t' -k4 -n -r $OUT | head -25 | awk -F'\t' '{printf "  %-45s %7.1f s  rss %5.2f GB  peak %5.2f GB\n", $1, $2, $3/1048576, $4/1073741824}'
rm -rf $TMPD
[ "$bad" = 0 ] && [ "$(wc -l < $OUT)" = "$N" ] && echo "FINAL ok" || echo "FINAL FAIL"
