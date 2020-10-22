import asyncio
import json

import websockets
from escpos.printer import Dummy

LOGO_IMAGE_PATH = '/home/kraken/printing/bosch-printing/bosch_logo/bosch-logo.png'

""" Dummy """
printer = Dummy()


async def print_content(websocket, path):
    # Receive
    content = await websocket.recv()
    content = json.loads(content)
    print('GOT: {}'.format(content))

    # IMAGE PART
    printer.set(align='center', bold=False)
    printer.image(img_source=LOGO_IMAGE_PATH, center=True)
    printer.ln(count=1)

    # DATETIME PART
    printer.text('Datum: {}\n'.format(content['datetime']))

    # NUMBER PART
    printer.text('Številka naročila: ')
    printer.set(align='center', bold=True)
    printer.text('{}\n'.format(content['number']))
    printer.set(align='center', bold=False)
    printer.ln(count=2)

    # ITEMS PART
    CHARS_IN_ROW = 48
    CHARS_IN_LEFT_COL = 30
    strings_to_print = []

    # Header
    LEFT_COL_HEADER = 'Ime izdelka (EAN)'
    RIGHT_COL_HEADER = 'Količina'
    spaces_in_between = CHARS_IN_ROW - len(LEFT_COL_HEADER) - len(RIGHT_COL_HEADER)
    strings_to_print.append('{}{}{}'.format(LEFT_COL_HEADER, ' '*spaces_in_between, RIGHT_COL_HEADER))

    # Items
    for item in content['items']:
        name = item['name']
        ean = str(item['ean'])
        quantity = str(item['quantity'])
        # Divide name into substrings of CHARS_IN_LEFT_COL length
        name_substrings = [name[0+i:CHARS_IN_LEFT_COL+i] for i in range(0, len(name), CHARS_IN_LEFT_COL)]
        for i, name_substring in enumerate(name_substrings):
            if i == 0:
                # First row
                spaces_in_between = CHARS_IN_ROW - len(name_substring) - len(quantity)
                strings_to_print.append('{}{}{}'.format(name_substring, ' ' * spaces_in_between, quantity))
            else:
                # Every other row
                spaces_in_between = CHARS_IN_ROW - len(name_substring)
                strings_to_print.append('{}{}'.format(name_substring, ' ' * spaces_in_between))
        # Last row (EAN)
        ean_substring = '({})'.format(ean)
        spaces_in_between = CHARS_IN_ROW - len(ean_substring)
        strings_to_print.append('{}{}'.format(ean_substring, ' ' * spaces_in_between))

    # Actually print strings_to_print with first row bold
    printer.set(align='left', bold=True)
    printer.text('{}\n'.format(strings_to_print[0]))
    printer.set(align='left', bold=False)
    for string_to_print in strings_to_print[1:]:
        printer.text('{}\n'.format(string_to_print))

    printer.set(align='center', bold=False)
    printer.ln(count=3)

    # QR PART
    printer.text('Tole je vaš kod za naročilo\n')
    printer.qr(content=str(content['number']), size=8, native=False, center=True)

    # CUT
    printer.cut()

    # Print to file
    with open('output.prn', 'wb') as file:
        file.write(printer.output)

start_server = websockets.serve(print_content, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
