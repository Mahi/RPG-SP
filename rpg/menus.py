from menus import PagedMenu
from menus import SimpleMenu


class _SimpleRpgMenu(SimpleMenu):
    """Base class for simple RPG menus.

    Adds a :attr:`player` attribute which can be set in the ``__init__``
    for later use in the menu's callbacks.
    Also adds the :attr:`parent_menu` attribute known from
    Source.Python's :class:`menus.radio.PagedRadioMenu`.
    """

    def __init__(self, player, *args, parent_menu=None, **kwargs):
        """Initialize the menu with its custom attributes.

        :param players.entity.Player player:
            Entity of the player using the menu
        :param tuple *args:
            Args to forward to :class:`menus.radio.SimpleRadioMenu`
        :param menus.base._BaseMenu parent_menu:
            Parent menu to store into the :attr:`parent_menu` attribute
        :param dict **kwargs:
            Kwargs to forward to :class:`menus.radio.SimpleRadioMenu`
        """
        super().__init__(
            *args, **kwargs,
            build_callback=self._build_callback,
            select_callback=self._select_callback,
        )
        self.player = player
        self.parent_menu = parent_menu


class _PagedRpgMenu(PagedMenu):
    """Base class for simple RPG menus.

    Adds a :attr:`player` attribute which can be set in the ``__init__``
    for later use in the menu's callbacks.
    """

    def __init__(self, player, *args, **kwargs):
        """Initialize the menu with its custom attributes.

        :param players.entity.Player player:
            Entity of the player using the menu
        :param tuple *args:
            Args to forward to :class:`menus.radio.SimpleRadioMenu`
        :param dict **kwargs:
            Kwargs to forward to :class:`menus.radio.SimpleRadioMenu`
        """
        super().__init__(
            *args, **kwargs,
            build_callback=self._build_callback,
            select_callback=self._select_callback,
            top_separator=None,
            bottom_separator=None,
        )
        self.player = player
