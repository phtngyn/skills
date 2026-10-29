"""Check the port's observable output at native compatibility boundaries."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/port_poteto.py'
SPEC = importlib.util.spec_from_file_location('port_poteto', SCRIPT)
porter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(porter)


class PortTests(unittest.TestCase):
    def test_domain_body_survives_metadata_conversion(self):
        body = '# Principle\n\nPreserve the invariant, exact gates, and reviewer count.\n'
        source = '---\nname: principle-example\ndescription: Example.\ndisable-model-invocation: true\n---\n\n' + body
        result = porter.render(source, 'principle-example/SKILL.md')
        self.assertEqual(result.split('\n---\n', 1)[1], '\n' + body)
        self.assertNotIn('disable-model-invocation', result)

    def test_script_mapping_leaves_transcript_names_intact(self):
        result = porter.render('Keep agent-transcripts/ and run bun scripts/orch/orch.ts.\n', 'poteto-mode/playbooks/prototype.md')
        self.assertIn('agent-transcripts/', result)
        self.assertIn('bun "${PSTACK_SKILLS_ROOT}/poteto-mode/scripts/orch/orch.ts"', result)

    def test_plan_reads_installed_skills_and_project_control_from_its_trunk(self):
        source = ('node pstack/skills/poteto-mode/scripts/check-plan.mjs <plan>\n'
                  'git show origin/main:pstack/skills/swarm/SKILL.md`\n'
                  'git show origin/main:<control skill path>`\n')
        result = porter.render(source, 'poteto-mode/playbooks/prototype.md')
        self.assertIn('node "${PSTACK_SKILLS_ROOT}/poteto-mode/scripts/check-plan.mjs" <plan>', result)
        self.assertIn('cat "${PSTACK_SKILLS_ROOT}/swarm/SKILL.md"`', result)
        self.assertIn('git show origin/main:<control skill path>`', result)

    def test_refresh_removes_tracked_obsolete_helpers_without_touching_personal_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            paths = ['skills/statechart/scripts/old.mjs', 'skills/effect/SKILL.md']
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('existing content\n')
            subprocess.run(['git', '-C', str(root), 'add', 'skills'], check=True)
            local = root / 'skills/statechart/local-notes.md'
            local.write_text('untracked notes\n')
            expected = {'statechart/SKILL.md': b'new skill\n'}
            self.assertEqual(porter.obsolete_files(root, expected), ['statechart/scripts/old.mjs'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
