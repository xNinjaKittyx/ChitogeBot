import requests
import json
import asyncio
import discord
from discord.ext import commands


class PAD:
    def __init__(self, bot):
        self.bot = bot
        r = requests.get('https://www.padherder.com/api/monsters/')
        if r.status_code is not 200:
            print('/api/monsters/ is down')
        else:
            self.monsters = json.loads(r.text)
        r = requests.get('https://www.padherder.com/api/active_skills/')
        if r.status_code is not 200:
            print('/api/active_skills/ is down')
        else:
            self.active_skills = json.loads(r.text)

        r = requests.get('https://www.padherder.com/api/awakenings/')
        if r.status_code is not 200:
            print('/api/awakenings/ is down')
        else:
            self.awakenings = json.loads(r.text)

        r = requests.get('https://www.padherder.com/api/evolutions/')
        if r.status_code is not 200:
            print('/api/evolutions/ is down')
        else:
            self.evolutions = json.loads(r.text)

        r = requests.get('https://www.padherder.com/api/food/')
        if r.status_code is not 200:
            print('/api/food/ is down')
        else:
            self.monsterdb = json.loads(r.text)

    def getlink(self, id):
        return 'http://puzzledragonx.com/en/monster.asp?n=' + str(id)

    @commands.command(pass_context=True, no_pm=True)
    async def pad(self, ctx, *, arg: str):
        """ Searches a PAD monster"""

        # First check if str is too short...
        if len(arg) < 4:
            await self.bot.say('Please use more than 3 letters')
            return

        results = []
        arg = arg.lower()

        for m in self.monsters:
            if arg in m['name'].lower():
                results.append(m)

        if len(results) > 1:
            string = ''
            for m in results:
                if arg == m['name'].lower():
                    await self.bot.say(self.getlink(m['id']))
                    return
                string += str(m['name']) + '\n'
            await self.bot.say('Which one did you mean?\n' + string)
        elif len(results) == 1:
            await self.bot.say(self.getlink(results[0]['id']))
        else:
            await self.bot.say('No Monster Found')


def setup(bot):
    bot.add_cog(PAD(bot))
