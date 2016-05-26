import easyplayer


class Player(easyplayer.Player):

    def __init__(self, index, level=0, xp=0, credits=0, skills=None):
        super().__init__(index)
        self._level = level
        self._xp = xp
        self._credits = credits
        self.skills = skills if skills is not None else []

    @property
    def level(self):
        return self._level

    @property
    def credits(self):
        return self._credits

    @property
    def required_xp(self):
        return 300 + 15 * self.level

    @property
    def xp(self):
        return self._xp

    def give_xp(self, amount):
        if amount < 0:
            raise ValueError('Negative value passed for give_xp()')
        self._xp += amount
        while self.xp > self.required_xp:
            self._xp -= self.required_xp
            self._level += 1
            self._credits += 5

    def reset_rpg_progress(self):
        self._level = 0
        self._xp = 0
        self._credits = 0
        for skill in self.skills:
            skill.level = 0
