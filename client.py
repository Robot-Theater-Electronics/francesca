import asyncio
import json
import configparser
import aiohttp
import socket
from player import Player

# parse config
config = configparser.ConfigParser()
config.read('config.ini')
ip = config['server'].get('ip')
uri = f'http://{ip}:8080/ws'

hostname = socket.gethostname()
current_command = -1
player = Player(hostname)

async def woodmanClient(debug=False):
    
    session = aiohttp.ClientSession()
    
    async with session.ws_connect(uri) as ws:
        
        await ws.send_json(hostname)

        async for msg in ws:
            
            if msg.data != 'disconected':
                decoded = msg.json()
                if 'comm' in decoded:
                    player.play(decoded['radio'], 
                                decoded['comm'],
                                decoded['extra_radios'], True)
                if debug:
                    print(msg)

            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break

    
loop = asyncio.get_event_loop()
loop.run_until_complete(woodmanClient(True))