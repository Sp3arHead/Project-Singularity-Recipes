#!/usr/bin/env python3
"""Builds recipes/<id>/recipe.yaml from the definitions below and checks them.

Usage:
    python scripts/build_recipes.py            # build and check every recipe
    python scripts/build_recipes.py qbox-full  # only some

Every package is downloaded once into scripts/.cache. The build reads the real
archives, so the paths a recipe moves are the paths inside the zip. Then it
checks each recipe as deployed:

- every dependency and @include of every resource is installed or provided
- every SQL file the recipe runs exists
- every ui_page a resource names exists in the package
- server.cfg starts every installed resource (by name or by its [folder])

Packages come as GitHub branch archives (github.com/<o>/<r>/archive/...) or
release zips, never through api.github.com, whose 60 requests an hour for
servers without a GitHub token a large recipe would run out of.
"""
import json
import os
import pathlib
import re
import sys
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / 'scripts' / '.cache'
RAW = 'https://raw.githubusercontent.com/Sp3arHead/Project-Singularity-Recipes/main/recipes'

# Started by FXServer itself (system resources) or by the panel
BUILTIN = {'chat', 'sessionmanager', 'hardcap', 'yarn', 'webpack', 'monitor', 'rconlog'}


# =============================================================================
#  Packages
# =============================================================================
def archive(owner, repo, branch):
    return {'url': f'https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip', 'src': f'{owner}/{repo}@{branch}'}


def release(owner, repo, file=None, tag=None):
    where = f'download/{tag}' if tag else 'latest/download'
    return {'url': f'https://github.com/{owner}/{repo}/releases/{where}/{file or repo}.zip', 'src': f'{owner}/{repo} release {tag or "latest"}'}


PKG = {
    # Cfx.re
    'cfx': archive('citizenfx', 'cfx-server-data', 'master'),
    # Overextended
    'oxmysql': release('overextended', 'oxmysql'),
    'ox_lib': release('overextended', 'ox_lib'),
    'ox_target': release('overextended', 'ox_target'),
    'ox_inventory': release('overextended', 'ox_inventory'),
    'ox_doorlock': release('overextended', 'ox_doorlock'),
    'ox_fuel': release('overextended', 'ox_fuel'),
    'ox_core': release('overextended', 'ox_core'),
    'ox_banking': release('overextended', 'ox_banking'),
    'ox_commands': archive('overextended', 'ox_commands', 'main'),
    # ESX
    'esx_core': archive('esx-framework', 'esx_core', 'main'),
    'esx_addons': archive('esx-framework', 'ESX-Legacy-Addons', 'main'),
    'esx_seasonal': archive('esx-framework', 'ESX-Legacy-Seasonal', 'main'),
    # Common third party
    'pma-voice': archive('AvarianKnight', 'pma-voice', 'main'),
    'bob74_ipl': archive('Bob74', 'bob74_ipl', 'master'),
    'illenium-appearance': release('iLLeniumStudios', 'illenium-appearance'),
    'screenshot-basic': release('project-error', 'screenshot-basic', tag='1.0.1'),
    'screencapture': release('itschip', 'screencapture'),
    'npwd': release('project-error', 'npwd'),
    'npwd-3.16.0': release('project-error', 'npwd', tag='3.16.0'),
    'sd-phone': release('Samuels-Development', 'sd-phone'),
    'sd-phone-props': archive('Samuels-Development', 'sd-phone-props', 'main'),
    'pe-basicloading': archive('DokaDoka', 'pe-basicloading', 'ox'),
    # Qbox and the resources it is built around
    'Renewed-Banking': release('Renewed-Scripts', 'Renewed-Banking'),
    'Renewed-Weathersync': release('Renewed-Scripts', 'Renewed-Weathersync'),
    'scully_emotemenu': archive('Scullyy', 'scully_emotemenu', 'main'),
    'xt-prison': release('xT-Development', 'xt-prison'),
    'vehiclehandler': release('QuantumMalice', 'vehiclehandler'),
    'mana_audio': release('Manason', 'mana_audio'),
    'MugShotBase64': archive('BaziForYou', 'MugShotBase64', 'main'),
    'ultra-voltlab': archive('ultrahacx', 'ultra-voltlab', 'main'),
    'loadscreen': release('D4isDAVID', 'loadscreen'),
    'pillbox': archive('Lorenc95', 'pillbox', 'main'),
    'qbx_invimages': archive('Qbox-project', 'qbx_invimages', 'main'),
}

