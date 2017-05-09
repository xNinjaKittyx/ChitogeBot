""" To Get an Anime or Manga from MyAnimeList"""

# -*- coding: utf8 -*-
import asyncio
from datetime import datetime
import json
import re
from time import strftime
import html.parser as htmlparser

import requests

from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import tools.discordembed as dmbd


class Anime:
    """Searches up stuff on My Anime List"""
    def getaccesstoken(self):
        req = requests.post(
            'https://anilist.co/api/auth/access_token', data={
                'grant_type': 'client_credentials',
                'client_id': self.anilistid,
                'client_secret': self.anilistsecret
            }
        )
        if req.status_code != 200:
            print("Cannot get Anilist Access Token")
            return
        results = json.loads(req.text)
        return results['access_token'], datetime.today()

    def __init__(self, bot):
        self.bot = bot
        with open('./json/setup.json') as data_file:
            settings = json.load(data_file)
        self.anilistid = settings["AnilistID"]
        self.anilistsecret = settings["AnilistSecret"]
        self.access_token, self.lastaccess = self.getaccesstoken()

    def getinfo(self, author, series):
        """ Get the Info Message of the MalLink Class. Returns with Embed"""
        parser = htmlparser.HTMLParser()

        em = dmbd.newembed(
            author,
            series['title_japanese'],
            series['title_romaji'],
            self.getlink(series['id'], series['series_type'])
        )
        em.set_thumbnail(url="https://anilist.co/img/logo_al.png")
        em.set_image(url=series['image_url_med'])
        if series['series_type'] == 'anime': # if anime
            self.bot.cogs['WordDB'].cmdcount('anime')
            em.add_field(name="Episodes", value=series['total_episodes'])
            try:
                em.add_field(name="Length", value=series['duration'] + " minutes")
            except KeyError:
                pass
            try:
                em.add_field(name="Status", value=series['airing_status'])
            except KeyError:
                pass

        elif series['series_type'] == 'manga': # if manga
            self.bot.cogs['WordDB'].cmdcount('manga')
            em.add_field(name="Chapters", value=series['total_chapters'])
            em.add_field(name="Volumes", value=series['total_volumes'])
            try:
                em.add_field(name="Status", value=series['publishing_status'])
            except KeyError:
                pass

        em.add_field(name="Score", value=series['average_score'])
        em.add_field(name="Type", value=series['type'])
        if series['description'] != None:
            cleantext = BeautifulSoup(series['description'], "html.parser").text[:500] + "..."
            em.add_field(name="Synopsis", value=cleantext)
        return em

    def getlink(self, series_id, series_type):
        """Getter Function for Anime or Manga Link from MAL"""

        if series_type == 'anime':
            return str("https://anilist.co/anime/" + str(series_id))
        elif series_type == 'manga':
            return str("https://anilist.co/manga/" + str(series_id))

    def refreshtoken(self):
        delta = (datetime.today() - self.lastaccess)
        if delta.seconds > 3600 or delta.days > 0:
            self.access_token, self.lastaccess = self.getaccesstoken()

    @commands.command(pass_context=True)
    async def anime(self, ctx, *, ani: str):
        """ Returns the top anime of whatever the user asked for."""
        self.refreshtoken()

        url = (
            'https://anilist.co/api/anime/search/' +
            ani + "?access_token=" + self.access_token
        )

        req = requests.get(url)
        if req.status_code == 200:
            animelist = json.loads(req.text)

            try:
                await self.bot.say(animelist["error"]["message"][0])
            except:
                pass

            chosen = {}
            for x in animelist:
                if x['title_romaji'].lower() == ani.lower():
                    chosen = x
                    break
                elif x['title_english'].lower() == ani.lower():
                    chosen = x
                    break
            if chosen == {}:
                for x in animelist:
                    if x['type'] == "TV":
                        chosen = x
                        break
                if chosen == {}:
                    for x in animelist:
                        if x['type'] == "Movie":
                            chosen = x
                            break
            if chosen == {}:
                chosen = animelist[0]
            await self.bot.say(embed=self.getinfo(ctx.message.author, chosen))

        elif req.status_code == 204:
            await self.bot.say("No Anime Found")
        else:
            print("Not connected.")


    @commands.command(pass_context=True)
    async def manga(self, ctx, *, mang: str):
        """ Returns the top manga of whatever the user asked for."""

        self.refreshtoken()
        url = (
            'https://anilist.co/api/manga/search/' +
            mang + "?access_token=" + self.access_token
        )
        req = requests.get(url)
        if req.status_code == 200:
            mangalist = json.loads(req.text)
            try:
                await self.bot.say(mangalist["error"]["message"][0])
            except:
                pass
            chosen = {}
            for x in mangalist:
                if x['title_romaji'].lower() == mang.lower():
                    chosen = x
                    break
                elif x['title_english'].lower() == mang.lower():
                    chosen = x
                    break
            if chosen == {}:
                for x in mangalist:
                    if x['type'] == "Manga" or x['type'] == "Novel":
                        chosen = x
                        break
                if chosen == {}:
                    for x in mangalist:
                        if x['type'] == "Manhua" or x['type'] == "Manhwa":
                            chosen = x
                            break
            if chosen == {}:
                chosen = mangalist[0]
            await self.bot.say(embed=self.getinfo(ctx.message.author, chosen))
        else:
            print("Not connected.")



def setup(bot):
    """Setup Anime.py"""
    bot.add_cog(Anime(bot))
