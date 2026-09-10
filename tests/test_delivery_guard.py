"""Delivery fixtures are generated synthetic data, never real secrets or drafts."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_delivery.py'


@pytest.fixture
def guard():
    assert SCRIPT.is_file(), 'Delivery guard is not implemented yet.'
    spec = importlib.util.spec_from_file_location('delivery_guard', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    (tmp_path / '.gitignore').write_text('.internal/\n.local/\nignored-note.md\n', encoding='utf-8')
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'docs/guide.md').write_text('Public maintenance guidance.', encoding='utf-8')
    return tmp_path


def test_ordinary_public_docs_and_tests_are_scanned(guard, repo):
    (repo / 'tests/example.py').write_text('assert 1 == 1\n', encoding='utf-8')
    report = guard.check_repository(repo)
    assert report['status'] == 'PASS'
    assert report['files_checked'] == 3


@pytest.mark.parametrize('name', ['.internal/log.md', '.local/draft.md',
                                  'docs/private-manuscript.md', 'tests/raw-review.md',
                                  'docs/debug.log', '.env', 'id_rsa', 'docs/backup.zip'])
def test_tracked_private_paths_rejected_without_reading(guard, repo, monkeypatch, name):
    target = repo / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('Synthetic private fixture.', encoding='utf-8')
    subprocess.run(['git', '-C', str(repo), 'add', '-f', '--', name], check=True)
    original = Path.read_bytes
    def observe(path):
        assert path != target, 'Private contents should not be opened.'
        return original(path)
    monkeypatch.setattr(Path, 'read_bytes', observe)
    report = guard.check_repository(repo)
    assert report['status'] == 'FAIL'
    assert any(item['path'] == name for item in report['issues'])


def test_ignored_private_contents_never_opened(guard, repo, monkeypatch):
    private = repo / 'ignored-note.md'
    private.write_text('Synthetic private data.', encoding='utf-8')
    original = Path.read_bytes
    def observe(path):
        assert path != private
        return original(path)
    monkeypatch.setattr(Path, 'read_bytes', observe)
    assert guard.check_repository(repo)['status'] == 'PASS'


@pytest.mark.parametrize('directory', ['docs', 'tests'])
def test_machine_paths_in_any_public_text_are_findings(guard, repo, directory):
    text = '/' + 'Users/' + 'synthetic-person/project/private.md'
    (repo / directory / 'public.md').write_text(text, encoding='utf-8')
    report = guard.check_repository(repo)
    assert any(item['rule'] == 'machine_path' for item in report['issues'])


def test_json_escaped_windows_machine_path_is_found(guard, repo):
    value = 'C:' + '\\' + 'Users' + '\\' + 'synthetic-person' + '\\' + 'draft.md'
    (repo / 'docs/path.json').write_text(json.dumps({'source': value}), encoding='utf-8')
    assert any(item['rule'] == 'machine_path' for item in guard.check_repository(repo)['issues'])


def test_generated_token_detected_without_echoing(guard, repo):
    token = 'ghp_' + 'aB3dE5gH7jK9mN1pQ3sT5vW7yZ9aB1cD3eF5'
    (repo / 'docs/public.md').write_text(token, encoding='utf-8')
    report = guard.check_repository(repo)
    assert any(item['rule'] == 'credential_pattern' for item in report['issues'])
    result = subprocess.run([sys.executable, '-B', str(SCRIPT), str(repo), '--json'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1
    assert token not in result.stdout + result.stderr
    assert 'docs/public.md' not in result.stdout
    assert json.loads(result.stdout)['status'] == 'FAIL'


def test_symlink_never_follows_private_target(guard, repo):
    target = repo / '.internal/private.md'
    target.parent.mkdir()
    target.write_text('Synthetic private target.', encoding='utf-8')
    try:
        (repo / 'docs/link.md').symlink_to(target)
    except OSError:
        pytest.skip('This host cannot create symlinks for this fixture.')
    report = guard.check_repository(repo)
    assert any(item['rule'] == 'unsafe_file' for item in report['issues'])


def test_index_scans_staged_blob_not_clean_worktree(guard, repo):
    path = repo / 'docs/public.md'
    path.write_text('/' + 'Users/' + 'synthetic-person/private.md', encoding='utf-8')
    subprocess.run(['git', '-C', str(repo), 'add', '--', 'docs/public.md'], check=True)
    path.write_text('Now clean only in the working tree.', encoding='utf-8')
    assert guard.check_repository(repo)['status'] == 'PASS'
    assert guard.check_repository(repo, index=True)['status'] == 'FAIL'


def test_removed_tracked_file_is_not_read(guard, repo):
    path = repo / 'docs/removed.md'
    path.write_text('Public old guidance.', encoding='utf-8')
    subprocess.run(['git', '-C', str(repo), 'add', '--', 'docs/removed.md'], check=True)
    path.unlink()
    assert guard.check_repository(repo)['status'] == 'PASS'


def test_package_manifest_and_extra_private_file(guard, tmp_path):
    package = tmp_path / 'academic-writing-assistant'
    package.mkdir()
    (package / 'SKILL.md').write_text('Synthetic exported instructions.', encoding='utf-8')
    (package / 'package-manifest.json').write_text(json.dumps({'format': 1, 'skill': 'academic-writing-assistant', 'files': ['SKILL.md', 'package-manifest.json']}), encoding='utf-8')
    assert guard.check_package(package)['status'] == 'PASS'
    (package / '.internal').mkdir()
    (package / '.internal/private.md').write_text('Synthetic private output.', encoding='utf-8')
    report = guard.check_package(package)
    assert report['status'] == 'FAIL'
    assert any(item['rule'] in {'private_path', 'unlisted_package_file'} for item in report['issues'])


def test_package_traversal_manifest_rejected(guard, tmp_path):
    package = tmp_path / 'academic-writing-assistant'
    package.mkdir()
    (package / 'package-manifest.json').write_text(json.dumps({'format': 1, 'skill': 'academic-writing-assistant', 'files': ['../private.md']}), encoding='utf-8')
    assert guard.check_package(package)['status'] == 'FAIL'


def test_invalid_root_has_no_traceback():
    result = subprocess.run([sys.executable, '-B', str(SCRIPT), 'nonexistent-delivery-root'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 2
    assert 'Traceback' not in result.stderr


@pytest.mark.parametrize('content', [
    ('/' + 'Users/synthetic-person/draft.md').encode('utf-16'),
    b'\0' + ('/' + 'Users/synthetic-person/draft.md').encode(),
])
def test_nul_in_text_is_insufficient_coverage_not_binary_pass(guard, repo, content):
    path = repo / 'docs/guide.md'
    path.write_bytes(content)
    subprocess.run(['git', '-C', str(repo), 'add', '--', 'docs/guide.md'], check=True)
    for index in (False, True):
        report = guard.check_repository(repo, index=index)
        assert report['status'] == 'FAIL'
        assert report['binary_files'] == 0
        assert any(x['rule'] == 'text_decode_coverage' for x in report['issues'])


@pytest.mark.parametrize('value', [
    '/' + 'Users/a/draft.md',
    '/' + 'Users/' + chr(0x738b) + chr(0x660e) + '/draft.md',
    '/' + 'home/synthetic-person',
    'C:' + '/' + 'Users/synthetic-person',
    'C:' + '\\' + 'Users' + '\\' + chr(0x738b),
    'file://' + '/' + 'Users/a/draft.md',
])
def test_machine_user_path_boundaries_in_worktree_and_index(guard, repo, value):
    (repo / 'docs/guide.md').write_text(value, encoding='utf-8')
    subprocess.run(['git', '-C', str(repo), 'add', '--', 'docs/guide.md'], check=True)
    for index in (False, True):
        report = guard.check_repository(repo, index=index)
        assert any(x['rule'] == 'machine_path' for x in report['issues'])


@pytest.mark.parametrize('value', [
    'See https://example.org/home/synthetic-person/guide for public guidance.',
    'https://example.org/a//home/synthetic-person/guide',
    '$HOME/project/guide.md',
    'Path pattern: /' + 'home/.../guide',
])
def test_public_urls_and_variable_roots_are_not_machine_paths(guard, repo, value):
    (repo / 'docs/guide.md').write_text(value, encoding='utf-8')
    assert guard.check_repository(repo)['status'] == 'PASS'


@pytest.mark.parametrize('package_mode', [False, True])
def test_hardlink_alias_is_rejected_before_content_read(guard, repo, monkeypatch, package_mode):
    target = repo / '.internal/fixture.md'
    target.parent.mkdir()
    target.write_text('Clearly synthetic private fixture.', encoding='utf-8')
    root = repo
    if package_mode:
        root = repo / 'academic-writing-assistant'
        root.mkdir()
        (root / 'package-manifest.json').write_text(json.dumps({
            'format': 1, 'skill': root.name,
            'files': ['package-manifest.json', 'SKILL.md'],
        }), encoding='utf-8')
    alias = root / ('SKILL.md' if package_mode else 'docs/alias.md')
    os.link(target, alias)
    original = Path.read_bytes
    def observe(path):
        assert path not in (target, alias), 'Private inode aliases must not be opened.'
        return original(path)
    monkeypatch.setattr(Path, 'read_bytes', observe)
    report = guard.check_package(root) if package_mode else guard.check_repository(root)
    assert report['status'] == 'FAIL'
    assert any(x['rule'] == 'unsafe_file' for x in report['issues'])


@pytest.mark.parametrize('name', ['.env.example', 'LICENSE', 'unknown.data', 'fake.png'])
def test_text_coverage_cannot_be_bypassed_by_renaming(guard, name):
    report = guard.new_report()
    guard.inspect_content(report, name, 'Synthetic configuration.'.encode('utf-16'))
    assert report['status'] == 'FAIL'
    assert report['binary_files'] == 0
    assert report['issues'][0]['rule'] == 'text_decode_coverage'


def test_retained_logo_is_counted_for_separate_image_review(guard):
    report = guard.new_report()
    guard.inspect_content(report, 'logo.png', (ROOT / 'assets/logo/revision-compass.png').read_bytes())
    assert report['status'] == 'PASS'
    assert report['binary_files'] == 1


def test_deep_package_json_is_a_controlled_input_error(tmp_path):
    package = tmp_path / 'academic-writing-assistant'
    package.mkdir()
    manifest = package / 'package-manifest.json'
    data = '[' * 10000 + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * 10000
    manifest.write_text(data, encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--package', str(package), '--json'],
                            capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 2
    assert 'Traceback' not in result.stderr
    assert 'SYNTHETIC_PRIVATE_MARKER' not in result.stderr + result.stdout
    assert manifest.read_text(encoding='utf-8') == data
