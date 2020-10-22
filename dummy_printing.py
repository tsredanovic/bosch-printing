import asyncio
import json

import websockets
from escpos.printer import Dummy

""" Dummy """
my_printer_def = Dummy()


async def print_content(websocket, path):
    # Receive
    content = await websocket.recv()
    content = json.loads(content)
    print('GOT: {}'.format(content))

    # Align text
    my_printer_def.set(align='center')
    # Print items part
    for item in content['items']:
        my_printer_def.text('{} {}\n'.format(item['ean'], item['quantity']))
    # Print QR part
    my_printer_def.text('Tole je vas kod za narocilo\n')
    my_printer_def.qr(content=str(content['number']), size=8, native=False, center=True)
    my_printer_def.cut()
    with open('output.prn', 'wb') as file:
        file.write(my_printer_def.output)

start_server = websockets.serve(print_content, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
