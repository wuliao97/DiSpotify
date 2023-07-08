import discord
import spotipy
from dateutil import parser
import urllib

from config import spotify_green, spotify_client, spotify_secret
from spotipy.oauth2 import SpotifyClientCredentials
from utils.functions import toURL


class Spotify:
    def __init__(self, user: discord.Member, query: str = None):
        self.user = user
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(client_id=spotify_client, client_secret=spotify_secret))
        self.spotify_activity = self.extract()
        self.spotify_obj = None
        self.urls = []
        self.query = query
        self.base_search_url = "https://open.spotify.com/search/"

    class Details(discord.ui.View):
        def __init__(self, track_id, timeout=180):
            super().__init__(timeout=timeout, disable_on_timeout=False)
        
        



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
