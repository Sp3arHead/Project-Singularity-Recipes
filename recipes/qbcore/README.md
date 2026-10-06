# QBCore

Complete QBCore roleplay server for Project Singularity.

**Based on:** the official recipe in [qbcore-framework/txAdminRecipe](https://github.com/qbcore-framework/txAdminRecipe).

## Included

- Default Cfx.re resources (the old `chat` is replaced by the system chat)
- `qb-core` and 57 `qb-*` resources: multicharacter, spawn, inventory, garages,
  houses, apartments, banking, shops, phone, HUD, radial menu, robberies, and the
  police, ambulance, mechanic, taxi, bus, news, tow, garbage, recycle and hot dog jobs
- oxmysql, menuv, PolyZone, progressbar, interact-sound, safecracker, screencapture
- pma-voice with qb-radio
- Maps: hospital, dealer, prison
- The QBCore database (`qbcore.sql`)

## Requirements

MariaDB or MySQL, a Cfx.re license key, OneSync (on), game build 3095.

## Changes against the official recipe

- `connectqueue` is left out: the panel has its own connection queue
  (*Players → Queue*), and two queues would fight over the free slots.
- `server.cfg` from this folder, with notes on the panel.

## In the panel

The in-game menu's inventory and money tools detect QBCore on their own
(*Master Actions → Framework*).
