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
        return {
            'status': response.status,
            'json': await response.json(),
        }


@bot.command()
async def profil(ctx, username):
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await fetch(session, f'/user/{username}')

    if response['status'] != 200:
        await ctx.send('Nie znaleziono takiego użytkownika!')
        return

    data = response['json']['data']

    embed = Embed(
        title=f'[Profil] {data["info"]["username"]}',
        description=data['info']['description'],
        colour=Colour.from_rgb(0, 144, 255),
        url=data['url'],
    )

    info = f"""
    **Rola:** {data['info']['role']}
    **Aktywny:** {data['info']['last_logged_relative']}
    **Napisanych komentarzy:** {data['stats']['written_comments']}
    **Oddanych diamentów:** {data['stats']['given_diamonds']}
    """

    embed.add_field(name='Informacje', value=info, inline=True)

    stats = f"""
    <:diax:589865302100017172> Diamenty: {data['stats']['diamond_sum']}
    <:gwiazdka:589865302230040576> Obserwujących: {data['stats']['follower_count']}
    <:mapa:589865302020456456> Wrzuconych map: {data['stats']['map_count']}
    """

    embed.add_field(name='Statystyki', value=stats, inline=True)

    embed.set_thumbnail(url=data['info']['avatar_url'])
    embed.set_footer(text=f'Invoked by {ctx.author} • {ctx.author.id}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


bot.run(TOKEN)
