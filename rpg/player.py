import easyplayer


class Player(easyplayer.EasyPlayer):

    def __init__(self, index):
        super().__init__(index)
        self._level = 0
        self._xp = 0

    @staticmethod
    def xp_to_level_up(level):
        return 300 + 15 * level

    @property
    def required_xp(self):
        return Player.xp_to_level_up(self.level)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value < self.level:
            raise ValueError("No support for removing levels.")
        self._level = value

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, value):
        if value < self.xp:
            raise ValueError("No support for removing XP.")
        self._xp = value
        self._sync_level_to_xp()

    def _sync_level_to_xp(self):
        levels = 0
        while True:
            required_xp = Player.xp_to_level_up(self.level + levels)
            if required_xp > self.xp:
                break
            self._xp -= required_xp
            levels += 1
        self.level += levels
