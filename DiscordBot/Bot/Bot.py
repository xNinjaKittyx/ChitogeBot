import logging
import requests
import threading
import random

import discord
from discord.utils import find
import wikipedia
from cassiopeia import riotapi
from cassiopeia import type
import re

__author__ = "Daniel Ahn"
__version__ = "0.4"
name = "ChitogeBot"

random.seed()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

games = requests.get('https://gist.githubusercontent.com/ZetaHunter/56f9e37455bbcdd7f2ef/raw/981703ac5ea835bdf4d418ec919c10af24d04f7e/games.json').json()

riotapi.set_region("NA")
riotapi.set_api_key("37a65ef7-6cfa-4d98-adc0-a3300b9cfc3a")

client = discord.Client()
client.login('daniel.s.ahn@biola.edu', 'Daniel7415295051')


if not client.is_logged_in:
    print('Logging in to Discord failed')
    exit(1)


def bot(message):
    client.send_message(message.channel,
                        "Hi, I'm {name}. I am running version {version}.".format(name=name, version=__version__))


def hello(message):
    client.send_message(message.channel, 'Hello {}-san!'.format(message.author.mention()))


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
                                    'Name: ' + member.name + '\nStatus: ' + member.status.capitalize() + '\nGame Playing: ' + gameplaying + '\nJoined on: ' + str(
                                        member.joined_at.month) + '/' + str(member.joined_at.day) + '/' + str(
                                        member.joined_at.year))

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


def lookup(message):
    argname = message.content[8:]

    def worker():
        try:
            summoner = riotapi.get_summoner_by_name(argname)
            client.send_message(message.channel, "Name: {name}\nLevel: {level}\nRank: {rank}".format(name=summoner.name, level=summoner.level, rank=summoner.leagues()[0]))
        except type.api.exception.APIError as e:
            client.send_message(message.channel, 'Lookup Failed.\nError: ' + str(e.error_code))

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


def roll(message):
    x = random.randint(1, 6)
    client.send_message(message.channel, '{} rolled a {}!'.format(message.author.mention(), x))


def cleverTalk(message):

    def worker():
        content = message.content()
        re.sub(client.user.mention() + " ", "",content, count=1)



@client.event
def on_message(message):

    if message.content.startswith('!bot'):
        bot(message)

    elif message.content.startswith('!help'):
        client.send_message(message.author, 'Type !help for help.')
        client.send_message(message.author, 'Type !hello for a hello message from the bot.')
        client.send_message(message.author, 'Type !who [user] for more info on the user.')
        client.send_message(message.author, 'Type !wiki [topic] for a wiki page.')

    elif message.content.startswith('Hello {}'.format(client.user.mention())):
        hello(message)

    elif message.content.startswith('!who'):
        who(message)

    elif message.content.startswith('!wiki'):
        wiki(message)

    elif message.content.startswith('!lookup'):
        lookup(message)

    elif message.content.startswith('!roll'):
        roll(message)

    elif message.content.startswith('#TeamOnodera'):
        client.send_message(message.channel, 'Fk off.')

    elif message.content.startswith('#TeamChitoge'):
        client.send_message(message.channel, 'Chitoge is so cute isn\'t she :D')

    elif message.content.startswith('#Tsunderes4Life'):
        client.send_message(message.channel, 'I like the way you think.')

    elif message.content.startswith('@{}'.format(str(client.user))):
        cleverTalk(message)




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


client.run()
