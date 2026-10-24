# Contributing a Mod to AIX PLANET

(Bản tiếng Việt: [CONTRIBUTING.vi.md](CONTRIBUTING.vi.md))

Thanks for building for the planet. This repo is the only public surface of a
closed-source game, so the rules below keep mods safe, original and shippable.

## Submission flow

1. **Fork** this repo and create your mod:
   - Lua mod: a new folder `mods/<mod_id>/` with `manifest.json` + `main.lua`.
   - Visual morph: one JSON file in `mods/visuals/`.
   - Weather scenario: one JSON file in `mods/weather/`.
2. **Validate** before submitting:
   `python tools/validate_mod.py mods/<mod_id>` (or pass a JSON file path).
   Your PR description must include the validator output.
3. **Open a Pull Request** using the mod submission template. One mod per PR.

## Review standards

- **Original work only.** Write your own code and data. Do not copy code from
  other games or projects (including GPL-licensed ones). Learning *design
  ideas* from other games is fine — say so in your PR; copied code is not.
- **Self-contained.** A mod is its folder (plus its optional `assets/`).
  Nothing outside the folder may be required, and removing the folder must
  fully uninstall the mod.
- **Safe by construction.** Lua mods run in a scrubbed sandbox (no `os`, `io`,
  `debug`, filesystem or network). Mods that error are isolated and reported;
  a mod must never rely on crashing or on blocking the tick.
- **Balance is a conversation.** Weather directives and config writes affect
  a shared, persistent world. Radical effects are welcome as ideas — expect
  the maintainers to tune numbers with you rather than reject the concept.
- **API contract.** Target `api_version: "1"` (see [MODDING.md](MODDING.md)).
  Manifests with a newer `api_version` than the engine supports are flagged,
  not loaded.

## Licensing of contributions

- You keep the copyright to your mod.
- By opening a Pull Request you license your mod under the **MIT License**
  (inbound = outbound), and you grant AIXLAB the right to ship the approved
  mod inside AIX PLANET, with your `author` name credited in the manifest and
  the in-game mod list.
- Only submit work you have the right to license this way.

## What happens after merge

Approved mods are synced from this repo into the game build and hot-loaded
(`POST /api/mods/reload`, admin side). If a shipped mod ever needs to be
pulled for balance or safety, it is disabled via its manifest — your authorship
record stays in this repo's history.
