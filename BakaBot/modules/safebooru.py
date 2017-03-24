import requests
import xmltodict
import asyncio
import discord
import random
from discord.ext import commands


class Safebooru:

    def __init__(self, bot):
        self.bot = bot

    def getlink(self, link):
        r = requests.get(link)
        if r.status_code != 200:
            print('Safebooru returned ' + r.status_code)
            return
        weeblist = xmltodict.parse(r.text)
        return weeblist

    @commands.command(pass_context=True, no_pm=True)
    async def safebooru(self, ctx, *, search: str):
        """Searches Safebooru"""
        link = ("http://safebooru.org/index.php?page=dapi&s=post&q=index" +
                "&tags=" + search.replace(' ', '_'))
        weeblist = self.getlink(link)
        numOfResults = int(weeblist['posts']['@count'])

        # Find how many pages there are

        numOfPages = int(numOfResults / 100)
        remaining = numOfResults % 100

        if numOfResults == 0:
            await self.bot.say("No Results Found")
        elif numOfResults == 1:
            await self.bot.say(weeblist['posts']['post']['@file_url'])
        else:
            if numOfPages == 0:
                chosenone = random.randint(0, min(99, numOfResults-1))
                await self.bot.say(weeblist['posts']['post'][chosenone]['@file_url'])
            else:
                page = random.randint(0, numOfPages)
                # Avoiding oversearching, and cutting the page limit to 3.
                # Sometimes really unrelated stuff gets put in.
                weeblist = self.getlink(link + '&pid=' + str(min(3,page)))
                if page == numOfPages:
                    chosenone = random.randint(0, min(99, remaining))
                    await self.bot.say('https:' + str(weeblist['posts']['post'][chosenone]['@file_url']))
                else:
                    chosenone = random.randint(0, 99)
                    await self.bot.say('https:' + str(weeblist['posts']['post'][chosenone]['@file_url']))




def setup(bot):
    bot.add_cog(Safebooru(bot))
