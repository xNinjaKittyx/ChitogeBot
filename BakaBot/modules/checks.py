import discord


def checkdev(message):
    """Checks if the developer used the command. AKA ME"""
    if message.author.id == "82221891191844864":
        return True
    else:
        return False

def checkignorelist(message, ignore):
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
