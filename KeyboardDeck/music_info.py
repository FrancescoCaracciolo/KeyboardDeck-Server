from threading import Thread
import time
import dbus
import platform

from sympy import false

class NowPlaying():
    def __init__(self) -> None:
        self.supported = ["Linux"]
        self.os = platform.system()
        self.listener_running = False
        
    
    def is_supported(self) -> bool:
        """Checks if now playing is supported on current OS

        Returns:
            bool: true if is supported, false otherwise
        """
        if self.os in self.supported:
            return True
        return False

    def get_playing(self) -> dict:
        """Automatically detect OS and get current song playing, returns None if unsupported

        Returns:
            dict: song information
        """
        if (self.os == "Linux"):
            return self.get_playing_linux()
        return None

    def get_playing_linux(self) -> dict:
        """Get current song playing on linux using dbus

        Returns:
            dict: information about the song
        """
        try:
            bus = dbus.SessionBus()
            for service in bus.list_names():
                if service.startswith('org.mpris.MediaPlayer2.'):
                    player = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')

                    status=player.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus', dbus_interface='org.freedesktop.DBus.Properties')
                    metadata = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata', dbus_interface='org.freedesktop.DBus.Properties')
                    artist = metadata.get("xesam:artist")[0]
                    songtitle = metadata.get("xesam:title")
                    result = {'title': songtitle, 'artist': artist}
                    return result
        except Exception as e:
            return None
    
    def music_listener(self, onchange: callable, interval: int = 1):
        """Starts music listener on current thread

        Args:
            onchange (callable): function to call on music change, a dict with song information is passed
            interval (int, optional): Interval to check for music change. Defaults to 1.
        """
        self.stop = False
        if not self.is_supported:
            return None
        current = {"title": "", "artist": ""}
        while not self.stop:
            edited = False
            song = self.get_playing()
            for x in song:
                if (x in current and song[x] != current[x]) or x not in current:
                    current[x] = song[x]
                    edited = True
            if edited:
                onchange(current)
            time.sleep(interval)
    
    def music_listener_th(self, onchange: callable, interval: int = 1):
        """Starts music listener on another thread

        Args:
            onchange (callable): function to call on music change, a dict with song information is passed
            interval (int, optional): Interval to check for music change. Defaults to 1.
        """
        self.listener_running = True
        self.thread = Thread(target= self.music_listener, args=(onchange, interval))
        self.thread.start()
    
    def stop_listener(self):
        """Stops music listener on another thread"""
        self.stop = True
        if self.listener_running == True:
            self.thread.join()
            self.stop = False
            self.listener_running = False
    