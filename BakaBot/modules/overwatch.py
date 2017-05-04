""" Overwatch API usage"""

import asyncio
import json
import random

import discord
from discord.ext import commands
import requests


class Overwatch:
    def __init__(self, bot):
        self.bot = bot

        self.heroes = ['Genji', 'McCree', 'Pharrah', 'Reaper', 'Soldier 76',
                       'Tracer', 'Bastion', 'Hanzo', 'Junkrat', 'Mei',
                       'Torbjorn', 'Widowmaker', 'D.va', 'Reinhardt', 'Roadhog',
                       'Winston','Zarya', 'Lucio', 'Mercy',
                       'Symmetra', 'Zenyatta', 'Sombra']

    @commands.command()
    async def owstats(self, *, tag: str):
        """ This only works in US Server Currently"""
        if '#' in tag:
            tag = tag.replace('#', '-')

        req = requests.get('https://api.lootbox.eu/pc/us/' + tag + '/profile')
        if req.status_code != 200:
            print('Lootbox is down.')
            return
        profile = json.loads(req.text)
        profile = profile['data']
        quick = profile['games']['quick']
        comp = profile['games']['competitive']
        result = ('```\nUsername: ' + profile['username'] +
                  '\nLevel: ' + str(profile['level']) +
                  '\nQuickPlay Wins: ' + str(quick['wins']) +
                  '\nQuickPlay Playtime: ' + str(profile['playtime']['quick']))

        if profile['competitive']['rank'] != None:
            result += ('\nCompetitive Rank: ' + str(profile['competitive']['rank']) +
                       '\nCompetitive Score: ' + str(comp['wins']) + " - " + str(comp['lost']) +
                       '\nCompetitive Win Ratio: ' + str(float(comp['wins']) / (float(comp['wins']) + float(comp['lost']))) +
                       '\nCompetitive PlayTime: ' + str(profile['playtime']['competitive']))

        result += '```'

        await self.bot.say(result)
        self.bot.cogs['WordDB'].cmdcount('owstats')

    @commands.command()
    async def owrng(self):
        """ RNG OVERWATCH """
        await self.bot.say("Play {}!".format(random.choice(self.heroes)))
        self.bot.cogs['WordDB'].cmdcount('owrng')

    @commands.command()
    async def owteam(self, num: int = 6):
        """ Get a random OW Team """
        result = random.shuffle(self.heroes)[:num]
        await self.bot.say("Here's your teamcomp! Good luck!\n" +
                           "{}".format(" ".join(result)))
        self.bot.cogs['WordDB'].cmdcount('manga')



def setup(bot):
    """ Setup OW Module"""
    bot.add_cog(Overwatch(bot))
