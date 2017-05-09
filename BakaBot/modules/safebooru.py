
import asyncio
import xmltodict
import random
import requests

import discord
from discord.ext import commands
import tools.discordembed as dmbd

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

        author = ctx.message.author
        title = 'Safebooru'
        desc = 'Searched For ' + search
        em = dmbd.newembed(author, title, desc)

        if numOfResults == 0:
            em.description = "No Results Found For " + search
        elif numOfResults == 1:
            em.set_image(url='https:' + str(weeblist['posts']['post']['@file_url']))
        else:
            if numOfPages == 0:
                chosenone = random.randint(0, min(99, numOfResults-1))
                em.set_image(url='https:' + str(weeblist['posts']['post'][chosenone]['@file_url']))
            else:
                page = random.randint(0, numOfPages)
                # Avoiding oversearching, and cutting the page limit to 3.
                # Sometimes really unrelated stuff gets put in.
                weeblist = self.getlink(link + '&pid=' + str(min(3, page)))
                if page == numOfPages:
                    chosenone = random.randint(0, min(99, remaining))
                    em.set_image(url='https:' + str(weeblist['posts']['post'][chosenone]['@file_url']))
                else:
                    chosenone = random.randint(0, 99)
                    em.set_image(url='https:' + str(weeblist['posts']['post'][chosenone]['@file_url']))

            self.bot.cogs['WordDB'].cmdcount('safebooru')
        await self.bot.say(embed=em)



def setup(bot):
    bot.add_cog(Safebooru(bot))
