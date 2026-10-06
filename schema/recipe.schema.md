# Recipe format

A recipe is a YAML file the Project Singularity deployer runs to build a complete
server: it downloads resources, prepares the database and writes `server.cfg`.
The deployer is the recipe engine Project Singularity inherited from txAdmin
(engine version 3), so recipes written for txAdmin run unchanged.

Every recipe runs inside the folder it deploys to. Paths are relative to that
folder and cannot leave it (`..` is refused). There is no action that runs
shell commands.

## Header

```yaml
$engine: 3              # required engine version; 3 is current
$minFxVersion: 12913    # optional, lowest FXServer build the recipe needs
$onesync: on            # optional: off, legacy or on
$steamRequired: false   # optional, asks for a Steam Web API key when true

name: My Server         # shown in the deployer
version: 1.0.0
author: Someone
description: One sentence about the server.

variables:              # optional, extra {{variables}} with default values
  myVar: "value"

tasks:
  - action: ...
```

## Variables

`{{name}}` is replaced in `server.cfg` after all tasks have run, and in any file
a `replace_string` task with `mode: all_vars` touches.

| Variable | Value |
|---|---|
| `serverName` | Server name from the panel |
| `recipeName`, `recipeAuthor`, `recipeDescription` | From the header |
| `deploymentID` | Id of this deployment |
| `svLicense` | Cfx.re license key entered in the deployer |
| `maxClients` | Slots (48 unless the host forces a number) |
| `serverEndpoints` | The `endpoint_add_tcp` / `endpoint_add_udp` lines |
| `addPrincipalsMaster` | `add_principal` lines that make the master account an admin in game |
| `dbHost`, `dbPort`, `dbUsername`, `dbPassword`, `dbName` | Database entered in the deployer |
| `dbConnectionString` | `mysql://user:password@host/database?charset=utf8mb4` |

A recipe cannot declare variables with the database or license names above.

## Actions

| Action | Options | Timeout |
|---|---|---|
| `download_github` | `src` (repo URL), `ref` (branch or tag, default branch when left out), `subpath`, `dest` | 180 s |
| `download_file` | `url`, `path` | 180 s |
| `unzip` | `src`, `dest` | 180 s |
| `move_path` | `src`, `dest`, `overwrite` | 180 s |
| `copy_path` | `src`, `dest`, `overwrite` | 180 s |
| `remove_path` | `path` (missing paths are fine) | 15 s |
| `ensure_dir` | `path` | 15 s |
| `write_file` | `file`, `data`, `append` | 15 s |
| `replace_string` | `file` (one or a list), `mode` (`template`, `literal`, `all_vars`), `search`, `replace` | 15 s |
| `connect_database` | none; creates the database when it does not exist | 30 s |
| `query_database` | `file` or `query` | 90 s |
| `load_vars` | `src`, a JSON file whose keys become variables | 5 s |
| `waste_time` | `seconds`, e.g. to avoid GitHub rate limits | 300 s |

Any task can set its own `timeoutSeconds`.

## What a finished deployment needs

After the last task the deployer checks that a `resources` folder and a
`server.cfg` exist, then replaces the variables in `server.cfg`. A recipe that
uses a `*_database` action asks for the database in the deployer.

## Example

```yaml
$engine: 3
$onesync: on
name: Minimal Server
version: 1.0.0
author: Example
description: The default Cfx.re resources and a server.cfg.

tasks:
  - action: download_github
    src: https://github.com/citizenfx/cfx-server-data
    ref: master
    subpath: resources
    dest: ./resources

  - action: write_file
    file: ./server.cfg
    data: |
      {{serverEndpoints}}
      sv_maxclients {{maxClients}}
      sv_licenseKey "{{svLicense}}"
      sv_hostname "{{serverName}}"
      ensure mapmanager
      ensure chat
      ensure spawnmanager
      ensure sessionmanager
      {{addPrincipalsMaster}}
```
