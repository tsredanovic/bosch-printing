import asyncio
import json

import websockets


async def hello():
    uri = "ws://localhost:5555"
    async with websockets.connect(uri) as websocket:
        payload = {
            "number": 69,
            "datetime": "22-10-2020 12:69",
            "items": [
                {
                    "ean": 1,
                    "quantity": 3,
                    "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                },
                {
                    "ean": 2,
                    "quantity": 1,
                    "name": "Sharaf"
                }
            ]
        }
        payload_json = json.dumps(payload)

        await websocket.send(payload_json)
        print('Sent: {}'.format(payload_json))

asyncio.get_event_loop().run_until_complete(hello())
