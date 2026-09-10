"""Synthetic fixtures for terminology relations and study-aware structure clues."""
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/academic-writing-assistant/scripts'
sys.path.insert(0, str(SCRIPTS))
import terminology_checker as terms
import structure_checker as structure
from check_utils import placeholder_spans


def entry(**kwargs):
    value = dict(recommended_zh='训练集', variants_zh=['训练集', '训练数据集'],
                 en='training set', note='Synthetic fixture.', relation='style_preference')
    value.update(kwargs)
    return value


def write_map(tmp_path, data):
    path = tmp_path / '术语 map.json'
    path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    return path


@pytest.mark.parametrize('data', [[], {'field': 1}, {'field': [None]},
    {'field': [{'variants_zh': ['甲', '乙']}]},
    {'field': [{'recommended_zh': '甲', 'variants_zh': [1, '乙'], 'en': 'x', 'note': 'x'}]},
    {'field': [dict(recommended_zh='丙', variants_zh=['甲', '乙'], en='x', note='x')]},
    {'field': [dict(recommended_zh='甲', variants_zh=['甲', '乙'], en=2, note='x')]},
    {'field': [entry(author_confirmed='yes')]}, {'field': [entry(relation='same')]},
    {'field': [entry(preferred='未知')]}, {},
])
def test_invalid_glossary_has_explained_value_error(tmp_path, data):
    with pytest.raises(ValueError, match='map|field|entry|variants|recommended|author|relation|preferred|term|glossary'):
        terms.load_terms(write_map(tmp_path, data))


def test_longest_nonoverlapping_matches_keep_locations():
    glossary = [dict(recommended_zh='模型', variants_zh=['模型', '大模型', '大模型'], en='model', note='Synthetic fixture.', relation='related_concepts')]
    text = '大模型与模型。\n大模型。'
    finding = terms.find_inconsistencies(text, glossary)[0]
    assert finding['found'] == {'大模型': 2, '模型': 1}
    assert [item['line'] for item in finding['occurrences']] == [1, 1, 2]
    assert all(text[item['start']:item['end']] == item['raw'] for item in finding['occurrences'])


def test_related_concepts_do_not_recommend_normalizing():
    glossary = [dict(recommended_zh='特征融合', variants_zh=['特征融合', '特征聚合'], en='fusion / aggregation', note='Distinct concepts in this synthetic study.', relation='related_concepts')]
    finding = terms.find_inconsistencies('特征融合与特征聚合是两个模块。', glossary)[0]
    assert finding['relation'] == 'related_concepts'
    assert finding['action'] == 'preserve_distinction'
    assert finding['recommended'] == ''
    assert finding['requires_review'] is False


def test_confirmed_author_preference_wins_over_majority():
    glossary = [entry(author_confirmed=True, preferred='训练数据集')]
    finding = terms.find_inconsistencies('训练集和训练集，亦称训练数据集。', glossary)[0]
    assert finding['dominant'] == '训练集'
    assert finding['recommended'] == '训练数据集'
    assert finding['priority'] == 'author_confirmed'


def test_english_case_word_boundaries_and_contexts():
    glossary = [entry(variants_en=['dataset', 'data set'], recommended_en='dataset')]
    finding = terms.find_inconsistencies('DATASET, datasets and data set.\nDatasets are plural.', glossary, language='en')[0]
    assert finding['found'] == {'dataset': 1, 'data set': 1}
    assert finding['language'] == 'en'
    assert finding['occurrences'][0]['raw'] == 'DATASET'


def test_terminology_code_regions_do_not_create_cooccurrences():
    assert terms.find_inconsistencies('训练集。\n```\n训练数据集\n```', [entry()]) == []


def test_terminology_report_escapes_every_user_field():
    glossary = [dict(recommended_zh='<b>甲|</b>', variants_zh=['<b>甲|</b>', '乙'], en='<script>x</script>', note='[evil](https://invalid.example)', relation='style_preference', field='<img src=x>')]
    rendered = terms.render_markdown(terms.find_inconsistencies('<b>甲|</b> 与乙。', glossary))
    assert '<script>' not in rendered and '<img' not in rendered and '<b>' not in rendered
    assert '&lt;script&gt;' in rendered


def test_author_map_is_not_merged_with_default(tmp_path):
    loaded = terms.load_terms(write_map(tmp_path, {'custom': [entry(author_confirmed=True)]}))
    assert len(loaded) == 1
    assert loaded[0]['field'] == 'custom'


