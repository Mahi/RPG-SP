from listeners.tick import TickRepeat

from rpg.skill import callback, Skill


class Health(Skill):
    "Gain +25 health for each level on spawn."
    max_level = 16

    @callback('player_spawn')
    def _spawn(self, player, **eargs):
        player.health += self.level * 25


class Regenerate(Skill):
    "Regenerate +1 health for each level every second."
    max_level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeat = TickRepeat(self._tick)

    @callback('player_victim')
    def _start_repeat(self, player, **eargs):
        self._repeat.args = (player, self._find_health_skill(player))
        self._repeat.start(1, 0)

    @callback('player_death')
    def _stop_repeat(self, **eargs):
        self._repeat.stop()

    def _tick(self, player, health_skill):
        health_bonus = health_skill.level * 25 if health_skill else 0
        if player.health < 100 + health_bonus:
            player.health = min(player.health + self.level, 100 + health_bonus)
        else:
            self._repeat.stop()

    def _find_health_skill(self, player):
        for skill in player.skills:
            if type(skill) == Health:
                return skill
        return None


class Long_Jump(Skill):
    "Travel much further with your jumps."
    max_level = 6

    @callback('player_jump')
    def _jump_further(self, player, **eargs):
        player.push(1 + 0.25 * self.level, 1)
