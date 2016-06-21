# RPG:GO
*The* RPG plugin for Source.Python

### About
RPG:GO is a server-sided role-playing mod for Counter-Strike: Global Offensive.
It extends the game's players with an experience system and a set of unique skills — additional powers for players to spice up the game with.

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

### Installation
Before installing RPG:GO onto your game server, you must first install the two dependencies:

- [Source.Python](http://sourcepython.com) to allow the Python programming language to be used with Source engine.
- [EasyPlayer](https://github.com/Mahi/EasyPlayer) to enable additional player effects.

Once that's done,

1. download [RPG:GO's latest version](https://github.com/Mahi/RPG-GO/archive/master.zip)
2. locate the `addons` folder inside of the downloaded `master.zip`
3. extract the `addons` folder into your game folder (so you end up having `csgo/addons` folder)
4. load the plugin with the `sp load rpg` command

It's highly recommended to put the `sp load rpg` command into your server's `autoexec.cfg` so that the plugin gets loaded automatically whenever the server is started. 
