"""Validation checks should test contracts rather than exact presentation."""
import sys
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/academic-writing-assistant/scripts'))
import skill_lint as lint


@pytest.mark.parametrize('frontmatter', [
    'name: academic-writing-assistant\ndescription: 42',
    'name: academic-writing-assistant\ndescription: [one, two]',
    'name: academic-writing-assistant\ndescription: a\ndescription: b',
    'name: academic-writing-assistant\ndescription: "unterminated',
    'name: Academic-Writing\ndescription: fine',
    'name: academic-writing-assistant\ndescription: fine\nmetadata: {version: 3}',
    'name: academic-writing-assistant\ndescription: ' + 'x' * 1025,
])
def test_real_yaml_shape_validation(frontmatter):
    assert lint.validate_frontmatter('---\n' + frontmatter + '\n---\nBody', 'academic-writing-assistant')


def test_valid_yaml_does_not_depend_on_line_spelling():
    assert not lint.validate_frontmatter('---\nname: "academic-writing-assistant"\ndescription: >-\n  Polish a paragraph.\nmetadata:\n  version: "0.3.0"\n---\nBody', 'academic-writing-assistant')


def test_public_inventory_excludes_ignored_internal_records():
    paths = lint.public_files(ROOT)
    assert paths
    assert not any('.internal' in p.parts or '.local' in p.parts or '.git' in p.parts for p in paths)
    assert ROOT / 'docs/design.md' in paths


def test_logo_validation_accepts_size_and_attribute_order_changes():
    text = '<img width="160" alt="Revision Compass logo" src="assets/logo/revision-compass.svg">'
    assert not lint.validate_logo(text, ROOT)
    assert lint.validate_logo(text.replace('Revision Compass logo', ''), ROOT)
    assert lint.validate_logo(text.replace('revision-compass.svg', 'missing.svg'), ROOT)


def test_refusal_and_counterexample_are_not_promises():
    assert not lint.find_promises('禁止绕过检测。\nDo not promise guaranteed acceptance.\n反例：保证录用。')
    assert lint.find_promises('We offer guaranteed acceptance for every manuscript.')


def test_missing_root_is_explained(tmp_path):
    failures = lint.check(tmp_path / 'absent')
    assert failures


def test_package_must_include_runtime_helpers(tmp_path):
    pkg = tmp_path / 'academic-writing-assistant'
    shutil.copytree(ROOT / 'skills/academic-writing-assistant', pkg)
    (pkg / 'LICENSE').write_text('SYNTHETIC TEST LICENSE', encoding='utf-8')
    (pkg / 'THIRD_PARTY_NOTICES.md').write_text('SYNTHETIC TEST NOTICE', encoding='utf-8')
    assert lint.check(pkg, package=True) == []
    for name in ('prose_utils.py', 'check_utils.py', 'fidelity_parser.py'):
        (pkg / 'scripts' / name).unlink()
    assert lint.check(pkg, package=True)


@pytest.mark.parametrize('change', ['semver', 'skills', 'author', 'interface_type'])
def test_manifest_rejects_schema_contract_errors(tmp_path, change):
    manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    (tmp_path / 'skills').mkdir()
    path = tmp_path / 'plugin.json'
    path.write_text(json.dumps(manifest), encoding='utf-8')
    assert lint.validate_manifest(path, tmp_path) == []
    if change == 'semver':
        manifest['version'] = 'not a semver'
    elif change == 'skills':
        manifest['skills'] = '/outside'
    elif change == 'author':
        manifest.pop('author', None)
    else:
        manifest['interface']['displayName'] = 42
    path = tmp_path / 'plugin.json'
    path.write_text(json.dumps(manifest), encoding='utf-8')
    assert lint.validate_manifest(path, tmp_path)


@pytest.mark.parametrize('src', ['../assets/logo/revision-compass.svg', '/assets/logo/revision-compass.svg'])
def test_wrong_logo_paths_are_not_accepted(src):
    assert lint.validate_logo('<img src="' + src + '" alt="Revision Compass">', ROOT)


def test_description_limit_uses_decoded_string_length():
    text = ('---\nname: academic-writing-assistant\ndescription: "' + ' ' * 50 +
            'x' * 1024 + ' ' * 50 + '"\n---\nBody')
    assert lint.validate_frontmatter(text, 'academic-writing-assistant')