# Every QBCore resource the QBCore team publishes (qbcore-fivem), including the
# forks it maintains. connectqueue is left out: the panel has its own queue.
QB_RESOURCES = [
    'qb-adminmenu', 'qb-ambulancejob', 'qb-apartments', 'qb-banking', 'qb-bankrobbery', 'qb-busjob',
    'qb-cityhall', 'qb-clothing', 'qb-core', 'qb-crafting', 'qb-crypto', 'qb-diving', 'qb-doorlock',
    'qb-drugs', 'qb-fuel', 'qb-garages', 'qb-garbagejob', 'qb-hotdogjob', 'qb-houserobbery', 'qb-houses',
    'qb-hud', 'qb-input', 'qb-interior', 'qb-inventory', 'qb-jewelery', 'qb-lapraces', 'qb-loading',
    'qb-management', 'qb-mechanicjob', 'qb-menu', 'qb-minigames', 'qb-multicharacter', 'qb-newsjob',
    'qb-pawnshop', 'qb-phone', 'qb-policejob', 'qb-prison', 'qb-radialmenu', 'qb-radio', 'qb-recyclejob',
    'qb-scoreboard', 'qb-scrapyard', 'qb-shops', 'qb-smallresources', 'qb-spawn', 'qb-storerobbery',
    'qb-streetraces', 'qb-target', 'qb-taxijob', 'qb-towjob', 'qb-truckerjob', 'qb-truckrobbery',
    'qb-vehiclekeys', 'qb-vehiclesales', 'qb-vehicleshop', 'qb-vineyard', 'qb-weapons', 'qb-weathersync',
    'qb-weed',
]
QB_STANDALONE = ['PolyZone', 'menuv', 'progressbar', 'interact-sound', 'safecracker', 'bob74_ipl']
QB_MAPS = ['dealer_map', 'hospital_map']
for name in QB_RESOURCES + QB_STANDALONE + QB_MAPS + ['prison_map']:
    branch = 'master' if name in ('PolyZone', 'menuv', 'interact-sound', 'bob74_ipl') else 'main'
    PKG['qb:' + name] = archive('qbcore-fivem', name, branch)

# Every Qbox resource (Qbox-project), including the forks it maintains. Left
# out: qbx_db_backup and qbx_grafana_map (dashboard tools), qbxsql (tooling).
QBX_RELEASE = [
    'qbx_core', 'qbx_adminmenu', 'qbx_binoculars', 'qbx_density', 'qbx_divegear', 'qbx_diving',
    'qbx_fireworks', 'qbx_garages', 'qbx_hud', 'qbx_management', 'qbx_radialmenu', 'qbx_smallresources',
    'qbx_spawn', 'qbx_truckrobbery', 'qbx_vehiclekeys', 'qbx_vehicles', 'mhacking', 'mm_radio',
    'npwd_qbx_garages', 'npwd_qbx_mail',
]
QBX_SOURCE = [
    'qbx_ambulancejob', 'qbx_bankrobbery', 'qbx_busjob', 'qbx_carwash', 'qbx_chat_theme', 'qbx_cityhall',
    'qbx_drugs', 'qbx_garbagejob', 'qbx_houserobbery', 'qbx_jewelery', 'qbx_lapraces', 'qbx_mechanicjob',
    'qbx_medical', 'qbx_newsjob', 'qbx_npwd', 'qbx_pawnshop', 'qbx_police', 'qbx_properties',
    'qbx_recyclejob', 'qbx_scoreboard', 'qbx_scrapyard', 'qbx_seatbelt', 'qbx_storerobbery',
    'qbx_streetraces', 'qbx_taxijob', 'qbx_towjob', 'qbx_truckerjob', 'qbx_vehiclesales', 'qbx_vehicleshop',
    'qbx_vineyard', 'qbx_weed', 'qbx_idcard', 'qbx_customs', 'safecracker',
]
for name in QBX_RELEASE:
    PKG['qbx:' + name] = release('Qbox-project', name)
for name in QBX_SOURCE:
    PKG['qbx:' + name] = archive('Qbox-project', name, 'main')


# =============================================================================
#  Recipe building blocks
# =============================================================================
class Recipe:
    def __init__(self, rid, name, description, framework, kind, onesync='on', min_fx=None):
        self.rid, self.name, self.description = rid, name, description
        self.framework, self.kind, self.onesync, self.min_fx = framework, kind, onesync, min_fx
        self.sections = []      # (title, [task dict])
        self.installs = []      # (pkg, inner, dest)
        self.sql = []           # deployed paths of SQL files
        self.not_started = []   # folders installed on purpose without starting them
        self.requires = ['MariaDB or MySQL', 'a Cfx.re license key', 'OneSync (on)']
        self.notes = []         # shown in the README

    def section(self, title):
        self.sections.append((title, []))

    def task(self, **t):
        self.sections[-1][1].append(t)

    def install(self, pkg, *takes):
        """takes: (inner path inside the package's top folder, deploy dest)."""
        tmp = f'./tmp/{safe(pkg)}'
        self.task(action='download_file', url=PKG[pkg]['url'], path=f'{tmp}.zip')
        self.task(action='unzip', src=f'{tmp}.zip', dest=tmp)
        for inner, dest in takes:
            self.installs.append((pkg, inner, dest))
            self.task(action='move_path', src=f'{tmp}/{{TOP:{pkg}}}{("/" + inner) if inner else ""}', dest=dest)

    def query(self, path):
        self.sql.append(path)
        self.task(action='query_database', file=path)


