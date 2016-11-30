import requests
import json
import asyncio
import discord
from discord.ext import commands


class Cat:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meow(self):
        r = requests.get('http://random.cat/meow')
        if r.status_code is not 200:
            print("Could not get a meow")
        catlink = json.loads(r.text)

        await self.bot.say(catlink["file"])


def setup(bot):
    bot.add_cog(Cat(bot))
