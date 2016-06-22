import operator

from commands import CommandReturn
from commands.client import ClientCommand
from commands.say import SayCommand
from events import Event
from paths import PLUGIN_DATA_PATH
from players.dictionary import PlayerDictionary
from players.helpers import index_from_userid
from players.helpers import playerinfo_from_index

import rpg.database
import rpg.listeners
import rpg.menus
import rpg.player
import rpg.skills


# ======================================================================
# >> FUNCTIONS
# ======================================================================

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
    for skill_cls in rpg.skills.skills:
        skill_data = _database.load_skill_data(steamid, skill_cls.class_id)
        player.skills.append(skill_cls(*skill_data))
    return player


def _save_player_data(player):
    """Save player's RPG data into the database."""
    _database.save_player_data(player.steamid, player.level, player.xp, player.credits)
    for skill in player.skills:
        _database.save_skill_data(player.steamid, skill.class_id, skill.level)


# ======================================================================
# >> GLOBALS
# ======================================================================

_database = rpg.database.Database(PLUGIN_DATA_PATH / 'rpg.db')
_players = PlayerDictionary(_new_player)


# ======================================================================
# >> DATABASE EVENT CALLBACKS
# ======================================================================

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


# ======================================================================
# >> SKILL EXECUTION EVENT CALLBACKS
# ======================================================================

@Event('player_jump', 'player_spawn')
def _execute_independent_skill_callbacks(event):
    """Execute skill callbacks for events with only one user.

    Also makes sure the player is in a valid team to prevent
    accidental errors with spectators and unassigned players.
    """
    event_args = event.variables.as_dict()
    player = _players.from_userid(event_args.pop('userid'))
    if player.team not in (2, 3):
        return
    player.execute_skill_callbacks(event.name, **event_args)


_event_names = {
    # event.name: (attacker_event_name, victime_event_name),
    'player_death': ('player_kill', 'player_death'),
    'player_hurt': ('player_attack', 'player_victim'),
}

@Event('player_death', 'player_hurt')
def _execute_interaction_skill_callbacks(event):
    """Execute skill callbacks for events with multiple participants.

    Takes the game event's name and finds the corresponding
    attacker and victim event names from the ``_event_names`` dict.
    """
    if not event['attacker'] or event['attacker'] == event['userid']:
        return
    event_args = event.variables.as_dict()
    attacker = _players.from_userid(event_args.pop('attacker'))
    victim = _players.from_userid(event_args.pop('userid'))
    event_args.update(attacker=attacker, victim=victim)
    attacker.execute_skill_callbacks(_event_names[event.name][0], **event_args)
    victim.execute_skill_callbacks(_event_names[event.name][1], **event_args)


@rpg.listeners.OnPlayerUpgradeSkill
def _execute_skill_upgrade_skill_callbacks(player, skill, **event_args):
    """Execute skill callbacks for player upgrading a skill.

    Executes ``player_upgrade_skill`` on all player's skills,
    and ``skill_upgrade`` on the skill being upgraded.
    """
    player.execute_skill_callbacks('player_upgrade_skill', skill=skill, **event_args)
    skill.execute_callbacks('skill_upgrade', player=player, **event_args)


@rpg.listeners.OnPlayerDowngradeSkill
def _execute_skill_downgrade_skill_callbacks(player, skill, **event_args):
    """Execute skill callbacks for player downgrading a skill.

    Executes ``player_downgrade_skill`` on all player's skills,
    and ``skill_upgrade`` on the skill being downgraded.
    """
    player.execute_skill_callbacks('player_downgrade_skill', skill=skill, **event_args)
    skill.execute_callbacks('skill_downgrade', player=player, **event_args)


# ======================================================================
# >> MISCELLANEOUS CALLBACKS
# ======================================================================

@ClientCommand('rpg')
@SayCommand('rpg')
def _send_rpg_menu(command, player_index, team_only=None):
    """Send rpg menu to the player using the command."""
    menu = rpg.menus.MainMenu(_players[player_index])
    menu.send(player_index)
    return CommandReturn.BLOCK


@Event('player_death')
def _give_kill_xp(event):
    """Give attacker XP from killing the victim."""
    if not event['attacker'] or event['attacker'] == event['userid']:
        return
    attacker = _players.from_userid(event['attacker'])
    victim = _players.from_userid(event['userid'])
    attacker.give_xp(victim.level)


@Event('player_hurt')
def _give_hurt_xp(event):
    """Give attacker XP from hurting the victim."""
    if not event['attacker'] or event['attacker'] == event['userid']:
        return
    attacker = _players.from_userid(event['attacker'])
    attacker.give_xp(event['dmg_health'])
