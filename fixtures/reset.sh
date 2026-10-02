#!/bin/sh
# Reset a pinned fixture to its commit and remove everything else. Usage: reset.sh <arrow|httpie|rich>
# POSIX counterpart of reset.ps1 (same exit codes: 2 no pin, 3 reset failed, 4 HEAD != pin).
set -u
name="${1:?usage: reset.sh <arrow|httpie|rich>}"
here="$(cd "$(dirname "$0")" && pwd)"
commit="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2],{}).get('commit',''))" "$here/pins.json" "$name" 2>/dev/null \
  || python3.12 -c "import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2],{}).get('commit',''))" "$here/pins.json" "$name")"
[ -n "$commit" ] || { echo "no pin for $name" >&2; exit 2; }
fx="$here/$name"
git -C "$fx" worktree prune >/dev/null
git -C "$fx" reset --hard --quiet "$commit" || exit 3
git -C "$fx" clean -fdxq
git -C "$fx" checkout --detach --quiet "$commit"
head="$(git -C "$fx" rev-parse HEAD)"
[ "$head" = "$commit" ] || { echo "HEAD $head != pin" >&2; exit 4; }
echo "$name reset to $head"
