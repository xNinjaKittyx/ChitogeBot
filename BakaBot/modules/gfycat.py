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

    def gfylink(self, keyword, count):
        link = "https://api.gfycat.com/v1test/gfycats/search?search_text=" + str(keyword) + "&count=" + str(count)
        r = requests.get(link)
        if r.status_code != 200:
            print('Gyfcat returned ' + r.status_code)
            return
        giflist = json.loads(r.text)

        return giflist

    @commands.command(pass_context=True)
    async def owgif(self, ctx):
        giflist = self.gfylink("overwatch", 100)

        if not giflist:
            print('giflist not loaded correctly')
            return
        ayylmao = random.randint(0,99)
        author = ctx.message.author
        title = giflist["gfycats"][ayylmao]["gfyName"]
        desc = giflist["gfycats"][ayylmao]["title"]
        if giflist["gfycats"][ayylmao]["tags"] != None:
            desc += " #" + " #".join([x for x in giflist["gfycats"][ayylmao]["tags"]])
        url = "https://gfycat.com/" + title

        em = dmbd.newembed(author, title, desc, url)
        await self.bot.say(embed=em)
        await self.bot.say(url)

def setup(bot):
    bot.add_cog(Gfycat(bot))
