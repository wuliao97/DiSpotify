from config import TOKEN, COGS

import discord
from discord.ext import commands

bot = commands.Bot(
    intents=discord.Intents.all()
)


@bot.event
async def on_ready():
    print("[ BOT ] %s is ready" % bot.user)


if __name__ == "__main__":
    for cog in COGS:
        bot.load_extension(cog)

    bot.run(TOKEN)
