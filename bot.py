import logging
import discord
import datetime
import asyncio
from discord.ext import commands
from cogs.util.config import Configuration
config = Configuration()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

description = '''Omega chat bot'''
startup_extensions = ["members", "moderator", "help"]
bot = commands.Bot(command_prefix=config.prefix, description=description)


@bot.event
async def on_ready():
    logger.info('Loading the bot')
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(date)
    print('------')


@bot.event
async def on_command_error(exception, context):
    if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
        msg = """Sorry, this command is unknown to me... \
                \nType !help [command] to get help."""
        print('CommandNotFound: ' + str(type(exception)) + str(exception))
    elif isinstance(exception,
                    discord.ext.commands.errors.CheckFailure):
        msg = """you are not allowed to do this... """
        print('CheckFailure: ' + str(type(exception)) + str(exception))
    elif isinstance(exception,
                    discord.ext.commands.errors.MissingRequiredArgument):
        msg = """You forgot parameters... \
                \nType !help [command] to get help."""
        print('MissingRequiredArgument: ' + str(type(exception)) + str(exception))
    elif isinstance(exception,
                    discord.ext.commands.errors.BadArgument):
        msg = """Wrong parameters... \
                \nType !help [command] to get help."""
        print('BadArgument: ' + str(type(exception)) + str(exception))
    elif isinstance(exception,
                    discord.ext.commands.errors.CommandInvokeError):
        msg = """Sorry, there is no such command... \
                \nType !help [command] to get help."""
        print('CommandInvokeError: ' + str(type(exception)) + str(exception))
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
            print('Loaded extension: ' + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.token)
