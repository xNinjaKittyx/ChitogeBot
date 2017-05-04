""" To Get an Anime or Manga from MyAnimeList"""

import asyncio
import json
import re
from time import strftime
import html.parser as htmlparser

import requests
import xmltodict

import discord
from discord.ext import commands
import tools.discordembed as dmbd

def cleanhtml(raw_html):
    """ Kudos to http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class Anime:
    """Searches up stuff on My Anime List"""

    def __init__(self, bot):
        self.bot = bot
        with open('./json/setup.json') as data_file:
            settings = json.load(data_file)
        self.username = settings["MALUsername"]
        self.password = settings["MALPassword"]

    def getlink(self, iden, num):
        """Getter Function for Anime or Manga Link from MAL"""

        if num == 1:
            return str("http://myanimelist.net/anime/" + str(iden))
        elif num == 2:
            return str("http://myanimelist.net/manga/" + str(iden))

    def getinfo(self, author, mal, num):
        """ Get the Info Message of the MalLink Class. Returns with Embed"""
        parser = htmlparser.HTMLParser()

        em = dmbd.newembed(author, mal['title'], mal['english'], self.getlink(mal['id'], num))
        em.set_thumbnail(url="http://img05.deviantart.net/1d5b/i/2014/101/c/c/myanimelist___logo_by_theresonly1cryo-d7dzp0l.png")
        em.set_image(url=mal['image'])
        if num == 1: # if anime
            self.bot.cogs['WordDB'].cmdcount('anime')
            em.add_field(name="Episodes", value=mal['episodes'])

        elif num == 2: # if manga
            self.bot.cogs['WordDB'].cmdcount('manga')
            em.add_field(name="Chapters", value=mal['chapters'])
            em.add_field(name="Volumes", value=mal['volumes'])

        em.add_field(name="Status", value=mal['status'])
        em.add_field(name="Score", value=mal['score'])
        em.add_field(name="Type", value=mal['type'])
        em.add_field(name="Synopsis", value=cleanhtml(parser.unescape(mal['synopsis']))[:500] + "...")
        return em

    @commands.command(pass_context=True)
    async def anime(self, ctx, *, anime: str):
        """ Returns the top anime of whatever the user asked for."""

        url = 'https://' + self.username + ":" + self.password + \
              '@myanimelist.net/api/anime/search.xml?q=' + anime.replace(' ', '_')
        req = requests.get(url)
        if req.status_code == 200:
            animelist = xmltodict.parse(req.content)
            try:
                mal = animelist['anime']['entry'][0]
                entry = 1
                for x in animelist['anime']['entry']:
                    if x['title'] == anime:
                        await self.bot.say(embed=self.getinfo(ctx.message.author, x, 1))
                        return
                while mal['type'] != 'TV' and mal['type'] != 'Movie':
                    mal = animelist['anime']['entry'][entry]
                    entry += 1
                await self.bot.say(embed=self.getinfo(ctx.message.author, mal, 1))

            except KeyError:
                print("Probably only 1 anime listed. Trying something else")

                mal = animelist['anime']['entry']
                await self.bot.say(embed=self.getinfo(ctx.message.author, mal, 1))

        elif req.status_code == 204:
            await self.bot.say("No Anime Found")
        else:
            print("Not connected.")


    @commands.command(pass_context=True)
    async def manga(self, ctx, *, manga: str):
        """ Returns the top manga of whatever the user asked for."""

        manga.replace(' ', '_')
        url = 'https://' + self.username + ":" + self.password + \
               '@myanimelist.net/api/manga/search.xml?q=' + manga
        req = requests.get(url, auth=(self.username, self.password))
        if req.status_code == 200:
            mangalist = xmltodict.parse(req.content)
            try:
                mal = mangalist['manga']['entry'][0]
                for x in mangalist['manga']['entry']:
                    if x['title'] == manga:
                        await self.bot.say(embed=self.getinfo(ctx.message.author, x, 2))
                        return
                await self.bot.say(embed=self.getinfo(ctx.message.author, mal, 2))

            except KeyError:
                print("Probably only 1 manga listed. Trying something else")

                mal = mangalist['manga']['entry']
                await self.bot.say(embed=self.getinfo(ctx.message.author, mal, 2))

        elif req.status_code == 204:
            await self.bot.say("No Manga Found")
        else:
            print("Not connected.")



def setup(bot):
    """Setup Anime.py"""
    bot.add_cog(Anime(bot))
