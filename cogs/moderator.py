import logging
import discord
import asyncio
from discord.ext import commands
from .util.permission import Permission
permit = Permission()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Moderator():
    def __init__(self, bot):
        logger.info('Initialize the moderator class')
        self.bot = bot

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def ping(self, ctx):
        logger.info('Sends a ping to the bot')
        """Sends a ping to the bot"""
        await self.bot.send_message(ctx.message.channel, 'pong')
        await asyncio.sleep(5)
        await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def presence(self, ctx, *, game: str=None):
        logger.info('Changing the status of the bot')
        """Change the status to 'playing <game>'"""
        try:
            if game:
                logger.info('Given change_presence arguments is ' + game)
                await self.bot.change_presence(game=discord.Game(name=game, status=None, afk=False))
            else:
                logger.info('Given change_presence arguments is None')
                await self.bot.change_presence(game=discord.Game(name=game, status=None, afk=False))
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            logger.info('Changed the status of the bot')
            await self.bot.send_message(ctx.message.channel, 'presence updated.')
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def load(self, ctx, *, extension: str):
        logger.info('Loading extension: ' + extension)
        """Loads an extension."""
        extension = 'cogs.{}'.format(extension)
        try:
            logger.info('loading extension: ' + extension)
            self.bot.load_extension(extension)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            logger.info('Loaded extension: ' + extension)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, extension: str):
        logger.info('Unloading extension: ' + extension)
        """Unloads an extension."""
        extension = 'cogs.{}'.format(extension)
        try:
            logger.info('unloading extension: ' + extension)
            self.bot.unload_extension(extension)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            logger.info('Unloaded extension: ' + extension)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True, hidden=True)
    async def reload(self, ctx, *, extension: str):
        logger.info('Reloading extension: ' + extension)
        """Reloads an extension."""
        extension = 'cogs.{}'.format(extension)
        try:
            self.bot.unload_extension(extension)
            logger.info('unloading extension: ' + extension)
            await asyncio.sleep(1)
            self.bot.load_extension(extension)
            logger.info('loading extension: ' + extension)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            logger.info('Reloaded extension: ' + extension)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)


def setup(bot):
    logger.info('Setting up the moderator class')
    bot.add_cog(Moderator(bot))
