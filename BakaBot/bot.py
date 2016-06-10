
import asyncio
import json
import logging
import random
import os

import discord
from discord.ext import commands
from discord.utils import find
import wikipedia
import modules.checks as checks
import praw
# import BakaBot.modules.decorators as decorators
# import cmdhandler as cmdhandler



__author__ = "Daniel Ahn"
__version__ = "0.6"
name = "BakaBot"

if not os.path.exists('../json'):
    os.makedirs('../json')

if not os.path.isfile('../json/ignore.json'):
    with open('../json/ignore.json', 'w',) as outfile:
        json.dump({"servers": [], "channels": [], "users": []},
                  outfile, indent=4)

with open('../json/ignore.json') as data_file:
    ignore = json.load(data_file)

logger = logging.getLogger('discord')
logger.setLevel(logging.CRITICAL)
handler = logging.FileHandler(filename='../discord.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: \
                                        %(name)s: %(message)s'))
logger.addHandler(handler)

random.seed()

r = praw.Reddit(user_agent='/u/firefwing24 using for discord. Private Bot displaying top 10 of subreddits on demand.')


description = '''An idiot Bot...'''
bot = commands.Bot(command_prefix='~', description=description)


# probably needs to have a different json file
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
    channel = find(lambda chan: chan.name == 'public-spam',
                   member.server.channels)
    if checkignorelistevent(channel) is True:
        return
    bot.say(channel, 'Please welcome {} to the server!'.format(member.mention))


@bot.event
async def on_member_remove(member):
    channel = find(lambda chan: chan.name == 'public-spam',
                   member.server.channels)
    if checkignorelistevent(channel) is True:
        return
    bot.say(channel, '{} has left the server.'.format(member))


@bot.event
async def on_ready():

    print('Logged in as')
    print("Username " + bot.user.name)
    print("ID: " + bot.user.id)
    if not discord.opus.is_loaded():
        discord.opus.load_opus("opus.dll")
    print("Loaded Opus Library")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not checks.checkdev(message) and checks.checkignorelist(message, ignore):
        return
    await bot.process_commands(message)


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command()
async def topreddit(subreddit: str):
    """ Grabs the top 10 of a given subreddit """
    sr = r.get_subreddit(subreddit)

    result = '\n'.join(str(submission) for submission in sr.get_top(limit=10))
    await bot.say(result)


@bot.command()
async def wiki(search: str):
    """ Grabs Wikipedia Article """
    wikipedia.summary(search, 3)

if __name__ == "__main__":
    bot.load_extension('modules.musicplayer')
    bot.load_extension('modules.mal')
    bot.run('MTg5OTM5NTI0NjY1NzM3MjE3.Cjke-Q.Kj4uv-WyUeNCxtZ7yokSb66TxhE')
