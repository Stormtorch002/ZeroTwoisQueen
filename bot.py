from discord.ext import commands, tasks
from config import TOKEN
from discord import Colour, Embed
from random import choice
from aiohttp import ClientSession


SUB_URL = 'https://reddit.com/r/zerotwo.json'
bot = commands.AutoShardedBot(
    command_prefix='*',
    case_insensitive=True,
    help_command=None
)
bot.image_data = []


@tasks.loop(minutes=1)
async def update_images():
    async with ClientSession() as request:
        async with request.get(SUB_URL) as response:
            data = await response.json()
    data = data['data']['children']
    bot.image_data = data


def get_image():
    while True:
        post = choice(bot.image_data)['data']
        if not post['over_18'] and not post['pinned']:
            break
    image_url = post['url_overridden_by_dest']
    embed = Embed(
        title=post['title'],
        color=Colour.magenta(),
        url='https://reddit.com/' + post['permalink']
    )
    embed.set_image(url=image_url)
    embed.set_footer(text='u/' + post['author'])
    return embed


@bot.command(aliases=['02', 'zerotwo'])
async def zt(ctx):
    await ctx.send(embed=get_image())


update_images.start()
bot.run(TOKEN)