def safe(s):
    return re.sub(r'[^A-Za-z0-9_-]', '_', s)


# =============================================================================
#  Package cache and inspection
# =============================================================================
def fetch(pkg):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (safe(pkg) + '.zip')
    if not path.exists():
        req = urllib.request.Request(PKG[pkg]['url'], headers={'User-Agent': 'sgl-recipes'})
        with urllib.request.urlopen(req, timeout=600) as r:
            data = r.read()
        if not data.startswith(b'PK'):
            raise RuntimeError(f'{pkg}: {PKG[pkg]["url"]} did not return a zip file')
        path.write_bytes(data)
    try:
        return zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        path.unlink()
        raise RuntimeError(f'{pkg}: the cached download was damaged and has been removed, run again')


def top_folder(z):
    """The single top folder of an archive, or '' when files lie in the root."""
    tops = {n.split('/')[0] for n in z.namelist()}
    roots = [n for n in z.namelist() if '/' not in n]
    if len(tops) == 1 and not roots:
        return tops.pop()
    return ''


def strip_comments(lua):
    lua = re.sub(r'--\[(=*)\[.*?\]\1\]', '', lua, flags=re.S)
    return re.sub(r'--[^\n]*', '', lua)


def manifest_info(text):
    t = strip_comments(text)
    # `name '@scope/package'` is an npm style name, not an include
    t = re.sub(r'''^\s*name\s*\(?\s*["'][^"']*["']''', '', t, flags=re.M)
    deps, provides = [], []
    for m in re.finditer(r'\bdependenc(?:y|ies)\s*(\{[^}]*\}|["\'][^"\']+["\'])', t):
        deps += re.findall(r'["\']([^"\']+)["\']', m.group(1))
    for m in re.finditer(r'\bprovides?\s*(\{[^}]*\}|["\'][^"\']+["\'])', t):
        provides += re.findall(r'["\']([^"\']+)["\']', m.group(1))
    includes = re.findall(r'["\']@([A-Za-z0-9_\-]+)/', t)
    ui = re.findall(r'\bui_page\s*\(?\s*["\']([^"\']+)["\']', t)
    return {
        'deps': [d for d in deps if not d.startswith('/')],
        'includes': sorted(set(includes)),
        'provides': provides,
        'ui': [u for u in ui if not u.startswith(('http://', 'https://', 'nui://'))],
    }


# =============================================================================
#  Build and check
# =============================================================================
def build(recipe):
    tops = {}
    deployed = {}   # deployed resource folder -> (pkg, folder inside zip)
    problems = []

    for pkg, inner, dest in recipe.installs:
        z = fetch(pkg)
        top = tops.setdefault(pkg, top_folder(z))
        base = '/'.join(p for p in (top, inner) if p)
        names = z.namelist()
        if base and not any(n == base or n == base + '/' or n.startswith(base + '/') for n in names):
            problems.append(f'{pkg}: "{base}" is not in the package')
            continue
        # every resource below base, mapped to where it lands
        for n in names:
            b = n.rsplit('/', 1)[-1]
            if b not in ('fxmanifest.lua', '__resource.lua'):
                continue
            folder = n[: -len(b)].rstrip('/')
            if base and not (folder == base or folder.startswith(base + '/')):
                continue
            rel = folder[len(base):].lstrip('/') if base else folder
            target = dest.rstrip('/') + (('/' + rel) if rel else '')
            deployed[target] = (pkg, folder, n)

    # names and what they provide
    resources = {}
    for target, (pkg, folder, mpath) in deployed.items():
        name = target.rsplit('/', 1)[-1]
        info = manifest_info(fetch(pkg).read(mpath).decode('utf-8', 'replace'))
        resources[name] = {**info, 'target': target, 'pkg': pkg, 'folder': folder}
    available = set(resources) | BUILTIN
    for r in resources.values():
        available |= set(r['provides'])

    # Soft dependencies: exports of other resources called from Lua without
    # declaring them. Reported, not failed; some are guarded at runtime.
    exp = re.compile(r'''exports\s*(?:\[\s*["']([A-Za-z0-9_\-]+)["']\s*\]|\.([A-Za-z_][A-Za-z0-9_]*)\s*:)''')
    state = re.compile(r'''GetResourceState\(\s*["']([A-Za-z0-9_\-]+)["']''')
    notes = []
    for name, r in sorted(resources.items()):
        z = fetch(r['pkg'])
        pre = r['folder'] + '/' if r['folder'] else ''
        used, guarded = set(), set()
        for n in z.namelist():
            if n.startswith(pre) and n.endswith('.lua'):
                t = z.read(n).decode('utf-8', 'replace')
                used |= {a or b for a, b in exp.findall(t)}
                guarded |= set(state.findall(t))
        for u in sorted(used - available - {name} - guarded):
            notes.append(f'{name} calls exports of "{u}", which is not installed')

    for name, r in sorted(resources.items()):
        for d in sorted(set(r['deps']) | set(r['includes'])):
            if d not in available and d != name:
                problems.append(f'{name}: needs "{d}", which is not installed')
        files = set(fetch(r['pkg']).namelist())
        for ui in r['ui']:
            if '/'.join(x for x in (r['folder'], ui) if x) not in files:
                problems.append(f'{name}: ui_page "{ui}" is not in the package (needs a build)')

    # SQL files: found through the install that put them there
    for path in recipe.sql:
        p = path[2:] if path.startswith('./') else path
        hit = False
        for pkg, inner, dest in recipe.installs:
            d = dest[2:] if dest.startswith('./') else dest
            zbase = '/'.join(x for x in (tops[pkg], inner) if x)
            if p == d:
                rel = ''
            elif p.startswith(d + '/'):
                rel = p[len(d) + 1:]
            else:
                continue
            hit = '/'.join(x for x in (zbase, rel) if x) in set(fetch(pkg).namelist())
            break
        if not hit:
            problems.append(f'SQL file {path} is not in any installed package')

    # server.cfg starts everything
    cfg = (ROOT / 'recipes' / recipe.rid / 'server.cfg').read_text(encoding='utf-8')
    started = set()
    for m in re.finditer(r'^\s*(?:ensure|start)\s+(\S+)', cfg, flags=re.M):
        started.add(m.group(1))
    for name, r in sorted(resources.items()):
        parts = r['target'].split('/')
        if name in started or any(p in started for p in parts if p.startswith('[')):
            continue
        if any(r['target'].startswith(f + '/') for f in recipe.not_started):
            continue
        problems.append(f'{name}: installed but server.cfg does not start it')
    for s in sorted(started):
        if s.startswith('['):
            if not any(f'/{s}/' in r['target'] + '/' for r in resources.values()):
                problems.append(f'server.cfg starts {s}, but no resource is in that folder')
        elif s not in available:
            problems.append(f'server.cfg starts {s}, which is not installed')

    write(recipe, tops)
    write_readme(recipe, resources)
    return resources, problems, notes


