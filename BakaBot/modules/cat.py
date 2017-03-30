""" Module for generating a random cat picture"""

import asyncio
import json
from time import strftime

from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import requests


class Cat:
    """ Cat Module"""

    def __init__(self, bot):
        """ Initialize Cat Class"""

        self.bot = bot

    @commands.command(pass_context=True)
    async def meow(self, ctx):
        """ When User Types ~meow, return a cat link """
        req = requests.get('http://random.cat/meow')
        if req.status_code != 200:
            print("Could not get a meow")
        catlink = json.loads(req.text)
        rngcat = catlink["file"]
        author = ctx.message.author
        em = discord.Embed(title='Random.Cat', description='Here have a cat.', url=rngcat, colour=0xC154F5)
        em.set_author(name=author.name + '#' + author.discriminator, icon_url=author.avatar_url)
        em.set_footer(text="Powered by discord.py | " + strftime('%a %b %d, %Y at %I:%M %p'), icon_url="https://my.mixtape.moe/jhbhte.png")
        em.set_image(url=rngcat)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def woof(self, ctx):
        """When user types ~woof, return a woof link """

        req = requests.get('http://random.dog/')
        if req.status_code != 200:
            print("Could not get a woof")
        doglink = BeautifulSoup(req.text, 'html.parser')
        rngdog = 'http://random.dog/' + doglink.img['src']
        author = ctx.message.author
        em = discord.Embed(title='Random.Dog', description='Here have a dog.', url=rngdog, colour=0xC154F5)
        em.set_author(name=author.name + '#' + author.discriminator, icon_url=author.avatar_url)
        em.set_footer(text="Powered by discord.py | " + strftime('%a %b %d, %Y at %I:%M %p'), icon_url="https://my.mixtape.moe/jhbhte.png")
        em.set_image(url=rngdog)
        await self.bot.say(embed=em)


def setup(bot):
    """ Setup Cat Module"""
    bot.add_cog(Cat(bot))
