from flask import Flask,render_template
from flask import request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'JdeEVd0uzGzjRxTC$DM2LKy!'

import logging
logging.basicConfig(filename='anime-backend.log', encoding='utf-8', level=logging.DEBUG)

#websocket
from flask_socketio import SocketIO, emit
socketio = SocketIO(app,cors_allowed_origins='*',async_mode="threading")

#import CPU Thread from thread.py
from thread import AnimeThread

from anime_search import MyAnime, AnimeSearch,Anime
import json
import threading

#start reverse proxy for setting headers
anime = AnimeSearch()
print(f"Starting proxy server on {anime.serverAddress}")
server = threading.Thread(
    target=anime.run_server,
    args=(
        anime.searchApi,
        anime.serverAddress,
    ),
    daemon=True,
)
server.start()
    

#Websocket old Way
@app.route('/old/')
def index():
    return render_template('index.html')


#Anime-Search API
@app.route("/api/", methods=['GET'])
def search():
    keyword = request.args.get("search")
    print(keyword)
    animes = anime.search_animes(keyword)
    myanimes = [json.loads(MyAnime(anime).toJSON()) for anime in animes]
    return jsonify(myanimes)

@app.route("/api/<anime_id>/",methods=['GET'])
def get_episodes_count(anime_id):
    dummy = Anime(anime_id, anime_id)
    return jsonify(anime.get_episodes_count(dummy))

@app.route("/api/<anime_id>/<episode>/",methods=['GET'])
def set_video_url(anime_id,episode):
    dummy = Anime(anime_id, anime_id)
    video_url = anime.get_video_url(dummy, episode)
    
    device = request.args.get("device")
    if not device:
        return "Device get var needed"
    else:
        if (anime.set_video_url(video_url, device)):
            return "Anime set on " + device

# Anime Websocket for clients
@socketio.on('connect', namespace='/anime')
def test_connect():
    logging.debug("Connected with socket.io")
    thread = AnimeThread(socketio=socketio,namespace='/anime')
    thread.start()

@socketio.on('disconnect', namespace='/anime')
def test_disconnect():
    logging.debug("Client disconnected")

if __name__ == "__main__":
   
    import eventlet
    eventlet.monkey_patch()

    socketio.run(app)


