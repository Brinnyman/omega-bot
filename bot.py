import discord
import asyncio
from discord.ext import commands
from config import Configuration
from validation import validation
from member import Member
import random

config = Configuration()
member = Member()
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


async def delete_message(time, invoke, response):
    await asyncio.sleep(time)
    await bot.delete_message(invoke)
    await bot.delete_message(response)


# mod commands
@bot.command(pass_context=True)
@validation()
async def ping(ctx):
    msg = await bot.say('Pong!')
    await delete_message(5, ctx.message, msg)


@bot.command(pass_context=True)
@validation()
async def roleid(ctx, message):
    for i in ctx.message.server.roles:
        if message.capitalize() == i.name:
            msg = await bot.say(i.name + ' ' + i.id)
            await delete_message(5, ctx.message, msg)


@bot.command(pass_context=True)
@validation()
async def userid(ctx):
    mentioned = ctx.message.mentions[0]
    msg = await bot.say(mentioned.name+' '+mentioned.id)
    await delete_message(5, ctx.message, msg)


@bot.command(pass_context=True)
@validation()
async def presence(ctx, message):
    await bot.delete_message(ctx.message)
    if message == 'stop':
        await bot.change_presence(game=None)
    else:
        await bot.change_presence(game=discord.Game(name=message, status=None, afk=False))


# member commands
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

    msg = await bot.say('Changed your profile color to '+message+' !!')
    await delete_message(5, ctx.message, msg)


@bot.command(pass_context=True)
@validation()
async def flip(ctx):
    coin = random.randint(1, 2)
    msg = await bot.say('Flipping a coin!!')

    await asyncio.sleep(2)
    if coin == 1:
        msg2 = await bot.edit_message(msg, 'You flipped Heads!!')
    if coin == 2:
        msg2 = await bot.edit_message(msg, 'You flipped Tails!!')

    await delete_message(5, ctx.message, msg2)


@bot.command(pass_context=True)
@validation()
async def profile(ctx):
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
    await delete_message(15, ctx.message, msg)


@bot.command(pass_context=True)
async def givexp(ctx, message):
    mentioned = ctx.message.mentions[0]
    member.setxp(mentioned, message)
    await bot.say('{} received {} experience!!'.format(mentioned.name, message))


@bot.command(pass_context=True)
async def removexp(ctx, message):
    mentioned = ctx.message.mentions[0]
    await bot.say('{} lost {} experience!!'.format(mentioned.name, message))


@bot.command(pass_context=True)
async def showxp(ctx):
    mentioned = ctx.message.mentions[0]
    await bot.say('{} has {} experience in channel {}'.format(mentioned.name, member.getxp(mentioned), ctx.message.channel))


# @bot.command(pass_context=True)
# async def calculatexp(ctx):
#     oldxp = 0
#     mentioned = ctx.message.mentions[0]
#     async for msg in bot.logs_from(ctx.message.channel, limit=9999999):
#         if msg.author == mentioned:
#             oldxp += 1
#
#     member.checkxp(mentioned, oldxp)
#     await bot.say('{} had {} experience in channel {}'.format(mentioned.name, oldxp, ctx.message.channel))


bot.run(config.token)
