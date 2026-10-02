#!/bin/sh
# Create a pinned fixture clone and venv (POSIX counterpart of the Phase 1a manual setup).
# Usage: fixtures/setup.sh <arrow|httpie|rich> [python]      (needs git, uv, python3.12)
# Clone: fixtures/<name> at the pinned commit; venv: fixtures/.venvs/<name>; deps: fixtures/requirements/<name>.txt
# rich's metadata is stale after a plain editable install of an old tag; we install -e . --no-deps last.
set -eu
name="${1:?usage: setup.sh <arrow|httpie|rich> [python]}"
py="${2:-python3.12}"
here="$(cd "$(dirname "$0")" && pwd)"
pins="$here/pins.json"
get() { "$py" -c "import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]][sys.argv[3]])" "$pins" "$name" "$1"; }
repo="$(get repo)"; commit="$(get commit)"
fx="$here/$name"; venv="$here/.venvs/$name"
if [ ! -d "$fx/.git" ]; then git clone --quiet "$repo" "$fx"; fi
git -C "$fx" checkout --quiet --detach "$commit"
[ "$(git -C "$fx" rev-parse HEAD)" = "$commit" ] || { echo "HEAD != pin" >&2; exit 4; }
uv venv --quiet --python "$py" "$venv"
uv pip install --quiet --python "$venv/bin/python" -r "$here/requirements/$name.txt"
uv pip install --quiet --python "$venv/bin/python" -e "$fx" --no-deps
echo "$name ready at $commit ($("$venv/bin/python" --version))"
