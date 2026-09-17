#!/usr/bin/env python3
"""Install via the real skills CLI and verify every packaged resource for each agent."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/android-static-env'
CLI_VERSION = '1.6.0'
AGENTS = {
    'codex': '.agents/skills',
    'claude-code': '.claude/skills',
    'cursor': '.agents/skills',
    'github-copilot': '.agents/skills',
    'gemini-cli': '.agents/skills',
    'opencode': '.agents/skills',
    'windsurf': '.windsurf/skills',
    'cline': '.agents/skills',
    'roo': '.roo/skills',
}


def inventory(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=str(ROOT), help='Local repository or public GitHub source')
    parser.add_argument('--agent', choices=AGENTS, action='append', help='Defaults to all documented agents')
    parser.add_argument('--mode', choices=['copy', 'symlink'], default='copy')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    npx = shutil.which('npx')
    if not npx:
        parser.error('Node.js >=22.20.0 and npm/npx are required')
    env = dict(os.environ, DISABLE_TELEMETRY='1', DO_NOT_TRACK='1', CI='1')
    expected = inventory(SKILL)
    results = []
    for name in args.agent or AGENTS:
        with tempfile.TemporaryDirectory(prefix='android-skill-install-') as workspace:
            workspace = Path(workspace)
            command = [npx, '--yes', 'skills@' + CLI_VERSION, 'add', args.source,
                       '--skill', 'android-static-env', '--agent', name, '--yes']
            if args.mode == 'copy':
                command.append('--copy')
            if os.name == 'nt':
                command = ['cmd.exe', '/d', '/c'] + command
            result = subprocess.run(command, cwd=workspace, env=env, capture_output=True, text=True, timeout=180)
            installed = workspace / AGENTS[name] / 'android-static-env'
            error = None
            if result.returncode:
                error = 'Installer returned ' + str(result.returncode)
            elif not installed.is_dir():
                error = 'Skill missing from agent discovery directory: ' + AGENTS[name]
            elif inventory(installed) != expected:
                error = 'Installed resources differ from the distributable skill'
            elif (workspace / '.android-static').exists():
                error = 'Installing the skill unexpectedly started toolchain provisioning'
            record = {'agent': name, 'mode': args.mode, 'path': AGENTS[name] + '/android-static-env',
                      'status': 'failed' if error else 'passed', 'error': error,
                      'file_count': len(expected), 'installer_exit_code': result.returncode}
            if error:
                record['stdout'] = result.stdout
                record['stderr'] = result.stderr
                print(result.stdout, result.stderr, file=sys.stderr)
            results.append(record)
            print(f'{record["status"].upper()} {name}: {record["path"]} ({len(expected)} files)', flush=True)
    report = {'cli': 'skills@' + CLI_VERSION, 'source': args.source, 'mode': args.mode, 'results': results,
              'scope': 'Real installer, discovery paths, all resource hashes; does not run models or provision Android tools.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return int(any(r['status'] != 'passed' for r in results))


if __name__ == '__main__':
    sys.exit(run())
