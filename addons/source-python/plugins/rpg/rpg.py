# Python imports
from typing import Dict

# Source.Python imports
from commands import CommandReturn
from commands.client import ClientCommand
from commands.say import SayCommand
from listeners.tick import Repeat
from events import Event
from menus import ListMenu
from menus import ListOption
from menus import PagedMenu
from menus import PagedOption
from menus import Text
from messages import SayText2
from paths import PLUGIN_PATH
from players.dictionary import PlayerDictionary
from players.helpers import index_from_userid
from translations.strings import LangStrings

# RPG:GO imports
import rpg.builder
import rpg.config
import rpg.database
import rpg.listeners
import rpg.player
import rpg.skill
import rpg.utils


# Translations
_tr = LangStrings('rpg')


# ========================
#  Player management
# ========================

def new_player(index: int) -> rpg.player.Player:
    """Create and prepare a new `rpg.player.Player` instance.

    Initializes the player object with instances of each RPG skill.
    Loads the player's data from the database,
    or creates the data if it's a new player.
    """
    player = rpg.player.Player(index)
    for skill_type in skill_types.values():
        player.add_skill(rpg.skill.Skill(skill_type))

    if not rpg.database.load_player(player):
        rpg.database.create_player(player)

    return player


skill_types: Dict[str, rpg.skill.SkillType] = rpg.builder.build_skill_types(PLUGIN_PATH / 'rpg' / 'skills')
players: Dict[int, rpg.player.Player] = PlayerDictionary(new_player)


def save_all_players():
    for player in players.values():
        rpg.database.save_player(player)


def unload():
    _data_save_repeat.stop()
    save_all_players()


@Event('player_disconnect')
def save_player_data_on_disconnect(event):
    index = index_from_userid(event['userid'])
    if index not in players:
        return
    rpg.database.save_player(players[index])
    del players[index]


_data_save_repeat = Repeat(save_all_players)
_data_save_repeat.start(240, 0)


# ========================
#  Menus
# ========================

def _on_main_menu_build(menu, player_index):
    """Build the main menu."""
    player = players[player_index]
    menu.clear()
    menu.description = _tr['Credits'].get_string(credits=player.credits)
    menu.extend([
        PagedOption(_tr['Upgrade Skills'], upgrade_skills_menu),
        PagedOption(_tr['Downgrade Skills'], downgrade_skills_menu),
        PagedOption(_tr['Skill Descriptions'], skill_descriptions_menu),
        PagedOption(_tr['Stats'], stats_menu),
    ])

def _on_main_menu_select(menu, player_index, choice):
    """React to a main menu selection."""
    return choice.value

main_menu = PagedMenu(
    title=_tr['Main Menu'],
    build_callback=_on_main_menu_build,
    select_callback=_on_main_menu_select,
)


def _on_upgrade_skills_menu_build(menu, player_index):
    """Build the upgrade skills menu."""
    player = players[player_index]
    menu.clear()
    menu.description = _tr['Credits'].get_string(credits=player.credits)
    for skill in player.skills:
        cost_text = _tr['Cost'].get_string(cost=skill.upgrade_cost)
        text = f'{skill.name.get_string()} [{skill.level}/{skill.max_level}] ({cost_text})'
        can_upgrade = player.can_upgrade_skill(skill)
        menu.append(PagedOption(text, skill, highlight=can_upgrade, selectable=can_upgrade))

def _on_upgrade_skills_menu_select(menu, player_index, choice):
    """React to an upgrade skills menu selection."""
    player = players[player_index]
    player.upgrade_skill(choice.value)
    return menu

upgrade_skills_menu = PagedMenu(
    title=_tr['Upgrade Skills'],
    parent_menu=main_menu,
    build_callback=_on_upgrade_skills_menu_build,
    select_callback=_on_upgrade_skills_menu_select,
)


def _on_downgrade_skills_menu_build(menu, player_index):
    """Build the downgrade skills menu."""
    player = players[player_index]
    menu.clear()
    menu.description = _tr['Credits'].get_string(credits=player.credits)
    for skill in player.skills:
        text = _tr['Skill Text'].get_string(skill=skill, credits=skill.downgrade_refund)
        can_downgrade = player.can_downgrade_skill(skill)
        menu.append(PagedOption(text, skill, highlight=can_downgrade, selectable=can_downgrade))

def _on_downgrade_skills_menu_select(menu, player_index, choice):
    """React to a downgrade skills menu selection."""
    player = players[player_index]
    player.downgrade_skill(choice.value)
    return menu

downgrade_skills_menu = PagedMenu(
    title=_tr['Downgrade Skills'],
    parent_menu=main_menu,
    build_callback=_on_downgrade_skills_menu_build,
    select_callback=_on_downgrade_skills_menu_select,
)


