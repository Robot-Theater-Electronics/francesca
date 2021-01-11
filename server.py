import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
import asyncio
import mido
import configparser

import datetime

#q = queue.Queue()
queue = asyncio.Queue()
RADIOS = []


######################
## Aiohttp Handlers ##
######################
@aiohttp_jinja2.template('base.html')
async def handle(request):
    title = "Francesca Woodman's Alarm Clocks Server"
    time = datetime.datetime.now()
    return {'title': title, 'current_date': time, 'radios': RADIOS, 'connected': len(RADIOS) }
   
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    RADIOS.append(ws)    
        
    async for msg in ws:
        print('ws server ms:', msg)
        for _ws in RADIOS:
            await _ws.send_json(msg.data)
            
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    RADIOS.remove(ws)
    for _ws in RADIOS:
        await _ws.send_str('disconected')

    return ws

##########
## MIDI ##
##########

def midiIn():   
    with mido.open_input() as port:
        for msg in port:
            queue.put_nowait(msg)
            print('queue size: ', queue.qsize())
            
async def getQueue(debug:False):
    while True: #investigate if loop is needed
        if queue.qsize() > 0:
            item = await queue.get()
            if debug:
                print('queue item: ', item)
            await radioCommand(item)
        await asyncio.sleep(0.01)            

async def radioCommand(msg):
        session = aiohttp.ClientSession()
        async with session.ws_connect("http://0.0.0.0:8080/ws") as ws:
            #while True:
            #await websocket.send(json)
            #json = json.dumps({"radio": msg.channel+1, "comm": msg.note})
            await ws.send_json({"radio": msg.channel+1, "comm": msg.note})      
            queue.task_done()
        

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/ws', websocket_handler),
                web.static('/js', 'js')
                ]) 

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader("templates")
)

if __name__ == '__main__':
    #threading.Thread(target=midiIn, daemon=True).start()
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, midiIn)
    asyncio.run_coroutine_threadsafe(getQueue(True), loop)
    web.run_app(app)