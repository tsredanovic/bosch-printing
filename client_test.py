import asyncio
import websockets


async def hello():
    uri = "ws://localhost:5555"
    async with websockets.connect(uri) as websocket:
        name = input('What to send: ')

        await websocket.send(name)
        print('Sent: {}'.format(name))

        greeting = await websocket.recv()
        print('Got: {}'.format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
