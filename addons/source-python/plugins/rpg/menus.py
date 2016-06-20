from menus import PagedMenu
from menus import PagedOption
from menus import SimpleMenu
from menus import SimpleOption
from menus import Text


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


class MainMenu(_SimpleRpgMenu):
    """Main RPG menu for navigating the submenus."""

    @staticmethod
    def _build_callback(self, player_index):
        self.clear()
        self.extend([
            Text('RPG Main Menu'),
            Text('Credits: {0}'.format(self.player.credits)),
            SimpleOption(1, 'Upgrade Skills', UpgradeSkillsMenu),
            SimpleOption(2, 'Downgrade Skills', DowngradeSkillsMenu),
            SimpleOption(3, 'Stats', StatsMenu),
            SimpleOption(9, 'Close'),
        ])

    @staticmethod
    def _select_callback(self, player_index, choice):
        return choice.value(self.player, parent_menu=self)


class UpgradeSkillsMenu(_PagedRpgMenu):
    """Menu for upgrading skills."""

    def __init__(self, player, *args, **kwargs):
        super().__init__(player, *args, **kwargs, title='Upgrade Skills')

    @staticmethod
    def _build_callback(self, player_index):
        self.clear()
        self.description = 'Credits: {0}'.format(self.player.credits)
        for skill in self.player.skills:
            text = '{s.name} [{s.level}/{s.max_level}] ({s.upgrade_cost} credits)'.format(s=skill)
            self.append(PagedOption(text, skill, True, True))

    @staticmethod
    def _select_callback(self, player_index, choice):
        self.player.upgrade_skill(choice.value)
        return self


class DowngradeSkillsMenu(_PagedRpgMenu):
    """Menu for downgrading skills."""

    def __init__(self, player, *args, **kwargs):
        super().__init__(player, *args, **kwargs, title='Downgrade Skills')

    @staticmethod
    def _build_callback(self, player_index):
        self.clear()
        self.description = 'Credits: {0}'.format(self.player.credits)
        for skill in self.player.skills:
            text = '{s.name} [{s.level}/{s.max_level}] ({s.downgrade_refund} credits)'.format(s=skill)
            self.append(PagedOption(text, skill, True, True))

    @staticmethod
    def _select_callback(self, player_index, choice):
        self.player.downgrade_skill(choice.value)
        return self


class StatsMenu(_SimpleRpgMenu):
    """Menu for showing player's RPG stats."""

    @staticmethod
    def _build_callback(self, player_index):
        self.clear()
        self.extend([
            Text('Stats'),
            Text('Credits: {0}'.format(self.player.credits)),
            Text('Level: {0}'.format(self.player.level)),
            Text('XP: {0}/{1}'.format(self.player.xp, self.player.required_xp)),
            SimpleOption(7, 'Back', self.parent_menu),
            SimpleOption(9, 'Close'),
        ])

    @staticmethod
    def _select_callback(self, player_index, choice):
        return choice.value
