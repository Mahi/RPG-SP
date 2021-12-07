# Python imports
from collections import OrderedDict
from typing import Any, Dict, Iterable, Optional

# Custom package imports
import easyplayer

# RPG imports
from .config import REQUIRED_XP
from .listeners import OnPlayerDowngradeSkill, OnPlayerLevelUp, OnPlayerUpgradeSkill
from .skill import Skill


class Player(easyplayer.Player):
    """RPG player class with leveling system and skills.

    Implements the leveling system with `xp` and `level` attributes.
    Leveling up grants `credits`, which can be spent
    to upgrade the player's skills to give them bonus powers.

    Subclasses `easyplayer.Player` for its player effects.
    """

    def __init__(self,
        index: int,
        *,
        level: int=0,
        xp: int=0,
        credits: int=0,
    ) -> None:
        super().__init__(index)
        self._level = level
        self._xp = xp
        self.credits = credits
        self._skills = OrderedDict()

    def add_skill(self, skill: Skill) -> None:
        """Add a skill for the player.
        
        Calls the skill's `init_callback`, if any.
        """
        self._skills[skill.key] = skill
        if skill._init_callback is not None:
            skill._init_callback(player=self, skill=skill)

    def get_skill(self, key: str) -> Optional[Skill]:
        """Get a skill by it's key."""
        return self._skills.get(key)

    @property
    def skills(self) -> Iterable[Skill]:
        """Iterate the player's skills."""
        return iter(self._skills.values())

    @property
    def level(self) -> int:
        """Player's current level."""
        return self._level

    @property
    def xp(self) -> int:
        """Player's current XP progress."""
        return self._xp

    @property
    def required_xp(self) -> int:
        """XP required to reach the next level."""
        return REQUIRED_XP['base'] + REQUIRED_XP['per_level'] * self.level

    def give_xp(self, amount: int) -> None:
        """Give experience points to the player.

        Grants levels and credits when the player levels up.
        """
        if amount < 0:
            raise ValueError(f"Negative amount '{amount}' passed for Player.give_xp()")

        initial_level, initial_credits = self.level, self.credits

        self._xp += amount
        while self.xp >= self.required_xp:
            self._xp -= self.required_xp
            self._level += 1
            self.credits += 5

        if initial_level < self.level:
            OnPlayerLevelUp.manager.notify(
                player=self,
                levels=initial_level - self.level,
                credits=initial_credits - self.credits,
            )

    def set_level(self, value: int) -> None:
        """Set a player's level.
        
        Resets the current XP to zero.
        """
        if value < 0:
            raise ValueError(f"Negative value '{value}' passed for Player.set_level()")
        self._level = value
        self._xp = 0

    def reset_rpg_progress(self) -> None:
        """Completely reset player's RPG progress.

        Resets level, XP, credits, and all the levels of each skill.
        """
        self._level = 0
        self._xp = 0
        self.credits = 0
        for skill in self.skills:
            skill.level = 0

    def can_upgrade_skill(self, skill: Skill) -> bool:
        """Check if a player can upgrade his skill.

        Returns whether the skill can be upgraded or not.
        """
        return (
            self.credits >= skill.upgrade_cost
            and skill.max_level > skill.level
        )

    def can_downgrade_skill(self, skill: Skill) -> bool:
        """Check if a player can downgrade his skill.

        Returns whether the skill can be downgraded or not.
        """
        return skill.level > 0

    def upgrade_skill(self, skill: Skill) -> None:
        """Upgrade the player's skill's level by one.

        Raises RuntimeError if the skill can't be upgraded.
        """
        if not self.can_upgrade_skill(skill):
            raise RuntimeError(f"Unable to upgrade {self.name}'s skill '{skill.name}'")
        self.credits -= skill.upgrade_cost
        skill.level += 1
        OnPlayerUpgradeSkill.manager.notify(player=self, skill=skill)

    def downgrade_skill(self, skill: Skill) -> None:
        """Downgrade the player's skill's level by one.

        Raises RuntimeError if the skill can't be downgraded.
        """
        if not self.can_downgrade_skill(skill):
            raise RuntimeError(f"Unable to downgrade {self.name}'s skill '{skill.name}'")
        self.credits += skill.downgrade_refund
        skill.level -= 1
        OnPlayerDowngradeSkill.manager.notify(player=self, skill=skill)

    def trigger_skills(self, event_name: str, **event_args: Dict[str, Any]) -> None:
        """Trigger each skill with matching event name.

        Ensures the skill has been leveled before trigger it.
        """
        for skill in self.skills:
            if skill.level > 0:
                event_args['player'] = self
                skill.trigger(event_name, **event_args)
