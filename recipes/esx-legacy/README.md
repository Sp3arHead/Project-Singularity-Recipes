# ESX Legacy

Complete ESX Legacy roleplay server for Project Singularity.

**Based on:** the official recipe in [esx-framework/ESX-recipes](https://github.com/esx-framework/ESX-recipes) (branch `legacy`).

## Included

- Default Cfx.re resources (the old `chat` is replaced by the system chat)
- ESX core (`es_extended`, `esx_lib` and the rest of `[core]`) and all of [ESX Legacy Addons](https://github.com/esx-framework/ESX-Legacy-Addons)
- oxmysql, ox_lib, pma-voice, bob74_ipl
- sd-phone with its props
- The ESX database (`legacy.sql`)

## Requirements

MariaDB or MySQL, a Cfx.re license key, OneSync (on), game build 3258.

## Changes against the official recipe

- `server.cfg` from this folder: notes on the panel, and the ESX language is set
  here (`setr esx:locale "en"`), because ESX would otherwise take it from a txAdmin
  setting that Project Singularity does not have.

## In the panel

The in-game menu's inventory and money tools detect ESX on their own
(*Master Actions → Framework*).
