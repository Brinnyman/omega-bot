import discord
import random
from .config import Configuration
from .permission import Permission
from .experience import Experience
config = Configuration()
permit = Permission()
experience = Experience()


def validation():
    def decorator(function):
        async def wrapper(*args):
            client = args[0]
            author = args[1]
            message = args[2]
            command = message.content.split(' ', 1)[0][1:]
            print(author.name, command)
            if author.id == config.ownerid:
                return await function(*args)
            else:
                for i in author.roles:
                    if i.id in config.permitted:
                        if permit.check_command(i.name, command):
                            return await function(*args)
                        else:
                            return await client.send_message(message.channel, 'You dont have the right permission!!')
        return wrapper
    return decorator


def embed_command():
    def decorator(function):
        async def wrapper(*args):
            client = args[0]
            message = args[2]
            embed = await function(*args)
            await client.send_message(message.channel, embed=embed)
        return wrapper
    return decorator


@validation()
@embed_command()
async def ping(client, author, message):
    msg = 'Pong!'
    Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
    Embed.set_author(name=author.name, icon_url=author.avatar_url)
    print(Embed.to_dict())
    return Embed


@validation()
async def presence(client, author, message):
    state = message.content.split(' ', 1)[-1]
    if state == message.content:
        await client.change_presence(game=None)
    else:
        await client.change_presence(game=discord.Game(name=state, status=None, afk=False))


@validation()
@embed_command()
async def flip(client, author, message):
    coin = random.randint(1, 2)
    msg = 'Flipping a coin!!'
    Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
    Embed.set_author(name=author.name, icon_url=author.avatar_url)

    if coin == 1:
        msg = 'You flipped Heads and received 5 experience points!! '
        experience.setxp(author, 5)
        Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
        Embed.set_author(name=author.name, icon_url=author.avatar_url)
    if coin == 2:
        msg = 'You flipped tails and lost 5 experience points!!'
        experience.removexp(author, 5)
        Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
        Embed.set_author(name=author.name, icon_url=author.avatar_url)
    print(Embed.to_dict())
    return Embed


@validation()
@embed_command()
async def profile(client, author, message):
    mentioned = message.mentions[0]

    Embed = discord.Embed(
        color=mentioned.color,
    )
    Embed.set_author(
        name="User Info: " + mentioned.name + "#" + mentioned.discriminator,
    )
    Embed.add_field(
        name="ID",
        value=mentioned.id,
        inline=True
    )
    Embed.add_field(
        name="Nickname",
        value=mentioned.display_name,
        inline=True
    )
    Embed.add_field(
        name="Status",
        value=mentioned.status,
        inline=True
    )
    Embed.add_field(
        name="Playing",
        value=mentioned.game,
        inline=True
    )
    Embed.add_field(
        name="Role",
        value=mentioned.top_role,
        inline=True
    )
    Embed.add_field(
        name="Avatar",
        value="[Full size](" + mentioned.avatar_url + ")",
        inline=True
    )
    Embed.add_field(
        name="Experience points",
        value=experience.getxp(mentioned),
        inline=True
    )
    Embed.add_field(
        name="Account Created",
        value=str(mentioned.created_at).split('.', 1)[0],
        inline=True
    )
    Embed.add_field(
        name="Join Date",
        value=str(mentioned.joined_at).split('.', 1)[0],
        inline=True
    )
    Embed.set_thumbnail(
        url=mentioned.avatar_url
    )
    print(Embed.to_dict())
    return Embed


@validation()
@embed_command()
async def color(client, author, message):
    role_color = message.content.split(' ', 1)[-1]
    role_colorint = int(message.content.split(' ', 1)[-1], 16)
    role = discord.utils.get(author.server.roles, name=author.name)
    if role is None:
        role = await client.create_role(message.server, name=message.author.name, color=discord.Colour(role_colorint), hoist=False, mentionable=False)
        position = None
        for i in message.server.roles:
            if i.name.lower() == 'member':
                position = i
        await client.move_role(message.server, role, position=position.position)
        await client.add_roles(message.author, role)
    elif role in message.server.roles:
        await client.edit_role(message.server, role, colour=discord.Colour(role_colorint))

    msg = 'Changed your profile color to '+str(role_color)+' !!'
    Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
    Embed.set_author(name=author.name, icon_url=author.avatar_url)
    print(Embed.to_dict())
    return Embed


@validation()
@embed_command()
async def showxp(client, author, message):
    mentioned = message.mentions[0]
    msg = '{} currently has {} experience points!!'.format(mentioned.name, experience.getxp(mentioned))
    Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
    Embed.set_author(name=author.name, icon_url=author.avatar_url)
    print(Embed.to_dict())
    return Embed


@validation()
@embed_command()
async def givexp(client, author, message):
    mentioned = message.mentions[0]
    amount = message.content.split(' ', 2)[2]
    experience.setxp(mentioned, amount)
    msg = mentioned.name + '#' + mentioned.discriminator + ' received ' + amount + ' experience points!!'
    Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
    Embed.set_author(name=author.name, icon_url=author.avatar_url)
    print(Embed.to_dict())
    return Embed


@validation()
@embed_command()
async def removexp(client, author, message):
    mentioned = message.mentions[0]
    amount = message.content.split(' ', 2)[2]
    experience.removexp(mentioned, amount)
    msg = mentioned.name + '#' + mentioned.discriminator + ' lost ' + amount + ' experience points!!'
    Embed = discord.Embed(description=msg, colour=0x42eef4, title="")
    Embed.set_author(name=author.name, icon_url=author.avatar_url)
    print(Embed.to_dict())
    return Embed
