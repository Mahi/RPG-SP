from listeners.tick import TickRepeat

from rpg.skill import callback, Skill


class Health(Skill):
    "Gain +25 health for each level on spawn."
    max_level = 16

    @property
    def bonus_health(self):
        return self.level * 25

    @callback('player_spawn')
    def _give_bonus_health(self, player, **eargs):
        player.health += self.bonus_health


class Regenerate(Skill):
    "Regenerate +1 health for each level every second."
    max_level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeat = TickRepeat(self._tick)

    def _tick(self, player, health_skill):
        max_health = 100 + health_skill.health_bonus
        player.health = min(player.health + self.level, max_health)
        if player.health >= max_health:
            self._repeat.stop()

    @callback('player_victim', 'player_upgrade_skill')
    def _start_repeat(self, player, **eargs):
        self._repeat.args = (player, player.find_skill(Health.class_id))
        self._repeat.start(1, 0)

    @callback('player_death')
    def _stop_repeat(self, **eargs):
        self._repeat.stop()

    @callback('player_downgrade_skill')
    def _stop_repeat_if_fully_downgraded(self, skill, **eargs):
        if skill == self and skill.level <= 0:
            self._repeat.stop()


class Long_Jump(Skill):
    "Travel much further with your jumps."
    max_level = 6

    @property
    def jump_multiplier(self):
        return 1 + 0.25 * self.level

    @callback('player_jump')
    def _jump_further(self, player, **eargs):
        player.push(self.jump_multiplier, 1)
