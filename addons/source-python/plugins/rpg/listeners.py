# Source.Python imports
from listeners import ListenerManager
from listeners import ListenerManagerDecorator


class OnPlayerLevelUp(ListenerManagerDecorator):
    """Listener to notify when a player levels up.

    Arguments for callbacks:
        player: Player who leveled up
        levels: Amount of levels gained
        credits: Amount of credits gained
    """
    manager = ListenerManager()


class OnPlayerUpgradeSkill(ListenerManagerDecorator):
    """Listener to notify when a player upgrades one of his skills.

    Arguments for callbacks:
        player: Player who upgraded a skill
        skill: Skill being upgraded
        levels: Amount of levels upgraded
    """
    manager = ListenerManager()


class OnPlayerDowngradeSkill(ListenerManagerDecorator):
    """Listener to notify when a player downgrades one of his skills.

    Arguments for callbacks:
        player: Player who downgraded a skill
        skill: Skill being downgraded
        levels: Amount of levels downgraded
    """
    manager = ListenerManager()
