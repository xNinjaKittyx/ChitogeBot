""" To Get an Anime or Manga from MyAnimeList"""

import asyncio
import json

import requests
import xmltodict

import discord
from discord.ext import commands


class MalLink:
    """ Any Instance of a MAL API XML document"""
   # pylint: disable=too-many-instance-attributes,c0103
    def __init__(self, info, num):
        self.id = info['id']
        self.title = info['title']
        self.english = info['english']
        # self.synonyms = info['synonyms']
        if num == 1:
            self.episodes = info['episodes']
        elif num == 2:
            self.chapters = info['chapters']
            self.volumes = info['volumes']
        self.score = info['score']
        self.type = info['type']
        self.status = info['status']
        # self.start_date = info['start_date']
        # self.end_date = info['end_date']
        self.synopsis = info['synopsis']
        self.image = info['image']
        self.num = num

    def getlink(self):
        """Getter Function for Anime or Manga Link from MAL"""

        if self.num == 1:
            return str('<http://myanimelist.net/anime/' + str(self.id) + '>')
        elif self.num == 2:
            return str('<http://myanimelist.net/manga/' + str(self.id) + '>')

    def getinfo(self):
        """ Get the Info Message of the MalLink Class"""
        if self.num == 1:
            result = ('`Title:` **{0}**\n'
                      '`English Title:` {1}\n'
                      '`Episodes:` {2}\n'
                      '`Status:` {3}\n'
                      '`Score:` {4}\n'
                      '`Type:` {5}\n'
                      '`Link:` {6}\n'
                      '`Synopsis:` {7}...\n'
                      '`Img:` {8}\n').format(self.title, self.english,
                                             self.episodes, self.status,
                                             self.score, self.type,
                                             self.getlink(),
                                             self.synopsis[:500], self.image)

        elif self.num == 2:
            result = ('`Title:` **{0}**\n'
                      '`English Title:` {1}\n'
                      '`Chapters:` {2}\n'
                      '`Volumes:` {3}\n'
                      '`Status:` {4}\n'
                      '`Score:` {5}\n'
                      '`Type:` {6}\n'
                      '`Link:` {7}\n'
                      '`Synopsis:` {8}...\n'
                      '`Img:` {9}\n').format(self.title, self.english,
                                             self.chapters, self.volumes,
                                             self.status, self.score,
                                             self.type, self.getlink(),
                                             self.synopsis[:500], self.image)
        return result


class Anime:
    """Searches up stuff on My Anime List"""

    def __init__(self, bot):
        self.bot = bot
        with open('./json/setup.json') as data_file:
            settings = json.load(data_file)
        self.username = settings["MALUsername"]
        self.password = settings["MALPassword"]

    @commands.command()
    async def anime(self, *, anime: str):
        """ Returns the top anime of whatever the user asked for."""

        url = 'https://' + self.username + ":" + self.password + \
              '@myanimelist.net/api/anime/search.xml?q=' + anime.replace(' ', '_')
        req = requests.get(url, auth=(self.username, self.password))
        if req.status_code == 200:
            animelist = xmltodict.parse(req.content)
            try:
                result = animelist['anime']['entry'][0]
                final = MalLink(result, 1)
                entry = 1
                while final.type is not 'TV' or final.type is not 'Movie':
                    result = animelist['anime']['entry'][entry]
                    final = MalLink(result, 1)
                    entry += 1
                await self.bot.say(final.getinfo())

            except KeyError:
                print("Probably only 1 anime listed. Trying something else")

                result = animelist['anime']['entry']
                final = MalLink(result, 1)
                await self.bot.say(final.getinfo())
            else:
                print("Something with wrong with MAL::Anime")

        elif req.status_code == 204:
            await self.bot.say("No Anime Found")
        else:
            print("Not connected.")

    @commands.command()
    async def manga(self, *, manga: str):
        """ Returns the top manga of whatever the user asked for."""

        manga.replace(' ', '_')
        url = 'https://' + self.username + ":" + self.password + \
               '@myanimelist.net/api/manga/search.xml?q=' + manga
        req = requests.get(url, auth=(self.username, self.password))
        if req.status_code == 200:
            mangalist = xmltodict.parse(req.content)
            try:
                result = mangalist['manga']['entry'][0]
                final = MalLink(result, 2)
                await self.bot.say(final.getinfo())

            except KeyError:
                print("Probably only 1 manga listed. Trying something else")

                result = mangalist['manga']['entry']
                final = MalLink(result, 2)
                await self.bot.say(final.getinfo())
            else:
                print("Something with wrong with MAL::Manga")

        elif req.status_code == 204:
            await self.bot.say("No Manga Found")
        else:
            print("Not connected.")


def setup(bot):
    """Setup Anime.py"""
    bot.add_cog(Anime(bot))
