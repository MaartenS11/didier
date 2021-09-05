from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USERNAME, DB_DIALECT, DB_DRIVER
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from urllib.parse import quote_plus

# Encode password
_encoded_pw = quote_plus(DB_PASSWORD)

engine = create_engine(
    # Format: dialect+driver://username:password@host:port/database
    f"{DB_DIALECT}{'+' if DB_DRIVER else ''}{DB_DRIVER}://{DB_USERNAME}:{_encoded_pw}@{DB_HOST}/{DB_NAME}"
)
session: Session = sessionmaker(bind=engine)()

Base = declarative_base()
