def player_attack(skill, player, variables, dmg_health, **eargs):
    attempt_heal = int(dmg_health * skill.level * variables['heal_per_damage_per_level'])
    heal = max(attempt_heal, skill.level * variables['maximum_heal_per_level'])
    player.health = min(player.health + heal, player.max_health)