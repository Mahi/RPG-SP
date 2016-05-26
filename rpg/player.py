import easyplayer


class Player(easyplayer.Player):
    """RPG player class with leveling system and skills.

    Implements the leveling system with :attr:`xp` and :attr:`level`
    attributes. Leveling up grants ``5`` :attr:`credits`, which can be
    spent to upgrade skills to give the player bonus powers.

    Subclasses :class:`easyplayer.Player`, so all of its custom features
    are also supported by :class:`Player` objects.
    """

    def __init__(self, index, level=0, xp=0, credits=0, skills=None):
        """Initialize the RPG player.

        :param int index:
            Index of the player entity
        """
        super().__init__(index)
        self._level = level
        self._xp = xp
        self._credits = credits
        self.skills = skills if skills is not None else []

    @property
    def level(self):
        """Player's current RPG level."""
        return self._level

    @property
    def credits(self):
        """Player's credits used to buy skill upgrades."""
        return self._credits

    @property
    def required_xp(self):
        """Required experience points to level up."""
        return 300 + 15 * self.level

    @property
    def xp(self):
        """Player's current experience points."""
        return self._xp

    def give_xp(self, amount):
        """Give experience points to the player.

        Grants levels and credits if the new XP value surpasses player's
        :attr:`required_xp`.

        :param int amount:
            Positive amount of XP to give
        :raises ValueError:
            If the provided amount is negative
        """
        if amount < 0:
            raise ValueError('Negative value passed for give_xp()')
        self._xp += amount
        while self.xp > self.required_xp:
            self._xp -= self.required_xp
            self._level += 1
            self._credits += 5

    def reset_rpg_progress(self):
        """Completely reset player's RPG progress.

        Resets level, XP, credits, and all the levels of each skill.
        """
        self._level = 0
        self._xp = 0
        self._credits = 0
        for skill in self.skills:
            skill.level = 0
