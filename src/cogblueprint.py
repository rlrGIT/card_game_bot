import disnake

from disnake.ext import commands



class CogBlueprint(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    """
    @commands.slash_command(
        name='',
        description=''
    )
    async def _(inter) -> None:
        pass
    """

def setup(bot : commands.Bot) -> None:
    bot.add_cog(BotUtil(bot))
