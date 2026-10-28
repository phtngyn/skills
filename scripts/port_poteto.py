#!/usr/bin/env python3
"""Rebuild the retained Poteto skills from the pinned source with native substitutions."""
from pathlib import Path
import argparse
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'make-bot-ui', 'typescript-best-practices', 'create-formal-verification-skill', 'maintain-formal-verification-skill'}
REMOVED = ('poteto-mode/references/codex.md', 'no-comments/references/comment-reviewer.md')


def section(text, heading, replacement):
    pattern = re.escape(heading) + r'\n.*?(?=\n## |\Z)'
    result, count = re.subn(pattern, lambda _: replacement.rstrip() + '\n', text, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one section: {heading}')
    return result


def line(text, prefix, replacement):
    rows = text.splitlines(keepends=True)
    matches = [i for i, row in enumerate(rows) if row.startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(f'Expected one line: {prefix}')
    rows[matches[0]] = replacement.rstrip() + '\n'
    return ''.join(rows)


def render(text, relative):
    """Preserve upstream prose; change only unavailable metadata, tools, paths and roles."""
    if relative.endswith('SKILL.md') and text.startswith('---\n'):
        front, body = text[4:].split('\n---\n', 1)
        front = re.sub(r'^(?:disable-model-invocation|icon|color|paths):[^\n]*\n?', '', front, flags=re.M)
        text = '---\n' + front.rstrip() + '\n---\n' + body

    if relative == 'poteto-mode/SKILL.md':
        text = line(text, 'Bundled skills live', "Bundled skills live at `../<name>/SKILL.md` from this file, so put this file's absolute path in every implementation delegate's prompt. Set `PSTACK_SKILLS_ROOT` to that installed skills directory, resolving symlinks; script paths below use it.")
        start = text.index('## Subagents\n')
        stop = text.index('**Fresh subagents by default.**', start)
        text = text[:start] + '''## Subagents

For a playbook-step delegate, include this skill's absolute path and require it to read the skill in full before its assigned unit. The parent runs the playbook. Routed workflow skills (`how`, `why`, `interrogate`, `reflect`, `swarm`) own their specialist roles.

Role choices are `roles` in `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json`. `$setup-pstack` configures them. Missing roles inherit the parent model; panels default to two inherited entries. Use configured models and reasoning efforts only when supported. Do not manufacture model slugs. Report unavailable diversity.

Code playbooks use their `feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb` role. The hardest cross-cutting designs, concurrency problems, and algorithms use `hardest tasks`; prose and judgment use `judgment and prose`. Trivial mechanical edits use the configured code model at lower effort.

Start with the role's configured reasoning budget. Raise it one supported level for the hardest work, lower it one for judgment and two or more for routine work. Use fast mode only for urgency, such as red CI or a blocked person; otherwise use standard speed. Verification keeps the `swarm workers` model and speed. Keep the configured model family; inheritance stays on the parent. If an adjustment is unavailable, use the configured choice and report it.

You own every subagent's work. Review the diff and write your own summary, don't pass through what it said. A second opinion is the same prompt against a different model. Agreement is high-signal.

''' + text[stop:]
        text = text.replace('- Before commit → the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`).', '- Before commit → review the diff for slop and remove it.')
        text = line(text, '- Shipping UI / IDE / CLI', '- Shipping UI / IDE / CLI → the matching project verification skill or available app-control tools. For bug fixes, reproduce first on the same surface yourself. Hand to the user only under the narrow Bug fix step 1 exception.')
    elif relative == 'how/SKILL.md':
        text = line(text, 'Every spawn is a Task subagent', 'Use read-only agents. Explorers use the `how explorer` role and explainers use `how explainer`, configured by `$setup-pstack`; otherwise inherit the parent model.')
    elif relative == 'why/SKILL.md':
        text = line(text, 'Each spawn below names a role line', 'Use the `why investigators` and `why synthesizer` roles configured by `$setup-pstack`; otherwise inherit the parent model.')
        text = line(text, 'Every spawn is `generalPurpose`', 'Investigators and the synthesizer need the relevant read tools and connectors. They do not edit files or external systems.')
        text = line(text, 'Before spawning investigators, list the available MCPs', 'Before spawning investigators, list the available connectors and their tools from the active tool catalog.')
    elif relative == 'architect/SKILL.md':
        text = line(text, 'Take the runners from', 'Take the runners from the `architect runners` role configured by `$setup-pstack`, in place of `arena runners`. Default to two inherited candidates.')
    elif relative == 'arena/SKILL.md':
        text = line(text, '3. Pick the runners.', '3. Pick the runners from `arena runners`, configured by `$setup-pstack`. Default to two inherited candidates. Spawn more runners when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive.')
        text = line(text, 'After all Phase B candidates complete, choose one model', "After all Phase B candidates complete, choose one model from `arena cross-judge pool`, configured by `$setup-pstack`, or inherit the parent model. Prefer a different model family when available. Spawn one read-only judge. It sees the rubric and candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't spawn it while candidates are still writing.")
    elif relative == 'interrogate/SKILL.md':
        start = text.index('Launch all reviewers in a single message')
        stop = text.index('Read `references/reviewer-prompt.md`', start)
        text = text[:start] + '''Launch all reviewers together, one per configured `interrogate reviewers` entry from `$setup-pstack`, labeled Reviewer A, B, and so on. Default to two fresh read-only reviewers inheriting the parent model. Report unavailable model diversity.

''' + text[stop:]
    elif relative == 'swarm/SKILL.md':
        text = line(text, '3. Pick the worker model', '3. Pick the worker model from the `swarm workers` role configured by `$setup-pstack`, or inherit the parent model. For a model race, name each available arm up front.')
        text = line(text, 'Spawn all N workers in one message', "Spawn all N workers with isolated writable workspaces. Use the current machine only when a worker needs access to local resources.")
    elif relative == 'reflect/SKILL.md':
        text = section(text, '## 1. Locate the active transcript', '''## 1. Locate the active transcript

Use the current conversation, supported host history, or an explicitly identified transcript for this workspace. If complete tool traces are unavailable, pass a tight session digest and mark missing evidence.
''')
        text = line(text, 'One message, three `Task` calls', 'Spawn three reviewers together, with access to relevant read tools and connectors. They return findings without edits.')
        text = line(text, 'Each reviewer and the synthesizer name a role line', 'Use each role configured by `$setup-pstack`, or inherit the parent model.')
        text = line(text, 'One `Task` call, `subagent_type:', 'Spawn one synthesizer using `reflect judgment, divergent, synthesizer`, or inherit the parent model. It spot-verifies citations through the available connectors. Pass `references/synthesizer.md` verbatim, with every reviewer\'s full output inlined where marked. It returns an Accepted / Rejected / Backlog list.')
    elif relative == 'recall/SKILL.md':
        text = line(text, 'Transcripts live at', 'Use supported host history or explicitly identified transcripts for this workspace. If prior chats are unavailable, mark the brief partial and use the visible conversation and shared record.')
    elif relative == 'automate-me/SKILL.md':
        text = line(text, 'Locate the active workspace\'s transcripts', 'Locate the requested workspace\'s history through supported host tools or explicitly identified transcripts before fanning out. Do not search unrelated session stores.')
    elif relative == 'no-comments/SKILL.md':
        text = line(text, '1. Spawn `Task` with', '1. Spawn a fresh comment reviewer with the scoped files or diff and the path to `references/comment-sicko.md`. It reads that persona in full. Do not restate its rules.')
    elif relative == 'poteto-help/SKILL.md':
        text = line(text, 'pstack is built for Cursor', 'This collection installs with its [setup script](../../README.md#install). Invoke a skill with `$skill-name`.')
        text = line(text, 'Other tools can read the skills', 'Per-role model choices are optional and configured by `$setup-pstack`.')
        text = line(text, 'Link [Cursor\'s skills docs]', 'Mid-chat, "new task" makes the mode match a fresh playbook. Playbook-step delegates read `poteto-mode` in full before their assigned unit.')
        text = '\n'.join(row for row in text.split('\n') if not row.startswith(('- Option+Enter', '- Cursor\'s docs list', '- `/deslop`,', '- `/loop` and')))
        text = text.replace('It was started with Enter. Start it as a Custom Mode, or start each task with `/poteto-mode`.', 'Start each new task with `$poteto-mode`.')
        text = text.replace('1. Install with `/add-plugin pstack` in chat, or from Customize in the sidebar.', '1. Install using the [collection setup](../../README.md#install).')
        text = text.replace(' and mention once that a Custom Mode keeps it on.', '.')
        text = text.replace('Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.', 'Then it offers to generate a verification skill unless the project already has one.')
    elif relative == 'setup-pstack/SKILL.md':
        text = '''---
name: setup-pstack
description: Configure pstack models per role and reasoning budget. Use for $setup-pstack or changing pstack's model choices.
---

# Setup pstack

Write `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json` with optional model choices per role. Unconfigured roles inherit the parent model. This file is read by the skills, not applied globally.

## Steps

1. Detect the model and reasoning-effort choices supported by the active agent tools. Do not write an unverified model name. `inherit-parent` and `auto` keep the parent model.
2. Load the existing JSON if present. Preserve the current budget and role choices; drop retired roles.
3. Ask for a budget: `unlimited` requests max, `large` requests xhigh, `medium` requests high, and `small` requests medium. Apply supported efforts to real model entries, keeping inheritance unchanged. Show the resulting roles and ask which choices to change. Do not replace a configured model family with another without a user choice.
4. Validate every chosen model and reasoning effort against the available set.
5. Write `budget` and `roles` as JSON. A role value is an object with `model` and optional `reasoning_effort`. Panel and pool values are lists of these objects; panel length sets the agent count and a pool supplies one cross-judge. Preserve unspecified choices and parse the written file to validate it.
6. Report the path and effective choices. They apply when a skill next reads them.
7. If the project has no way to drive the app for proof, offer once to create one with `$create-verification-skill`.

Roles: `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `hardest tasks`, `how explorer`, `how explainer`, `why investigators`, `why synthesizer`, `reflect tooling`, `reflect judgment, divergent, synthesizer`, `swarm workers`.

Panels: `arena runners`, `architect runners`, `interrogate reviewers`. Pool: `arena cross-judge pool`.
'''

    # Source references to retired skills remain excluded from this installation.
    text = '\n'.join(row for row in text.split('\n') if not any(name in row for name in EXCLUDED - {'typescript-best-practices'}))
    text = '\n'.join(row for row in text.split('\n') if not (row.startswith('|') and 'typescript-best-practices' in row))
    text = re.sub(r'^- No formal verification skill.*\n', '', text, flags=re.M)
    text = text.replace(' For TypeScript syntax, see the `typescript-best-practices` skill.', '')
    text = text.replace('- Frontmatter `disable-model-invocation: true` by default.', '- Set `policy.allow_implicit_invocation: false` in `agents/openai.yaml` by default.')

    # Native metadata, invocation syntax and filesystem locations.
    names = {p.parent.name for p in (ROOT / 'repos/pstack/pstack/skills').glob('*/SKILL.md')}
    text = re.sub(r'(?<![\w./:])/(%s)\b' % '|'.join(sorted(names, key=len, reverse=True)), lambda m: '$' + m[1], text)
    text = text.replace("Cursor's built-in `create-skill`", '`skill-creator`')
    text = text.replace('**create-skill** skill (Cursor\'s built-in for authoring SKILL.md files)', '**skill-creator** skill')
    text = text.replace('**create-skill** skill', '**skill-creator** skill').replace('`create-skill`', '`skill-creator`').replace('/create-skill', '$skill-creator')
    text = text.replace('~/.cursor/rules/pstack-models.mdc', '${CODEX_HOME:-$HOME/.codex}/pstack/roles.json').replace('`pstack-models.mdc` rule', '`roles` configuration from `$setup-pstack`')
    text = text.replace('configured by `$setup-pstack`', 'from `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json`')
    text = text.replace('~/.cursor/skills/', '~/.agents/skills/').replace('.cursor/skills/', '.agents/skills/').replace('~/.cursor/plugins/', '~/.agents/skills/')
    text = text.replace(' (default `grok-4.7-xhigh-fast`)', '').replace(' (default `claude-opus-5-5-xhigh`)', '')
    text = text.replace('default `grok-4.7-xhigh-fast`', 'default inherited model').replace('default `claude-opus-5-5-xhigh`', 'default inherited model')
    text = text.replace('`grok-4.7-xhigh-fast`', '`inherit-parent`').replace('`claude-opus-5-5-xhigh`', '`inherit-parent`')
    text = text.replace('Pick each subagent\'s reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.', 'Use the configured role and supported reasoning effort.')
    text = text.replace('Pick each subagent\'s reasoning level and fast or standard speed for the job, per the Subagents section.', 'Use the configured role and supported reasoning effort.')
    text = text.replace('`run_in_background: true`, ', '').replace(' with `run_in_background: true`', '')
    text = text.replace('`subagent_type: "poteto-agent"` and an explicit model per the Subagents section', 'the playbook-delegate brief from the Subagents section')
    text = text.replace('`subagent_type: generalPurpose`, ', '').replace('`readonly: true`', 'read-only scope')
    text = text.replace('`environment: "cloud"`', 'an isolated worktree').replace('`environment: "local"`', 'the current machine').replace('`cloud_base_branch`', 'the base revision')
    text = re.sub(r'\bTask tool\b', 'agent tool', text).replace('`Task`', '`spawn_agent`').replace('Task subagent', 'subagent').replace('Task response', 'agent response')
    text = text.replace('`AskQuestion` tool (structured multi-choice)', 'available question tool').replace('`AskQuestion`', 'a user question').replace('AskQuestion', 'structured questions')
    text = text.replace('Cursor\'s `/loop` command (a built-in, not a pstack skill)', "the host's event watcher or scheduled wake-up")
    text = text.replace('`/loop 1h`', 'an hourly scheduled wake-up').replace('`/loop`', "the host's scheduled loop").replace('/loop until', 'run until')
    text = text.replace('Cursor cloud agent', 'isolated background agent').replace('cloud agent\'s status in the Cursor dashboard', 'agent status from the host').replace('a Cursor restart', 'a host restart').replace('a Cursor restart', 'a host restart').replace('After a Cursor restart', 'After a host restart')
    text = text.replace('not Cursor\'s built-in babysit skill', 'not another babysit skill').replace('replaces Cursor\'s built-in babysit skill', 'owns the babysit workflow')
    text = text.replace('the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`)', 'a slop review of the diff')
    text = text.replace('Run `/deslop` from `cursor-team-kit` over the diff before commit', 'Review the diff for slop before commit')
    text = text.replace('`control-ui` or `control-cli` runtime verification (from `cursor-team-kit`)', 'runtime verification through the project harness or app-control tools')
    text = text.replace('via the control skill', 'via the project harness or available control tools')
    text = text.replace('Browser, Electron, and web UIs use `control-ui` from `cursor-team-kit`. CLIs and TUIs use `control-cli` from `cursor-team-kit`.', 'Browser, Electron, web UI, CLI, and TUI checks use the matching project harness or available control tools.')
    text = text.replace('Run `/loop`', 'Run the scheduled loop')
    text = text.replace("Cursor's the host's scheduled loop command", "the host's scheduled loop")
    text = text.replace("Cursor's Plan Mode", 'Plan mode')
    text = text.replace('a isolated background agent', 'an isolated background agent')
    text = text.replace('Each live lane runs on its own cloud VM', 'Each live lane runs in its own isolated worktree')
    text = text.replace("current agent's store (path in the system prompt)", "recorded durable store under `.audit/pstack/<task-slug>/` in the main checkout; give every owner its absolute path")
    text = text.replace("root agent's store (path in the system prompt)", "root's recorded `.audit/pstack/<task-slug>/` store in the main checkout")
    text = text.replace("under the agent store's `docs/`", "under `.audit/pstack/<task-slug>/docs/` in the main checkout")
    text = text.replace('such as `control-ui` or `control-cli` from `cursor-team-kit`', 'the project harness or available app-control tools')
    text = text.replace('Drive through `control-ui` or `control-cli` from `cursor-team-kit`.', 'Drive through the project harness or available app-control tools.')
    text = text.replace('Run `/deslop` before each commit', 'Review the diff for slop before each commit').replace('`/deslop`', 'a slop review')
    text = text.replace('nesting works to depth 3, and a nested spawn has the full Task schema including `environment`', 'nesting follows the host\'s supported depth and agent schema')
    text = text.replace("Read this run's transcript under the active workspace's `agent-transcripts/` directory (the system prompt names the path). Don't glob across `~/.cursor/projects/*/`. That reads unrelated private chats.", "Read this run's supported host history or explicitly identified workspace transcript. Mark missing tool traces as unverified.")
    text = text.replace("A local transcript under the active workspace's `agent-transcripts/` directory (the system prompt names the path. Do not glob across `~/.cursor/projects/*/`, that crosses workspace boundaries and reads private chats from unrelated projects), a cloud-agent URL, or a pushed branch.", 'Supported host history, an explicitly identified workspace transcript, a task identifier, or a pushed branch.')
    text = text.replace("Read each candidate's local transcript under the active workspace's `agent-transcripts/` directory (the system prompt names this path). Do not glob across `~/.cursor/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects.", "Read each candidate's supported host tool traces or explicitly identified workspace transcript. Mark unavailable traces as unverified.")
    text = text.replace('../../docs/', '../../repos/pstack/pstack/docs/')
    if relative.startswith('poteto-mode/playbooks/'):
        text = re.sub(r'(?<![\w./-])scripts/([\w./-]*[\w/])', lambda m: '"${PSTACK_SKILLS_ROOT}/poteto-mode/scripts/' + m[1] + '"', text)
        text = text.replace('node pstack/skills/poteto-mode/scripts/check-plan.mjs', 'node "${PSTACK_SKILLS_ROOT}/poteto-mode/scripts/check-plan.mjs"')
        text = re.sub(r'git show origin/main:pstack/skills/([^`\n]+)', r'cat "${PSTACK_SKILLS_ROOT}/\1"', text)
        text = text.replace('pstack/skills/', '${PSTACK_SKILLS_ROOT}/')
        text = text.replace('Read these from trunk at program start. Re-read them at every tick.', 'Read the installed skill sources below and the project control skill from trunk at program start. Re-read them at every tick.')
    if relative == 'statechart/SKILL.md':
        text = text.replace('`node pstack/skills/statechart/scripts/statechart.mjs`', '`node scripts/statechart.mjs`')
    return text.rstrip('\n') + '\n'


def expected_files(root=ROOT):
    source = root / 'repos/pstack/pstack/skills'
    files = {}
    for folder in sorted(source.iterdir()):
        if folder.name in EXCLUDED or not (folder / 'SKILL.md').is_file():
            continue
        original = (folder / 'SKILL.md').read_text()
        for path in folder.rglob('*'):
            if not path.is_file() or 'node_modules' in path.parts:
                continue
            relative = path.relative_to(source).as_posix()
            payload = path.read_bytes()
            if path.suffix == '.md':
                payload = render(payload.decode(), relative).encode()
            elif relative == 'poteto-mode/scripts/worktree-audit.sh':
                text = payload.decode()
                text = text.replace('# Transcripts dir: ~/.cursor/projects/<slugified-repo-path>/agent-transcripts.\nslug=$(printf \'%s\' "$main_wt" | sed \'s#^/##; s#/#-#g\')\ntranscripts="$HOME/.cursor/projects/$slug/agent-transcripts"', '# Optional workspace transcript directory supplied by the caller.\ntranscripts="${PSTACK_TRANSCRIPTS:-}"')
                payload = text.encode()
            files[relative] = payload
        implicit = 'false' if 'disable-model-invocation: true' in original else 'true'
        files[f'{folder.name}/agents/openai.yaml'] = f'policy:\n  allow_implicit_invocation: {implicit}\n'.encode()
    persona = source.parent / 'agents/comment-sicko.md'
    if persona.exists():
        files['no-comments/references/comment-sicko.md'] = render(persona.read_text(), 'no-comments/references/comment-sicko.md').encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report drift without writing.')
    args = parser.parse_args()
    pin_row = next(row for row in (ROOT / 'UPSTREAM.md').read_text().splitlines() if row.startswith('| Poteto |'))
    pin = re.findall(r'`([0-9a-f]{40})`', pin_row)[-1]
    revision = subprocess.check_output(['git', '-C', str(ROOT / 'repos/pstack'), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != pin:
        parser.error(f'Poteto checkout is at {revision}, expected {pin}')
    dirty = subprocess.check_output(['git', '-C', str(ROOT / 'repos/pstack'), 'status', '--porcelain'], text=True).strip()
    if dirty:
        parser.error('Poteto source has local changes; preserve or resolve them before regeneration.')
    files = expected_files()
    changed = []
    for relative, payload in files.items():
        destination = ROOT / 'skills' / relative
        if not destination.exists() or destination.read_bytes() != payload:
            changed.append(relative)
            if not args.check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(payload)
                original = ROOT / 'repos/pstack/pstack/skills' / relative
                if original.exists():
                    destination.chmod(original.stat().st_mode & 0o777)
    for relative in REMOVED:
        destination = ROOT / 'skills' / relative
        if destination.exists():
            changed.append(relative + ' (remove)')
            if not args.check:
                destination.unlink()
    if args.check and changed:
        print('Poteto port drift:\n' + '\n'.join(changed), file=sys.stderr)
        return 1
    print(f'{len(files)} upstream-derived files {"match" if args.check else "generated"}; {len(changed)} changes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
