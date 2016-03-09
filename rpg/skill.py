import utils


class Skill:

    def __init__(self, level=0):
        self.level = level

    @utils.ClassProperty
    def name(cls):
        return cls.__name__.replace(' ', '')

    @utils.ClassProperty
    def description(cls):
        return cls.__doc__

    max_level = None
    upgrade_cost = 5
    downgrade_refund = 4

    @utils.ClassProperty
    def class_id(cls):
        return cls.__qualname__