def yaml_str(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if re.fullmatch(r'[A-Za-z0-9_./:\-\[\]{}@ ]+', s) and not s.startswith(('[', '{', '@')) and ': ' not in s:
        return s
    return json.dumps(s, ensure_ascii=False)


def write_readme(recipe, resources):
    cfg = (ROOT / 'recipes' / recipe.rid / 'server.cfg').read_text(encoding='utf-8')
    build = re.search(r'sv_enforceGameBuild\s+(\d+)', cfg)
    groups = {}
    for name, r in resources.items():
        folder = '/'.join(p for p in r['target'].split('/')[2:-1]) or 'resources'
        groups.setdefault(folder, []).append(name)
    lines = [
        f'# {recipe.name}', '',
        recipe.description, '',
        f'**Resources:** {len(resources)}  ', f'**Tasks:** {sum(len(t) for _, t in recipe.sections)}', '',
        '## Requirements', '',
    ]
    req = list(recipe.requires)
    if build:
        req.append(f'game build {build.group(1)} (set in server.cfg)')
    if recipe.min_fx:
        req.append(f'FXServer {recipe.min_fx} or newer')
    lines += [f'- {x}' for x in req] + ['', '## Included', '']
    for folder in sorted(groups):
        lines.append(f'- `{folder}`: ' + ', '.join(f'`{n}`' for n in sorted(groups[folder], key=str.lower)))
    lines += ['', '## Database', '']
    lines += [f'- `{p[2:]}`' for p in recipe.sql]
    if recipe.notes:
        lines += ['', '## Notes', ''] + [f'- {n}' for n in recipe.notes]
    lines += ['', 'This folder is built by `scripts/build_recipes.py`; change the definitions there.', '']
    (ROOT / 'recipes' / recipe.rid / 'README.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')


def write(recipe, tops):
    out = [
        f'# Project Singularity recipe: {recipe.name}',
        '# Built by scripts/build_recipes.py from the definitions there; edit those, not this file.',
        '$engine: 3',
    ]
    if recipe.min_fx:
        out.append(f'$minFxVersion: {recipe.min_fx}')
    out += [
        f'$onesync: {recipe.onesync}',
        f'name: {yaml_str(recipe.name)}',
        'version: 1.0.0',
        'author: Project Singularity',
        f'description: {yaml_str(recipe.description)}',
        '',
        'tasks:',
    ]
    for title, tasks in recipe.sections:
        if not tasks:
            continue
        out.append(f'  ## {title}')
        for t in tasks:
            t = dict(t)
            for k in ('src',):
                if isinstance(t.get(k), str):
                    t[k] = re.sub(r'\{TOP:([^}]+)\}', lambda m: tops[m.group(1)], t[k]).replace('//', '/').rstrip('/')
            keys = list(t)
            out.append(f'  - action: {t["action"]}')
            for k in keys:
                if k == 'action':
                    continue
                v = t[k]
                if isinstance(v, list):
                    out.append(f'    {k}:')
                    out += [f'      - {yaml_str(x)}' for x in v]
                else:
                    out.append(f'    {k}: {yaml_str(v)}')
        out.append('')
    path = ROOT / 'recipes' / recipe.rid / 'recipe.yaml'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(out).rstrip() + '\n', encoding='utf-8', newline='\n')


