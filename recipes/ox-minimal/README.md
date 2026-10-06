# ox_core (minimal)

ox_core with its built-in character selection and the appearance menu, nothing else.

**Resources:** 7  
**Tasks:** 24

## Requirements

- MariaDB 11.4 or newer
- a Cfx.re license key
- OneSync (on)
- game build 3258 (set in server.cfg)
- FXServer 12913 or newer

## Included

- `[cfx]`: `baseevents`, `mapmanager`, `spawnmanager`
- `[ox]`: `ox_core`, `ox_lib`, `oxmysql`
- `[standalone]`: `illenium-appearance`

## Database

- `resources/[ox]/ox_core/sql/install.sql`
- `resources/[standalone]/illenium-appearance/sql/playerskins.sql`
- `resources/[standalone]/illenium-appearance/sql/player_outfits.sql`

## Notes

- ox_core brings its own character selection; illenium-appearance lets players shape their character.
- install.sql creates its own database `overextended`; the recipe points it at the database chosen in the deployer.
- The in-game menu of Project Singularity has no preset for this framework yet; its inventory and money tools need the custom framework event (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
