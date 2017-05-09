
# -*- coding: utf8 -*-
import requests
import json
import asyncio
import discord
from discord.ext import commands
import tools.discordembed as dmbd

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

    def getawaken(self, skills):
        result = ""
        if skills == []:
            return 'None'
        for x in skills:
            result += self.awakenings[x+1]['name'] + "\n"
        return result

    def gettype(self, type1, type2=None, type3=None):
        types = [
        "Evo Material", "Balanced", "Physical", "Healer", "Dragon", "God",
        "Attacker", "Devil", "Machine", "", "", "", "", "", "Enhance Material"
        ]
        if type2 == None:
            return types[type1]
        elif type3 == None:
            return "{0}/{1}".format(types[type1], types[type2])
        else:
            return "/".join([types[type1], types[type2], types[type3]])

    def getlink(self, mon, author, index):
        title = mon['name']
        description = mon["name_jp"] + "\n" + "*" * mon["rarity"]
        url = 'http://puzzledragonx.com/en/monster.asp?n=' + str(mon['id'])
        em = dmbd.newembed(author, title, description, url)
        em.set_image(url='https://www.padherder.com' + mon['image60_href'])
        em.add_field(name='Type', value=self.gettype(mon['type'], mon['type2'], mon['type3']))
        em.add_field(name='Cost', value=mon['team_cost'])
        em.add_field(name='MaxLv', value="{0} ({1}xp)".format(mon['max_level'], mon['xp_curve']))
        em.add_field(name='HP', value="[{0}][{1}]".format(mon['hp_min'], mon['hp_max']))
        em.add_field(name='ATK', value="[{0}][{1}]".format(mon['atk_min'], mon['atk_max']))
        em.add_field(name='RCV', value="[{0}][{1}]".format(mon['rcv_min'], mon['rcv_max']))
        em.add_field(name='Leader Skill', value=str(mon['leader_skill']))
        em.add_field(name='Active Skill', value=str(mon['active_skill']))
        em.add_field(name='MP Sell Price', value=mon['monster_points'])
        em.add_field(name='Awakenings', value=self.getawaken(mon['awoken_skills']), inline=False)

        self.bot.cogs['WordDB'].cmdcount('pad')
        return em

    @commands.command(pass_context=True, no_pm=True)
    async def pad(self, ctx, *, arg: str):
        """ Searches a PAD monster"""
        author = ctx.message.author
        results = []
        index = []
        try:
            arg = int(arg)
            if arg in range(1, self.monsters[-1]['id']+1):
                for (n, x) in enumerate(self.monsters):
                    if arg == x['id']:
                        await self.bot.say(embed=self.getlink(x, author, n))
                        return
            await self.bot.say("ID is not valid.")
            return
        except ValueError:
            if len(arg) < 4:
                await self.bot.say('Please use more than 3 letters')
                return
            arg = arg.lower()
        # First check if str is too short...
        for (n, m) in enumerate(self.monsters):
            if arg in m['name'].lower():
                results.append(m)
                index.append(n)

        if len(results) > 1:
            string = ''
            for (n, m) in enumerate(results):
                if arg == m['name'].lower():
                    await self.bot.say(embed=self.getlink(m, author, index[n]))
                    return
                string += str(m['name']) + '\n'
            await self.bot.say('Which one did you mean?\n' + string)
        elif len(results) == 1:
            await self.bot.say(embed=self.getlink(results[0], author, index[0]))
        else:
            await self.bot.say('No Monster Found')


def setup(bot):
    bot.add_cog(PAD(bot))
