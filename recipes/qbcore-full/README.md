# QBCore (full)

Every resource the QBCore team publishes: all jobs, robberies, housing, vehicles, phone, admin menu, maps and voice.

**Resources:** 77  
**Tasks:** 236

## Requirements

- MariaDB or MySQL
- a Cfx.re license key
- OneSync (on)
- game build 3095 (set in server.cfg)

## Included

- `[cfx]`: `baseevents`, `basic-gamemode`, `mapmanager`, `spawnmanager`
- `[defaultmaps]`: `dealer_map`, `hospital_map`
- `[defaultmaps]/[prison_map]`: `prison_canteen`, `prison_main`, `prison_meeting`
- `[qb]`: `qb-adminmenu`, `qb-ambulancejob`, `qb-apartments`, `qb-banking`, `qb-bankrobbery`, `qb-busjob`, `qb-cityhall`, `qb-clothing`, `qb-core`, `qb-crafting`, `qb-crypto`, `qb-diving`, `qb-doorlock`, `qb-drugs`, `qb-fuel`, `qb-garages`, `qb-garbagejob`, `qb-hotdogjob`, `qb-houserobbery`, `qb-houses`, `qb-hud`, `qb-input`, `qb-interior`, `qb-inventory`, `qb-jewelery`, `qb-lapraces`, `qb-loading`, `qb-management`, `qb-mechanicjob`, `qb-menu`, `qb-minigames`, `qb-multicharacter`, `qb-newsjob`, `qb-pawnshop`, `qb-phone`, `qb-policejob`, `qb-prison`, `qb-radialmenu`, `qb-radio`, `qb-recyclejob`, `qb-scoreboard`, `qb-scrapyard`, `qb-shops`, `qb-smallresources`, `qb-spawn`, `qb-storerobbery`, `qb-streetraces`, `qb-target`, `qb-taxijob`, `qb-towjob`, `qb-truckerjob`, `qb-truckrobbery`, `qb-vehiclekeys`, `qb-vehiclesales`, `qb-vehicleshop`, `qb-vineyard`, `qb-weapons`, `qb-weathersync`, `qb-weed`
- `[standalone]`: `bob74_ipl`, `interact-sound`, `menuv`, `oxmysql`, `PolyZone`, `progressbar`, `safecracker`, `screenshot-basic`
- `[voice]`: `pma-voice`

## Database

- `resources/[qb]/qb-core/qbcore.sql`
- `resources/[qb]/qb-apartments/qb-apartments.sql`
- `resources/[qb]/qb-banking/banking.sql`
- `resources/[qb]/qb-clothing/qb-clothing.sql`
- `resources/[qb]/qb-crypto/qb-crypto.sql`
- `resources/[qb]/qb-drugs/qb-drugs.sql`
- `resources/[qb]/qb-garages/player_vehicles.sql`
- `resources/[qb]/qb-houses/qb-houses.sql`
- `resources/[qb]/qb-inventory/qb-inventory.sql`
- `resources/[qb]/qb-lapraces/qb-lapraces.sql`
- `resources/[qb]/qb-phone/qb-phone.sql`
- `resources/[qb]/qb-vehiclesales/qb-vehiclesales.sql`
- `resources/[qb]/qb-vehicleshop/vehshop.sql`
- `resources/[qb]/qb-weed/qb-weed.sql`

## Notes

- Every resource the QBCore team publishes in qbcore-fivem, including the forks it maintains (PolyZone, menuv, interact-sound, bob74_ipl).
- connectqueue is left out: the panel has its own connection queue, two queues would fight over the free slots.
- qb-adminmenu is included next to the in-game menu of Project Singularity.
- The in-game menu of Project Singularity finds this framework on its own for its inventory and money tools (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
