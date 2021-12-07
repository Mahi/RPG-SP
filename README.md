# RPG:SP
RPG plugin for [Source.Python](https://sourcepython.com/).

## About
RPG:SP is a server-sided role-playing mod for CS:GO, built with Source.Python.

RPG:SP extends the game's player objects with an experience system and
a set of *skills* — additional powers for players to spice up the game with.

The objective is to gain experience points (*XP* for short) by attacking the opposing team's players.
Reaching enough XP will level your player up, granting you *credits* that can be spent to upgrade your skills.

## Skills
Here's a list of the pre-implemented skills:

- Health+ — Increase maximum health.
- Regeneration — Regenerate lost health over time.
- Long Jump — Travel further with jumps.
- Vampirism — Steal health with attacks.
- Impulse — Gain temporary speed boost when attacked.
- Stealth — Become partially invisible.
- Ice Stab — Freeze the enemy with the stronger knife stab.

But you can always implement more skills yourself (or make an issue in GitHub)!
You should start from the `addons/source-python/plugins/rpg/skills/README.md` file
and see the pre-implemented skills for more examples.

## Installation
Before installing RPG:SP onto your game server, you must first install the following dependencies:

- [Source.Python](http://sourcepython.com) to run Python plugins on the server
- [EasyPlayer](https://github.com/Mahi/EasyPlayer) to allow additional player effects for the skills
- [`PyYAML`](https://pypi.org/project/PyYAML/) to parse skills from YAML files

Once that's done,

1. download RPG:SP's latest version from the [releases page](https://github.com/Mahi/RPG-SP/releases)
2. locate the `addons` and `resource` folders inside of the downloaded `.zip` file
3. extract the two folders into your game folder
4. load the plugin with the `sp plugin load rpg` command

It's highly recommended to put the `sp plugin load rpg` command into your server's `autoexec.cfg`
so that the plugin gets loaded automatically whenever the server is started. 
