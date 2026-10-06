# QBCore (minimal)

qb-core with character selection, spawn, the starter apartment, inventory and the clothing menu, nothing else.

**Resources:** 16  
**Tasks:** 49

## Requirements

- MariaDB or MySQL
- a Cfx.re license key
- OneSync (on)
- game build 3095 (set in server.cfg)

## Included

- `[cfx]`: `baseevents`, `basic-gamemode`, `mapmanager`, `spawnmanager`
- `[qb]`: `qb-apartments`, `qb-clothing`, `qb-core`, `qb-interior`, `qb-inventory`, `qb-menu`, `qb-multicharacter`, `qb-spawn`, `qb-weapons`, `qb-weathersync`
- `[standalone]`: `oxmysql`, `PolyZone`

## Database

- `resources/[qb]/qb-core/qbcore.sql`
- `resources/[qb]/qb-apartments/qb-apartments.sql`
- `resources/[qb]/qb-clothing/qb-clothing.sql`
- `resources/[qb]/qb-inventory/qb-inventory.sql`

## Notes

- qb-multicharacter needs qb-spawn and qb-apartments, which need qb-interior, qb-clothing, qb-weathersync and PolyZone.
- qb-inventory (with qb-weapons) is included because qb-multicharacter hands out the starter items through it; qb-menu runs the starter apartment door menus.
- qb-target is not included; `UseTarget` is off in server.cfg.
- The in-game menu of Project Singularity finds this framework on its own for its inventory and money tools (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
