# ESX Legacy (minimal)

The ESX core with character registration and the skin menu, nothing else.

**Resources:** 9  
**Tasks:** 22

## Requirements

- MariaDB or MySQL
- a Cfx.re license key
- OneSync (on)
- game build 3258 (set in server.cfg)

## Included

- `[cfx]`: `baseevents`, `mapmanager`, `spawnmanager`
- `[core]`: `es_extended`, `esx_identity`, `esx_lib`, `esx_skin`, `skinchanger`
- `[standalone]`: `oxmysql`

## Database

- `resources/[core]/es_extended/es_extended.sql`
- `resources/[core]/esx_identity/esx_identity.sql`
- `resources/[core]/esx_skin/esx_skin.sql`

## Notes

- es_extended.sql creates its own database `es_extended`; the recipe points it at the database chosen in the deployer.
- ESX would take its language from a txAdmin setting; server.cfg sets `esx:locale` instead.
- The in-game menu of Project Singularity finds this framework on its own for its inventory and money tools (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
