#!/usr/bin/env python3

import asyncio
import websockets
import json
import mido
import threading, queue
import configparser

q = queue.Queue()
RADIOS = set()

# parse config
config = configparser.ConfigParser()
config.read('config.ini')
uri = "ws://" + config['server'].get('ip') + ":8765"


async def register(websocket):
    RADIOS.add(websocket)
    await notify_radios()


async def unregister(websocket):
    RADIOS.remove(websocket)
    await notify_radios()

def radio_event():
    return json.dumps({"type": "RADIOS", "count": len(RADIOS)})

async def notify_radios():
    if RADIOS:  # asyncio.wait doesn't accept an empty list
        message = radio_event()
        await asyncio.wait([radio.send(message) for radio in RADIOS])
    
async def radioCommand(msg):
    if RADIOS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps({"radio": msg.channel+1, "comm": msg.note})
        await asyncio.wait([radio.send(message) for radio in RADIOS])

async def francescaServer(websocket, path):
    loop = asyncio.get_running_loop()
    await register(websocket)
    #loop.run_in_executor(None, midiIn) 
    try:
        async for msg in websocket:     
            print(msg)
            #await radioCommand()
    except websockets.ConnectionClosed:
        print("connection error")
    finally:
        await unregister(websocket)

async def hello():
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        
def midiIn():   
    with mido.open_input() as port:
        for msg in port:
            q.put(msg)
            print(q.qsize())

async def websocketSend(msg):
    async with websockets.connect(uri) as websocket:
        #while True:
        #await websocket.send(json)  
        await radioCommand(msg)

async def getQueue(debug:False):
    while True: #investigate if loop is needed
        if q.qsize() > 0:
            item = q.get()
            if debug:
                print(item)
            await websocketSend(item)
        await asyncio.sleep(0.01)

    
async def main():
    print("\nFrancesca server ON...\n")
    start_server = websockets.serve(francescaServer, config['server'].get('ip'), 8765)
    threading.Thread(target=midiIn, daemon=True).start()
    await asyncio.gather( start_server, getQueue(True) )

asyncio.run(main())
