#!/bin/bash
# read-only survey of top-level home entries
cd ~
for e in * .[!.]*; do
  [ -e "$e" ] || continue
  sz=$(du -xsk -- "$e" 2>/dev/null | cut -f1)
  mt=$(find "$e" -xdev -type f -printf '%TY-%Tm-%Td\n' 2>/dev/null | sort | tail -1)
  if [ -d "$e" ] && git -C "$e" rev-parse --show-toplevel >/dev/null 2>&1 && [ "$(git -C "$e" rev-parse --show-toplevel)" = "$HOME/$e" ]; then
    h=$(git -C "$e" rev-parse HEAD 2>/dev/null); b=$(git -C "$e" rev-parse --abbrev-ref HEAD 2>/dev/null)
    r=$(git -C "$e" remote get-url origin 2>/dev/null | sed 's#.*/##')
    dm=$(git -C "$e" status --porcelain -uno 2>/dev/null | wc -l)
    un=$(git -C "$e" status --porcelain 2>/dev/null | grep -c '^??')
    unk=$(git -C "$e" status --porcelain 2>/dev/null | awk '/^\?\?/{print $2}' | (cd "$e"; xargs -r du -sk 2>/dev/null) | awk '{s+=$1}END{print s+0}')
    ig=$(git -C "$e" status --porcelain --ignored 2>/dev/null | awk '/^!!/{print $2}' | (cd "$e"; xargs -r du -sk 2>/dev/null) | awk '{s+=$1}END{print s+0}')
    gt=$( [ -f "$e/.git" ] && echo wt || echo repo)
    printf '%s\tgit\t%s\t%s\t%s\t%s\t%s\tdirty=%s\tuntr=%s(%sK)\tign=%sK\t%s\n' "$e" "$sz" "$mt" "$gt" "$b" "$h" "$dm" "$un" "$unk" "$ig" "$r"
  else
    t=$( [ -d "$e" ] && echo dir || echo file)
    printf '%s\t%s\t%s\t%s\n' "$e" "$t" "$sz" "$mt"
  fi
done
