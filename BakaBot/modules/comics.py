
import asyncio
import json
import random
import re

from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import requests

class Comic:
    def __init__(self, status, current):
        self.status = status
        self.current = current

class Comics:
    def __init__(self, bot):
        self.bot = bot
        req = requests.get("http://xkcd.com/info.0.json")
        if req.status_code != 200:
            print("XKCD is currently down")
            self.eckskay = Comic(0, 0)
        else:
            info = json.loads(req.text)
            self.eckskay = Comic(1, info["num"])
        req = requests.get('http://explosm.net/comics/latest')
        if req.status_code != 200:
            print("explosm.net is down")
            self.cyanide = Comic(0, 0)
        else:
            soup = BeautifulSoup(req.text, 'html.parser')
            current = int(re.findall(r'\d+', soup.find(id="permalink", type="text").get("value"))[0])
            self.cyanide = Comic(1, current)


    @commands.command()
    async def xkcd(self):
        """Gives a random XKCD Comic"""
        if self.eckskay.status == 0:
            req = requests.get("http://xkcd.com/info.0.json")
            if req.status_code == 200:
                self.eckskay.status = 1
            else:
                await self.bot.say("XKCD is down for some reason...")
                return
        number = random.randint(1, self.eckskay.current)
        link = "http://xkcd.com/" + str(number)
        req = requests.get(link + "/info.0.json")
        if req.status_code != 200:
            await self.bot.say("XKCD is currently down")
            return

        info = json.loads(req.text)
        await self.bot.say(link)
        self.bot.cogs['WordDB'].cmdcount('xkcd')

    @commands.command()
    async def ch(self):
        """ Gives a random Cyanide & Happiness Comic"""
        if self.cyanide.status == 0:
            req = requests.get('http://explosm.net/comics/latest')
            if req.status_code == 200:
                self.cyanide.status = 1
            else:
                await self.bot.say("C&H is down for some reason...")
                return
        number = random.randint(1, self.cyanide.current)
        link = 'http://explosm.net/comics/' + str(number)
        await self.bot.say(link)
        self.bot.cogs['WordDB'].cmdcount('ch')

    @commands.command()
    async def chrng(self):
        """ Gives a randomly generated Cyanide & Happiness Comic"""
        req = requests.get('http://explosm.net/rcg')
        if self.cyanide.status == 0:
            if req.status_code == 200:
                self.cyanide.status = 1
            else:
                await self.bot.say("C&H is down for some reason...")
                return
        soup = BeautifulSoup(req.text, 'html.parser')
        await self.bot.say(soup.find(id="permalink", type="text").get("value"))
        self.bot.cogs['WordDB'].cmdcount('chrng')


def setup(bot):
    bot.add_cog(Comics(bot))
