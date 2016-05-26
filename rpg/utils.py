class ClassProperty:
    """Read-only property for classes instead of instances.

    Acts as a combination of :func:`property` and :func:`classmethod`
    to create properties for classes.

    Although it is possible to create a plain class property and
    set the :attr:`fget` manually later on, it's usually easier to
    use :class:`ClassProperty` as a decorator:

    .. code-block:: python

        class My_Class:

            @ClassProperty
            def name(cls):
                return cls.__name__.replace('_', ' ')

        obj = My_Class()

        print('Accessed through the class:', My_Class.name)
        print('Accessed through the object:', obj.name)

        class My_Subclass(My_Class):
            pass

        print('Accessed through the subclass:', My_Subclass.name)

    Output:

    .. code-block:: none

        Accessed through the class: My Class
        Accessed through the object: My Class
        Accessed through the subclass: My Subclass
    """

    def __init__(self, fget=None):
        """Initialize the class property with a function.

        :param callable|None fget:
            Function to call when the property is accessed
        """
        self.fget = fget


    def __get__(self, obj, type_):
        """Call the :attr:`fget` when the class property is accessed.

        :param object obj:
            Object used to access the class property (can be None)
        :param type type_:
            Class used to access the class property
        """
        if type_ is None and obj is not None:
            type_ = type(obj)
        return self.fget(type_) 


def get_subclasses(cls):
    """Get a flat generator of a class's subclasses.

    Yields each subclass recursively (meaning that children get priority
    over siblings in the order of the yielding).

    :param type cls:
        Class whose subclasses to get
    """
    for subcls in cls.__subclasses__():
        yield subcls
        yield from get_subclasses(subcls)
