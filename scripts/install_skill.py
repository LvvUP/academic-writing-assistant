#!/usr/bin/env python3
"""Install, update, uninstall or export one local Skill; Python 3.9+, no network.

Only explicit package files are copied. Updates/removal require an unchanged
installation receipt. The receipt records local ownership, not authenticity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile

SKILL_NAME = 'academic-writing-assistant'
TOOL_ID = 'academic-writing-assistant/install_skill'
RECEIPT_NAME = '.academic-writing-assistant-install.json'
HOST_PATHS = {'codex': '.agents/skills', 'claude': '.claude/skills',
              'cursor': '.cursor/skills', 'grok-build': '.grok/skills'}
MANIFEST_NAME = 'package-manifest.json'
IS_WINDOWS = os.name == 'nt'
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_PACKAGE_BYTES = 64 * 1024 * 1024


class InstallError(Exception):
    """An operation was refused or could not safely complete."""


def safe_path(value):
    """Keep lexical traversal visible, and reject existing symlink ancestors."""
    original = Path(value).expanduser()
    if '..' in original.parts:
        raise InstallError('Paths containing .. are refused; provide a direct path.')
    path = Path(os.path.abspath(str(original)))
    for part in [*reversed(path.parents), path]:
        try:
            mode = part.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise InstallError('Symlink path refused: ' + str(part))
        if part != path and not stat.S_ISDIR(mode):
            raise InstallError('A path ancestor is not a directory: ' + str(part))
    return path


def selected_target(value):
    target = safe_path(value)
    if target.name != SKILL_NAME:
        raise InstallError('The destination directory must be named ' + SKILL_NAME + '.')
    return target


def select_destination(destination=None, host=None, home_root=None):
    if destination is not None and (host is not None or home_root is not None):
        raise InstallError('Choose --destination or --host with --home-root, not both.')
    if destination is not None:
        return selected_target(destination)
    if host not in HOST_PATHS or home_root is None:
        raise InstallError('Supply --destination, or both --host and --home-root.')
    return selected_target(safe_path(home_root) / HOST_PATHS[host] / SKILL_NAME)


def read_regular(path, limit=MAX_FILE_BYTES):
    safe_path(path)
    try:
        info = path.lstat()
    except FileNotFoundError:
        raise InstallError('Required file is missing: ' + str(path)) from None
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise InstallError('Only regular files without hard links are accepted: ' + str(path))
    if info.st_size > limit:
        raise InstallError('File exceeds the local size limit: ' + str(path))
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    with os.fdopen(os.open(path, flags), 'rb') as handle:
        opened = os.fstat(handle.fileno())
        if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
            raise InstallError('File changed while being opened: ' + str(path))
        data = handle.read(limit + 1)
    if len(data) > limit or len(data) != info.st_size:
        raise InstallError('File changed size while being read: ' + str(path))
    return data


def package_name(name):
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*(?:/[A-Za-z0-9][A-Za-z0-9_.-]*)*', name):
        return False
    path = PurePosixPath(name)
    reserved = {'con', 'prn', 'aux', 'nul', *('com' + str(i) for i in range(1, 10)),
                *('lpt' + str(i) for i in range(1, 10))}
    if any(part in {'.', '..', '__pycache__', 'private'} or part.endswith('.')
           or part.split('.')[0].lower() in reserved for part in path.parts):
        return False
    if name in {'SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', MANIFEST_NAME, 'agents/openai.yaml'}:
        return True
    return len(path.parts) >= 2 and {
        'references': '.md', 'scripts': '.py', 'assets': '.json',
    }.get(path.parts[0]) == path.suffix


def parse_package_manifest(raw):
    try:
        manifest = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_mapping)
    except (UnicodeError, ValueError, RecursionError):
        raise InstallError('Cannot parse the public package manifest.') from None
    if (not isinstance(manifest, dict) or set(manifest) != {'format', 'skill', 'files'}
            or type(manifest['format']) is not int or manifest['format'] != 1
            or manifest['skill'] != SKILL_NAME):
        raise InstallError('Unrecognized public package manifest.')
    names = manifest['files']
    if (not isinstance(names, list) or not 1 <= len(names) <= 2048
            or not all(package_name(name) for name in names)
            or len({name.casefold() for name in names}) != len(names)
            or not {'SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', MANIFEST_NAME} <= set(names)):
        raise InstallError('Invalid public package file inventory.')
    spellings = {}
    for name in names:
        path = PurePosixPath(name)
        for prefix in [path, *path.parents]:
            spelling = prefix.as_posix()
            key = spelling.casefold()
            if key in spellings and spellings[key] != spelling:
                raise InstallError('Case aliases in the package path inventory are refused.')
            spellings[key] = spelling
        if any(parent.as_posix() in names for parent in path.parents):
            raise InstallError('Package inventory uses one path as both file and directory.')
    return tuple(names)


def package_payload(source):
    source = safe_path(source)
    if not source.is_dir():
        raise InstallError('Source package is missing or is not a directory.')
    raw = read_regular(source / MANIFEST_NAME, 128 * 1024)
    names = parse_package_manifest(raw)
    # No directory exploration: only individually approved manifest paths are
    # read. Ignored/private notes and configuration cannot join via a suffix.
    payload = {}
    total = 0
    for name in names:
        payload[name] = raw if name == MANIFEST_NAME else read_regular(source / name)
        total += len(payload[name])
        if total > MAX_PACKAGE_BYTES:
            raise InstallError('Package exceeds the 64 MiB local size limit.')
    return payload


def fingerprint(data):
    return {'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)}


def receipt_for(payload):
    return {'format': 1, 'tool': TOOL_ID, 'skill': SKILL_NAME,
            'files': {name: fingerprint(data) for name, data in sorted(payload.items())}}


def encoded_receipt(receipt):
    return (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def expected_directories(names):
    return {str(parent) for name in names for parent in PurePosixPath(name).parents
            if str(parent) != '.'}


def inventory(root, max_entries):
    files, directories = set(), set()
    pending = [root]
    while pending:
        directory = pending.pop()
        safe_path(directory)
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                relative = path.relative_to(root).as_posix()
                if len(files) + len(directories) >= max_entries:
                    raise InstallError('Installation has additional files/directories; refusing removal.')
                # Windows DirEntry.stat caches zero link/inode/device fields.
                # Fetch full, non-following metadata before enforcing nlink == 1.
                info = path.lstat()
                if stat.S_ISLNK(info.st_mode):
                    raise InstallError('Installation contains a symlink: ' + relative)
                if stat.S_ISDIR(info.st_mode):
                    directories.add(relative)
                    pending.append(path)
                elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                    files.add(relative)
                else:
                    raise InstallError('Installation contains a nonregular or hard-linked file: ' + relative)
    return files, directories


def unique_mapping(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate receipt field.')
        result[key] = value
    return result


def verify_installation(target):
    target = safe_path(target)
    if not target.is_dir():
        raise InstallError('No managed installation directory exists at this destination.')
    raw = read_regular(target / RECEIPT_NAME, 128 * 1024)
    try:
        receipt = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_mapping)
    except (ValueError, UnicodeError, RecursionError):
        raise InstallError('Installation receipt is invalid; preserve this directory and inspect it manually.') from None
    if (not isinstance(receipt, dict) or set(receipt) != {'format', 'tool', 'skill', 'files'}
            or type(receipt['format']) is not int or receipt['format'] != 1
            or receipt['tool'] != TOOL_ID or receipt['skill'] != SKILL_NAME):
        raise InstallError('This directory has no recognized installation receipt.')
    records = receipt['files']
    if not isinstance(records, dict) or not {'SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', MANIFEST_NAME} <= set(records):
        raise InstallError('The installation receipt has an invalid file inventory.')
    for name, record in records.items():
        # Restrict even a receipt-provided path to the same public resource
        # rules as packaging. No absolute, traversal or hidden paths.
        if not package_name(name) or not isinstance(record, dict) or set(record) != {'sha256', 'size'}:
            raise InstallError('The installation receipt contains an unsupported file record.')
        if (not isinstance(record['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', record['sha256'])
                or type(record['size']) is not int or not 0 <= record['size'] <= MAX_FILE_BYTES):
            raise InstallError('The installation receipt contains an invalid fingerprint.')
    if raw != encoded_receipt(receipt):
        raise InstallError('Installation receipt was changed; refusing replacement or removal.')
    names = parse_package_manifest(read_regular(target / MANIFEST_NAME, 128 * 1024))
    if set(names) != set(records):
        raise InstallError('Installation receipt does not match its public package manifest.')
    actual_files, actual_directories = inventory(target, len(records) + len(expected_directories(records)) + 1)
    if actual_files != set(records) | {RECEIPT_NAME} or actual_directories != expected_directories(records):
        raise InstallError('Installation has missing or additional files/directories; preserve your changes before updating or uninstalling.')
    for name, record in records.items():
        if fingerprint(read_regular(target / name)) != record:
            raise InstallError('Installed file was modified; refusing to remove or replace it: ' + name)
    return receipt


def make_parents(parent):
    safe_path(parent)
    parent.mkdir(parents=True, exist_ok=True)
    safe_path(parent)


def _write_file(path, content):
    with path.open('xb') as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())


def stage_payload(parent, payload, managed):
    container = Path(tempfile.mkdtemp(prefix='.awa-stage-', dir=parent))
    staged = container / SKILL_NAME
    try:
        staged.mkdir()
        data = dict(payload)
        if managed:
            data[RECEIPT_NAME] = encoded_receipt(receipt_for(payload))
        for name, content in data.items():
            path = staged / name
            path.parent.mkdir(parents=True, exist_ok=True)
            _write_file(path, content)
        return container, staged
    except BaseException:
        # This is a newly created, private staging directory, never an existing
        # installation or user-provided directory.
        shutil.rmtree(container)
        raise


def _publish(staged, target):
    """Reserve an absent name exclusively, then replace our own empty directory.

    Plain rename could overwrite an existing empty user directory. mkdir is the
    exclusive reservation; a conflicting name is never removed to make room.
    """
    safe_path(target)
    try:
        target.mkdir()
    except FileExistsError:
        raise InstallError('Destination already exists; no files were overwritten.') from None
    reserved = target.stat()
    owns_reservation = True
    try:
        safe_path(target)
        current = target.stat()
        if (reserved.st_dev, reserved.st_ino) != (current.st_dev, current.st_ino) or any(target.iterdir()):
            raise InstallError('Destination changed during installation; refusing replacement.')
        if IS_WINDOWS:
            # Windows rename refuses any existing destination. Release only our
            # verified empty reservation; a concurrent replacement then causes
            # rename to fail, rather than being overwritten.
            target.rmdir()
            owns_reservation = False
        staged.rename(target)
    except BaseException:
        # Remove only our still-empty reserved directory. A concurrent file or
        # replacement directory is preserved.
        try:
            current = target.lstat()
            if owns_reservation and (reserved.st_dev, reserved.st_ino) == (current.st_dev, current.st_ino):
                target.rmdir()
        except OSError:
            pass
        raise


def compatible_paths(source, target):
    source = safe_path(source)
    if source == target or source in target.parents or target in source.parents:
        raise InstallError('Source and destination must be separate directory trees.')


def clean_container(container):
    # Staging contents are generated exclusively by this operation.
    if container.exists():
        shutil.rmtree(container)


def create(source, destination, managed):
    target = selected_target(destination)
    compatible_paths(source, target)
    if target.exists():
        raise InstallError('Destination already exists; choose a new directory or use update for a managed installation.')
    payload = package_payload(source)
    make_parents(target.parent)
    container, staged = stage_payload(target.parent, payload, managed)
    try:
        _publish(staged, target)
    finally:
        clean_container(container)
    return {'status': 'installed' if managed else 'exported', 'destination': str(target), 'files': len(payload)}


def install(source, destination):
    return create(source, destination, True)


def export(source, destination):
    return create(source, destination, False)


def remove_verified(target, expected):
    if verify_installation(target) != expected:
        raise InstallError('Installation changed; preserved at ' + str(target))
    # Delete only recorded, unchanged regular files; rmdir refuses any extra
    # files that appear after verification. Never rmtree an installed directory.
    for name, record in expected['files'].items():
        path = target / name
        if fingerprint(read_regular(path)) != record:
            raise InstallError('File changed during removal; remaining files preserved at ' + str(target))
        path.unlink()
    for name in sorted(expected_directories(expected['files']), key=lambda value: len(PurePosixPath(value).parts), reverse=True):
        (target / name).rmdir()
    if read_regular(target / RECEIPT_NAME) != encoded_receipt(expected):
        raise InstallError('Receipt changed during removal; remaining files preserved at ' + str(target))
    (target / RECEIPT_NAME).unlink()
    target.rmdir()


def park_existing(target, expected):
    if verify_installation(target) != expected:
        raise InstallError('Installation changed before replacement; no files were removed.')
    container = Path(tempfile.mkdtemp(prefix='.awa-previous-', dir=target.parent))
    previous = container / SKILL_NAME
    try:
        target.rename(previous)
    except BaseException:
        container.rmdir()
        raise
    return container, previous


def update(source, destination):
    target = selected_target(destination)
    compatible_paths(source, target)
    original = verify_installation(target)
    payload = package_payload(source)
    container, staged = stage_payload(target.parent, payload, True)
    backup_container = previous = None
    try:
        backup_container, previous = park_existing(target, original)
        try:
            _publish(staged, target)
        except (OSError, InstallError) as exc:
            try:
                _publish(previous, target)
            except (OSError, InstallError):
                raise InstallError('Update stopped; previous installation preserved at ' + str(previous)) from exc
            raise InstallError('Update failed; the previous installation was restored.') from exc
        try:
            remove_verified(previous, original)
        except (OSError, InstallError) as exc:
            raise InstallError('New version installed; previous files need inspection at ' + str(previous)) from exc
    finally:
        clean_container(container)
        if backup_container is not None and backup_container.exists() and not any(backup_container.iterdir()):
            backup_container.rmdir()
    return {'status': 'updated', 'destination': str(target), 'files': len(payload)}


def uninstall(destination):
    target = selected_target(destination)
    original = verify_installation(target)
    container, previous = park_existing(target, original)
    try:
        remove_verified(previous, original)
    except (OSError, InstallError) as exc:
        raise InstallError('Removal stopped; remaining files preserved at ' + str(previous)) from exc
    finally:
        if container.exists() and not any(container.iterdir()):
            container.rmdir()
    return {'status': 'uninstalled', 'destination': str(target), 'files': len(original['files'])}


def configure_utf8_output():
    """Keep redirected CLI output UTF-8 regardless of the process locale."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, 'reconfigure', None)
        if callable(reconfigure):
            reconfigure(encoding='utf-8', errors='backslashreplace')


