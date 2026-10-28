# CLI tools

Available: `rg` for text search; `fd` for finding files; `ast-grep` for structural code search/rewrites; `jq` for JSON; `yq` (Mike Farah) for YAML/config queries and edits; `hyperfine` for repeated command benchmarks (distinguish warm/cold caches); `gh` for GitHub; `uv` for Python environments/tools. Use `fzf --filter` for noninteractive filtering. Prefer project-owned commands for checks and review diffs after automated rewrites.

# Browser

Prefer T3 preview: `preview_status`, then `preview_open` if needed. If unavailable or the same step fails twice, switch to Chrome or Zen without asking. Honor the task’s browser preference; otherwise try Chrome first. Briefly report the error and fallback, continue at the same URL, and preserve user tabs and data. If neither browser is controllable, report the blocker and continue independent work.
