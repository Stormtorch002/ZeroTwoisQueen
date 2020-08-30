from discord.ext import commands, tasks
from config import TOKEN
from discord import Colour, Embed, Game
from random import choice
from aiohttp import ClientSession


SUB_URL = 'https://reddit.com/r/zerotwo.json'
INVITE_URL = '<https://discord.com/oauth2/authorize?client_id=749416423889043477&scope=bot&permissions=19456&' \
             'redirect_uri=https%3A%2F%2Fgithub.com%2FStormtorch002%2FZeroTwoisQueen>'
bot = commands.AutoShardedBot(
    command_prefix='*',
    case_insensitive=True,
    help_command=None,
    activity=Game("github.com/Stormtorch002/ZeroTwoisqueen")
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


@bot.command()
async def invite(ctx):
    await ctx.send(INVITE_URL)
    

update_images.start()
bot.run(TOKEN)
