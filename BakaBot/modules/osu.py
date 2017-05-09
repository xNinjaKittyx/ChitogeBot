import requests
import json
import asyncio
import discord
from discord.ext import commands
import tools.discordembed as dmbd

class OsuPlayer:

    def __init__(self, player):
        self.id = player["user_id"]
        self.username = player["username"]
        self.c300 = player["count300"]
        self.c100 = player["count100"]
        self.c50 = player["count50"]
        self.playcount = player["playcount"]
        self.ranked = player["ranked_score"]
        self.total = player["total_score"]
        self.pp = player["pp_rank"]
        self.level = player["level"]
        self.pp_raw = player["pp_raw"]
        self.accuracy = player["accuracy"]
        self.count_ss = player["count_rank_ss"]
        self.count_s = player["count_rank_s"]
        self.count_a = player["count_rank_a"]
        self.country = player["country"]
        self.pp_country_rank = player["pp_country_rank"]

    def display(self, author):
        title = self.username
        desc = self.country.upper()
        url = 'https://osu.ppy.sh/u/' + self.username
        em = dmbd.newembed(author, title, desc, url)
        em.add_field(name='Performance', value=self.pp_raw + 'pp')
        em.add_field(name='Accuracy', value="{0:.2f}%".format(float(self.accuracy)))
        lvl = int(float(self.level))
        percent = int((float(self.level) - lvl) * 100)
        em.add_field(name='Level', value="{0} ({1}%)".format(lvl,percent))
        em.add_field(name='Rank', value=self.pp)
        em.add_field(name='Country Rank', value=self.pp_country_rank)
        em.add_field(name='Playcount', value=self.playcount)
        em.add_field(name='Total Score', value=self.total)
        em.add_field(name='Ranked Score', value=self.ranked)
        return em
        # ('`Username:` ' + self.username +
        #         '\n`Performance:` ' + self.pp_raw + 'pp' +
        #         '\n`Accuracy:` ' + self.accuracy +
        #         '\n`Level:` ' + self.level +
        #         '\n`Rank:` ' + self.pp +
        #         '\nhttps://osu.ppy.sh/u/' + self.username
        #         )


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
        await self.bot.say(embed=hvick.display(ctx.message.author))

        self.bot.cogs['WordDB'].cmdcount('osu')

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
        author = ctx.message.author
        em = dmbd.newembed(author)
        em.set_image(url="http://lemmmy.pw/osusig/sig.php?colour=hex66ccff&uname=" + peppy + "&mode=" + kek)

        await self.bot.say(embed=em)
        self.bot.cogs['WordDB'].cmdcount('osusig')



def setup(bot):
    bot.add_cog(Osu(bot))
