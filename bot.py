import discord
from discord.ext import commands
from config import Configuration
from validation import validation
from karma import Karma
import random
import math

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
    await bot.send_message(context.message.channel, msg)


@bot.command(pass_context=True)
@validation()
async def ping(ctx):
    await bot.say('Pong!')


@bot.command(pass_context=True)
@validation()
async def roleid(ctx):
    for i in ctx.message.server.roles:
        await bot.say(i.name + ' ' + i.id)


@bot.command(pass_context=True)
@validation()
async def presence(ctx, message):
    if message == 'stop':
        await bot.change_presence(game=None)
    else:
        await bot.change_presence(game=discord.Game(name=message, status=None, afk=False))


@bot.command(pass_context=True)
@validation()
async def joined(ctx, member: discord.Member):
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.command(pass_context=True)
@validation()
async def color(ctx, message):
    role_color = int(message, 16)
    role = discord.utils.get(ctx.message.server.roles, name=ctx.message.author.name)
    if role is None:
        role = await bot.create_role(ctx.message.server, name=ctx.message.author.name, color=discord.Colour(role_color), hoist=False, mentionable=False)
        position = None
        for i in ctx.message.server.roles:
            if i.name.lower() == 'member':
                position = i
        await bot.move_role(ctx.message.server, role, position=position.position)
        await bot.add_roles(ctx.message.author, role)
    elif role in ctx.message.server.roles:
        await bot.edit_role(ctx.message.server, role, colour=discord.Colour(role_color))


@bot.command(pass_context=True)
@validation()
async def flip(ctx):
    coin = random.randint(1, 2)
    await bot.say('Flipping a coin!!!')
    if coin == 1:
        await bot.say('Heads')
    if coin == 2:
        await bot.say('Tails')


@bot.command(pass_context=True)
@validation()
async def givexp(ctx):
    counter = 0
    mentioned = ctx.message.mentions[0]

    async for msg in bot.logs_from(ctx.message.channel, limit=9999999):
        if msg.author == mentioned:
            counter += 1

    # mesg = await bot.say('Calculating...')
    modifier = 1.5
    xp = math.ceil(counter * modifier)
    karma = Karma()
    karma._process_scores(mentioned, xp)
    # await bot.edit_message(mesg, '{} has {}xp in the {} channel.'.format(mentioned.name, karma._check_score(mentioned), ctx.message.channel))


@bot.command(pass_context=True)
async def getKarma(ctx):
    karma = Karma()
    mentioned = ctx.message.mentions[0]
    await bot.say('{} has {}xp in the {} channel.'.format(mentioned.name, karma._check_score(mentioned), ctx.message.channel))


bot.run(config.token)
