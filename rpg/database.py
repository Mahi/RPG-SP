import sqlite3


class Database:
    """Wrapper class around sqlite3 for storing RPG players' data."""

    def __init__(self, path=':memory:'):
        """Connect and create ``players`` and ``skills`` tables.

        :param str path:
            Path to the database file or ``':memory:'`` for RAM
        """
        self._connection = sqlite3.connect(path)

    def close(self):
        """Close the connection to the database."""
        self._connection.close()

