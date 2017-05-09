# -*- coding: utf8 -*-
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
        self.active = 0
        self.currentboard = ""

    async def display(self, guess, misses, author, picture, win=0):
        subtitle = "Where you test your weeb level!"
        em = dmbd.newembed(author, "Anime Hangman!", subtitle)
        em.set_image(url=picture)

        em.add_field(name="Word", value="`" + self.currentboard.title() + "`", inline=False)
        if misses != []:
            em.add_field(name="Guess", value=guess)
            em.add_field(name="Misses", value=' '.join(misses))
        if not (len(misses) == 6 or win == 1):
            em.add_field(
                name="How to Play",
                value=(
                "Use " + self.bot.command_prefix +
                "guess [x] to guess the next letter\n"
                "Type $guess quit to exit\n"
                ),
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
            self.active = 0

        if win == 1:
            em.add_field(name="You Win!", value="You weeb...", inline=False)
        return await self.bot.say(embed=em)

    async def displayanswer(self, author, char):
        try:
            anime = char['anime'][0]
        except:
            anime = char['anime']
        subtitle = anime['title_japanese']
        url = "https://anilist.co/anime/" + str(anime['id'])
        em = dmbd.newembed(author, 'Here\'s the answer!', subtitle, url)
        em.set_image(url=anime['image_url_lge'])
        em.add_field(name=anime['title_romaji'], value=anime['title_english'])
        em.add_field(name="Type", value=anime['type'])
        em.add_field(name='Rating', value=anime['average_score'])
        xstr = lambda s: s or ""
        em.add_field(name=char['name_japanese'], value=char['name_first'] + " " + xstr(char['name_last']))

        await self.bot.say(embed=em)


    @commands.command(pass_context=True, no_pm=True)
    async def animecharhangman(self, ctx):
        """ Play Hangman!"""
        if self.active == 1:
            await self.bot.say("There's already a game running!")
            return
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
            if character["anime"] == [] or character['image_url_lge'] == "https://cdn.anilist.co/img/dir/character/reg/default.jpg":
                continue
            char = character

        answer = char["name_first"].lower()
        self.currentboard = "_"*len(char["name_first"])
        if char["name_last"]:
            answer += " " + char["name_last"].lower()
            self.currentboard += " " + "_"*len(char["name_last"])
        misses = []
        guess = "FirstDisplay"
        picture = char["image_url_lge"]
        author = ctx.message.author
        prev_message = await self.display(guess, misses, author, picture)
        self.active = 1
        while self.currentboard != answer or self.active == 1:

            def check(msg):
                return msg.content.startswith(self.bot.command_prefix + 'guess')

            msg = await self.bot.wait_for_message(
                channel=ctx.message.channel,
                check=check
                )
            await self.bot.delete_message(prev_message)
            author = msg.author
            guess = msg.content[6:].strip().lower()

            if len(guess) > 1:
                await self.bot.say("You need to give me a letter!")
            elif guess == 'quit':
                self.active = 0
                await self.bot.say("You Ragequit? What a loser.")
                for x in range(6 - len(misses)):
                    misses.append('.')
                await self.display(guess, misses, author, picture, 0)
                await self.displayanswer(author, char)
                return
            elif len(guess) > 1:
                if len(answer) < len(guess):
                    # TODO: keeps saying guess is too long when it's not.
                    await self.bot.say("Your guess is too long. Try Again.")
                    guess = ";^)"
                elif guess == answer:
                    self.currentboard = answer
                else:
                    misses.append(guess)
            elif guess in misses:
                await self.bot.say("You've already used that letter!")
            elif guess in answer:
                for x in range(len(answer)):
                    if answer[x] == guess:
                        self.currentboard = self.currentboard[:x] + answer[x] + self.currentboard[x+1:]
            else:
                misses.append(guess)


            if self.currentboard == answer:
                await self.display(guess, misses, author, picture, 1)
                await self.displayanswer(author, char)
                self.active = 0
                return
            elif len(misses) >= 6:
                await self.display(guess, misses, author, picture, 0)
                await self.displayanswer(author, char)
                self.active = 0
                return
            else:
                prev_message = await self.display(guess, misses, author, picture, 0)

        self.active = 0

def setup(bot):
    bot.add_cog(Animehangman(bot))
