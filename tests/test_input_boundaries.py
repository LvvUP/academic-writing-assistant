"""CLI boundary tests use only temporary synthetic files and no network."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/academic-writing-assistant/scripts'


def cli(script, *args, input_text=None, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          input=input_text, text=True, encoding='utf-8', capture_output=True, cwd=cwd)


@pytest.mark.parametrize('script,args', [('terminology_checker.py', []), ('structure_checker.py', ['--section', 'abstract']), ('term_consistency_check.py', []), ('section_audit.py', ['--section', 'abstract'])])
def test_missing_empty_and_decode_errors_no_traceback(tmp_path, script, args):
    path = tmp_path / 'draft.txt'
    for data in [None, b'', b'\xff']:
        if data is not None: path.write_bytes(data)
        result = cli(script, *args, path)
        assert result.returncode == 2
        assert 'Traceback' not in result.stderr


@pytest.mark.parametrize('script,args', [('terminology_checker.py', []), ('structure_checker.py', ['--section', 'abstract'])])
def test_bom_stdin_chinese_space_path_other_cwd_and_immutable_input(tmp_path, script, args):
    path = tmp_path / '中文 文件.md'; path.write_text('\ufeff本文关注目标检测和对象检测。', encoding='utf-8')
    original = path.read_bytes()
    file_result = cli(script, *args, path, '--json', cwd=tmp_path)
    stdin_result = cli(script, *args, '-', '--json', input_text='\ufeff本文关注目标检测和对象检测。', cwd=tmp_path)
    assert file_result.returncode == stdin_result.returncode == 0
    assert json.loads(file_result.stdout) == json.loads(stdin_result.stdout)
    assert path.read_bytes() == original


def test_custom_map_bom_and_invalid_structures_exit_two(tmp_path):
    path = tmp_path / 'map.json'
    for value in [[], {'x': None}, {'x': [None]}, {'x': [{'variants_zh': '甲乙'}]}]:
        path.write_text('\ufeff' + json.dumps(value), encoding='utf-8')
        result = cli('terminology_checker.py', '--map', path, input_text='Synthetic text.')
        assert result.returncode == 2 and 'Traceback' not in result.stderr


def test_default_advisory_and_strict_status():
    for script, args, text in [('terminology_checker.py', [], '目标检测与对象检测。'), ('structure_checker.py', ['--section', 'abstract'], '仅有背景。')]:
        assert cli(script, *args, input_text=text).returncode == 0
        assert cli(script, *args, '--strict', input_text=text).returncode == 1


def test_related_terms_are_information_not_strict_failure():
    result = cli('terminology_checker.py', '--strict', '--json', input_text='特征融合与特征聚合采用不同定义。')
    assert result.returncode == 0
    assert json.loads(result.stdout)[0]['action'] == 'preserve_distinction'


def test_structure_research_type_and_invalid_parameters():
    result = cli('structure_checker.py', '--section', 'method', '--research-type', 'theoretical', '--json', input_text='Assumptions support the proof of a theorem.')
    assert result.returncode == 0
    assert json.loads(result.stdout)['research_type'] == 'theoretical'
    assert cli('structure_checker.py', '--section', 'method', '--research-type', 'unknown', input_text='text').returncode == 2
    assert cli('terminology_checker.py', '--language', 'unknown', input_text='text').returncode == 2


def test_large_synthetic_terms_input_has_exact_counts():
    text = ('目标检测对象检测\n' * 3000)
    result = cli('terminology_checker.py', '--json', input_text=text)
    assert result.returncode == 0
    finding = json.loads(result.stdout)[0]
    assert finding['found'] == {'目标检测': 3000, '对象检测': 3000}
    assert len(finding['occurrences']) == 6000


def test_placeholder_raw_text_uses_original_input():
    text = r'[请填写\textbf{结果}]'
    result = cli('structure_checker.py', '--section', 'abstract', '--json', input_text=text)
    assert result.returncode == 0
    item = json.loads(result.stdout)['placeholder_items'][0]
    assert item['raw'] == text[item['start']:item['end']]


@pytest.mark.parametrize('depth', [1100, 10000])
def test_deep_custom_json_is_a_private_controlled_input_error(tmp_path, depth):
    path = tmp_path / 'map.json'
    data = '[' * depth + '"SYNTHETIC_PRIVATE_MARKER"' + ']' * depth
    path.write_text(data, encoding='utf-8')
    result = cli('terminology_checker.py', '--map', path, input_text='Synthetic text.')
    assert result.returncode == 2
    assert 'Traceback' not in result.stderr
    assert 'SYNTHETIC_PRIVATE_MARKER' not in result.stderr + result.stdout
    assert path.read_text(encoding='utf-8') == data
