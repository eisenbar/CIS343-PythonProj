import curses
import curses.textpad
import sys
from exception import error as err
from library.lib import library
import os

class FrontEnd:

    def __init__(self, player):
        self.player = player

        """
        Invalid amount of arguments exception
        Calls CLI_Audio_Exception if there is an incorrect amount of arguments
        """
        if len(sys.argv) != 2:
           raise err.CLI_Audio_Exception('Incorrect number of arguments yo!')

        self.player.play(sys.argv[1])
        self.library = library('./media')
        curses.wrapper(self.menu)

    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(8,10, "a - Add song")
        self.stdscr.addstr(9,10, "n - New Playlist")
        self.stdscr.addstr(10,10, "r - Put Song in Playlist")
        self.stdscr.addstr(12,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                # COULDNT FIND UPDATED SONG
                # Throws CLI_Audio_File_Exception if the song could not be changed or updated
                try:
                    self.changeSong()
                    self.updateSong()
                except err.CLI_Audio_File_Exception:
                    self.stdscr.addstr(15,10,'                                   ')
                    self.stdscr.addstr(15,10,'Could not change songs')
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('l'):
                self.stdscr.addstr(16,10, "\n" + self.library.list_library())
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('a'):
                try:
                    self.addSong()
                except err.CLI_Audio_File_Exception:
                    self.stdscr.addstr(15,10,"                                 ")
                    self.stdscr.addstr(15,10,"Could not add song")
                    self.stdscr.touchwin()
                    self.stdscr.refresh()
            elif c == ord('n'):
                self.createPlaylist()
            elif c == ord('r'):
                try:
                    self.putInPlaylist()
                except err.CLI_Audio_File_Exception:
                    self.stdscr.addstr(15,10,"                               ")
                    self.stdscr.addstr(15,10,"Invalid name")
                    self.stdscr.touchwin()
                    self.stdscr.refresh()
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    """
    Changes song to new song
    @param self
    """
    def changeSong(self):
       

        #try to create new window
        #throws CLI_Audio_Screen_Size_Exception
        try:
             changeWindow = curses.newwin(5, 40, 5, 50)
             changeWindow.border()
             changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
             self.stdscr.refresh()
             curses.echo()
             path = changeWindow.getstr(1,1, 30)
             curses.noecho()
             del changeWindow
        except CLI_Audio_Screen_Size_Exception:
             print('invalid screen size)
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()

        #If the song does not exist raises CLI_Audio_File_Exception
        if not self.library.is_in(path.decode(encoding="utf-8")):
            raise err.CLI_Audio_File_Exception
        self.player.play(path.decode(encoding="utf-8"))
        

    def quit(self):
        self.player.stop()
        exit()
    """
    Creates a new window and adds a song with a given file path
    @param self
    """
    def addSong(self):
        addWindow = curses.newwin(5,40,5,50)
        addWindow.border()
        addWindow.addstr(0,0,"What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        song = addWindow.getstr(1,1,30)
        curses.noecho()
        del addWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

        #if the song does not exist or is not a .wav file, raises CLI_Audio_File_Exception
        if os.path.isfile(song) and song.decode(encoding='utf-8').endswith('.wav'):
            self.library.add(song.decode(encoding='utf-8'))
        else:
            raise err.CLI_Audio_File_Exception
    """
    Creates a new playlist for the user to add songs too. Calls putInPlaylist to add the song
    @param self
    """
    def createPlaylist(self):
        playlistWindow = curses.newwin(5,40,5,50)
        playlistWindow.border()
        playlistWindow.addstr(0,0,"What is the name of the playlist?",curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        playlist = playlistWindow.getstr(1,1,30)
        curses.noecho()
        del playlistWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.library.add_playlist(playlist.decode(encoding='utf-8'))
    """
    Puts a song in current playlist
    @param self
    """
    def putInPlaylist(self):
        playlistWindow = curses.newwin(5,40,5,50)
        playlistWindow.border()
        playlistWindow.addstr(0,0,"What is the name of the playlist?",curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        playlist = playlistWindow.getstr(1,1,30).decode(encoding='utf-8')
        curses.noecho()

        #raises CLI_Audio_File_Exception if playlist is not created
        if not playlist in self.library.get_playlists():
            raise err.CLI_Audio_File_Exception

        playlistWindow.touchwin()
        playlistWindow.refresh()
        playlistWindow.addstr(0,0,"                                    ",curses.A_REVERSE)
        playlistWindow.addstr(0,0,"What is the name of the song?",curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        song = playlistWindow.getstr(1,1,30).decode(encoding='utf-8')
        curses.noecho()
        del playlistWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

        #If the song does not exist ot it is not a .wav file, raises CLI_Audio_File_Exception
        if not self.library.is_in(song) or not song.endswith('.wav'):
            raise err.CLI_Audio_File_Exception
        self.library.put_in_playlist(playlist,song)
