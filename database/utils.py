from database import all_models, engine


def create_all_tables():
    """
    Create all tables in case they don't exist yet
    so the user doesn't have to do this manually
    when a new table is added
    """
    for model in all_models:
        model.__table__.create(engine, checkfirst=True)
