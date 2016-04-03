
import asyncio
import json
import logging
import random
import threading
import time
import os


import discord
from discord.utils import find
import wikipedia
from cassiopeia import riotapi
from cassiopeia import type


__author__ = "Daniel Ahn"
__version__ = "0.6"
name = "ChitogeBot"

if not os.path.exists('../json'):
    os.makedirs('../json')

if not os.path.isfile('../json/ignore.json'):
    with open('../json/ignore.json', 'w',) as outfile:
        json.dump({"servers": [], "channels": [], "users": []},
                  outfile, indent=4)


with open('../json/ignore.json') as data_file:
    ignore = json.load(data_file)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: \
                                        %(name)s: %(message)s'))
logger.addHandler(handler)

print("Welcome to ChitogeBot. Please type in your credentials.")
username = input("Username: ")
password = input("Password: ")

client = discord.Client()


random.seed()


riotapi.set_region("NA")
riotapi.set_api_key("37a65ef7-6cfa-4d98-adc0-a3300b9cfc3a")

voiceclient = 0
voiceclient_player = 0


##############
# Decorators #
##############


def display(func):
    """Displays the message returned by a function"""
    async def inner(*args, **kwargs):
        channel, message = func(*args, **kwargs)
        await client.send_message(channel, message)
        return
    return inner


def logger(func):
    """Logs the function used to the console"""
    def inner(message):
        print('Function: {0} was used by {1}'.format(func, message.author))
        return
    return inner

##################
# Admin Commands #
##################


def updatejsonfile():
    """Update the json file"""
    with open('../json/ignore.json', 'w',) as outfile:
        json.dump(ignore, outfile, indent=4)


def checkdev(message):
    """Checks if the developer used the command. AKA ME"""
    if message.author.id == "82221891191844864":
        return True
    else:
        return False


def checkPrivate(message):
    """Checks if the message is a PM"""
    if message.channel.is_private is True:
        return True
    else:
        return False


@display
def ignoreserver(message):
    """Ignore the Discord Server"""
    if not checkdev(message):
        return
    count = 0
    for serverid in ignore["servers"]:
        if serverid == message.channel.server.id:
            ignore["servers"].pop(count)
            updatejsonfile()
            return message.channel, 'Server Unignored'
        count += 1
    ignore["servers"].append(message.channel.server.id)
    updatejsonfile()
    return message.channel, 'Server Ignored'


@display
def ignorechannel(message):
    """Ignore the Channel"""
    if not checkdev(message):
        return
    count = 0
    for channelid in ignore["channels"]:
        if channelid == message.channel.id:
            ignore["channels"].pop(count)

            updatejsonfile()
            return message.channel, 'Channel Unignored'
        count += 1
    ignore["channels"].append(message.channel.id)

    updatejsonfile()
    return message.channel, 'Channel Ignored'


@display
def ignoreuser(message):
    """Ignore a specific user"""
    if not checkdev(message):
        return
    argname = message.content[12:]
    member = find(lambda m: m.name == argname, message.server.members)
    count = 0
    for userid in ignore["users"]:
        if userid == member.id:
            ignore["users"].pop(count)

            updatejsonfile()
            return message.channel, 'I\'ll listen to ' + member.name
        count += 1
    ignore["users"].append(member.id)

    updatejsonfile()
    return message.channel, 'Alright, I\'ll ignore ' + member.name


def checkignorelist(message):
    """If on the list, return true; if not, return false."""
    for serverid in ignore["servers"]:
        if serverid == message.channel.server.id:
            return True

    for channelid in ignore["channels"]:
        if channelid == message.channel.id:
            return True

    for userid in ignore["users"]:
        if userid == message.author.id:
            return True

    return False


#################
# Info Commands #
#################


@display
def avatar(message):
    """ Returns the user's avatar """
    user = message.content[8:]
    member = find(lambda m: m.name == user, message.server.members)
    if member:
        return (message.channel, message.author.avatar_url)


@display
def bot(message):
    """Returns the bot's info"""
    return (message.channel,
            "Hi, I'm {0}. Version: {1}. I am using {2}"
            .format(name, __version__, discord.__version__))


@display
def cinfo(message):
    """Returns the Channel's Info"""
    if not message.channel.is_private:
        return (message.channel, ("```Name: {0}\nID: {1}\nType: {2}```"
                .format(message.channel.name, message.channel.id,
                        message.channel.type)))
    else:
        return (message.channel, ("```User: {0}\nID: {1}```"
                .format(message.channel.user, message.channel.id)))


@display
def hello(message):
    """Respond with a hello message"""
    return message.channel, 'Hello {}-san!'.format(message.author.mention)


