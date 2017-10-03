import discord
import asyncio
from discord.ext import commands
from .experience import Experience
from .permission import Permission
experience = Experience()
permit = Permission()


class Game():
    def __init__(self, bot):
        self.bot = bot

    @permit.check()
    @commands.command(pass_context=True)
    async def showxp(self, ctx, member: discord.Member):
        """Displays a members' experience points."""
        # msg = '{} currently has {} experience points!!'.format(member.name, experience.getxp(member))
        msg = '{} currently has {} experience points and is a {}!!'.format(member.name, experience.getxp(member), experience.getrank(member))
        Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True)
    async def givexp(self, ctx, member: discord.Member, amount: str):
        """Gives a member experience points."""
        experience.setxp(member, amount)
        msg = member.name + ' received ' + amount + ' experience points!!'
        Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)

        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True)
    async def removexp(self, ctx, member: discord.Member, amount: str):
        """Removes experience points from a members."""
        experience.removexp(member, amount)
        msg = member.name + ' lost ' + amount + ' experience points!!'
        Embed = discord.Embed(description=msg, color=ctx.message.server.me.color)
        Embed.set_footer(text='Invoked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=Embed)

        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Game(bot))
