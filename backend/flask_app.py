from flask import Flask,render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'JdeEVd0uzGzjRxTC$DM2LKy!'

import logging
logging.basicConfig(filename='anime-backend.log', encoding='utf-8', level=logging.DEBUG)

#websocket
from flask_socketio import SocketIO, emit
socketio = SocketIO(app,cors_allowed_origins='*',async_mode="threading")

#import CPU Thread from thread.py
from thread import AnimeThread

#Websocket old Way
@app.route('/old/')
def index():
    return render_template('index.html')

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

    
