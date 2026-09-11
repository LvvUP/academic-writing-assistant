"""Synthetic metadata and native Windows junction boundary regressions."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/academic-writing-assistant'
sys.path.insert(0, str(SKILL / 'scripts'))
import skill_lint as lint


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_module('reparse_installer', ROOT / 'scripts/install_skill.py')
guard = load_module('reparse_delivery', ROOT / 'scripts/check_delivery.py')


@pytest.fixture
def source(tmp_path):
    target = tmp_path.resolve() / 'source' / installer.SKILL_NAME
    names = json.loads((SKILL / 'package-manifest.json').read_text(encoding='utf-8'))['files']
    for name in names:
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SKILL / name, path)
    return target


def reparse_info(info, directory=False):
    fields = {name: getattr(info, name) for name in dir(info) if name.startswith('st_')}
    fields['st_file_attributes'] = fields.get('st_file_attributes', 0) | 0x400
    fields['st_reparse_tag'] = 0xA0000003
    if directory:
        fields['st_mode'] = stat.S_IFDIR | 0o755
    return SimpleNamespace(**fields)


def forbid_open(monkeypatch, forbidden):
    """Observe the actual file-open boundary, including paths through aliases."""
    original = os.open
    def checked(path, *args, **kwargs):
        if isinstance(path, (str, bytes, os.PathLike)):
            resolved = Path(os.fsdecode(path)).resolve()
            assert resolved != forbidden and forbidden not in resolved.parents, 'Outside content was opened.'
        return original(path, *args, **kwargs)
    monkeypatch.setattr(os, 'open', checked)


@pytest.mark.parametrize('relative', ['.', '..', 'references', 'SKILL.md', 'package-manifest.json'])
@pytest.mark.parametrize('action', ['install', 'export'])
def test_reparse_source_metadata_is_rejected_before_open(source, tmp_path, monkeypatch, relative, action):
    marked = source.parent if relative == '..' else source / relative
    marked = marked.absolute()
    original = Path.lstat
    def metadata(path, *args, **kwargs):
        info = original(path, *args, **kwargs)
        return reparse_info(info) if path == marked else info
    forbidden = marked.resolve()
    forbid_open(monkeypatch, forbidden)
    monkeypatch.setattr(Path, 'lstat', metadata)
    target = tmp_path.resolve() / 'output' / installer.SKILL_NAME
    with pytest.raises(installer.InstallError):
        getattr(installer, action)(source, target)
    assert not target.exists()


@pytest.mark.parametrize('reader', ['installer', 'delivery', 'lint'])
def test_opened_reparse_handle_is_rejected(tmp_path, monkeypatch, reader):
    root = tmp_path.resolve()
    path = root / 'synthetic.md'
    path.write_text('Synthetic material.', encoding='utf-8')
    original = os.fstat
    monkeypatch.setattr(os, 'fstat', lambda descriptor: reparse_info(original(descriptor)))
    with pytest.raises(installer.InstallError if reader == 'installer' else ValueError):
        if reader == 'installer':
            installer.read_regular(path)
        elif reader == 'delivery':
            guard.read_regular(root, path)
        else:
            lint.read_public_text(path, root)


@pytest.fixture(params=['simulated_metadata', 'native_windows'])
def junction(request, monkeypatch):
    """The native case must create a real junction on Windows; never emulate it."""
    native = request.param == 'native_windows'
    if native and os.name != 'nt':
        pytest.skip('Native Windows junction integration requires Windows.')
    aliases = []
    original = Path.lstat
    if not native:
        def metadata(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            return reparse_info(info, directory=True) if path in aliases else info
        monkeypatch.setattr(Path, 'lstat', metadata)

    def create(alias, target):
        if os.name == 'nt':
            result = subprocess.run(['cmd', '/d', '/c', 'mklink', '/J', str(alias), str(target)],
                                    capture_output=True)
            assert result.returncode == 0, 'Windows could not create the required junction fixture.'
            info = original(alias)
            assert info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
            assert info.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
            assert not stat.S_ISLNK(info.st_mode)
        else:
            alias.symlink_to(target, target_is_directory=True)
        aliases.append(alias)
        return alias

    yield create
    for alias in reversed(aliases):
        if os.path.lexists(alias):
            os.rmdir(alias) if os.name == 'nt' else os.unlink(alias)


def snapshot(directory):
    return {str(path.relative_to(directory)): path.read_bytes()
            for path in directory.rglob('*') if path.is_file()}


@pytest.mark.parametrize('location', ['root', 'references'])
def test_junction_source_does_not_export_outside_content(source, tmp_path, junction, monkeypatch, location):
    external = tmp_path.resolve() / 'outside-source'
    alias = source if location == 'root' else source / 'references'
    alias.rename(external)
    junction(alias, external)
    before = snapshot(external)
    forbid_open(monkeypatch, external)
    target = tmp_path.resolve() / 'export' / installer.SKILL_NAME
    with pytest.raises(installer.InstallError):
        installer.export(source, target)
    assert not target.exists()
    assert snapshot(external) == before


def test_junction_destination_does_not_write_outside(source, tmp_path, junction, monkeypatch):
    external = tmp_path.resolve() / 'outside-destination'
    external.mkdir()
    (external / 'sentinel.txt').write_text('Synthetic user-owned file.', encoding='utf-8')
    alias = junction(tmp_path.resolve() / 'selected-parent', external)
    before = snapshot(external)
    forbid_open(monkeypatch, external)
    with pytest.raises(installer.InstallError):
        installer.install(source, alias / installer.SKILL_NAME)
    assert snapshot(external) == before
    assert not (external / installer.SKILL_NAME).exists()


@pytest.mark.parametrize('action', ['update', 'uninstall'])
def test_junction_installation_preserves_external_files(source, tmp_path, junction, monkeypatch, action):
    target = tmp_path.resolve() / 'installation' / installer.SKILL_NAME
    installer.install(source, target)
    external = tmp_path.resolve() / 'outside-installation'
    (target / 'references').rename(external)
    junction(target / 'references', external)
    before = snapshot(external)
    forbid_open(monkeypatch, external)
    with pytest.raises(installer.InstallError):
        installer.update(source, target) if action == 'update' else installer.uninstall(target)
    assert snapshot(external) == before
    assert target.is_dir()
    assert not list(target.parent.glob('.awa-previous-*'))


@pytest.mark.parametrize('location', ['root', 'ancestor', 'references'])
def test_junction_roots_and_resources_are_not_read_by_validators(source, tmp_path, junction, monkeypatch, location):
    external = tmp_path.resolve() / 'outside-validator'
    alias = source if location == 'root' else source.parent if location == 'ancestor' else source / 'references'
    alias.rename(external)
    junction(alias, external)
    before = snapshot(external)
    forbid_open(monkeypatch, external)
    if location == 'references':
        assert guard.check_package(source)['status'] == 'FAIL'
    else:
        with pytest.raises(ValueError):
            guard.check_package(source)
        with pytest.raises(ValueError):
            guard.check_repository(source)
    assert lint.check(source, package=True)
    assert snapshot(external) == before


def test_directory_junctions_are_pruned_before_inventory_walk(source, tmp_path, junction, monkeypatch):
    external = tmp_path.resolve() / 'outside-walk'
    external.mkdir()
    (external / 'sentinel.md').write_text('Synthetic external material.', encoding='utf-8')
    junction(source / 'references/alias', external)
    original = os.scandir
    def checked(path):
        if not isinstance(path, int):
            resolved = Path(path).resolve()
            assert resolved != external and external not in resolved.parents, 'Outside directory was enumerated.'
        return original(path)
    monkeypatch.setattr(os, 'scandir', checked)
    assert guard.check_package(source)['status'] == 'FAIL'
    assert all('alias' not in path.relative_to(source).parts for path in lint.public_files(source))


@pytest.mark.parametrize('checker', ['delivery', 'lint'])
def test_file_reparse_metadata_is_rejected_by_validators(source, monkeypatch, checker):
    target = source / 'SKILL.md'
    forbidden = target.resolve()
    original = Path.lstat
    def metadata(path, *args, **kwargs):
        info = original(path, *args, **kwargs)
        return reparse_info(info) if path == target else info
    forbid_open(monkeypatch, forbidden)
    monkeypatch.setattr(Path, 'lstat', metadata)
    if checker == 'delivery':
        assert guard.check_package(source)['status'] == 'FAIL'
    else:
        assert lint.check(source, package=True)
