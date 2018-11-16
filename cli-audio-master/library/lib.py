import sys
from exception import error as err
import os

class library:
    def __init__(self, media_folder):
        self.library = ['media/' + song for song in os.listdir(media_folder) if song.endswith('.wav')]
        
        self.playlists = {}

    def list_library(self):
        rtn_str = "Library:\n"
        for song in self.library:
            rtn_str = rtn_str + '\t' + song + '\n'
        rtn_str = rtn_str + "Playlists:\n"
        for name,plist in self.playlists.items():
            rtn_str = rtn_str + '\t' + name + '\n'
            for song in plist:
                rtn_str = rtn_str + '\t\t' + song + '\n'
        return rtn_str
    
    def add(self, song):
        self.library.append(song)

    def get_song(self, index):
        return self.library[index]
    
    def add_playlist(self, name):
        self.playlists[name] = list()

    def put_in_playlist(self, playlist, song):
        self.playlists[playlist].append(song)

    def get_playlists(self):
        return self.playlists

    def get_playlist(self, playlist):
        return self.playlists[playlist]

    def is_in(self, song):
        return song in self.library
