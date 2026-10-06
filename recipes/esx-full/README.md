# ESX Legacy (full)

Every ESX Legacy resource: the whole core, all addons and the seasonal content, with phone, voice and the ox library.

**Resources:** 64  
**Tasks:** 40

## Requirements

- MariaDB or MySQL
- a Cfx.re license key
- OneSync (on)
- game build 3258 (set in server.cfg)

## Included

- `[cfx]`: `baseevents`, `mapmanager`, `spawnmanager`
- `[core]`: `cron`, `es_extended`, `esx_chat_theme`, `esx_context`, `esx_identity`, `esx_inventory`, `esx_lib`, `esx_loadingscreen`, `esx_menu_default`, `esx_menu_dialog`, `esx_menu_list`, `esx_multicharacter`, `esx_notify`, `esx_progressbar`, `esx_skin`, `esx_textui`, `skinchanger`
- `[esx_addons]`: `esx_accessories`, `esx_addonaccount`, `esx_addoninventory`, `esx_adminmenu`, `esx_ambulancejob`, `esx_animations`, `esx_banking`, `esx_barbershop`, `esx_basicneeds`, `esx_billing`, `esx_boat`, `esx_clotheshop`, `esx_cruisecontrol`, `esx_datastore`, `esx_dmvschool`, `esx_drugs`, `esx_garage`, `esx_hud`, `esx_joblisting`, `esx_jobs`, `esx_license`, `esx_lscustom`, `esx_mechanicjob`, `esx_optionalneeds`, `esx_policejob`, `esx_property`, `esx_rpchat`, `esx_scoreboard`, `esx_service`, `esx_shops`, `esx_society`, `esx_status`, `esx_taxijob`, `esx_vehicleshop`, `esx_weaponshop`, `esx_weather`
- `[esx_seasonal]/[esx_seasonal]`: `esx_christmas`
- `[standalone]`: `bob74_ipl`, `ox_lib`, `oxmysql`, `pma-voice`, `screenshot-basic`, `sd-phone`, `sd-phone-props`

## Database

- `tmp/esx-legacy.sql`

## Notes

- Everything in esx_core `[core]`, ESX-Legacy-Addons and ESX-Legacy-Seasonal.
- The seasonal content (`[esx_seasonal]`) is installed but not started; server.cfg shows how to start it.
- esx_adminmenu is included next to the in-game menu of Project Singularity.
- sd-phone comes from its own release; the ESX fork of it has none.
- The in-game menu of Project Singularity finds this framework on its own for its inventory and money tools (Master Actions -> Framework).

This folder is built by `scripts/build_recipes.py`; change the definitions there.
