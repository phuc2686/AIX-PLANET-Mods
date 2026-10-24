-- Harsh Winter: at the first tick of every winter, drop the global
-- temperature offset for drama. Restores it when spring returns.
return {
    id = "harsh_winter",
    name = "Harsh Winter",
    on_tick = function(ctx)
        if ctx.season == "WINTER" and ctx.tick % 12 == 0 then
            return {
                { type = "set_config", key = "global_temp_offset", value = "-4.0" },
                { type = "log", message = "Harsh winter grips the planet (-4C)." },
            }
        end
        if ctx.season == "SPRING" and ctx.tick % 12 == 0 then
            return {
                { type = "set_config", key = "global_temp_offset", value = "0.0" },
            }
        end
        return {}
    end,
}
