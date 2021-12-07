def init(player, skill):
    skill._delay = None


def player_victim(player, skill, variables, **eargs):
    if skill._delay is not None and skill._delay.running:
        return  # Limit to one speed boost
    amount = variables['boost']['base'] + variables['boost']['per_level'] * skill.level
    duration = variables['duration']['base'] + variables['duration']['per_level'] * skill.level
    skill._delay = player.shift_property('speed', amount, duration)


def player_death(skill, **eargs):
    if skill._delay is not None and skill._delay.running:
        skill._delay.cancel()
        skill._delay = None


player_disconnect = player_death
