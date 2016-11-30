import requests
import xmltodict
import asyncio
import discord
import json
from discord.ext import commands


class MalLink:
    def __init__(self, info, num):
        self.id = info['id']
        self.title = info['title']
        self.english = info['english']
        self.synonyms = info['synonyms']
        if num == 1:
            self.episodes = info['episodes']
        elif num == 2:
            self.chapters = info['chapters']
            self.volumes = info['volumes']
        self.score = info['score']
        self.type = info['type']
        self.status = info['status']
        self.start_date = info['start_date']
        self.end_date = info['end_date']
        self.synopsis = info['synopsis']
        self.image = info['image']
        self.num = num

    def getlink(self):
        if self.num == 1:
            return str('<http://myanimelist.net/anime/' + str(self.id) + '>')
        elif self.num == 2:
            return str('<http://myanimelist.net/manga/' + str(self.id) + '>')

    def getinfo(self):
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
    """Searches up stuff on My Anime List
    """
    def __init__(self, bot):
        self.bot = bot
        with open('./json/setup.json') as data_file:
            setup = json.load(data_file)
        self.username = setup["MALUsername"]
        self.password = setup["MALPassword"]
        print(self.username)
        print(self.password)

    @commands.command(pass_context=True)
    async def anime(self, ctx, *, anime: str):
        """ Returns the top anime of whatever the user asked for."""
        anime.replace(' ', '_')
        url = 'http://myanimelist.net/api/anime/search.xml?q=' + anime
        r = requests.get(url, auth=(self.username, self.password))
        if r.status_code == 200:
            animelist = xmltodict.parse(r.content)
            try:
                result = animelist['anime']['entry'][0]
                final = MalLink(result, 1)
                await self.bot.say(final.getinfo())

            except KeyError:
                print("Probably only 1 anime listed. Trying something else")

                result = animelist['anime']['entry']
                final = MalLink(result, 1)
                await self.bot.say(final.getinfo())
            else:
                print("Something with wrong with MAL::Anime")

        elif r.status_code == 204:
            await self.bot.say("No Anime Found")
        else:
            print("Not connected.")

    @commands.command(pass_context=True)
    async def manga(self, ctx, *, manga: str):
        """ Returns the top manga of whatever the user asked for."""
        manga.replace(' ', '_')
        url = 'http://myanimelist.net/api/manga/search.xml?q=' + manga
        r = requests.get(url, auth=(self.username, self.password))
        if r.status_code == 200:
            mangalist = xmltodict.parse(r.content)
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

        elif r.status_code == 204:
            await self.bot.say("No Manga Found")
        else:
            print("Not connected.")


def setup(bot):
    bot.add_cog(Anime(bot))
