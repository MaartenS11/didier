from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, BigInteger, Numeric, Date, Boolean
from typing import Set


Base = declarative_base()


# TODO fill in non-nulls everywhere
# TODO comments

class BankAccount(Base):
    __tablename__ = "currencytable"

    userid = Column(BigInteger, primary_key=True)
    dinks = Column(Numeric, default=0.0)
    banklevel = Column(Integer, default=1)
    investedamount = Column(Numeric, default=0.0)
    investeddays = Column(Integer, default=0)
    profit = Column(Numeric, default=0.0)
    defense = Column(Integer, default=1)
    offense = Column(Integer, default=1)
    bitcoins = Column(Numeric, default=0.0)
    nightly = Column(Integer, default=0)
    nightly_streak = Column(Integer, default=0)


class Birthday(Base):
    __tablename__ = "birthdays"

    userid = Column(BigInteger, primary_key=True)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class ChannelActivity(Base):
    __tablename__ = "channel_activity"

    channel_id = Column(BigInteger, primary_key=True)
    message_count = Column(Numeric)


class CommandAlias(Base):
    __tablename__ = "custom_command_aliases"

    id = Column(Integer, autoincrement=True, primary_key=True)
    command = Column(Integer)
    alias = Column(String, unique=True)


class CommandStats(Base):
    __tablename__ = "command_stats"

    day = Column(Date, primary_key=True)
    commands = Column(Integer, default=0)
    slash_commands = Column(Integer, default=0)
    context_menus = Column(Integer, default=0)


class CustomCommand(Base):
    __tablename__ = "custom_commands"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    response = Column(String)


class DadJoke(Base):
    __tablename__ = "dad_jokes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    joke = Column(String)


class FAQCategory(Base):
    __tablename__ = "faq_categories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)


class FAQEntry(Base):
    __tablename__ = "faq_entries"

    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    answer_markdown = Column(String)


class GitHub(Base):
    __tablename__ = "githubs"

    userid = Column(BigInteger, primary_key=True)
    githublink = Column(String)


class Inventory(Base):
    __tablename__ = "inventory"

    userid = Column(BigInteger, primary_key=True)
    itemid = Column(Integer, primary_key=True)
    amount = Column(Integer, default=0)


class Meme(Base):
    __tablename__ = "memes"

    # TODO id primary key
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    fields = Column(Integer)


class Muttn(Base):
    __tablename__ = "muttn"

    userid = Column(BigInteger, primary_key=True)
    stats = Column(Numeric)
    count = Column(Integer)
    message = Column(BigInteger)
    highest = Column(Integer, default=0)


class PokeInfo(Base):
    __tablename__ = "poke"

    current = Column(BigInteger, primary_key=True)
    poketime = Column(BigInteger)
    previous = Column(BigInteger)


class Prison(Base):
    __tablename__ = "prison"

    userid = Column(BigInteger, primary_key=True)
    bail = Column(Numeric)
    days = Column(Integer)
    daily = Column(Numeric)


class Reminders(Base):
    __tablename__ = "remind"

    userid = Column(BigInteger, primary_key=True)
    nightly = Column(Boolean, default=False)
    les = Column(Boolean, default=False)


class StoreItem(Base):
    __tablename__ = "store"

    itemid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    price = Column(BigInteger)
    limit = Column(Integer)


class TrumpQuote(Base):
    __tablename__ = "trump"

    id = Column(Integer, autoincrement=True, primary_key=True)
    quote = Column(String)
    date = Column(String)
    location = Column(String)


class TwitchChannel(Base):
    __tablename__ = "twitch"

    userid = Column(BigInteger, primary_key=True)
    link = Column(String)


class UserInfo(Base):
    __tablename__ = "info"

    userid = Column(BigInteger, primary_key=True)
    poke_blacklist = Column(Boolean, default=False)


class UserStats(Base):
    __tablename__ = "personalstats"

    userid = Column(BigInteger, primary_key=True)
    poked = Column(Integer, default=0)
    robs_success = Column(Integer, default=0)
    robs_failed = Column(Integer, default=0)
    robs_total = Column(Numeric, default=0)
    longest_streak = Column(Integer, default=0)
    nightlies_count = Column(Integer, default=0)
    profit = Column(Numeric, default=0.0)
    cf_wins = Column(Integer, default=0)
    cf_profit = Column(Numeric, default=0.0)
    bails = Column(Integer, default=0)
    messages = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    last_message = Column(BigInteger, default=0)


class TestTable(Base):
    __tablename__ = "test_table"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    other_column = Column(Integer)


# A list of all models in this file, this is used to
# create all tables later on
all_models: Set[Base] = {
    BankAccount, Birthday, ChannelActivity, CommandAlias, CommandStats,
    CustomCommand, DadJoke, FAQCategory, FAQEntry, GitHub, Inventory,
    Meme, Muttn, PokeInfo, Prison, Reminders, StoreItem, TrumpQuote,
    TwitchChannel, UserInfo, UserStats, TestTable
}
