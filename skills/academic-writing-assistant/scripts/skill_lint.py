#!/usr/bin/env python3
"""Developer validation for the repository or an exported Skill package.

PyYAML is an optional development dependency used here for real, safe YAML
parsing. The four manuscript checks require only the Python standard library.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

REQUIRED_REFERENCES = [
    'task-router.md', 'field-adapter.md', 'writing-workflows.md', 'style-guide-zh.md',
    'style-guide-en.md', 'output-templates.md', 'quality-checklist.md', 'examples.md',
    'fidelity-protocol.md', 'citation-safety.md', 'reviewer-response.md',
    'terminology.md', 'submission-package.md', 'latex-and-formats.md', 'consistency-pass.md',
    'workflow-context.md', 'research-types.md', 'policy-sources.md',
]
REQUIRED_SCRIPTS = ['fidelity_check.py', 'manuscript_audit.py', 'terminology_checker.py',
                    'structure_checker.py', 'skill_lint.py', 'fidelity_parser.py', 'prose_utils.py',
                    'check_utils.py', 'section_audit.py', 'term_consistency_check.py']
PRIVATE_PARTS = {'.git', '.internal', '.local', '.venv', '__pycache__', '.pytest_cache',
                 'private', 'node_modules', '.idea', '.vscode'}
PUBLIC_DIRS = {'skills', 'assets', 'docs', 'examples', 'evals', 'tests', 'scripts',
               '.github', '.codex-plugin'}



def safe_ancestors(path):
    """Reject directory aliases before any file contents are opened."""
    try:
        return all(stat.S_ISDIR(parent.lstat().st_mode) for parent in path.absolute().parents)
    except OSError:
        return False


def safe_public_file(path, root):
    """A public filename must identify one regular inode inside a real root."""
    try:
        info = path.lstat()
        return (stat.S_ISREG(info.st_mode) and info.st_nlink == 1
                and safe_ancestors(path)
                and path.resolve().is_relative_to(root.resolve()))
    except (OSError, RuntimeError):
        return False


def read_public_text(path, root):
    if not safe_public_file(path, root):
        raise ValueError('Unsafe public file; refusing to read its contents.')
    before = path.lstat()
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    with os.fdopen(os.open(path, flags), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
            raise ValueError('Public file changed before reading; retry after inspecting it.')
        return stream.read().decode('utf-8-sig')

def validate_frontmatter(text, directory_name):
    try:
        import yaml
    except ImportError:
        return ['YAML validation needs the optional development dependency PyYAML; install requirements-dev.txt.']
    match = re.match(r'\A\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        return ['SKILL.md needs a delimited YAML frontmatter mapping.']

    class UniqueSafeLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError('Frontmatter keys must be unique strings.')
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        tokens = list(yaml.scan(match.group(1)))
        if any(isinstance(t, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken)) for t in tokens):
            return ['Use explicit frontmatter values; YAML anchors/aliases are not supported by this validator.']
        data = yaml.load(match.group(1), Loader=UniqueSafeLoader)
    except (yaml.YAMLError, ValueError, TypeError, RecursionError):
        return ['Invalid YAML frontmatter, or nesting exceeds parser limits.']
    if not isinstance(data, dict):
        return ['Frontmatter must be a mapping.']
    failures = []
    name = data.get('name')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        failures.append('name must be 1–64 lowercase letters/digits with single internal hyphens.')
    if name != directory_name:
        failures.append('name must match the Skill directory name.')
    description = data.get('description')
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        failures.append('description must be a nonempty string of at most 1024 characters.')
    for key in ('license', 'compatibility', 'allowed-tools'):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            failures.append(key + ' must be a nonempty string.')
    if isinstance(data.get('compatibility'), str) and len(data['compatibility']) > 500:
        failures.append('compatibility must be at most 500 characters.')
    if 'metadata' in data and (not isinstance(data['metadata'], dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in data['metadata'].items())):
        failures.append('metadata must map strings to strings.')
    allowed = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
    if set(data) - allowed:
        failures.append('Host-specific frontmatter fields need an explicit compatibility decision: ' + ', '.join(sorted(set(data) - allowed)))
    return failures


def public_files(root):
    """Do not open ignored/private content just to lint public documentation."""
    root = root.resolve()
    paths = []
    if (root / '.git').exists():
        result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                                capture_output=True, check=True)
        paths = [root / name.decode('utf-8') for name in result.stdout.split(b'\0') if name]
    else:
        # Exported archives have no Git index. Restrict traversal to public trees.
        for path in root.iterdir() if root.is_dir() else []:
            if path.is_symlink():
                continue
            if path.is_file() and not path.name.startswith('.env'):
                paths.append(path)
            elif path.is_dir() and path.name in PUBLIC_DIRS:
                paths.extend(p for p in path.rglob('*') if p.is_file())
    return sorted(set(p for p in paths if p.is_file() and not p.is_symlink()
                      and not any(part in PRIVATE_PARTS for part in p.relative_to(root).parts)
                      and not any(part.startswith('.env') for part in p.relative_to(root).parts)))


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))


def validate_logo(text, root):
    parser = Images(); parser.feed(text)
    images = parser.images + [{'src': src, 'alt': alt} for alt, src in re.findall(r'!\[([^\]]*)\]\(([^ )]+)\)', text)]
    for item in images:
        if item.get('src', '').removeprefix('./') == 'assets/logo/revision-compass.svg' and item.get('alt', '').strip():
            if (root / 'assets/logo/revision-compass.svg').is_file() and (root / 'assets/logo/revision-compass.png').is_file():
                return []
    return ['README must reference the original Revision Compass SVG with meaningful alt text, and both logo assets must exist.']


def find_promises(text):
    """Narrow publication-promise lint, not truth/citation validation.

    Rejection statements and explicitly marked counterexamples are data. All
    accepted prose still needs semantic review; keyword absence proves nothing.
    """
    findings = []
    marker = re.compile(r'guaranteed (?:acceptance|publication)|保证录用|绕过检测|规避检测', re.I)
    negation = re.compile(r'禁止|不(?:得|能|接受|保证|提供)|拒绝|反例|错误示例|bad (?:example|revision)|counterexample|do not|never|not (?:offer|promise|guarantee)|no guarantee', re.I)
    for number, line in enumerate(text.splitlines(), 1):
        if marker.search(line) and not negation.search(line):
            findings.append(f'line {number}: possible publication/detection promise; inspect context')
    return findings


def validate_manifest(path, root):
    if not safe_public_file(path, root):
        return ['Unsafe plugin manifest path.']
    try:
        data = json.loads(read_public_text(path, root))
    except (OSError, UnicodeError, ValueError, RecursionError):
        return ['Cannot parse plugin.json, or nesting exceeds parser limits.']
    if not isinstance(data, dict):
        return ['plugin.json must be an object.']
    failures = []
    for key in ('name', 'version', 'description', 'license', 'skills'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            failures.append('plugin.json ' + key + ' must be a nonempty string.')
    if data.get('name') != 'academic-writing-assistant':
        failures.append('plugin.json name must remain academic-writing-assistant.')
    version = data.get('version')
    if not isinstance(version, str) or not re.fullmatch(r'(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', version):
        failures.append('plugin version must use semantic versioning.')
    resource = data.get('skills')
    if isinstance(resource, str):
        path = Path(resource)
        if path.is_absolute() or '..' in path.parts or not (root / path).resolve().is_relative_to(root) or not (root / path).is_dir():
            failures.append('plugin skills must resolve to a directory inside the plugin root.')
    author = data.get('author')
    if not isinstance(author, dict) or not isinstance(author.get('name'), str) or not author.get('name', '').strip():
        failures.append('The compatibility plugin manifest requires author with a nonempty string name.')
    interface = data.get('interface')
    if not isinstance(interface, dict):
        return failures + ['plugin.json interface must be an object.']
    for key in ('displayName', 'shortDescription', 'longDescription', 'developerName', 'category', 'brandColor'):
        if key in interface and not isinstance(interface[key], str):
            failures.append('plugin interface.' + key + ' must be a string.')
    for key in ('logo', 'composerIcon'):
        value = interface.get(key)
        if value != './assets/logo/revision-compass.png':
            failures.append('plugin.json interface.' + key + ' must preserve the original PNG logo.')
    prompts = interface.get('defaultPrompt', [])
    if not isinstance(prompts, (str, list)) or isinstance(prompts, list) and not all(isinstance(x, str) for x in prompts):
        failures.append('plugin defaultPrompt must be a string or list of strings.')
    return failures


def validate_package_resources(skill):
    """Validate only the explicit public inventory and its transitive links.

    Never enumerate arbitrary local resource folders or read a link target
    before checking that it stays inside this package and its public manifest.
    """
    def safe_resource(target):
        return (safe_public_file(target, skill)
                and not any(part.startswith('.') or part in PRIVATE_PARTS
                            for part in target.resolve().relative_to(skill).parts))

    path = skill / 'package-manifest.json'
    if not safe_resource(path):
        return ['Missing or unsafe package-manifest.json.']
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate package manifest key.')
            result[key] = value
        return result
    try:
        data = json.loads(read_public_text(path, skill), object_pairs_hook=unique)
    except (OSError, UnicodeError, ValueError, RecursionError):
        return ['Cannot parse package-manifest.json, or nesting exceeds parser limits.']
    if (not isinstance(data, dict) or set(data) != {'format', 'skill', 'files'}
            or type(data.get('format')) is not int or data['format'] != 1
            or data.get('skill') != skill.name or not isinstance(data.get('files'), list)
            or not all(isinstance(name, str) for name in data['files'])):
        return ['Invalid package manifest structure.']
    names = data['files']
    failures = []
    if not 1 <= len(names) <= 2048 or len({name.casefold() for name in names}) != len(names):
        failures.append('Duplicate or case-colliding package manifest paths.')
    prefixes = {}
    for name in names:
        parts = PurePosixPath(name).parts
        for depth in range(1, len(parts) + 1):
            prefix = '/'.join(parts[:depth])
            if prefixes.setdefault(prefix.casefold(), prefix) != prefix:
                failures.append('Case-colliding package path ancestor: ' + name)
    required = {'SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'package-manifest.json',
                'agents/openai.yaml', 'assets/terminology-map.zh-en.json', 'assets/venue-policies.json'}
    required.update('references/' + name for name in REQUIRED_REFERENCES)
    required.update('scripts/' + name for name in REQUIRED_SCRIPTS)
    failures.extend('Package manifest omits required resource: ' + name for name in sorted(required - set(names)))
    safe_names = set()
    for name in names:
        relative = PurePosixPath(name)
        target = skill / name
        if (not package_resource_name(name) or relative.is_absolute() or str(relative) != name
                or any(part.startswith('.') or part in PRIVATE_PARTS for part in relative.parts)
                or not safe_resource(target)):
            failures.append('Missing or unsafe manifest resource: ' + name)
        else:
            safe_names.add(name)
    # Markdown links in fenced examples are data, not package dependencies.
    for name in sorted(safe_names):
        if not name.endswith('.md'):
            continue
        source = skill / name
        visible, fence = [], None
        for line in read_public_text(source, skill).splitlines():
            opening = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
            if fence:
                if opening and opening[1][0] == fence[0] and len(opening[1]) >= len(fence) and not opening[2].strip():
                    fence = None
                continue
            if opening:
                fence = opening[1]; continue
            visible.append(line)
        links, unsupported = markdown_resource_links('\n'.join(visible))
        if unsupported:
            failures.append(name + ': unsupported or incomplete Markdown link; resource coverage incomplete.')
        for raw in links:
            parsed = urlsplit(raw)
            if parsed.scheme in {'https', 'http', 'mailto'} or raw.startswith('#'):
                continue
            target = source.parent / unquote(parsed.path)
            if parsed.scheme or parsed.netloc or not target.resolve().is_relative_to(skill):
                failures.append(name + ': unsafe local resource link: ' + raw)
                continue
            relative = target.resolve().relative_to(skill).as_posix()
            if relative not in safe_names or not safe_resource(target):
                failures.append(name + ': local resource absent from package inventory: ' + raw)
    return failures


def package_resource_name(name):
    """Match the installer's portable public-resource path contract."""
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*(?:/[A-Za-z0-9][A-Za-z0-9_.-]*)*', name):
        return False
    path = PurePosixPath(name)
    reserved = {'con', 'prn', 'aux', 'nul', *('com' + str(i) for i in range(1, 10)),
                *('lpt' + str(i) for i in range(1, 10))}
    if any(part in PRIVATE_PARTS or part.endswith('.') or part.split('.')[0].lower() in reserved for part in path.parts):
        return False
    if name in {'SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'package-manifest.json', 'agents/openai.yaml'}:
        return True
    return len(path.parts) >= 2 and {'references': '.md', 'scripts': '.py', 'assets': '.json'}.get(path.parts[0]) == path.suffix


def markdown_resource_links(text):
    """Bounded inline/reference destination parsing, without rendering content."""
    text = re.sub(r'(`+)(.*?)\1', lambda m: ' ' * len(m[0]), text, flags=re.S)
    links, unsupported = [], False
    # Reference definitions can be used later, or with collapsed/shortcut links.
    for match in re.finditer(r'(?m)^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]*>|\S+)', text):
        links.append(match[1][1:-1] if match[1].startswith('<') else match[1])
    for match in re.finditer(r'(?<!\\)\[[^\]\n]*\]\(', text):
        i = match.end()
        while i < len(text) and text[i].isspace():
            i += 1
        start = i
        if i < len(text) and text[i] == '<':
            end = text.find('>', i + 1)
            if end < 0 or '\n' in text[i:end]:
                unsupported = True; continue
            destination = text[i + 1:end]; i = end + 1
        else:
            depth = 0
            while i < len(text):
                if text[i] == '\\' and i + 1 < len(text):
                    i += 2; continue
                if text[i].isspace() or text[i] == ')' and depth == 0:
                    break
                if text[i] == '(':
                    depth += 1
                elif text[i] == ')':
                    depth -= 1
                i += 1
            destination = text[start:i]
            if depth:
                unsupported = True; continue
        while i < len(text) and text[i].isspace():
            i += 1
        if i < len(text) and text[i] in {'"', "'", '('}:
            closer = ')' if text[i] == '(' else text[i]
            i += 1
            while i < len(text) and text[i] != closer:
                i += 2 if text[i] == '\\' else 1
            i += 1
            while i < len(text) and text[i].isspace():
                i += 1
        if i >= len(text) or text[i] != ')' or not destination:
            unsupported = True; continue
        links.append(re.sub(r'\\([!"#$%&\'()*+,\-./:;<=>?@\[\]\\^_`{|}~])', r'\1', destination))
    return links, unsupported


def check(root, package=False):
    root = Path(root).absolute()
    if not root.is_dir() or root.is_symlink() or not safe_ancestors(root):
        return ['Validation root is missing, not a directory, or has a linked ancestor.']
    root = root.resolve()
    skill = root if package else root / 'skills/academic-writing-assistant'
    failures = []
    path = skill / 'SKILL.md'
    if not path.is_file():
        return ['Missing SKILL.md in the selected Skill root.']
    if not safe_public_file(path, root):
        return ['Unsafe SKILL.md path; refusing to read outside the selected package.']
    text = read_public_text(path, root)
    failures.extend(validate_frontmatter(text, skill.name))
    failures.extend(validate_package_resources(skill))
    def safe_file(target):
        return safe_public_file(target, skill)
    for name in REQUIRED_REFERENCES:
        if not safe_file(skill / 'references' / name):
            failures.append('Missing reference: ' + name)
    for name in REQUIRED_SCRIPTS:
        if not safe_file(skill / 'scripts' / name):
            failures.append('Missing script: ' + name)
    for relative in re.findall(r'(?:references|assets|scripts)/[A-Za-z0-9_.\-/]+\.(?:md|json|py)', text):
        target = skill / relative
        if '..' in Path(relative).parts or not safe_file(target):
            failures.append('Missing or unsafe Skill resource: ' + relative)
    if package:
        for name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            if not safe_file(skill / name):
                failures.append('Standalone package missing ' + name)
        return failures
    for filename, other in [('README.md', 'README_EN.md'), ('README_EN.md', 'README.md')]:
        path = root / filename
        if not path.is_file():
            failures.append('Missing ' + filename); continue
        if not safe_public_file(path, root):
            failures.append(filename + ': unsafe path.'); continue
        readme = read_public_text(path, root)
        failures.extend(filename + ': ' + error for error in validate_logo(readme, root))
        if not re.search(r'\[[^\]]+\]\(' + re.escape(other) + r'\)', readme):
            failures.append(filename + ': missing language switch.')
        for pattern, label in [(r'安装|[Ii]nstall', 'installation'), (r'示例|[Ee]xample', 'examples'),
                               (r'诚信|[Ii]ntegrity', 'integrity'), (r'许可|[Ll]icense', 'license'),
                               (r'路线图|ROADMAP|[Rr]oadmap', 'roadmap'), (r'贡献|CONTRIBUTING|[Cc]ontribut', 'contributing')]:
            if not re.search(pattern, readme):
                failures.append(filename + ': missing ' + label + ' guidance or link.')
    failures.extend(validate_manifest(root / '.codex-plugin/plugin.json', root))
    for path in public_files(root):
        relative = path.relative_to(root)
        # User-facing promises only; examples/evals/tests are verified separately
        # for source facts, not by banning their deliberately unsafe inputs.
        if path.suffix == '.md' and (path.name.startswith('README') or relative.parts[0] == 'docs'):
            if not safe_public_file(path, root):
                failures.append(str(relative) + ': unsafe public file path.'); continue
            failures.extend(str(relative) + ': ' + issue for issue in find_promises(read_public_text(path, root)))
    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--package', action='store_true', help='Validate a standalone Skill directory, without repository-only files.')
    args = parser.parse_args(argv)
    try:
        failures = check(Path(args.root), args.package)
    except (OSError, UnicodeError, ValueError, subprocess.SubprocessError) as exc:
        sys.stderr.write('Validation input error: ' + str(exc).splitlines()[0] + '\n')
        return 2
    print('# Skill Lint Report\n\nStatus: ' + ('FAIL' if failures else 'PASS'))
    for failure in failures:
        print('- ' + failure)
    if not failures:
        print('\nConfigured structural checks passed; semantic/behavioral review is separate.')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
