import asyncio
import json
import random

import discord
from discord.ext import commands
import requests

class Xkcd:
    def __init__(self, bot):
        self.bot = bot
        req = requests.get("http://xkcd.com/info.0.json")
        if req.status_code != 200:
            print("XKCD is currently down")
            self.status = 0
            return
        self.status = 1
        info = json.loads(req.text)
        self.current = info["num"]

    @commands.command()
    async def xkcd(self):
        """Gives a random XKCD Comic"""
        if self.status == 0:
            req = requests.get("http://xkcd.com/info.0.json")
            if req.status_code == 200:
                self.status = 1
            else:
                return
        number = random.randint(1, self.current)
        link = "http://xkcd.com/" + str(number)
        req = requests.get(link + "/info.0.json")
        if req.status_code != 200:
            await self.bot.say("XKCD is currently down")
            return

        info = json.loads(req.text)
        await self.bot.say(link + "\n" + info["img"])

def setup(bot):
    bot.add_cog(Xkcd(bot))
