from enum import IntEnum
from typing import Dict, List

from database.db import session
from database.utils import row_to_dict
from database.models import CommandStats
from functions.stringFormatters import leading_zero as lz
import time


class InvocationType(IntEnum):
    TextCommand = 0
    SlashCommand = 1
    ContextMenu = 2


def invoked(inv: InvocationType):
    t = time.localtime()
    day_string: str = f"{t.tm_year}-{lz(t.tm_mon)}-{lz(t.tm_mday)}"
    _update(day_string, inv)


def _is_present(date: str) -> bool:
    """
    Check if a given date is present in the database
    """
    res = session.query(CommandStats).filter(CommandStats.day == date).scalar()
    return res is not None


def _add_date(date: str):
    """
    Add a date into the db
    """
    entry = CommandStats(day=date, commands=0, slash_commands=0, context_menus=0)
    session.add(entry)


def _update(date: str, inv: InvocationType):
    """
    Increase the counter for a given day
    """
    # Date wasn't present yet, add it
    if not _is_present(date):
        _add_date(date)

    column_name: str = ["commands", "slash_commands", "context_menus"][inv.value]
    session.query(CommandStats).filter(CommandStats.day == date)\
        .update({column_name: (getattr(CommandStats, column_name) + 1)})

    # Commit changes, including adding the date if necessary
    session.commit()


def query_command_stats() -> List[Dict]:
    """
    Return all rows as dicts
    """
    stats = []

    instance: CommandStats
    for instance in session.query(CommandStats).order_by(CommandStats.day):
        stats.append(row_to_dict(instance))

    return stats
