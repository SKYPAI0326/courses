"""由控制器擷取原文、保留問題身分及組裝局部更正。"""
import copy
import re
from pathlib import Path

from src.course_improvement_loop import require, digest


def reading_blocks(task):
    text = Path(task['target']['path']).read_text(encoding='utf-8')
    require(not task['target'].get('sha256') or digest(task['target']['path']) == task['target']['sha256'], '引文來源版本已變動')
    return [{'id': f'p{i:04d}', 'text': m.group(0), 'length': len(m.group(0))} for i, m in enumerate(
        re.finditer(r'\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*', text), 1)]


def reference_schema(obj):
    return obj({'block': {'type': 'string'}, 'start': {'type': 'integer', 'minimum': 0},
                'end': {'type': 'integer', 'minimum': 1}})


def resolve_reference(task, ref):
    require(isinstance(ref, dict) and set(ref) == {'block', 'start', 'end'}, '引文位置欄位不符')
    blocks = {row['id']: row['text'] for row in reading_blocks(task)}
    require(ref['block'] in blocks, '引文段落不存在')
    text = blocks[ref['block']]
    require(type(ref['start']) is int and type(ref['end']) is int
            and 0 <= ref['start'] < ref['end'] <= len(text), '引文範圍越界')
    return text[ref['start']:ref['end']]


def hydrate_reading(task, answer):
    result = copy.deepcopy(answer)
    for row in result['reading_decision']['passages']:
        require('quote' not in row and 'support_quotes' not in row, '位置契約不可混入手抄引文')
        row['quote'] = resolve_reference(task, row.pop('quote_ref'))
        refs = row.pop('support_refs')
        require(isinstance(refs, list) and refs, '重述須有正文位置依據')
        row['support_quotes'] = [resolve_reference(task, ref) for ref in refs]
    return result


def clean_closed_references(evaluation):
    result = copy.deepcopy(evaluation)
    for grade in result['grades'].values():
        for collection in ('problems', 'questions'):
            known = {r['id']: r for r in result[collection]}
            require(all(key in known for key in grade[collection]), '評級引用未知問題ID')
            grade[collection] = [key for key in grade[collection] if known[key]['open']]
    return result


def merge_issue_updates(prior, evaluation):
    """既有身分由控制器保存；省略不表示關閉，改判仍由模型明示。"""
    result = copy.deepcopy(evaluation)
    for collection, identity in (('problems', 'core'), ('questions', 'required')):
        known = {r['id']: {k: v for k, v in r.items() if k != 'basis'} for r in prior[collection]}
        seen = set()
        for row in result[collection]:
            key = row['id']
            require(key not in seen, '問題更新ID重複')
            seen.add(key)
            if key in known:
                require(set(row) in ({'id', 'open'}, {'id', 'open', 'description', identity}), '問題更新欄位不符')
                for field in ('description', identity):
                    require(field not in row or row[field] == known[key][field], '不得變更控制器保存的問題身分')
                known[key]['open'] = row['open']
            else:
                require(set(row) == {'id', 'open', 'description', identity}, '新問題須提供完整定義')
                known[key] = row
        result[collection] = list(known.values())
    result = clean_closed_references(result)
    for collection in ('problems', 'questions'):
        referenced = {key for grade in result['grades'].values() for key in grade[collection]}
        required = {r['id'] for r in result[collection] if r['open'] and (collection == 'problems' or r['required'])}
        require(required <= referenced, '尚未解決的問題不得從評級引用消失')
    return result


def apply_report_patch(task, original, patch):
    require(isinstance(patch, dict) and set(patch) == {'replacements'}, '局部更正不可包含評級或問題紀錄')
    rows = patch['replacements']
    require(isinstance(rows, list) and rows, '局部更正不得空白')
    result = copy.deepcopy(original)
    passages = result['reading_decision']['passages']
    seen = set()
    for row in rows:
        require(set(row) == {'passage', 'quote_ref', 'support_refs'}, '局部更正欄位不符')
        index = row['passage']
        require(type(index) is int and 0 <= index < len(passages) and index not in seen, '更正段落索引錯誤或重複')
        seen.add(index)
        require(isinstance(row['support_refs'], list) and row['support_refs'], '更正須保留重述依據')
        if task.get('citation_contract') == 'locations-v1':
            passages[index]['quote_ref'] = row['quote_ref']
            passages[index]['support_refs'] = row['support_refs']
        else:
            passages[index]['quote'] = resolve_reference(task, row['quote_ref'])
            passages[index]['support_quotes'] = [resolve_reference(task, ref) for ref in row['support_refs']]
    if task.get('citation_contract') == 'locations-v1':
        result = hydrate_reading(task, result)
        result['evaluation'] = merge_issue_updates(task['current_evaluation'], result['evaluation'])
    else:
        result['evaluation'] = clean_closed_references(result['evaluation'])
    passages = result['reading_decision']['passages']
    result['documents']['report'] += '\n\n## 控制器組裝的引文更正\n\n' + '\n\n'.join(
        f'段落{index}：\n\n{passages[index]["quote"]}\n\n依據：' + '\n'.join(passages[index]['support_quotes'])
        for index in sorted(seen))
    return result