def test_skill_symlink_cannot_read_outside_selected_root(tmp_path, monkeypatch):
    repo = tmp_path / 'repo'
    skill = repo / 'skills/academic-writing-assistant'
    skill.mkdir(parents=True)
    private = tmp_path / 'private.md'
    private.write_text('---\nname: academic-writing-assistant\ndescription: synthetic\n---\nBody', encoding='utf-8')
    (skill / 'SKILL.md').symlink_to(private)
    original_read = Path.read_text
    touched = []
    def observed_read(path, *args, **kwargs):
        if path.resolve() == private:
            touched.append(path)
        return original_read(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', observed_read)
    assert lint.check(repo)
    assert touched == []


@pytest.mark.parametrize('relative', ['scripts/prose_utils.py', 'references/fidelity-protocol.md', 'LICENSE'])
def test_package_required_resources_cannot_point_outside(tmp_path, relative):
    package = tmp_path / 'academic-writing-assistant'
    shutil.copytree(ROOT / 'skills/academic-writing-assistant', package)
    (package / 'LICENSE').write_text('SYNTHETIC TEST LICENSE', encoding='utf-8')
    (package / 'THIRD_PARTY_NOTICES.md').write_text('SYNTHETIC TEST NOTICE', encoding='utf-8')
    assert lint.check(package, package=True) == []
    outside = tmp_path / 'outside.txt'
    outside.write_text('SYNTHETIC PRIVATE RESOURCE', encoding='utf-8')
    target = package / relative
    target.unlink()
    target.symlink_to(outside)
    assert lint.check(package, package=True)


@pytest.mark.parametrize('target', ['missing.md', '../../../private.md', '%2e%2e/%2e%2e/private.md'])
def test_transitive_reference_links_are_validated_without_reading_private(tmp_path, monkeypatch, target):
    package = tmp_path / 'academic-writing-assistant'
    shutil.copytree(ROOT / 'skills/academic-writing-assistant', package)
    private = tmp_path / 'private.md'
    private.write_text('SYNTHETIC PRIVATE CONTENT', encoding='utf-8')
    page = package / 'references/submission-package.md'
    page.write_text(page.read_text(encoding='utf-8') + '\n[additional resource](' + target + ')\n', encoding='utf-8')
    touched = []
    original = Path.read_text
    def observe(path, *args, **kwargs):
        if path == private:
            touched.append(path)
        return original(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', observe)
    assert lint.check(package, package=True)
    assert not touched


@pytest.mark.parametrize('mutation', ['missing_manifest', 'duplicate', 'omitted_reference', 'escape'])
def test_standalone_manifest_tracks_its_actual_dependencies(tmp_path, mutation):
    package = tmp_path / 'academic-writing-assistant'
    shutil.copytree(ROOT / 'skills/academic-writing-assistant', package)
    path = package / 'package-manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if mutation == 'missing_manifest':
        path.unlink()
    else:
        if mutation == 'duplicate':
            manifest['files'].append(manifest['files'][0])
        elif mutation == 'omitted_reference':
            manifest['files'].remove('references/policy-sources.md')
        else:
            manifest['files'].append('../private.txt')
        path.write_text(json.dumps(manifest), encoding='utf-8')
    assert lint.check(package, package=True)


def copy_review_package(tmp_path):
    package = tmp_path / 'academic-writing-assistant'
    shutil.copytree(ROOT / 'skills/academic-writing-assistant', package)
    return package


def test_symlink_ancestor_cannot_open_internal_resource(tmp_path, monkeypatch):
    package = copy_review_package(tmp_path)
    internal = package / '.internal'
    internal.mkdir()
    private = internal / 'private.md'
    private.write_text('Synthetic private fixture.', encoding='utf-8')
    (package / 'references/alias').symlink_to(internal, target_is_directory=True)
    manifest = package / 'package-manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['files'].append('references/alias/private.md')
    manifest.write_text(json.dumps(data), encoding='utf-8')
    touched = []
    read = Path.read_text
    def observe(path, *args, **kwargs):
        if path.resolve() == private:
            touched.append(str(path))
        return read(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', observe)
    failures = lint.check(package, package=True)
    assert not touched, touched
    assert failures


@pytest.mark.parametrize('markup', [
    '[extra][resource]\n\n[resource]: ../../../private.md',
    '[extra](<missing resource.md>)',
    '[extra](missing.md \'resource title\')',
])
def test_supported_markdown_forms_cannot_bypass_missing_resource_check(tmp_path, markup):
    package = copy_review_package(tmp_path)
    reference = package / 'references/citation-safety.md'
    reference.write_text(reference.read_text(encoding='utf-8') + '\n\n' + markup + '\n', encoding='utf-8')
    assert lint.check(package, package=True)


def test_manifest_empty_path_is_rejected(tmp_path):
    package = copy_review_package(tmp_path)
    manifest = package / 'package-manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['files'].append('')
    manifest.write_text(json.dumps(data), encoding='utf-8')
    assert lint.check(package, package=True)


def test_schema_bool_format_rejected(tmp_path):
    package = copy_review_package(tmp_path)
    manifest = package / 'package-manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['format'] = True
    manifest.write_text(json.dumps(data), encoding='utf-8')
    assert lint.check(package, package=True)


@pytest.mark.parametrize('name', ['references/CON.md', 'assets/raw.csv'])
def test_manifest_inventory_matches_installer_path_contract(tmp_path, name):
    package = copy_review_package(tmp_path)
    (package / name).write_text('Synthetic unsupported resource.', encoding='utf-8')
    manifest = package / 'package-manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['files'].append(name)
    manifest.write_text(json.dumps(data), encoding='utf-8')
    assert lint.check(package, package=True)



@pytest.mark.parametrize('relative', ['SKILL.md', 'package-manifest.json',
                                     'references/fidelity-protocol.md', 'LICENSE'])
def test_package_hardlink_is_rejected_before_content_read(tmp_path, monkeypatch, relative):
    import os
    package = copy_review_package(tmp_path)
    target = package / relative
    private = tmp_path / 'synthetic-private.md'
    private.write_bytes(target.read_bytes())
    target.unlink()
    os.link(private, target)
    touched = []
    original_read, original_open = Path.read_text, os.open
    def read(path, *args, **kwargs):
        if path == target:
            touched.append('read_text')
        return original_read(path, *args, **kwargs)
    def opened(path, *args, **kwargs):
        if Path(path) == target:
            touched.append('os.open')
        return original_open(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', read)
    monkeypatch.setattr(os, 'open', opened)
    failures = lint.check(package, package=True)
    assert not touched, 'Unsafe inode must be rejected before it is opened.'
    assert failures
    assert private.read_bytes() == target.read_bytes()


@pytest.mark.parametrize('relative', ['README.md', '.codex-plugin/plugin.json', 'docs/guide.md'])
def test_repository_public_hardlink_is_rejected_before_read(tmp_path, monkeypatch, relative):
    import os
    repo = tmp_path / 'repo'
    shutil.copytree(ROOT / 'skills', repo / 'skills')
    shutil.copytree(ROOT / '.codex-plugin', repo / '.codex-plugin')
    shutil.copytree(ROOT / 'assets', repo / 'assets')
    for name in ('README.md', 'README_EN.md'):
        shutil.copyfile(ROOT / name, repo / name)
    (repo / 'docs').mkdir()
    (repo / 'docs/guide.md').write_text('Public synthetic guidance.', encoding='utf-8')
    target = repo / relative
    private = tmp_path / 'synthetic-private.md'
    private.write_bytes(target.read_bytes())
    target.unlink()
    os.link(private, target)
    touched = []
    original = Path.read_text
    original_open = os.open
    def read(path, *args, **kwargs):
        if path == target:
            touched.append('read_text')
        return original(path, *args, **kwargs)
    def opened(path, *args, **kwargs):
        if Path(path) == target:
            touched.append('os.open')
        return original_open(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', read)
    monkeypatch.setattr(os, 'open', opened)
    failures = lint.check(repo)
    assert not touched
    assert failures


def test_selected_package_symlink_root_is_not_resolved_before_validation(tmp_path, monkeypatch):
    package = copy_review_package(tmp_path)
    alias = tmp_path / 'alias'
    alias.symlink_to(package, target_is_directory=True)
    original = Path.read_text
    touched = []
    def read(path, *args, **kwargs):
        touched.append(path)
        return original(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', read)
    assert lint.check(alias, package=True)
    assert not touched


def test_deep_yaml_is_a_controlled_lint_failure():
    text = '---\nname: academic-writing-assistant\ndescription: ' + '[' * 600 + 'synthetic' + ']' * 600 + '\n---\n'
    failures = lint.validate_frontmatter(text, 'academic-writing-assistant')
    assert failures
    assert 'synthetic' not in '\n'.join(failures)


@pytest.mark.parametrize('kind', ['plugin', 'package'])
@pytest.mark.parametrize('depth', [1100, 10000])
def test_deep_json_is_a_controlled_lint_failure(tmp_path, kind, depth):
    nested = '[' * depth + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * depth
    if kind == 'plugin':
        path = tmp_path / 'plugin.json'
        path.write_text(nested, encoding='utf-8')
        failures = lint.validate_manifest(path, tmp_path)
    else:
        package = copy_review_package(tmp_path)
        (package / 'package-manifest.json').write_text(nested, encoding='utf-8')
        failures = lint.check(package, package=True)
    assert failures
    assert 'SYNTHETIC_PRIVATE_MARKER' not in '\n'.join(failures)


def test_real_directory_parent_path_remains_usable(tmp_path):
    package = copy_review_package(tmp_path)
    (package / 'empty').mkdir()
    assert lint.check(package / 'empty/..', package=True) == []


@pytest.mark.parametrize('kind', ['yaml', 'manifest'])
def test_deep_package_configuration_cli_fails_without_traceback(tmp_path, kind):
    import subprocess
    package = copy_review_package(tmp_path)
    if kind == 'yaml':
        target = package / 'SKILL.md'
        data = '---\nname: academic-writing-assistant\ndescription: ' + '[' * 600 + 'SYNTHETIC_PRIVATE_MARKER' + ']' * 600 + '\n---\n'
    else:
        target = package / 'package-manifest.json'
        data = '[' * 10000 + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * 10000
    target.write_text(data, encoding='utf-8')
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'skills/academic-writing-assistant/scripts/skill_lint.py'),
                             '--package', str(package)], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1
    assert 'Status: FAIL' in result.stdout
    assert 'Traceback' not in result.stderr
    assert 'SYNTHETIC_PRIVATE_MARKER' not in result.stdout + result.stderr
    assert target.read_text(encoding='utf-8') == data
