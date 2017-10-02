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
        Embed = discord.Embed(description=msg, color=0x42f4a1)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def profile(self, ctx, member: discord.Member):
        """Displays a members' profile."""
        mentioned = member
        roles = str([r.name for r in member.roles if '@everyone' and mentioned.name not in r.name]).strip('[]').replace(', ', '\n').replace("'", '')
        if roles is '':
            roles = 'Member has no assigned roles.'

        Embed = discord.Embed(
            color=0x42f4a1,
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
        Embed = discord.Embed(description=msg, colour=0x42f4a1)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

# TODO: maybe use this try exception methode with every command, custom error message
    @commands.command(pass_context=True)
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        rolls, limit = map(int, dice.split('d'))
        msg = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        Embed = discord.Embed(description=msg, colour=0x42eef4)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

        # try:
        #     rolls, limit = map(int, dice.split('d'))
        #     msg = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        #     Embed = discord.Embed(description=msg, colour=0x42eef4)
        #     print(Embed.to_dict())
        #     await self.bot.send_message(ctx.message.channel, embed=Embed)
        # except Exception:
        #     msg = 'Format has to be in NdN!'
        #     Embed = discord.Embed(description=msg, colour=0x42eef4)
        #     await self.bot.send_message(ctx.message.channel, embed=Embed)
        #     return

    @commands.command(pass_context=True)
    async def choose(self, ctx, *choice: str):
        """Chooses between multiple choices."""
        choices = str([i for i in choice]).strip('[]').replace("'", '')
        msg = self.bot.user.name + ' chose: ' + random.choice(choice) + '\nfrom the following choices: ' + choices
        Embed = discord.Embed(description=msg, colour=0x42eef4)
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
            msg = '{} flipped Heads and received 5 experience points!!'.format(author.name)
            Embed = discord.Embed(description=msg, colour=0x42f4a1)
        if coin == 2:
            msg = '{} flipped tails and lost 5 experience points!!'.format(author.name)
            Embed = discord.Embed(description=msg, colour=0x42f4a1)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Members(bot))
