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

Install/update: reconcile sources to UPSTREAM.md's adopted pins, then link skills.
Check: verify sources, resources, and installed links without fetching or writing.
Uninstall: remove only this collection's links, preserving other entries.

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

is_our_link() {
  local entry="$1" expected destination
  [[ -L "$entry" ]] || return 1
  expected="$collection_root/skills/${entry##*/}"
  destination="$(readlink "$entry")"
  [[ "$destination" == "$expected" ]] && return 0
  if [[ -d "$entry" ]]; then
    [[ "$(cd -- "$entry" && pwd -P)" == "$expected" ]]
    return
  fi
  # A removed skill can leave a dangling link through a relative or aliased path.
  [[ "$destination" == /* ]] || destination="${entry%/*}/$destination"
  [[ "${destination##*/}" == "${entry##*/}" && -d "${destination%/*}" ]] || return 1
  [[ "$(cd -- "${destination%/*}" && pwd -P)" == "$collection_root/skills" ]]
}

if [[ "$action" == uninstall ]]; then
  removed=0
  for entry in "$target_dir"/*; do
    if is_our_link "$entry"; then
      rm -- "$entry"
      printf 'removed: %s\n' "$entry"
      removed=$((removed + 1))
    fi
  done
  printf 'Removed %s collection links. Other entries were preserved.\n' "$removed"
  exit 0
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

# Reject conflicts before cloning sources or changing installation links.
if [[ "$action" == install ]]; then
  conflicts=0
  for name in "${skill_names[@]}"; do
    entry="$target_dir/$name"
    if [[ -e "$entry" || -L "$entry" ]] && ! is_our_link "$entry"; then
      printf 'conflict: %s (left unchanged)\n' "$entry" >&2
      conflicts=$((conflicts + 1))
    fi
  done
  [[ "$conflicts" -eq 0 ]] || fail 'resolve or back up conflicting entries before installing'
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

for name in "${skill_names[@]}"; do
  skill_dir="$collection_root/skills/$name"
  [[ -f "$skill_dir/SKILL.md" ]] || fail "unavailable entry point: $name"
  for resource in "$skill_dir"/*; do
    if [[ -L "$resource" && ! -e "$resource" ]]; then
      fail "broken resource link: $resource"
    fi
  done
done

if [[ "$action" == install ]]; then
  mkdir -p -- "$target_dir"
  target_dir="$(cd -- "$target_dir" && pwd -P)"
fi

# Reconcile retired skills only after all sources and current skills pass preflight.
for entry in "$target_dir"/*; do
  if is_our_link "$entry" && [[ ! -f "$collection_root/skills/${entry##*/}/SKILL.md" ]]; then
    if [[ "$action" == check ]]; then
      fail "retired collection link: $entry; run setup to remove it"
    fi
    rm -- "$entry"
    printf 'removed retired link: %s\n' "$entry"
  fi
done

missing=0
for name in "${skill_names[@]}"; do
  entry="$target_dir/$name"
  if is_our_link "$entry"; then
    printf 'installed: %s\n' "$name"
  elif [[ "$action" == check ]]; then
    printf 'missing or conflicting link: %s\n' "$entry" >&2
    missing=$((missing + 1))
  else
    [[ ! -e "$entry" && ! -L "$entry" ]] || fail "destination changed during setup: $entry"
    ln -s -- "$collection_root/skills/$name" "$entry"
    printf 'linked: %s\n' "$name"
  fi
done
[[ "$missing" -eq 0 ]] || fail "$missing installation links need attention"
printf '%s skills ready in %s\n' "${#skill_names[@]}" "$target_dir"
