import asyncio
import json
import websockets
import time

USERS = {}

def rmsg(state, msg):
    return json.dumps({'state':state, 'msg':msg})

async def connect(username, websocket):
    print('connect')
    USERS[username] = websocket
    await USERS[username].send(rmsg('ok', 'connected'))
    if '*_temp' in USERS:
        del USERS['*_temp']

async def disconnect(username):
    if username in USERS:
        await USERS[username].send(rmsg('ok', 'disconnected'))
        del USERS[username]
    else:
        print('no such user')
    if '*_temp' in USERS:
        del USERS['*_temp']

async def notify(username):
    if username in USERS:
        user = USERS[username]
        await user.send(rmsg('ok', 'new'))
    else:
        print('no such user')

async def temp(websocket):
    USERS['*_temp'] = websocket

async def handle(websocket, path):
    await temp(websocket)
    try:
        await websocket.send(rmsg('ok', 'server online'))
        async for message in websocket:
            body = json.loads(message)        

            action = body['action']
            data = body['data']
            print(time.strftime("%Y-%m-%d %H:%M:%S: ", time.localtime()), body)

            if action == 'connect':
                await connect(data, websocket)
            elif action == 'disconnect':
                await disconnect(data)
            elif action == 'new':
                await notify(data)
            else:
                print(rmsg('fail', 'no such action'))
    except Exception as e:
        # print(e)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': no action or data')
        await websocket.send(rmsg('fail', 'handle error'))
    finally:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': disconnect')
        # await disconnect(data)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), USERS)
        
        

start_server = websockets.serve(handle, '10.104.198.199', 6789)
# start_server = websockets.serve(handle, '172.18.32.97', 6789)
# start_server = websockets.serve(handle, '172.19.39.66', 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()