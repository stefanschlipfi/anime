from threading import Thread
from time import sleep
import json

class AnimeThread(Thread):
    def __init__(self,socketio,namespace):
        self.delay = 5
        self.socketio = socketio
        self.namespace = namespace
        self.streams = None
        super().__init__()

    def load_stream(self,filename = "/home/stefan/develop/anime/backend/stream.json") -> dict:
        job = None
        with open(filename,'r') as jfile:
            job = json.load(jfile)
        return job

    def get_streams(self):
        """
        Get temperature from sensor.py
        """
        #print("Entered infinity loop, delay: {}".format(self.delay))

        while True:
            dummy = self.load_stream();

            if not self.streams or not self.streams == dummy:
                self.streams = dummy
                self.socketio.emit('streams',self.streams,namespace = self.namespace)
            sleep(self.delay)

    def run(self):
        self.get_streams()
