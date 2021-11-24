from anime_cli.anime import Anime
from anime_cli.search import SearchApi
from anime_cli.proxy_server import proxyServer
from anime_cli.search.gogoanime import GogoAnime
import json

STREAMS_FILE = "/home/stefan/develop/anime/backend/stream.json"

class MyAnime(Anime):
    def __init__(self, anime):
        self.id = anime.id
        self.title = anime.title
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class AnimeSearch():
    def __init__(self):
        self.searchApi = GogoAnime(mirror="pe")
        self.anime = None
        self.serverAddress = ("0.0.0.0", 8081)

    def run_server(self,searchApi, serverAddress):
        """Run server function creates a server for the searchApi and runs it
        Args:
            searchApi: The api to create the proxy server for
            serverAddress: The server address to bind the server to
        """
        server = proxyServer(searchApi.get_headers(), serverAddress)
        server.serve_forever()
        server.server_close()

    def search_animes(self,keyword):
        """
        query keyword through searchApi 
        return list of Anime
        """
        return self.searchApi.search_anime(keyword)

    def get_episodes_count(self,anime):
        """
        get episodes count
        return int
        """
        return self.searchApi.get_episodes_count(anime)
    
    def get_video_url(self,anime,episode):
        """
        get video stream url m3u8 from Anime
        return url
        """
        embed_url = self.searchApi.get_embed_video(anime,episode)
        return self.searchApi.get_video_url(embed_url)
    
    def set_video_url(self,video_url,device):
        """
        set video url in streams.json
        """
        streams = None
        with open(STREAMS_FILE,'r') as jfile:
            streams = json.load(jfile)

        video_url = f"http://jarvis.steinanet.at:{self.serverAddress[1]}/{video_url}"
        streams.update({device:video_url})

        with open(STREAMS_FILE,'w') as jfile:
            json.dump(streams, jfile)

        return True

if (__name__ == "__main__"):
    attack = AnimeSearch()
    animes = attack.search_animes("attack on titan")
    video_url = attack.get_video_url(animes[2],9)
    attack.set_video_url(video_url, "living_room_tv")