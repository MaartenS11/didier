import datetime
from typing import List, Dict

from database.db import session
from database.models import BankAccount, Inventory
from functions.database import utils, stats
import time


def dinks(userid) -> float:
    return float(get_or_add_user(userid).dinks)


def dinks_all(userid) -> Dict:
    platinum_dinks = 0

    inventory = session.query(Inventory).filter(Inventory.userid == userid and Inventory.itemid == 1).scalar()

    # Don't add to db if not present, doesn't matter
    if inventory is not None:
        platinum_dinks = inventory.amount

    return {"dinks": dinks(userid), "platinum": platinum_dinks}


def get_all_rows() -> List[BankAccount]:
    return session.query(BankAccount).all()


def get_all_plat_dinks() -> Dict[str, int]:
    users: List[Inventory] = session.query(Inventory).filter(Inventory.itemid == 1).all()

    dic = {}
    for user in users:
        dic[str(user.userid)] = user.amount

    return dic


def get_or_add_user(userid: int) -> BankAccount:
    user = session.query(BankAccount).filter(BankAccount.userid == userid).scalar()

    # User doesn't exist yet, add them
    if user is None:
        session.add(BankAccount(userid=userid))
        session.commit()

    return user


# TODO check for nightly bonus & add+return that instead of 420
def nightly(userid):
    user = get_or_add_user(userid)

    today = datetime.datetime.today().date()
    last_nightly = datetime.datetime.fromtimestamp(user.nightly).date()
    streak = user.nightly_streak

    if last_nightly < today:
        user.dinks = float(user.dinks) + 420.0
        user.nightly = int(time.time())

        # Update the streak
        if (today - last_nightly).days > 1:
            user.nightly_streak = 1
            streak = 1
        else:
            user.nightly_streak += 1
            streak += 1

        s = stats.getOrAddUser(userid)

        # TODO when stats is done
        if streak > int(s[5]):
            stats.update(userid, "longest_streak", streak)

        stats.update(userid, "nightlies_count", int(s[6]) + 1)

        session.commit()

        return [True, 420, streak]
    return [False, 0, -1]


# TODO fix usages first
def update(userid, column, value):
    _ = get_or_add_user(userid)
    connection = utils.connect()
    cursor = connection.cursor()
    query = "UPDATE currencytable " \
            "SET {} = %s " \
            "WHERE userid = %s".format(column)
    cursor.execute(query, (value, userid,))
    connection.commit()
