import asyncio
import json
import os
import operator

import discord
from discord.ext import commands

class WordDB:

    def __init__(self, bot):
        self.bot = bot

        if not os.path.exists('./json'):
            os.makedirs('./json')
        if not os.path.isfile('./json/wordDB.json'):
            with open('./json/wordDB.json', 'w',) as outfile:
                json.dump({}, outfile, indent=4)
        with open('./json/wordDB.json') as data_file:
            self.wordDB = json.load(data_file)

    def updatejsonfile(self):
        """Update the json file"""
        with open('./json/wordDB.json', 'w',) as outfile:
            json.dump(self.wordDB, outfile, indent=4)

    async def on_message(self, message):
        if message.content.startswith('~'):
            return
        if message.author.bot:
            return

        for x in message.content.split(' '):
            if x in self.wordDB:
                self.wordDB[str(x)] += 1
            else:
                self.wordDB[str(x)] = 1

        self.updatejsonfile()

    @commands.command()
    async def topwords(self):
        sorted_db = sorted(self.wordDB.items(), key=operator.itemgetter(1), reverse=True)

        string = ''
        digits = max(map(len, sorted_db))
        f = '{0:>%d} | {1}\n' % (digits)
        for i, x in zip(range(10), sorted_db):
            string += (str(x) + '\n')
        await self.bot.say(string)

def setup(bot):
    bot.add_cog(WordDB(bot))
