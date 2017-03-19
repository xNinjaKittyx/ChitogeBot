
import asyncio
import discord
from discord.utils import find
import os
import json
from discord.ext import commands


class Ranks:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def weeb(self, ctx):
        """ Weeb is a lifestyle chosen once... Then stuck with you forever... """
        weeb = find(lambda r: r.name == "Weeb", ctx.message.server.roles)
        if weeb in ctx.message.author.roles:
            return
        if weeb is None:
            await self.bot.say(ctx.message.channel, "~weeb is broken. PLSFIX :LUL:")
            return
        normie = find(lambda r: r.name == "Normies", ctx.message.server.roles)
        await self.bot.add_roles(ctx.message.author, weeb)
        await self.bot.remove_roles(ctx.message.author, normie)

    @commands.command(pass_context=True, no_pm=True)
    async def normie(self, ctx):
        """ Get access to the server! """
        if len(ctx.message.author.roles) == 1:
            normie = find(lambda r: r.name == "Normies", ctx.message.server.roles)
            await self.bot.add_roles(ctx.message.author, normie)
            await self.bot.delete_message(ctx.message)
            await self.bot.send_message(ctx.message.server.default_channel, "Welcome {0} to the server!".format(ctx.message.author.mention))

    @commands.command(pass_context=True, no_pm=True)
    async def bdo(self, ctx):
        """ Access to BDO channel """
        bdo = find(lambda r: r.name == "BDO", ctx.message.server.roles)
        if bdo in ctx.message.author.roles:
            await self.bot.remove_roles(ctx.message.author, bdo)
        else:
            await self.bot.add_roles(ctx.message.author, bdo)

def setup(bot):
    bot.add_cog(Ranks(bot))
