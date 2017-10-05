import discord
import asyncio
import random
from discord.ext import commands
from .experience import Experience
experience = Experience()


class Members():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        msg = '{0.name} joined in {0.joined_at}'.format(member)
        Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def profile(self, ctx, member: discord.Member):
        """Displays a members' profile."""
        mentioned = member
        roles = str([r.name for r in member.roles if '@everyone' not in r.name]).strip('[]').replace(', ', '\n').replace("'", '')
        if roles is '':
            roles = 'Member has no assigned roles.'

        Embed = discord.Embed(
            color=ctx.message.server.me.color
        )
        Embed.set_author(
            name="Member Info: " + mentioned.name + "#" + mentioned.discriminator,
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
            value=roles,
            inline=True
        )
        Embed.add_field(
            name="Avatar",
            value="[Full size](" + mentioned.avatar_url + ")",
            inline=True
        )
        Embed.add_field(
            name="Rusty points",
            value=experience.getxp(mentioned),
            inline=True
        )
        Embed.add_field(
            name="Rank",
            value=experience.getrank(mentioned),
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
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(10)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def color(self, ctx, color: str):
        """Change the color of the member's nickname."""
        author = ctx.message.author
        role_color = color
        role_colorint = int(color, 16)
        role = discord.utils.get(author.server.roles, name=author.name)
        if role is None:
            role = await self.bot.create_role(ctx.message.server, name=author.name, color=discord.Colour(role_colorint), hoist=False, mentionable=False)
            position = None
            for i in ctx.message.server.roles:
                if i.name.lower() == 'member':
                    position = i
            await self.bot.move_role(ctx.message.server, role, position=position.position)
            await self.bot.add_roles(author, role)
        elif role in ctx.message.server.roles:
            await self.bot.edit_role(ctx.message.server, role, colour=discord.Colour(role_colorint))

        msg = 'Changed {}\'s nickname color to '+str(role_color)+' !!'.format(author.name)
        Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

# TODO: maybe use this try exception methode with every command, custom error message
    @commands.command(pass_context=True)
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            msg = ctx.message.author.name + ' rolled: ' + dice + ' and got ' + ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
            Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=Embed)
        except Exception:
            msg = 'Format has to be in NdN!'
            Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
            message = await self.bot.send_message(ctx.message.channel, embed=Embed)
            await asyncio.sleep(5)
            await self.bot.delete_message(message)

        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def choose(self, ctx, *choice: str):
        """Chooses between multiple choices."""
        choices = str([i for i in choice]).strip('[]').replace("'", '')
        msg = self.bot.user.name + ' chose: ' + random.choice(choice) + '\nFrom the following choices: ' + choices
        Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """Flips a coin."""
        author = ctx.message.author
        coin = random.randint(1, 2)
        if coin == 1:
            experience.setxp(author, 5)
            msg = '{} flipped Heads and received 5 Rusty points!!'.format(author.name)
            Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        if coin == 2:
            experience.removexp(author, 2)
            msg = '{} flipped tails and lost 2 Rusty points!!'.format(author.name)
            Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def jump(self, ctx):
        """Join Rusty."""
        author = ctx.message.author
        if experience.getxp(author) < 10:
            msg = 'You dont have enough Rusty points, current amount {}\nYou need 10 Rusty points to join him\nFlip coins to win Rusty points!!'.format(experience.getxp(author))
            Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
            message = await self.bot.send_message(ctx.message.channel, embed=Embed)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)
            await self.bot.delete_message(message)
        else:
            experience.removexp(author, 10)
            msg = author.name + ' jumped and joined Rusty'
            Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
            Embed.set_image(url='https://cdn.discordapp.com/attachments/355869544113373184/356221955109814273/YouEvenStarcraft2.png')
            await self.bot.send_message(ctx.message.channel, embed=Embed)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Members(bot))
