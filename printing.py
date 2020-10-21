import asyncio

import websockets
from escpos.printer import Serial

""" 9600 Baud, 8N1, Flow Control Enabled """
p = Serial(devfile='/dev/ttyUSB0',
           baudrate=19200,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True)


async def print_content(websocket, path):
    # Receive
    content = await websocket.recv()
    print('GOT: {}'.format(content))

    # Print
    p.text("Tole je vas kod za narocilo\n")
    p.qr(str(content), size=8, native=True)
    p.cut()
    print('PRINTING: {}'.format(content))

start_server = websockets.serve(print_content, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
