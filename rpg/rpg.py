from event import Event
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


@Event('player_jump', 'player_spawn')
def _execute_independent_skill_callbacks(event):
    """Execute skill callbacks for events with only one user.

    Also makes sure the player is in a valid team to prevent
    accidental errors with spectators and unassigned players.
    """
    eargs = event.variables.as_dict()
    player = _players.from_userid(eargs.pop('userid'))
    if player.team not in (2, 3):
        return
    player.execute_skill_callbacks(event.name, player=player, **eargs)


_event_names = {
    # event.name: (attacker_event_name, victime_event_name),
    'player_death': ('player_kill', 'player_death'),
    'player_hurt': ('player_attack', 'player_victim'),
}

@Event('player_death', 'player_hurt')
def _execute_interaction_skill_callbacks(event):
    """Execute skill callbacks for events with multiple participants."""
    eargs = event.variables.as_dict()
    attacker = _players.from_userid(eargs.pop('attacker'))
    victim = _players.from_userid(eargs.pop('userid'))
    if attacker is None or attacker == victim:
        return
    eargs.update(attacker=attacker, victim=victim)
    attacker.execute_skill_callbacks(
        _event_names[event.name][0], player=attacker, **eargs)
    victim.execute_skill_callbacks(
        _event_names[event.name][1], player=victim, **eargs)
