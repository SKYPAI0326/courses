"""Source-only HTML preparation and dependency fingerprints; never writes PDFs."""
from __future__ import annotations

import base64
import copy
import hashlib
import importlib.metadata
import json
import mimetypes
import re
import unicodedata
from html import escape
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class PipelineError(ValueError):
    pass


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise PipelineError(f'Workspace-relative path required: {relative}')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise PipelineError(f'Path escapes workspace: {relative}')
    return path


def normalize_text(text: str) -> str:
    # Preserve punctuation, numbers, CJK and code; only layout whitespace is removed.
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', text))


def validate_recipe(root: Path, recipe: dict) -> dict:
    allowed = {'schema_version', 'artifact_id', 'course', 'output', 'profile', 'sources',
               'font_files', 'exclude', 'expand', 'dependencies', 'remote_assets', 'notes',
               'source_courses','paper_fallbacks'}
    if not isinstance(recipe, dict) or set(recipe) - allowed:
        raise PipelineError('Unknown recipe fields or non-object recipe')
    if recipe.get('schema_version') != 1 or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', recipe.get('artifact_id', '')):
        raise PipelineError('schema_version=1 and a stable artifact_id are required')
    course = recipe.get('course', '')
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', course):
        raise PipelineError('Invalid course slug')
    output = inside(root, recipe.get('output', ''))
    library = inside(root, f'output/pdf/{course}')
    if output.parent != library or output.suffix.lower() != '.pdf':
        raise PipelineError('Output must be output/pdf/<course>/<filename>.pdf')
    inside(root, recipe.get('profile', ''))
    for field in ('font_files','dependencies','exclude','expand'):
        if not isinstance(recipe.get(field,[]),list): raise PipelineError(f'{field} must be an array')
    if not isinstance(recipe.get('remote_assets',{}),dict): raise PipelineError('remote_assets must be an object')
    if not isinstance(recipe.get('sources'), list) or not recipe['sources']:
        raise PipelineError('An ordered source list is required')
    seen = set()
    source_courses=recipe.get('source_courses',[course])
    if not isinstance(source_courses,list) or not source_courses or not all(isinstance(c,str) and re.fullmatch(r'[a-z0-9][a-z0-9_-]*',c) for c in source_courses):
        raise PipelineError('Explicit source_courses slugs are required for a cross-course book')
    for item in recipe.get('paper_fallbacks',[]):
        if not isinstance(item,dict) or set(item)!={'selector','mode','reason'} or item['mode']!='print-source-values' or not item['selector'] or not item['reason']:
            raise PipelineError('Paper fallbacks must explicitly print existing native source values')
    for source in recipe['sources']:
        if not isinstance(source,dict): raise PipelineError('Source entries must be objects')
        if set(source) - {'path', 'selectors', 'source_url', 'static_content_confirmed'}:
            raise PipelineError('Unknown source fields')
        path = inside(root, source.get('path', ''))
        if path.suffix.lower() != '.html' or not any(path.is_relative_to(root / c) for c in source_courses):
            raise PipelineError('Source HTML must belong to the selected course')
        if path in seen:
            raise PipelineError('Duplicate source page')
        seen.add(path)
        if not isinstance(source.get('selectors'),list) or not source['selectors'] or not all(isinstance(s, str) for s in source['selectors']):
            raise PipelineError('Explicit content selectors are required')
        if source.get('static_content_confirmed') is not True:
            raise PipelineError('Static teaching content must be inspected and confirmed')
        if urlsplit(source.get('source_url', '')).scheme not in {'https', 'http'}:
            raise PipelineError('A confirmed public source_url is required for link mapping')
    for field in ('exclude', 'expand'):
        for item in recipe.get(field, []):
            if not isinstance(item,dict) or set(item) != {'selector', 'reason'} or not item['selector'] or not item['reason']:
                raise PipelineError(f'{field} requires selector and reason')
    return recipe


def load_recipe(root: Path, path: Path) -> dict:
    return validate_recipe(root.resolve(), json.loads(path.read_text(encoding='utf-8')))


