import sqlite3


class Database:
    """Wrapper class around sqlite3 for storing RPG players' data."""

    def __init__(self, path=':memory:'):
        """Connect and create ``players`` and ``skills`` tables.

        :param str path:
            Path to the database file or ``':memory:'`` for RAM
        """
        self._connection = sqlite3.connect(path)
        self._connection.row_factory = sqlite3.Row
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

    def commit(self):
        """Commit changes to the database."""
        self._connection.commit()

    def save_player_data(self, steamid, level, xp, credits):
        """Save player's data into the database."""
        self._connection.execute(
            'INSERT OR REPLACE INTO players VALUES (?, ?, ?, ?)',
            (steamid, level, xp, credits))

    def save_skill_data(self, steamid, class_id, level):
        """Save skill's data into the database."""
        self._connection.execute(
            'INSERT OR REPLACE INTO skills VALUES (?, ?, ?)',
            (steamid, class_id, level))

    def __enter__(self):
        """Enter method to allow usage with ``with`` statement.

        :returns Database:
            The database object itself
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Commit changes and close the database safely."""
        self.commit()
        self.close()
