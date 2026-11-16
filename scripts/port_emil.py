#!/usr/bin/env python3
"""Copy retained Emil skills byte for byte with explicit invocation metadata."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'ask-sonner', 'pick-ui-library', 'write-swift', 'animate-expo'}
NAMES = {'ask-emil', 'animate', 'animation-performance', 'animation-vocabulary',
         'apple-design', 'break-ui', 'choreograph', 'emil-design-eng',
         'find-animation-opportunities', 'gestures', 'improve-animations',
         'learn-taste', 'mobile-native', 'prototype', 'remove-animations', 'review-animations'}


def expected_files(root=ROOT):
    source = root / 'repos/emil'
    files = {}
    for name in sorted(NAMES):
        folder = source / 'skills' / name
        if not (folder / 'SKILL.md').is_file():
            raise FileNotFoundError(f'Missing Emil entry point: {folder / "SKILL.md"}')
        for path in folder.rglob('*'):
            if not path.is_file():
                continue
            relative = Path(name) / path.relative_to(folder)
            data = path.read_bytes()
            files[str(relative)] = data
        files[f'{name}/agents/openai.yaml'] = b'policy:\n  allow_implicit_invocation: false\n'
        files[f'{name}/LICENSE'] = (source / 'LICENSE').read_bytes()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    for relative, data in expected_files().items():
        target = ROOT / 'skills' / relative
        if target.is_symlink() or not target.is_file() or target.read_bytes() != data:
            changed.append(relative)
            if not args.check:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.is_symlink():
                    target.unlink()
                target.write_bytes(data)
    if args.check and changed:
        print('Emil port drift:\n' + '\n'.join(changed), file=sys.stderr)
        return 1
    print(f'Emil skills: {len(changed)} files {"need updates" if args.check else "updated"}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