# =============================================================================
#  Recipes
# =============================================================================
def base(r, gamemode=False):
    r.section('server.cfg')
    r.task(action='download_file', url=f'{RAW}/{r.rid}/server.cfg', path='./server.cfg')
    r.section('Cfx.re resources')
    takes = [('resources/[managers]/mapmanager', './resources/[cfx]/mapmanager'),
             ('resources/[managers]/spawnmanager', './resources/[cfx]/spawnmanager'),
             ('resources/[system]/baseevents', './resources/[cfx]/baseevents')]
    if gamemode:
        takes.append(('resources/[gamemodes]/basic-gamemode', './resources/[cfx]/basic-gamemode'))
    r.install('cfx', *takes)
    r.section('Database')
    r.task(action='connect_database')


def rel_resource(r, pkg, dest_folder, name=None):
    """A release zip whose top folder is the resource."""
    r.install(pkg, ('', f'{dest_folder}/{name or pkg}'))


def finish(r):
    r.section('Cleanup')
    r.task(action='remove_path', path='./tmp')


RECIPES = {}


def recipe(fn):
    r = fn()
    RECIPES[r.rid] = r
    return fn


# ---------------------------------------------------------------- ESX
@recipe
def esx_minimal():
    r = Recipe('esx-minimal', 'ESX Legacy (minimal)',
               'The ESX core with character registration and the skin menu, nothing else.', 'esx', 'minimal')
    base(r)
    r.section('ESX core')
    rel_resource(r, 'oxmysql', './resources/[standalone]')
    r.install('esx_core', *[(f'[core]/{n}', f'./resources/[core]/{n}') for n in
                            ('es_extended', 'esx_lib', 'esx_identity', 'esx_skin', 'skinchanger')])
    r.section('Database tables')
    # es_extended.sql creates and switches to its own database "es_extended";
    # the tables have to go into the database chosen in the deployer
    r.task(action='replace_string', file='./resources/[core]/es_extended/es_extended.sql',
           search='`es_extended`', replace='`{{dbName}}`')
    r.query('./resources/[core]/es_extended/es_extended.sql')
    r.query('./resources/[core]/esx_identity/esx_identity.sql')
    r.query('./resources/[core]/esx_skin/esx_skin.sql')
    finish(r)
    return r


@recipe
def esx_full():
    r = Recipe('esx-full', 'ESX Legacy (full)',
               'Every ESX Legacy resource: the whole core, all addons and the seasonal content, with phone, voice and the ox library.',
               'esx', 'full')
    base(r)
    r.section('Libraries')
    for p in ('oxmysql', 'ox_lib'):
        rel_resource(r, p, './resources/[standalone]')
    r.section('ESX core, all addons, seasonal content')
    r.install('esx_core', ('[core]', './resources/[core]'), ('[SQL]/legacy.sql', './tmp/esx-legacy.sql'))
    r.install('esx_addons', ('[esx_addons]', './resources/[esx_addons]'))
    # Seasonal content (snow, Christmas …) is installed but not started; see server.cfg
    r.install('esx_seasonal', ('', './resources/[esx_seasonal]'))
    r.not_started.append('./resources/[esx_seasonal]')
    r.section('Phone, voice, map')
    r.install('sd-phone', ('', './resources/[standalone]/sd-phone'))
    r.install('sd-phone-props', ('', './resources/[standalone]/sd-phone-props'))
    r.install('pma-voice', ('', './resources/[standalone]/pma-voice'))
    r.install('bob74_ipl', ('', './resources/[standalone]/bob74_ipl'))
    r.install('screenshot-basic', ('', './resources/[standalone]/screenshot-basic'))
    r.section('Database tables')
    r.query('./tmp/esx-legacy.sql')
    finish(r)
    return r


