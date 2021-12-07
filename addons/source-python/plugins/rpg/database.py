# Site-Package imports
from sqlalchemy import create_engine, Column, ForeignKey, Integer, MetaData, Table, Text
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import bindparam

# RPG:GO imports
from . import config
from .player import Player


# Initialize table metadata
metadata = MetaData()
player_table = Table('player', metadata,
    Column('steamid', Text, primary_key=True),
    Column('level', Integer, nullable=False, default=0),
    Column('xp', Integer, nullable=False, default=0),
    Column('credits', Integer, nullable=False, default=0),
)

skill_table = Table('skill', metadata,
    Column('id', Integer, primary_key=True),
    Column('key', Text, nullable=False),
    Column('level', Integer, nullable=False, default=0),
    Column('steamid', Text, ForeignKey('player.steamid'), nullable=False),
)

# Create engine and missing tables
engine = create_engine(URL(**config.DATABASE_URL))
metadata.create_all(bind=engine)


def create_player(player: Player) -> None:
    """Insert a new player and their skills into the database.
    
    Also sets the skill objects's `_db_id` to match their database ID.
    """
    with engine.connect() as conn:

        conn.execute(
            player_table.insert().values(
                steamid=player.steamid,
                level=player.level,
                xp=player.xp,
                credits=player.credits,
            )
        )

        skills = list(player.skills)
        result = conn.execute(
            skill_table.insert().values([
                {
                    'key': skill.key,
                    'level': skill.level,
                    'steamid': player.steamid,
                }
                for skill in skills
            ])
        )

        for id, skill in zip(result.inserted_primary_key, skills):
            skill._db_id = id


def save_player(player: Player) -> None:
    """Update a player's and their skills's data into the database."""
    with engine.connect() as conn:

        conn.execute(
            player_table.update().where(player_table.c.steamid==player.steamid).values(
                level=player.level,
                xp=player.xp,
                credits=player.credits
            )
        )

        conn.execute(
            skill_table.update().where(skill_table.c.id==bindparam('db_id')).values(
                {
                    'level': skill.level,
                    'db_id': skill._db_id
                }
                for skill in list(player.skills)
            )
        )


def load_player(player: Player) -> bool:
    """Fetch a player's and their skills's data from the database.
    
    Returns `False` if there was no match for the player's steamid.
    """
    with engine.connect() as conn:

        result = conn.execute(
            select([player_table]).where(player_table.c.steamid==player.steamid)
        )
        player_data = result.first()
        if player_data is None:
            return False
        player._level = player_data.level
        player._xp = player_data.xp
        player.credits = player_data.credits

        result = conn.execute(
            select([skill_table]).where(skill_table.c.steamid==player.steamid)
        )
        for skill_data in result:
            skill = player.get_skill(skill_data.key)
            if skill is not None:
                 skill.level = skill_data.level
                 skill._db_id = skill_data.id

    return True
