-- Blood Moon: when the world gets crowded, the sky answers.
-- Every 48 ticks (one full year), if global biomass is high, call down a meteor.
return {
    id = "blood_moon",
    name = "Blood Moon",
    on_tick = function(ctx)
        if ctx.tick % 48 == 0 and ctx.total_biomass > 500000 then
            return {
                { type = "spawn_weather", event_type = "METEOR",
                  radius = 1, remaining_ticks = 2 },
                { type = "log", message = "Blood Moon rises over the continents..." },
            }
        end
        return {}
    end,
}
