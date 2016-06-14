from events import Event
from paths import PLUGIN_DATA_PATH
from players.dictionary import PlayerDictionary
from players.helpers import index_from_userid
from players.helpers import playerinfo_from_index

import rpg.database
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
    steamid = playerinfo_from_index(index).steamid
    player_data = _database.load_player_data(steamid)
    player = rpg.player.Player(index, *player_data)
    for skill_cls in _skill_classes:
        skill_data = _database.load_skill_data(steamid, skill_cls.class_id)
        player.skills.append(skill_cls(*skill_data))
    return player


# Globals
_database = rpg.database.Database(PLUGIN_DATA_PATH / 'rpg.db')
_players = PlayerDictionary(_new_player)
_skill_classes = list(rpg.utils.get_subclasses(rpg.skill.Skill))


def _save_player_data(player):
    """Save player's RPG data into the database."""
    _database.save_player_data(player.steamid, player.level, player.xp, player.credits)
    for skill in player.skills:
        _database.save_skill_data(player.steamid, skill.class_id, skill.level)


def unload():
    """Store players' data and close the the database."""
    for player in _players.values():
        _save_player_data(player)
    _database.commit()
    _database.close()


@Event('player_disconnect', 'player_spawn')
def _save_player_data_on_event(event):
    """Save player's RPG data into the database."""
    index = index_from_userid(event['userid'])
    if index not in _players:
        return
    _save_player_data(_players[index])
    _database.commit()


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
