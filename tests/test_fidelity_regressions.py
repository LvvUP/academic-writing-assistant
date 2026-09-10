"""Synthetic fidelity regressions; values and citation keys are fixtures only."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills' / 'academic-writing-assistant' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('fidelity_regression_module', SCRIPTS / 'fidelity_check.py')
fidelity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fidelity)


def changed(report):
    return any(data.get('missing') or data.get('added') or data.get('context_changes')
               for name, data in report.items() if not name.startswith('_'))


@pytest.mark.parametrize('before,after', [
    ('Value: 3.2e-4.', 'Value: 3.2e-2.'),
    ('Value: -5.', 'Value: 5.'),
    ('Value: −5.', 'Value: 5.'),
    ('Dose: 5 mg.', 'Dose: 5 g.'),
    ('p < 0.05.', 'p > 0.05.'),
    ('p ≤ 0.05.', 'p ≥ 0.05.'),
    ('p = 0.05.', 'p ≤ 0.05.'),
    ('Accuracy: 5%.', 'Accuracy: 5 percentage points.'),
    ('范围5–7 mg。', '范围5–9 mg。'),
    ('95% CI [1.2, 3.4].', '95% CI [1.2, 3.8].'),
    ('Mean: 89.2 ± 0.3.', 'Mean: 89.2 ± 0.5.'),
    ('Count: 1,024.', 'Count: 1,204.'),
    ('准确率为92.3%。', '准确率为94.3%。'),
    ('值为５．２％。', '值为５．３％。'),
    (r'Accuracy: 92.3\%.', r'Accuracy: 92.3.'),
    (r'Dose: \SI{5}{\milli\gram}.', r'Dose: \SI{5}{\gram}.'),
    (r'Value: \num{3.2e-4}.', r'Value: \num{3.2e-2}.'),
    ('Table 1.', 'Figure 1.'),
    (r'Work \citep{synthetic:key}.', r'Work \citet{synthetic:key}.'),
    (r'See \eqref{synthetic:x}.', r'See \ref{synthetic:x}.'),
    (r'Use \method{alpha}.', r'Use \method{beta}.'),
    (r'Use \method{a{nested}}.', r'Use \method{b{nested}}.'),
    (r'$\text{a b}$', r'$\text{ab}$'),
    ('Accuracy is 90. Recall is 80.', 'Accuracy is 80. Recall is 90.'),
    ('Claim A [1]. Claim B [2].', 'Claim A [2]. Claim B [1].'),
])
def test_protected_mutations_are_detected(before, after):
    assert changed(fidelity.build_report(before, after))


def test_repeated_differences_keep_multiplicity():
    result = fidelity.compare(['5', '5', '5'], ['5'])
    assert result['missing'] == ['5', '5']


def test_source_locations_and_context_are_original():
    original = 'Synthetic fixture.\n剂量为5 mg，p < 0.05。'
    result = fidelity.build_report(original, original)
    items = result['numbers']['before_items']
    dose = next(item for item in items if '5 mg' in item['raw'])
    assert dose['line'] == 2
    assert original[dose['start']:dose['end']] == dose['raw']
    assert dose['column'] == 4
    assert '剂量' in dose['context']


@pytest.mark.parametrize('before,after', [
    ('Dose: −5 mg.', 'Dose: -5 mg.'),
    ('Count: 1,024.', 'Count: 1024.'),
    ('Value: 3.2E-4.', 'Value: 3.2e-4.'),
    (r'Accuracy: 92.3\%.', 'Accuracy: 92.3%.'),
    (r'$x + y = 2$', r'$x+y=2$'),
    ('The accuracy was 90.1%.', 'The accuracy reached 90.1%.'),
    ('A is 5. B is 7.', 'B is 7. A is 5.'),
])
def test_safe_formatting_or_prose_changes_do_not_report_mutations(before, after):
    assert not changed(fidelity.build_report(before, after))


@pytest.mark.parametrize('text', ['', 'Only ordinary prose.', '$x + 2', r'\method{broken'])
def test_zero_or_invalid_coverage_is_not_pass(text):
    report = fidelity.build_report(text, text)
    rendered, clean = fidelity.render(report)
    assert not clean
    assert 'INSUFFICIENT' in rendered
    assert report['_meta']['status'] == 'INSUFFICIENT'


def test_comments_and_code_are_not_manuscript_numbers():
    text = 'Value: 5.\n% comment: 8\n```tex\n\\cite{fake} 99\n```\n\\begin{verbatim}\n12\n\\end{verbatim}'
    report = fidelity.build_report(text, text)
    assert report['numbers']['before_count'] == 1
    assert report['citations']['before_count'] == 0
    assert report['_meta']['before_coverage']['excluded_regions']


def test_escaped_dollars_do_not_start_math():
    report = fidelity.build_report(r'Cost: \$5, result $x=2$.', r'Cost: \$5, result $x=2$.')
    assert report['math_blocks']['before_count'] == 1
    assert report['numbers']['before_count'] == 1


def test_nested_math_and_text_spaces_are_kept():
    report = fidelity.build_report(r'$\text{a {b c}} + x$', r'$\text{a {bc}} + x$')
    assert report['math_blocks']['missing']


def test_html_and_markdown_are_escaped_in_reports():
    rendered, _ = fidelity.render(fidelity.build_report(r'\method{<script>x</script>`|}', r'\method{b}'))
    assert '<script>' not in rendered
    assert '&lt;script&gt;' in rendered


def run_cli(*args, input_text=None, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPTS / 'fidelity_check.py'), *map(str, args)],
                          input=input_text, text=True, encoding='utf-8', capture_output=True, cwd=cwd)


def test_cli_stdin_bom_chinese_path_and_immutable_files(tmp_path):
    after = tmp_path / '中文 path.tex'
    after.write_text('\ufeffDose: 5 mg.', encoding='utf-8')
    original = after.read_bytes()
    result = run_cli('--before', '-', '--after', after, '--json', '--strict',
                     input_text='Dose: 5 mg.', cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['_meta']['status'] == 'UNCHANGED_WITHIN_COVERAGE'
    assert after.read_bytes() == original


@pytest.mark.parametrize('kind', ['empty', 'decode', 'missing', 'both_stdin'])
def test_cli_input_errors_have_exit_two_without_traceback(tmp_path, kind):
    good = tmp_path / 'good.txt'; good.write_text('Value: 5.', encoding='utf-8')
    bad = tmp_path / 'bad.txt'
    if kind == 'empty': bad.write_text('  ', encoding='utf-8')
    if kind == 'decode': bad.write_bytes(b'\xff')
    args = ['--before', bad, '--after', good]
    if kind == 'both_stdin': args = ['--before', '-', '--after', '-']
    result = run_cli(*args, input_text='Value: 5.')
    assert result.returncode == 2
    assert 'Traceback' not in result.stderr


def test_strict_change_and_coverage_exit_codes(tmp_path):
    before = tmp_path / 'before.txt'; after = tmp_path / 'after.txt'
    before.write_text('Value: 5 mg.', encoding='utf-8'); after.write_text('Value: 5 g.', encoding='utf-8')
    assert run_cli('--before', before, '--after', after).returncode == 0
    assert run_cli('--before', before, '--after', after, '--strict').returncode == 1
    before.write_text('Ordinary prose.', encoding='utf-8'); after.write_text('Ordinary prose.', encoding='utf-8')
    assert run_cli('--before', before, '--after', after, '--strict').returncode == 1


def test_large_synthetic_input_preserves_counts():
    text = ('Synthetic value: 5 mg.\n' * 3000)
    report = fidelity.build_report(text, text)
    assert report['numbers']['before_count'] == 3000
    assert not changed(report)


@pytest.mark.parametrize('before,after', [
    ('5 cm2', '5 cm3'),
    (r'p \leq 0.05', r'p \geq 0.05'),
    (r'5 \pm 0.3', r'5 \mp 0.3'),
    ('5 foounit', '5 barunit'),
    ('3.2 × 10⁻⁴', '3.2 × 10⁻²'),
])
def test_further_numeric_notation_boundaries(before, after):
    assert changed(fidelity.build_report(before, after))


@pytest.mark.parametrize('before,after', [('5 %', '5%'),
                                         (r'\cite{synthetic:a, synthetic:b}', r'\cite{synthetic:a,synthetic:b}')])
def test_harmless_token_spacing(before, after):
    assert not changed(fidelity.build_report(before, after))


@pytest.mark.parametrize('text', [r'\method alpha', r'$\input{synthetic}$', '5 foounit'])
def test_unsupported_notation_reports_coverage_gap(text):
    report = fidelity.build_report(text, text)
    assert report['_meta']['coverage_insufficient']


def test_math_comments_are_excluded_and_layout_can_change():
    before = '$x=5 % synthetic comment\n +y$'
    after = '$x=5+y$'
    assert not changed(fidelity.build_report(before, after))


def test_untrusted_latex_is_never_executed(tmp_path):
    sentinel = tmp_path / 'synthetic-private.txt'
    sentinel.write_text('synthetic secret fixture', encoding='utf-8')
    text = r'\input{' + str(sentinel) + r'} \write18{echo untrusted}'
    report = fidelity.build_report(text, text)
    assert report['_meta']['coverage_insufficient']
    assert 'synthetic secret fixture' not in json.dumps(report)
    assert sentinel.read_text(encoding='utf-8') == 'synthetic secret fixture'


@pytest.mark.parametrize('text', [r'\num{banana}', r'\SI{5}', r'\method{' + '{' * 130 + 'x' + '}' * 131])
def test_invalid_or_excessive_argument_constructs_are_insufficient(text):
    assert fidelity.build_report(text, text)['_meta']['coverage_insufficient']


def test_large_single_line_input_does_not_invent_items():
    text = 'synthetic ' * 10000 + '5 mg'
    report = fidelity.build_report(text, text)
    assert report['numbers']['before_count'] == 1
    assert not changed(report)


def test_numeric_table_cells_swapped_require_association_review():
    before = '| Accuracy | Recall |\n| 90 | 80 |'
    after = '| Accuracy | Recall |\n| 80 | 90 |'
    report = fidelity.build_report(before, after)
    assert report['numbers']['missing'] == []
    assert report['numbers']['added'] == []
    assert report['numbers']['context_changes'][0]['kind'] == 'unresolved_sequence_change'


def test_positions_of_repeated_protected_values_are_distinct():
    text = 'Value: 5 mg.\nValue: 5 mg.'
    items = fidelity.build_report(text, text)['numbers']['before_items']
    assert [item['line'] for item in items] == [1, 2]
    assert items[0]['start'] < items[1]['start']


@pytest.mark.parametrize('before,after', [
    (r'$a\ b$', r'$a\b$'),
    ('Value: 3.2 × 10⁻⁴.', 'Value: 3.2 ÷ 10⁻⁴.'),
    ('Accuracy: 95% and recall 80%.\n```tex\n\\begin{document}\n```',
     'Accuracy: 95% and recall 90%.\n```tex\n\\begin{document}\n```'),
    (r'\begin{document}{Result 5 mg.}\end{document}',
     r'\begin{document}{Result 7 mg.}\end{document}'),
])
def test_independent_review_protected_mutations(before, after):
    assert changed(fidelity.build_report(before, after))


@pytest.mark.parametrize('text', [r'Result 5 mg \cite{}.', r'Result 5 mg \ref{}.',
                                  r'\num{5e}', r'\SI{+}{\gram}'])
def test_independent_review_empty_or_invalid_arguments(text):
    assert fidelity.build_report(text, text)['_meta']['coverage_insufficient']


def test_citation_arity_does_not_consume_adjacent_prose_group():
    text = r'Work \cite{synthetic:a,synthetic:b}{ text with 5 mg}.'
    report = fidelity.build_report(text, text)
    assert [item['key'] for item in report['citations']['before_items']] == ['synthetic:a', 'synthetic:b']
    assert report['numbers']['before_count'] == 1
    assert report['citations']['before_items'][0]['raw'] == r'\cite{synthetic:a,synthetic:b}'


def test_ordinary_count_adjective_is_not_an_unknown_unit():
    text = 'There were 5 healthy participants.'
    report = fidelity.build_report(text, text)
    assert not report['_meta']['coverage_insufficient']
    assert report['numbers']['before_items'][0]['value'] == '5'
