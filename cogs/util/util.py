import discord
import datetime
from .config import Configuration
config = Configuration()


class Util():
    def __init__(self, bot):
        self.bot = bot

    async def on_message_delete(self, message):
        if message.author.id is not message.server.me.id:
            if message.content[:1] is not '!':
                if len(message.attachments) > 0:
                    content = message.attachments[0].get('url')
                else:
                    content = message.content

                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Embed = discord.Embed(description='Message deleted:', color=message.server.me.color)
                Embed.add_field(name='Message:', value=content, inline=False)
                Embed.add_field(name='Channel:', value=message.channel, inline=False)
                Embed.add_field(name='Author:', value=message.author, inline=False)
                Embed.set_footer(text='Deleted on {}'.format(date))
                await self.bot.send_message(self.bot.get_channel(config.logchannel), embed=Embed)

    async def on_message_edit(self, before, after):
        if before.author.id is not before.server.me.id:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Embed = discord.Embed(description='Message edited:', color=before.server.me.color)
            Embed.add_field(name='Before:', value=before.content, inline=False)
            Embed.add_field(name='After:', value=after.content, inline=False)
            Embed.add_field(name='Author:', value=before.author, inline=False)
            Embed.add_field(name='Channel:', value=before.channel, inline=False)
            Embed.set_footer(text='Edited on {}'.format(date))
            await self.bot.send_message(self.bot.get_channel(config.logchannel), embed=Embed)


def setup(bot):
    bot.add_cog(Util(bot))
