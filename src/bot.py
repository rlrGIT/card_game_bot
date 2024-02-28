import disnake
import os

from dotenv import load_dotenv
from typing import Final

from disnake import Intents
from disnake.ext import commands

class Bot(commands.InteractionBot):
    GAME_COG = 'gamecommands' # name of file containing commands

    def __init__(self) -> None:
        self.running = True

        super().__init__(
                max_messages=None,
                intents=disnake.Intents.default(),
                command_sync_flags=commands.CommandSyncFlags.default()
        )

        self.add_app_command_check(
                self.permissions_check,
                slash_commands=True,
                user_commands=True,
                message_commands=True
        )
    
    async def on_ready(self) -> None: #Override
        print('Logged in as: {}'.format(self.user))

    async def permissions_check(self, inter) -> bool:
        return await self.is_owner(inter.author)


    async def dm_user(self, user : disnake.User, msg : str) -> None:
        if not user.bot:
            try:
                await user.send(content=msg)

            except disnake.errors.HTTPException as failed_to_send:
                print(failed_to_send)
            except disnake.Forbidden as permissions:
                print(permissions)
            except TypeError as type_error:
                print(type_error)
            except ValueError as file_size:
                print(file_size)


    async def respond_with(self, inter : disnake.Interaction, msg : str) -> None:
        try:
            await inter.send(content=msg)

        except disnake.errors.HTTPException as failed_to_send:
            print(failed_to_send)
        except disnake.Forbidden as permissions:
            print(permissions)
        except TypeError as type_error:
            print(type_error)
        except ValueError as file_size:
            print(file_size)

    

    def launch(self) -> None:
        load_dotenv()
        TOKEN : Final[str] = os.getenv('DISCORD_TOKEN')
        # need this for each cog
        #self.add_app_command_check(slash_commands=True)
        self.load_extension(self.GAME_COG)
        self.run(token=TOKEN)
