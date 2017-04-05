import discord
from time import strftime

def newembed(a, t=None, d=None, u=None, c=0xC154F5):
    author = a.name + '#' + a.discriminator
    em = discord.Embed(title=t, description=d, url=u, colour=c)
    em.set_author(name=author, icon_url=a.avatar_url)
    em.set_footer(text="Powered by NinjaKitty | " + strftime('%a %b %d, %Y at %I:%M %p'), icon_url="https://my.mixtape.moe/jhbhte.png")

    return em
