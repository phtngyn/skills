"""Check exact upstream copies and explicit invocation metadata."""
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
    def test_import_preserves_frontmatter_body_paths_and_binary_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'repos/pstack/pstack/skills/example'
            source.mkdir(parents=True)
            entry = b'---\nname: example\ndescription: Example.\ndisable-model-invocation: true\nicon: original\n---\nUse /make-bot-ui and `Task`. Read ~/.cursor/rules/pstack-models.mdc.\n'
            (source / 'SKILL.md').write_bytes(entry)
            (source / 'resource.bin').write_bytes(b'\x00\xff\r\n')
            (source / 'guide.md').write_bytes(b'Run scripts/tool.ts\r\n')
            files = porter.expected_files(root)
            self.assertEqual(files['example/SKILL.md'], entry)
            self.assertEqual(files['example/resource.bin'], b'\x00\xff\r\n')
            self.assertEqual(files['example/guide.md'], b'Run scripts/tool.ts\r\n')
            self.assertEqual(files['example/agents/openai.yaml'], b'policy:\n  allow_implicit_invocation: false\n')

    def test_skills_without_upstream_invocation_flag_are_still_explicit_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'repos/pstack/pstack/skills/example'
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('---\nname: example\ndescription: Example.\n---\n')
            files = porter.expected_files(root)
            self.assertEqual(files['example/agents/openai.yaml'], b'policy:\n  allow_implicit_invocation: false\n')

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
