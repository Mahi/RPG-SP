# RPG:GO skills directory

Add any RPG:GO skills to this directory.

Each skill should be its own directory, with the following files in it:
```
rpg/
  skills/
    my_custom_skill/
      data.yml
      events.py
      strings.ini
```

The name of the skill's directory is used as its unique identifier `key`,
so modifying the directory name **will** remove all player progress for that skill.
This functionality can be overridden by providing a `key` attribute
in the skill's `data.yml` file (see `data.yml` below).

If a `rpg/skills/skills.txt` file is provided, that file will be used to determine
1. which skills are loaded by the mod and
2. in which order are the skills listed for players.

If file is missing, then *all* skills in the `rpg/skills` directory will be loaded,
and they will be listed in an alphabetical order.

## `data.yml`
The `data.yml` file holds all numeric data of the skill in it.
Separating the data from the code allows easy fine tuning and re-balancing,
without having to touch the underlying code.

The data should be in the format of:
```yml
max_level: <integer>
author: <string>  # Optional
variables:
  my_custom_variable: <any>
```
The `variables` can be literally anything, and the whole structure
will be passed to the event handles as a Python dictionary.

## `strings.ini`
This file simply contains any translation strings your skill needs.
It uses Source.Python's `TranslationStrings`/`LangStrings`,
so the file should be of the format:
```ini
[name]
en = "My Custom Skill"
fi = "Mun Oma Skilli"

[description]
en = "This is a very good skill."
fi = "Tämä on todella hyvä skilli."

[custom_field]
en = "I could have named this custom_field anything."
fi = "Olisin voinut nimetä tämän custom_field:in miten haluan."
```
By defauly you should provide `[name]` and `[description]`,
as they are used by the mod internally, but you can also provide any
additional strings your skill might need, for example for chat messages.

## `events.py`
This file holds the actual executable code for the skill.
Populate this script with module-level event callbacks,
where the callback's name name matches an event's name.

These event callbacks will receive the following arguments:
- `player`: The player who is triggering the event
- `skill`: The skill that was triggered (`self`/`this`)
- `variables`: The `variables` field from the skill's `data.yml` file
- `strings`: The translation strings from the skill's `strings.ini` file
- Additional event arguments from the game event itself

You can also provide an `init(player, skill)` function for the skill.
All other functions and variables should be prefixed with an underscore (`_`)
to avoid them from being interpreted as event callbacks.
