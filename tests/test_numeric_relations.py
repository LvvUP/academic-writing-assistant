"""Synthetic numeric-relation fixtures; no measurements are real results."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills' / 'academic-writing-assistant' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import fidelity_check as fidelity


MUTATIONS = [
    ('Mean: 5 ms ± 1 ms.', 'Mean: 5 ms ∓ 1 ms.'),
    ('Range: 5 ms – 10 ms.', 'Range: 5 ms + 10 ms.'),
    ('Rate: 5 m / 2 s.', 'Rate: 5 m × 2 s.'),
    ('95% CI: [1, 2].', '95% CI: (1, 2).'),
    ('The interval is [1, 2).', 'The interval is (1, 2].'),
    ('The dose is 5 < x.', 'The dose is 5 > x.'),
    ('Difference: 5 - 3.', 'Difference: 5 to 3.'),
    ('Rate: 5m/2s.', 'Rate: 5m×2s.'),
    ('Mean: 5^2 ms ± 1^2 ms.', 'Mean: 5^2 ms ∓ 1^2 ms.'),
    ('Bounds: 1 < x ≤ 5.', 'Bounds: 1 < x ≥ 5.'),
]


@pytest.mark.parametrize('before,after', MUTATIONS)
def test_numeric_relations_preserve_operators_and_endpoints(before, after):
    prefix = '合成材料。\n'
    report = fidelity.build_report(prefix + before, prefix + after)
    assert report['_meta']['status'] == 'REVIEW_NEEDED'
    assert report['numbers']['status'] == 'REVIEW_NEEDED'
    assert report['numbers']['missing'] and report['numbers']['added']
    assert not report['_meta']['coverage_insufficient']
    for side, source in [('before', prefix + before), ('after', prefix + after)]:
        for item in report['numbers'][side + '_items']:
            assert item['line'] == 2
            assert item['column'] == item['start'] - len(prefix) + 1
            assert source[item['start']:item['end']] == item['raw']


@pytest.mark.parametrize('before,after', [
    ('Mean: 5ms ±1ms.', 'Mean: 5 ms ± 1 ms.'),
    (r'Mean: 5 ms\pm1 ms.', 'Mean: 5 ms±1 ms.'),
    (r'Mean: 5 ms\pm 1 ms.', 'Mean: 5ms ± 1ms.'),
    ('95% CI[1,2].', '95 % CI [1, 2].'),
    ('95% CI: [−1, 2).', '95 % CI: [-1,2).'),
    ('Difference: 5 − 3.', 'Difference: 5 - 3.'),
    ('Dose: −5 mg.', 'Dose: -5mg.'),
    (r'$5\,\mathrm{ms} \pm 1\,\mathrm{ms}$',
     r'$5\,\mathrm{ms}\pm1\,\mathrm{ms}$'),
    ('95% CI [1.2,3.4].', '95% CI [1.2, 3.4].'),
    (r'p \leq0.05.', 'p ≤0.05.'),
    ('Bounds: 1 < x ≤ 5.', 'Bounds: 1<x≤5.'),
])
def test_numeric_relation_layout_changes_remain_clean(before, after):
    report = fidelity.build_report(before, after)
    assert report['_meta']['status'] == 'UNCHANGED_WITHIN_COVERAGE'
    assert not report['_meta']['coverage_insufficient']
    assert report['numbers']['missing'] == report['numbers']['added'] == []


def test_units_belong_to_each_operand_and_repetitions_keep_original_locations():
    first = 'Mean: 5 ms ± 1 ms.'
    before = first + '\n' + first
    after = first + '\nMean: 5 ms ∓ 1 ms.'
    report = fidelity.build_report(before, after)
    numbers = report['numbers']
    assert numbers['before_count'] == numbers['after_count'] == 2
    assert len(numbers['missing']) == len(numbers['added']) == 1
    assert [i['raw'] for i in numbers['before_items']] == ['5 ms ± 1 ms'] * 2
    assert [i['line'] for i in numbers['before_items']] == [1, 2]
    assert [i['start'] for i in numbers['before_items']] == [6, len(first) + 7]


def test_interval_endpoints_are_one_numeric_item_but_plain_citation_is_not():
    text = '95% CI [1, 2].\nThe interval is [1, 2).\nSee [1,2].'
    report = fidelity.build_report(text, text)
    assert report['numbers']['before_count'] == 3
    assert [i['raw'] for i in report['numbers']['before_items']] == ['95%', '[1, 2]', '[1, 2)']
    citation = report['bracket_citations']['before_items']
    assert len(citation) == 1 and citation[0]['raw'] == '[1,2]'
    assert citation[0]['line'] == 3
    assert report['_meta']['status'] == 'UNCHANGED_WITHIN_COVERAGE'


@pytest.mark.parametrize('text', ['95% CI [1, 2', '95% CI [1, x]', 'Range: 5 foounit ± 1 foounit.'])
def test_unsupported_numeric_relations_remain_insufficient(text):
    report = fidelity.build_report(text, text)
    assert report['_meta']['coverage_insufficient']
    assert report['_meta']['status'] == 'INSUFFICIENT'


@pytest.mark.parametrize('ending', ['', ' ', '.', ';', '。', '；', '. Next sentence.', '\n;', ')'])
def test_numeric_comparison_without_operand_is_incomplete_at_punctuation(ending):
    text = 'Bound: 5 < ' + ending
    report = fidelity.build_report(text, text)
    assert report['_meta']['coverage_insufficient']
    assert report['_meta']['status'] == 'INSUFFICIENT'


@pytest.mark.parametrize('operand', ['x.', '(x + 1).', '.5.'])
def test_numeric_comparison_supported_side_is_not_a_missing_operand(operand):
    text = 'Bound: 5 < ' + operand
    report = fidelity.build_report(text, text)
    assert not report['_meta']['coverage_insufficient']
    assert report['_meta']['status'] == 'UNCHANGED_WITHIN_COVERAGE'


@pytest.mark.parametrize('before_text,after_text', MUTATIONS)
def test_relation_mutations_cli_strict_and_advisory_preserve_input(tmp_path, before_text, after_text):
    before = tmp_path / '合成 before.txt'
    after = tmp_path / '合成 after.txt'
    before.write_text(before_text, encoding='utf-8')
    after.write_text(after_text, encoding='utf-8')
    saved = [before.read_bytes(), after.read_bytes()]
    command = [sys.executable, '-B', str(SCRIPTS / 'fidelity_check.py'),
               '--before', str(before), '--after', str(after), '--json']
    advisory = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    strict = subprocess.run(command + ['--strict'], cwd=tmp_path, capture_output=True, text=True)
    assert advisory.returncode == 0, advisory.stderr
    assert strict.returncode == 1, strict.stderr
    result = json.loads(strict.stdout)
    assert result['_meta']['status'] == 'REVIEW_NEEDED'
    assert result['numbers']['missing'] and result['numbers']['added']
    assert [before.read_bytes(), after.read_bytes()] == saved


LINEWRAPPED_MUTATIONS = [
    ('Mean: 5 ms\n± 1 ms.', 'Mean: 5 ms\n∓ 1 ms.'),
    ('Mean: 5\n± 1.', 'Mean: 5\n∓ 1.'),
    ('Bound: 5\n< x.', 'Bound: 5\n> x.'),
    ('Dose: 5\nms.', 'Dose: 5\nns.'),
    ('Mean: 5 ms\r\n  ± 1 ms.', 'Mean: 5 ms\r\n  ∓ 1 ms.'),
    ('Dose: 5\r\n  ms.', 'Dose: 5\r\n  ns.'),
    ('Mean: 5 ms\n\n± 1 ms.', 'Mean: 5 ms\n\n∓ 1 ms.'),
    ('Bound: x <\n5.', 'Bound: x >\n5.'),
]


@pytest.mark.parametrize('before,after', LINEWRAPPED_MUTATIONS)
def test_linewrapped_numeric_relationships_explicitly_report_coverage_gap(before, after):
    report = fidelity.build_report(before, after)
    assert report['_meta']['coverage_insufficient']
    assert report['_meta']['status'] != 'UNCHANGED_WITHIN_COVERAGE'
    for side, source in [('before', before), ('after', after)]:
        warnings = report['_meta'][side + '_coverage']['warnings']
        wraps = [w for w in warnings if w['kind'] == 'linewrapped_numeric_relationship']
        assert wraps
        for warning in wraps:
            assert 0 <= warning['start'] < warning['end'] <= len(source)
            assert '\n' in source[warning['start']:warning['end']]
        for item in report['numbers'][side + '_items']:
            assert source[item['start']:item['end']] == item['raw']


@pytest.mark.parametrize('single_line,wrapped', [
    ('Mean: 5 ms ± 1 ms.', 'Mean: 5 ms\n± 1 ms.'),
    ('Mean: 5 ms ± 1 ms.', 'Mean: 5 ms ±\n1 ms.'),
    ('Dose: 5 ms.', 'Dose: 5\nms.'),
    ('Bound: x < 5.', 'Bound: x <\n5.'),
])
def test_linewrap_only_changes_are_not_claimed_fully_covered(single_line, wrapped):
    report = fidelity.build_report(single_line, wrapped)
    assert report['_meta']['coverage_insufficient']
    assert report['_meta']['after_coverage']['status'] == 'INSUFFICIENT'
    same = fidelity.build_report(wrapped, wrapped)
    assert same['_meta']['status'] == 'INSUFFICIENT'


@pytest.mark.parametrize('text', [
    'There were 5\nparticipants in this synthetic sample.',
    'The total was 5.\nThe following paragraph discusses limitations.',
])
def test_unrelated_prose_line_breaks_do_not_create_numeric_warnings(text):
    report = fidelity.build_report(text, text)
    assert report['_meta']['status'] == 'UNCHANGED_WITHIN_COVERAGE'
    assert not report['_meta']['coverage_insufficient']


@pytest.mark.parametrize('before_text,after_text', LINEWRAPPED_MUTATIONS[:4])
def test_linewrapped_numeric_cli_strict_requires_review_and_preserves_files(tmp_path, before_text, after_text):
    before, after = tmp_path / '换行 before.txt', tmp_path / '换行 after.txt'
    before.write_text(before_text, encoding='utf-8')
    after.write_text(after_text, encoding='utf-8')
    saved = [before.read_bytes(), after.read_bytes()]
    command = [sys.executable, '-B', str(SCRIPTS / 'fidelity_check.py'),
               '--before', str(before), '--after', str(after), '--json']
    for flags, expected in [([], 0), (['--strict'], 1)]:
        result = subprocess.run(command + flags, cwd=tmp_path, capture_output=True, text=True)
        assert result.returncode == expected, result.stderr
        report = json.loads(result.stdout)
        assert report['_meta']['coverage_insufficient']
        assert report['_meta']['status'] != 'UNCHANGED_WITHIN_COVERAGE'
    assert [before.read_bytes(), after.read_bytes()] == saved
