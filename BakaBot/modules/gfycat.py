import requests
import asyncio
import discord
import json
import random
from discord.ext import commands

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

    @commands.command()
    async def owgif(self):
        giflist = self.gfylink("overwatch", 200)
        ayylmao = random.randint(0,199)
        gif = giflist["gfycats"][ayylmao]["gfyName"]
        link = "https://gfycat.com/" + gif
        await self.bot.say(link)

def setup(bot):
    bot.add_cog(Gfycat(bot))
