import sqlite3


class Database:
    """Wrapper class around sqlite3 for storing RPG players' data."""

    def __init__(self, path=':memory:'):
        """Connect and create ``players`` and ``skills`` tables.

        :param str path:
            Path to the database file or ``':memory:'`` for RAM
        """
        self._connection = sqlite3.connect(path)
        self._connection.execute('''
            CREATE TABLE IF NOT EXISTS players (
                steamid TEXT PRIMARY KEY NOT NULL,
                level INTEGER NOT NULL,
                xp INTEGER NOT NULL,
                credits INTEGER NOT NULL
            )''')
        self._connection.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                steamid TEXT NOT NULL,
                class_id TEXT NOT NULL,
                level INTEGER NOT NULL,
                FOREIGN KEY (steamid) REFERENCES players(steamid),
                PRIMARY KEY (steamid, class_id)
            )''')

    def close(self):
        """Close the connection to the database."""
        self._connection.close()

