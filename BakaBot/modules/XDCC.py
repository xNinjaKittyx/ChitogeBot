import asyncio
import json
import os

import discord
from discord.ext import commands



class XDCC:

    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists('./json'):
            os.makedirs('./json')
        if not os.path.isfile('./json/downloads.json'):
            with open('./json/downloads.json', 'w',) as outfile:
                json.dump({0 : {'Name': 'asdf', 'Size': 0, 'Link': 'asdf'}}, outfile, indent=4)
        with open('./json/downloads.json') as data_file:
            self.downloads = json.load(data_file)
        #Downloads Format should be...
        # ID, Name, Size, Link
    @commands.group(pass_context=True)
    async def xdcc(self, ctx):
        with open('./json/downloads.json') as data_file:
            self.downloads = json.load(data_file)
        if ctx.invoked_subcommand is None:
            await self.bot.say('No command passed. Type ~xdcc help for more info')


    @xdcc.command()
    async def help(self):
        string = """
```
This is actually a fake, wannabe XDCC command.
Commands:
~xdcc help
    Gets this help page.
~xdcc list
    Sends you list of everything in a PM
~xdcc list [a] [b]
    Sends you list of everything from a to b (IDS)
~xdcc search *search terms*
    Search for file.
~xdcc info [x]
    Get info for a file
~xdcc get [x]
    Get specific file.
```"""
        await self.bot.say(string)

    @xdcc.command(pass_context=True)
    async def list(self):
        """See ~xdcc help for more info"""
        return

    @xdcc.command(pass_context=True)
    async def search(self):
        """See ~xdcc help for more info"""
        return

    @xdcc.command()
    async def info(self, request: str):
        """See ~xdcc help for more info"""
        if request in self.downloads:
            info = self.downloads[request]
            await self.bot.say("```\nID: " + request +
                               "\nName: " + info['Name'] +
                               "\nSize: " + str(info['Size']) + " MB```")
        else:
            await self.bot.say('Not Found')
        return

    @xdcc.command(pass_context=True)
    async def get(self, ctx, request: str):
        """See ~xdcc help for more info"""
        if request in self.downloads:
            info = self.downloads[request]
            await self.bot.send_message(ctx.message.author,
                                    "```\nID: " + request +
                                    "\nName: " + info['Name'] +
                                    "\nSize: " + str(info['Size']) + " MB```")
            await self.bot.send_message(ctx.message.author,
                                        self.downloads[request]['Link'])
        else:
            await self.bot.send_message(ctx.message.author, 'Not Found')
        return

def setup(bot):
    bot.add_cog(XDCC(bot))
