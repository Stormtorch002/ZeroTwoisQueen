from discord.ext import commands
from config import POSTGRES, PREFIX
from aiohttp import ClientSession
from time import time
import random
import asyncpg
import discord


class Waifus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.on_ready())
        self.query = 'SELECT sub_url FROM waifus WHERE name = $1'
        self.last_updates = {}
        self.image_data = {}

    async def on_ready(self):
        db = await asyncpg.create_pool(**POSTGRES)
        self.bot.db = db
        queries = [
            '''CREATE TABLE IF NOT EXISTS waifus (
                "id" SERIAL PRIMARY KEY,
                "name" VARCHAR(16),
                "sub_url" VARCHAR(64)
            )'''
        ]
        [await db.execute(query) for query in queries]

    async def update_images(self, url):
        async with ClientSession() as request:
            async with request.get(url) as response:
                data = await response.json()
                data = data['data']['children']
                self.image_data[url] = data

    async def get_image(self, guild, sub_url):
        if self.last_updates[sub_url] + 3600 < time():
            await self.update_images(sub_url)
            self.last_updates[sub_url] = time()
        while True:
            post = random.choice(self.image_data[sub_url])['data']
            if not (post['over_18'] and guild.id != 728371976690728961) and not post['pinned'] and \
                    post.get('url_overridden_by_dest') and not post['is_video']:
                break

        image_url = post['url_overridden_by_dest']
        embed = discord.Embed(
            title=post['title'],
            color=discord.Colour.magenta(),
            url='https://reddit.com' + post['permalink']
        )
        embed.set_image(url=image_url)
        embed.set_footer(text='u/' + post['author'])
        return embed

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.bot or not message.guild or not message.content.startswith(PREFIX):
            return
        waifu = message.content.lstrip('*').lower()
        waifu = await self.bot.db.fetchrow(self.query, waifu)
        if waifu:
            await message.channel.send(embed=await self.get_image(message.guild, waifu['sub_url']))
        else:
            await self.bot.process_commands(message)

    @commands.command()
    async def hentai(self, ctx):
        await ctx.send('https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.mp4')

    @commands.command()
    async def addwaifu(self, ctx, name, sub_name):
        url = f'https://reddit.com/r/{sub_name}.json?limit=420'
        await self.bot.db.execute(
            'INSERT INTO waifus (name, sub_url) VALUES ($1, $2)',
            name, url
        )
        await ctx.send(f'Added command `{name}` with subreddit {url}')


def setup(bot):
    bot.add_cog(Waifus(bot))
