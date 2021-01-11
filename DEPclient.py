#!/usr/bin/env python3

# WS client example

import asyncio
import socket
import websockets
import json
import configparser
from player import Player
#import threading

# parse config
config = configparser.ConfigParser()
config.read('config.ini')
uri = "ws://" + config['server'].get('ip') + ":8080/ws"

hostname = socket.gethostname()
current_command = -1
player = Player(hostname, config)

async def woodmanClient(debug=False):
    try:
        async with websockets.connect(uri) as websocket:
            msg = json.dumps({"client": hostname})
            await websocket.send(msg)
            
            try:
                async for msg in websocket:
                    decoded = json.loads(msg)
                    if 'comm' in decoded:
                        player.play(decoded['radio'], decoded['comm'], True)
                    if debug:
                        print(msg)
            except websockets.ConnectionClosed:
                print("connection error")             
            finally:
                print("websoket connection closed, trying to reconnect...")

    except ConnectionRefusedError:
        print("server not booted")
    finally:
        await asyncio.sleep(0.2)
            
    

asyncio.get_event_loop().run_until_complete(woodmanClient(True))