def _on_skill_descriptions_menu_build(menu, player_index):
    """Build the skill descriptions menu."""
    player = players[player_index]
    menu.clear()
    menu.description = _tr['Credits'].get_string(credits=player.credits)
    menu.extend([
        ListOption(f'{skill.name.get_string()}\n{skill.description.get_string()}')
        for skill in player.skills
    ])

skill_descriptions_menu = ListMenu(
    title=_tr['Skill Descriptions'],
    parent_menu=main_menu,
    items_per_page=3,
    build_callback=_on_skill_descriptions_menu_build,
)


def _on_stats_menu_build(menu, player_index):
    """Build the stats menu."""
    player = players[player_index]
    menu.clear()
    menu.description = _tr['Credits'].get_string(credits=player.credits)
    menu.extend([
        Text(_tr['Level'].get_string(player=player)),
        Text(_tr['XP'].get_string(player=player)),
    ])

stats_menu = ListMenu(
    title=_tr['Stats'],
    parent_menu=main_menu,
    items_per_page=6,
    build_callback=_on_stats_menu_build,
)


# ========================
#  Skill triggering
# ========================

@Event('player_jump', 'player_spawn', 'player_disconnect')
def trigger_solo_player_callbacks(event):
    """Trigger skill callbacks for events with only one player.

    Also makes sure the player is in a valid team to prevent
    accidental errors with spectators and unassigned players.
    """
    event_args = event.variables.as_dict()
    player = players.from_userid(event_args.pop('userid'))
    if player.team not in (2, 3):
        return
    player.trigger_skills(event.name, **event_args)


_DUO_PLAYER_EVENTS = {
    'player_death': ('player_kill', 'player_death', 'player_suicide'),
    'player_hurt': ('player_attack', 'player_victim', 'player_selfharm'),
}

@Event('player_death', 'player_hurt')
def trigger_duo_player_callbacks(event):
    """Trigger skill callbacks for events with multiple participants.

    Finds the corresponding attacker and victim event names
    from the `_DUO_PLAYER_EVENTS` dict.
    """
    event_args = event.variables.as_dict()
    if event['attacker']:
        attacker = players.from_userid(event_args.pop('attacker'))
    else:
        attacker = None
    victim = players.from_userid(event_args.pop('userid'))
    event_args.update(attacker=attacker, victim=victim)

    (attack_event, victim_event, selfvictim_event) = _DUO_PLAYER_EVENTS[event.name]
    if attacker is None:
        victim.trigger_skills(selfvictim_event, **event_args)
    else:
        attacker.trigger_skills(attack_event, **event_args)
        victim.trigger_skills(victim_event, **event_args)


@rpg.listeners.OnPlayerUpgradeSkill
def trigger_skill_upgrade_callbacks(player, skill, **event_args):
    """Trigger skill callbacks for player upgrading a skill."""
    player.trigger_skills('player_upgrade_skill', skill=skill, **event_args)
    skill.trigger('skill_upgrade', skill=skill, player=player, **event_args)


@rpg.listeners.OnPlayerDowngradeSkill
def trigger_skill_downgrade_callbacks(player, skill, **event_args):
    """Trigger skill callbacks for player downgrading a skill."""
    player.trigger_skills('player_downgrade_skill', skill=skill, **event_args)
    skill.trigger('skill_downgrade', skill=skill, player=player, **event_args)


# ========================
#  Misc callbacks
# ========================

@ClientCommand('rpg')
@SayCommand('rpg')
def send_rpg_menu(command, player_index, team_only=None):
    """Send rpg menu to the player using the command."""
    main_menu.send(player_index)
    players[player_index].give_xp(500000)
    return CommandReturn.BLOCK


@Event('player_death')
def give_kill_xp(event):
    """Give the attacker XP for killing the victim."""
    if not event['attacker'] or event['attacker'] == event['userid']:
        return
    attacker = players.from_userid(event['attacker'])
    victim = players.from_userid(event['userid'])
    xp_on_kill = rpg.config.XP_GAIN['on_kill']
    attacker.give_xp(xp_on_kill['base'] + victim.level * xp_on_kill['per_level_difference'])


@Event('player_hurt')
def give_hurt_xp(event):
    """Give the attacker XP for hurting the victim."""
    if not event['attacker'] or event['attacker'] == event['userid']:
        return
    attacker = players.from_userid(event['attacker'])
    attacker.give_xp(int(event['dmg_health'] * rpg.config.XP_GAIN['on_damage']['per_damage']))


_level_up_message = SayText2(_tr['Level Up Message'])

@rpg.listeners.OnPlayerLevelUp
def upgrade_player_skill(player, levels, credits):
    """Send a level up message to the leveling player."""
    if player.steamid != 'BOT':
        _level_up_message.send(player.index, player=player)
        upgrade_skills_menu.send(player.index)

    else:  # Force bots to upgrade random skills
        for skill in rpg.utils.shuffled(player.skills):
            if player.can_upgrade_skill(skill):
                player.upgrade_skill(skill)
                break
