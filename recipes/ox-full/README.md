# ox_core (full)

Every maintained Overextended resource: inventory, banking, doorlock, target, fuel, commands, with appearance, NPWD phone, voice and maps.

**Resources:** 18  
**Tasks:** 59

## Requirements

- MariaDB 11.4 or newer
- a Cfx.re license key
- OneSync (on)
- game build 3258 (set in server.cfg)
- FXServer 12913 or newer

## Included

- `[cfx]`: `baseevents`, `mapmanager`, `spawnmanager`
- `[ox]`: `ox_banking`, `ox_commands`, `ox_core`, `ox_doorlock`, `ox_fuel`, `ox_inventory`, `ox_lib`, `ox_target`, `oxmysql`
- `[standalone]`: `bob74_ipl`, `illenium-appearance`, `npwd`, `pe-basicloading`, `pma-voice`, `screenshot-basic`

## Database

- `resources/[ox]/ox_core/sql/install.sql`
- `resources/[standalone]/illenium-appearance/sql/playerskins.sql`
- `resources/[standalone]/illenium-appearance/sql/player_outfits.sql`
- `resources/[ox]/ox_doorlock/sql/ox_doorlock.sql`
- `resources/[standalone]/npwd/import.sql`

## Notes

- Every maintained Overextended resource. Left out: ox_property (needs pefcl and ox_appearance, which no longer exist), ox_police (unmaintained since 2023), ox_mdt, ox_vehicledealer and ox_identityapp (no release, would need a build), qtarget (replaced by ox_target).
- ox_inventory is set to the ox framework in server.cfg (`inventory:framework "ox"`); its default would be ESX.
- The in-game menu of Project Singularity has no preset for this framework yet; its inventory and money tools need the custom framework event (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
