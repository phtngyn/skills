### Authoring a skill

1. Use Codex's `skill-creator` when available. Inspect existing instructions and the skill's actual callers before changing it.
2. Ground the workflow in the task, source code, and available tool schemas. Keep essential decisions in `SKILL.md`; link conditional detail from references. Resolve resources relative to the skill's real directory.
3. Use supported frontmatter and `agents/openai.yaml`. Preserve existing invocation policy unless the user asks to change it. Use `.agents/skills/<name>/` for project skills and the configured personal skill directory for personal skills.
4. Check references, scripts, descriptions, and realistic routing. Run the available skill validator. For complex changes, independently exercise a realistic task in an isolated workspace, then inspect its actual result.
5. Apply `unslop`. Deliver the validated files; commit or publish only within the task's delivery scope.
