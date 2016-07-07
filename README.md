# RPG:SP
*The* RPG plugin for Source.Python

### About
RPG:SP is a server-sided role-playing mod built with Source.Python.
It has been tested only on CS:GO and CS:S, but should work fine on most Source engine games.

RPG:SP extends the game's players with an experience system and a set of unique skills — additional powers for players to spice up the game with.
The objective is to gain experience points (XP for short) by attacking the opposing team's players.
Once a player gains enough XP to fill his XP quota, the player will level up and gain credits, which can be spent to upgrade the player's skills.
Each of these skills provides an unique effect for the player, allowing him to gain an advantage over a normal player.

### Skills
Here's a list of the current skills and a short description for each:

- Health+ — Increase maximum health.
- Regeneration — Regenerate lost health over time.
- Long Jump — Travel further with jumps.
- Vampirism — Steal health with attacks.
- Blacksmith — Generate armor over time.
- Impulse — Gain temporary speed boost when attacked.
- Fire Grenade — Burn your enemies with grenades.
- Ice Stab — Freeze the enemy with the stronger knife stab.

### Installation
Before installing RPG:SP onto your game server, you must first install the two dependencies:

- [Source.Python](http://sourcepython.com) to allow the Python programming language to be used with the Source engine.
- [EasyPlayer](https://github.com/Mahi/EasyPlayer) to enable additional player effects.

Once that's done,

1. download [RPG:SP's latest version](https://github.com/Mahi/RPG-SP/archive/master.zip)
2. locate the `addons` folder inside of the downloaded `master.zip`
3. extract the `addons` folder into your game folder (so you end up having f.e. `csgo/addons` folder)
4. load the plugin with the `sp load rpg` command

It's highly recommended to put the `sp load rpg` command into your server's `autoexec.cfg` so that the plugin gets loaded automatically whenever the server is started. 
