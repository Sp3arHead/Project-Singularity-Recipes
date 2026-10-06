# Qbox (full)

Every Qbox resource with the ox stack, Renewed banking and weather, NPWD phone, appearance, voice and maps.

**Resources:** 78  
**Tasks:** 251

## Requirements

- MariaDB or MySQL
- a Cfx.re license key
- OneSync (on)
- game build 3258 (set in server.cfg)

## Included

- `[assets]`: `pillbox`
- `[cfx]`: `baseevents`, `mapmanager`, `spawnmanager`
- `[npwd-apps]`: `npwd_qbx_garages`, `npwd_qbx_mail`
- `[npwd]`: `npwd`, `qbx_npwd`
- `[ox]`: `ox_doorlock`, `ox_fuel`, `ox_inventory`, `ox_lib`, `ox_target`, `oxmysql`
- `[qbx]`: `mhacking`, `qbx_adminmenu`, `qbx_ambulancejob`, `qbx_bankrobbery`, `qbx_binoculars`, `qbx_busjob`, `qbx_carwash`, `qbx_chat_theme`, `qbx_cityhall`, `qbx_core`, `qbx_customs`, `qbx_density`, `qbx_divegear`, `qbx_diving`, `qbx_drugs`, `qbx_fireworks`, `qbx_garages`, `qbx_garbagejob`, `qbx_houserobbery`, `qbx_hud`, `qbx_idcard`, `qbx_jewelery`, `qbx_lapraces`, `qbx_management`, `qbx_mechanicjob`, `qbx_medical`, `qbx_newsjob`, `qbx_pawnshop`, `qbx_police`, `qbx_properties`, `qbx_radialmenu`, `qbx_recyclejob`, `qbx_scoreboard`, `qbx_scrapyard`, `qbx_seatbelt`, `qbx_smallresources`, `qbx_spawn`, `qbx_storerobbery`, `qbx_streetraces`, `qbx_taxijob`, `qbx_towjob`, `qbx_truckerjob`, `qbx_truckrobbery`, `qbx_vehiclekeys`, `qbx_vehicles`, `qbx_vehiclesales`, `qbx_vehicleshop`, `qbx_vineyard`, `qbx_weed`
- `[standalone]`: `bob74_ipl`, `illenium-appearance`, `loadscreen`, `mana_audio`, `MugShotBase64`, `Renewed-Banking`, `Renewed-Weathersync`, `safecracker`, `screencapture`, `scully_emotemenu`, `ultra-voltlab`, `vehiclehandler`, `xt-prison`
- `[voice]`: `mm_radio`, `pma-voice`

## Database

- `resources/[qbx]/qbx_core/qbx_core.sql`
- `resources/[qbx]/qbx_vehicles/vehicles.sql`
- `resources/[qbx]/qbx_vehiclesales/qbx_vehiclesales.sql`
- `resources/[qbx]/qbx_vehicleshop/vehshop.sql`
- `resources/[qbx]/qbx_weed/sql/qbx_weed.sql`
- `resources/[qbx]/qbx_lapraces/qbx_lapraces.sql`
- `resources/[qbx]/qbx_drugs/qbx_drugs.sql`
- `resources/[qbx]/qbx_properties/property.sql`
- `resources/[qbx]/qbx_properties/decorations.sql`
- `resources/[standalone]/illenium-appearance/sql/playerskins.sql`
- `resources/[standalone]/illenium-appearance/sql/player_outfits.sql`
- `resources/[ox]/ox_doorlock/sql/ox_doorlock.sql`
- `resources/[npwd]/npwd/import.sql`

## Notes

- Every Qbox resource in Qbox-project, including the forks it maintains (qbx_idcard, qbx_customs). Left out: qbx_db_backup and qbx_grafana_map (dashboard tools) and qbxsql (tooling).
- qbx_core's own queue is switched off (`qbx:enableQueue false`): the panel has its own connection queue.
- NPWD is pinned to 3.16.0, the version qbx_npwd is made for.
- qbx_adminmenu is included next to the in-game menu of Project Singularity.
- The in-game menu of Project Singularity has no preset for this framework yet; its inventory and money tools need the custom framework event (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
