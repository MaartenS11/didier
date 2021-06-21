from typing import List

from dotenv import load_dotenv
import os


load_dotenv()


def _to_bool(value: str) -> bool:
    """
    Env variables are strings so this converts them to booleans
    """
    return value.lower() in ["true", "1", "y", "yes"]


# Sandbox or live
SANDBOX: bool = _to_bool(os.getenv("SANDBOX", "true"))

# Tokens & API keys
URBANDICTIONARY: str = os.getenv("URBANDICTIONARY", "")
IMGFLIP_NAME: str = os.getenv("IMGFLIPNAME", "")
IMGFLIP_PASSWORD: str = os.getenv("IMGFLIPPASSWORD", "")
UFORA_TOKEN: str = os.getenv("UFORA_TOKEN", "")

# Database credentials
DB_USERNAME: str = os.getenv("DBUSERNAME", "postgres")
DB_PASSWORD: str = os.getenv("DBPASSWORD", "")
DB_HOST: str = os.getenv("DBHOST", "localhost")
DB_NAME: str = os.getenv("DBNAME", "")
DB_DIALECT: str = os.getenv("DBDIALECT", "postgresql")
DB_DRIVER: str = os.getenv("DBDRIVER", "")

# Discord-related
TOKEN: str = os.getenv("TOKEN", "")
HOST_IPC: bool = _to_bool(os.getenv("HOSTIPC", "false"))
READY_MESSAGE: str = os.getenv("READYMESSAGE", "I'M READY I'M READY I'M READY I'M READY")  # Yes, this is a Spongebob reference
STATUS_MESSAGE: str = os.getenv("STATUSMESSAGE", "with your Didier Dinks.")

# Guilds to test slash commands in
# Ex: 123,456,789
_guilds = os.getenv("SLASHTESTGUILDS", "").replace(" ", "")
SLASH_TEST_GUILDS: List[int] = list(map(lambda x: int(x), _guilds.split(","))) if _guilds else None