# ---------------------------------------------------------------- QBCore
@recipe
def qbcore_minimal():
    r = Recipe('qbcore-minimal', 'QBCore (minimal)',
               'qb-core with character selection, spawn, the starter apartment, inventory and the clothing menu, nothing else.', 'qbcore', 'minimal')
    base(r, gamemode=True)
    r.section('Libraries')
    rel_resource(r, 'oxmysql', './resources/[standalone]')
    r.install('qb:PolyZone', ('', './resources/[standalone]/PolyZone'))
    r.section('QBCore')
    # qb-multicharacter hands out the starter items through qb-inventory (which
    # needs qb-weapons), and the starter apartment's door menus use qb-menu
    for n in ('qb-core', 'qb-multicharacter', 'qb-spawn', 'qb-apartments', 'qb-interior', 'qb-clothing',
              'qb-weathersync', 'qb-inventory', 'qb-weapons', 'qb-menu'):
        r.install('qb:' + n, ('', f'./resources/[qb]/{n}'))
    r.section('Database tables')
    r.query('./resources/[qb]/qb-core/qbcore.sql')
    r.query('./resources/[qb]/qb-apartments/qb-apartments.sql')
    r.query('./resources/[qb]/qb-clothing/qb-clothing.sql')
    r.query('./resources/[qb]/qb-inventory/qb-inventory.sql')
    finish(r)
    return r


@recipe
def qbcore_full():
    r = Recipe('qbcore-full', 'QBCore (full)',
               'Every resource the QBCore team publishes: all jobs, robberies, housing, vehicles, phone, admin menu, maps and voice.',
               'qbcore', 'full')
    base(r, gamemode=True)
    r.section('Libraries and standalone resources')
    rel_resource(r, 'oxmysql', './resources/[standalone]')
    for n in QB_STANDALONE:
        r.install('qb:' + n, ('', f'./resources/[standalone]/{n}'))
    r.install('screenshot-basic', ('', './resources/[standalone]/screenshot-basic'))
    r.section('Voice')
    r.install('pma-voice', ('', './resources/[voice]/pma-voice'))
    r.section('Maps')
    for n in QB_MAPS:
        r.install('qb:' + n, ('', f'./resources/[defaultmaps]/{n}'))
    r.install('qb:prison_map', ('', './resources/[defaultmaps]/[prison_map]'))
    r.section('QBCore, every resource')
    for n in QB_RESOURCES:
        r.install('qb:' + n, ('', f'./resources/[qb]/{n}'))
    r.section('Database tables')
    for sql in ('qb-core/qbcore.sql', 'qb-apartments/qb-apartments.sql', 'qb-banking/banking.sql',
                'qb-clothing/qb-clothing.sql', 'qb-crypto/qb-crypto.sql', 'qb-drugs/qb-drugs.sql',
                'qb-garages/player_vehicles.sql', 'qb-houses/qb-houses.sql', 'qb-inventory/qb-inventory.sql',
                'qb-lapraces/qb-lapraces.sql', 'qb-phone/qb-phone.sql', 'qb-vehiclesales/qb-vehiclesales.sql',
                'qb-vehicleshop/vehshop.sql', 'qb-weed/qb-weed.sql'):
        r.query('./resources/[qb]/' + sql)
    finish(r)
    return r


# ---------------------------------------------------------------- Qbox
QBOX_ITEMS = 'https://raw.githubusercontent.com/Qbox-project/txAdminRecipe/main/items.lua'


@recipe
def qbox_minimal():
    r = Recipe('qbox-minimal', 'Qbox (minimal)',
               'qbx_core with its inventory, ID cards and the appearance menu, nothing else.', 'qbox', 'minimal')
    base(r)
    r.section('Overextended')
    for p in ('oxmysql', 'ox_lib', 'ox_inventory'):
        rel_resource(r, p, './resources/[ox]')
    # qbx_core gives new characters an ID card and a driver license; the items
    # have to exist in ox_inventory, which knows only its own items by default
    r.task(action='download_file', url=QBOX_ITEMS, path='./resources/[ox]/ox_inventory/data/items.lua')
    r.section('Qbox')
    rel_resource(r, 'qbx:qbx_core', './resources/[qbx]', 'qbx_core')
    r.install('qbx:qbx_idcard', ('', './resources/[qbx]/qbx_idcard'))
    r.install('MugShotBase64', ('MugShotBase64', './resources/[standalone]/MugShotBase64'))
    rel_resource(r, 'illenium-appearance', './resources/[standalone]')
    r.section('Database tables')
    r.query('./resources/[qbx]/qbx_core/qbx_core.sql')
    for sql in ('playerskins.sql', 'player_outfits.sql'):
        r.query('./resources/[standalone]/illenium-appearance/sql/' + sql)
    finish(r)
    return r


