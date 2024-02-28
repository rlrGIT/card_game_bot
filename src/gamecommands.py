import disnake

from disnake.ext import commands
from gamestate import GameState
from player import Player

class GameCommands(commands.Cog):
    CMD_NEW_GAME = 'new'
    CMD_ADD_PLAYER = 'add'
    CMD_REM_PLAYER = 'remove'

    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        self.in_game = False
        self.state = GameState()
    
    @commands.slash_command(
        name=CMD_NEW_GAME,
        description='Start a new game with all present members'
    )
    async def new_game(self, inter : disnake.ApplicationCommandInteraction) -> None:
        if self.in_game:
            await self.bot.respond_with(inter, 'Game instance already running')
            return
        
        await self.bot.respond_with(inter, 'Starting...')
        self.in_game = True

        # assert that this isn't in a DM
        if inter.channel:
            for user in inter.channel.members:
                _ = await self.add_player(inter, user)

            _ = await self.add_player(inter, inter.author)
            await self.bot.respond_with(inter, 'Started game with: {} players'.format(str(len(self.state.players))))
        else:
            print('New game attempted in DM or unusable thread, ignoring.')


    @commands.slash_command(
        name=CMD_ADD_PLAYER,
        description='Add a new player to an existing game'
    )
    async def add_player(self, inter : disnake.ApplicationCommandInteraction, user : disnake.User) -> None:
        name : str = user.display_name
        await self.bot.respond_with(inter, 'Adding player: {}'.format(name))

        if self.state.add_player(name):
            await self.bot.dm_user(user, 'Joined game as: {}'.format(name))
        else:
            #TODO handle collisions somehow...
            await self.bot.respond_with(inter, '{} already exists'.format(name))


    # TODO create an event for on member leaving the channel instead of this?
    @commands.slash_command(
        name=CMD_REM_PLAYER,
        description='Remove a new player from the game'
    )
    async def remove_player(self, inter : disnake.ApplicationCommandInteraction, user : disnake.User) -> None:
        name : str = user.display_name
        await self.bot.respond_with(inter, 'Removing player: {}'.format(name))

        if self.state.remove_player(name):
            await self.bot.dm_user(user, 'You were removed from the game.')
        else:
            await self.bot.respond_with(inter, 'Player not found... retry')


def setup(bot : commands.Bot) -> None:
    bot.add_cog(GameCommands(bot))
