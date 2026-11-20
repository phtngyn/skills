#!/usr/bin/env bash
set -euo pipefail

collection_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
target_dir="$HOME/.agents/skills"
action="install"
action_selected=false
clone_temp=""

usage() {
  cat <<'EOF'
Usage: ./scripts/setup.sh [--check | --uninstall] [--target DIRECTORY]

Install/update: reconcile sources to UPSTREAM.md's adopted pins, then install skill copies.
Check: verify sources, resources, and installed copies without fetching or writing.
Uninstall: remove only this collection's copies and legacy links, preserving other entries.

The default target is ~/.agents/skills. Clean sources move to the adopted pins;
missing commits are fetched as needed. Local edits and branch pointers are preserved.
EOF
}

fail() { printf 'error: %s\n' "$*" >&2; exit 1; }
cleanup() { if [[ -n "$clone_temp" ]]; then rm -rf -- "$clone_temp"; fi; }
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check|--uninstall)
      [[ "$action_selected" == false ]] || fail 'choose only one action'
      action="${1#--}"
      action_selected=true
      shift
      ;;
    --target)
      [[ $# -ge 2 && -n "$2" ]] || fail '--target requires a directory'
      target_dir="$2"
      shift 2
      ;;
    --help|-h) usage; exit 0 ;;
    *) fail "unknown option: $1" ;;
  esac
done

[[ "$target_dir" == /* ]] || target_dir="$PWD/$target_dir"
if [[ -e "$target_dir" || -L "$target_dir" ]]; then
  [[ -d "$target_dir" ]] || fail "target is not a directory: $target_dir"
  target_dir="$(cd -- "$target_dir" && pwd -P)"
fi

command -v python3 >/dev/null 2>&1 || fail 'python3 is required'
installer="$collection_root/scripts/install_skills.py"
if [[ "$action" == uninstall ]]; then
  exec python3 "$installer" uninstall "$collection_root" "$target_dir"
fi

command -v git >/dev/null 2>&1 || fail 'git is required'
skill_names=()
for skill_dir in "$collection_root"/skills/*; do
  [[ -d "$skill_dir" ]] || continue
  name="${skill_dir##*/}"
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail "invalid skill directory: $name"
  [[ -f "$skill_dir/SKILL.md" || -L "$skill_dir/SKILL.md" ]] || fail "missing entry point: $name"
  skill_names+=("$name")
done
[[ ${#skill_names[@]} -gt 0 ]] || fail 'no skills found'

if [[ "$action" == install ]]; then
  python3 "$installer" preflight "$collection_root" "$target_dir" "${skill_names[@]}"
fi

# UPSTREAM.md is the single source of repository locations and adopted revisions.
source_rows="$(awk -F '|' '$4 ~ /`repos\// {
  for (i = 3; i <= 6; i++) gsub(/[ \t`]/, "", $i)
  printf "%s\t%s\t%s\n", $4, $3, $6
}' "$collection_root/UPSTREAM.md")"
[[ -n "$source_rows" ]] || fail 'no upstream sources found in UPSTREAM.md'

while IFS=$'\t' read -r repo remote commit; do
  [[ "$repo" =~ ^repos/[a-zA-Z0-9_-]+$ ]] || fail "invalid upstream path: $repo"
  [[ -n "$remote" && "$commit" =~ ^[0-9a-f]{40}$ ]] || fail "invalid source or adopted pin: $repo"
done <<< "$source_rows"

while IFS=$'\t' read -r repo remote commit; do
  checkout="$collection_root/$repo"
  if [[ ! -e "$checkout" && ! -L "$checkout" ]]; then
    [[ "$action" == install ]] || fail "missing source: $repo; run setup to clone it"
    mkdir -p -- "$collection_root/repos"
    clone_temp="$(mktemp -d "$collection_root/repos/.setup-${repo##*/}.XXXXXX")"
    printf 'clone: %s at adopted revision %s\n' "$repo" "$commit"
    git clone --filter=blob:none --no-checkout -- "$remote" "$clone_temp" || fail "clone failed: $repo"
    if [[ "$repo" == repos/pstack ]]; then
      git -C "$clone_temp" sparse-checkout set --cone pstack || fail 'Poteto sparse checkout failed'
    fi
    git -C "$clone_temp" checkout --detach "$commit" || fail "adopted revision unavailable: $repo"
    [[ ! -e "$checkout" && ! -L "$checkout" ]] || fail "source appeared during setup: $repo"
    mv -- "$clone_temp" "$checkout"
    clone_temp=""
  fi
  [[ -e "$checkout/.git" ]] || fail "not an upstream Git checkout: $repo"
  current="$(git -C "$checkout" rev-parse HEAD)" || fail "cannot read source revision: $repo"
  dirty="$(GIT_OPTIONAL_LOCKS=0 git -C "$checkout" status --porcelain)" || fail "cannot inspect source: $repo"
  [[ -z "$dirty" ]] || fail "source has local changes: $repo; commit, stash, or move them, then rerun setup; checkout preserved"
  if [[ "$current" != "$commit" ]]; then
    [[ "$action" == install ]] || fail "$repo is at $current, expected $commit; run ./scripts/setup.sh to update it"
    if ! GIT_NO_LAZY_FETCH=1 git -C "$checkout" cat-file -e "$commit^{commit}" 2>/dev/null; then
      printf 'fetch: %s adopted revision %s\n' "$repo" "$commit"
      git -C "$checkout" fetch --no-tags -- "$remote" "$commit" || fail "cannot fetch adopted revision for $repo; checkout preserved; check network access and rerun setup"
    fi
    printf 'update: %s from %s to %s\n' "$repo" "$current" "$commit"
    git -C "$checkout" checkout --detach "$commit" || fail "cannot adopt revision for $repo; no forced reset was attempted"
  fi
  printf 'source ready: %s @ %s\n' "$repo" "$commit"
done <<< "$source_rows"

# Keep the catalog entry in sync with the adopted Stageshow source.
stageshow_source="$collection_root/repos/benjitaylor/stageshow/SKILL.md"
stageshow_entry="$collection_root/skills/stageshow/SKILL.md"
if [[ -f "$stageshow_source" ]]; then
  if [[ "$action" == install ]]; then
    if [[ -L "$stageshow_entry" ]] || ! cmp -s "$stageshow_source" "$stageshow_entry"; then
      rm -f -- "$stageshow_entry"
      cp -- "$stageshow_source" "$stageshow_entry"
    fi
  else
    [[ ! -L "$stageshow_entry" ]] && cmp -s "$stageshow_source" "$stageshow_entry" || fail 'stageshow entry point needs syncing; run setup'
  fi
fi

exec python3 "$installer" "$action" "$collection_root" "$target_dir" "${skill_names[@]}"
