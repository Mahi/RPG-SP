from commands import CommandReturn
from commands.client import ClientCommand
from commands.say import SayCommand
from events import Event
from listeners.tick import TickRepeat
from menus import ListMenu
from menus import PagedMenu
from menus import PagedOption
from menus import Text
from paths import PLUGIN_DATA_PATH
from players.dictionary import PlayerDictionary
from players.helpers import index_from_userid
from players.helpers import playerinfo_from_index
from translations.strings import LangStrings

import rpg.database
import rpg.listeners
import rpg.player
import rpg.skills
import rpg.utils


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
_tr = LangStrings('rpg')


# ======================================================================
# >> DATABASE FUNCTIONS
# ======================================================================

def unload():
    """Store players' data and close the the database."""
    _data_save_repeat.stop()
    _save_everyones_data()
    _database.close()


@Event('player_disconnect')
def _save_player_data_upon_disconnect(event):
    """Save player's RPG data into the database."""
    index = index_from_userid(event['userid'])
    if index not in _players:
        return
    _save_player_data(_players[index])
    del _players[index]


def _save_everyones_data():
    """Save every player's RPG data into the database."""
    for player in _players.values():
        _save_player_data(player)
    _database.commit()

_data_save_repeat = TickRepeat(_save_everyones_data)
_data_save_repeat.start(240, 0)


# ======================================================================
# >> SKILL EXECUTION EVENT CALLBACKS
# ======================================================================

@Event('player_jump', 'player_spawn', 'player_disconnect')
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
    event_args = event.variables.as_dict()
    if event['attacker']:
        attacker = _players.from_userid(event_args.pop('attacker'))
    else:
        attacker = None
    victim = _players.from_userid(event_args.pop('userid'))
    event_args.update(attacker=attacker, victim=victim)
    if attacker is not None:
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
    main_menu.send(player_index)
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


@rpg.listeners.OnPlayerLevelUp
def _make_bots_upgrade_skills(player, levels, credits):
    """Selects an unupgraded skill and levels it."""
    if player.steamid != 'BOT':
        return
    for skill in rpg.utils.shuffled(player.skills):
        if player.can_upgrade_skill(skill):
            player.upgrade_skill(skill)
            break


# ======================================================================
# >> MENUS
# ======================================================================

def _on_main_menu_build(menu, player_index):
    """Build the main menu."""
    player = _players[player_index]
    menu.clear()
    menu.description = 'Credits: {0}'.format(player.credits)
    menu.extend([
        PagedOption('Upgrade Skills', upgrade_skills_menu),
        PagedOption('Downgrade Skills', downgrade_skills_menu),
        PagedOption('Stats', stats_menu),
    ])

def _on_main_menu_select(menu, player_index, choice):
    """React to a main menu selection."""
    player = _players[player_index]
    return choice.value

main_menu = PagedMenu(
    title='RPG Main Menu',
    build_callback=_on_main_menu_build,
    select_callback=_on_main_menu_select,
)


def _on_upgrade_skills_menu_build(menu, player_index):
    """Build the upgrade skills menu."""
    player = _players[player_index]
    menu.clear()
    menu.description = 'Credits: {0}'.format(player.credits)
    text = '{s.name} [{s.level}/{s.max_level}] ({s.upgrade_cost} credits)'
    menu.extend([
        PagedOption(text.format(s=skill), skill)
        for skill in player.skills
    ])

def _on_upgrade_skills_menu_select(menu, player_index, choice):
    """React to an upgrade skills menu selection."""
    player = _players[player_index]
    player.upgrade_skill(choice.value)
    return menu

upgrade_skills_menu = PagedMenu(
    title='Upgrade Skills',
    parent_menu=main_menu,
    build_callback=_on_upgrade_skills_menu_build,
    select_callback=_on_upgrade_skills_menu_select,
)


def _on_downgrade_skills_menu_build(menu, player_index):
    """Build the downgrade skills menu."""
    player = _players[player_index]
    menu.clear()
    menu.description = 'Credits: {0}'.format(player.credits)
    text = '{s.name} [{s.level}/{s.max_level}] ({s.downgrade_refund} credits)'
    menu.extend([
        PagedOption(text.format(s=skill), skill)
        for skill in player.skills
    ])

def _on_downgrade_skills_menu_select(menu, player_index, choice):
    """React to a downgrade skills menu selection."""
    player = _players[player_index]
    player.downgrade_skill(choice.value)
    return menu

downgrade_skills_menu = PagedMenu(
    title='Downgrade Skills',
    parent_menu=main_menu,
    build_callback=_on_downgrade_skills_menu_build,
    select_callback=_on_downgrade_skills_menu_select,
)


def _on_stats_menu_build(menu, player_index):
    """Build the stats menu."""
    player = _players[player_index]
    menu.clear()
    menu.description = 'Credits: {0}'.format(player.credits)
    menu.append(Text('Level: {0}'.format(player.level)))
    menu.append(Text('XP: {0}/{1}'.format(player.xp, player.required_xp)))

stats_menu = ListMenu(
    title='Stats',
    parent_menu=main_menu,
    items_per_page=6,
    build_callback=_on_stats_menu_build,
)
