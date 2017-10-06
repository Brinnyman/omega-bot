import discord
import asyncio
from discord.ext import commands
from .util.permission import Permission
permit = Permission()


class Moderator():
    def __init__(self, bot):
        self.bot = bot

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def ping(self, ctx):
        """Sends a ping to the bot"""
        await self.bot.send_message(ctx.message.channel, 'pong')
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def presence(self, ctx, *, game: str=None):
        """Change the status to 'playing <game>'"""
        try:
            if game:
                await self.bot.change_presence(game=discord.Game(name=game, status=None, afk=False))
            else:
                await self.bot.change_presence(game=discord.Game(name=game, status=None, afk=False))
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, 'presence updated.')
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def load(self, ctx, *, extension: str):
        """Loads an extension."""
        extension = 'cogs.{}'.format(extension)
        try:
            self.bot.load_extension(extension)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            print(extension + ' extension loaded')
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, extension: str):
        """Unloads an extension."""
        extension = 'cogs.{}'.format(extension)
        try:
            self.bot.unload_extension('cogs.'+extension)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            print(extension + ' extension unloaded')
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def reload(self, ctx, *, extension: str):
        """Reloads an extension."""
        extension = 'cogs.{}'.format(extension)
        try:
            self.bot.unload_extension('cogs.'+extension)
            await asyncio.sleep(1)
            self.bot.load_extension('cogs.'+extension)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            print(extension + ' extension reloaded')
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Moderator(bot))
