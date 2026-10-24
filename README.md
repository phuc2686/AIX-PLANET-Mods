# AIX PLANET — Community Mods

**English** | [Tiếng Việt](README.vi.md)

Community mods for **AIX PLANET**, a persistent multiplayer evolution-ecosystem
simulation by **AIXLAB**. Thousands of creature cores evolve, migrate, hybridize
and go extinct on a living planet that ticks every 90 seconds — and mods let you
bend its weather, ecology and appearance.

> The game engine is closed-source and lives in a private repository.
> **This repo is the public modding surface**: the full Lua Mod API contract,
> data-driven mod formats, working examples, validation tooling, and the
> community mods that ship in the game. You never need the engine source to
> build a mod — mods are self-contained, drop-in folders.

## About the game

**AIX PLANET** is a persistent, multiplayer macro-evolution simulation. The
world never pauses: a tick runs every **90 seconds**, seasons turn, species
rise and go extinct whether or not anyone is watching.

- **A living planet** — 81,358 hexagonal cells (Uber H3) across continents and
  oceans, with latitude biomes from arctic tundra to equatorial desert. A year
  lasts 120 ticks (Spring 20 · Summer 40 · Autumn 20 · Winter 40) and a
  generation spans 480 ticks.
- **Six powers** — the human-played **Solaris Vanguard** (PLAYER_1), four AI
  warlord empires (Frostborn Syndicate, Verdant Swarm, Dune Ravagers, Abyssal
  Armada), and the wild **SYSTEM_AI** ecosystem that seeds and reseeds the
  planet's wildlife.
- **Creatures with real genetics** — every core carries a 4-axis DNA
  (thermal tolerance, mobility, metabolism, combat morphology), one of four
  doctrines (ZERG swarm, PREDATOR hunter, TURTLE survivor, NOMAD explorer),
  and climbs **5 evolution stages**, judged by its generation peak
  (Stage 2 at 2,500 · Stage 3 at 10,000 · Stage 4 at 15,000 · Stage 5 at
  100,000 individuals).
- **An ecology that pushes back** — large cores graze a multi-cell footprint
  (up to 19 cells), breeding runs in seasonal cohort windows, different clades
  can **hybridize**, long-term neighbours can form **symbiosis**, epidemics
  spread cell to cell, deserts creep, and an AI storyteller throws droughts,
  blooms and crises into the chronicle.
- **Players steer, the world remembers** — issue direct orders (move, split,
  merge, mutate, long-range migration), let the Governor autopilot guard your
  cores while you are offline, and read a full *"while you were away"* digest
  when you return. Lineage trees, a gene heritage vault, faction chronicles
  and weekly/monthly leaderboards record everything.
- **Glory, not victory** — there is no final win screen. Dynasties earn
  honors, achievements and naming rights; a faction that holds #1 biomass for
  **3 consecutive days** unlocks a one-shot eco-catastrophe of its own
  (FAMINE, FREEZE, DEFOREST — or PLAGUE, seeded into a rival's densest cells).
- **World eras (v10.0)** — every generation the planet enters a new era
  (Fertile, Ice, Plague, Hunt, Peace or Harsh), announced 120 ticks in
  advance, and one predator clade may rise as the **Apex Ascendant**.

*World snapshot (audited health check, tick 2829): 3.7 million biomass,
962 living cores, the first 10 Stage-3 apex cores.*

**Your mods run inside this world** — the same persistent planet the players
inhabit, not a sandbox copy.

## Quickstart

1. Copy the example mod:
   `cp -r mods/example_bloom_festival mods/<your_mod_id>`
2. Edit `manifest.json` (unique `id`, your name as `author`) and `main.lua`
   (an `on_tick(ctx)` hook that returns directives — see [MODDING.md](MODDING.md)).
3. Validate locally:
   `python tools/validate_mod.py mods/<your_mod_id>`
4. Open a Pull Request. Reviews follow [CONTRIBUTING.md](CONTRIBUTING.md)
   ([bản tiếng Việt](CONTRIBUTING.vi.md)).

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
