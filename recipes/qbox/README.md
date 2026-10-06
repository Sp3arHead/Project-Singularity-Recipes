# Qbox

Complete Qbox roleplay server for Project Singularity. Qbox keeps a QBCore
bridge, so most QBCore resources keep working.

**Based on:** the official recipe in [Qbox-project/txAdminRecipe](https://github.com/Qbox-project/txAdminRecipe).

## Included

- Default Cfx.re resources (the old `chat` is replaced by the system chat)
- `qbx_core` and 48 `qbx_*` resources: vehicles, garages, properties, police,
  medical and ambulance, mechanic, jobs, robberies, customs, ID card, HUD and more
- ox_lib, ox_target, ox_inventory (with the Qbox item list and images), ox_doorlock, ox_fuel, oxmysql
- illenium-appearance, Renewed-Banking, Renewed-Weathersync, xt-prison, vehiclehandler, scully_emotemenu
- NPWD phone with the Qbox garage and mail apps
- pma-voice with mm_radio, a loading screen, the Pillbox hospital
- The Qbox databases (core, vehicles, vehicle shop and sales, weed, lap races, drugs, NPWD)

## Requirements

MariaDB or MySQL, a Cfx.re license key, OneSync (on), game build 3258.

## Changes against the official recipe

- `qbx_core`'s built-in queue is switched off (`set qbx:enableQueue "false"`):
  the panel has its own connection queue (*Players → Queue*).
- `server.cfg` from this folder, with notes on the panel and the server's own
  name in the welcome message. `voice.cfg`, `ox.cfg`, `permissions.cfg` and
  `misc.cfg` come unchanged from the official recipe.

## In the panel

Qbox is not one of the presets of the in-game menu's inventory and money tools.
Its QBCore bridge may let the QBCore preset work; this has not been tested. The
*custom* framework event always works (*Master Actions → Framework*).