def main(argv=None):
    configure_utf8_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('install', 'update', 'uninstall', 'export'))
    parser.add_argument('--destination', type=Path, help='Exact Skill directory, relative to your current working directory if not absolute.')
    parser.add_argument('--host', choices=tuple(HOST_PATHS))
    parser.add_argument('--home-root', type=Path, help='Explicit home directory used with --host; no environment variables are changed.')
    parser.add_argument('--json', action='store_true', help='Print a structured result.')
    args = parser.parse_args(argv)
    if (args.destination is not None and (args.host is not None or args.home_root is not None)
            or args.destination is None and (args.host is None or args.home_root is None)):
        parser.error('choose --destination or both --host and --home-root')
    if args.action == 'export' and args.destination is None:
        parser.error('export requires an explicit --destination')
    try:
        target = select_destination(args.destination, args.host, args.home_root)
        source = Path(__file__).resolve().parents[1] / 'skills' / SKILL_NAME
        if args.action == 'uninstall':
            result = uninstall(target)
        else:
            result = {'install': install, 'update': update, 'export': export}[args.action](source, target)
    except (InstallError, OSError) as exc:
        message = str(exc).splitlines()[0]
        if args.json:
            print(json.dumps({'status': 'refused', 'error': message}, ensure_ascii=False), file=sys.stderr)
        else:
            print('install_skill: ' + message, file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False) if args.json else
          result['status'] + ': ' + result['destination'] + ' (' + str(result['files']) + ' package files)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
