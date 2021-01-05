#!/usr/bin/env python3

# WS client example

import asyncio
import socket
import websockets
import json
import configparser
from pydub import AudioSegment
from pydub.playback import play

# parse config
config = configparser.ConfigParser()
config.read('config.ini')
uri = "ws://" + config['server'].get('ip') + ":8765"
music = config['midi_to_music']
hostname = socket.gethostname();

async def woodmanClient():
    async with websockets.connect(uri) as websocket:
        msg = json.dumps({"client": hostname})
        await websocket.send(msg)
        
        try:
            async for msg in websocket:
                decoded = json.loads(msg)
                if 'comm' in decoded:
                    player(decoded['radio'], decoded['comm'])
                    
                    print(msg, comm, radio)
                else:
                    print(msg)
                
        finally:
            print("websoket connection closed")
            

def player(radio, num):
    if config['radios'].get(radio) == hostname:
        sound = AudioSegment.from_file(music.get(num), format="wav")
        play(sound)
    

asyncio.get_event_loop().run_until_complete(woodmanClient())