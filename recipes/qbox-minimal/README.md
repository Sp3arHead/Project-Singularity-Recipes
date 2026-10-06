# Qbox (minimal)

qbx_core with its inventory, ID cards and the appearance menu, nothing else.

**Resources:** 10  
**Tasks:** 33

## Requirements

- MariaDB or MySQL
- a Cfx.re license key
- OneSync (on)
- game build 3258 (set in server.cfg)

## Included

- `[cfx]`: `baseevents`, `mapmanager`, `spawnmanager`
- `[ox]`: `ox_inventory`, `ox_lib`, `oxmysql`
- `[qbx]`: `qbx_core`, `qbx_idcard`
- `[standalone]`: `illenium-appearance`, `MugShotBase64`

## Database

- `resources/[qbx]/qbx_core/qbx_core.sql`
- `resources/[standalone]/illenium-appearance/sql/playerskins.sql`
- `resources/[standalone]/illenium-appearance/sql/player_outfits.sql`

## Notes

- qbx_core uses ox_inventory for all items and requires qbx_idcard (with MugShotBase64) when a character is created.
- ox_inventory gets the Qbox item list, so the starter ID card and driver license exist.
- The in-game menu of Project Singularity has no preset for this framework yet; its inventory and money tools need the custom framework event (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
