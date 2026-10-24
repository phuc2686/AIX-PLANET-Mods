#!/usr/bin/env python3
"""
Offline validator for AIX PLANET community mods. No game install required.

Usage:
    python tools/validate_mod.py mods/<mod_id>          # a Lua mod folder
    python tools/validate_mod.py mods/visuals/x.json    # a visual morph mod
    python tools/validate_mod.py mods/weather/y.json    # a weather scenario mod
    python tools/validate_mod.py mods/lua/z.lua         # a legacy Lua script

Checks, mirroring what the game engine actually consumes:
- manifest.json: required fields, id format, semver, api_version supported.
- Visual / weather JSON: the exact trigger/effects fields the engine reads.
- main.lua: if the `lupa` package is available, the script is loaded in a
  scrubbed runtime (like the game's sandbox) and its on_tick hook is invoked
  with a fake context; every returned directive is validated. Without lupa,
  a basic structural check runs instead.

Exit code 0 = valid, 1 = problems found.
"""
import json
import os
import re
import sys

SUPPORTED_API_VERSION = "1"
ID_RE = re.compile(r"^[a-z0-9_]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
EVENT_TYPES = {"ICE_AGE", "DROUGHT", "ACID_RAIN", "METEOR", "BLOOM", "WARM_FRONT"}
STRATEGIES = {"ZERG", "PREDATOR", "TURTLE", "NOMAD"}
TERRAINS = {"WATER", "FOREST", "PLAINS", "DESERT", "MOUNTAIN", "TUNDRA", "SWAMP", "JUNGLE"}
VISUAL_TRAIT_KEYS = {"mobility_min", "thermal_min", "thermal_max", "combat_morph_min", "metabolism_min"}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_id_name_type(data, kind):
    if not ID_RE.match(str(data.get("id", ""))):
        err(f"{kind}: 'id' must match ^[a-z0-9_]+$, got {data.get('id')!r}")
    if not data.get("name"):
        err(f"{kind}: 'name' is required")


def validate_manifest(mod_dir):
    path = os.path.join(mod_dir, "manifest.json")
    if not os.path.exists(path):
        err("manifest.json is missing")
        return None
    try:
        m = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        err(f"manifest.json is not valid JSON: {e}")
        return None
    check_id_name_type(m, "manifest")
    if not SEMVER_RE.match(str(m.get("version", ""))):
        err(f"manifest: 'version' must be semver (x.y.z), got {m.get('version')!r}")
    api = str(m.get("api_version", ""))
    if not api:
        err("manifest: 'api_version' is required")
    elif api > SUPPORTED_API_VERSION:
        err(f"manifest: api_version {api!r} is newer than the supported {SUPPORTED_API_VERSION!r}")
    if m.get("enabled") is False:
        warn("manifest: 'enabled' is false — the mod will not load")
    return m


def validate_visual(data):
    check_id_name_type(data, "visual mod")
    if data.get("type") != "visual_morph":
        err("visual mod: 'type' must be 'visual_morph'")
    trig = data.get("trigger")
    if not isinstance(trig, dict) or not trig:
        err("visual mod: 'trigger' must be a non-empty object")
        trig = {}
    if "stage_min" in trig and not (1 <= int(trig["stage_min"]) <= 5):
        err("visual mod: trigger.stage_min must be 1..5")
    if "terrain" in trig and trig["terrain"] not in TERRAINS:
        err(f"visual mod: trigger.terrain {trig['terrain']!r} is not a known terrain")
    if "strategy" in trig and trig["strategy"] not in STRATEGIES:
        err(f"visual mod: trigger.strategy {trig['strategy']!r} is not a known strategy")
    for k in (trig.get("traits") or {}):
        if k not in VISUAL_TRAIT_KEYS:
            warn(f"visual mod: trigger.traits.{k} is not read by the engine")
    eff = data.get("effects") or {}
    if not eff.get("visual_id"):
        err("visual mod: effects.visual_id is required")
    if "color" in eff and not COLOR_RE.match(str(eff["color"])):
        err("visual mod: effects.color must be #RRGGBB")


def validate_weather(data):
    check_id_name_type(data, "weather mod")
    if data.get("type") != "weather_trigger":
        err("weather mod: 'type' must be 'weather_trigger'")
    trig = data.get("trigger") or {}
    if not isinstance(trig.get("cell_population_min"), int) or trig["cell_population_min"] < 1:
        err("weather mod: trigger.cell_population_min (positive integer) is required")
    eff = data.get("effects") or {}
    if eff.get("event_type") not in EVENT_TYPES:
        err(f"weather mod: effects.event_type must be one of {sorted(EVENT_TYPES)}")
    if "radius_k" in eff and not (0 <= int(eff["radius_k"]) <= 3):
        err("weather mod: effects.radius_k must be 0..3")
    if "duration_ticks" in eff and int(eff["duration_ticks"]) < 1:
        err("weather mod: effects.duration_ticks must be >= 1")


def fake_ctx():
    return {
        "tick": 96,
        "season": "SPRING",
        "total_biomass": 100000,
        "living_cores": 10,
        "factions": {"PLAYER_1": {"biomass": 5000, "cores": 1}},
    }


def validate_directives(directives, src):
    if directives is None:
        return
    if not isinstance(directives, (list, tuple)):
        err(f"{src}: on_tick must return a table (list) of directives")
        return
    for i, d in enumerate(directives):
        if not isinstance(d, dict):
            err(f"{src}: directive #{i} is not a table")
            continue
        t = d.get("type")
        if t == "spawn_weather":
            if d.get("event_type") not in EVENT_TYPES:
                err(f"{src}: directive #{i} event_type must be one of {sorted(EVENT_TYPES)}")
        elif t == "set_config":
            if not d.get("key"):
                err(f"{src}: directive #{i} set_config needs a 'key'")
        elif t == "log":
            if not d.get("message"):
                err(f"{src}: directive #{i} log needs a 'message'")
        else:
            err(f"{src}: directive #{i} has unknown type {t!r}")


def validate_lua_file(lua_path):
    src = open(lua_path, encoding="utf-8").read()
    try:
        from lupa import LuaRuntime
    except ImportError:
        if "on_tick" not in src or "return" not in src:
            err(f"{lua_path}: no on_tick hook / return found (structural check only — install 'lupa' for a full run)")
        else:
            warn(f"{lua_path}: 'lupa' not installed — structural check only, on_tick was not executed")
        return
    import lupa
    lua = LuaRuntime(unpack_returned_tuples=True)
    g = lua.globals()
    for name in ("os", "io", "debug", "loadfile", "dofile", "require", "load", "loadstring"):
        g[name] = None  # mirror the game's sandbox scrubbing
    try:
        mod = lua.execute(src)
    except Exception as e:
        err(f"{lua_path}: does not load in a scrubbed runtime: {e}")
        return
    if lupa.lua_type(mod) != "table" or mod["on_tick"] is None:
        err(f"{lua_path}: script must return a table with an on_tick function")
        return
    try:
        result = mod["on_tick"](lua.table_from(fake_ctx()))
    except Exception as e:
        err(f"{lua_path}: on_tick crashed on a fake context: {e}")
        return
    if result is not None:
        def to_py(v, depth=0):
            if depth > 6:
                return v
            if lupa.lua_type(v) == "table":
                items = [(k, to_py(val, depth + 1)) for k, val in v.items()]
                if not items:
                    return []
                keys = [k for k, _ in items]
                if keys and all(isinstance(k, int) for k in keys):
                    return [val for _, val in sorted(items, key=lambda kv: kv[0])]
                return dict(items)
            return v
        validate_directives(to_py(result), lua_path)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    target = sys.argv[1]
    if os.path.isdir(target):
        validate_manifest(target)
        lua_path = os.path.join(target, "main.lua")
        if not os.path.exists(lua_path):
            err("main.lua is missing")
        else:
            validate_lua_file(lua_path)
    elif target.endswith(".json"):
        try:
            data = json.load(open(target, encoding="utf-8"))
        except Exception as e:
            err(f"{target}: not valid JSON: {e}")
            data = None
        if data is not None:
            if "/visuals/" in target.replace(os.sep, "/"):
                validate_visual(data)
            elif "/weather/" in target.replace(os.sep, "/"):
                validate_weather(data)
            else:
                err(f"{target}: place JSON mods under mods/visuals/ or mods/weather/ so the engine picks them up")
    elif target.endswith(".lua"):
        validate_lua_file(target)
    else:
        err(f"{target}: expected a mod folder, a .json mod, or a .lua script")
        return 1

    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"INVALID — {len(errors)} problem(s).")
        return 1
    print(f"OK — {target} is a valid AIX PLANET mod.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