def environment() -> dict:
    result = {}
    for package in ('beautifulsoup4', 'playwright', 'pypdf'):
        try:
            result[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            result[package] = None
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            executable = Path(p.chromium.executable_path)
            result['chromium'] = {'path': str(executable), 'sha256': sha(executable) if executable.exists() else None}
    except ImportError:
        result['chromium'] = None
    return result


def prepare(root: Path, recipe: dict) -> dict:
    from bs4 import BeautifulSoup
    root = root.resolve()
    validate_recipe(root, recipe)
    deps, transformations, links, units = {}, [], [], []
    output = inside(root, recipe['output'])
    source_paths = [inside(root, s['path']) for s in recipe['sources']]

    def add(path: Path, kind='asset', external=False):
        path = path.resolve()
        if path == output:
            return
        if kind=='linked-material' and path.suffix.lower()=='.pdf' and path.is_relative_to(root/'output/pdf'):
            # Managed handouts are output references, not automatic byte inputs.
            return
        if not path.is_file():
            raise PipelineError(f'Missing dependency: {path}')
        if not external and not path.is_relative_to(root):
            raise PipelineError(f'Dependency escapes workspace: {path}')
        key = str(path) if external else path.relative_to(root).as_posix()
        deps[key] = {'path': key, 'sha256': sha(path), 'bytes': path.stat().st_size, 'kind': kind}

    def resource(ref: str, base: Path) -> Path | None:
        parsed = urlsplit(ref)
        if ref.startswith(('data:', '#')) or not parsed.path:
            return None
        if parsed.scheme or parsed.netloc:
            pin = recipe.get('remote_assets', {}).get(ref)
            if not pin or set(pin) != {'path', 'sha256'}:
                raise PipelineError(f'External render asset must be pinned locally: {ref}')
            path = inside(root, pin['path'])
            add(path, 'pinned-remote')
            if sha(path) != pin['sha256']:
                raise PipelineError(f'Pinned asset hash changed: {ref}')
            return path
        rel = unquote(parsed.path)
        path = (root / rel.lstrip('/')) if rel.startswith('/') else (base.parent / rel)
        add(path)
        return path.resolve()

    def data_uri(path: Path) -> str:
        return 'data:' + (mimetypes.guess_type(path.name)[0] or 'application/octet-stream') + ';base64,' + base64.b64encode(path.read_bytes()).decode()

    css_stack = set()
    def css_content(text: str, base: Path) -> str:
        def imported(match):
            ref = match.group(1) or match.group(2)
            path = resource(ref, base)
            if path is None or path in css_stack:
                raise PipelineError(f'Unsupported/cyclic CSS import: {ref}')
            css_stack.add(path)
            value = css_content(path.read_text(encoding='utf-8'), path)
            css_stack.remove(path)
            return value
        text = re.sub(r'@import\s+(?:url\(\s*[\"\x27]?([^\"\x27\s)]+)[\"\x27]?\s*\)|[\"\x27]([^\"\x27]+)[\"\x27])\s*;', imported, text)
        if '@import' in text:
            raise PipelineError('Unsupported conditional CSS import; resolve it explicitly')
        def asset(match):
            ref = match.group(1).strip().strip('\"\x27')
            path = resource(ref, base)
            return 'url("' + data_uri(path) + '")' if path else match.group(0)
        return re.sub(r'url\(([^)]+)\)', asset, text)

    profile_path = inside(root, recipe['profile'])
    add(profile_path, 'profile')
    profile = css_content(profile_path.read_text(encoding='utf-8'), profile_path)
    font_css = []
    for i, filename in enumerate(recipe.get('font_files', [])):
        path = Path(filename) if Path(filename).is_absolute() else inside(root, filename)
        add(path, 'font', external=path.is_absolute() and not path.resolve().is_relative_to(root))
        font_css.append(f'@font-face{{font-family:"CoursePDF{i}";src:url("{data_uri(path)}")}}')
    if font_css:
        profile += '\nbody,body *{font-family:CoursePDF0,sans-serif!important}'
    for filename in recipe.get('dependencies', []):
        add(inside(root, filename), 'declared')
    for path in sorted((root / 'course-manager/src').glob('pdf_*.py')):
        add(path, 'engine')
    cli = root / 'course-manager/scripts/pdf_pipeline.py'
    if cli.exists(): add(cli, 'engine')

    id_maps, soups, source_styles = [], [], []
    for i, source in enumerate(recipe['sources']):
        path = source_paths[i]
        add(path, 'html')
        document = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        selected = []
        for selector in source['selectors']:
            matches = document.select(selector)
            if not matches:
                raise PipelineError(f'No content matched {source["path"]}: {selector}')
            selected.extend(matches)
        if len({id(x) for x in selected}) != len(selected) or any(any(p is other for p in node.parents) for node in selected for other in selected if node is not other):
            raise PipelineError('Duplicate or overlapping content selectors')
        # Keep document order, even when selectors are written in a different order.
        order = {id(node): j for j, node in enumerate(document.find_all(True))}
        selected.sort(key=lambda n: order[id(n)])
        fragment = BeautifulSoup(''.join(str(n) for n in selected), 'html.parser')
        if fragment.select('canvas, iframe, video, audio, object, embed'):
            raise PipelineError('Necessary interactive/media content needs a confirmed source fallback')
        for item in recipe.get('paper_fallbacks',[]):
            for node in fragment.select(item['selector']):
                if node.name not in {'input','textarea','select'}:
                    raise PipelineError('Native paper fallback selector matched non-form content')
                if node.name=='input' and node.get('type','text')=='password':
                    raise PipelineError('Password field has no paper fallback: '+source['path'])
                if node.name=='input' and node.get('type')=='hidden':
                    transformations.append({'source':source['path'],'action':'omit-nonvisible-form-parameter',**item})
                    node.decompose(); continue
                values=[o.get_text() for o in node.select('option')] if node.name=='select' else [node.get_text() or node.get('value') or node.get('placeholder','')]
                replacement=fragment.new_tag('pre');replacement['class']=['pdf-native-source-values']
                if node.get('id'): replacement['id']=node['id']
                replacement.string='\n'.join(values)
                transformations.append({'source':source['path'],'action':'print-native-source-values',
                                        'element':node.name,'values':values,**item})
                node.replace_with(replacement)
        for node in fragment.select('input'):
            label=node.find_parent('label')
            if label is None and node.get('id'):
                label=fragment.find('label',attrs={'for':node['id']})
            if node.get('type') not in {'radio','checkbox'} or label is None or not normalize_text(label.get_text()):
                raise PipelineError('Native input needs a confirmed existing paper fallback: '+source['path'])
            transformations.append({'source':source['path'],'action':'remove-choice-widget','type':node.get('type'),'label':label.get_text()})
            node.decompose()
        if fragment.select('select,textarea'):
            raise PipelineError('Native form content needs a confirmed source fallback')
        for item in recipe.get('exclude', []):
            for node in fragment.select(item['selector']):
                if node.name not in {'button', 'nav'} and not (node.name == 'div' and node.get('role') == 'navigation'):
                    raise PipelineError('UI exclusions may only remove buttons or navigation containers')
                if node.select('p,pre,code,table,img,h1,h2,h3,details,input,select,textarea'):
                    raise PipelineError('UI exclusion contains teaching material')
                transformations.append({'source':source['path'], 'action':'exclude-ui', **item, 'text':node.get_text()})
                node.decompose()
        for item in recipe.get('expand', []):
            for node in fragment.select(item['selector']):
                node.attrs.pop('hidden', None)
                node['style'] = re.sub(r'(display\s*:\s*none|visibility\s*:\s*hidden)\s*!?important?\s*;?', '', node.get('style',''), flags=re.I)
                node['style'] = re.sub(r'(display\s*:\s*none|visibility\s*:\s*hidden)\s*;?', '', node.get('style',''), flags=re.I)
                transformations.append({'source':source['path'], 'action':'expand-existing', **item})
        for node in fragment.select('[hidden], [style]'):
            if node.has_attr('hidden') or re.search(r'(display\s*:\s*none|visibility\s*:\s*hidden)',node.get('style',''),re.I):
                raise PipelineError(f'Hidden teaching node requires an explicit expansion: {source["path"]}')
        for details in fragment.select('details'):
            details['open'] = ''
            transformations.append({'source':source['path'],'action':'open-details','text':details.get_text()})
        for node in fragment.select('script, style'):
            node.decompose()
        for script in document.select('script[src]'):
            resource(script['src'], path)
        styles = [css_content(s.get_text(), path) for s in document.select('style')]
        for link in document.select('link[rel~=stylesheet][href]'):
            ref = link['href']
            if urlsplit(ref).netloc == 'fonts.googleapis.com' and font_css:
                transformations.append({'source':source['path'],'action':'replace-web-fonts','url':ref})
                continue
            stylesheet = resource(ref, path)
            if stylesheet: styles.append(css_content(stylesheet.read_text(encoding='utf-8'), stylesheet))
        ids = [n['id'] for n in fragment.select('[id]')]
        if len(set(ids)) != len(ids): raise PipelineError(f'Duplicate source ids: {source["path"]}')
        mapping = {original:f'unit-{i}--{original}' for original in ids}
        for node in fragment.select('[id]'): node['id'] = mapping[node['id']]
        for node in fragment.find_all(True):
            for attr in ('for','aria-labelledby','aria-describedby'):
                if node.has_attr(attr): node[attr]=' '.join(mapping.get(x,x) for x in node[attr].split())
            for attr,value in list(node.attrs.items()):
                if isinstance(value,str):
                    for old,new in mapping.items():
                        value=value.replace('url(#'+old+')','url(#'+new+')')
                    if node.name=='use' and attr in {'href','xlink:href'} and value.startswith('#'):
                        if value[1:] not in mapping: raise PipelineError('SVG use target is outside selected content')
                        value='#'+mapping[value[1:]]
                    node[attr]=value
            for attr in list(node.attrs):
                if attr.lower().startswith('on'): del node[attr]
            if node.has_attr('srcset'):
                raise PipelineError('Resolve responsive srcset to a confirmed existing image before conversion')
            for attr in ('src', 'poster'):
                if node.has_attr(attr):
                    target = resource(node[attr],path)
                    if target: node[attr] = data_uri(target)
            if node.has_attr('style'): node['style'] = css_content(node['style'],path)
        expected = fragment.get_text(separator='\n',strip=False)
        if not normalize_text(expected): raise PipelineError('No teaching text selected')
        id_maps.append(mapping); soups.append(fragment); source_styles.append(styles)
        units.append({'source':source['path'],'selectors':source['selectors'],'text':expected,
                      'title':document.title.get_text() if document.title else (fragment.h1.get_text() if fragment.h1 else output.stem),
                      'tables':len(fragment.select('table')),'images':len(fragment.select('img')),
                      'code_blocks':len(fragment.select('pre'))})

    rendered = []
    for i, (source, fragment, styles) in enumerate(zip(recipe['sources'],soups,source_styles)):
        path = source_paths[i]
        for node in fragment.select('a[href]'):
            original = node['href']
            parsed = urlsplit(original)
            if parsed.scheme in {'javascript','file'}: raise PipelineError(f'Unsupported teaching link: {original}')
            absolute = urljoin(source['source_url'], original)
            mapped, target_index, fragment_id = absolute, None, unquote(parsed.fragment)
            for j, other in enumerate(recipe['sources']):
                if urlsplit(absolute)._replace(fragment='') == urlsplit(other['source_url'])._replace(fragment=''):
                    target_index=j; break
            if not parsed.scheme and not parsed.netloc and parsed.path:
                local = (root / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else path.parent / unquote(parsed.path)
                local = local.resolve()
                if not local.is_relative_to(root):
                    if not (local.is_relative_to(root.parent) and local.suffix.lower()=='.html' and local.is_file()):
                        raise PipelineError(f'Link escapes workspace: {original}')
                if local in source_paths: target_index = source_paths.index(local)
                elif local != output:
                    if not local.exists(): raise PipelineError(f'Missing linked asset/page: {original}')
                    if local.is_file() and local.suffix.lower() != '.html': add(local,'linked-material')
            if original.startswith('#'): target_index=i
            if target_index is not None:
                if fragment_id:
                    if fragment_id not in id_maps[target_index]: raise PipelineError(f'Anchor outside selected teaching content: {absolute}')
                    mapped = '#' + id_maps[target_index][fragment_id]
                else: mapped = f'#unit-{target_index}'
            node['href'] = mapped
            links.append({'source':source['path'],'original':original,'mapped':mapped,
                          'validation':'local-anchor' if mapped.startswith('#') else 'external-not-live-checked'})
        scoped = []
        for style in styles:
            def rewrite_selectors(match):
                selector=match.group(1)
                for old,new in id_maps[i].items():
                    selector=re.sub(r'#'+re.escape(old)+r'(?![\w-])','#'+new,selector)
                return selector+'{'
            style=re.sub(r'([^{}]+)\{',rewrite_selectors,style)
            for old,new in id_maps[i].items(): style=style.replace('url(#'+old+')','url(#'+new+')')
            style=re.sub(r'(?<![\w-])(?::root|html|body)(?=\s*[,\{>:.#\[])', ':scope',style)
            scoped.append(f'@scope (#unit-{i}){{{style}}}')
        rendered.append(f'<style>{"".join(scoped)}</style><section class="pdf-unit" id="unit-{i}">{fragment}</section>')
    title=units[0]['title'] if len(units)==1 else output.stem
    html = '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>'+escape(title)+'</title><style>'+''.join(font_css)+profile+'</style></head><body>'+''.join(rendered)+'</body></html>'
    dependency_list = sorted(deps.values(), key=lambda x:x['path'])
    env = environment()
    fingerprint = canonical_hash({'recipe':recipe,'dependencies':dependency_list,'environment':env})
    return {'html':html,'expected_text':'\n'.join(u['text'] for u in units),'units':units,
            'dependencies':dependency_list,'transformations':transformations,'links':links,
            'environment':env,'fingerprint':fingerprint,'recipe':copy.deepcopy(recipe)}
