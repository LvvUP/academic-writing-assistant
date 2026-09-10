"""Synthetic regression fixtures; no real research results or manuscripts."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/academic-writing-assistant/scripts'
sys.path.insert(0, str(SCRIPTS))
import manuscript_audit as audit
from prose_utils import mask_prose


def significance(text):
    return [f for f in audit.check_claims(text) if f['type'] == 'significance_without_test']


def test_tex_body_nested_formatting_and_original_positions():
    text = ('\\documentclass{article}\n\\begin{document}\n\\begin{abstract}\n'
            '\\textbf{Our \\emph{method} significantly improves accuracy.}\n'
            '\\end{abstract}\n\\end{document}\n')
    prose = audit.strip_markup(text)
    assert len(prose) == len(text)
    assert prose.count('\n') == text.count('\n')
    assert 'significantly improves accuracy' in prose
    findings = significance(text)
    assert len(findings) == 1
    assert findings[0]['line'] == 4
    assert text[findings[0]['start']:findings[0]['end']].startswith('Our ')


def test_repeated_sentences_have_distinct_original_locations():
    text = 'Our method significantly improves accuracy.\n\nOur method significantly improves accuracy.'
    findings = significance(text)
    assert [f['line'] for f in findings] == [1, 3]
    assert [f['start'] for f in findings] == [0, text.rfind('Our')]


@pytest.mark.parametrize('evidence', ['std = 0.3', 'SD 0.3', '± 0.3', 'standard deviation 0.3', '95% CI [0.1, 0.8]', 'p = 0.01'])
def test_distant_statistics_do_not_certify_current_claim(evidence):
    assert len(significance(f'Another outcome: {evidence}.\n\nOur method significantly improves accuracy.')) == 1


@pytest.mark.parametrize('text', [
    'The improvement was statistically significant (paired t-test, p = 0.01).',
    'The difference was not statistically significant.',
    'No significant difference was observed.',
    'We cannot conclude that the difference is significant.',
    'The parameter has three significant digits.',
    'This is of practical significance.',
    '该差异不具有统计显著性。',
    '未观察到显著差异。',
    '显著性水平设为 0.05。',
])
def test_careful_or_nonstatistical_language_is_not_a_positive_claim(text):
    assert not significance(text)


def test_chinese_sentences_without_spaces_and_decimals():
    text = '均值为0.35。该方法显著提升准确率。该方法显著提升准确率。'
    findings = significance(text)
    assert len(findings) == 2
    assert [f['start'] for f in findings] == [text.find('该方法'), text.rfind('该方法')]
    assert len(audit.split_sentences('Dr. A used e.g. 0.35 as a value. Another sentence.')) == 2


def test_comments_math_code_masked_without_losing_following_lines():
    text = ('% Our method significantly improves accuracy.\n'
            '$\\text{significantly improves}$\n'
            '\\begin{verbatim}\nOur method significantly improves accuracy.\n\\end{verbatim}\n'
            '```python\nOur method significantly improves accuracy.\n```\n'
            'Our method significantly improves accuracy.')
    findings = significance(text)
    assert len(findings) == 1
    assert findings[0]['line'] == 9


def test_normal_method_present_and_experiment_past_are_allowed():
    assert audit.check_tense('The encoder extracts features. We trained it for 10 epochs.') == []


@pytest.mark.parametrize('code', ['```tex\n\\begin{document}\n```', '`\\documentclass{article}`'])
def test_tex_markers_in_code_do_not_hide_percent_following_prose(code):
    text = code + '\nAccuracy is 95% and significantly improves over baseline.'
    prose, _, excluded = mask_prose(text)
    assert '95% and significantly improves' in prose
    assert not any(item['kind'] == 'comment' for item in excluded)
    findings = significance(text)
    assert len(findings) == 1
    assert findings[0]['line'] == text.count('\n') + 1


def test_actual_tex_context_still_masks_inline_comments():
    text = '\\begin{document}\nAccuracy is 95\\%. % significantly improves\n\\end{document}'
    prose, _, excluded = mask_prose(text)
    assert 'significantly improves' not in prose
    assert any(item['kind'] == 'comment' for item in excluded)


def test_abbreviation_positions_are_in_original_tex():
    text = '\\begin{document}\n\\textbf{MSFF} is used here.\nMulti-scale feature fusion (MSFF) follows.\n\\end{document}'
    findings = audit.check_abbreviations(text)
    finding = next(f for f in findings if f['type'] == 'abbreviation_used_before_definition')
    assert finding['line'] == 2
    assert text[finding['start']:finding['end']] == 'MSFF'


def test_cli_errors_strict_and_readonly(tmp_path):
    path = tmp_path / '中文 稿件.tex'
    path.write_text('\ufeff\\begin{document}\nOur method significantly improves accuracy.\n\\end{document}', encoding='utf-8')
    original = path.read_bytes()
    result = subprocess.run([sys.executable, str(SCRIPTS / 'manuscript_audit.py'), str(path), '--json', '--strict', '--checks', 'claims'], capture_output=True, text=True, encoding='utf-8', cwd=tmp_path)
    assert result.returncode == 1
    assert json.loads(result.stdout)['claims'][0]['line'] == 2
    assert path.read_bytes() == original
    for args in [['--checks', ''], ['--limit-words', '-1'], ['--limit-chars', '0']]:
        result = subprocess.run([sys.executable, str(SCRIPTS / 'manuscript_audit.py'), str(path), *args], capture_output=True, text=True, encoding='utf-8')
        assert result.returncode == 2
        assert 'Traceback' not in result.stderr


def test_untrusted_markup_is_escaped_in_report():
    output = audit.render({'claims': [{'type': 'synthetic', 'item': '<script>alert(1)</script> | **x**', 'line': 1, 'note': ''}]}, None)
    assert '<script>' not in output


@pytest.mark.parametrize('text', [
    'Our method significantly\nimproves accuracy.',
    'Our method significantly improves accuracy without a statistical test.',
    'Our method significantly improves accuracy and does not require supervision.',
    'Our method significantly improves accuracy, and we plan to run a t-test.',
    'Our method significantly improves accuracy (`p = 0.01`).',
    'The score was 95% and the method significantly improves accuracy with $\\alpha$.',
])
def test_significance_review_cannot_be_silenced_by_unrelated_syntax(text):
    assert len(significance(text)) == 1


def test_reported_inline_math_p_value_is_visible_as_evidence():
    assert not significance('Our method significantly improves accuracy (paired t-test, $p = 0.01$).')


def test_wrapped_sentence_is_checked():
    text = 'Our method significantly\nimproves accuracy.'
    result = significance(text)
    assert len(result) == 1
    assert result[0]['start'] == 0


@pytest.mark.parametrize('text', [
    'Our method significantly improves accuracy without a statistical test.',
    'Our method significantly improves accuracy and does not require supervision.',
    'Our method not only significantly improves accuracy, it also reduces memory.',
    'The values use three significant digits and the method significantly improves accuracy.',
])
def test_unrelated_negation_or_nonstat_phrase_cannot_hide_claim(text):
    assert len(significance(text)) == 1


@pytest.mark.parametrize('text', [
    'Our method significantly improves accuracy, and we plan to run a t-test.',
    'A changed (p = 0.01), while B significantly improved.',
    'Our method significantly improves accuracy (`p = 0.01`).',
    r'Our method significantly improves accuracy (\begin{comment}p=0.01\end{comment}).',
])
def test_unperformed_unrelated_or_excluded_evidence_cannot_certify_claim(text):
    assert len(significance(text)) == 1


def test_markdown_math_does_not_turn_percent_into_tex_comment():
    text = r'The score was 95% and our method significantly improves accuracy with $\alpha$.'
    prose, warnings, _ = mask_prose(text)
    assert 'significantly improves' in prose or warnings


def test_unread_tex_include_is_coverage_limit():
    assert mask_prose(r'Normal prose. \input{results}')[1]


def test_unclosed_text_argument_is_coverage_limit():
    assert mask_prose(r'Normal \textbf{content here.')[1]


def test_indented_tilde_fence_excludes_style_text():
    text = '   ~~~python\nWith the rapid development of science\n   ~~~'
    assert audit.check_style(text) == []


def test_newcommand_body_is_not_prose():
    text = r'\newcommand{\myterm}[1]{Our method significantly improves #1.}' + '\nNormal prose.'
    assert significance(text) == []


def test_comment_brace_does_not_close_citation_group():
    text = r'\cite{a % }' + '\n' + r'b} Our method significantly improves accuracy.'
    result = significance(text)
    assert len(result) == 1
    assert result[0]['start'] == text.index('Our')


def test_excluded_spaces_do_not_count_as_visible_characters():
    text = r'A \cite{a' + ' ' * 200 + r'b} B'
    result = audit.check_length(text, None, 10, False)
    assert not any(f['type'] == 'over_char_limit' for f in result)


def test_empty_check_selection_is_usage_error():
    result = subprocess.run([sys.executable, str(SCRIPTS / 'manuscript_audit.py'),
                             '--checks', ',,,', '--strict', '--json'],
                            input='Normal prose.', capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 2


def test_comment_inside_math_cannot_supply_evidence():
    text = r'Our method significantly improves accuracy ($x=1 % p=0.01' + '\n' + r'$).'
    assert len(significance(text)) == 1


@pytest.mark.parametrize('text', [
    'The differences were significant.',
    '两组之间的差异显著。',
    '两组之间存在显著的差异。',
    '准确率显著高于基线。',
])
def test_common_positive_significance_grammar_is_covered(text):
    assert len(significance(text)) == 1


@pytest.mark.parametrize('text', [
    'The differences were not significant.',
    '两组之间的差异不显著。',
])
def test_matched_negative_grammar_remains_quiet(text):
    assert significance(text) == []


@pytest.mark.parametrize('text', [
    'Normal prose. \\label{sec} {Our method significantly improves accuracy.}',
    '\\cite{a}\n\n{Our method significantly improves accuracy.}',
])
def test_opaque_command_does_not_eat_later_prose_group(text):
    found = significance(text)
    assert len(found) == 1
    assert found[0]['start'] == text.index('Our')


def test_unmatched_text_environment_reports_insufficient_coverage():
    assert mask_prose('Normal prose. \\begin{abstract}Text.\\end{document}')[1]


@pytest.mark.parametrize('text', [
    'The differences were significant.', '两组之间的差异显著。',
    '两组之间存在显著的差异。', '准确率显著高于基线。',
    'Our method significantly improves accuracy ($x=1 % p=0.01\n$).',
])
def test_additional_positive_claim_syntax(text):
    assert len(significance(text)) == 1


@pytest.mark.parametrize('text', ['The differences were not significant.', '两组差异不显著。',
                                 '准确率未显著高于基线。'])
def test_additional_negated_claim_syntax(text):
    assert not significance(text)


@pytest.mark.parametrize('sentence', [
    'Outcome A changed (p = 0.01), and outcome B significantly improved.',
    'Outcome A changed (p = 0.01) and outcome B significantly improved.',
    'Outcome A changed (p = 0.01), while outcome B significantly improved.',
    'Outcome A changed (p = 0.01), and the second outcome significantly improved.',
])
def test_final_claims_other_outcome_cannot_supply_significance(sentence):
    text = 'Synthetic introduction.\n' + sentence
    original = text
    findings = significance(text)
    assert len(findings) == 1
    finding = findings[0]
    subject = 'the second outcome' if 'second outcome' in text else 'outcome B'
    assert finding['type'] == 'significance_without_test'
    assert finding['start'] == text.index(subject)
    assert finding['end'] == len(text)
    assert finding['line'] == 2
    assert finding['source'] == text[finding['start']:finding['end']]
    assert 'p = 0.01' not in finding['source']
    assert text == original


@pytest.mark.parametrize('sentence', [
    'Outcome A changed (p = 0.01), and outcome B significantly improved (p = 0.02).',
    'Accuracy significantly improved (p = 0.01) and remained stable.',
    'Accuracy and recall significantly improved (paired t-test, p = 0.01).',
    'Accuracy significantly improved according to a paired t-test and Wilcoxon test.',
    'Accuracy significantly improved, and a paired t-test returned p = 0.01.',
])
def test_final_claims_conjunction_does_not_break_local_statistical_support(sentence):
    assert significance(sentence) == []


@pytest.mark.parametrize('sentence', [
    'Our method outperforms all three evaluated baselines on DatasetA.',
    'Our method outperforms all 3 baselines on DatasetA.',
    'Our method outperforms all evaluated methods.',
    'Our method outperforms all the selected models.',
    'Our method outperforms all methods evaluated in this study.',
    'Our method is superior to all three evaluated baselines on DatasetA.',
])
def test_final_claims_bounded_comparison_set_is_not_universal(sentence):
    assert not [f for f in audit.check_claims(sentence) if f['type'] == 'unbounded_claim']


@pytest.mark.parametrize('sentence', [
    'Our method outperforms all existing methods.',
    'Our method outperforms all methods on DatasetA.',
    'Our evaluated method outperforms all other methods.',
    'Our method outperforms all three evaluated baselines and all existing methods.',
    'We evaluated three baselines, but our method outperforms all methods.',
])
def test_final_claims_unbounded_comparison_is_still_reviewed(sentence):
    text = 'Synthetic introduction.\n' + sentence
    findings = [f for f in audit.check_claims(text) if f['type'] == 'unbounded_claim']
    assert len(findings) == 1
    finding = findings[0]
    assert finding['line'] == 2
    assert finding['source'] == text[finding['start']:finding['end']]
    assert 'outperforms all' in finding['source']


@pytest.mark.parametrize('sentence', [
    'This association does not establish that A causes B.',
    'We cannot conclude that A causes B.',
    'A does not cause B.',
    "A doesn't cause B.",
    "This association doesn't establish that A causes B.",
    'The change is not due to A.',
    'We tested whether A causes B.',
    '这种相关性不能证明A导致B。',
])
def test_final_claims_explicit_causal_denial_or_question_is_not_assertion(sentence):
    assert not [f for f in audit.check_claims(sentence) if f['type'] == 'causal_language']


@pytest.mark.parametrize('sentence', [
    'A causes B.',
    'A not only causes B, it also affects C.',
    'We do not measure C, but A causes B.',
    'This association does not establish that A causes B, but C causes D.',
    'We cannot conclude that A causes B, and C causes D.',
])
def test_final_claims_affirmative_causality_survives_unrelated_negation(sentence):
    text = 'Synthetic introduction.\n' + sentence
    findings = [f for f in audit.check_claims(text) if f['type'] == 'causal_language']
    assert len(findings) == 1
    finding = findings[0]
    assert finding['line'] == 2
    assert finding['source'] == text[finding['start']:finding['end']]
    if 'C causes D' in sentence:
        assert 'C causes D' in finding['source']


@pytest.mark.parametrize('strict, expected_exit', [(False, 0), (True, 1)])
def test_final_claims_cli_json_stdin_bom_and_readonly(tmp_path, strict, expected_exit):
    text = ('Outcome A changed (p = 0.01), and outcome B significantly improved.\n'
            'Our method outperforms all three evaluated baselines on DatasetA.\n'
            'This association does not establish that A causes B.')
    path = tmp_path / '合成 claims.md'
    path.write_text('\ufeff' + text, encoding='utf-8')
    before = path.read_bytes()
    command = [sys.executable, '-B', str(SCRIPTS / 'manuscript_audit.py')]
    flags = ['--checks', 'claims', '--json'] + (['--strict'] if strict else [])
    file_result = subprocess.run(command + [str(path)] + flags, capture_output=True,
                                 text=True, encoding='utf-8', cwd=tmp_path)
    stdin_result = subprocess.run(command + ['-'] + flags, input='\ufeff' + text,
                                  capture_output=True, text=True, encoding='utf-8', cwd=tmp_path)
    for result in [file_result, stdin_result]:
        assert result.returncode == expected_exit
        assert result.stderr == ''
        findings = json.loads(result.stdout)['claims']
        assert [f['type'] for f in findings] == ['significance_without_test']
        assert findings[0]['start'] == text.index('outcome B')
        assert findings[0]['source'] == 'outcome B significantly improved.'
    assert path.read_bytes() == before


def test_final_claims_bounded_first_comparison_does_not_hide_universal_second_object():
    text = 'Our method is superior to all three tested models and to all existing methods.'
    assert [f['type'] for f in audit.check_claims(text)] == ['unbounded_claim']


def test_final_claims_later_outcome_cannot_supply_earlier_significance():
    text = 'Outcome B significantly improved, and outcome A changed (p = 0.01).'
    findings = significance(text)
    assert len(findings) == 1
    assert findings[0]['start'] == 0
    assert findings[0]['end'] < text.index('outcome A')
    assert 'p = 0.01' not in findings[0]['source']
    assert findings[0]['source'] == text[:findings[0]['end']]