@pytest.mark.parametrize('study,text,expected', [
    ('theoretical', 'We define the assumptions and prove a theorem using a lemma.', ['Assumptions and definitions', 'Proof strategy']),
    ('qualitative', 'Interviews use purposive sampling and thematic coding with reflexivity.', ['Sampling and context', 'Data collection', 'Analysis approach']),
    ('review', 'We search the literature using eligibility criteria and synthesize evidence.', ['Source scope', 'Selection approach', 'Synthesis approach']),
    ('empirical', 'We describe study design, materials and procedure.', ['Study design', 'Materials or data', 'Procedure']),
])
def test_research_specific_method_clues(study, text, expected):
    result = structure.audit('method', text, research_type=study)
    assert set(expected).issubset(result['present'])
    assert not any('Training' in label or 'Architecture' in label or 'Ablation' in label for label in result['missing'])
    assert result['research_type'] == study
    assert result['coverage'] == 'keyword_clues_only'


def test_default_empirical_does_not_require_ablation_or_neural_networks():
    result = structure.audit('experiment', 'We collected observations and reported outcomes.')
    assert 'Ablation' not in result['missing']
    assert not any('Training' in label or 'network' in label.lower() for label in result['missing'])


def test_structure_keyword_positions_are_original():
    text = 'Synthetic.\n研究问题：采用访谈和主题分析。'
    result = structure.audit('method', text, research_type='qualitative')
    match = next(item for item in result['matches'] if item['raw'] == '访谈')
    assert match['line'] == 2
    assert text[match['start']:match['end']] == match['raw']


def test_structure_does_not_count_code_as_evidence():
    result = structure.audit('abstract', '本文讨论一个问题。\n```\nresults experiment dataset\n```')
    assert 'Evidence' in result['missing']


@pytest.mark.parametrize('text', ['[数据集]', '[主要指标]', '[结果与结论待实验完成后填写]', '[已确认完成的修改与真实位置]', '[实际用途与范围]', '[对应作者提供的署名与联系方式]', '[tool/version if required]', '【待填写结果】', '[TBD]', '[X–Y]'])
def test_real_project_placeholder_forms(text):
    assert structure.count_placeholders(text) == 1
    assert len(placeholder_spans(text)) == 1


@pytest.mark.parametrize('text', ['[12]', '[3, 5–7]', '[0.2, 0.8]', '[Title](guide.md)', '[dataset name](guide.md)', '[reference safety](https://example.invalid)'])
def test_citations_intervals_and_markdown_links_are_not_placeholders(text):
    assert structure.count_placeholders(text) == 0
    assert placeholder_spans(text) == []


def test_legacy_relation_provenance_survives_loading_and_scanning(tmp_path):
    value = entry()
    del value['relation']
    loaded = terms.load_terms(write_map(tmp_path, {'custom': [value]}))
    finding = terms.find_inconsistencies('训练集与训练数据集。', loaded)[0]
    assert finding['relation'] == 'style_preference'
    assert finding['relation_source'] == 'legacy_style_default'


def test_narrative_review_does_not_require_systematic_protocol():
    result = structure.audit('method', 'We explain the scope and source selection rationale and synthesize the literature.', research_type='review')
    assert 'Search strategy' not in result['missing']
    assert 'Eligibility criteria' not in result['missing']
    assert 'narrative' in result['study_note'].lower()


def test_confirmed_preference_detects_only_the_nonpreferred_form():
    finding = terms.find_inconsistencies('训练集。', [entry(author_confirmed=True, preferred='训练数据集')])[0]
    assert finding['recommended'] == '训练数据集'
    assert finding['requires_review']
    assert finding['type'] == 'author_preference_mismatch'


def test_glossary_duplicate_json_keys_are_rejected(tmp_path):
    path = tmp_path / 'duplicate.json'
    path.write_text('{"field": [], "field": []}')
    with pytest.raises(ValueError, match='Duplicate'):
        terms.load_terms(path)


def test_relation_source_type_error_is_explained(tmp_path):
    with pytest.raises(ValueError, match='relation_source'):
        terms.load_terms(write_map(tmp_path, {'custom': [entry(relation_source=[])]}))


@pytest.mark.parametrize('count', [3000, 10000])
def test_large_mixed_citations_and_placeholders_keep_counts_and_positions(count):
    unit = '[12] TODO \n'
    text = unit * count
    items = placeholder_spans(text)
    assert len(items) == count
    assert items[0] == {'start': 5, 'end': 9, 'raw': 'TODO', 'line': 1}
    assert items[-1] == {'start': (count - 1) * len(unit) + 5,
                          'end': (count - 1) * len(unit) + 9, 'raw': 'TODO', 'line': count}
    assert all(text[item['start']:item['end']] == item['raw'] for item in items)
