import os

import aiohttp
from discord import Embed, Colour
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')

headers = {'Accept': 'application/json'}


async def fetch(session, endpoint):
    async with session.get('https://minecraftmapy.pl/api' + endpoint) as response:
        return await response.json()


@bot.command()
async def profil(ctx, username):
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await fetch(session, '/user/{}'.format(username))
    data = response['data']

    embed = Embed(
        title='[Profil] {}'.format(data['info']['username']),
        description=data['info']['description'],
        colour=Colour.from_rgb(0, 144, 255),
        url=data['url'],
    )

    info = """
    **Rola:** {}
    **Aktywny:** {}
    **Napisanych komentarzy:** {}
    **Oddanych diamentów:** {}
    """.format(data['info']['role'], data['info']['last_logged_relative'], data['stats']['written_comments'],
               data['stats']['given_diamonds'])

    embed.add_field(name='Informacje', value=info, inline=True)

    stats = """
    <:diax:589865302100017172> Diamenty: {}
    <:gwiazdka:589865302230040576> Obserwujących: {}
    <:mapa:589865302020456456> Wrzuconych map: {}
    """.format(data['stats']['diamond_sum'], data['stats']['follower_count'], data['stats']['map_count'])

    embed.add_field(name='Statystyki', value=stats, inline=True)

    embed.set_thumbnail(url=data['info']['avatar_url'])
    embed.set_footer(text='Invoked by {}#{} • {}'.format(ctx.author.name, ctx.author.discriminator, ctx.author.id),
                     icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


bot.run(TOKEN)