@display
def helpmsg(message):
    """Sends the Help Message"""
    return (message.channel, ('HERES ALL THE COMMANDS {}-SAMA\n'
                              '!help - Display this help message.\n'
                              '!cinfo - Channel Information\n'
                              '!who [user] - User Information\n'
                              '!wiki [topic] - Look for a wiki page\n'
                              '!listmusic - '
                              'List all music files available on the bot\n\n'
                              '!lookup [Summoner] - Find Summoner on LoL\n'
                              '!next - Play the next song\n'
                              '!pause - Pause the song\n'
                              '!play [song] - Play a song\n'
                              '!resume - Resume the player\n'
                              '!stop - Stop the player - '
                              'Currently not working\n'
                              '!roll - Roll a die\n'
                              '!uptime - Bot uptime\n'
                              'More to Come!\n'
                              'Check https://github.com/'
                              'xNinjaKittyx/ChitogeBot\n'
                              .format(message.author.mention)))


@display
def uptime(message):
    """Returns bot's Uptime"""
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
    return (message.channel, ('ChitogeBot has been running for {} days, '
                              '{} hours, {} minutes, and {} seconds '
                              ).format(totalDay, totalHr, totalMin, totalSec))


@display
def who(message):
    """ Displays who someone is """
    argname = message.content[5:]
    if len(argname) == 0:
        return message.channel, 'Usage: !who [user]'
    elif len(argname) < 3:
        return message.channel,
        'You need to type more than 3 letters for the user!'
    else:
        for member in message.channel.server.members:
            if member.name.lower() == argname.lower():
                return (message.channel,
                        '```Name: {name}\nID: {id}\nStatus: {status}'
                        '\nGame Playing: {game}\nAvatar: '
                        '{avatar}\nJoined on: {month}/{day}/{year}```'
                        .format(name=member.name, id=member.id,
                                status=member.status,
                                game=member.game,
                                avatar=member.avatar_url,
                                month=str(member.joined_at.month),
                                day=str(member.joined_at.day),
                                year=str(member.joined_at.year)))

        for member in message.channel.server.members:
            if member.name.lower().startswith(argname.lower()):
                return (message.channel,
                        '```Name: {name}\nStatus: {status}'
                        '\nGame Playing: {game}'
                        '\nJoined on: {month}/{day}/{year}```'
                        .format(name=member.name,
                                status=member.status,
                                game=member.game,
                                month=member.joined_at.month,
                                day=member.joined_at.day,
                                year=member.joined_at.year))
    return (message.channel, 'User not found.')


##################
# Debug Commands #
##################

@display
def debug(message):
    argname = message.content[7:]

    if checkdev(message):
        try:
            exec(argname)
        except SyntaxError as err:
            return (message.channel, ("```{}```".format(err)))


@display
def execute(message):
    argname = message.content[6:]

    if checkdev(message):
        try:
            exec(argname)
        except SyntaxError as err:
            return (message.channel, ("```{}```".format(err)))


@display
def evaluate(message):
    argname = message.content[6:]

    if checkdev(message):
        try:
            return (message.channel, ("```{}```".format(eval(argname))))
        except SyntaxError as err:
            return (message.channel, ("```{}```".format(err)))


##################
# Music Commands #
##################


async def join(message):
    """ Joins a voice channel"""
    channel = message.content[6:]
    global voiceclient

    voice_channel = find(lambda c: c.name.startswith(channel), message.server.channels)
    if voice_channel.type is discord.ChannelType.text:
        return
    try:
        if not voiceclient == 0:
            await voiceclient.disconnect()
        voiceclient = await client.join_voice_channel(voice_channel)
    except InvalidArgument:
        print("Tried to join an invalid channel.")
    except asyncio.TimeoutError:
        print("Timed out.")
    except ClientException:
        print("Already joined a voice channel.")
    except OpusNotLoaded:
        print("Opus is not loaded.")


async def disconnect():
    global voiceclient
    global voiceclient_player
    if voiceclient == 0:
        return
    voiceclient_player.stop()
    await voiceclient.disconnect()
    voiceclient = 0


def next():
    '''Next Song'''


def skip():
    '''Stop the current playing song, and Start the next'''


def stop():
    global voiceclient_player
    if voiceclient_player:
        voiceclient_player.stop()


async def yt(message):
    global voiceclient
    global voiceclient_player
    if client.is_voice_connected() is False:
        return
    if not voiceclient_player == 0:
        if voiceclient_player.is_playing() is True:
            return
    link = message.content[4:]
    if not link.startswith("http"):
        return
    ydl_opts = {
        'noplaylist': True
    }
    try:
        voiceclient_player = await voiceclient.create_ytdl_player(link, options=ydl_opts, after=next())
        voiceclient_player.start()
    except Exception as e:
        print("Something went wrong with yt player")
        print(e)

################
# Fun Commands #
################


