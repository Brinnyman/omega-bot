import discord
import asyncio
import random
import os
from discord.ext import commands
from tinydb import TinyDB
from tinydb import where
from .util.permission import Permission
permit = Permission()

path = os.path.abspath('')
db_file = os.path.join(path, 'config', 'db.json')
db = TinyDB(db_file)


class Game():
    def __init__(self, bot):
        self.bot = bot

    def getpoints(self, user):
        try:
            userid = user.id
            if db.search(where('userid') == userid):
                for data in db.search(where('userid') == userid):
                    return data['points']
            else:
                db.insert({'userid': userid, 'points': 0})
                return 0
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))

    def setpoints(self, user, points):
        try:
            userid = user.id
            points = int(points)
            if db.search(where('userid') == userid):
                for data in db.search(where('userid') == userid):
                    points += data['points']
                    db.update({'points': points}, where('userid') == userid)
            else:
                db.insert({'userid': userid, 'points': points})
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))

    def removepoints(self, user, points):
        try:
            userid = user.id
            points = int(points)
            if db.search(where('userid') == userid):
                for data in db.search(where('userid') == userid):
                    if data['points'] - points < 0:
                        data['points'] = 0
                    else:
                        data['points'] -= points

                    db.update({'points': data['points']}, where('userid') == userid)
            else:
                db.insert({'userid': userid, 'points': points})
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))

    def getrank(self, user):
        try:
            points = self.getpoints(user)
            rank = ''

            if points >= 100:
                rank = 'King'
            elif points >= 50:
                rank = 'Alpha'
            elif points >= 0:
                rank = 'Pleb'
            return rank
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))

    @permit.check()
    @commands.command(pass_context=True)
    async def showxp(self, ctx, member: discord.Member):
        """Displays a members' experience points."""
        try:
            message = '{} currently has {} experience points and is a {}!!'.format(member.name, self.getpoints(member), self.getrank(member))
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, message)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True)
    async def givexp(self, ctx, member: discord.Member, amount: str):
        """Give experience points to a members."""
        try:
            self.setpoints(member, amount)
            message = member.name + ' gained ' + amount + ' experience points!!'
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, message)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @permit.check()
    @commands.command(pass_context=True)
    async def removexp(self, ctx, member: discord.Member, amount: str):
        """Removes experience points from a members."""
        try:
            self.removepoints(member, amount)
            message = member.name + ' lost ' + amount + ' experience points!!'
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, message)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """Flips a coin."""
        try:
            coin = random.randint(1, 2)
            if coin == 1:
                self.setpoints(ctx.message.author, 5)
                message = '{} flipped Heads and received 5 Rusty points!!'.format(ctx.message.author.name)
            elif coin == 2:
                self.removepoints(ctx.message.author, 2)
                message = '{} flipped tails and lost 2 Rusty points!!'.format(ctx.message.author.name)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.send_message(ctx.message.channel, message)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def jump(self, ctx):
        """Join Rusty."""
        try:
            if self.getpoints(ctx.message.author) < 10:
                message = 'You dont have enough Rusty points, current amount {}\n'.format(self.getpoints(ctx.message.author))
                message += 'You need 10 Rusty points to join him\nFlip coins to win Rusty points!!'
                msg = await self.bot.send_message(ctx.message.channel, message)
            else:
                self.removepoints(ctx.message.author, 10)
                message = ctx.message.author.name + ' jumped and joined Rusty'
                Embed = discord.Embed(description=message, color=ctx.message.server.me.color)
                Embed.set_image(url='https://cdn.discordapp.com/attachments/355869544113373184/356221955109814273/YouEvenStarcraft2.png')
                await self.bot.send_message(ctx.message.channel, embed=Embed)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await asyncio.sleep(5)
            await self.bot.delete_message(msg)
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Game(bot))