@recipe
def qbox_full():
    r = Recipe('qbox-full', 'Qbox (full)',
               'Every Qbox resource with the ox stack, Renewed banking and weather, NPWD phone, appearance, voice and maps.',
               'qbox', 'full')
    base(r)
    r.section('Overextended')
    for p in ('oxmysql', 'ox_lib', 'ox_target', 'ox_inventory', 'ox_doorlock', 'ox_fuel'):
        rel_resource(r, p, './resources/[ox]')
    r.task(action='download_file', url=QBOX_ITEMS, path='./resources/[ox]/ox_inventory/data/items.lua')
    r.install('qbx_invimages', ('images', './resources/[ox]/ox_inventory/web/images'))
    r.sections[-1][1][-1]['overwrite'] = True
    r.section('Qbox, every resource')
    for n in QBX_RELEASE:
        dest = './resources/[voice]' if n == 'mm_radio' else './resources/[npwd-apps]' if n.startswith('npwd_') else './resources/[qbx]'
        rel_resource(r, 'qbx:' + n, dest, n)
    for n in QBX_SOURCE:
        dest = './resources/[npwd]' if n == 'qbx_npwd' else './resources/[standalone]' if n == 'safecracker' else './resources/[qbx]'
        r.install('qbx:' + n, ('', f'{dest}/{n}'))
    r.section('Standalone resources Qbox works with')
    for p in ('illenium-appearance', 'Renewed-Banking', 'Renewed-Weathersync', 'xt-prison', 'vehiclehandler',
              'mana_audio', 'loadscreen', 'screencapture'):
        rel_resource(r, p, './resources/[standalone]')
    r.install('scully_emotemenu', ('', './resources/[standalone]/scully_emotemenu'))
    r.install('MugShotBase64', ('MugShotBase64', './resources/[standalone]/MugShotBase64'))
    r.install('ultra-voltlab', ('', './resources/[standalone]/ultra-voltlab'))
    r.install('bob74_ipl', ('', './resources/[standalone]/bob74_ipl'))
    r.section('Voice and phone')
    r.install('pma-voice', ('', './resources/[voice]/pma-voice'))
    rel_resource(r, 'npwd-3.16.0', './resources/[npwd]', 'npwd')
    r.task(action='move_path', src='./resources/[npwd]/qbx_npwd/config.json',
           dest='./resources/[npwd]/npwd/config.json', overwrite=True)
    r.section('Maps')
    r.install('pillbox', ('', './resources/[assets]/pillbox'))
    r.section('Database tables')
    for sql in ('[qbx]/qbx_core/qbx_core.sql', '[qbx]/qbx_vehicles/vehicles.sql',
                '[qbx]/qbx_vehiclesales/qbx_vehiclesales.sql', '[qbx]/qbx_vehicleshop/vehshop.sql',
                '[qbx]/qbx_weed/sql/qbx_weed.sql', '[qbx]/qbx_lapraces/qbx_lapraces.sql',
                '[qbx]/qbx_drugs/qbx_drugs.sql', '[qbx]/qbx_properties/property.sql',
                '[qbx]/qbx_properties/decorations.sql',
                '[standalone]/illenium-appearance/sql/playerskins.sql',
                '[standalone]/illenium-appearance/sql/player_outfits.sql',
                '[ox]/ox_doorlock/sql/ox_doorlock.sql', '[npwd]/npwd/import.sql'):
        r.query('./resources/' + sql)
    finish(r)
    return r


# ---------------------------------------------------------------- ox_core
def ox_sql(r):
    # install.sql creates and switches to its own database "overextended"
    r.task(action='replace_string', file='./resources/[ox]/ox_core/sql/install.sql',
           search='overextended', replace='{{dbName}}')
    r.query('./resources/[ox]/ox_core/sql/install.sql')


@recipe
def ox_minimal():
    r = Recipe('ox-minimal', 'ox_core (minimal)',
               'ox_core with its built-in character selection and the appearance menu, nothing else.', 'ox', 'minimal',
               min_fx=12913)
    base(r)
    r.section('Overextended')
    for p in ('oxmysql', 'ox_lib', 'ox_core'):
        rel_resource(r, p, './resources/[ox]')
    rel_resource(r, 'illenium-appearance', './resources/[standalone]')
    r.section('Database tables')
    ox_sql(r)
    for sql in ('playerskins.sql', 'player_outfits.sql'):
        r.query('./resources/[standalone]/illenium-appearance/sql/' + sql)
    finish(r)
    return r


@recipe
def ox_full():
    r = Recipe('ox-full', 'ox_core (full)',
               'Every maintained Overextended resource: inventory, banking, doorlock, target, fuel, commands, with appearance, NPWD phone, voice and maps.',
               'ox', 'full', min_fx=12913)
    base(r)
    r.section('Overextended, every maintained resource')
    for p in ('oxmysql', 'ox_lib', 'ox_core', 'ox_inventory', 'ox_target', 'ox_doorlock', 'ox_banking', 'ox_fuel'):
        rel_resource(r, p, './resources/[ox]')
    r.install('ox_commands', ('', './resources/[ox]/ox_commands'))
    r.section('Appearance, phone, voice, map, loading screen')
    rel_resource(r, 'illenium-appearance', './resources/[standalone]')
    rel_resource(r, 'npwd', './resources/[standalone]')
    r.install('screenshot-basic', ('', './resources/[standalone]/screenshot-basic'))
    r.install('pma-voice', ('', './resources/[standalone]/pma-voice'))
    r.install('bob74_ipl', ('', './resources/[standalone]/bob74_ipl'))
    r.install('pe-basicloading', ('', './resources/[standalone]/pe-basicloading'))
    r.section('Database tables')
    ox_sql(r)
    for sql in ('[standalone]/illenium-appearance/sql/playerskins.sql',
                '[standalone]/illenium-appearance/sql/player_outfits.sql',
                '[ox]/ox_doorlock/sql/ox_doorlock.sql', '[standalone]/npwd/import.sql'):
        r.query('./resources/' + sql)
    finish(r)
    return r


