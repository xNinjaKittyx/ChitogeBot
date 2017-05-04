

import asyncio
from datetime import datetime
import json
import random
import os

import discord
from discord.ext import commands
import requests
import tools.discordembed as dmbd


class Animehangman:
    def getaccesstoken(self):
        req = requests.post(
            'https://anilist.co/api/auth/access_token', data={
                'grant_type': 'client_credentials',
                'client_id': self.anilistid,
                'client_secret': self.anilistsecret
        })
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
        self.max = 90248

    async def display(self, currentboard, guess, misses, author, picture, win=0):
        subtitle = "Where you test your weeb level!"
        em = dmbd.newembed(author, "Anime Hangman!", subtitle)
        em.set_image(url=picture)

        em.add_field(name="Word", value="`" + currentboard + "`")
        if misses != []:
            em.add_field(name="Guess", value=guess, inline=False)
            em.add_field(name="Misses", value=' '.join(misses))
        if not (len(misses) == 6 or win == 1):
            em.add_field(
                name="How to Play",
                value="Use " + self.bot.command_prefix + "guess [x] to guess the next letter",
                inline=False
            )

        if len(misses) == 0:
            em.set_thumbnail(url="https://goo.gl/FMUQrp")
        elif len(misses) == 1:
            em.set_thumbnail(url="https://goo.gl/fKvyTp")
        elif len(misses) == 2:
            em.set_thumbnail(url="https://goo.gl/dTVKVX")
        elif len(misses) == 3:
            em.set_thumbnail(url="https://goo.gl/BqiCFi")
        elif len(misses) == 4:
            em.set_thumbnail(url="https://goo.gl/XgytvK")
        elif len(misses) == 5:
            em.set_thumbnail(url="https://goo.gl/AevCAI")
        elif len(misses) == 6:
            em.set_thumbnail(url="https://goo.gl/8ymxqs")
            em.add_field(name="You Lose!", value="lul", inline=False)

        if win == 1:
            em.add_field(name="You Win!", value="You weeb...", inline=False)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def animecharhangman(self, ctx):
        """ Play Hangman!"""
        delta = (datetime.today() - self.lastaccess)
        if delta.seconds > 3600 or delta.days > 0:
            self.access_token, self.lastaccess = self.getaccesstoken()
        char = None
        while char is None:
            req = requests.get(
                "https://anilist.co/api/character/" +
                str(random.randint(1, self.max)) +
                "/page?access_token=" +
                self.access_token
            )
            if req.status_code != 200:
                print("ANIME CHARACTER RETURNING 404")
                continue
            character = json.loads(req.text)
            print(character["id"])
            if character["anime"] == []:
                continue
            char = character
        if char["name_last"] == None:
            answer = char["name_first"]
            currentboard = "_"*len(char["name_first"])
        else:
            answer = char["name_first"] + " " + char["name_last"]
            currentboard = "_"*len(char["name_first"]) + " " + "_"*len(char["name_last"])
        misses = []
        guess = "FirstDisplay"
        picture = char["image_url_lge"]
        author = ctx.message.author
        while currentboard != answer or len(misses) == 6:
            await self.display(currentboard, guess, misses, author, picture)

            def check(msg):
                return msg.content.startswith(self.bot.command_prefix + 'guess')

            msg = await self.bot.wait_for_message(
                channel=ctx.message.channel,
                check=check
                )
            author = msg.author
            guess = msg.content[6:].strip()
            if len(guess) > 1:
                await self.bot.say("Please 1 letter at a time.")
                continue
            if guess in misses:
                await self.bot.say("You've already used that letter!")
                continue
            if guess in answer:
                for x in range(len(answer)):
                    if answer[x].lower() == guess or answer[x].upper() == guess:
                        currentboard = currentboard[:x] + answer[x] + currentboard[x+1:]
            else:
                misses.append(guess)

        if currentboard == answer:
            await self.display(currentboard, guess, misses, author, picture, 1)
        else:
            await self.display(currentboard, guess, misses, author, picture, 0)


def setup(bot):
    bot.add_cog(Animehangman(bot))
