from decorators import help
from discord.ext import commands
from enums.help_categories import Category
from functions import checks, config
from functions.football import get_matches, get_table, get_jpl_code


class Football(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Don't allow any commands to work when locked
    def cog_check(self, ctx):
        return not self.client.locked

    @commands.group(name="Jpl", case_insensitive=True, invoke_without_command=True)
    @commands.check(checks.allowedChannels)
    @help.Category(Category.Sports)
    async def jpl(self, ctx, *args):
        pass

    @jpl.command(name="Matches", aliases=["M"], usage="[Week]*")
    async def matches(self, ctx, day: int = None):
        # Default is current day
        if day is None:
            day = int(config.get("jpl_day"))

        await ctx.send(get_matches(day))

    @jpl.command(name="Table", aliases=["Ranking", "Rankings", "Ranks", "T"])
    async def table(self, ctx):
        await ctx.send(get_table())

    @commands.check(checks.isMe)
    @jpl.command(name="Update")
    async def update(self, ctx):
        code = get_jpl_code()
        config.config("jpl", code)
        await ctx.message.add_reaction("✅")


def setup(client):
    client.add_cog(Football(client))
