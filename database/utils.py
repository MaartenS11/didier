from database import all_models, engine, Base
from typing import Dict


def create_all_tables():
    """
    Create all tables in case they don't exist yet
    so the user doesn't have to do this manually
    when a new table is added
    """
    for model in all_models:
        model.__table__.create(engine, checkfirst=True)


def row_to_dict(row: Base) -> Dict:
    """
    Create a dictionary from a database entry
    vars() or dict() can NOT be used as these add extra SQLAlchemy-related properties!
    """
    d = {}

    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d
