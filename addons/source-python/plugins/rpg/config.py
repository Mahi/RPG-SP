from paths import PLUGIN_DATA_PATH


REQUIRED_XP = {
    'base': 100,
    'per_level': 20,
}


XP_GAIN = {
    'on_kill': {
        'base': 80,
        'per_level_difference': 2,
    },
    'on_damage': {
        'per_damage': 0.5,
    },
}


DATABASE_URL = {
    'drivername': 'sqlite',
    'username': '',
    'password': '',
    'host': '',
    'port': None,
    'database': PLUGIN_DATA_PATH / 'rpg.db',
    'query': '',
}
