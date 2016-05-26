import collections

import utils


def callback(*event_names):
    def decorator(callback):
        callback._events = event_names
        return callback
    return decorator


class _SkillMeta(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._event_callbacks = collections.defaultdict(list)
        for f in attrs.values():
            if not hasattr(f, '_event'):
                continue
            for event_name in f._events:
                cls._event_callbacks[event_name] = f


class Skill(metaclass=_SkillMeta):

    @utils.ClassProperty
    def class_id(cls):
        return cls.__qualname__

    @utils.ClassProperty
    def name(cls):
        return cls.__name__.replace('_', ' ')

    @utils.ClassProperty
    def description(cls):
        return cls.__doc__

    max_level = None

    def __init__(self, level=0):
        self.level = level

    @property
    def upgrade_cost(self):
        return (self.level + 1) * 5

    @property
    def downgrade_refund(self):
        return self.level * 4

    def execute_callback(self, event_name, **event_args):
        if event_name in self._event_callbacks:
            self._event_callbacks[event_name](self, **event_args)
