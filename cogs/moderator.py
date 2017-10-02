import discord
import asyncio
from discord.ext import commands
from .permission import Permission
permit = Permission()


class Moderator():
    def __init__(self, bot):
        self.bot = bot

    @permit.check()
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Sends a ping to the bot"""
        msg = 'Pong!'
        Embed = discord.Embed(description=msg, colour=0x42f4a1)
        message = await self.bot.send_message(ctx.message.channel, embed=Embed)

        await asyncio.sleep(5)
        await self.bot.delete_message(message)
        await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True)
    async def presence(self, ctx, state: str=None):
        """Change the presence state of the bot"""
        if state:
            await self.bot.change_presence(game=discord.Game(name=state, status=None, afk=False))
        else:
            await self.bot.change_presence(game=discord.Game(name=state, status=None, afk=False))

        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True)
    async def load(self, ctx, *extension_names: str):
        """Loads an extension."""
        for extension in extension_names:
            try:
                self.bot.load_extension('cogs.'+extension)
                msg = "Extension {} has been loaded.".format(extension)
                await self.bot.send_message(ctx.message.channel, "```py\n{}\n```".format(msg))

            except (AttributeError, ImportError) as e:
                await self.bot.send_message(ctx.message.channel, "```py\n{}: {}\n```".format(type(e).__name__, str(e)))
                return

    @permit.check()
    @commands.command(pass_context=True)
    async def unload(self, ctx, *extension_names: str):
        """Unloads an extension."""
        for extension in extension_names:
            if(extension != 'moderator'):
                self.bot.unload_extension('cogs.'+extension)
                msg = "Extension {} has been unloaded.".format(extension)
                await self.bot.send_message(ctx.message.channel, "```py\n{}\n```".format(msg))
            else:
                msg = "Extension {} can not be unloaded.".format(extension)
                await self.bot.send_message(ctx.message.channel, "```py\n{}\n```".format(msg))


def setup(bot):
    bot.add_cog(Moderator(bot))
