#!/usr/bin/env bash
set -euo pipefail

REPOS=(
  "repos/mattpocock https://github.com/mattpocock/skills.git main"
  "repos/pstack https://github.com/cursor/plugins.git main pstack"
  "repos/emil https://github.com/emilkowalski/skills.git main"
  "repos/effect https://github.com/Effect-TS/effect.git main"
)

if root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  :
else
  root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
cd "$root"
mkdir -p repos

for repo in "${REPOS[@]}"; do
  read -r path remote branch sparse_path <<< "$repo"

  if [[ ! -e "$path" ]]; then
    echo "clone: $path from $remote $branch"
    if [[ -n "$sparse_path" ]]; then
      git clone --filter=blob:none --sparse --branch "$branch" --single-branch "$remote" "$path"
      git -C "$path" sparse-checkout set "$sparse_path"
    else
      git clone --branch "$branch" --single-branch "$remote" "$path"
    fi
    if [[ "$path" == "repos/emil" ]]; then
      emil_commit="$(awk -F '|' '$2 ~ /^ Emil $/ {gsub(/[ `]/, "", $6); print $6}' UPSTREAM.md)"
      git -C "$path" checkout --detach "$emil_commit"
    fi
    continue
  fi

  if [[ ! -d "$path/.git" ]]; then
    echo "not a git clone: $path"
    exit 1
  fi

  echo "update: $path from $remote $branch"
  git -C "$path" remote set-url origin "$remote"
  if [[ -n "$sparse_path" ]]; then
    git -C "$path" sparse-checkout set --cone "$sparse_path"
  fi
  git -C "$path" fetch origin "$branch"
  if [[ "$path" == "repos/emil" ]]; then
    echo "Emil fetched; checkout preserved. Record origin/main in UPSTREAM.md and review before adopting."
    continue
  fi
  git -C "$path" checkout "$branch"
  git -C "$path" merge --ff-only "origin/$branch"
done
