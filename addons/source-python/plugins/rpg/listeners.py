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