@display
def roll(message):
    num = 6
    arg = message.content[6:]

    def isinteger(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    if isinteger(arg):
        num = int(arg)

    x = random.randint(1, num)
    return (message.channel,
            '{} rolled a {}!'.format(message.author.mention, x))


async def invite(message):
    # TODO: join a server by invite. Need to make IGNORE list first
    website = message.content[8:]
    if not checkdev:
        return
    try:
        await client.accept_invite(website)
    except InvalidArgument:
        return (message.channel, 'This is an invalid invite!')
    except HTTPException:
        print('HTTPException!')

#################
# Riot Commands #
#################


def lookup(message):
    argname = message.content[8:]

    @display
    def worker():
        try:
            summoner = riotapi.get_summoner_by_name(argname)
            return (message.channel,
                    "Name: {name}\nLevel: {level}\nRank: {rank}"
                    .format(name=summoner.name,
                            level=summoner.level,
                            rank=summoner.leagues()[0]))
        except type.api.exception.APIError as e:
            return (message.channel, 'Lookup Failed.\nError: ' +
                    str(e.error_code))

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


######################
# Wikipedia Commands #
######################

def wiki(message):
    argname = message.content[6:]

    @display
    def worker():
        try:
            wikipage = wikipedia.page(argname)
            return (message.channel, wikipage.url)
        except wikipedia.exceptions.DisambiguationError:
            return (message.channel, 'Too Ambiguous.')
        except wikipedia.exceptions.HTTPTimeoutError:
            return (message.channel, 'Wikipedia Timed Out.')
        except wikipedia.exceptions.PageError:
            return (message.channel, 'There is no match.')
        except wikipedia.exceptions.RedirectError:
            return (message.channel, 'Redirect Error, Check Console.')
        except wikipedia.exceptions.WikipediaException:
            return (message.channel, 'Something Wrong with wikipedia.')

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


@client.event
async def on_message(message):
    if checkignorelist(message) and not checkdev(message):
        return

    if message.content.startswith('!bot'):
        await bot(message)
    ##################
    # Admin Commands #
    ##################
    elif message.content.startswith('!debug'):
        await debug(message)

    elif message.content.startswith('!eval'):
        await evaluate(message)

    elif message.content.startswith('!ignoreserver'):
        await ignoreserver(message)

    elif message.content.startswith('!ignorechannel'):
        await ignorechannel(message)

    elif message.content.startswith('!ignoreuser'):
        await ignoreuser(message)

    elif message.content.startswith('!avatar'):
        await avatar(message)

    elif message.content.startswith('!join'):
        await join(message)

    elif message.content.startswith('!invite'):
        await invite(message)

    elif message.content.startswith('!cinfo'):
        await cinfo(message)

    elif message.content.startswith('!help'):
        await helpmsg(message)

    elif message.content.startswith('Hello {}'.format(client.user.mention)):
        await hello(message)

    elif message.content.startswith('!listmusic'):
        await listmusic(message)

    elif message.content.startswith('!lookup'):
        await lookup(message)

    elif message.content.startswith('!play'):
        play(message)

    elif message.content.startswith('!disconnect'):
        disconnect()

    elif message.content.startswith('!yt'):
        await yt(message)

    elif message.content.startswith('!stop'):
        stop()

    elif message.content.startswith('!roll'):
        await roll(message)

    elif message.content.startswith('!uptime'):
        await uptime(message)

    elif message.content.startswith('!who'):
        await who(message)

    elif message.content.startswith('!wiki'):
        await wiki(message)

    elif message.content.startswith('#TeamOnodera'):
        client.send_message(message.channel, 'Fk off.')

    elif message.content.startswith('#TeamChitoge'):
        client.send_message(message.channel,
                            'Chitoge is so cute isn\'t she :D')

    elif message.content.startswith('#Tsunderes4Life'):
        client.send_message(message.channel, 'I like the way you think.')

#    elif message.content.startswith('{}'.format(client.user.mention)):
#        client.send_message(message.channel, 'You have mentioned me.')


def checkignorelistevent(chan):
    # checkignorelist given a channel.

    for serverid in ignore["servers"]:
        if serverid == chan.server.id:
            return True

    for channelid in ignore["channels"]:
        if channelid == chan.id:
            return True


@client.async_event
def on_member_join(member):
    channel = find(lambda chan: chan.name == 'public-chat',
                   member.server.channels)
    if checkignorelistevent(channel) is True:
        return
    client.send_message(channel, 'Please welcome {} to the server!'
                        .format(member.mention))


@client.async_event
def on_member_remove(member):
    channel = find(lambda chan: chan.name == 'public-chat',
                   member.server.channels)
    if checkignorelistevent(channel) is True:
        return
    client.send_message(channel, '{} has left the server.'
                        .format(member))


@client.async_event
def on_ready():
    global username
    global password
    username = None
    password = None

    print('Logged in as')
    print("Username " + client.user.name)
    print("ID: " + client.user.id)

    discord.opus.load_opus("opus.dll")
    print("Loaded Opus Library")

upTime = time.clock()
client.run(username, password)
