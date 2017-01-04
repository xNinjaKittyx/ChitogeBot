import asyncio
import random

import discord
from discord.ext import commands


class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='Ask the Bot to choose one')
    async def choose(self, *choices: str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))

    @commands.command(name='8ball')
    async def ball(self):
        """ Ask the 8Ball """
        answers = ['It is certain', 'It is decidedly so', 'Without a doubt',
                   'Yes, definitely', 'You may rely on it', 'As I see it, yes',
                   'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                   'Reply hazy try again', 'Ask again later',
                   'Better not tell you now', 'Cannot predict now',
                   'Concentrate and ask again', 'Don\'t count on it',
                   'My reply is no', 'My sources say no',
                   'Outlook not so good', 'Very doubtful']

        await self.bot.say(random.choice(answers))


    @commands.command(pass_context=True)
    async def avatar(self, ctx, *, name: str):
        """ Grabbing an avatar of a person """
        await self.bot.say(ctx.message.server.get_member_named(name).avatar_url)


    @commands.command()
    async def brainpower(self):
        """ ADRENALINE IS PUMPING """
        await self.bot.say("O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo " +
                           "AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-" +
                           " JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA")

def setup(bot):
    bot.add_cog(Fun(bot))
