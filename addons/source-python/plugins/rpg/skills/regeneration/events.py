from listeners.tick import Repeat


def init(player, skill):
    skill.tick_repeat = Repeat(_tick)


def _tick(stop_ticking, player, regeneration_per_tick):
    player.health = min(player.health + regeneration_per_tick, player.max_health)
    if player.health >= player.max_health:
        stop_ticking()


def player_victim(skill, player, variables, **eargs):
    regeneration_per_second = skill.level * variables['regeneration_per_second_per_level']
    skill.tick_repeat.args = (skill.tick_repeat.stop, player, regeneration_per_second)
    skill.tick_repeat.start(1)


skill_upgrade = player_victim


def player_death(skill, **eargs):
    skill.tick_repeat.stop()


player_disconnect = player_death


def player_downgrade_skill(skill, **eargs):
    if skill.level == 0:
        skill.tick_repeat.stop()
