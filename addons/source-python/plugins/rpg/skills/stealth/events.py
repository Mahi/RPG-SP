def player_spawn(player, skill, variables, **eargs):
    amount = variables['base_stealth'] + variables['stealth_per_level'] * skill.level
    player.color = player.color.with_alpha(int(255 * (1 - amount)))


skill_upgrade = player_spawn