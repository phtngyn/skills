"""Install independent skill directories and reconcile this collection's legacy links."""

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile


OWNER = 'phtngyn/skills'
RECEIPT = '.skills-install.json'
IGNORED = {'node_modules', '__pycache__', '.DS_Store'}


def legacy_link(entry, skills):
    return entry.is_symlink() and entry.resolve() == skills / entry.name


def receipt(entry):
    path = entry / RECEIPT
    if entry.is_symlink() or path.is_symlink() or not path.is_file():
        return None
    try:
        record = json.loads(path.read_text())
    except (UnicodeError, ValueError):
        return None
    if isinstance(record, dict) and record.get('owner') == OWNER:
        return record


def tree_files(root, *, installed=False, parents=()):
    """Walk resources, dereferencing legacy source links and detecting cycles."""
    resolved = root.resolve(strict=True)
    if resolved in parents:
        raise ValueError(f'cyclic resource link: {root}')
    result = {}
    for path in sorted(root.iterdir()):
        if installed and path.name == RECEIPT and not parents:
            continue
        if not installed and path.name in IGNORED:
            continue
        if not installed and path.name == RECEIPT and not parents:
            raise ValueError(f'reserved installation receipt name: {path}')
        if installed and path.is_symlink():
            raise ValueError(f'modified installation contains a symbolic link: {path}')
        if path.is_dir():
            result[path.name] = None
            result.update({
                f'{path.name}/{name}': file
                for name, file in tree_files(path, installed=installed, parents=(*parents, resolved)).items()
            })
        elif path.is_file():
            result[path.name] = path
        else:
            raise ValueError(f'unavailable skill resource: {path}')
    return result


def fingerprint(files):
    digest = hashlib.sha256()
    for name, path in sorted(files.items()):
        if path is None:
            row = (name, None)
        else:
            content = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(65536), b''):
                    content.update(chunk)
            row = (name, stat.S_IMODE(path.stat().st_mode), content.hexdigest())
        digest.update(json.dumps(row).encode())
    return digest.hexdigest()


def candidates(target, skills, names, action):
    entries = {path.name for path in target.iterdir()} if target.is_dir() else set()
    managed = {}
    for name in sorted(entries):
        entry = target / name
        if legacy_link(entry, skills):
            managed[name] = None
        elif (record := receipt(entry)) is not None:
            managed[name] = record
        elif name in names and action != 'uninstall':
            raise ValueError(f'conflict: {entry} (left unchanged)')
    for name, record in managed.items():
        if record is not None and record.get('digest') != fingerprint(tree_files(target / name, installed=True)):
            raise ValueError(f'locally modified skill: {target / name}; preserve the edits before updating or removing it')
    return managed


def sources(collection, names):
    files = {}
    for name in names:
        directory = collection / 'skills' / name
        resources = tree_files(directory)
        stageshow = collection / 'repos/benjitaylor/stageshow'
        if name == 'stageshow' and (stageshow / 'SKILL.md').is_file():
            resources = tree_files(stageshow) | resources
        if resources.get('SKILL.md') is None:
            raise ValueError(f'unavailable entry point: {name}')
        files[name] = resources
    return files


@contextmanager
def locked_target(target):
    descriptor = os.open(target, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def reconcile(collection, target, action, names):
    skills = collection / 'skills'
    wanted = set(names) if action != 'uninstall' else set()
    managed = candidates(target, skills, wanted, action)
    if action == 'preflight':
        return

    files = sources(collection, sorted(wanted)) if wanted else {}
    digests = {name: fingerprint(resources) for name, resources in files.items()}
    changed = [name for name in sorted(wanted) if (managed.get(name) or {}).get('digest') != digests[name]]
    retired = sorted(managed.keys() - wanted)
    if action == 'check':
        if changed or retired:
            raise ValueError(f'installed skills need setup: {", ".join(changed + retired)}')
    elif changed or retired:
        target.mkdir(parents=True, exist_ok=True)
        with locked_target(target):
            if managed != candidates(target, skills, wanted, action):
                raise ValueError('installation changed during setup; retry')
            with tempfile.TemporaryDirectory(prefix='.skills-install-', dir=target) as temporary:
                stage = Path(temporary)
                pending = stage / 'copies'
                backups = stage / 'backups'
                pending.mkdir()
                backups.mkdir()
                for name in changed:
                    destination = pending / name
                    destination.mkdir()
                    for relative, source in files[name].items():
                        path = destination / relative
                        if source is None:
                            path.mkdir(parents=True, exist_ok=True)
                        else:
                            path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(source, path)
                    if fingerprint(tree_files(destination, installed=True)) != digests[name]:
                        raise ValueError(f'skill source changed during setup: {name}; retry')
                    (destination / RECEIPT).write_text(json.dumps({'owner': OWNER, 'digest': digests[name]}) + '\n')
                moved = []
                published = []
                try:
                    for name in changed + retired:
                        entry = target / name
                        if name in managed:
                            entry.rename(backups / name)
                            moved.append(name)
                        elif entry.exists() or entry.is_symlink():
                            raise ValueError(f'destination changed during setup: {entry}')
                        if name in wanted:
                            (pending / name).rename(entry)
                            published.append(name)
                except BaseException:
                    for name in reversed(published):
                        (target / name).rename(pending / name)
                    for name in reversed(moved):
                        (backups / name).rename(target / name)
                    raise
    if action == 'uninstall':
        print(f'Removed {len(retired)} collection skills. Other entries were preserved.')
    else:
        print(f'{len(wanted)} skills ready in {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('preflight', 'install', 'check', 'uninstall'))
    parser.add_argument('collection', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('names', nargs='*')
    args = parser.parse_args()
    try:
        reconcile(args.collection, args.target, args.action, args.names)
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f'error: {error}\n')


if __name__ == '__main__':
    main()
