from discord.ext import commands
from config import TOKEN
from discord import Colour, Embed, Game
from random import choice
from aiohttp import ClientSession
from time import time


SUB_URLS = [
    'https://reddit.com/r/ZeroTwo.json?limit=420',
    'https://reddit.com/r/MikuNakano.json?limit=420',
    'https://reddit.com/r/CHIKA.json?limit=420',
    'https://reddit.com/r/Hayasaka.json?limit=420',
    'https://reddit.com/r/Mami.json?limit=420'
]
INVITE_URL = '<https://discord.com/oauth2/authorize?client_id=749416423889043477&scope=bot&permissions=19456>'
GITHUB_URL = 'https://github.com/Stormtorch002/ZeroTwoisQueen'
bot = commands.AutoShardedBot(
    command_prefix='*',
    case_insensitive=True,
    help_command=None,
    activity=Game("with new waifus! *chika, *miku, *hayasaka, *mami")
)
bot.image_data = {}
bot.last_updates = {url: 0 for url in SUB_URLS}


async def update_images(url):
    async with ClientSession() as request:
        async with request.get(url) as response:
            data = await response.json()
            data = data['data']['children']
            bot.image_data[url] = data


async def get_image(ctx, sub_url):
    if bot.last_updates[sub_url] + 3600 < time():
        await update_images(sub_url)
        bot.last_updates[sub_url] = time()
    while True:
        post = choice(bot.image_data[sub_url])['data']
        if not (post['over_18'] and ctx.guild.id != 728371976690728961) and not post['pinned'] and \
                post.get('url_overridden_by_dest') and not post['is_video']:
            break

    image_url = post['url_overridden_by_dest']
    embed = Embed(
        title=post['title'],
        color=Colour.magenta(),
        url='https://reddit.com' + post['permalink']
    )
    embed.set_image(url=image_url)
    embed.set_footer(text='u/' + post['author'])
    return embed


@bot.command(aliases=['02', 'zerotwo'])
async def zt(ctx):
    await ctx.send(embed=await get_image(ctx, SUB_URLS[0]))


@bot.command()
async def miku(ctx):
    await ctx.send(embed=await get_image(ctx, SUB_URLS[1]))


@bot.command()
async def chika(ctx):
    await ctx.send(embed=await get_image(ctx, SUB_URLS[2]))


@bot.command(aliases=['hayasaka'])
async def ai(ctx):
    await ctx.send(embed=await get_image(ctx, SUB_URLS[3]))


@bot.command()
async def mami(ctx):
    await ctx.send(embed=await get_image(ctx, SUB_URLS[4]))


@bot.command()
async def invite(ctx):
    await ctx.send(INVITE_URL)


@bot.command()
async def github(ctx):
    await ctx.send(GITHUB_URL)


bot.run(TOKEN)
