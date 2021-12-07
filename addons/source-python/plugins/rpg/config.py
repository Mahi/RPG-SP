# Source.Python imports
from paths import PLUGIN_DATA_PATH


# How much XP is required to level up
REQUIRED_XP = {
    'base': 100,
    'per_level': 20,
}


# How much XP to gain from kills/damage
XP_GAIN = {
    'on_kill': {
        'base': 80,
        'per_level_difference': 2,
    },
    'on_damage': {
        'per_damage': 0.5,
    },
}


# Database URL in SQLAlchemy's format
DATABASE_URL = {
    'drivername': 'sqlite',
    'username': '',
    'password': '',
    'host': '',
    'port': None,
    'database': PLUGIN_DATA_PATH / 'rpg.db',
    'query': '',
}
