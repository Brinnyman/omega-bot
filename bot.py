import discord
import asyncio
from discord.ext import commands
from cogs.config import Configuration
from cogs.permission import Permission
config = Configuration()
permit = Permission()

description = '''Omega chat bot'''
startup_extensions = ["members", "moderator", "help"]
bot = commands.Bot(command_prefix=config.prefix, description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='observing...', status=None, afk=False))


@bot.event
async def on_command_error(exception, context):
    if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
        msg = """Sorry, this command is unknown to me... \
                \nType !help [command] to get help."""
    elif isinstance(exception,
                    discord.ext.commands.errors.CheckFailure):
        msg = """you are not allowed to do this... """
    elif isinstance(exception,
                    discord.ext.commands.errors.MissingRequiredArgument):
        msg = """You forgot parameters... \
                \nType !help [command] to get help."""
    elif isinstance(exception,
                    discord.ext.commands.errors.BadArgument):
        msg = """Wrong parameters... \
                \nType !help [command] to get help."""
    elif isinstance(exception,
                    discord.ext.commands.errors.CommandInvokeError):
        msg = """Sorry, there is no such command... \
                \nType !help [command] to get help."""
    else:
        print("inconnu... " + str(type(exception)) + str(exception))

    message = await bot.send_message(context.message.channel, "```py\n{}\n```".format(msg))
    await asyncio.sleep(5)
    await bot.delete_message(message)
    await bot.delete_message(context.message)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension('cogs.' + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.token)
