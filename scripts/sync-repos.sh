#!/usr/bin/env bash
set -euo pipefail

REPOS=(
  "Matt|repos/mattpocock|https://github.com/mattpocock/skills.git|pinned"
  "Poteto|repos/pstack|https://github.com/cursor/plugins.git|pinned|pstack"
  "Emil|repos/emil|https://github.com/emilkowalski/skills.git|pinned"
  "Good CSS|repos/good-css|https://github.com/vojtaholik/good-css.git|pinned"
  "Effect|repos/effect|https://github.com/Effect-TS/effect.git|tracking"
)

cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p repos

for repo in "${REPOS[@]}"; do
  IFS='|' read -r source_name path remote policy sparse_path <<< "$repo"

  if [[ "$policy" == "pinned" ]]; then
    source_commit="$(awk -F '|' -v source="$source_name" '$2 == " " source " " {gsub(/[ `]/, "", $6); print $6}' UPSTREAM.md)"
    [[ "$source_commit" =~ ^[0-9a-f]{40}$ ]] || { echo "missing based-on commit for $source_name" >&2; exit 1; }
  fi

  if [[ ! -e "$path" ]]; then
    echo "clone: $path from $remote main"
    if [[ -n "$sparse_path" ]]; then
      git clone --filter=blob:none --sparse --branch main --single-branch "$remote" "$path"
      git -C "$path" sparse-checkout set "$sparse_path"
    else
      git clone --branch main --single-branch "$remote" "$path"
    fi
    if [[ "$policy" == "pinned" ]]; then
      git -C "$path" checkout --detach "$source_commit"
    fi
    continue
  fi

  if [[ ! -d "$path/.git" ]]; then
    echo "not a git clone: $path"
    exit 1
  fi

  echo "fetch: $path from $remote main"
  git -C "$path" remote set-url origin "$remote"
  if [[ -n "$sparse_path" ]]; then
    git -C "$path" sparse-checkout set --cone "$sparse_path"
  fi
  git -C "$path" fetch origin main
  if [[ "$policy" == "pinned" ]]; then
    echo "$source_name fetched; checkout preserved. Record origin/main in UPSTREAM.md and review before adopting."
    continue
  fi
  git -C "$path" checkout main
  git -C "$path" merge --ff-only origin/main
done
