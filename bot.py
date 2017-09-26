import discord
import asyncio
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
    msg1 = await bot.send_message(context.message.channel, msg)
    await asyncio.sleep(5)
    await bot.delete_message(msg1)


@bot.command(pass_context=True)
@validation()
async def ping(ctx):
    await bot.delete_message(ctx.message)
    msg = await bot.say('Pong!')

    await asyncio.sleep(5)
    await bot.delete_message(msg)


@bot.command(pass_context=True)
@validation()
async def roleid(ctx, message):
    await bot.delete_message(ctx.message)
    for i in ctx.message.server.roles:
        if message.capitalize() == i.name:
            msg = await bot.say(i.name + ' ' + i.id)
            await asyncio.sleep(5)
            await bot.delete_message(msg)


@bot.command(pass_context=True)
@validation()
async def userid(ctx):
    await bot.delete_message(ctx.message)
    mentioned = ctx.message.mentions[0]
    msg = await bot.say(mentioned.name+' '+mentioned.id)
    await asyncio.sleep(5)
    await bot.delete_message(msg)


@bot.command(pass_context=True)
@validation()
async def presence(ctx, message):
    # await bot.delete_message(ctx.message)
    if message == 'stop':
        await bot.change_presence(game=None)
    else:
        await bot.change_presence(game=discord.Game(name=message, status=None, afk=False))


@bot.command(pass_context=True)
@validation()
async def joined(ctx, member: discord.Member):
    await bot.delete_message(ctx.message)
    joined = str(member.joined_at).split('.', 1)[0]
    msg = await bot.say('{0.name} joined in '.format(member) + joined)

    await asyncio.sleep(5)
    await bot.delete_message(msg)


@bot.command(pass_context=True)
@validation()
async def color(ctx, message):
    await bot.delete_message(ctx.message)
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

    msg = await bot.say('Changed your profile color to '+role_color+' !!')

    await asyncio.sleep(5)
    await bot.delete_message(msg)


@bot.command(pass_context=True)
@validation()
async def flip(ctx):
    await bot.delete_message(ctx.message)
    coin = random.randint(1, 2)
    msg = await bot.say('Flipping a coin!!')

    if coin == 1:
        msg2 = await bot.edit_message(msg, 'You flipped Heads!!')
    if coin == 2:
        msg2 = await bot.edit_message(msg, 'You flipped Tails!!')

    await asyncio.sleep(5)
    await bot.delete_message(msg2)


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


@bot.command(pass_context=True)
@validation()
async def profile(ctx):
    await bot.delete_message(ctx.message)
    mentioned = ctx.message.mentions[0]

    embed = discord.Embed(
        color=mentioned.color,
    )
    embed.set_author(
        name="User Info: " + mentioned.name + "#" + mentioned.discriminator,
    )
    embed.add_field(
        name="ID",
        value=mentioned.id,
        inline=True
    )
    embed.add_field(
        name="Nickname",
        value=mentioned.display_name,
        inline=True
    )
    embed.add_field(
        name="Status",
        value=mentioned.status,
        inline=True
    )
    embed.add_field(
        name="Playing",
        value=mentioned.game,
        inline=True
    )
    embed.add_field(
        name="Role",
        value=mentioned.top_role,
        inline=True
    )
    embed.add_field(
        name="Avatar",
        value="[Full size](" + mentioned.avatar_url + ")",
        inline=True
    )
    embed.add_field(
        name="Account Created",
        value=str(mentioned.created_at).split('.', 1)[0],
        inline=True
    )
    embed.add_field(
        name="Join Date",
        value=str(mentioned.joined_at).split('.', 1)[0],
        inline=True
    )
    embed.set_thumbnail(
        url=mentioned.avatar_url
    )
    msg = await bot.say(embed=embed)
    await asyncio.sleep(15)
    await bot.delete_message(msg)


bot.run(config.token)
