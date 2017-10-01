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

    @commands.command(pass_context=True)
    async def showxp(self, ctx, member: discord.Member):
        """Displays a members' experience points."""
        msg = '{} currently has {} experience points!!'.format(member.name, experience.getxp(member))
        Embed = discord.Embed(description=msg, colour=0x42eef4)
        message = await self.bot.send_message(ctx.message.channel, embed=Embed)
        await asyncio.sleep(5)
        await self.bot.delete_message(message)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def givexp(self, ctx, member: discord.Member, amount: str):
        """Gives a member experience points."""
        if(permit.check_command(ctx.message.author, ctx.message.content.split(' ', 1)[0][1:])):
            experience.setxp(member, amount)
            msg = member.name + ' received ' + amount + ' experience points!!'
            Embed = discord.Embed(description=msg, colour=0x42eef4)
            message = await self.bot.send_message(ctx.message.channel, embed=Embed)
        else:
            msg = 'You dont have the right permission!!'
            Embed = discord.Embed(description=msg, colour=0x42f4a1)
            message = await self.bot.send_message(ctx.message.channel, embed=Embed)

        await asyncio.sleep(5)
        await self.bot.delete_message(message)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def removexp(self, ctx, member: discord.Member, amount: str):
        """Removes experience points from a members."""
        if(permit.check_command(ctx.message.author, ctx.message.content.split(' ', 1)[0][1:])):
            experience.removexp(member, amount)
            msg = member.name + ' lost ' + amount + ' experience points!!'
            Embed = discord.Embed(description=msg, colour=0x42eef4)
            message = await self.bot.send_message(ctx.message.channel, embed=Embed)
        else:
            msg = 'You dont have the right permission!!'
            Embed = discord.Embed(description=msg, colour=0x42f4a1)
            message = await self.bot.send_message(ctx.message.channel, embed=Embed)

        await asyncio.sleep(5)
        await self.bot.delete_message(message)
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Game(bot))
