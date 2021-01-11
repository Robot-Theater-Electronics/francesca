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
        
        
    def play(self, radio, num, extra_radios, debug=False):
        """Play a music file by mapping the incomming command to a music file as defined in the config.ini"""
        if int(num) == 127:
            self._currentComm = -1
            m.music.fadeout(self._config['client'].getint('fadeout'))            
        else:
            decoded = self.decodeMsg(radio, num, extra_radios)
    
            if self.conditionToPlay(decoded) or self._config['radios'].get(str(radio)) == 'all':
                
                if self._currentComm != num:
                    self._currentComm = num
                    if self._name in decoded['extra_radios']:
                        m.music.load("music_files/" + decoded['tracks'][
                            decoded['extra_radios'].index(self._name) % len(decoded['tracks'])
                        ])
                    else:
                        m.music.load("music_files/" + decoded['tracks'][0])
                    m.music.play()
                    if debug:
                        print('playing', radio, num)
                    #self._playobj.wait_done()
                else:
                    if debug:
                        print('stop', radio, num)
                    self._currentComm = -1
                    m.music.fadeout(self._config['client'].getint('fadeout'))
                
    
    def decodeMsg(self, chan, num, vel, debug=False):
        """decodes the incoming midi note on msg based on the ini file"""
        extra_radios = []
        radios = []
        tracks = []
        try:
            radios = [ x.strip() for x in self._config['radios'].get(str(chan)).split(',') ]
        except AttributeError:
            print(f'radio number: {chan} is not mapped in ini file')
            
        try:
            tracks = [ x.strip() for x in self._config['midi_to_music'].get(str(num)).split(',') ]
        except AttributeError:
            print(f'track number: {num} is not mapped in ini file')            
            
        if vel > 0:
            try:
                extra_radios = [ x.strip() for x in self._config['extra_radios'].get(str(vel)).split(',') ]
            except AttributeError:
                print(f'extra_radios number: {vel} is not mapped in ini file')
                
        return {"radios": radios, "tracks": tracks, "extra_radios": extra_radios}
        
        
    def conditionToPlay(self, decoded):
        """ see if the current radio meets the conditions to play"""
        if self._name in decoded['radios'] or self._name in decoded['extra_radios']:
            return True 
        else:
            return False
        
        