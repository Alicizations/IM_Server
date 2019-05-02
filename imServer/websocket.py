import asyncio
import json
import websockets

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
            print(body, action, data)

            if action == 'connect':
                await connect(data, websocket)
            elif action == 'disconnect':
                await disconnect(data)
            elif action == 'new':
                await notify(data)
            else:
                print(rmsg('fail', 'no such action'))
    except Exception as e:
        print(e)
        await websocket.send(rmsg('fail', 'handle error'))
    finally:
        print('disconnect')
        print(USERS)
        # await disconnect(data)
        

start_server = websockets.serve(handle, '10.104.198.199', 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()