class ClassProperty:

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, type_):
        return self.fget(type_)


def get_subclasses(cls):
    for subcls in cls.__subclasses__():
        yield subcls
        yield from get_subclasses(subcls)
