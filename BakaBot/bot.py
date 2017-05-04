import asyncio
import json
import logging
import random
import os
import time

import discord
import requests
import tools.checks as checks
import tools.discordembed as dmbd
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
        json.dump({u"botkey": None,
                   u"MALUsername": None,
                   u"MALPassword": None,
                   u"GoogleAPIKey": None,
                   u"DarkSkyAPIKey": None,
                   u"CleverbotAPI": None,
                   u"AnilistID": None,
                   u"AnilistSecret": None,
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
if settings["CleverbotAPI"]:
    try:
        cw = CleverWrap(settings["CleverbotAPI"])
    except:
        log.output("CleverbotAPIKey was not accepted.")
else:
    log.output("No CleverBotAPI was Provided")

prefix = settings["Prefix"]
description = '''Baka means Idiot in Japanese.'''
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=True)

modules = {
    'modules.anime',
    'modules.cat',
    'modules.comics',
    'modules.fun',
    'modules.gfycat',
    'modules.info',
#    'modules.musicplayer',
    'modules.osu',
    'modules.overwatch',
#    'modules.pad',
#    'modules.ranks',
#    'modules.safebooru',
#    'modules.weather',
    'modules.wordDB',
#    'modules.XDCC'
    'modules.animehangman'

}



def checkignorelistevent(chan):
    # checkignorelist given a channel.
    for serverid in ignore["servers"]:
        if serverid == chan.server.id:
            return True

    for channelid in ignore["channels"]:
        if channelid == chan.id:
            return True

@bot.command(pass_context=True, hidden=True)
async def kill(ctx):
    if not checks.checkdev(ctx.message):
        return
    bot.cogs['WordDB'].cmdcount('kill')
    await bot.say("*Bot is kill in 3 seconds.*")
    await asyncio.sleep(3)
    await bot.close()

@bot.command(hidden=True)
async def testembed():
    title = 'My Embed Title'
    desc = 'My Embed Description'
    em = dmbd.newembed(bot.user, title, desc)
    em.set_image(url="https://myanimelist.cdn-dena.com/images/anime/3/67177.jpg")
    em.set_thumbnail(url="http://wiki.faforever.com/images/e/e9/Discord-icon.png")
    em.add_field(name="wololol", value='[ohayo](http://www.google.com)')
    em.add_field(name=":tururu:", value="wtf")
    em.add_field(name="wololol", value="wtf")
    em.add_field(name="imgay", value="baka", inline=False)
    em.add_field(name="imgay", value="baka", inline=False)
    em.add_field(name="imgay", value="baka", inline=False)
    await bot.say(embed=em)


@bot.command(pass_context=True, hidden=True)
async def status(ctx, *, s: str):
    """ Changes Status """
    if checks.checkdev(ctx.message):
        await bot.change_presence(game=discord.Game(name=s))
        bot.cogs['WordDB'].cmdcount('status')

@bot.command(pass_context=True, hidden=True)
async def changeavatar(ctx, *, url: str):
    if checks.checkdev(ctx.message):
        response = requests.get(url)

        if response.content is None:
            bot.send_message(ctx.message.author, "Picture conversion Failed")
            return
        try:
            await bot.edit_profile(avatar=response.content)
            bot.cogs['WordDB'].cmdcount('changeavatar')
        except HTTPException as e:
            print("Editing the profile failed.")

@bot.command(pass_context=True, hidden=True)
async def changeusername(ctx, *, s: str):
    if checks.checkdev(ctx.message):
        await bot.edit_profile(username=s)
        bot.cogs['WordDB'].cmdcount('changeusername')


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
    if message.author == bot.user:
        return
    msg = '{0} deleted the following message: \n{1}'.format(message.author.name, message.content)
    modlog = find(lambda c: c.name == "modlog", message.server.channels)
    await bot.send_message(modlog, msg)
    log.output(msg)

@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return
    if before.content == after.content:
        return
    msg = '{0} edit the following message: \nBefore: {1}\n After: {2}'.format(before.author.name, before.content, after.content)
    modlog = find(lambda c: c.name == "modlog", before.server.channels)
    await bot.send_message(modlog, msg)
    log.output(msg)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(prefix):
        msg = message.author.name + " attempted to use the command: " + message.content
        modlog = find(lambda c: c.name == "modlog", message.server.channels)
        log.output(msg)
        await bot.send_message(modlog, msg)
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


if __name__ == "__main__":
    random.seed()
    try:
        for x in modules:
            bot.load_extension(x)
    except ImportError as e:
        print(e)
        print('[WARNING] : One or more modules did not import.')
    bot.run(settings["botkey"])
