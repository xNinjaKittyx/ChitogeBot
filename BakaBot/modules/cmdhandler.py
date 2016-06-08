""" This will handle all commands.
This will lead the commandhandler to all
other commands in other modules.
"""
import BakaBot.Bot
import json
import BakaBot.modules.musicplayer


def updatejsonfile():
    """Update the json file"""
    with open('../json/ignore.json', 'w',) as outfile:
        json.dump(Bot.ignore, outfile, indent=4)


def checkdev(message):
    """Checks if the developer used the command. AKA ME"""
    if message.author.id == "82221891191844864":
        return True
    else:
        return False


def checkignorelist(message):
    """If on the list, return true; if not, return false."""
    for serverid in Bot.ignore["servers"]:
        if serverid == message.channel.server.id:
            return True

    for channelid in Bot.ignore["channels"]:
        if channelid == message.channel.id:
            return True

    for userid in Bot.ignore["users"]:
        if userid == message.author.id:
            return True

    return False


async def command(message):
    if checkignorelist(message) and not checkdev(message):
        return

    if not message.content.startswith('~'):
        return

    cmd = message.content[1:]

    if cmd.startswith('join'):
        musicplayer.join(message)

    f = open('../command.log', 'w')
    f.write('[' + str(message.timestamp) + '] ' + str(message.author.name) + '\
            used ' + cmd)
    updatejsonfile()
"""    if cmd.startswith('bot'):

    elif cmd.startswith('eval'):

    elif cmd.startswith('ignoreserver'):

    elif cmd.startswith('ignorechannel'):

    elif cmd.startswith('ignoreuser'):

    elif cmd.startswith('avatar'):

    elif cmd.startswith('join'):

    elif cmd.startswith('invite'):

    elif cmd.startswith('cinfo'):

    elif cmd.startswith('help'):

    elif cmd.startswith('listmusic'):

    elif cmd.startswith('lookup'):

    elif cmd.startswith('play'):

    elif cmd.startswith('disconnect'):

    elif cmd.startswith('yt'):

    elif cmd.startswith('stop'):

    elif cmd.startswith('roll'):

    elif cmd.startswith('uptime'):

    elif cmd.startswith('who'):

    elif cmd.startswith('wiki'):"""
