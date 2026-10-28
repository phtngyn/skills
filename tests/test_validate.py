"""Check catalog and documentation failures using isolated collection fixtures."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/validate.py'
SPEC = importlib.util.spec_from_file_location('collection_validate', SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='skill validation ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.upstream = self.root / 'repos/pstack/pstack/skills'
        for name in ['alpha', 'principle-check', 'make-bot-ui', 'typescript-best-practices', 'create-formal-verification-skill', 'maintain-formal-verification-skill']:
            self.write_skill(self.upstream / name, name, upstream=True)
        for name in ['alpha', 'principle-check', *sorted(validator.PERSONAL)]:
            self.write_skill(self.root / 'skills' / name, name)
        self.skill_count = len(validator.PERSONAL) + 2
        self.readme = self.root / 'README.md'
        self.readme.write_text(
            f'# Collection\n\n{self.skill_count} skills: the 2 Poteto core skills retained.\n\n'
            '| Skill | Purpose |\n| --- | --- |\n'
            '| `alpha` | A workflow. |\n'
            + ''.join(f'| `{name}` | Personal skill. |\n' for name in sorted(validator.PERSONAL))
            + '\n'
            'The remaining 1 skills are principles:\n\n- `check`\n'
        )

    def write_skill(self, folder, name, upstream=False):
        folder.mkdir(parents=True)
        extra = 'disable-model-invocation: true\n' if upstream else ''
        (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Fixture skill.\n{extra}---\n\n# Fixture\n')
        if not upstream and name != 'effect':
            (folder / 'agents').mkdir()
            (folder / 'agents/openai.yaml').write_text('policy:\n  allow_implicit_invocation: false\n')

    def validate(self):
        return validator.validate(self.root)

    def test_current_catalog_passes_with_retired_skills_excluded(self):
        self.assertEqual(self.validate(), [])
        self.write_skill(self.root / 'skills/typescript-best-practices', 'typescript-best-practices')
        self.assertTrue(any('Catalog mismatch' in error for error in self.validate()))

    def test_unreviewed_poteto_prose_changes_are_reported_as_source_drift(self):
        document = self.root / 'skills/alpha/SKILL.md'
        document.write_text(document.read_text() + '\nReplace the upstream workflow.\n')
        self.assertTrue(any('Poteto source drift: alpha/SKILL.md' in error for error in self.validate()))

    def test_removed_runtime_manual_cannot_return(self):
        document = self.root / 'skills/poteto-mode/references/codex.md'
        document.parent.mkdir(parents=True)
        document.write_text('# Runtime manual\n')
        self.assertTrue(any('Redundant port manual' in error for error in self.validate()))

    def test_readme_must_list_every_skill_and_no_unknown_skill(self):
        original = self.readme.read_text()
        self.readme.write_text(original.replace('| `alpha` |', '| `retired` |'))
        errors = self.validate()
        self.assertTrue(any("missing=['alpha']" in error and "extra=['retired']" in error for error in errors), errors)
        self.readme.write_text(original)
        self.assertEqual(self.validate(), [])

    def test_root_documents_cannot_claim_stale_counts(self):
        doc = self.root / 'POTETO.md'
        for claim in ['9 skills', '9 Poteto skill directories', '9 principles', '9 playbooks']:
            with self.subTest(claim=claim):
                doc.write_text(claim + '\n')
                self.assertTrue(any('claims 9' in error for error in self.validate()))
        doc.write_text(f'{self.skill_count} skills, 2 Poteto skill directories, 1 principles, 0 playbooks.\n')
        self.assertEqual(self.validate(), [])

    def test_design_subskills_are_required_catalog_members(self):
        (self.root / 'skills/design-mobile/SKILL.md').unlink()
        self.assertTrue(any("missing=['design-mobile']" in error for error in self.validate()))

    def test_design_family_requires_explicit_invocation(self):
        policy = self.root / 'skills/design-ui/agents/openai.yaml'
        policy.write_text('policy:\n  allow_implicit_invocation: true\n')
        self.assertTrue(any('design-ui: Design skills require explicit invocation' in error for error in self.validate()))

    def test_design_family_cannot_load_poteto_skills(self):
        document = self.root / 'skills/design-ui/SKILL.md'
        original = document.read_text()
        document.write_text(original + '\nRead [alpha](../alpha/SKILL.md).\n')
        self.assertTrue(any('Design family cannot depend on Poteto skill alpha' in error for error in self.validate()))
        document.write_text(original + '\nRead [CSS](../design-css/SKILL.md).\n')
        self.assertEqual(self.validate(), [])

    def test_titled_links_are_checked_in_skills_and_root_docs(self):
        for document in [self.root / 'POTETO.md', self.root / 'skills/alpha/guide.md']:
            with self.subTest(document=document):
                document.write_text('[Guide](missing.md "Read the guide")\n')
                self.assertTrue(any('missing link missing.md' in error for error in self.validate()))
                document.unlink()
        self.assertEqual(self.validate(), [])

    def test_angled_paths_with_spaces_and_local_line_links_resolve(self):
        (self.root / 'A guide.md').write_text('# Résumé\n')
        (self.root / 'POTETO.md').write_text(
            '[Guide](<A guide.md#résumé> "Read this")\n'
            '[Source](skills/alpha/SKILL.md:5)\n'
            '[Site](https://example.invalid/missing.md#missing)\n'
        )
        self.assertEqual(self.validate(), [])

    def test_heading_renames_break_links_until_the_link_is_updated(self):
        guide = self.root / 'guide.md'
        guide.write_text('# Run `the check`\n\n## Run the check\n')
        (self.root / 'POTETO.md').write_text('[Repeat](guide.md#run-the-check-1 "Second heading")\n')
        self.assertEqual(self.validate(), [])
        guide.write_text('# Run the check\n\n## Updated check\n')
        self.assertTrue(any('missing heading' in error for error in self.validate()))
        (self.root / 'POTETO.md').write_text('[Updated](guide.md#updated-check)\n')
        self.assertEqual(self.validate(), [])

    def test_same_document_anchors_exclude_fenced_example_headings(self):
        document = self.root / 'skills/alpha/guide.md'
        document.write_text('# Real\n\n````md\n# Example\n```\n````\n\n[Example](#example)\n')
        self.assertTrue(any('missing heading in link #example' in error for error in self.validate()))
        document.write_text(document.read_text().replace('[Example](#example)', '[Real](#real)'))
        self.assertEqual(self.validate(), [])

    def test_upstream_prompt_link_placeholder_is_not_a_missing_resource(self):
        document = self.root / 'skills/alpha/synthesizer-prompt.md'
        document.write_text('Source: [PR #123](url).\n')
        self.assertEqual(self.validate(), [])
        document.write_text('[Actual reference](missing.md).\n')
        self.assertTrue(any('missing link missing.md' in error for error in self.validate()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
