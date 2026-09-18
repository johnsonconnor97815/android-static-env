#!/usr/bin/env python3
"""Check the portable skill package and its local links without third-party modules."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/android-static-env'


def validate():
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    front = text.split('---\n', 2)
    assert len(front) == 3 and front[0] == '', 'Missing YAML frontmatter'
    # This package deliberately uses only flat string fields in its frontmatter.
    fields = dict(line.split(': ', 1) for line in front[1].splitlines() if line)
    assert fields['name'] == SKILL.name
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', fields['name'])
    assert len(fields['name']) <= 64 and 0 < len(fields['description']) <= 1024
    assert fields['license'] == 'MIT'
    assert len(text.splitlines()) < 500
    assert (SKILL / 'LICENSE').read_bytes() == (ROOT / 'LICENSE').read_bytes()
    required = ['scripts/setup.py', 'scripts/smoke.py', 'scripts/inspect_so.py',
                'scripts/test_setup.py', 'assets/toolchain.lock.json', 'agents/openai.yaml',
                'scripts/mcp_setup.py', 'scripts/mcp_probe.py', 'scripts/mcp_smoke.py',
                'scripts/ghidra_mcp_entry.py', 'scripts/test_mcp.py',
                'assets/mcp.lock.json', 'references/mcp.md']
    assert all((SKILL / p).is_file() for p in required)
    for file in SKILL.rglob('*'):
        if not file.is_file() or '__pycache__' in file.parts:
            continue
        assert not file.is_symlink(), f'External or broken resource symlink: {file}'
        assert file.stat().st_size < 1_000_000, f'Unexpected large artifact: {file}'
        if file.suffix == '.json':
            json.loads(file.read_text(encoding='utf-8'))
        if file.suffix == '.py':
            ast.parse(file.read_text(encoding='utf-8'), filename=str(file))
        if file.suffix == '.md':
            body = file.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)', body):
                if urlparse(target).scheme or target.startswith('#'):
                    continue
                linked = (file.parent / unquote(target.split('#', 1)[0])).resolve()
                assert linked.is_relative_to(SKILL.resolve()), f'Link escapes installed skill: {target}'
                assert linked.exists(), f'Missing packaged link: {file}: {target}'
    lock = json.loads((SKILL / 'assets/toolchain.lock.json').read_text())
    assert lock['schema'] == 1 and lock['platform'] == 'linux-x86_64'
    assert {'ghidra', 'rizin', 'sdk', 'jadx', 'apktool'} <= lock['artifacts'].keys()
    assert {'lief', 'pyelftools', 'capstone'} == {'lief', *lock['python']['native-python']['extra_packages']}
    for entry in list(lock['artifacts'].values()) + lock['smali']['artifacts']:
        assert entry['url'].startswith('https://')
        checksum = entry.get('checksum')
        if checksum:
            algorithm, value = checksum.split(':', 1)
            assert algorithm in ['sha1', 'sha256']
            assert len(value) == {'sha1': 40, 'sha256': 64}[algorithm]
            assert re.fullmatch('[0-9a-f]+', value)
    mcp = json.loads((SKILL / 'assets/mcp.lock.json').read_text())
    assert mcp['schema'] == 1
    for recipe in mcp['artifacts'].values():
        assert recipe['url'].startswith('https://')
        if recipe.get('checksum'):
            assert re.fullmatch(r'sha256:[0-9a-f]{64}', recipe['checksum'])
    assert mcp['artifacts']['mcp-jadx-plugin']['version'] == mcp['artifacts']['mcp-jadx-server']['version']
    assert re.fullmatch('[0-9a-f]{40}', mcp['artifacts']['mcp-jadx-plugin-source']['git_blob_sha1'])
    print('Portable Agent Skills package: valid')
    return 0


if __name__ == '__main__':
    sys.exit(validate())
