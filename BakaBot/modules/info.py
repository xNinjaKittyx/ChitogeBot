import json
import requests
import time

import asyncio
import discord
from discord.ext import commands
import psutil
import tools.discordembed as dmbd

class Info:

    def __init__(self, bot):
        self.bot = bot
        self.initialtime = time.time()

    def getuptime(self):
        seconds = int(time.time() - self.initialtime)
        minutes = 0
        hours = 0
        days = 0

        if seconds > 86399:
            days = int(seconds/86400)
            seconds = seconds % 86400
        if seconds > 3599:
            hours = int(seconds/3600)
            seconds = seconds % 3600
        if seconds > 59:
            minutes = int(seconds/60)
            seconds = seconds % 60

        return "{d}d {h}h {m}m {s}s".format(d=days, h=hours, m=minutes, s=seconds)

    def getcpuusage(self):
        return psutil.Process().cpu_percent() / psutil.cpu_count()

    def getmemusage(self):
        return psutil.Process().memory_info().rss / (1024 ** 2)

    @commands.command(pass_context=True, hidden=True)
    async def stats(self, ctx):
        author = ctx.message.author
        title = 'Stats for Rin'
        desc = 'Don\'t..t..t... look at my stats... Baka!'
        url = "https://github.com/xNinjaKittyx/ChitogeBot"
        trello = "https://trello.com/b/DUquXypS/rin"
        inviteurl = "https://discordapp.com/oauth2/authorize?client_id=189939510480470016&scope=bot&permissions=0"

        em = dmbd.newembed(author, title, desc, url)
        em.add_field(name='Users', value=len(ctx.message.server.members))
        em.add_field(name='Uptime', value=self.getuptime())
        em.add_field(name='CPU', value="{0:.2f}%".format(self.getcpuusage()))
        em.add_field(name='Memory', value="{0:.2f} MB".format(self.getmemusage()))
        em.add_field(name='Trello', value='[Trello Page]({})'.format(trello))
        em.add_field(name='Invite', value='[Click Me :)]({})'.format(inviteurl))

        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Info(bot))
