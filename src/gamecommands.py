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
    

    # make me take arguments
    def game_running() -> None:
        def game_status(ctx) -> bool:
            return self.in_game
        return commands.check(game_status)


    @commands.slash_command(
        name=CMD_NEW_GAME,
        description='Start a new game with all present members'
    )
    @commands.guild_only()
    async def new_game(self, inter) -> None:
        if self.in_game:
            await inter.send('Game instance already running')
            return
        
        await inter.send('Starting...')
        self.in_game = True
        self.state.load_cards()

        active_players = []
        for user in inter.channel.members:
            await self.add_player(inter, user)
            active_players.append(user.display_name)

        await self.add_player(inter, inter.author)
        active_players.append(inter.author.display_name)
        await inter.send('Started game with: {}'.format(str(active_players)))


    @commands.slash_command(
        name=CMD_ADD_PLAYER,
        description='Add a new player to an existing game'
    )
    @commands.guild_only()
    async def add_player(self, inter, user : disnake.User) -> None:
        name : str = user.display_name
        player = self.state.add_player(name)
        await inter.send('Added player: {}'.format(name))

        if player:
            await inter.send('{} joined the game!'.format(name))
            await self._deal_to(inter, user)
        else:
            #TODO handle collisions somehow...
            await inter.send('{} already exists'.format(name))


    # TODO create an event for on member leaving the channel as a backup?
    @commands.slash_command(
        name=CMD_REM_PLAYER,
        description='Remove a new player from the game'
    )
    @commands.guild_only()
    async def remove_player(self, inter, user : disnake.User) -> None:
        player = self.state.remove_player(user.display_name)
        if player:
            await inter.send('{} was removed from the game.'.format(player.name))
        else:
            await inter.send('Player not found...')

    async def _deal_to(self, inter, user : disnake.User) -> None:
        player = self.state.players[user.display_name]
        self.state.deal_hand(player)
        for card in player.cards.keys():
            try:
                # in the future, we want to render a view/UI to the user, not 
                # send messages
                await user.send(card)
            except disnake.errors.HTTPException as permissions_issue:
                pass

def setup(bot : commands.Bot) -> None:
    bot.add_cog(GameCommands(bot))

