# Python imports
from collections import OrderedDict
from inspect import getmembers
from importlib import import_module
from typing import Dict

# Site-Package imports
import yaml

# Source.Python imports
from path import Path
from translations.strings import LangStrings

# RPG imports
import rpg.skills
from .skill import SkillType


def build_skill_types(root: Path) -> Dict[str, SkillType]:
    """Build skill type objects from a directory of skills.
    
    Attempt to order the skills by `order.txt` file's content.
    """
    skill_types = OrderedDict()
    for path in root.dirs():
        skill = build_skill(path)
        if skill is None:
            print(f"Unable to build skill for path '{path}'")
        else:
            skill_types[skill.key] = skill

    try:
        with open(root / 'order.txt') as order_file:
            order_data = order_file.readlines()
    except FileNotFoundError:
        return skill_types  # Alphabetical order from filesystem

    ordered = OrderedDict()
    for key in order_data:
        key = key.strip()
        if key in skill_types:
            ordered[key] = skill_types.pop(key)
        else:
            print(f"Unable to find skill for key '{key}'")
    return ordered


def build_skill(path: Path) -> SkillType:
    """Build a skill from a directory.
    
    The directory must have `data.yml`, `events.py`,
    and `strings.ini` files in it.
    See `skills/README.md` for more information.
    """
    key = str(path.name)  # Remove "pathiness"
    with open(path / 'data.yml') as data_file:
        data = yaml.safe_load(data_file)
    if 'key' in data:
        key = data.pop('key')
    strings = LangStrings(path / 'strings')

    init_callback = None
    event_callbacks = {}
    events_module = import_module(f'rpg.skills.{path.name}.events', rpg.skills)
    for name, attr in getmembers(events_module):
        if name == 'init':
            init_callback = attr
        elif not name.startswith('_'):
            event_callbacks[name] = attr

    return SkillType(
        key,
        lang_strings=strings,
        init_callback=init_callback,
        event_callbacks=event_callbacks,
        **data,
    )
