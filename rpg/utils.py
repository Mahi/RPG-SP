class ClassProperty:

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, type_):
        return self.fget(type_)
