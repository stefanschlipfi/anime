from anime_cli.anime import Anime
from anime_cli.search import SearchApi
from anime_cli.search.gogoanime import GogoAnime
import json

class MyAnime(Anime):
    def __init__(self, anime: Anime):
        self.id = anime.id
        self.title = anime.title
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class AnimeSearch():
    def __init__(self):
        self.searchApi = GogoAnime(mirror="pe")
        self.anime = None

    def search_animes(self,keyword: str) -> list:
        """
        query keyword through searchApi 
        return list of Anime
        """
        return self.searchApi.search_anime(keyword)

    def get_episodes_count(self,anime: Anime) -> int:
        """
        get episodes count
        return int
        """
        return self.searchApi.get_episodes_count(anime)
    
    def get_video_url(self,anime: Anime,episode: int) -> str:
        """
        get video stream url m3u8 from Anime
        return url
        """
        embed_url = self.searchApi.get_embed_video(anime,episode)
        return self.searchApi.get_video_url(embed_url)
    
    def set_video_url(self,video_url: str,device: str):
        """
        set video url in streams.json
        """
        filename = "/home/stefan/develop/anime/backend/stream.json"
        streams = None
        with open(filename,'r') as jfile:
            streams = json.load(jfile)

        streams.update({device:video_url})

        with open(filename,'w') as jfile:
            json.dump(streams, jfile)

        return True

if (__name__ == "__main__"):
    attack = AnimeSearch()
    animes = attack.search_animes("attack on titan")
    video_url = attack.get_video_url(animes[2],9)
    attack.set_video_url(video_url, "living_room_tv")