def print_image_part(printer, image_path):
    printer.set(align='center', bold=False)
    printer.image(img_source=image_path, center=True)
    printer.ln(count=1)


def print_datetime_part(printer, datetime):
    printer.text('Datum: {}\n'.format(datetime))


def print_number_part(printer, number):
    printer.text('Številka naročila: ')
    printer.set(align='center', bold=True)
    printer.text('{}\n'.format(number))
    printer.set(align='center', bold=False)
    printer.ln(count=2)


def print_items_part(printer, items_text_lines):
    printer.set(align='left', bold=True)
    printer.text('{}\n'.format(items_text_lines[0]))
    printer.set(align='left', bold=False)
    for string_to_print in items_text_lines[1:]:
        printer.text('{}\n'.format(string_to_print))

    printer.set(align='center', bold=False)
    printer.ln(count=3)


def print_qr_part(printer, number):
    printer.text('Tole je vaš kod za naročilo\n')
    qr_string = 'Številka naročila: {}'.format(number)
    printer.qr(content=qr_string, size=10, native=True, center=False)
