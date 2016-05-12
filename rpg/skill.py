import collections
import utils


def callback(event_name):
    def decorator(callback):
        callback._event = event_name
        return callback
    return decorator


class _SkillMeta(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._event_callbacks = collections.defaultdict(list)
        for method in attrs.values():
            if hasattr(method, '_event'):
                cls._event_callbacks[method._event].append(method)


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

    def __init__(self, level=0):
        self.level = level

    def upgrade_cost(self):
        return (self.level + 1) * 5

    def downgrade_refund(self):
        return self.level * 4
