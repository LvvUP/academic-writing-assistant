"""Installation tests use temporary sources and explicit isolated destinations."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "scripts/install_skill.py"
spec = importlib.util.spec_from_file_location("install_skill", ENTRY)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
PACKAGE_FILES = json.loads((ROOT / "skills" / installer.SKILL_NAME / installer.MANIFEST_NAME).read_text(encoding='utf-8'))["files"]


@pytest.fixture
def source(tmp_path):
    target = tmp_path.resolve() / "source" / installer.SKILL_NAME
    for name in PACKAGE_FILES:
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("SYNTHETIC PACKAGE FILE: " + name + "\n", encoding='utf-8')
    (target / installer.MANIFEST_NAME).write_text(json.dumps({"format": 1, "skill": installer.SKILL_NAME, "files": PACKAGE_FILES}), encoding='utf-8')
    return target


def inventory(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


def destination(tmp_path):
    return tmp_path.resolve() / "isolated home" / ".agents/skills" / installer.SKILL_NAME


def test_install_and_uninstall_preserve_surrounding_files(source, tmp_path):
    target = destination(tmp_path)
    sibling = target.parent / "other-skill.txt"
    sibling.parent.mkdir(parents=True)
    sibling.write_text("SYNTHETIC USER FILE", encoding='utf-8')
    original_home = os.environ.get("HOME")
    result = installer.install(source, target)
    assert result["status"] == "installed"
    assert set(inventory(target)) == set(PACKAGE_FILES) | {installer.RECEIPT_NAME}
    assert (target / "LICENSE").read_bytes() == (source / "LICENSE").read_bytes()
    assert (target / "THIRD_PARTY_NOTICES.md").read_bytes() == (source / "THIRD_PARTY_NOTICES.md").read_bytes()
    installer.uninstall(target)
    assert not target.exists()
    assert sibling.read_text(encoding='utf-8') == "SYNTHETIC USER FILE"
    assert os.environ.get("HOME") == original_home


def test_export_is_only_the_explicit_package_inventory(source, tmp_path):
    (source / "scripts/__pycache__").mkdir(exist_ok=True)
    (source / "scripts/__pycache__/ignored.pyc").write_bytes(b"synthetic cache")
    (source / "private-notes.md").write_text("SYNTHETIC PRIVATE NOTES", encoding='utf-8')
    target = tmp_path.resolve() / "export" / installer.SKILL_NAME
    installer.export(source, target)
    files = inventory(target)
    assert set(files) == set(PACKAGE_FILES)
    assert installer.RECEIPT_NAME not in files
    assert files == {name: (source / name).read_bytes() for name in PACKAGE_FILES}


@pytest.mark.parametrize("existing", ["empty", "file", "unmanaged", "managed"])
def test_install_never_overwrites_existing_destination(source, tmp_path, existing):
    target = destination(tmp_path)
    target.parent.mkdir(parents=True)
    if existing == "file":
        target.write_text("SYNTHETIC USER FILE", encoding='utf-8')
    elif existing == "managed":
        installer.install(source, target)
    else:
        target.mkdir()
        if existing == "unmanaged":
            (target / "SKILL.md").write_text("SYNTHETIC MANUAL INSTALL", encoding='utf-8')
    before = inventory(target) if target.is_dir() else target.read_bytes()
    with pytest.raises(installer.InstallError):
        installer.install(source, target)
    assert (inventory(target) if target.is_dir() else target.read_bytes()) == before


def test_update_replaces_only_unchanged_owned_installation(source, tmp_path):
    target = destination(tmp_path)
    installer.install(source, target)
    (source / "SKILL.md").write_bytes((source / "SKILL.md").read_bytes() + b"\nSynthetic revision.\n")
    installer.update(source, target)
    assert (target / "SKILL.md").read_bytes() == (source / "SKILL.md").read_bytes()
    assert not list(target.parent.glob(".awa-*"))
    installer.uninstall(target)


@pytest.mark.parametrize("action", ["update", "uninstall"])
@pytest.mark.parametrize("change", ["edited", "extra_file", "extra_directory", "missing", "symlink", "bad_receipt"])
def test_mutations_refuse_user_changes(source, tmp_path, action, change):
    target = destination(tmp_path)
    installer.install(source, target)
    if change == "edited":
        (target / "SKILL.md").write_text("SYNTHETIC USER EDIT", encoding='utf-8')
    elif change == "extra_file":
        (target / "my-notes.md").write_text("SYNTHETIC USER NOTES", encoding='utf-8')
    elif change == "extra_directory":
        (target / "user-empty-folder").mkdir()
    elif change == "missing":
        (target / "SKILL.md").unlink()
    elif change == "symlink":
        outside = tmp_path.resolve() / "outside.md"
        outside.write_text("SYNTHETIC OUTSIDE FILE", encoding='utf-8')
        (target / "SKILL.md").unlink()
        (target / "SKILL.md").symlink_to(outside)
    else:
        (target / installer.RECEIPT_NAME).write_text("not JSON", encoding='utf-8')
    before = inventory(target)
    with pytest.raises(installer.InstallError):
        getattr(installer, action)(source, target) if action == "update" else installer.uninstall(target)
    assert inventory(target) == before
    assert target.exists()


@pytest.mark.parametrize("action", ["update", "uninstall"])
def test_unmanaged_installation_is_never_adopted_implicitly(source, tmp_path, action):
    target = destination(tmp_path)
    shutil.copytree(source, target)
    before = inventory(target)
    with pytest.raises(installer.InstallError):
        getattr(installer, action)(source, target) if action == "update" else installer.uninstall(target)
    assert inventory(target) == before


@pytest.mark.parametrize("relative", ["SKILL.md", "scripts/prose_utils.py", "LICENSE", "references"])
def test_source_symlinks_are_rejected(source, tmp_path, relative):
    original = source / relative
    outside = tmp_path.resolve() / "outside-source"
    original.rename(outside)
    original.symlink_to(outside, target_is_directory=outside.is_dir())
    target = destination(tmp_path)
    with pytest.raises(installer.InstallError):
        installer.install(source, target)
    assert not target.exists()


def test_destination_symlink_ancestor_is_rejected(source, tmp_path):
    outside = tmp_path.resolve() / "outside"
    outside.mkdir()
    linked = tmp_path.resolve() / "linked"
    linked.symlink_to(outside, target_is_directory=True)
    with pytest.raises(installer.InstallError):
        installer.install(source, linked / installer.SKILL_NAME)
    assert not list(outside.iterdir())


def test_destination_traversal_and_wrong_leaf_are_rejected(source, tmp_path):
    for target in (tmp_path.resolve() / "part/../academic-writing-assistant", tmp_path.resolve() / "wrong-name"):
        with pytest.raises(installer.InstallError):
            installer.install(source, target)
    assert not (tmp_path / "part").exists()


@pytest.mark.parametrize("field,value", [
    ("tool", "unknown-installer"), ("format", True),
    ("files", {"../outside.txt": {"sha256": "0" * 64, "size": 0}}),
    ("files", {"/outside.txt": {"sha256": "0" * 64, "size": 0}}),
    ("files", {"SKILL.md": {"sha256": "bad", "size": 0}}),
])
def test_receipt_cannot_authorize_unrelated_paths(source, tmp_path, field, value):
    target = destination(tmp_path)
    installer.install(source, target)
    path = target / installer.RECEIPT_NAME
    receipt = json.loads(path.read_text(encoding='utf-8'))
    receipt[field] = value
    path.write_text(json.dumps(receipt), encoding='utf-8')
    before = inventory(target)
    with pytest.raises(installer.InstallError):
        installer.uninstall(target)
    assert inventory(target) == before


def test_failed_update_restores_previous_installation(source, tmp_path, monkeypatch):
    target = destination(tmp_path)
    installer.install(source, target)
    before = inventory(target)
    (source / "SKILL.md").write_text("SYNTHETIC NEW CONTENT", encoding='utf-8')
    publish = installer._publish
    failed = False
    def fail_once(staged, destination):
        nonlocal failed
        if not failed:
            failed = True
            raise OSError("synthetic failure before replacement")
        return publish(staged, destination)
    monkeypatch.setattr(installer, "_publish", fail_once)
    with pytest.raises(installer.InstallError):
        installer.update(source, target)
    assert inventory(target) == before
    assert not list(target.parent.glob(".awa-*"))


@pytest.mark.parametrize("host,relative", [
    ("codex", ".agents/skills"), ("claude", ".claude/skills"),
    ("cursor", ".cursor/skills"), ("grok-build", ".grok/skills"),
])
def test_host_mapping_uses_explicit_home_without_environment_changes(tmp_path, host, relative):
    before = dict(os.environ)
    isolated = tmp_path.resolve() / "隔离 home"
    assert installer.select_destination(None, host, isolated) == isolated / relative / installer.SKILL_NAME
    assert dict(os.environ) == before


def test_cli_from_unrelated_cwd_and_installed_runtime(source, tmp_path):
    cwd = tmp_path.resolve() / "其他 工作目录"
    cwd.mkdir()
    target = destination(tmp_path)
    result = subprocess.run([sys.executable, "-B", str(ENTRY), "install", "--destination", str(target), "--json"], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "installed"
    draft = cwd / "合成 稿件.txt"
    draft.write_text("This study describes a method.", encoding='utf-8')
    result = subprocess.run([sys.executable, "-B", str(target / "scripts/manuscript_audit.py"), str(draft), "--checks", "claims", "--json"], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["claims"] == []
    result = subprocess.run([sys.executable, "-B", str(target / "scripts/terminology_checker.py"), str(draft)], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    assert draft.read_text(encoding='utf-8') == "This study describes a method."


@pytest.mark.parametrize("arguments", [[], ["install"], ["install", "--host", "codex"], ["install", "--destination", ".", "--host", "cursor", "--home-root", "."]])
def test_cli_invalid_selection_is_usage_error(arguments, tmp_path):
    result = subprocess.run([sys.executable, "-B", str(ENTRY), *arguments], cwd=tmp_path, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 2
    assert "Traceback" not in result.stderr


def test_new_public_policy_and_workflow_files_are_in_manifest():
    assert {'references/workflow-context.md', 'references/research-types.md',
            'references/policy-sources.md', 'assets/venue-policies.json',
            installer.MANIFEST_NAME} <= set(PACKAGE_FILES)


def test_ignored_and_private_resources_are_never_read_or_exported(source, tmp_path, monkeypatch):
    extras = ['assets/local-config.json', 'references/private-notes.md', 'scripts/local-debug.py']
    (source / '.gitignore').write_text('\n'.join(extras), encoding='utf-8')
    for name in extras:
        (source / name).write_text('SYNTHETIC PRIVATE MATERIAL', encoding='utf-8')
    original_read = installer.read_regular
    reads = []
    def observed_read(path, *args, **kwargs):
        reads.append(path.relative_to(source).as_posix())
        return original_read(path, *args, **kwargs)
    monkeypatch.setattr(installer, 'read_regular', observed_read)
    target = tmp_path.resolve() / 'export' / installer.SKILL_NAME
    installer.export(source, target)
    assert not set(extras) & set(reads)
    assert not set(extras) & set(inventory(target))
    assert set(inventory(target)) == set(PACKAGE_FILES)


@pytest.mark.parametrize('invalid', ['duplicate', 'case_alias', 'traversal', 'absolute', 'windows_device', 'wrong_type', 'missing_license', 'malformed'])
def test_invalid_package_manifest_refuses_before_writing(source, tmp_path, invalid):
    path = source / installer.MANIFEST_NAME
    data = json.loads(path.read_text(encoding='utf-8'))
    if invalid == 'duplicate':
        data['files'].append('SKILL.md')
    elif invalid == 'case_alias':
        data['files'].extend(['assets/extra.json', 'assets/EXTRA.json'])
    elif invalid == 'traversal':
        data['files'].append('assets/../../outside.json')
    elif invalid == 'absolute':
        data['files'].append('/outside.json')
    elif invalid == 'windows_device':
        data['files'].append('assets/CON.json')
    elif invalid == 'wrong_type':
        data['format'] = True
    elif invalid == 'missing_license':
        data['files'].remove('LICENSE')
    path.write_text('{' if invalid == 'malformed' else json.dumps(data), encoding='utf-8')
    target = destination(tmp_path)
    with pytest.raises(installer.InstallError):
        installer.install(source, target)
    assert not target.exists()
    assert not target.parent.exists()


def test_reformatted_receipt_is_refused_before_any_file_is_removed(source, tmp_path):
    target = destination(tmp_path)
    installer.install(source, target)
    path = target / installer.RECEIPT_NAME
    path.write_text(json.dumps(json.loads(path.read_text(encoding='utf-8'))), encoding='utf-8')
    before = inventory(target)
    with pytest.raises(installer.InstallError):
        installer.uninstall(target)
    assert inventory(target) == before


def test_update_conflict_preserves_previous_and_concurrent_files(source, tmp_path, monkeypatch):
    target = destination(tmp_path)
    installer.install(source, target)
    before = inventory(target)
    def conflicting_publish(staged, destination):
        if not destination.exists():
            destination.mkdir()
            (destination / 'new-user-file.md').write_text('SYNTHETIC CONCURRENT USER FILE', encoding='utf-8')
        raise installer.InstallError('synthetic concurrent destination conflict')
    monkeypatch.setattr(installer, '_publish', conflicting_publish)
    with pytest.raises(installer.InstallError, match='previous installation preserved'):
        installer.update(source, target)
    assert (target / 'new-user-file.md').read_text(encoding='utf-8') == 'SYNTHETIC CONCURRENT USER FILE'
    backups = list(target.parent.glob('.awa-previous-*/academic-writing-assistant'))
    assert len(backups) == 1
    assert inventory(backups[0]) == before


@pytest.mark.parametrize('action', ['install', 'update'])
def test_enospc_during_staging_preserves_old_and_unrelated_files(source, tmp_path, monkeypatch, action):
    import errno
    target = destination(tmp_path)
    target.parent.mkdir(parents=True)
    if action == 'update':
        installer.install(source, target)
    before = inventory(target) if target.exists() else None
    existing = target.parent / '.awa-stage-user-owned'
    existing.mkdir()
    (existing / 'note.md').write_text('SYNTHETIC USER FILE', encoding='utf-8')
    original_write = installer._write_file
    count = 0
    def disk_full_after_one_file(path, data):
        nonlocal count
        count += 1
        if count == 2:
            raise OSError(errno.ENOSPC, 'synthetic disk full during staging')
        original_write(path, data)
    monkeypatch.setattr(installer, '_write_file', disk_full_after_one_file)
    with pytest.raises(OSError) as error:
        getattr(installer, action)(source, target)
    assert error.value.errno == errno.ENOSPC
    assert (inventory(target) if target.exists() else None) == before
    assert (existing / 'note.md').read_text(encoding='utf-8') == 'SYNTHETIC USER FILE'
    assert list(target.parent.glob('.awa-*')) == [existing]


@pytest.mark.parametrize('conflict', [False, True])
def test_windows_publish_releases_only_own_empty_reservation(tmp_path, monkeypatch, conflict):
    # This is a branch/rename-contract simulation on the local OS, not a Windows
    # host test. Native Windows execution remains separately reported.
    parent = tmp_path.resolve()
    staged = parent / 'staged'
    staged.mkdir()
    (staged / 'payload.txt').write_text('SYNTHETIC PACKAGE', encoding='utf-8')
    target = parent / installer.SKILL_NAME
    original_rename = Path.rename
    def windows_rename(path, destination):
        assert not destination.exists(), 'reservation must be removed on Windows'
        if conflict:
            destination.mkdir()
            (destination / 'user.txt').write_text('SYNTHETIC CONCURRENT FILE', encoding='utf-8')
            raise FileExistsError('synthetic Windows destination conflict')
        return original_rename(path, destination)
    monkeypatch.setattr(installer, 'IS_WINDOWS', True)
    monkeypatch.setattr(Path, 'rename', windows_rename)
    if conflict:
        with pytest.raises(FileExistsError):
            installer._publish(staged, target)
        assert (target / 'user.txt').read_text(encoding='utf-8') == 'SYNTHETIC CONCURRENT FILE'
        assert (staged / 'payload.txt').read_text(encoding='utf-8') == 'SYNTHETIC PACKAGE'
    else:
        installer._publish(staged, target)
        assert (target / 'payload.txt').read_text(encoding='utf-8') == 'SYNTHETIC PACKAGE'
        assert not staged.exists()


def test_normal_python_cache_blocks_both_mutations_and_can_be_preserved(tmp_path):
    source = ROOT / 'skills' / installer.SKILL_NAME
    target = destination(tmp_path)
    installer.install(source, target)
    script = target / 'scripts/manuscript_audit.py'
    result = subprocess.run([sys.executable, str(script), '--checks', 'claims', '--json'],
                            input='This study describes a method.', text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    caches = list(target.rglob('__pycache__'))
    assert caches and any(p.suffix == '.pyc' for p in caches[0].iterdir())
    before = inventory(target)
    for action in ('update', 'uninstall'):
        with pytest.raises(installer.InstallError):
            getattr(installer, action)(source, target) if action == 'update' else installer.uninstall(target)
        assert inventory(target) == before
    saved = tmp_path.resolve() / 'user-kept-cache'
    saved.mkdir()
    for index, cache in enumerate(caches):
        cache.rename(saved / str(index))
    saved_before = inventory(saved)
    installer.update(source, target)
    installer.uninstall(target)
    assert inventory(saved) == saved_before
    assert not target.exists()


def test_real_cli_isolated_lifecycle_and_standalone_lint(tmp_path):
    cwd = tmp_path.resolve() / 'separate work'
    cwd.mkdir()
    isolated = tmp_path.resolve() / 'explicit isolated home'
    original_home = os.environ.get('HOME')
    original_codex_home = os.environ.get('CODEX_HOME')
    args = ['--host', 'codex', '--home-root', str(isolated), '--json']
    for action in ('install', 'update'):
        result = subprocess.run([sys.executable, '-B', str(ENTRY), action, *args], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout)['status'] == {'install': 'installed', 'update': 'updated'}[action]
    exported = tmp_path.resolve() / 'exported' / installer.SKILL_NAME
    result = subprocess.run([sys.executable, '-B', str(ENTRY), 'export', '--destination', str(exported), '--json'], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    assert set(inventory(exported)) == set(PACKAGE_FILES)
    result = subprocess.run([sys.executable, '-B', str(exported / 'scripts/skill_lint.py'), '--package', str(exported)], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    result = subprocess.run([sys.executable, '-B', str(ENTRY), 'uninstall', *args], cwd=cwd, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    assert not (isolated / '.agents/skills' / installer.SKILL_NAME).exists()
    assert os.environ.get('HOME') == original_home
    assert os.environ.get('CODEX_HOME') == original_codex_home


def test_parent_directory_case_alias_is_refused_before_publish(source, tmp_path):
    # Distinct filenames inside aliased directories are legal on both sensitive
    # and insensitive filesystems; the manifest must remain portable on both.
    extra = ['references/Case/a.md', 'references/case/b.md']
    path = source / installer.MANIFEST_NAME
    manifest = json.loads(path.read_text(encoding='utf-8'))
    manifest['files'].extend(extra)
    path.write_text(json.dumps(manifest), encoding='utf-8')
    for name in extra:
        (source / name).parent.mkdir(parents=True, exist_ok=True)
        (source / name).write_text('SYNTHETIC CASE ALIAS', encoding='utf-8')
    target = destination(tmp_path)
    with pytest.raises(installer.InstallError, match='[Cc]ase|[Ii]nventory'):
        installer.install(source, target)
    assert not target.exists()


def test_deep_source_manifest_refuses_before_install(source, tmp_path):
    path = source / installer.MANIFEST_NAME
    path.write_text('[' * 1100 + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * 1100, encoding='utf-8')
    target = destination(tmp_path)
    before = inventory(source)
    with pytest.raises(installer.InstallError) as error:
        installer.install(source, target)
    assert 'SYNTHETIC_PRIVATE_MARKER' not in str(error.value)
    assert not target.exists()
    assert inventory(source) == before


@pytest.mark.parametrize('action', ['update', 'uninstall'])
@pytest.mark.parametrize('depth', [1100, 10000])
def test_deep_receipt_cli_refuses_and_preserves_installation(source, tmp_path, action, depth):
    target = destination(tmp_path)
    installer.install(source, target)
    (target / installer.RECEIPT_NAME).write_text('[' * depth + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * depth, encoding='utf-8')
    before = inventory(target)
    result = subprocess.run([sys.executable, '-B', str(ENTRY), action,
                             '--destination', str(target), '--json'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1
    assert 'Traceback' not in result.stderr
    assert json.loads(result.stderr)['status'] == 'refused'
    assert 'SYNTHETIC_PRIVATE_MARKER' not in result.stderr + result.stdout
    assert inventory(target) == before


@pytest.mark.parametrize('action', ['install', 'export'])
def test_deep_source_manifest_cli_is_controlled_and_creates_nothing(source, tmp_path, action):
    tool = tmp_path.resolve() / 'tool'
    (tool / 'scripts').mkdir(parents=True)
    entry = tool / 'scripts/install_skill.py'
    shutil.copyfile(ENTRY, entry)
    copied = tool / 'skills' / installer.SKILL_NAME
    shutil.copytree(source, copied)
    (copied / installer.MANIFEST_NAME).write_text('[' * 10000 + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * 10000, encoding='utf-8')
    before = inventory(copied)
    target = destination(tmp_path)
    result = subprocess.run([sys.executable, '-B', str(entry), action,
                             '--destination', str(target), '--json'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1
    assert 'Traceback' not in result.stderr
    assert json.loads(result.stderr)['status'] == 'refused'
    assert 'SYNTHETIC_PRIVATE_MARKER' not in result.stderr + result.stdout
    assert not target.exists()
    assert inventory(copied) == before


@pytest.fixture
def windows_direntry_stat(monkeypatch):
    """Simulate documented Windows DirEntry metadata, not Windows execution."""
    from contextlib import contextmanager
    from types import SimpleNamespace
    real_scandir = os.scandir
    class Entry:
        def __init__(self, entry):
            self.path = entry.path
            self.original = entry
        def stat(self, *, follow_symlinks=True):
            info = self.original.stat(follow_symlinks=follow_symlinks)
            return SimpleNamespace(st_mode=info.st_mode, st_size=info.st_size,
                                   st_ino=0, st_dev=0, st_nlink=0)
    @contextmanager
    def zero_stat_scandir(path):
        with real_scandir(path) as entries:
            yield (Entry(entry) for entry in entries)
    # Keep shutil/pathlib and the test runtime on their real OS implementation.
    # Only the installer sees the simulated DirEntry cache.
    class InstallerOS:
        scandir = staticmethod(zero_stat_scandir)
        def __getattr__(self, name):
            return getattr(os, name)
    monkeypatch.setattr(installer, 'os', InstallerOS())


def test_windows_direntry_zero_fields_do_not_reject_own_installation(source, tmp_path, windows_direntry_stat):
    target = destination(tmp_path)
    installer.install(source, target)
    assert installer.verify_installation(target)['skill'] == installer.SKILL_NAME
    revision = b'SYNTHETIC UPDATED PACKAGE\n'
    (source / 'SKILL.md').write_bytes(revision)
    installer.update(source, target)
    assert (target / 'SKILL.md').read_bytes() == revision
    installer.uninstall(target)
    assert not target.exists()
    assert (source / 'SKILL.md').read_bytes() == revision


@pytest.mark.parametrize('action', ['update', 'uninstall'])
def test_windows_direntry_zero_fields_still_reject_actual_hardlinks(source, tmp_path, windows_direntry_stat, action):
    target = destination(tmp_path)
    installer.install(source, target)
    relative = 'references/fidelity-protocol.md'
    alias = target / relative
    private = tmp_path.resolve() / 'synthetic-private.md'
    private.write_bytes(alias.read_bytes())
    alias.unlink()
    os.link(private, alias)
    assert alias.lstat().st_nlink > 1
    before = inventory(target)
    with pytest.raises(installer.InstallError) as error:
        installer.update(source, target) if action == 'update' else installer.uninstall(target)
    assert relative in str(error.value), 'Reject the actual hard link, not an unrelated regular receipt.'
    assert inventory(target) == before
    assert private.read_bytes() == alias.read_bytes()


@pytest.mark.parametrize('json_output', [False, True])
@pytest.mark.parametrize('existing', [False, True])
def test_cli_output_is_utf8_under_cp1252_redirection(source, tmp_path, json_output, existing):
    tool = tmp_path.resolve() / 'tool'
    (tool / 'scripts').mkdir(parents=True)
    entry = tool / 'scripts/install_skill.py'
    shutil.copyfile(ENTRY, entry)
    shutil.copytree(source, tool / 'skills' / installer.SKILL_NAME)
    target = tmp_path.resolve() / '中文 安装目录' / installer.SKILL_NAME
    if existing:
        target.mkdir(parents=True)
        (target / '用户笔记.txt').write_text('合成用户内容', encoding='utf-8')
    before = inventory(target) if existing else None
    wrapper = ("import runpy,sys; "
               "sys.stdout.reconfigure(encoding='cp1252',errors='strict'); "
               "sys.stderr.reconfigure(encoding='cp1252',errors='strict'); "
               "sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')")
    action = 'uninstall' if existing else 'install'
    args = [sys.executable, '-B', '-c', wrapper, str(entry), action, '--destination', str(target)]
    if json_output:
        args.append('--json')
    # Capture bytes to verify the actual output codec, independent of the caller's locale.
    result = subprocess.run(args, capture_output=True)
    stdout, stderr = result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    assert result.returncode == (1 if existing else 0), stderr
    assert 'Traceback' not in stderr
    output = stderr if existing else stdout
    assert '中文 安装目录' in output
    if json_output:
        assert json.loads(output)['status'] == ('refused' if existing else 'installed')
    if existing:
        assert inventory(target) == before
    else:
        installer.uninstall(target)


def test_cli_usage_error_is_utf8_under_cp1252_redirection(tmp_path):
    wrapper = ("import runpy,sys; "
               "sys.stdout.reconfigure(encoding='cp1252',errors='strict'); "
               "sys.stderr.reconfigure(encoding='cp1252',errors='strict'); "
               "sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')")
    result = subprocess.run([sys.executable, '-B', '-c', wrapper, str(ENTRY), '无效操作'],
                            cwd=tmp_path, capture_output=True)
    stderr = result.stderr.decode('utf-8')
    assert result.returncode == 2
    assert '无效操作' in stderr and 'Traceback' not in stderr
    assert not list(tmp_path.iterdir())
