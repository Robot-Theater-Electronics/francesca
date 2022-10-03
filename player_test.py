""" 
The player class for Francesca Woodman. Plays and stops wav files. That's it.
"""            
from pygame import mixer as m
import configparser

m.init()
m.music.load("/media/mnt/1")
m.music.play()
        
        