import json
import logging
import random
import re
import requests
import threading
import time
import os

import discord
from discord.utils import find
import wikipedia
from cassiopeia import riotapi
from cassiopeia import type
from pyglet import media

__author__ = "Daniel Ahn"
__version__ = "0.5.1"
name = "ChitogeBot"

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
client.login('daniel.s.ahn@biola.edu', 'Daniel7415295051')

if not client.is_logged_in:
    print('Logging in to Discord failed')
    exit(1)

random.seed()

games = requests.get(
    'https://gist.githubusercontent.com/ZetaHunter/56f9e37455bbcdd7f2ef/raw/981703ac5ea835bdf4d418ec919c10af24d04f7e/games.json').json()

riotapi.set_region("NA")
riotapi.set_api_key("37a65ef7-6cfa-4d98-adc0-a3300b9cfc3a")

player = media.Player()


def bot(message):
    client.send_message(message.channel,
                        "Hi, I'm {name}. I am running version {version}.".format(name=name, version=__version__))


def cinfo(message):
    if not message.channel.is_private:
        client.send_message(message.channel, "```Name: " + message.channel.name + "\nID: " + message.channel.id +
                            "\nType: " + message.channel.type + "```")
    else:
        client.send_message(message.channel, "```User: " + message.channel.user + "\nID: " + message.channel.id + "```")


def debug(message):
    argname = message.content[7:]

    if message.author.id == "82221891191844864":
        try:
            client.send_message(message.channel, "```{}```".format(eval(argname)))
        except SyntaxError as err:
            client.send_message(message.channel, "```{}```".format(err))


def exec(message):
    argname = message.content[6:]

    if message.author.id == "82221891191844864":
        try:
            client.send_message(message.channel, "```{}```".format(exec(argname)))
        except SyntaxError as err:
            client.send_message(message.channel, "```{}```".format(err))


def eval(message):
    argname = message.content[6:]

    if message.author.id == "82221891191844864":
        try:
            client.send_message(message.channel, "```{}```".format(eval(argname)))
        except SyntaxError as err:
            client.send_message(message.channel, "```{}```".format(err))


def hello(message):
    client.send_message(message.channel, 'Hello {}-san!'.format(message.author.mention()))


def invite(message):
    argname = message.content[8:]
    #TODO: join a server by invite. Need to make IGNORE list first


def join(message):
    argname = message.content[6:]
    #TODO: Join A Voice_Channel


def listmusic(message):
    list = ""
    files = [f for f in os.listdir('music') if os.path.isfile('music/' + f)]
    for f in files:
        list += str(f) + " || "
    client.send_message(message.channel, "```\n" + list[:-4] + "\n```")


def lookup(message):
    argname = message.content[8:]

    def worker():
        try:
            summoner = riotapi.get_summoner_by_name(argname)
            client.send_message(message.channel, "Name: {name}\nLevel: {level}\nRank: {rank}".format(name=summoner.name,
                                                                                                     level=summoner.level,
                                                                                                     rank=
                                                                                                     summoner.leagues()[
                                                                                                         0]))
        except type.api.exception.APIError as e:
            client.send_message(message.channel, 'Lookup Failed.\nError: ' + str(e.error_code))

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


def play(message):
    argname = message.content[6:]
    songname = ''
    if argname.len() < 3:
        client.send_message(message.channel, '```Songname too short```')
        return
    try:
        files = [f for f in os.listdir('music') if os.path.isfile('music/' + f)]
        for f in files:
            if f.startswith(argname):
                songname = f
                break
        song = media.load('music/' + songname, streaming=False)
        player.queue(song)
        player.play()
    except FileNotFoundError:
        client.send_message(message.channel, '```No such file or directory```')



def roll(message):
    x = random.randint(1, 6)
    client.send_message(message.channel, '{} rolled a {}!'.format(message.author.mention(), x))


def uptime(message):
    totalMin = 0
    totalHr = 0
    totalDay = 0

    totalSec = int(time.clock() - upTime)
    if totalSec > 60:
        totalMin = int(totalSec / 60)
        totalSec -= (totalMin * 60)
    if totalMin > 60:
        totalHr = int(totalMin / 60)
        totalMin -= (totalHr * 60)
    if totalHr > 24:
        totalDay = int(totalHr / 24)
        totalHr -= (totalDay * 24)
    client.send_message(message.channel,
                        'ChitogeBot has been running for {} days, {} hours, {} minutes, and {} seconds '
                        .format(totalDay, totalHr, totalMin, totalSec))


