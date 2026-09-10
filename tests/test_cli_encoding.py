"""Exercise the CLI UTF-8 protocol independently of the host's stream locale."""
import importlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/academic-writing-assistant/scripts'
CASES = [
    ('fidelity_check.py', [], 'Mean: 5 ms ∓ 1 ms.', '∓'),
    ('manuscript_audit.py', ['--checks', 'claims'], '本文显著提高准确率。', '显著'),
    ('terminology_checker.py', [], '目标检测与对象检测。', '目标检测'),
    ('structure_checker.py', ['--section', 'abstract'], '[请填写结果]', '请填写结果'),
    ('term_consistency_check.py', [], '目标检测与对象检测。', '目标检测'),
    ('section_audit.py', ['--section', 'abstract'], '[请填写结果]', '请填写结果'),
]


def run_cli(script, args, *, encoding='cp1252', input_bytes=None):
    # Child-only settings reproduce legacy redirected Windows streams even on
    # a UTF-8 development machine. Parent pipes stay bytes, with no locale codec.
    env = dict(os.environ, PYTHONIOENCODING=encoding, PYTHONUTF8='0')
    return subprocess.run([sys.executable, '-B', str(SCRIPTS / script), *map(str, args)],
                          input=input_bytes, capture_output=True, env=env)


def manuscript_args(tmp_path, script, args, input_path):
    if script == 'fidelity_check.py':
        before = tmp_path / '原稿 文件.md'
        before.write_text('Mean: 5 ms ± 1 ms.', encoding='utf-8')
        return ['--before', before, '--after', input_path]
    return [*args, input_path]


@pytest.mark.parametrize('script,args,text,needle', CASES)
@pytest.mark.parametrize('from_stdin', [False, True], ids=['file', 'stdin'])
@pytest.mark.parametrize('as_json', [False, True], ids=['markdown', 'json'])
def test_cp1252_cli_preserves_utf8_reports(tmp_path, script, args, text, needle,
                                         from_stdin, as_json):
    path = tmp_path / '稿件 文件.md'
    original = ('\ufeff' + text).encode('utf-8')
    path.write_bytes(original)
    command = manuscript_args(tmp_path, script, args, '-' if from_stdin else path)
    if as_json:
        command.append('--json')
    input_bytes = original if from_stdin else None
    for flags, status in [([], 0), (['--strict'], 1)]:
        expected = run_cli(script, command + flags, encoding='utf-8', input_bytes=input_bytes)
        result = run_cli(script, command + flags, input_bytes=input_bytes)
        assert expected.returncode == status, expected.stderr.decode('utf-8')
        expected_text = expected.stdout.decode('utf-8')
        if not as_json and script in ('structure_checker.py', 'section_audit.py'):
            # Markdown summarizes placeholders by count; JSON retains raw text.
            assert '1 placeholder(s) found.' in expected_text
        else:
            assert needle in expected_text
        assert any(ord(char) > 127 for char in expected_text)
        assert result.returncode == status, result.stderr.decode('utf-8')
        assert result.stdout == expected.stdout
        assert result.stderr == expected.stderr
        if as_json:
            json.loads(result.stdout.decode('utf-8'))
    assert path.read_bytes() == original


@pytest.mark.parametrize('script,args,text,needle', CASES)
@pytest.mark.parametrize('invalid_kind', ['stdin', 'file', 'missing'])
def test_cp1252_cli_input_errors_are_controlled(tmp_path, script, args, text, needle,
                                               invalid_kind):
    path = tmp_path / '无效 稿件.md'
    if invalid_kind == 'file':
        path.write_bytes(b'\xff')
    command = manuscript_args(tmp_path, script, args, '-' if invalid_kind == 'stdin' else path)
    result = run_cli(script, command, input_bytes=b'\xff' if invalid_kind == 'stdin' else None)
    assert result.returncode == 2
    assert not result.stdout
    error = result.stderr.decode('utf-8')
    assert 'Traceback' not in error
    if invalid_kind == 'missing':
        assert path.name in error
    else:
        assert 'utf-8' in error and 'decode' in error
    if invalid_kind == 'file':
        assert path.read_bytes() == b'\xff'


@pytest.mark.parametrize('script', [case[0] for case in CASES] + ['skill_lint.py'])
def test_cp1252_cli_argument_errors_keep_unicode(script):
    args = ['--unexpected-option=中文∓']
    if script == 'fidelity_check.py':
        args.extend(['--before', 'before.md', '--after', 'after.md'])
    elif script in ('structure_checker.py', 'section_audit.py'):
        args.extend(['--section', 'abstract'])
    result = run_cli(script, args)
    assert result.returncode == 2
    error = result.stderr.decode('utf-8')
    assert 'Traceback' not in error
    assert '中文∓' in error


def test_cp1252_lint_report_keeps_unicode_paths(tmp_path):
    package = tmp_path / 'academic-writing-assistant'
    package.mkdir()
    (package / 'SKILL.md').write_text(
        '---\nname: academic-writing-assistant\ndescription: Synthetic fixture.\n---\n'
        '[missing resource](<缺少 文件.md>)\n', encoding='utf-8')
    (package / 'package-manifest.json').write_text(json.dumps({
        'format': 1, 'skill': 'academic-writing-assistant',
        'files': ['SKILL.md', 'package-manifest.json'],
    }), encoding='utf-8')
    expected = run_cli('skill_lint.py', ['--package', package], encoding='utf-8')
    result = run_cli('skill_lint.py', ['--package', package])
    assert expected.returncode == result.returncode == 1
    assert '缺少 文件.md' in expected.stdout.decode('utf-8')
    assert result.stdout == expected.stdout
    assert result.stderr == expected.stderr == b''


def test_library_imports_leave_host_stream_encoding_alone():
    code = """
import importlib, sys
sys.path.insert(0, sys.argv[1])
streams = (sys.stdin, sys.stdout, sys.stderr)
before = [(stream.encoding, stream.errors) for stream in streams]
for name in ('check_utils', 'fidelity_check', 'manuscript_audit',
             'terminology_checker', 'structure_checker', 'skill_lint'):
    importlib.import_module(name)
assert (sys.stdin, sys.stdout, sys.stderr) == streams
assert [(stream.encoding, stream.errors) for stream in streams] == before
assert all(encoding == 'cp1252' for encoding, errors in before)
"""
    result = subprocess.run([sys.executable, '-B', '-c', code, str(SCRIPTS)],
                            env=dict(os.environ, PYTHONIOENCODING='cp1252'),
                            capture_output=True)
    assert result.returncode == 0, result.stderr.decode('utf-8')


def test_cli_stream_configuration_accepts_stringio(monkeypatch):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    from check_utils import configure_cli_streams
    streams = [io.StringIO('\ufeff目标检测'), io.StringIO(), io.StringIO()]
    for name, stream in zip(('stdin', 'stdout', 'stderr'), streams):
        monkeypatch.setattr(sys, name, stream)
    configure_cli_streams()
    assert (sys.stdin, sys.stdout, sys.stderr) == tuple(streams)
    from check_utils import read_input
    assert read_input() == '目标检测'
    module = importlib.import_module('terminology_checker')
    monkeypatch.setattr(sys, 'stdin', io.StringIO('目标检测与对象检测。'))
    assert module.main(['--json']) == 0
    assert json.loads(streams[1].getvalue())[0]['found'] == {'目标检测': 1, '对象检测': 1}
