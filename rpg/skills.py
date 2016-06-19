from rpg.skill import event_callback
from rpg.skill import Skill
from rpg.skill import TickRepeatSkill
from rpg.utils import DecoratorAppendList


# Global list for storing all the skills to be used by the plugin
skills = DecoratorAppendList()


@skills.append
class Health(Skill):
    "Gain +25 health for each level on spawn."
    max_level = 16

    @property
    def bonus_health(self):
        return self.level * 25

    @event_callback('player_upgrade_skill')
    def _give_level_bonus(self, player, skill, **event_args):
        if skill == self:
            player.health += 25

    @event_callback('player_downgrade_skill')
    def _take_level_bonus(self, player, skill, **event_args):
        if skill == self and player.health > 100 + self.bonus_health:
            player.health = 100 + self.bonus_health

    @event_callback('player_spawn')
    def _give_bonus_health(self, player, **event_args):
        player.health += self.bonus_health


@skills.append
class Regeneration(TickRepeatSkill):
    "Regenerate +1 health for each level every second."
    max_level = 5

    def _tick(self, player, health_skill):
        max_health = 100 + health_skill.bonus_health
        player.health = min(player.health + self.level, max_health)
        if player.health >= max_health:
            self.tick_repeat.stop()

    @event_callback('player_victim', 'player_upgrade_skill')
    def _start_repeat(self, player, **event_args):
        self.tick_repeat.args = (player, player.find_skill(Health.class_id))
        self.tick_repeat.start(1, 0)

    @event_callback('player_death')
    def _stop_repeat(self, **event_args):
        self.tick_repeat.stop()

    @event_callback('player_downgrade_skill')
    def _stop_repeat_if_fully_downgraded(self, skill, **event_args):
        if skill == self and skill.level <= 0:
            self.tick_repeat.stop()


@skills.append
class Long_Jump(Skill):
    "Travel much further with your jumps."
    max_level = 6

    @property
    def jump_multiplier(self):
        return 1 + 0.05 * self.level

    @event_callback('player_jump')
    def _jump_further(self, player, **event_args):
        velocity = player.velocity
        velocity.x *= self.jump_multiplier
        velocity.y *= self.jump_multiplier
        player.base_velocity = velocity


@skills.append
class Lifesteal(Skill):
    "Steal health from enemies upon damaging them."
    max_level = 5

    def get_steal_amount(self, damage_dealt):
        return min(damage_dealt * self.level // 10, 10 * self.level)

    @event_callback('player_attack')
    def _grant_health(self, player, dmg_health, **eargs):
        health_skill = player.find_skill(Health.class_id)
        new_health = player.health + self.get_steal_amount(dmg_health)
        max_health = 100 + health_skill.bonus_health
        player.health = min(new_health, max_health)


@skills.append
class Armor_Regeneration(TickRepeatSkill):
    "Regenerate +1 armor for each level every second."
    max_level = 5

    def _tick(self, player):
        player.armor = min(player.armor + self.level, 100)
        if player.armor >= 100:
            self.tick_repeat.stop()

    @event_callback('player_victim', 'player_upgrade_skill')
    def _start_repeat(self, player, **event_args):
        self.tick_repeat.args = (player,)
        self.tick_repeat.start(1, 0)

    @event_callback('player_death')
    def _stop_repeat(self, **event_args):
        self.tick_repeat.stop()

    @event_callback('player_downgrade_skill')
    def _stop_repeat_if_fully_downgraded(self, skill, **event_args):
        if skill == self and skill.level <= 0:
            self.tick_repeat.stop()
