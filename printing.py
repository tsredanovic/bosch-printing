import asyncio
import json

import websockets
from escpos.printer import Serial

""" 9600 Baud, 8N1, Flow Control Enabled """
printer = Serial(devfile='/dev/ttyUSB0',
                 baudrate=19200,
                 bytesize=8,
                 parity='N',
                 stopbits=1,
                 timeout=1.00,
                 dsrdtr=True)


async def print_content(websocket, path):
    # Receive
    content = await websocket.recv()
    content = json.loads(content)
    print('GOT: {}'.format(content))

    # Align text
    printer.set(align='center')
    # Print datetime part
    printer.text('Datum: {}\n'.format(content['datetime']))
    printer.ln(count=2)
    # Print number part
    printer.text('Številka naročila: {}\n'.format(content['number']))
    printer.ln(count=2)
    # Print items part
    for item in content['items']:
        printer.text('{} ({}) - {}\n'.format(item['name'], item['ean'], item['quantity']))
    printer.ln(count=4)
    # Print QR part
    printer.text('Tole je vas kod za narocilo\n')
    printer.ln(count=2)
    printer.qr(content=str(content['number']), size=8, native=False, center=True)
    printer.cut()

start_server = websockets.serve(print_content, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
