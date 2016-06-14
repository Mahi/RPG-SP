from players.dictionary import PlayerDictionary

import rpg.player
import rpg.skill
import rpg.skills
import rpg.utils


def _new_player(index):
    """Create and prepare a new :class:`rpg.player.Player` instance.

    Initializes the player object with instances of each RPG skill.

    :param int index:
        Index of the player entity
    :returns rpg.player.Player:
        The RPG player entity
    """
    player = rpg.player.Player(index)
    player.skills.extend(skill() for skill in _skills)
    return player


# Globals
_players = PlayerDictionary(_new_player)
_skills = list(rpg.utils.get_subclasses(rpg.skill.Skill))
