# Project Singularity Recipes

Complete server presets for [Project Singularity](https://github.com/Sp3arHead/Project-Singularity).
A recipe builds a whole FiveM server in one run: framework, jobs, inventory,
phone, voice, maps, the database and a ready `server.cfg`.

| Recipe | Framework | Tasks | Folder |
|---|---|---|---|
| ESX Legacy | `es_extended` | 21 | [recipes/esx-legacy](recipes/esx-legacy) |
| QBCore | `qb-core` | 89 | [recipes/qbcore](recipes/qbcore) |
| Qbox | `qbx_core` (QBCore compatible) | 120 | [recipes/qbox](recipes/qbox) |
| ox_core | `ox_core` | 39 | [recipes/ox-core](recipes/ox-core) |

The list the panel reads is [index.yaml](index.yaml).

## What every recipe needs

- An empty folder to deploy into.
- A MariaDB or MySQL server; the deployer creates the database when it does not exist.
- A Cfx.re license key from [portal.cfx.re](https://portal.cfx.re).
- OneSync, which the recipes switch on.

## Based on the official recipes

Each recipe starts from the framework team's own recipe, so the resources and
their order are the ones the framework expects. The changes for Project
Singularity are marked with `Singularity:` in the recipe file:

- Our own `server.cfg` per recipe (in the recipe's folder), with notes on the
  panel and without settings that only existed in txAdmin.
- No second connection queue: the panel has its own (*Players → Queue*), so
  QBCore's `connectqueue` is left out and Qbox's built-in queue is switched off.

Resources are downloaded from their latest releases or main branches at the
time of the run, exactly like the official recipes.

## Writing or changing a recipe

1. Put the recipe in `recipes/<id>/recipe.yaml`, with its `server.cfg` and a `README.md` next to it.
2. Add it to `index.yaml`.
3. Check it: `python scripts/check-sources.py <id>` looks up every repository,
   branch, download and file the recipe uses.
4. Open a pull request.

The format and all actions are described in [schema/recipe.schema.md](schema/recipe.schema.md).

## License

The recipes are released under the terms in [LICENSE.md](LICENSE.md). The
resources they download keep their own licenses.
