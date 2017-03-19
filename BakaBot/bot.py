import asyncio
import json
import logging
import random
import os
import time

import discord
import requests
import wikipedia
import modules.checks as checks
from discord.ext import commands
from discord.utils import find
from cleverwrap import CleverWrap
from PIL import Image
import log


__author__ = "Daniel Ahn"
__version__ = "0.6"
name = "BakaBot"


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
                   u"CleverbotAPI": u"PutAPIKeyHere",
                   u"Prefix": u"~"},
                  outfile, indent=4)
with open('./json/setup.json') as data_file:
    settings = json.load(data_file)

logging.basicConfig(filename='rin.log', level=logging.WARNING)

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='../discord.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: \
                                        %(name)s: %(message)s'))
logger.addHandler(handler)


random.seed()
cb = CleverWrap(settings["CleverbotAPI"])

prefix = settings["Prefix"]
description = '''Baka means Idiot in Japanese.'''
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=True)
initialtime = time.time()


modules = {
    'modules.anime',
    'modules.cat',
    'modules.comics',
    'modules.fun',
    'modules.gfycat',
    'modules.musicplayer',
    'modules.osu',
    'modules.overwatch',
    'modules.pad',
    'modules.ranks',
    'modules.safebooru',
    'modules.weather',
    'modules.wordDB',
    'modules.XDCC'

}

def checkignorelistevent(chan):
    # checkignorelist given a channel.
    for serverid in ignore["servers"]:
        if serverid == chan.server.id:
            return True

    for channelid in ignore["channels"]:
        if channelid == chan.id:
            return True


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

@bot.command(pass_context=True)
async def ask(ctx, *, s: str):
    """ Asks wolfram alpha"""
    s.replace(' ', '+')
    req = requests.get("http://api.wolframalpha.com/v1/result?appid=RPYQ54-Q3W9QJKWR9&i=" + s)
    await bot.say(req.text)

@bot.command()
async def uptime():
    """ Displays Uptime """
    seconds = int(time.time() - initialtime)
    minutes = 0
    hours = 0
    days = 0
    output = ""
    if seconds > 59:
        minutes = int(seconds / 60)
        seconds -= minutes * 60

    if minutes > 59:
        hours = int(minutes/60)
        minutes -= hours * 60

    if hours > 23:
        days = int(hours/24)
        hours -= days * 24

    if seconds == 1:
        output = " {} second.".format(seconds) + output
    elif seconds == 0:
        pass
    else:
        output = " {} seconds.".format(seconds) + output

    if minutes == 1:
        output = " {} minute,".format(minutes) + output
    elif minutes == 0:
        pass
    else:
        output = " {} minutes,".format(minutes) + output

    if hours == 1:
        output = " {} hour,".format(hours) + output
    elif hours == 0:
        pass
    else:
        output = " {} hours,".format(hours) + output

    if days == 1:
        output = " {} day,".format(days) + output
    elif days == 0:
        pass
    else:
        output = " {} days,".format(days) + output

    await bot.say("*This Bot has been alive for" + output +  "*")


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


@bot.event
async def on_member_join(member):
    await bot.send_message(member, "Welcome to {0}! Feel free to read the things in #announcement, and when you're ready, type ~normie in #openthegates".format(member.server.name))
    log.output(member.name + " has joined the server.")


@bot.event
async def on_member_remove(member):
    await bot.send_message(member.server.default_channel, '{} has left the server.'.format(member.name))
    log.output(member.name + " has left the server.")

@bot.event
async def on_message_delete(message):
    msg = '{0} deleted the following message: \n{1}'.format(message.author.name, message.content)
    modlog = find(lambda c: c.name == "modlog", message.server.channels)
    await bot.send_message(modlog, msg)
    log.output(msg)

@bot.event
async def on_message_edit(before, after):
    if before.content.startswith('http'):
        return
    msg = '{0} edit the following message: \nBefore: {1}\n After: {2}'.format(before.author.name, before.content, after.content)
    modlog = find(lambda c: c.name == "modlog", before.server.channels)
    await bot.send_message(modlog, msg)
    log.output(msg)


@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        msg = message.author.name + " attempted to use the command: " + message.content
        modlog = find(lambda c: c.name == "modlog", message.server.channels)
        log.output(msg)
        await bot.send_message(modlog, msg)
    if message.author == bot.user:
        return
    if not checks.checkdev(message) and checks.checkignorelist(message, ignore):
        return

    if message.content.startswith(bot.user.mention):
        await bot.send_typing(message.channel)
        try:
            response = cw.say(message.content.split(' ', 1)[1])
            await bot.send_message(message.channel,
                                   message.author.mention + ' ' + response)
        except IndexError:
            await bot.send_message(message.channel,
                                   message.author.mention + ' Don\'t give me '
                                   'the silent treatment.')
        return
    await bot.process_commands(message)


@bot.event
async def on_ready():

    log.output('Logged in as')
    log.output("Username " + bot.user.name)
    log.output("ID: " + bot.user.id)
    if not discord.opus.is_loaded() and os.name == 'nt':
        discord.opus.load_opus("opus.dll")

    if not discord.opus.is_loaded() and os.name == 'posix':
        discord.opus.load_opus("/usr/local/lib/libopus.so")
    log.output("Loaded Opus Library")
    initialtime = time.time()


if __name__ == "__main__":
    random.seed()
    try:
        for x in modules:
            bot.load_extension(x)
    except ImportError as e:
        print(e)
        print('[WARNING] : One or more modules did not import.')
    bot.run(settings["botkey"])
