import asyncio
import json
import configparser
import aiohttp
import socket
import subprocess
import time
import os
from player import Player

# parse config
working_dir = os.getcwd()
config = configparser.ConfigParser()
config.read(f'{working_dir}/config.ini')
ip = config['server'].get('ip')
uri = f'http://{ip}:8080/ws'

hostname = socket.gethostname()
current_command = -1
player = Player(hostname, working_dir)
connected = False

async def woodmanClient(debug=False):
    while not connected:
        session = aiohttp.ClientSession()
        try:
            
            await websocket(session, debug)
            
        except aiohttp.client_exceptions.ClientConnectorError:
            print("reconnecting..")
            await session.close()

        time.sleep(1)
        

async def websocket(session=None, debug=False):
    async with session.ws_connect(uri) as ws:
        connected = True
        await ws.send_json({'type': "conn", 'hostname': hostname})
    
        async for msg in ws:
            
            if msg.type == aiohttp.WSMsgType.TEXT:
                decoded = msg.json()
                if 'comm' in decoded:
                    player.play(decoded['radio'], 
                                decoded['comm'],
                                decoded['extra_radios'], True)
                    if player._error != '':
                        await ws.send_json({'type': "error", 'hostname': hostname, 'msg': player._error})
                        player._error = ''
                    
                if 'bash' in decoded:
                    if decoded['bash'] == 'pull':
                        git = subprocess.run(f'{working_dir}/gitpull.sh', capture_output=True)
                        await ws.send_json({'type': "bash", 'hostname': hostname, 'msg': git.stdout.decode('utf-8').strip()})
                    
                if debug:
                    print(msg)
    
            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break    
    
loop = asyncio.get_event_loop()
loop.run_until_complete(woodmanClient(True))