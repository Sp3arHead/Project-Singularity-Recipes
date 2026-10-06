#!/usr/bin/env python3
"""Checks every source a recipe uses: repos and refs, download URLs, and files
taken out of a downloaded repo (SQL files, logos, configs). Files inside release
zips cannot be checked without downloading them; their URL is checked instead.

Usage: python scripts/check-sources.py [recipe-id ...]   (needs git and PyYAML)
"""
import concurrent.futures as cf
import pathlib
import posixpath
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import yaml  # pip install pyyaml

BASE = pathlib.Path(__file__).resolve().parent.parent / 'recipes'
ids = sys.argv[1:] or sorted(p.name for p in BASE.iterdir() if (p / 'recipe.yaml').is_file())


def http_ok(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'sgl-recipe-check'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code == 405:  # some hosts refuse HEAD
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'sgl-recipe-check', 'Range': 'bytes=0-0'}), timeout=30) as r:
                    return r.status
            except urllib.error.HTTPError as e2:
                return e2.code
        return e.code
    except Exception as e:
        return str(e)[:60]


ref_cache = {}


def resolve_ref(src, ref):
    m = re.match(r'https://github\.com/([^/]+)/([^/]+?)/?$', src)
    owner, repo = m.group(1), m.group(2)
    key = (owner.lower(), repo.lower(), ref)
    if key in ref_cache:
        return ref_cache[key]
    out = subprocess.run(['git', 'ls-remote', '--symref', f'https://github.com/{owner}/{repo}'], capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        ref_cache[key] = (owner, repo, None, 'repo not found')
        return ref_cache[key]
    lines = out.stdout.splitlines()
    if ref is None:
        head = next((l for l in lines if l.startswith('ref:') and l.endswith('HEAD')), '')
        ref = head.split()[1].replace('refs/heads/', '') if head else None
    ok = any(l.split('\t')[-1] in (f'refs/heads/{ref}', f'refs/tags/{ref}') for l in lines if '\t' in l)
    ref_cache[key] = (owner, repo, ref, None if ok else f'ref {ref} not found')
    return ref_cache[key]


problems = []
for rid in ids:
    recipe = yaml.safe_load((BASE / rid / 'recipe.yaml').read_text(encoding='utf-8'))
    tasks = recipe['tasks']
    gh_dests = {}   # dest -> (owner, repo, ref, subpath)
    zip_dests = set()
    checks = []
    for i, t in enumerate(tasks, 1):
        a = t['action']
        if a == 'download_github':
            owner, repo, ref, err = resolve_ref(t['src'], t.get('ref'))
            if err:
                problems.append(f'{rid} #{i} {t["src"]}: {err}')
                continue
            dest = posixpath.normpath(t['dest'])
            gh_dests[dest] = (owner, repo, ref, t.get('subpath', ''))
            if t.get('subpath'):
                checks.append((i, f'subpath {t["subpath"]}', f'https://github.com/{owner}/{repo}/tree/{ref}/{urllib.parse.quote(t["subpath"])}'))
        elif a == 'download_file':
            checks.append((i, t['url'], t['url']))
            zip_dests.add(posixpath.normpath(t['path']))
        elif a == 'unzip':
            zip_dests.add(posixpath.normpath(t['dest']))
        # files taken out of a downloaded repo
        for key in ('src', 'file'):
            if a in ('move_path', 'copy_path', 'query_database', 'replace_string', 'load_vars') and isinstance(t.get(key), str):
                p = posixpath.normpath(t[key])
                for dest, (owner, repo, ref, sub) in gh_dests.items():
                    if p == dest or p.startswith(dest + '/'):
                        rel = posixpath.join(sub, p[len(dest) + 1:]) if p != dest else sub
                        if '.' in posixpath.basename(rel):  # a file, not a folder
                            url = f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/' + urllib.parse.quote(rel)
                        else:
                            url = f'https://github.com/{owner}/{repo}/tree/{ref}/' + urllib.parse.quote(rel)
                        checks.append((i, f'{a} {t[key]}', url))
                        break
    with cf.ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda c: (c, http_ok(c[2])), checks))
    bad = [(c, s) for c, s in results if s != 200]
    for (i, what, url), s in bad:
        problems.append(f'{rid} #{i} {what} -> {s} ({url})')
    print(f'{rid}: {len(gh_dests)} repos, {len(checks)} urls/files checked, {len(bad)} failed')

print('\n'.join(problems) if problems else 'ALL SOURCES OK')
