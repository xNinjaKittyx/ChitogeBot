import requests
import json
import asyncio
import discord
from discord.ext import commands


class OsuPlayer:

    def __init__(self, player):
        self.user_id = player["user_id"]
        self.username = player["username"]
        self.count300 = player["count300"]
        self.count100 = player["count100"]
        self.count50 = player["count50"]
        self.playcount = player["playcount"]
        self.ranked_score = player["ranked_score"]
        self.total_score = player["total_score"]
        self.pp_rank = player["pp_rank"]
        self.level = player["level"]
        self.pp_raw = player["pp_raw"]
        self.accuracy = player["accuracy"]
        self.count_rank_ss = player["count_rank_ss"]
        self.count_rank_s = player["count_rank_s"]
        self.count_rank_a = player["count_rank_a"]
        self.country = player["country"]
        self.pp_country_rank = player["pp_country_rank"]

    def display(self):
        return ('`Username:` ' + self.username +
                '\n`Performance:` ' + self.pp_raw + 'pp' +
                '\n`Accuracy:` ' + self.accuracy +
                '\n`Level:` ' + self.level +
                '\n`Rank:` ' + self.pp_rank +
                '\nhttps://osu.ppy.sh/u/' + self.username
                )


class Osu:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def osu(self, ctx, *, args: str):
        """
        Look up an osu player:
        Usage: osu [UserID/Username] [Optional:Mode(default Osu!)]
        Modes:
            0 - Default Osu!
            1 - Taiko
            2 - ChitogeBot
            3 - Osu!mania
        """

        memes = args.split(' ')
        if len(memes) == 2:
            peppy = memes[0]
            kek = memes[1]
        elif len(memes) == 1:
            peppy = memes[0]
            kek = "0"
        else:
            await self.bot.say('Wrong Syntax!')
            return
        # TODO: REMEMBER TO DELETE THIS
        cookiezi = '05b43eb66b2977d4f2c9148b00e3853688d515cf'
        link = ('http://osu.ppy.sh/api/get_user?k=' + cookiezi + '&u=' + peppy
                + '&m=' + kek)
        r = requests.get(link)

        if r.status_code != 200:
            print('Peppy Failed')
            return
        brainpower = json.loads(r.text)

        hvick = OsuPlayer(brainpower[0])
        await self.bot.say(hvick.display())

    @commands.command(pass_context=True, no_pm=True)
    async def osusig(self, ctx, *, args:str):
        """
        Look up an osu player:
        Usage: osusig [UserID/Username] [Optional:Mode(default Osu!)]
        Modes:
            0 - Default Osu!
            1 - Taiko
            2 - ChitogeBot
            3 - Osu!mania
        """

        memes = args.split(' ')
        if len(memes) == 2:
            peppy = memes[0]
            kek = memes[1]
        elif len(memes) == 1:
            peppy = memes[0]
            kek = "0"
        else:
            await self.bot.say('Wrong Syntax!')
            return

        await self.bot.say("http://lemmmy.pw/osusig/sig.php?colour=hex66ccff&uname=" + peppy + "&mode=" + kek)



def setup(bot):
    bot.add_cog(Osu(bot))
