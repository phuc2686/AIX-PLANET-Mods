# AIX PLANET — Community Mods

Community mods for **AIX PLANET**, a persistent multiplayer evolution-ecosystem
simulation by **AIXLAB**. Thousands of creature cores evolve, migrate, hybridize
and go extinct on a living planet that ticks every 90 seconds — and mods let you
bend its weather, ecology and appearance.

> The game engine is closed-source and lives in a private repository.
> **This repo is the public modding surface**: the full Lua Mod API contract,
> data-driven mod formats, working examples, validation tooling, and the
> community mods that ship in the game. You never need the engine source to
> build a mod — mods are self-contained, drop-in folders.

## Quickstart

1. Copy the example mod:
   `cp -r mods/example_bloom_festival mods/<your_mod_id>`
2. Edit `manifest.json` (unique `id`, your name as `author`) and `main.lua`
   (an `on_tick(ctx)` hook that returns directives — see [MODDING.md](MODDING.md)).
3. Validate locally:
   `python tools/validate_mod.py mods/<your_mod_id>`
4. Open a Pull Request. Reviews follow [CONTRIBUTING.md](CONTRIBUTING.md).

## Three ways to mod

| Kind | Where | Skill needed |
|---|---|---|
| **Lua mods** | `mods/<mod_id>/` with `manifest.json` + `main.lua` | Basic scripting — react to each tick, spawn weather events, write world config, log to the timeline |
| **Visual morphs** | `mods/visuals/*.json` | JSON only — define trigger conditions (stage, terrain, population, traits) and the special form a core morphs into |
| **Weather scenarios** | `mods/weather/*.json` | JSON only — define a population trigger and the ecological event it unleashes |

Full contracts: [MODDING.md](MODDING.md) · JSON schemas: [`schemas/`](schemas/)

## How a mod gets into the game

1. You open a PR in this repo.
2. Maintainers review it (originality, balance, safety — mods run sandboxed,
   and a broken mod can never crash a tick).
3. Approved mods are merged here, synced into the game build's `mods/` folder,
   and hot-loaded. **Your author name ships with the mod** in `manifest.json`
   and in the in-game mod list (`GET /api/mods`).

## Layout

```
mods/            Community mods (Lua folders, legacy .lua scripts, visuals/, weather/)
schemas/         JSON Schemas for manifest.json and the data-driven mod formats
tools/           validate_mod.py — offline checker (no game install required)
MODDING.md       The Lua Mod API contract (API v1)
CONTRIBUTING.md  Submission flow, review standards, licensing terms
```

## License

Repository documentation, examples and tooling: MIT (see [LICENSE](LICENSE)).
Contributed mods: authors keep their copyright and license their mod under MIT
by submitting it — see [CONTRIBUTING.md](CONTRIBUTING.md).
