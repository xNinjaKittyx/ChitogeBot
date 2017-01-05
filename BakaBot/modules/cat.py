""" Module for generating a random cat picture"""

import asyncio
import json

from bs4 import BeautifulSoup
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
        if req.status_code != 200:
            print("Could not get a meow")
        catlink = json.loads(req.text)

        await self.bot.say(catlink["file"])

    @commands.command()
    async def woof(self):
        """When user types ~woof, return a woof link """

        req = requests.get('http://random.dog/')
        if req.status_code != 200:
            print("Could not get a woof")
        doglink = BeautifulSoup(req.text, 'html.parser')

        await self.bot.say('http://random.dog/' + doglink.img['src'])


def setup(bot):
    """ Setup Cat Module"""
    bot.add_cog(Cat(bot))
