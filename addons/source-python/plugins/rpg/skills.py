from rpg.skill import event_callback
from rpg.skill import Skill
from rpg.skill import TickRepeatSkill
from rpg.utils import DecoratorAppendList


# Global list for storing all the skills to be used by the plugin
skills = DecoratorAppendList()


@skills.append
class Health(Skill):
    "Increase maximum health."
    name = 'Health+'
    max_level = 16

    @property
    def bonus_amount(self):
        return self.level * 25

    @event_callback('skill_upgrade')
    def _give_level_bonus(self, player, **event_args):
        player.health += 25

    @event_callback('skill_downgrade')
    def _take_level_bonus(self, player, **event_args):
        if player.health > 100 + self.bonus_amount:
            player.health = 100 + self.bonus_amount

    @event_callback('player_spawn')
    def _give_bonus_health(self, player, **event_args):
        player.health += self.bonus_amount


@skills.append
class Regeneration(TickRepeatSkill):
    "Regenerate lost health over time."
    max_level = 5

    def _tick(self, player, health_skill):
        max_health = 100 + health_skill.bonus_amount
        player.health = min(player.health + self.level, max_health)
        if player.health >= max_health:
            self.tick_repeat.stop()

    @event_callback('player_victim', 'skill_upgrade')
    def _start_repeat(self, player, **event_args):
        self.tick_repeat.args = (player, player.find_skill(Health.class_id))
        self.tick_repeat.start(1, 0)

    @event_callback('player_death', 'player_disconnect')
    def _stop_repeat(self, **event_args):
        self.tick_repeat.stop()

    @event_callback('skill_downgrade')
    def _stop_repeat_if_fully_downgraded(self, **event_args):
        if self.level == 0:
            self.tick_repeat.stop()


@skills.append
class Long_Jump(Skill):
    "Travel further with jumps."
    max_level = 6

    @property
    def vertical_velocity_multiplier(self):
        return 1 + 0.05 * self.level

    @event_callback('player_jump')
    def _jump_further(self, player, **event_args):
        velocity = player.velocity
        velocity.x *= self.vertical_velocity_multiplier
        velocity.y *= self.vertical_velocity_multiplier
        player.base_velocity = velocity


@skills.append
class Vampirism(Skill):
    "Steal health with attacks."
    max_level = 5

    def get_steal_amount(self, damage_dealt):
        return min(damage_dealt * self.level // 10, 10 * self.level)

    @event_callback('player_attack')
    def _grant_health(self, player, dmg_health, **eargs):
        health_skill = player.find_skill(Health.class_id)
        new_health = player.health + self.get_steal_amount(dmg_health)
        max_health = 100 + health_skill.bonus_amount
        player.health = min(new_health, max_health)


@skills.append
class Blacksmith(TickRepeatSkill):
    "Generate armor over time."
    max_level = 5

    def _tick(self, player):
        player.armor = min(player.armor + self.level, 100)
        if player.armor >= 100:
            self.tick_repeat.stop()

    @event_callback('player_spawn', 'player_victim', 'skill_upgrade')
    def _start_repeat(self, player, **event_args):
        self.tick_repeat.args = (player,)
        self.tick_repeat.start(1, 0)

    @event_callback('player_death', 'player_disconnect')
    def _stop_repeat(self, **event_args):
        self.tick_repeat.stop()

    @event_callback('skill_downgrade')
    def _stop_repeat_if_fully_downgraded(self, **event_args):
        if self.level == 0:
            self.tick_repeat.stop()


@skills.append
class Impulse(Skill):
    "Gain temporary speed boost when attacked."
    max_level = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._delay = None

    @property
    def speed_amount(self):
        return 0.4 + self.level * 0.2

    @property
    def duration(self):
        return 1 + self.level * 0.1

    @event_callback('player_victim')
    def _give_temporary_speed_boost(self, player, **event_args):

        # Limit to one speed boost only
        if self._delay is not None and self._delay.running:
            return  

        self._delay = player.shift_property('speed', self.speed_amount, self.duration)

    @event_callback('player_death', 'player_disconnect')
    def _cancel_delay(self, **event_args):
        if self._delay is not None and self._delay.running:
            self._delay.cancel()


@skills.append
class Fire_Grenade(Skill):
    "Burn your enemy with grenades."
    max_level = 10

    @property
    def duration(self):
        return self.level / 2

    @event_callback('player_attack')
    def _burn_victim(self, victim, weapon, **event_args):
        if weapon == 'hegrenade':
            victim.burn(self.duration)
