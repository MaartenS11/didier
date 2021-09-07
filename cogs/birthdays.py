from data import constants
import datetime
from decorators import help
import discord
from discord.ext import commands
from enums.help_categories import Category
from functions import timeFormatters, stringFormatters
from functions.database import birthdays


class Birthdays(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Don't allow any commands to work when locked
    def cog_check(self, ctx):
        return not self.client.locked

    @commands.group(name="Birthday", aliases=["Bd", "Birthdays"], case_insensitive=True, invoke_without_command=True)
    @help.Category(Category.Other)
    async def birthday(self, ctx, member: discord.Member = None):
        """
        Command to check the birthday of yourself/another person.
        :param ctx: Discord Context
        :param member: The member to check
        """
        if member is not None:
            # A member was tagged
            name_str = "**{}**'s".format(member.display_name)
            res = birthdays.get_user(member.id)
        else:
            # No member passed -> check the user's birthday
            name_str = "Jouw"
            res = birthdays.get_user(ctx.author.id)

        if res is None:
            # Nothing found in the db for this member
            return await ctx.send("{} verjaardag zit nog niet in de database.".format(name_str))

        # Create a datetime object of the upcoming birthday,
        # and a formatted string displaying the date
        day_dt, time_string = self.dm_to_dt(res.day, res.month)

        # Find the weekday related to this day
        weekday = timeFormatters.intToWeekday(day_dt.weekday()).lower()

        return await ctx.send("{} verjaardag staat ingesteld op **{} {}**.".format(
            name_str, weekday, time_string
        ))

    @birthday.command(name="Today", aliases=["Now"])
    async def today(self, ctx):
        """
        Command that lists all birthdays of the day.
        :param ctx: Discord Context
        """
        # Create a datetime object for today
        dt = timeFormatters.dateTimeNow()
        await ctx.send(self.get_bds_on_date(dt))

    @birthday.command(name="Tomorrow", aliases=["Tm", "Tmw"])
    async def tomorrow(self, ctx):
        """
        Command that lists all birthdays of tomorrow.
        :param ctx: Discord Context
        """
        # Create a datetime object for tomorrow
        dt = timeFormatters.dateTimeNow() + datetime.timedelta(days=1)
        await ctx.send(self.get_bds_on_date(dt).replace("Vandaag", "Morgen").replace("vandaag", "morgen"))

    @birthday.command(name="Week")
    async def week(self, ctx):
        """
        Command that lists all birthdays for the coming week.
        :param ctx: Discord Context
        """
        # Dict of all birthdays this week
        this_week = {}

        # Create a datetime object starting yesterday so the first line
        # of the loop can add a day every time,
        # as premature returning would prevent this from happening
        # & get the day stuck
        dt = timeFormatters.dateTimeNow() - datetime.timedelta(days=1)

        # Create an embed
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name="Verjaardagen deze week")

        # Add all people of the coming week
        for day_counter in range(7):
            dt += datetime.timedelta(days=1)
            res = birthdays.get_users_on_date(dt.day, dt.month)

            # No birthdays on this day
            if not res:
                continue

            # Add everyone from this day into the dict
            this_week[str(day_counter)] = {"day": dt.day, "month": dt.month, "users": []}

            for user in res:
                this_week[str(day_counter)]["users"].append(user.userid)

        # No one found
        if not this_week:
            embed.description = "Deze week is er niemand jarig."
            return await ctx.send(embed=embed)

        COC = self.client.get_guild(int(constants.CallOfCode))

        # For every day, add the list of users into the embed
        for day, value in this_week.items():

            dayDatetime, timeString = self.dm_to_dt(int(value["day"]), int(value["month"]))
            weekday = timeFormatters.intToWeekday(dayDatetime.weekday())

            embed.add_field(name="{} {}".format(weekday, timeString),
                            value=", ".join(COC.get_member(user).mention for user in value["users"]),
                            inline=False)

        await ctx.send(embed=embed)

    def get_bds_on_date(self, dt):
        """
        Function to get all birthdays on a certain date.
        Returns a string right away to avoid more code duplication.
        :param dt: the date (Python datetime instance)
        :return: A formatted string containing all birthdays on [dt]
        """
        res = birthdays.get_users_on_date(dt.day, dt.month)

        # Nobody's birthday
        if not res:
            return "Vandaag is er niemand jarig."

        COC = self.client.get_guild(int(constants.CallOfCode))

        # Create a list of member objects of the people that have a birthday on this date
        people = [COC.get_member(user.userid) for user in res]

        if len(people) == 1:
            return "Vandaag is **{}** jarig.".format(people[0].display_name)
        return "Vandaag zijn {} en {} jarig.".format(
            ", ".join("**" + user.display_name + "**" for user in people[:-1]),
            people[-1].display_name
        )

    def dm_to_dt(self, day, month):
        """
        Converts a day + month to a datetime instance.
        :param day: the day in the date
        :param month: the month in the date
        :return: a datetime instance representing the next time this date occurs,
                 and a formatted string for this date
        """
        now = timeFormatters.dateTimeNow()
        year = now.year

        # Add an extra year to the date in case it has already passed
        if month < now.month or (month == now.month and day < now.day):
            year += 1

        # Create a datetime object for this birthday
        time_string = "{}/{}/{}".format(
            stringFormatters.leading_zero(str(day)),
            stringFormatters.leading_zero(str(month)),
            year
        )

        day_dt = datetime.datetime.strptime(time_string, "%d/%m/%Y")
        return day_dt, time_string

    @birthday.command(name="Set", usage="[DD/MM/YYYY]")
    async def set(self, ctx, date=None, member: discord.Member = None):
        """
        Command to add your birthday into the database.
        :param ctx: Discord Context
        :param date: the date of your birthday
        :param member: another member whose birthday has to be added/changed
        """
        # No date passed
        if date is None:
            return await ctx.send("Geef een datum op.")

        # Invalid format used
        if date.count("/") != 2:
            return await ctx.send("Ongeldig formaat (gebruik DD/MM/YYYY).")

        # Check if anything is wrong with the date
        try:
            day = int(date.split("/")[0])
            month = int(date.split("/")[1])
            year = int(date.split("/")[2])

            # This is not used, but creating an invalid datetime object throws a ValueError
            # so it prevents invalid dates like 69/420/360
            dt = datetime.datetime(year=year, month=month, day=day)

            # Assume no one in the Discord is more than 5 years younger, or 10 years older
            # (which are also virtually impossible, but just to be sure)
            if year >= timeFormatters.dateTimeNow().year - 15 or year < 1990:
                raise ValueError

        except ValueError:
            return await ctx.send("Dit is geen geldige datum.")

        # A member was tagged, check if I did it
        if member is not None:
            if str(ctx.author.id) != str(constants.myId):
                return await ctx.send("Je kan andere mensen hun verjaardag niet instellen, {}.".format(ctx.author.display_name))
            else:
                birthdays.add_user(member.id, day, month, year)
                return await ctx.message.add_reaction("✅")

        # Birthday is already added
        if birthdays.get_user(ctx.author.id) and str(ctx.author.id) != constants.myId:
            return await ctx.send("Je verjaardag zit al in de database.")

        # Add into the db
        birthdays.add_user(ctx.author.id, day, month, year)
        return await ctx.message.add_reaction("✅")


def setup(client):
    client.add_cog(Birthdays(client))
