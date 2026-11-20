"""Check the Codex patch, untouched resources, and invocation metadata."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch as mock_patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/port_poteto.py'
SPEC = importlib.util.spec_from_file_location('port_poteto', SCRIPT)
porter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(porter)


class PortTests(unittest.TestCase):
    def test_import_applies_codex_patch_and_preserves_unmodified_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'repos/pstack/pstack/skills/example'
            source.mkdir(parents=True)
            entry = (
                b'---\nname: example\ndescription: Use /example.\n'
                b'disable-model-invocation: true\nicon: crown\ncolor: yellow\n'
                b'license: MIT\n---\nUse the upstream tool.\n'
            )
            (source / 'SKILL.md').write_bytes(entry)
            (source / 'resource.bin').write_bytes(b'\x00\xff\r\n')
            (source / 'guide.md').write_bytes(
                b'Run /example. Read ../example/SKILL.md and https://example.org/example.\r\n'
                b'Keep /example-long and /make-bot-ui unchanged.\r\n'
            )
            patch = root / 'scripts/poteto-codex.patch'
            patch.parent.mkdir()
            patch.write_text(
                'diff --git a/example/SKILL.md b/example/SKILL.md\n'
                '--- a/example/SKILL.md\n+++ b/example/SKILL.md\n'
                '@@ -5,2 +5,2 @@\n ---\n-Use the upstream tool.\n+Use the Codex tool.\n'
                'diff --git a/example/reference.md b/example/reference.md\n'
                'new file mode 100644\n'
                '--- /dev/null\n+++ b/example/reference.md\n'
                '@@ -0,0 +1 @@\n+# Codex reference\n'
            )
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            scratch_parent = root / 'scratch'
            scratch_parent.mkdir()
            with mock_patch.object(tempfile, 'tempdir', str(scratch_parent)):
                files = porter.expected_files(root)
            self.assertEqual(
                files['example/SKILL.md'],
                b'---\nname: example\ndescription: Use $example.\nlicense: MIT\n---\nUse the Codex tool.\n',
            )
            self.assertEqual(files['example/reference.md'], b'# Codex reference\n')
            self.assertEqual(files['example/resource.bin'], b'\x00\xff\r\n')
            self.assertEqual(
                files['example/guide.md'],
                b'Run $example. Read ../example/SKILL.md and https://example.org/example.\r\n'
                b'Keep /example-long and /make-bot-ui unchanged.\r\n',
            )
            self.assertEqual(files['example/agents/openai.yaml'], b'policy:\n  allow_implicit_invocation: false\n')
            self.assertEqual((source / 'SKILL.md').read_bytes(), entry)

            (source / 'SKILL.md').write_bytes(entry.replace(b'the upstream tool', b'another tool'))
            with self.assertRaisesRegex(ValueError, 'Codex port does not apply'):
                porter.expected_files(root)

    def test_missing_patch_in_collection_checkout_is_an_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'repos/pstack/pstack/skills').mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, 'Missing Codex port patch'):
                porter.expected_files(root)

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
