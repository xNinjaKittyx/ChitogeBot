import BakaBot.Bot


def display(func):
    """ Displays the message returned by a function """
    async def inner(*args, **kwargs):
        channel, message = func(*args, **kwargs)
        await Bot.client.send_message(channel, message)
        return
    return inner


def logmsg(func):
    """Logs the function used to the console"""
    def inner(message):
        print('Function: {0} was used by {1}'.format(func, message.author))
        return
    return inner
