#!/usr/bin/env python3
"""Check declared delivery files without discovering ignored private contents.

This local guard is complementary to Gitleaks and human privacy review. It does
not inspect Git history, interpret images or certify an absence of secrets.
Default output contains rule counts, never matched content or filenames.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

MAX_TEXT_BYTES = 2 * 1024 * 1024
PRIVATE_PARTS = {'.internal', '.local', '.venv', 'venv', '__pycache__', '.pytest_cache',
                 'private', 'manuscripts', 'raw-reviews', 'node_modules'}
SECRET_NAMES = {'id_rsa', 'id_ed25519', 'credentials.json', 'service-account.json',
                '.npmrc', '.pypirc', '.netrc'}
ENV_EXAMPLES = {'.env.example', '.env.sample', '.env.template'}
# Split path/prefix spellings in source so these patterns are not their own
# synthetic leakage fixtures. Placeholder roots such as $HOME remain valid.
MACHINE_PATH = re.compile(r'(?:/' + r'(?:Users|home)/\w[\w.-]{0,63}|'
                          r'(?i:[A-Z]:(?:[\\/]){1,2}Users(?:[\\/]){1,2}[\w][\w. -]{0,63}))')
PUBLIC_URL = re.compile(r'https?://[^\s<>"\x27`]+', re.IGNORECASE)
CREDENTIAL = re.compile(r'(?:gh[pousr]' + r'_[A-Za-z0-9]{30,255}|github_pat' +
                        r'_[A-Za-z0-9_]{60,255}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE' + r' KEY-----)')
SESSION_DATA = re.compile(r'(?:Message Type' + r': (?:NEW_TASK|FINAL_ANSWER)|<environment_' +
                          r'context>|<multi_agent_' + r'role>)')


def private_path(name):
    parts = PurePosixPath(name).parts
    if any(part.lower() in PRIVATE_PARTS for part in parts):
        return True
    leaf = parts[-1].lower() if parts else ''
    return (leaf in SECRET_NAMES or leaf.startswith('.env') and leaf not in ENV_EXAMPLES
            or leaf.endswith(('.log', '.pem', '.key', '.p12', '.pfx', '.zip', '.tar', '.gz', '.7z', '.rar'))
            or bool(re.search(r'(?:^|[-_.])(?:private[-_](?:manuscript|draft)|raw[-_](?:review|audit|scan|session))(?:[-_.]|$)', leaf)))


def safe_name(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and str(path) == name and '..' not in path.parts and '\\' not in name and '\x00' not in name


def regular_inside(root, path):
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink():
            return False
    if not path.resolve().is_relative_to(root) or not path.is_file():
        return False
    info = path.stat()
    # An ignored private file can otherwise be read through a public hard link.
    return stat.S_ISREG(info.st_mode) and info.st_nlink == 1


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise ValueError('Cannot read the selected Git inventory.')
    return result.stdout


def new_report():
    return {'status': 'PASS', 'files_checked': 0, 'binary_files': 0, 'issues': []}


def issue(report, path, rule):
    report['status'] = 'FAIL'
    report['issues'].append({'path': path, 'rule': rule})


def recognized_image(name, content):
    """Recognize declared image types for separate manual review, not certify them."""
    suffix = Path(name).suffix.lower()
    return ((suffix == '.png' and content.startswith(b'\x89PNG\r\n\x1a\n'))
            or (suffix in {'.jpg', '.jpeg'} and content.startswith(b'\xff\xd8\xff'))
            or (suffix == '.gif' and content.startswith((b'GIF87a', b'GIF89a')))
            or (suffix == '.webp' and content.startswith(b'RIFF') and content[8:12] == b'WEBP'))


def inspect_content(report, name, content):
    report['files_checked'] += 1
    if len(content) > MAX_TEXT_BYTES:
        issue(report, name, 'file_size_coverage')
        return
    if recognized_image(name, content):
        report['binary_files'] += 1
        return
    if b'\0' in content:
        issue(report, name, 'text_decode_coverage')
        return
    try:
        text = content.decode('utf-8-sig')
    except UnicodeError:
        issue(report, name, 'text_decode_coverage')
        return
    # Public web URLs may legitimately contain a /home/... path. Exclude those
    # spans only from machine-path detection; credentials are still scanned.
    url_spans = [match.span() for match in PUBLIC_URL.finditer(text)]
    if any(not any(start <= match.start() < end for start, end in url_spans)
           for match in MACHINE_PATH.finditer(text)):
        issue(report, name, 'machine_path')
    for pattern, rule in ((CREDENTIAL, 'credential_pattern'), (SESSION_DATA, 'agent_session')):
        if pattern.search(text):
            issue(report, name, rule)


def inspect_file(root, report, name):
    if not safe_name(name) or private_path(name):
        issue(report, name, 'private_path')
        return
    path = root / name
    if not regular_inside(root, path):
        issue(report, name, 'unsafe_file')
        return
    if path.stat().st_size > MAX_TEXT_BYTES:
        issue(report, name, 'file_size_coverage')
        return
    inspect_content(report, name, path.read_bytes())


def check_repository(root, index=False):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Selected repository does not exist.')
    top = Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel')).strip()).resolve()
    if top != root:
        raise ValueError('Select the repository root, not a nested directory.')
    report = new_report()
    if index:
        records = git(root, 'ls-files', '--stage', '-z').split(b'\0')
        for record in filter(None, records):
            header, raw_name = record.split(b'\t', 1)
            mode, oid, stage = header.decode('ascii').split()
            name = os.fsdecode(raw_name)
            if not safe_name(name) or private_path(name):
                issue(report, name, 'private_path')
            elif mode not in {'100644', '100755'} or stage != '0':
                issue(report, name, 'unsafe_index_entry')
            elif int(git(root, 'cat-file', '-s', oid)) > MAX_TEXT_BYTES:
                issue(report, name, 'file_size_coverage')
            else:
                inspect_content(report, name, git(root, 'cat-file', 'blob', oid))
    else:
        names = {os.fsdecode(value) for value in git(root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').split(b'\0') if value}
        for name in sorted(names):
            # A tracked deletion is not part of the current worktree delivery.
            if not (root / name).exists() and not (root / name).is_symlink():
                continue
            inspect_file(root, report, name)
    return report


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate package manifest key.')
        result[key] = value
    return result


def check_package(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Selected export does not exist.')
    report = new_report()
    manifest_path = root / 'package-manifest.json'
    if not regular_inside(root, manifest_path) or manifest_path.stat().st_size > MAX_TEXT_BYTES:
        issue(report, 'package-manifest.json', 'unsafe_manifest')
        return report
    try:
        data = json.loads(manifest_path.read_bytes().decode('utf-8-sig'), object_pairs_hook=unique_object)
    except RecursionError:
        raise ValueError('Package manifest nesting exceeds parser limits.') from None
    if (not isinstance(data, dict) or set(data) != {'format', 'skill', 'files'}
            or type(data.get('format')) is not int or data['format'] != 1
            or data.get('skill') != root.name or not isinstance(data.get('files'), list)
            or not 1 <= len(data['files']) <= 2048
            or not all(isinstance(name, str) and safe_name(name) for name in data['files'])
            or len(set(data['files'])) != len(data['files'])
            or 'package-manifest.json' not in data['files']):
        issue(report, 'package-manifest.json', 'invalid_manifest')
        return report
    names = set(data['files'])
    for folder, directories, files in os.walk(root, followlinks=False):
        for directory in list(directories):
            path = Path(folder) / directory
            name = path.relative_to(root).as_posix()
            if private_path(name) or path.is_symlink():
                issue(report, name, 'private_path' if private_path(name) else 'unsafe_file')
                directories.remove(directory)
        for filename in files:
            name = (Path(folder) / filename).relative_to(root).as_posix()
            if name not in names:
                issue(report, name, 'unlisted_package_file')
    for name in sorted(names):
        inspect_file(root, report, name)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--index', action='store_true', help='Inspect staged Git blobs, including tracked ignored files.')
    parser.add_argument('--package', action='store_true', help='Inspect an explicitly selected export and its declared manifest.')
    parser.add_argument('--json', action='store_true', help='Machine-readable counts; matched text is never emitted.')
    parser.add_argument('--show-paths', action='store_true', help='Include relative filenames for local diagnosis; do not publish this output.')
    args = parser.parse_args(argv)
    if args.index and args.package:
        parser.error('--index and --package are mutually exclusive.')
    try:
        report = check_package(args.root) if args.package else check_repository(args.root, args.index)
    except (OSError, UnicodeError, ValueError, subprocess.SubprocessError):
        sys.stderr.write('Delivery input could not be checked; inspect the selected path and inventory locally.\n')
        return 2
    counts = dict(sorted(Counter(item['rule'] for item in report['issues']).items()))
    public = {key: value for key, value in report.items() if key != 'issues'}
    public['rule_counts'] = counts
    if args.show_paths:
        public['issues'] = report['issues']
    if args.json:
        print(json.dumps(public, ensure_ascii=True, indent=2))
    else:
        print('Delivery ' + report['status'] + ': ' + str(report['files_checked']) + ' files inspected; ' + str(len(report['issues'])) + ' finding(s).')
        for rule, count in counts.items():
            print(rule + ': ' + str(count))
        if args.show_paths:
            for item in report['issues']:
                print(json.dumps(item, ensure_ascii=True))
    return 1 if report['issues'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
