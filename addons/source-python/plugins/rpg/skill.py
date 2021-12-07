# Python imports
from math import inf
from typing import Any, Callable, Dict, Optional

# Source.Python imports
from translations.strings import LangStrings, TranslationStrings


EventArgs = Dict[str, Any]
EventCallback = Callable[[EventArgs], None]


class SkillType:
    """Type object for skills.

    Contains the common attributes for skills of the same type:

    - unique `key` to identify the skill with
    - `strings` of type `LangStrings` for the skill's translations
    - `max_level` to limit the skill from being leveled further
    - `init_callback` to initialize a skill for a player
    - and `event_callbacks` dict to trigger the skill's functionality.

    Also implements `name` and `description` properties to fetch
    the name and descriptiong language strings automatically.
    """

    def __init__(self,
        key: str,
        *,
        lang_strings: Optional[LangStrings]=None,
        max_level: int=inf,
        variables: Optional[Dict[str, Any]]=None,
        init_callback: Optional[EventCallback]=None,
        event_callbacks: Optional[Dict[str, EventCallback]]=None,
    ) -> None:
        self.key = key
        self.lang_strings = lang_strings
        self.max_level = max_level
        self.variables = variables if variables is not None else {}
        self.init_callback = init_callback
        self.event_callbacks = event_callbacks if event_callbacks is not None else {}

    @property
    def name(self) -> TranslationStrings:
        """TranslationStrings of the skill's name."""
        return self.lang_strings['name']

    @property
    def description(self) -> TranslationStrings:
        """TranslationStrings of the skill's description."""
        return self.lang_strings['description']


def type_object_property(property_name: str) -> property:
    """Property for getting attribute's value from a `type_object`."""
    def fget(self):
        return getattr(self.type_object, property_name)
    return property(fget)


class Skill:
    """Skills are used by players to gain special powers.

    Each skill only contains a `type_object` and a `level`,
    everything else is induced from the type object.
    """

    def __init__(self, type_object: SkillType, level: int=0) -> None:
        self.type_object = type_object
        self.level = level

    key: str = type_object_property('key')
    name: TranslationStrings = type_object_property('name')
    description: TranslationStrings = type_object_property('description')
    max_level: int = type_object_property('max_level')
    _init_callback: Optional[EventCallback] = type_object_property('init_callback')
    _event_callbacks: Dict[str, EventCallback] = type_object_property('event_callbacks')

    @property
    def upgrade_cost(self) -> int:
        """Cost of upgrading the skill."""
        return (self.level + 1) * 5

    @property
    def downgrade_refund(self) -> int:
        """Refund for downgrading the skill."""
        return self.level * 4

    def trigger(self, event_name, **event_args) -> None:
        """Trigger a callback for an event.
        
        Does nothing if a callback for the specified event doesn't exist.
        """
        if event_name not in self._event_callbacks:
            return
        callback = self._event_callbacks.get(event_name)
        if callback is not None:
            event_args['skill'] = self
            callback(
                strings=self.type_object.lang_strings,
                variables=self.type_object.variables,
                **event_args
            )
