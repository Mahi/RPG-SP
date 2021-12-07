def player_jump(player, skill, variables, **eargs):
    v = player.velocity
    multiplier = 1 + variables['velocity_multiplier_per_level'] * skill.level
    v.x *= multiplier
    v.y *= multiplier
    player.base_velocity = v