def who(message):
    argname = message.content[5:]
    if len(argname) == 0:
        client.send_message(message.channel, 'Usage: !who [user]')
    elif len(argname) < 3:
        client.send_message(message.channel, 'You need to type more than 3 letters for the user!')
    else:
        userfound = False
        for member in message.channel.server.members:
            if member.name.lower() == argname.lower():
                userfound = True
                try:
                    gameplaying = find(lambda game: game['id'] == member.game_id, games)['name']
                except TypeError:
                    gameplaying = 'None'
                client.send_message(message.channel,
                                    '```Name: ' + member.name + '\nID: ' + member.id +
                                    '\nStatus: ' + member.status.capitalize() + '\nGame Playing: ' + gameplaying +
                                    '\nAvatar: ' + member.avatar_url() +
                                    '\nJoined on: ' + str(member.joined_at.month) + '/' +
                                    str(member.joined_at.day) + '/' + str(member.joined_at.year) + '```')

                break
        if not userfound:
            for member in message.channel.server.members:
                if member.name.lower().startswith(argname.lower()):
                    userfound = True
                    try:
                        gameplaying = find(lambda game: game['id'] == member.game_id, games)['name']
                    except TypeError:
                        gameplaying = 'None'
                    client.send_message(message.channel,
                                        'Name: ' + member.name + '\nStatus: ' + member.status.capitalize() + '\nGame Playing: ' + gameplaying + '\nJoined on: ' + str(
                                            member.joined_at.month) + '/' + str(member.joined_at.day) + '/' + str(
                                            member.joined_at.year))
                    break
        if not userfound:
            client.send_message(message.channel, "User not found.")


def wiki(message):
    argname = message.content[6:]

    def worker():
        try:
            wikipage = wikipedia.page(argname)
            client.send_message(message.channel, wikipage.url)
        except wikipedia.exceptions.DisambiguationError:
            client.send_message(message.channel, 'Too Ambiguous.')
        except wikipedia.exceptions.HTTPTimeoutError:
            client.send_message(message.channel, 'Wikipedia Timed Out.')
        except wikipedia.exceptions.PageError:
            client.send_message(message.channel, 'There is no match.')
        except wikipedia.exceptions.RedirectError:
            client.send_message(message.channel, 'Redirect Error, Check Console.')
        except wikipedia.exceptions.WikipediaException:
            client.send_message(message.channel, 'Something Wrong with wikipedia.')

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


def cleverTalk(message):
    def worker():
        content = message.content()
        re.sub(client.user.mention() + " ", "", content, count=1)


@client.event
def on_message(message):
    if message.content.startswith('!bot'):
        bot(message)

    elif message.content.startswith('!cinfo'):
        cinfo(message)

    elif message.content.startswith('!debug'):
        debug(message)

    elif message.content.startswith('!eval'):
        eval(message)

    elif message.content.startswith('!exec'):
        exec(message)

    elif message.content.startswith('!help'):
        client.send_message(message.author, '!help - Display this help message.\n' +
                            '!cinfo - Channel Information\n' +
                            '!who [user] - User Information\n' +
                            '!wiki [topic] - Look for a wiki page\n' +
                            '!listmusic - List all music files available on the bot\n' +
                            '!lookup [Summoner] - Find Summoner on LoL\n' +
                            '!next - Play the next song\n' +
                            '!pause - Pause the song\n' +
                            '!play [song] - Play a song\n' +
                            '!resume - Resume the player' +
                            '!stop - Stop the player - Currently not working\n' +
                            '!roll - Roll a die\n' +
                            '!uptime - Bot uptime\n' +
                            'More to Come! Check https://github.com/xNinjaKittyx/ChitogeBot')

    elif message.content.startswith('Hello {}'.format(client.user.mention())):
        hello(message)

    elif message.content.startswith('!listmusic'):
        listmusic(message)

    elif message.content.startswith('!lookup'):
        lookup(message)

    elif message.content.startswith('!next'):
        player.next_source()

    elif message.content.startswith('!pause'):
        player.pause()

    elif message.content.startswith('!play'):
        play(message)

    elif message.content.startswith('!resume'):
        player.play()

    elif message.content.startswith('!stop'):
        player.pause()

    elif message.content.startswith('!roll'):
        roll(message)

    elif message.content.startswith('!uptime'):
        uptime(message)

    elif message.content.startswith('!who'):
        who(message)

    elif message.content.startswith('!wiki'):
        wiki(message)

    elif message.content.startswith('#TeamOnodera'):
        client.send_message(message.channel, 'Fk off.')

    elif message.content.startswith('#TeamChitoge'):
        client.send_message(message.channel, 'Chitoge is so cute isn\'t she :D')

    elif message.content.startswith('#Tsunderes4Life'):
        client.send_message(message.channel, 'I like the way you think.')

    elif message.content.startswith('{}'.format(client.user.mention())):
        client.send_message(message.channel, 'You have mentioned me.')


@client.event
def on_member_join(member):
    channel = find(lambda chan: chan.name == 'public', member.server.channels)
    client.send_message(channel, 'Please welcome {name} to the server!'.format(name=member.mention()))


@client.event
def on_member_remove(member):
    channel = find(lambda chan: chan.name == 'public', member.server.channels)
    client.send_message(channel, '{name} has left the server.'.format(name=member))


@client.event
def on_ready():
    print('Logged in as')
    print("Username " + client.user.name)
    print("ID: " + client.user.id)

upTime = time.clock()
client.run()
