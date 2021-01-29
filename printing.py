import asyncio
import json
from datetime import datetime

import websockets
from escpos.printer import Serial

from printing_parts import *

LOGO_IMAGE_PATH = '/home/kraken/printing/bosch-printing/bosch_logo/bosch-logo.png'

# Init printer with: 9600 Baud, 8N1, Flow Control Enabled
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
    print("GOT at: {}", datetime.now().time())

    # IMAGE PART
    print_image_part(printer, LOGO_IMAGE_PATH)
    print("Image done at: {}", datetime.now().time())
    # DATETIME PART
    print_datetime_part(printer, content['datetime'])
    print("Datetime done at: {}", datetime.now().time())
    # NUMBER PART
    print_number_part(printer, content['number'])
    print("Number done at: {}", datetime.now().time())
    # ITEMS PART
    print_items_part(printer, content['items'])
    print("Items done at: {}", datetime.now().time())
    # QR PART
    print_qr_part(printer, content['number'])
    print("QR done at: {}", datetime.now().time())
    # CUT
    printer.cut()
    print("CUT done at: {}", datetime.now().time())

start_server = websockets.serve(print_content, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
