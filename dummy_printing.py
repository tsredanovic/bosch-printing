import asyncio
import json

import websockets
from escpos.printer import Dummy

""" Dummy """
printer = Dummy()


async def print_content(websocket, path):
    # Receive
    content = await websocket.recv()
    content = json.loads(content)
    print('GOT: {}'.format(content))

    # Align text
    printer.set(align='center', bold=False)
    # Print datetime part
    printer.text('Datum: {}\n'.format(content['datetime']))
    printer.ln(count=1)
    # Print number part
    printer.text('Številka naročila: ')
    printer.set(align='center', bold=True)
    printer.text('{}\n'.format(content['number']))
    printer.set(align='center', bold=False)
    printer.ln(count=2)
    # Print items part
    for item in content['items']:
        printer.text('{} ({}) - {}\n'.format(item['name'], item['ean'], item['quantity']))
    printer.ln(count=3)
    # Print QR part
    printer.text('Tole je vas kod za narocilo\n')
    printer.qr(content=str(content['number']), size=8, native=False, center=True)
    printer.cut()

    # Print to file
    with open('output.prn', 'wb') as file:
        file.write(printer.output)

start_server = websockets.serve(print_content, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
