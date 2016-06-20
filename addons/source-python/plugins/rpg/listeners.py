from listeners import ListenerManager
from listeners import ListenerManagerDecorator


class OnPlayerLevelUp(ListenerManagerDecorator):
    """Listener to notify when a player levels up.

    Arguments for callbacks:
        :class:`rpg.player.Player` player: Player who leveled up
        :class:`int` levels: Amount of levels gained
        :class:`int` credits: Amount of credits gained
    """
    manager = ListenerManager()


class OnPlayerUpgradeSkill(ListenerManagerDecorator):
    """Listener to notify when a player upgrades one of his skills.

    Arguments for callbacks:
        :class:`rpg.player.Player` player: Player who upgraded a skill
        :class:`rpg.skill.Skill` skill: Skill being upgraded
    """
    manager = ListenerManager()


class OnPlayerDowngradeSkill(ListenerManagerDecorator):
    """Listener to notify when a player downgrades one of his skills.

    Arguments for callbacks:
        :class:`rpg.player.Player` player: Player who downgraded a skill
        :class:`rpg.skill.Skill` skill: Skill being upgraded
    """
    manager = ListenerManager()
