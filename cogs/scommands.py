import sys
sys.path.append('../')

from utils.sfunctions import Spotify
from utils.functions import quote
import discord
from discord.commands import Option
from discord.ext import commands


class SpotifyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    spotify_cmd = discord.SlashCommandGroup("spotify", "Various Spotify Commands")
    spotify_search = spotify_cmd.create_subgroup("search", "Various Spotify Search Commands")

    @commands.Cog.listener()
    async def on_ready(self):
        print("[ COG ] SpotifyCommands is set")
    

    @spotify_cmd.command(name="listening")
    async def spotify_listening(
            self,
            inter: discord.Interaction,
            user: Option(discord.Member, default=None),
            simple: Option(bool, default=False)
    ):
        user: discord.Member = user or inter.user
        spotify = Spotify(user)
        view = discord.ui.View()

        if (spotify.isListening()):
            e = spotify.baseEmbed(user)
            e.add_field(name="Title", value=quote(spotify.getTitle()), inline=False)
            e.add_field(name="Album", value=quote(spotify.getAlbum()), inline=False)
            e.add_field(name="Artists", value=quote(spotify.getArtists()), inline=False)
            e.set_thumbnail(url=spotify.getCoverURL())
            e.set_footer(text=f"Time: {spotify.getTime()} | ID: {spotify.getID()}")
            view = spotify.Details(spotify.getID())
        else:
            e = discord.Embed(description="%s This user isn't listening the Spotify!" % (user.mention), color=0xff0000)

        await inter.response.send_message(embeds=[e], view=view)


def setup(bot: commands.Bot):
    return bot.add_cog(SpotifyCommands(bot))
