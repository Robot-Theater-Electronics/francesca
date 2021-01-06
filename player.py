""" 
The player class for Francesca Woodman. Plays and stops wav files. That's it.
"""            
import simpleaudio as sa 
import time

class Player():
    """Class to play the audio files and store references to the playing stream"""
    
    def __init__(self, hostname, config):
        self._playobj = None
        self._name = hostname
        self._config = config
        self._currentComm = -1
        
        
    def play(self, radio, num, debug=False):
        """Play a music file by mapping the incomming command to a music file as defined in the config.ini"""
        if self._config['radios'].get(str(radio)) == self._name:
            if self._currentComm != num:
                self._currentComm = num
                sound = sa.WaveObject.from_wave_file("music_files/" + self._config['midi_to_music'].get(str(num)) )
                self._playobj = sound.play()
                if debug:
                    print('playing', radio, num)
                #self._playobj.wait_done()
            else:
                if debug:
                    print('stop', radio, num)
                self._currentComm = -1
                self._playobj.stop()