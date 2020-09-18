from discord.ext import commands
from config import TOKEN, PREFIX
from discord import Game


INVITE_URL = '<https://discord.com/oauth2/authorize?client_id=749416423889043477&scope=bot&permissions=19456>'
bot = commands.AutoShardedBot(
    command_prefix=PREFIX,
    case_insensitive=True,
    help_command=None,
    activity=Game("waifus)))")
)
bot.load_extension('waifus')
bot.load_extension('jishaku')


@bot.command()
async def invite(ctx):
    await ctx.send(INVITE_URL)


bot.run(TOKEN)
