#!/usr/bin/env python3

# WS client example

import asyncio
import socket
import websockets
import json
import configparser
import threading
from pydub import AudioSegment
from pydub.playback import play

# parse config
config = configparser.ConfigParser()
config.read('config.ini')
uri = "ws://" + config['server'].get('ip') + ":8765"
music = config['midi_to_music']
hostname = socket.gethostname();

async def woodmanClient(debug=False):
    async with websockets.connect(uri) as websocket:
        msg = json.dumps({"client": hostname})
        await websocket.send(msg)
        
        try:
            async for msg in websocket:
                decoded = json.loads(msg)
                if 'comm' in decoded:
                    threading.Thread(target=player, args=(decoded['radio'], decoded['comm'])).start()
                if debug:
                    print(msg)
                
        finally:
            print("websoket connection closed")
            

def player(radio, num):
    if config['radios'].get(str(radio)) == hostname:
        try:
            sound = AudioSegment.from_file("music_files/" + music.get(str(num)), format="wav")
            play(sound)
        finally:
            print("error")
    

asyncio.get_event_loop().run_until_complete(woodmanClient(True))