import disnake
import os

from dotenv import load_dotenv
from typing import Final

from disnake import Intents
from disnake.ext import commands

class GameBot(commands.Bot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        """ Perhaps add game state and threads to this? """
        self.game_state = None
    
    """ populate other events """

    async def on_ready(self) -> None: #override
        print('Logged in as: {}'.format(self.user))


    async def on_message(self, received : disnake.Message) -> None: #override
        if received.author != self.user:
            """ Send to handling logic! """
    
def default_bot() -> commands.Bot:
    default : disnake.Intents = disnake.Intents.default()
    default.message_content = True # enable bot read access to user messages
    return GameBot(command_prefix='!', intents=default)

def start(instance : commands.Bot) -> None:
    load_dotenv()
    TOKEN : Final[str] = os.getenv('DISCORD_TOKEN')
    instance.run(token=TOKEN)
