# Project Singularity Recipes

Server presets for [Project Singularity](https://github.com/Sp3arHead/Project-Singularity).
A recipe builds a whole FiveM server in one run: framework, resources, the
database tables and a ready `server.cfg`.

Every framework comes in two kinds:

- **full**: every resource the framework team publishes (plus what those
  resources need), so the server starts with everything there is.
- **minimal**: as few resources as possible: the framework core, the database,
  and what it takes to create a character, shape it and spawn.

| Recipe | Resources | Tasks | Folder |
|---|---|---|---|
| ESX Legacy (full) | 64 | 40 | [recipes/esx-full](recipes/esx-full) |
| ESX Legacy (minimal) | 9 | 22 | [recipes/esx-minimal](recipes/esx-minimal) |
| QBCore (full) | 77 | 236 | [recipes/qbcore-full](recipes/qbcore-full) |
| QBCore (minimal) | 16 | 49 | [recipes/qbcore-minimal](recipes/qbcore-minimal) |
| Qbox (full) | 78 | 251 | [recipes/qbox-full](recipes/qbox-full) |
| Qbox (minimal) | 10 | 33 | [recipes/qbox-minimal](recipes/qbox-minimal) |
| ox_core (full) | 18 | 59 | [recipes/ox-full](recipes/ox-full) |
| ox_core (minimal) | 7 | 24 | [recipes/ox-minimal](recipes/ox-minimal) |

The list the panel reads is [index.yaml](index.yaml). Each folder has a README
with everything the recipe installs, its database tables and notes.

## What every recipe needs

- An empty folder to deploy into.
- A MariaDB or MySQL server (ox_core: MariaDB 11.4 or newer); the deployer
  creates the database when it does not exist.
- A Cfx.re license key from [portal.cfx.re](https://portal.cfx.re).
- OneSync, which the recipes switch on.

## How the recipes are built

The recipes are not copies of the framework teams' recipes. They are built by
[scripts/build_recipes.py](scripts/build_recipes.py) from the resource lists in
that file, and every build checks them against the real downloads:

- every path a recipe moves exists in the downloaded archive
- every dependency and `@include` of every resource is installed
- every SQL file the recipe runs exists
- every web interface a resource names exists (no resource that needs a build)
- `server.cfg` starts every installed resource

Before they were published, all eight were also run end to end with the
panel's own recipe engine (everything except the database steps, whose SQL
files were checked to exist and to use the deployer's database).

Downloads use GitHub release zips and branch archives, never the GitHub API:
the API allows a server without a GitHub token 60 requests an hour, which a
large recipe would run out of halfway.

Made for Project Singularity:

- No second connection queue: the panel has its own (*Players → Queue*), so
  connectqueue is left out and qbx_core's queue is switched off.
- Our own `server.cfg` per recipe, without settings that only existed in txAdmin.
- `ox_inventory` is set to the framework it runs with.
- SQL files that create their own database (`es_extended`, `overextended`) are
  pointed at the database chosen in the deployer.

## Changing a recipe

1. Edit the lists in `scripts/build_recipes.py` (and `server.cfg` in the recipe's folder).
2. Run `python scripts/build_recipes.py`; it rebuilds `recipe.yaml` and `README.md`
   and fails on any problem.
3. Optional: `python scripts/check-sources.py` looks every download up online.
4. Add new recipes to `index.yaml` and open a pull request.

The recipe format and all actions are described in [schema/recipe.schema.md](schema/recipe.schema.md).

## License

The recipes are released under the terms in [LICENSE.md](LICENSE.md). The
resources they download keep their own licenses.
