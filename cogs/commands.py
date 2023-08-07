import discord
from discord.ext import commands

from utils.functions import *


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[ COG ] Commands is set")

    @commands.slash_command(name="about")
    async def about_this_bot(self, inter: discord.Interaction):
        e = discord.Embed(description="For all of Spotify Lover and my friends!")
        e.add_field(name="source", value=quote(toURL("GITHUB", "https://github.com/wuliao97/DiSpotify")))

        await inter.response.send_message(embeds=[e])
        


def setup(bot: commands.Bot):
    return bot.add_cog(Commands(bot))