# def checkPrivate(message):
#     """Checks if the message is a PM"""
#     if message.channel.is_private is True:
#         return True
#     else:
#         return False
#
#
# @cmdhandler.display
# def ignoreserver(message):
#     """Ignore the Discord Server"""
#     if not checkdev(message):
#         return
#     count = 0
#     for serverid in ignore["servers"]:
#         if serverid == message.channel.server.id:
#             ignore["servers"].pop(count)
#             updatejsonfile()
#
#         count += 1
#     ignore["servers"].append(message.channel.server.id)
#     updatejsonfile()
#     return message.channel, 'Server Ignored'
#
#
# @decorators.display(client)
# def ignorechannel(message):
#     """Ignore the Channel"""
#     if not checkdev(message):
#         return
#     count = 0
#     for channelid in ignore["channels"]:
#         if channelid == message.channel.id:
#             ignore["channels"].pop(count)
#
#             updatejsonfile()
#             return message.channel, 'Channel Unignored'
#         count += 1
#     ignore["channels"].append(message.channel.id)
#
#     updatejsonfile()
#     return message.channel, 'Channel Ignored'
#
#
# @decorators.display(client)
# def ignoreuser(message):
#     """Ignore a specific user"""
#     if not checkdev(message):
#         return
#     argname = message.content[12:]
#     member = find(lambda m: m.name == argname, message.server.members)
#     count = 0
#     for userid in ignore["users"]:
#         if userid == member.id:
#             ignore["users"].pop(count)
#
#             updatejsonfile()
#             return message.channel, 'I\'ll listen to ' + member.name
#         count += 1
#     ignore["users"].append(member.id)
#
#     updatejsonfile()
#     return message.channel, 'Alright, I\'ll ignore ' + member.name
#
#
#
#
#
# #################
# # Info Commands #
# #################
#
#
# @decorators.display(client)
# def avatar(message):
#     """ Returns the user's avatar """
#     user = message.content[8:]
#     member = find(lambda m: m.name == user, message.server.members)
#     if member:
#         return (message.channel, message.author.avatar_url)
#
#
# @decorators.display(client)
# def bot(message):
#     """Returns the bot's info"""
#     return (message.channel,
#             "Hi, I'm {0}. Version: {1}. I am using {2}"
#             .format(name, __version__, discord.__version__))
#
#
# @decorators.display(client)
# def cinfo(message):
#     """Returns the Channel's Info"""
#     if not message.channel.is_private:
#         return (message.channel, ("```Name: {0}\nID: {1}\nType: {2}```"
#                 .format(message.channel.name, message.channel.id,
#                         message.channel.type)))
#     else:
#         return (message.channel, ("```User: {0}\nID: {1}```"
#                 .format(message.channel.user, message.channel.id)))
#
#
# @decorators.display(client)
# def hello(message):
#     """Respond with a hello message"""
#     return message.channel, 'Hello {}-san!'.format(message.author.mention)
#
#
# @decorators.display(client)
# def helpmsg(message):
#     """Sends the Help Message"""
#     return (message.channel, ('HERES ALL THE COMMANDS {}-SAMA\n'
#                               '!help - Display this help message.\n'
#                               '!cinfo - Channel Information\n'
#                               '!who [user] - User Information\n'
#                               '!wiki [topic] - Look for a wiki page\n'
#                               '!listmusic - '
#                               'List all music files available on the bot\n\n'
#                               '!lookup [Summoner] - Find Summoner on LoL\n'
#                               '!next - Play the next song\n'
#                               '!pause - Pause the song\n'
#                               '!play [song] - Play a song\n'
#                               '!resume - Resume the player\n'
#                               '!stop - Stop the player - '
#                               'Currently not working\n'
#                               '!roll - Roll a die\n'
#                               '!uptime - Bot uptime\n'
#                               'More to Come!\n'
#                               'Check https://github.com/'
#                               'xNinjaKittyx/ChitogeBot\n'
#                               .format(message.author.mention)))
#
#
# @decorators.display(client)
# def uptime(message):
#     """Returns bot's Uptime"""
#     totalMin = 0
#     totalHr = 0
#     totalDay = 0
#
#     totalSec = int(time.clock() - upTime)
#     if totalSec > 60:
#         totalMin = int(totalSec / 60)
#         totalSec -= (totalMin * 60)
#     if totalMin > 60:
#         totalHr = int(totalMin / 60)
#         totalMin -= (totalHr * 60)
#     if totalHr > 24:
#         totalDay = int(totalHr / 24)
#         totalHr -= (totalDay * 24)
#     return (message.channel, ('ChitogeBot has been running for {} days, '
#                               '{} hours, {} minutes, and {} seconds '
#                               ).format(totalDay, totalHr, totalMin, totalSec))
#
#
# @decorators.display(client)
# def who(message):
#     """ Displays who someone is """
#     argname = message.content[5:]
#     if len(argname) == 0:
#         return message.channel, 'Usage: !who [user]'
#     elif len(argname) < 3:
#         return message.channel,
#         'You need to type more than 3 letters for the user!'
#     else:
#         for member in message.channel.server.members:
#             if member.name.lower() == argname.lower():
#                 return (message.channel,
#                         '```Name: {name}\nID: {id}\nStatus: {status}'
#                         '\nGame Playing: {game}\nAvatar: '
#                         '{avatar}\nJoined on: {month}/{day}/{year}```'
#                         .format(name=member.name, id=member.id,
#                                 status=str(member.status).capitalize(),
#                                 game=member.game,
#                                 avatar=member.avatar_url,
#                                 month=str(member.joined_at.month),
#                                 day=str(member.joined_at.day),
#                                 year=str(member.joined_at.year)))
#
#         for member in message.channel.server.members:
#             if member.name.lower().startswith(argname.lower()):
#                 return (message.channel,
#                         '```Name: {name}\nStatus: {status}'
#                         '\nGame Playing: {game}'
#                         '\nJoined on: {month}/{day}/{year}```'
#                         .format(name=member.name,
#                                 status=str(member.status).capitalize(),
#                                 game=member.game,
#                                 month=member.joined_at.month,
#                                 day=member.joined_at.day,
#                                 year=member.joined_at.year))
#     return (message.channel, 'User not found.')
#
#
# ##################
# # Debug Commands #
# ##################
#
# @decorators.display(client)
# def debug(message):
#     argname = message.content[7:]
#
#     if checkdev(message):
#         try:
#             exec(argname)
#         except SyntaxError as err:
#             return (message.channel, ("```{}```".format(err)))
#
#
# @decorators.display(client)
# def execute(message):
#     argname = message.content[6:]
#
#     if checkdev(message):
#         try:
#             exec(argname)
#         except SyntaxError as err:
#             return (message.channel, ("```{}```".format(err)))
#
#
# @decorators.display(client)
# def evaluate(message):
#     argname = message.content[6:]
#
#     if checkdev(message):
#         try:
#             return (message.channel, ("```{}```".format(eval(argname))))
#         except SyntaxError as err:
#             return (message.channel, ("```{}```".format(err)))
#
# ################
# # Fun Commands #
# ################
#
#
# @decorators.display(client)
# def roll(message):
#     num = 6
#     arg = message.content[6:]
#
#     def isinteger(value):
#         try:
#             int(value)
#             return True
#         except ValueError:
#             return False
#
#     if isinteger(arg):
#         num = int(arg)
#
#     x = random.randint(1, num)
#     return (message.channel,
#             '{} rolled a {}!'.format(message.author.mention, x))
#
#
# async def invite(message):
#     # TODO: join a server by invite. Need to make IGNORE list first
#     website = message.content[8:]
#     if not checkdev:
#         return
#     try:
#         await client.accept_invite(website)
#     except InvalidArgument:
#         return (message.channel, 'This is an invalid invite!')
#     except HTTPException:
#         print('HTTPException!')
#
# #################
# # Riot Commands #
# #################
#
#
# def lookup(message):
#     argname = message.content[8:]
#
#     @decorators.display(client)
#     def worker():
#         try:
#             summoner = riotapi.get_summoner_by_name(argname)
#             return (message.channel,
#                     "Name: {name}\nLevel: {level}\nRank: {rank}"
#                     .format(name=summoner.name,
#                             level=summoner.level,
#                             rank=summoner.leagues()[0]))
#         except type.api.exception.APIError as e:
#             return (message.channel, 'Lookup Failed.\nError: ' +
#                     str(e.error_code))
#
#     t = threading.Thread(target=worker)
#     t.daemon = True
#     t.start()
#
#
# ######################
# # Wikipedia Commands #
# ######################
#
# def wiki(message):
#     argname = message.content[6:]
#
#     @decorators.display(client)
#     def worker():
#         try:
#             wikipage = wikipedia.page(argname)
#             return (message.channel, wikipage.url)
#         except wikipedia.exceptions.DisambiguationError:
#             return (message.channel, 'Too Ambiguous.')
#         except wikipedia.exceptions.HTTPTimeoutError:
#             return (message.channel, 'Wikipedia Timed Out.')
#         except wikipedia.exceptions.PageError:
#             return (message.channel, 'There is no match.')
#         except wikipedia.exceptions.RedirectError:
#             return (message.channel, 'Redirect Error, Check Console.')
#         except wikipedia.exceptions.WikipediaException:
#             return (message.channel, 'Something Wrong with wikipedia.')
#
#     t = threading.Thread(target=worker)
#     t.daemon = True
#     t.start()



    # if message.content.startswith('!bot'):
    #     await bot(message)
    # ##################
    # # Admin Commands #
    # ##################
    # elif message.content.startswith('!eval'):
    #     await evaluate(message)
    #
    # elif message.content.startswith('!ignoreserver'):
    #     await ignoreserver(message)
    #
    # elif message.content.startswith('!ignorechannel'):
    #     await ignorechannel(message)
    #
    # elif message.content.startswith('!ignoreuser'):
    #     await ignoreuser(message)
    #
    # elif message.content.startswith('!avatar'):
    #     await avatar(message)
    #
    # elif message.content.startswith('!join'):
    #     await join(message)
    #
    # elif message.content.startswith('!invite'):
    #     await invite(message)
    #
    # elif message.content.startswith('!cinfo'):
    #     await cinfo(message)
    #
    # elif message.content.startswith('!help'):
    #     await helpmsg(message)
    #
    # elif message.content.startswith('Hello {}'.format(client.user.mention)):
    #     await hello(message)
    #
    # elif message.content.startswith('!listmusic'):
    #     await listmusic(message)
    #
    # elif message.content.startswith('!lookup'):
    #     await lookup(message)
    #
    # elif message.content.startswith('!play'):
    #     play(message)
    #
    # elif message.content.startswith('!disconnect'):
    #     disconnect()
    #
    # elif message.content.startswith('!yt'):
    #     await yt(message)
    #
    # elif message.content.startswith('!stop'):
    #     stop()
    #
    # elif message.content.startswith('!roll'):
    #     await roll(message)
    #
    # elif message.content.startswith('!uptime'):
    #     await uptime(message)
    #
    # elif message.content.startswith('!who'):
    #     await who(message)
    #
    # elif message.content.startswith('!wiki'):
    #     await wiki(message)
    #
    # elif message.content.startswith('#TeamOnodera'):
    #     client.send_message(message.channel, 'Fk off.')
    #
    # elif message.content.startswith('#TeamChitoge'):
    #     client.send_message(message.channel,
    #                         'Chitoge is so cute isn\'t she :D')
    #
    # elif message.content.startswith('#Tsunderes4Life'):
    #     client.send_message(message.channel, 'I like the way you think.')

#    elif message.content.startswith('{}'.format(client.user.mention)):
#        client.send_message(message.channel, 'You have mentioned me.')
