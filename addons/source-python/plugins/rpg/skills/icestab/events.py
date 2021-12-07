from players.constants import PlayerButtons


def player_attack(player, skill, victim, weapon, variables, **eargs):
    if weapon == 'knife' and player.buttons & PlayerButtons.ATTACK2:
        victim.freeze(variables['duration_per_level'] * skill.level)