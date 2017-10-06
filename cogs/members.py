import discord
import random
import asyncio
from discord.ext import commands


class Members():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def joined(self, ctx, *, member: discord.Member=None):
        """Says when a member joined."""
        try:
            if member is None:
                member = ctx.message.author
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, '{0.name} joined in {0.joined_at}'.format(member))
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def profile(self, ctx, *, member: discord.Member=None):
        """Displays a members' profile."""
        try:
            if member is None:
                member = ctx.message.author
            roles = str([r.name for r in member.roles if '@everyone' not in r.name]).strip('[]').replace(', ', '\n').replace("'", '')
            if roles is '':
                roles = 'Member has no assigned roles.'

            Embed = discord.Embed(
                title='User Information For:',
                description='{0.name}#{0.discriminator}'.format(member),
                color=ctx.message.server.me.color
            )
            Embed.set_author(
                name='{0.name} || #{1.name}'.format(ctx.message.server, ctx.message.channel)
            )
            Embed.add_field(
                name="User ID",
                value=str(member.id),
                inline=True
            )
            Embed.add_field(
                name="Display Name:",
                value=member.display_name if not member.name else '(no display name set)',
                inline=True
            )
            Embed.add_field(
                name="Roles:",
                value=roles,
                inline=False
            )
            Embed.add_field(
                name="Account Created:",
                value=member.created_at.strftime('%b. %d, %Y\n%I:%M %p'),  # ('%Y-%m-%d %H:%M')
                inline=True
            )
            Embed.add_field(
                name="Joined Server:",
                value=member.joined_at.strftime('%b. %d, %Y\n%I:%M %p'),
                inline=True
            )
            Embed.set_thumbnail(
                url=member.avatar_url
            )
            Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, embed=Embed)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def color(self, ctx, *, color: str):
        """Change the color of the member's nickname."""
        try:
            role = discord.utils.get(ctx.message.author.server.roles, name=ctx.message.author.name)
            role_color = int(color, 16)

            if role is None:
                role = await self.bot.create_role(ctx.message.server, name=ctx.message.author.name, color=discord.Colour(role_color), hoist=False, mentionable=False)
                position = None
                for i in ctx.message.server.roles:
                    if i.name.lower() == 'member':
                        position = i
                await self.bot.move_role(ctx.message.server, role, position=position.position)
                await self.bot.add_roles(ctx.message.author, role)
            elif role in ctx.message.server.roles:
                await self.bot.edit_role(ctx.message.server, role, colour=discord.Colour(role_color))
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, 'Changed {}\'s nickname color to {} !!'.format(ctx.message.author.name, str(color)))
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def roll(self, ctx, *, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            message = ctx.message.author.name + ' rolled: ' + dice + ' and got ' + ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, message)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def choose(self, ctx, *choice: str):
        """Chooses between multiple choices."""
        try:
            choices = str([i for i in choice]).strip('[]').replace("'", '')
            choice = random.choice(choice)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, self.bot.user.name + ' chose: ' + random.choice(choice) + '\nFrom the following choices: ' + choices)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Members(bot))
