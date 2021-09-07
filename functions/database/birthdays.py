from database.db import session
from database.models import Birthday
from typing import Optional, List


def get_user(userid: int) -> Optional[Birthday]:
    return session.query(Birthday).filter(Birthday.userid == userid).scalar()


def get_users_on_date(day: int, month: int) -> List[Birthday]:
    return session.query(Birthday.userid).filter(Birthday.day == day and Birthday.month == month).all()


def add_user(userid: int, day: int, month: int, year: int):
    bd: Optional[Birthday] = get_user(userid)

    # Update user if they exist, otherwise insert entry
    if bd is not None:
        bd.day = day
        bd.month = month
        bd.year = year
    else:
        entry = Birthday(userid=userid, day=day, month=month, year=year)
        session.add(entry)

    session.commit()
