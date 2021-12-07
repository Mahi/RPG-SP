def player_spawn(player, skill, variables, **eargs):
    player.max_health = 100 + skill.level * variables['health_per_level']
    player.health = player.max_health


skill_upgrade = player_spawn