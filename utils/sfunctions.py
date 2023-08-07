import discord
from discord.ui.item import Item
import spotipy
from dateutil import parser
import urllib

from config import spotify_green, spotify_client, spotify_secret
from spotipy.oauth2 import SpotifyClientCredentials
from utils.functions import toURL


class Spotify:
    def __init__(
            self, 
            user: discord.Member = None, 
            track_id: str = None , 
            query: str = None
    ):
        self.user = user
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(client_id=spotify_client, client_secret=spotify_secret))
        self.spotify_activity = self.extract()
        self.spotify_obj = None
        self.urls = []
        self.query = query
        self.base_search_url = "https://open.spotify.com/search/"
        self.track_url = "https://open.spotify.com/track/"


    def extract(self):
        return next((activity for activity in self.user.activities if isinstance(activity, discord.Spotify)), None)

    def URLExtract(self, track_id):
        result = self.spotify.track(track_id)
        urls = [result['external_urls']['spotify'], result['album']['external_urls']['spotify'],
                [artist['external_urls']['spotify'] for artist in result['artists']]]
        return urls

    def isListening(self):
        if self.spotify_activity:
            self.urls = self.URLExtract(self.spotify_activity.track_id)
        return self.spotify_activity

    def baseEmbed(self, user:discord.Member = None):
        e = discord.Embed(color=spotify_green)
        if user:
            e.description = "%s is listening" % user.mention
        return e

    def getTitle(self):
        return toURL(self.spotify_activity.title, self.spotify_activity.track_url)

    def getAlbum(self):
        return toURL(self.spotify_activity.album, self.urls[1])

    def getArtists(self):
        return toURL(self.spotify_activity.artists, self.urls[2])

    def getCoverURL(self):
        return self.spotify_activity.album_cover_url

    def getTime(self):
        duration = self.spotify_activity.duration
        return parser.parse(str(duration)).strftime('%M:%S')

    def getFormattedArtists(self, symbol=", "):
        return symbol.join(self.getArtists())

    def getID(self):
        return self.spotify_activity.track_id

    def getThumbnail(self):
        return self.spotify_activity.album_cover_url

    def getActivity(self):
        return self.spotify_activity

    def search_url(self):
        return self.base_search_url + urllib.parser.quote(str(self.query))
    


    
class Details(discord.ui.View):
    def __init__(self, track_id, timeout=180):
        super().__init__(timeout=timeout, disable_on_timeout=False)
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client, client_secret=spotify_secret))
        
        
        self.track = self.spotify.track(track_id)

        self.album = self.spotify.album()
        self.artists = self.spotify.artists()
    




class SpotifyPageView(discord.ui.View):
    def __init__(self, embeds:list[discord.Embed], limit:int, timeout: float | None = 180, disable_on_timeout: bool = False):
        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.embeds = embeds
        self.limit = limit - 1
        self.current = 0
    
    @discord.ui.button(label="<<")
    async def rewind_button(self, button, inter:discord.Interaction):
        self.current = 0
        await inter.response.edit_message(embeds=[self.embeds[self.current]])

    @discord.ui.button(label="<")
    async def left_arrow_button(self, button, inter:discord.Interaction):
        self.current = current if (current:=self.current - 1) > 0 else self.current
        await inter.response.edit_message(embeds=[self.embeds[self.current]])

    @discord.ui.button(label=">")
    async def right_arrow_button(self, button, inter:discord.Interaction):
        self.current = current if ((self.limit) >= (current:=self.current + 1)) else self.current
        await inter.response.edit_message(embeds=[self.embeds[self.current]])

    @discord.ui.button(label=">>")
    async def fast_forward_button(self, button, inter:discord.Interaction):
        self.current = self.limit
        await inter.response.edit_message(embeds=[self.embeds[self.current]])

    
