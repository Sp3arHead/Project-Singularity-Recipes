# ox_core

Complete ox_core server for Project Singularity, built on the Overextended resources.

**Based on:** the official recipe in [overextended/txAdminRecipe](https://github.com/overextended/txAdminRecipe).

## Included

- Default Cfx.re resources and screenshot-basic
- ox_core with its database, oxmysql, ox_lib, ox_inventory, ox_banking, ox_doorlock,
  ox_commands, ox_fuel, ox_target
- illenium-appearance (with its tables)
- NPWD phone (with its tables)
- pma-voice, bob74_ipl, a loading screen

## Requirements

MariaDB or MySQL, a Cfx.re license key, OneSync (on), FXServer 12913 or newer, game build 3258.

## Changes against the official recipe

- `server.cfg` from this folder, with notes on the panel.

## In the panel

ox_core has no preset in the in-game menu's framework settings yet; inventory
and money tools need the *custom* framework event (*Master Actions → Framework*).
