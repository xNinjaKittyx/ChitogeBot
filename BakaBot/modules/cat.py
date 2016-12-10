""" Module for generating a random cat picture"""

import asyncio
import json

import discord
from discord.ext import commands
import requests


class Cat:
    """ Cat Module"""

    def __init__(self, bot):
        """ Initialize Cat Class"""

        self.bot = bot

    @commands.command()
    async def meow(self):
        """ When User Types ~meow, return a cat link """

        req = requests.get('http://random.cat/meow')
        if req.status_code is not 200:
            print("Could not get a meow")
        catlink = json.loads(req.text)

        await self.bot.say(catlink["file"])


def setup(bot):
    """ Setup Cat Module"""
    bot.add_cog(Cat(bot))
