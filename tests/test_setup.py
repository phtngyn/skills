"""Exercise setup against local Git sources and isolated installation directories."""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/setup.sh"
SKILLS = ("bro", "build", "design", "effect", "show-me-your-work", "write")


def git(directory, *arguments):
    return subprocess.check_output(
        ["git", "-C", str(directory), "-c", "user.name=Setup Test",
         "-c", "user.email=setup-test@example.invalid", *arguments],
        text=True, stderr=subprocess.DEVNULL,
    ).strip()


def snapshot(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        key = str(path.relative_to(directory))
        if path.is_symlink():
            result[key] = ("link", str(path.readlink()), path.lstat().st_mtime_ns)
        elif path.is_file():
            result[key] = ("file", hashlib.sha256(path.read_bytes()).hexdigest())
        else:
            result[key] = ("directory",)
    return result


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skills setup test ")
        self.base = Path(self.temporary.name)
        self.root = self.base / "collection with spaces"
        self.origin = self.base / "local upstream"
        self.target = self.base / "global skills"
        self.origin.mkdir()
        git(self.origin, "init", "-b", "main")
        (self.origin / "SKILL.md").write_text("---\nname: bro\ndescription: Simplify text.\n---\nOriginal source.\n")
        (self.origin / "LICENSE").write_text("Fixture license.\n")
        (self.origin / "source-version").write_text("adopted\n")
        (self.origin / "unrelated").mkdir()
        (self.origin / "unrelated/file.md").write_text("Not needed by sparse checkout.\n")
        git(self.origin, "add", ".")
        git(self.origin, "commit", "-m", "adopted source")
        self.pin = git(self.origin, "rev-parse", "HEAD")
        (self.origin / "source-version").write_text("newer upstream\n")
        git(self.origin, "commit", "-am", "newer source")
        self.tip = git(self.origin, "rev-parse", "HEAD")
        (self.root / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.root / "scripts/setup.sh")
        for name in SKILLS:
            package = self.root / "skills" / name
            package.mkdir(parents=True)
            if name == "bro":
                (package / "SKILL.md").symlink_to("../../repos/source/SKILL.md")
                (package / "LICENSE").symlink_to("../../repos/source/LICENSE")
            else:
                (package / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Fixture skill.\n---\n")
        self.write_sources()

    def tearDown(self):
        self.temporary.cleanup()

    def write_sources(self, repo="repos/source", pin=None, remote=None):
        (self.root / "UPSTREAM.md").write_text(
            "| Source | Repository | Local clone | Last fetched | Based on |\n"
            "| --- | --- | --- | --- | --- |\n"
            f"| Fixture | {remote or self.origin.as_uri()} | `{repo}` | `{self.tip}` | `{pin or self.pin}` |\n"
        )

    def run_setup(self, *arguments, succeeds=True):
        result = subprocess.run(
            ["bash", str(self.root / "scripts/setup.sh"), "--target", str(self.target), *arguments],
            cwd=self.base, text=True, capture_output=True,
        )
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_install_uses_adopted_pin_and_links_all_skills(self):
        self.run_setup()
        checkout = self.root / "repos/source"
        self.assertEqual(git(checkout, "rev-parse", "HEAD"), self.pin)
        self.assertNotEqual(self.pin, self.tip)
        self.assertEqual((checkout / "source-version").read_text(), "adopted\n")
        self.assertEqual(sorted(path.name for path in self.target.iterdir()), sorted(SKILLS))
        for name in SKILLS:
            self.assertTrue((self.target / name).is_symlink())
            self.assertEqual((self.target / name).resolve(), (self.root / "skills" / name).resolve())
        self.assertIn("Original source.", (self.target / "bro/SKILL.md").read_text())

    def test_rerun_preserves_links_and_does_not_fetch(self):
        self.run_setup()
        before = snapshot(self.target)
        (self.origin / "source-version").write_text("third version\n")
        git(self.origin, "commit", "-am", "upstream advanced")
        self.run_setup()
        self.assertEqual(snapshot(self.target), before)
        self.assertEqual(git(self.root / "repos/source", "rev-parse", "origin/main"), self.tip)

    def test_check_missing_sources_creates_nothing(self):
        before = snapshot(self.root)
        self.run_setup("--check", succeeds=False)
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse(self.target.exists())

    def test_check_installed_is_read_only(self):
        self.run_setup()
        before = snapshot(self.base)
        self.run_setup("--check")
        self.assertEqual(snapshot(self.base), before)

    def test_check_reports_missing_link(self):
        self.run_setup()
        (self.target / "design").unlink()
        self.run_setup("--check", succeeds=False)
        self.assertFalse((self.target / "design").exists())

    def test_real_directory_conflict_prevents_partial_install(self):
        (self.target / "write").mkdir(parents=True)
        (self.target / "write/personal.md").write_text("Keep this.\n")
        before = snapshot(self.target)
        self.run_setup(succeeds=False)
        self.assertEqual(snapshot(self.target), before)
        self.assertFalse((self.root / "repos").exists())

    def test_dangling_foreign_link_is_a_conflict(self):
        self.target.mkdir()
        (self.target / "write").symlink_to(self.base / "missing foreign skill")
        before = snapshot(self.target)
        self.run_setup(succeeds=False)
        self.assertEqual(snapshot(self.target), before)
        self.assertFalse((self.root / "repos").exists())

    def test_revision_mismatch_is_never_reset(self):
        self.run_setup()
        checkout = self.root / "repos/source"
        git(checkout, "checkout", "--detach", self.tip)
        self.run_setup(succeeds=False)
        self.assertEqual(git(checkout, "rev-parse", "HEAD"), self.tip)
        self.assertEqual((checkout / "source-version").read_text(), "newer upstream\n")

    def test_dirty_source_is_preserved(self):
        self.run_setup()
        checkout = self.root / "repos/source"
        (checkout / "source-version").write_text("local edit\n")
        self.run_setup(succeeds=False)
        self.assertEqual((checkout / "source-version").read_text(), "local edit\n")

    def test_untracked_source_file_is_preserved(self):
        self.run_setup()
        local = self.root / "repos/source/local-notes.md"
        local.write_text("Keep this.\n")
        self.run_setup(succeeds=False)
        self.assertEqual(local.read_text(), "Keep this.\n")

    def test_unavailable_pin_cleans_failed_clone(self):
        self.write_sources(pin="f" * 40)
        self.run_setup(succeeds=False)
        self.assertFalse(self.target.exists())
        self.assertEqual(list((self.root / "repos").iterdir()), [])

    def test_broken_resource_prevents_link_creation(self):
        (self.root / "skills/design/assets").symlink_to("../../missing-assets")
        self.run_setup(succeeds=False)
        self.assertFalse(self.target.exists())

    def test_existing_relative_owned_link_is_preserved(self):
        self.target.mkdir()
        relative = os.path.relpath(self.root / "skills/design", self.target)
        (self.target / "design").symlink_to(relative)
        self.run_setup()
        self.assertEqual(str((self.target / "design").readlink()), relative)
        self.run_setup("--check")

    def test_uninstall_preserves_foreign_entries_and_removes_retired_owned_link(self):
        self.run_setup()
        alias = self.base / "collection alias"
        alias.symlink_to(self.root, target_is_directory=True)
        (self.target / "retired").symlink_to(alias / "skills/retired")
        (self.target / "foreign").symlink_to(self.base / "missing foreign skill")
        (self.target / "personal").mkdir()
        (self.target / "personal/notes.md").write_text("Keep this.\n")
        self.run_setup("--uninstall")
        self.assertEqual(sorted(path.name for path in self.target.iterdir()), ["foreign", "personal"])
        self.assertTrue((self.target / "foreign").is_symlink())
        self.assertEqual((self.target / "personal/notes.md").read_text(), "Keep this.\n")
        self.run_setup("--uninstall")

    def test_uninstall_works_without_sources(self):
        self.run_setup()
        shutil.rmtree(self.root / "repos")
        self.run_setup("--uninstall")
        self.assertEqual(list(self.target.iterdir()), [])

    def test_poteto_sparse_checkout_preserves_required_resources(self):
        upstream_skill = self.origin / "pstack/skills/bro"
        upstream_skill.mkdir(parents=True)
        shutil.copy2(self.origin / "SKILL.md", upstream_skill / "SKILL.md")
        shutil.copy2(self.origin / "LICENSE", self.origin / "pstack/LICENSE")
        git(self.origin, "add", ".")
        git(self.origin, "commit", "-m", "Poteto layout")
        pin = git(self.origin, "rev-parse", "HEAD")
        self.write_sources(repo="repos/pstack", pin=pin)
        for filename, target in [("SKILL.md", "pstack/skills/bro/SKILL.md"), ("LICENSE", "pstack/LICENSE")]:
            link = self.root / "skills/bro" / filename
            link.unlink()
            link.symlink_to(f"../../repos/pstack/{target}")
        self.run_setup()
        self.assertTrue((self.target / "bro/SKILL.md").is_file())
        self.assertFalse((self.root / "repos/pstack/unrelated").exists())
        self.assertEqual(git(self.root / "repos/pstack", "rev-parse", "HEAD"), pin)

    def test_invalid_options_do_not_create_target(self):
        self.run_setup("--unknown", succeeds=False)
        self.run_setup("--check", "--uninstall", succeeds=False)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
