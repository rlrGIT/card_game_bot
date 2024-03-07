import disnake

from disnake.ext import commands
from gamestate import GameState
from player import Player

"""
    TODO: might be worth making some of these
    TaskGroups or using asyncio.gather() to avoid
    overusing the await keyword...

    sync game state in phases to make sure we are accessing
    complete information - do this with tasks and have the bot
    run automatically
"""

class GameCommands(commands.Cog):
    CMD_NEW_GAME = 'new'
    CMD_ADD_PLAYER = 'add'
    CMD_REM_PLAYER = 'remove'
    CMD_DEAL = 'deal'
    CMD_DEAL_ALL = 'deal_all'

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
            await self.bot.inter_response(inter, 'Game instance already running')
            return
        
        await self.bot.inter_response(inter, 'Starting...')
        self.in_game = True

        print('Loading deck...')
        self.state.load_cards()
        print('Done.')

        # assert that this isn't in a DM
        if inter.channel:
            # TODO the above line does not adequitely check for a DM - partialmessageable is returned 
            for user in inter.channel.members:
                _ = await self.add_player(inter, user)

            _ = await self.add_player(inter, inter.author)
            await self.bot.inter_response(inter, 'Started game with: {} players'.format(str(len(self.state.players))))
        else:
            print('New game attempted in DM or unusable thread, ignoring.')


    @commands.slash_command(
        name=CMD_DEAL_ALL,
        description='Load cards if needed, deal to all players'
    )
    async def deal_all(self, inter) -> None:
        pass

    @commands.slash_command(
        name=CMD_DEAL,
        description='Load cards if needed, deal to one player'
    )
    async def deal_to(self, inter, user : disnake.User) -> None:
        # maybe create a decorator for where these command can be invoked
        # instead of checking inter context
        player = self.state.players[user.display_name]
        self.state.deal_hand(player)
            """

                BAD - for debugging only
            for card in player.cards.keys():
                await self.bot.dm_user(user, card)
            """
    @commands.slash_command(
        name=CMD_ADD_PLAYER,
        description='Add a new player to an existing game'
    )
    async def add_player(self, inter, user : disnake.User) -> None:
        name : str = user.display_name
        await self.bot.inter_response(inter, 'Adding player: {}'.format(name))

        if self.state.add_player(name):
            await self.bot.dm_user(user, 'Joined game as: {}'.format(name))
        else:
            #TODO handle collisions somehow...
            await self.bot.inter_response(inter, '{} already exists'.format(name))


    # TODO create an event for on member leaving the channel instead of this?
    @commands.slash_command(
        name=CMD_REM_PLAYER,
        description='Remove a new player from the game'
    )
    async def remove_player(self, inter, user : disnake.User) -> None:
        name : str = user.display_name
        await self.bot.inter_response(inter, 'Removing player: {}'.format(name))

        if self.state.remove_player(name):
            await self.bot.dm_user(user, 'You were removed from the game.')
        else:
            await self.bot.inter_response(inter, 'Player not found... retry')


def setup(bot : commands.Bot) -> None:
    bot.add_cog(GameCommands(bot))
