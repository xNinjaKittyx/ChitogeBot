import asyncio
import json
import logging
import random
import os
from io import BytesIO
import sys

import discord
import requests
import wikipedia
import modules.checks as checks
from discord.ext import commands
from cleverbot import Cleverbot
from PIL import Image


__author__ = "Daniel Ahn"
__version__ = "0.6"
name = "BakaBot"

sys.stdout = open('./rin.log', 'w')


if not os.path.exists('./json'):
    os.makedirs('./json')
if not os.path.isfile('./json/ignore.json'):
    with open('./json/ignore.json', 'w',) as outfile:
        json.dump({"servers": [], "channels": [], "users": []},
                  outfile, indent=4)
with open('./json/ignore.json') as data_file:
    ignore = json.load(data_file)

if not os.path.isfile('./json/setup.json'):
    with open('./json/setup.json', 'w',) as outfile:
        json.dump({u"botkey": u"putkeyhere",
                   u"MALUsername": u"InsertUser",
                   u"MALPassword": u"Password",
                   u"GoogleAPIKey": u"PutKeyHere",
                   u"DarkSkyAPIKey": u"PutAPIKeyHere",
                   u"Prefix": u"~"},
                  outfile, indent=4)
with open('./json/setup.json') as data_file:
    settings = json.load(data_file)

logging.basicConfig(filename='rin.log', level=logging.WARNING)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: \
                                        %(name)s: %(message)s'))
logger.addHandler(handler)



random.seed()
cb = Cleverbot()


description = '''Baka means Idiot in Japanese.'''
bot = commands.Bot(command_prefix=settings["Prefix"], description=description, pm_help=True)

modules = {
    'modules.musicplayer',
    'modules.anime',
    'modules.pad',
    'modules.cat',
    'modules.osu',
    'modules.safebooru',
    'modules.fun',
    'modules.wordDB',
    'modules.XDCC',
    'modules.ranks',
    'modules.gfycat',
    'modules.weather',
    'modules.xkcd'

}
# TODO: Needs config with the following
# 3 - Command Prefix should also be a config
# 4 - Description probably?

def checkignorelistevent(chan):
    # checkignorelist given a channel.
    for serverid in ignore["servers"]:
        if serverid == chan.server.id:
            return True

    for channelid in ignore["channels"]:
        if channelid == chan.id:
            return True


@bot.event
async def on_member_join(member):
    await bot.send_message(member, "Welcome to {0}! Feel free to read the things in #announcement, and when you're ready, type ~normie in #openthegates".format(member.server.name))


@bot.event
async def on_member_remove(member):
    await bot.send_message(member.server.default_channel, '{} has left the server.'.format(member.name))


@bot.event
async def on_ready():

    print('Logged in as')
    print("Username " + bot.user.name)
    print("ID: " + bot.user.id)
    if not discord.opus.is_loaded() and os.name == 'nt':
        discord.opus.load_opus("opus.dll")

    if not discord.opus.is_loaded() and os.name == 'posix':
        discord.opus.load_opus("/usr/local/lib/libopus.so")
    print("Loaded Opus Library")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not checks.checkdev(message) and checks.checkignorelist(message, ignore):
        return

    if message.content.startswith(bot.user.mention):
        await bot.send_typing(message.channel)
        try:
            response = cb.ask(message.content.split(None, 1)[1])
            await bot.send_message(message.channel,
                                   message.author.mention + ' ' + response)
        except IndexError:
            await bot.send_message(message.channel,
                                   message.author.mention + ' Don\'t give me '
                                   'the silent treatment.')
        return
    await bot.process_commands(message)


@bot.command()
async def wiki(*, search: str):
    """ Grabs Wikipedia Article """
    searchlist = wikipedia.search(search)
    if len(searchlist) < 1:
        await bot.say('No Results Found')
    else:
        page = wikipedia.page(searchlist[0])
        await bot.say(wikipedia.summary(searchlist[0], 3))
        await bot.say('URL:' + page.url)

@bot.command(pass_context=True, hidden=True)
async def status(ctx, *, s: str):
    """ Changes Status """
    if checks.checkdev(ctx.message):
        await bot.change_presence(game=discord.Game(name=s))

@bot.command(pass_context=True, hidden=True)
async def changeAvatar(ctx, *, url: str):
    if checks.checkdev(ctx.message):
        response = requests.get(url)

        if response.content is None:
            bot.send_message(ctx.message.author, "Picture conversion Failed")
            return
        try:
            await bot.edit_profile(avatar=response.content)
        except HTTPException as e:
            print("Editing the profile failed.")

@bot.command(pass_context=True, hidden=True)
async def changeUsername(ctx, *, s: str):
    if checks.checkdev(ctx.message):
        await bot.edit_profile(username=s)



if __name__ == "__main__":
    random.seed()
    try:
        for x in modules:
            bot.load_extension(x)
    except ImportError as e:
        print(e)
        print('[WARNING] : One or more modules did not import.')
    bot.run(settings["botkey"])


    # ##################
    # # Admin Commands #
    # ##################
    # elif message.content.startswith('!eval'):
    #     await evaluate(message)
    #
    # elif message.content.startswith('!uptime'):
    #     await uptime(message)
    #
    # elif message.content.startswith('!who'):
    #     await who(message)
