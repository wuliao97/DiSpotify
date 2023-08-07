from utils.functions import *
from utils.starrail.profile import ImageDrawing

import discord
from discord.commands import Option
from discord.ext import commands

from mihomo import Language, MihomoAPI
from mihomo.models.v1 import StarrailInfoParsedV1




class StarrailCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = MihomoAPI(Language.JP)

    starrail = discord.SlashCommandGroup("starrail", "various star rail command!")
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[ COG ] Commands is set")

    @starrail.command(name="profile")
    async def starrail_profile(
        self,
        inter:discord.Interaction,
        uid:Option(int)
    ):
        
        data:StarrailInfoParsedV1 = await self.client.fetch_user_v1(uid)
        var = ImageDrawing(data.characters, self.client)

        e = discord.Embed(description="test").set_image(url=self.client.get_icon_url(data.characters[0].light_cone.icon))
        
        await inter.response.send_message(embeds=[e])

def setup(bot: commands.Bot):
    return bot.add_cog(StarrailCommands(bot))
