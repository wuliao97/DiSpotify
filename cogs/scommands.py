import sys
sys.path.append('../')

from utils.sfunctions import Spotify, SpotifyPageView, Details
from utils.functions import quote, toURL
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
            e.add_field(name="by", value=quote(spotify.getArtists()), inline=False)
            e.add_field(name="on", value=quote(spotify.getAlbum()), inline=False)
            e.set_thumbnail(url=spotify.getCoverURL())
            e.set_footer(text=f"Time: {spotify.getTime()} | ID: {spotify.getID()}")
            view = Details(spotify.getID())
        else:
            e = discord.Embed(description="%s This user isn't listening the Spotify!" % (user.mention), color=0xff0000)

        await inter.response.send_message(embeds=[e], view=view)



    @spotify_cmd.command(name="track")
    async def spotify_listening_track(
            self,
            inter: discord.Interaction,
            user: Option(discord.Member, default=None),
    ):
        user: discord.Member = user or inter.user
        spotify = Spotify(user)

        if (spotify.isListening()):
            await inter.response.send_message(spotify.track_url + spotify.getID())
        else:
            e = discord.Embed(description="%s This user isn't listening the Spotify!" % (user.mention), color=0xff0000)
            await inter.response.send_message(embeds=[e])



    @spotify_search.command(name="multi")
    async def spotify_search_multi(
        self, 
        inter:discord.Interaction,
        query:Option(str, max_lenght=50),
        limit:Option(int, min_value=1, max_value=50, default=20)
    ):
        spotify = Spotify(inter.user)
        result = spotify.spotify.search(q=query, limit=limit)["tracks"]["items"]

        track_lists = ["%s - %s" % ((idx + 1), toURL("**" + track["name"] + "** by **" + track["artists"][0]["name"] + "**", track["external_urls"]["spotify"])) for idx, track in enumerate(result)]
        total_track = calc_result if (calc_result:=round(len(track_lists) / 10)) != 0 else 1
        embeds = []
        count = 0

        for idx, _ in enumerate(track_lists):
            count += 1
            embeds.append(
                discord.Embed(
                    description=f"Page **{idx + 1}**/**{total_track}**"
                )
                .add_field(name="", value="\n".join(track_lists[10 * (idx) : 10 * (idx + 1)]))
            )
            
            if count == 5:
                break
        
        view = SpotifyPageView(embeds, round(limit / 10), result)

        await inter.response.send_message(embeds=embeds[:1], view=view)



def setup(bot: commands.Bot):
    return bot.add_cog(SpotifyCommands(bot))
