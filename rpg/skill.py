import collections
import utils


class _SkillMeta(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._event_callbacks = collections.defaultdict(list)


class Skill(metaclass=_SkillMeta):

    @utils.ClassProperty
    def class_id(cls):
        return cls.__qualname__

    @utils.ClassProperty
    def name(cls):
        return cls.__name__.replace(' ', '')

    @utils.ClassProperty
    def description(cls):
        return cls.__doc__

    max_level = None
    
    @classmethod
    def add_event_callback(cls, event_name, callback):
        callbacks = cls._event_callbacks[event_name]
        if callback not in callbacks:
            callbacks.append(callback)

    @classmethod
    def event(cls, *event_names):
        def decorator(callback):
            for event_name in event_names:
                cls.add_event_callback(event_name, callback)
            return callback
        return decorator

    def __init__(self, level=0):
        self.level = level

    def upgrade_cost(self):
        return (self.level + 1) * 5

    def downgrade_refund(self):
        return self.level * 4
