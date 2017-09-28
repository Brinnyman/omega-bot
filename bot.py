import discord
import asyncio
from discord.ext import commands
from Util.config import Configuration
import Util.commands as Commands
# msg = await bot.say(embed=embed)
# await delete_message(5, ctx.message, msg)
config = Configuration()
bot = commands.Bot(command_prefix=config.prefix)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_command_error(exception, context):
    if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
        msg = """:robot:  Sorry, this command is unknown to me... \
                    \nType !help [command] to get help."""
    elif isinstance(exception,
                    discord.ext.commands.errors.CheckFailure):
        msg = """:robot: you are not allowed to do this... """
    elif isinstance(exception,
                    discord.ext.commands.errors.MissingRequiredArgument):
        msg = """:robot: You forgot parameters... \
                    \nType !help [command] to get help."""
    else:
        msg = "inconnu... " + str(type(exception)) + str(exception)

    print(msg)
    msg1 = await bot.send_message(context.message.channel, msg)
    await asyncio.sleep(5)
    await bot.delete_message(msg1)


command_list = {
    "!ping": Commands.ping,
    "!presence": Commands.presence,
    "!flip": Commands.flip,
    "!profile": Commands.profile,
    "!color": Commands.color,
    "!showxp": Commands.showxp,
    "!givexp": Commands.givexp,
    "!removexp": Commands.removexp
    }


@bot.event
async def on_message(message):
    author = message.author
    for command, function in command_list.items():
        if message.content.startswith(command):
            await function(bot, author, message)

bot.run(config.token)
