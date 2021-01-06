""" 
The player class for Francesca Woodman. Plays and stops wav files. That's it.
"""            
from pygame import mixer as m

m.init()

class Player():
    """Class to play the audio files and store references to the playing stream"""
    
    def __init__(self, hostname, config):
        self._playobj = None
        self._name = hostname
        self._config = config
        self._currentComm = -1
        
        
    def play(self, radio, num, debug=False):
        """Play a music file by mapping the incomming command to a music file as defined in the config.ini"""
        if self._config['radios'].get(str(radio)) == self._name or self._config['radios'].get(str(radio)) == 'all':
            if self._currentComm != num:
                self._currentComm = num
                m.music.load("music_files/" + self._config['midi_to_music'].get(str(num)) )
                m.music.play(fade_ms=self.config['client'].getint('fadein'))
                if debug:
                    print('playing', radio, num)
                #self._playobj.wait_done()
            else:
                if debug:
                    print('stop', radio, num)
                self._currentComm = -1
                m.music.fadeout(self._config['client'].getint('fadeout'))
            