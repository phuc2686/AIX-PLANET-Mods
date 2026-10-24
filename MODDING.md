# MODDING.md — Creating Mods for AIX PLANET

> The drop-in mod folder architecture is inspired by **Endless Sky** (plugins = self-contained directories; drop in to run, remove to uninstall, zero core file edits) and **Unciv** (clean data-driven rules distributed via GitHub). Only architectural patterns were referenced; all code is original.

---

## 1. Mod Installation: Drop-in Directory Structure

```
mods/
  <mod_id>/
    manifest.json   -- Required: id, name, version, api_version
    main.lua        -- Required: returns the mod definition table
    assets/         -- Optional: custom textures, sounds, or visual assets
```

- **Install:** Copy your mod directory into `mods/`, and call `POST /api/mods/reload` (admin endpoint) or restart the server.
- **Uninstall:** Delete the directory and reload. The core game engine is never compromised.
- **Temporarily Disable:** Set `"enabled": false` inside `manifest.json` without needing to delete the directory.
- **Backward Compatibility:** Standalone `.lua` scripts placed inside `mods/lua/` remain supported for legacy setups.

---

## 2. manifest.json

```json
{
    "id": "bloom_festival",
    "name": "Bloom Festival",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Short description of the mod",
    "api_version": "1",
    "enabled": true
}
```

- `id`: Unique identifier, lowercase alphanumeric with underscores.
- `api_version`: Target Lua API contract version. Currently = `"1"`. If a mod declares an `api_version` newer than the host engine, the mod loader flags a clear compatibility warning instead of failing silently.

---

## 3. main.lua — Contract v1

The script must evaluate to a Lua table:

```lua
return {
    id = "bloom_festival",
    name = "Bloom Festival",
    -- Invoked ON EVERY TICK, AFTER engine tick calculations, WITHIN THE SAME SQLite transaction.
    -- Returned directives take effect from the NEXT tick.
    on_tick = function(ctx)
        -- ctx = {
        --   tick = number, season = "SPRING"|"SUMMER"|"AUTUMN"|"WINTER",
        --   total_biomass = number, living_cores = number,
        --   factions = { PLAYER_1 = { biomass = .., cores = .. }, ... }
        -- }
        if ctx.tick % 96 == 0 then
            return {
                { 
                    type = "spawn_weather", 
                    event_type = "BLOOM",
                    radius = 2, 
                    remaining_ticks = 4,
                    temp_delta = 2.0, 
                    food_multiplier = 1.8 
                },
                { 
                    type = "log", 
                    message = "Spring Bloom Festival has begun across the continents!" 
                },
            }
        end
        return {}
    end,
}
```

### Directive Types

| Type | Parameters | Effect |
|---|---|---|
| `spawn_weather` | `event_type` = ICE_AGE / DROUGHT / ACID_RAIN / METEOR / BLOOM / WARM_FRONT; `center_h3` (optional, randomized if omitted); `radius`, `remaining_ticks`, `temp_delta`, `food_multiplier` | Inserts into `weather_events`, processed starting from the next tick |
| `set_config` | `key`, `value` (string) | Upserts configuration into `world_config` |
| `log` | `message` | Appends entry to the tick log / interactive timeline |

---

## 4. Sandbox & Security

- A single, persistent `LuaRuntime` is shared across the process and reused on every tick.
- Dangerous globals are scrubbed: `os.execute`, `io`, `debug`, `loadfile`, etc.
- In the event of a mod runtime error, the error is safely isolated and recorded in `/api/mods`. Other mods continue executing, and **the simulation tick will never fail due to Lua script faults**.
- The entire Lua modding engine is gated behind the environment flag `LUA_MODS_ENABLED=true` (disabled by default for minimal overhead).

---

## 5. Mod Management APIs

- `GET /api/mods` — Lists all loaded mods (`id`, `name`, `version`, `type`, error status if any).
- `POST /api/mods/reload` — Hot-reloads all active mods on demand (Admin privilege required).

---

## 6. Reference Implementation

Refer to `mods/example_bloom_festival/` for a fully functional drop-in reference mod containing `manifest.json` and `main.lua`.
