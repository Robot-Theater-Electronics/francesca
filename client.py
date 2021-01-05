#!/usr/bin/env python3

# WS client example

import asyncio
import socket
import websockets
import json

async def woodmanClient():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        msg = json.dumps({"client": socket.gethostname()})
        await websocket.send(msg)
        
        try:
            async for message in websocket:
                print(message)
        finally:
            print("websoket connection closed")
            

asyncio.get_event_loop().run_until_complete(woodmanClient())