return {
    id = "bloom_festival",
    name = "Bloom Festival",
    on_tick = function(ctx)
        if ctx.tick % 96 == 0 then
            return {
                { type="spawn_weather", event_type="BLOOM", radius=2, remaining_ticks=4,
                  temp_delta=2.0, food_multiplier=1.8 },
                { type="log", message="Le Hoi Hoa No: mot vung dat bung no su song!" },
            }
        end
        return {}
    end,
}
