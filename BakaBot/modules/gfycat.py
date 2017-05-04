import requests
import asyncio
import discord
import json
import random
from discord.ext import commands
import tools.discordembed as dmbd

class Gfycat:

    def __init__(self, bot):
        self.bot = bot

    def gfylink(self, keyword, count, author):
        link = "https://api.gfycat.com/v1test/gfycats/search?search_text=" + str(keyword) + "&count=" + str(count)
        r = requests.get(link)
        if r.status_code != 200:
            print('Gyfcat returned ' + r.status_code)
            return
        giflist = json.loads(r.text)
        if not giflist:
            print('giflist not loaded correctly')
            return

        num = random.randint(0, count-1)
        gif = giflist["gfycats"][num]
        title = gif["gfyName"]
        desc = gif["title"]
        if gif["tags"] != None:
            desc += " #" + " #".join([x for x in gif["tags"]])

        url = "https://gfycat.com/" + title
        return dmbd.newembed(author, title, desc, url)

    @commands.command(pass_context=True)
    async def owgif(self, ctx):
        """Random Overwatch Gyfcat"""
        em = self.gfylink("overwatch", 100, ctx.message.author)
        await self.bot.say(embed=em)
        await self.bot.say(em.url)
        self.bot.cogs['WordDB'].cmdcount('owgif')

    @commands.command(pass_context=True)
    async def gfy(self, ctx, *, keyword: str):
        """Does a search on gyfcat"""
        em = self.gfylink(keyword, 50, ctx.message.author)
        await self.bot.say(embed=em)
        await self.bot.say(em.url)
        self.bot.cogs['WordDB'].cmdcount('gfy')


def setup(bot):
    bot.add_cog(Gfycat(bot))
