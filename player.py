""" 
The player class for Francesca Woodman. Plays and stops wav files. That's it.
"""            
from pygame import mixer as m
import configparser

m.init()


class Player():
    """Class to play the audio files and store references to the playing stream"""
    
    def __init__(self, hostname):
        self._playobj = None
        self._name = hostname
        self._config = configparser.ConfigParser()
        self._currentComm = -1
        
        
    def play(self, radio, num, extra_radios, debug=False):
        """Play a music file by mapping the incomming command to a music file as defined in the config.ini"""
        self._config.read('config.ini')
        if int(num) == 127:
            self._currentComm = -1
            m.music.fadeout(self._config['client'].getint('fadeout'))            
        else:
            decoded = self.decodeMsg(radio, num, extra_radios, self._config)
    
            if self.conditionToPlay(decoded) or self._config['radios'].get(str(radio)) == 'all':
                
                if self._currentComm != num:
                    self._currentComm = num
                    if self._name in decoded['extra_radios']:
                        try:
                            track = decoded['tracks'][
                                decoded['extra_radios'].index(self._name) % len(decoded['tracks'])]
                            m.music.load("/media/mnt/" + track)
                        except:
                            print(f"music file {track} doesn't exists")
                    else:
                        try: 
                            track = decoded['tracks'][0]
                            m.music.load("/media/mnt/" + track)
                        except:
                            print(f"music file {track} doesn't exists")
                    try:
                        m.music.play()
                    except:
                        print("didn't play...")
                        
                    if debug:
                        print('playing', radio, num)
                    #self._playobj.wait_done()
                else:
                    if debug:
                        print('stop', radio, num)
                    self._currentComm = -1
                    m.music.fadeout(self._config['client'].getint('fadeout'))
                
    
    def decodeMsg(self, chan, num, vel, config, debug=False):
        """decodes the incoming midi note on msg based on the ini file"""
        extra_radios = []
        radios = []
        tracks = []
        try:
            radios = [ x.strip() for x in config['radios'].get(str(chan)).split(',') ]
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
        
        