# =============================================================================
#  Notes for the READMEs
# =============================================================================
PANEL_AUTO = ('The in-game menu of Project Singularity finds this framework on its own for its '
              'inventory and money tools (Master Actions -> Framework).')
PANEL_CUSTOM = ('The in-game menu of Project Singularity has no preset for this framework yet; its '
                'inventory and money tools need the custom framework event (Master Actions -> Framework).')
NOTES = {
    'esx-minimal': [
        'es_extended.sql creates its own database `es_extended`; the recipe points it at the database chosen in the deployer.',
        'ESX would take its language from a txAdmin setting; server.cfg sets `esx:locale` instead.',
        PANEL_AUTO,
    ],
    'esx-full': [
        'Everything in esx_core `[core]`, ESX-Legacy-Addons and ESX-Legacy-Seasonal.',
        'The seasonal content (`[esx_seasonal]`) is installed but not started; server.cfg shows how to start it.',
        'esx_adminmenu is included next to the in-game menu of Project Singularity.',
        'sd-phone comes from its own release; the ESX fork of it has none.',
        PANEL_AUTO,
    ],
    'qbcore-minimal': [
        'qb-multicharacter needs qb-spawn and qb-apartments, which need qb-interior, qb-clothing, qb-weathersync and PolyZone.',
        'qb-inventory (with qb-weapons) is included because qb-multicharacter hands out the starter items through it; qb-menu runs the starter apartment door menus.',
        'qb-target is not included; `UseTarget` is off in server.cfg.',
        PANEL_AUTO,
    ],
    'qbcore-full': [
        'Every resource the QBCore team publishes in qbcore-fivem, including the forks it maintains (PolyZone, menuv, interact-sound, bob74_ipl).',
        'connectqueue is left out: the panel has its own connection queue, two queues would fight over the free slots.',
        'qb-adminmenu is included next to the in-game menu of Project Singularity.',
        PANEL_AUTO,
    ],
    'qbox-minimal': [
        'qbx_core uses ox_inventory for all items and requires qbx_idcard (with MugShotBase64) when a character is created.',
        'ox_inventory gets the Qbox item list, so the starter ID card and driver license exist.',
        PANEL_CUSTOM,
    ],
    'qbox-full': [
        'Every Qbox resource in Qbox-project, including the forks it maintains (qbx_idcard, qbx_customs). Left out: qbx_db_backup and qbx_grafana_map (dashboard tools) and qbxsql (tooling).',
        "qbx_core's own queue is switched off (`qbx:enableQueue false`): the panel has its own connection queue.",
        'NPWD is pinned to 3.16.0, the version qbx_npwd is made for.',
        'qbx_adminmenu is included next to the in-game menu of Project Singularity.',
        PANEL_CUSTOM,
    ],
    'ox-minimal': [
        'ox_core brings its own character selection; illenium-appearance lets players shape their character.',
        'install.sql creates its own database `overextended`; the recipe points it at the database chosen in the deployer.',
        PANEL_CUSTOM,
    ],
    'ox-full': [
        'Every maintained Overextended resource. Left out: ox_property (needs pefcl and ox_appearance, which no longer exist), ox_police (unmaintained since 2023), ox_mdt, ox_vehicledealer and ox_identityapp (no release, would need a build), qtarget (replaced by ox_target).',
        'ox_inventory is set to the ox framework in server.cfg (`inventory:framework "ox"`); its default would be ESX.',
        PANEL_CUSTOM,
    ],
}
for rid, n in NOTES.items():
    RECIPES[rid].notes = n
for rid in ('ox-minimal', 'ox-full'):
    RECIPES[rid].requires = ['MariaDB 11.4 or newer', 'a Cfx.re license key', 'OneSync (on)']


# =============================================================================
if __name__ == '__main__':
    wanted = sys.argv[1:] or list(RECIPES)
    failed = False
    summary = []
    for rid in wanted:
        r = RECIPES[rid]
        resources, problems, notes = build(r)
        tasks = sum(len(t) for _, t in r.sections)
        summary.append({'id': rid, 'resources': len(resources), 'tasks': tasks})
        print(f'{rid}: {len(resources)} resources, {tasks} tasks, {len(problems)} problems')
        for p in problems:
            print('   - ' + p)
        for n in notes:
            print('   ~ ' + n)
        failed |= bool(problems)
    (ROOT / 'scripts' / '.cache' / 'summary.json').write_text(json.dumps(summary, indent=1))
    sys.exit(1 if failed else 0)
