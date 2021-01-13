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
RADIOS = 0
REMOTES = {}


######################
## Aiohttp Handlers ##
######################
@aiohttp_jinja2.template('base.html')
async def handle(request):
    title = "Francesca Woodman's Alarm clocks Server"
    time = datetime.datetime.now()
    return {'title': title, 'current_date': time, 'radios': REMOTES, 'connected': len(REMOTES) }
   
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    if request.remote not in REMOTES:
        if 'Origin' in request.headers:
            REMOTES['web'] = ws
        else: 
            REMOTES[request.remote] = ws
    
    RADIOS = len(REMOTES)
    
    async for msg in ws:
        print('ws server msg:', msg)
        for _ws in REMOTES:
            try:
                await REMOTES[_ws].send_str(msg.data)
            except ConnectionResetError:
                await REMOTES[_ws].close()
                print('on send', ConnectionResetError)
            
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    closed = []
    #if request.remote in REMOTES:
    #REMOTES.pop(request.remote)
    for _ws in REMOTES:
        if REMOTES[_ws].closed:
            #await REMOTES[_ws].send_json({'type': "disconnected", 'ip': _ws})
            await REMOTES[_ws].close()
            closed.append(_ws)
            #print(len(REMOTES))
            #print(REMOTES[_ws].closed)
        #except ConnectionResetError:
            #await REMOTES[_ws].send_json({'type': "disconnected", 'ip': _ws})
            #await REMOTES[_ws].close()
            #pop = _ws
            #print('on remove', ConnectionResetError)
    
    for c in closed:
        if c == '127.0.0.1':
            RADIOS -= 1
        REMOTES.pop(c) 

    if len(REMOTES) < RADIOS:    
        # notify the web interface 
        if 'web' in REMOTES:
            connected_radios = list(REMOTES)
            connected_radios.remove('web')
            await REMOTES['web'].send_json({'type': "alive", 'radios': connected_radios})
    
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
            await ws.send_json({"radio": msg.channel+1, "comm": msg.note, "extra_radios": msg.velocity })      
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