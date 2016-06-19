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

    def __init__(self, fget=None, doc=None):
        """Initialize the class property with a function.

        :param callable|None fget:
            Function to call when the property is accessed
        """
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.fget = fget
        self.__doc__ = doc

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


class DecoratorAppendList(list):
    """List which allows ``append`` to be used as a decorator."""

    def append(self, item):
        """Append an item to the list.

        Returns the item so can be used as a decorator.

        :param object item:
            Item to append to the list
        :returns object:
            The appended item
        """
        super().append(item)
        return item
